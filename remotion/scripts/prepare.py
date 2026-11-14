#!/usr/bin/env python3
"""Bounded-memory media preparation: original voices -> PCM master, librosa features,
caption cues and source-PTS-aligned silent demo plates. No network calls or API keys.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, shutil, subprocess, sys, wave
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('NUMBA_CACHE_DIR',str(ROOT/'.cache/numba'))
import librosa
FPS=30; SR=48000; HOP=SR//FPS; NFFT=4096; OPEN=18; END=8
GEN=ROOT/'public/generated'; CACHE=ROOT/'.cache/prepare'; ASSETS=ROOT/'public/assets'

def run(args: list[str], *, capture=False):
 result=subprocess.run([str(a) for a in args],stdout=subprocess.PIPE if capture else subprocess.DEVNULL,stderr=subprocess.PIPE)
 if result.returncode:raise RuntimeError(f'Command failed: {args[0]}\n{result.stderr.decode(errors="replace")[-5000:]}')
 return result

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
 return h.hexdigest()

def probe(path):return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path],capture=True).stdout)

def decode_audio(path, audio_filter=None):
 args=['ffmpeg','-v','error','-i',path,'-vn']
 if audio_filter:args+=['-af',audio_filter]
 args+=['-ac','1','-ar',str(SR),'-f','f32le','-']
 return np.frombuffer(run(args,capture=True).stdout,dtype='<f4').copy()

def normalized_audio(path, target):
 signature=sha(path)+str(target)
 dst=CACHE/(hashlib.sha256(signature.encode()).hexdigest()[:20]+'.npy')
 if dst.exists():return np.load(dst,allow_pickle=False)
 if target is None:y=decode_audio(path)
 else:
  measure=run(['ffmpeg','-hide_banner','-i',path,'-af',f'loudnorm=I={target}:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture=True)
  stderr=measure.stderr.decode();i=stderr.rfind('{');j=stderr.rfind('}');values=json.loads(stderr[i:j+1])
  if not all(math.isfinite(float(values[k])) for k in ['input_i','input_tp','input_lra','input_thresh','target_offset']):raise ValueError(f'Cannot normalize silent or invalid recording: {path}')
  filt=f"loudnorm=I={target}:TP=-1.5:LRA=11:measured_I={values['input_i']}:measured_TP={values['input_tp']}:measured_LRA={values['input_lra']}:measured_thresh={values['input_thresh']}:offset={values['target_offset']}:linear=true"
  y=decode_audio(path,filt)
 if not np.isfinite(y).all():raise ValueError(f'Non-finite PCM in {path}')
 np.save(dst,y,allow_pickle=False);return y

def smooth(x,attack=.04,release=.18):
 out=np.zeros_like(x);last=0.
 for i,v in enumerate(x):
  tau=attack if v>last else release;last+=(1-math.exp(-1/(FPS*tau)))*(v-last);out[i]=last
 return out

def extract_features(y):
 """Voice-only analysis. Normalise each file independently, not the music/master."""
 rms=librosa.feature.rms(y=y,frame_length=NFFT,hop_length=HOP,center=True)[0]
 active=20*np.log10(np.maximum(rms,1e-9))>-45
 spec=np.abs(librosa.stft(y,n_fft=NFFT,hop_length=HOP,window='hann',center=True,pad_mode='constant'))**2
 freq=librosa.fft_frequencies(sr=SR,n_fft=NFFT)
 def norm_db(v):
  db=10*np.log10(np.maximum(v,1e-12));lo,hi=np.percentile(db[active],[10,95]) if active.any() else (0,0)
  if hi-lo<1e-6:return np.zeros_like(db)
  return smooth(np.clip((db-lo)/(hi-lo),0,1)*active)
 amplitude=norm_db(rms**2);bands=[norm_db(spec[(freq>=lo)&(freq<hi)].mean(axis=0)) for lo,hi in [(80,250),(250,2000),(2000,8000)]]
 high=bands[2];onsets=[];last=-12
 for i in range(1,len(high)):
  if high[i]>.65 and high[i]-high[i-1]>.18 and i-last>=12:onsets.append(i);last=i
 values=np.column_stack([amplitude,*bands]).round(4).tolist()
 return {'hopSamples':HOP,'windowSamples':NFFT,'bandsHz':[[80,250],[250,2000],[2000,8000]],'values':values,'onsets':onsets}

def write_pcm(writer,y):writer.writeframes((np.clip(y,-.999,.999)*32767).astype('<i2').tobytes())

def intro_sound():
 t=np.arange(OPEN*SR)/SR;envelope=np.minimum(t/2,1)*np.clip((OPEN-t)/3,0,1)
 y=.006*(np.sin(2*np.pi*56*t)+.25*np.sin(2*np.pi*112*t))*envelope
 for start,freq in [(1.5,420),(4,630),(8.5,540),(14,840)]:
  n=int(.28*SR);q=np.arange(n)/SR;v=.026*np.sin(2*np.pi*freq*q)*np.sin(np.pi*q/.28)**2;idx=int(start*SR);y[idx:idx+n]+=v
 return y.astype(np.float32)

def video_ok(path,frames):
 try:
  v=next(s for s in probe(path)['streams'] if s['codec_type']=='video')
  return int(v.get('nb_frames',-1))==frames and abs(float(v.get('start_time',0)))<.01 and v['width']==2320 and v['height']==1582
 except (Exception,StopIteration):return False

def hold_image(src,piece):
 key='n'+str(piece['holdFrame']) if 'holdFrame' in piece else 't'+str(piece['holdTime'])
 dst=CACHE/(src.stem+'-'+sha(src)[:10]+'-'+key+'.png')
 if not dst.exists():
  if 'holdFrame' in piece:
   filt=f"select=eq(n\\,{piece['holdFrame']}),crop=2320:1582:352:0"
   run(['ffmpeg','-y','-v','error','-i',src,'-vf',filt,'-frames:v','1','-pix_fmt','rgba',dst])
  else:run(['ffmpeg','-y','-v','error','-ss',str(piece['holdTime']),'-i',src,'-vf','crop=2320:1582:352:0','-frames:v','1','-pix_fmt','rgba',dst])
 return dst

def conform_demo(key,info):
 src=ASSETS/'demos'/info['source'];sig=hashlib.sha256((sha(src)+json.dumps(info,sort_keys=True)+'conform-v1').encode()).hexdigest()[:20]
 dst=GEN/'demos'/f'{key}.mp4';stamp=dst.with_suffix('.stamp');dst.parent.mkdir(parents=True,exist_ok=True)
 if dst.exists() and stamp.exists() and stamp.read_text()==sig and video_ok(dst,info['frames']):return dst
 pieces=[];cursor=0
 for index,piece in enumerate(info['pieces']):
  if piece['from']!=cursor:raise ValueError(f'Gap in demo map {key} at {cursor}')
  count=piece['to']-piece['from'];cursor=piece['to'];part=CACHE/f'{key}-{sig}-{index}.mp4';pieces.append(part)
  if video_ok(part,count):continue
  args=['ffmpeg','-y','-v','error','-threads','2','-filter_threads','2']
  if 'sourceStart' in piece:
   a,b=piece['sourceStart'],piece['sourceEnd'];ratio=(count/FPS)/(b-a)
   args+=['-ss',str(a),'-t',str(b-a),'-i',src];filt=f'crop=2320:1582:352:0,setpts=(PTS-STARTPTS)*{ratio:.12f},fps=30:round=near'
  else:args+=['-loop','1','-framerate','30','-i',hold_image(src,piece)];filt='fps=30'
  filt+=f',tpad=stop_mode=clone:stop_duration=1,trim=end_frame={count},setpts=N/(30*TB),format=yuv420p'
  args+=['-vf',filt,'-an','-frames:v',str(count),'-r','30','-fps_mode','cfr','-c:v','libx264','-preset','veryfast','-crf','18','-g','60','-threads','2','-video_track_timescale','30000','-movflags','+faststart',part]
  print(f'  {key}: piece {index+1}/{len(info["pieces"])} ({count} frames)',flush=True);run(args)
  if not video_ok(part,count):raise ValueError(f'Invalid conformed piece: {part}')
 if cursor!=info['frames']:raise ValueError(f'Incomplete {key} map')
 listing=CACHE/f'{key}-{sig}.ffconcat'
 def quote(p):return str(p.resolve()).replace('\\','/').replace("'","'\\''")
 listing.write_text(''.join(f"file '{quote(p)}'\n" for p in pieces))
 run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',listing,'-c:v','copy','-an','-movflags','+faststart',dst])
 if not video_ok(dst,info['frames']):raise ValueError(f'Unexpected duration/frame count in {dst}')
 stamp.write_text(sig);return dst

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--skip-demos',action='store_true');ap.add_argument('--no-normalize',action='store_true');ap.add_argument('--no-intro-sound',action='store_true');args=ap.parse_args()
 for executable in ['ffmpeg','ffprobe']:
  if not shutil.which(executable):raise SystemExit(f'{executable} not found. Install FFmpeg 6+ and add it to PATH.')
 GEN.mkdir(parents=True,exist_ok=True);CACHE.mkdir(parents=True,exist_ok=True)
 integrity=json.loads((ROOT/'src/data/source-integrity.json').read_text())
 for relative,expected in integrity.items():
  path=ROOT/'public'/relative
  if not path.exists() or sha(path)!=expected:raise ValueError(f'Original source asset differs: {relative}. The cue map is authored for the supplied takes. See README before replacing recordings.')
 script=json.loads((ROOT/'src/data/script.json').read_text());board=json.loads((ROOT/'src/data/storyboard.json').read_text());demo_map=json.loads((ROOT/'src/data/demo-map.json').read_text());sections=[];offset=OPEN*SR;fingerprint=hashlib.sha256();fingerprint.update(Path(__file__).read_bytes())
 for p in sorted((ROOT/'src/data').glob('*.json')):fingerprint.update(p.read_bytes())
 master=GEN/'narration.wav'
 with wave.open(str(master),'wb') as writer:
  writer.setnchannels(1);writer.setsampwidth(2);writer.setframerate(SR)
  write_pcm(writer,np.zeros(OPEN*SR,np.float32) if args.no_intro_sound else intro_sound())
  for row in script:
   key=row['id'];src=ASSETS/'audio'/f'{key}.ogg'
   if not src.exists():raise SystemExit(f'Missing {src}. Run import-assets.py or follow README folder structure.')
   original=decode_audio(src)
   if len(original)!=row['samples']:raise ValueError(f'{key} sample count changed ({len(original)} vs {row["samples"]}). Update the authored timing/captions before using a replacement take.')
   print(f'Analysing {key}: {len(original)/SR:.6f}s',flush=True);fingerprint.update(sha(src).encode())
   voice=normalized_audio(src,None if args.no_normalize else -16)
   if abs(len(voice)-len(original))>HOP:raise ValueError(f'Normalization changed timing in {key}')
   voice=np.pad(voice,(0,max(0,len(original)-len(voice))))[:len(original)]
   start_frame=round(offset/SR*FPS);end_frame=round((offset+len(voice))/SR*FPS)
   if board[key][-1]['end']!=end_frame-start_frame:raise ValueError(f'Authored motion does not cover {key}')
   sections.append({'id':key,'speaker':row['speaker'],'title':row['title'],'audioStartSamples':offset,'audioEndSamples':offset+len(voice),'startFrame':start_frame,'endFrame':end_frame,'features':extract_features(original),'captions':row['captions']})
   write_pcm(writer,voice);offset+=len(voice)
  picture_frames=round((offset/SR+END)*FPS);remaining=picture_frames*HOP-offset;write_pcm(writer,np.zeros(remaining,np.float32))
 # The proof audio uses exactly the same sample positions as its picture montage.
 with wave.open(str(master),'rb') as src,wave.open(str(GEN/'proof.wav'),'wb') as out:
  out.setparams(src.getparams())
  for clip in json.loads((ROOT/'src/data/proof-clips.json').read_text()):src.setpos(clip['start']*HOP);out.writeframes(src.readframes(clip['frames']*HOP))
 demos={}
 if not args.skip_demos:
  for key,info in demo_map.items():print(f'Conforming {key} from original source timestamps',flush=True);p=conform_demo(key,info);demos[key]={'file':f'generated/demos/{key}.mp4','frames':info['frames'],'sha256':sha(p)}
 else:
  for key,info in demo_map.items():
   p=GEN/'demos'/f'{key}.mp4'
   if not video_ok(p,info['frames']):raise ValueError('--skip-demos requires the already conformed demo plates.')
   demos[key]={'file':f'generated/demos/{key}.mp4','frames':info['frames'],'sha256':sha(p)}
 srt=[];cue=0
 def tc(t):
  v=round(t*1000);return f'{v//3600000:02}:{v//60000%60:02}:{v//1000%60:02},{v%1000:03}'
 for section in sections:
  for c in section['captions']:
   cue+=1;base=section['audioStartSamples']/SR;srt.append(f'{cue}\n{tc(base+c["start"])} --> {tc(base+c["end"])}\n{c["text"]}')
 (GEN/'captions.srt').write_text('\n\n'.join(srt)+'\n')
 manifest={'schemaVersion':1,'fps':FPS,'width':3840,'height':1920,'sampleRate':SR,'durationFrames':picture_frames,'voiceEndSamples':offset,'masterSamples':picture_frames*HOP,'narration':'generated/narration.wav','fingerprint':fingerprint.hexdigest(),'sections':sections,'demos':demos,'normalization':None if args.no_normalize else {'LUFS':-16,'truePeak':-1.5,'method':'two-pass FFmpeg loudnorm'}}
 tmp=GEN/'manifest.tmp';tmp.write_text(json.dumps(manifest,separators=(',',':')));tmp.replace(GEN/'manifest.json')
 print(f'Ready: {picture_frames} frames / {picture_frames/FPS:.3f}s / 3840×1920 at 30 fps',flush=True)
if __name__=='__main__':
 try:main()
 except (RuntimeError,ValueError,FileNotFoundError) as e:raise SystemExit(str(e))
