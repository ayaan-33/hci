"""Replace the opening, preserving the approved body video's encoded frames."""
import argparse,subprocess,json,hashlib,os,wave,array
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--original',required=True,type=Path);p.add_argument('--narration',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
root=Path(os.environ.get('EDITORIAL_FULL_WORK',str(Path(__file__).parent/'build')))
def run(cmd):return subprocess.run(cmd,check=True,capture_output=True,text=True).stdout

def probe(path):return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def vstream(path):return next(s for s in probe(path)['streams'] if s['codec_type']=='video')
def video_hash(path,seek=None):
 cmd=['ffmpeg','-v','error']
 if seek is not None:cmd+=['-ss',str(seek)]
 cmd+=['-i',str(path),'-map','0:v:0','-an','-c:v','copy','-bsf:v','filter_units=remove_types=6|7|8|9','-f','hash','-hash','sha256','-']
 return run(cmd).strip()
old=vstream(a.original)
assert (old['width'],old['height'],old['r_frame_rate'],int(old['nb_frames']))==(3840,1920,'30/1',13818)
# This approved source has an authored scene cut and keyframe at exactly 18 s.
run(['ffmpeg','-y','-v','error','-ss','18','-i',str(a.original),'-map','0:v:0','-an','-c:v','copy',str(root/'body-unchanged.mp4')])
assert int(vstream(root/'body-unchanged.mp4')['nb_frames'])==13278
assert int(vstream(root/'birthday-opening.mp4')['nb_frames'])==1050
run(['ffmpeg','-y','-v','error','-i',str(root/'birthday-opening.mp4'),'-map','0:v:0','-an','-c:v','copy',str(root/'opening-video.mp4')])
with wave.open(str(root/'assembled-narration.wav'),'wb') as dest:
 dest.setnchannels(2);dest.setsampwidth(2);dest.setframerate(48000)
 with wave.open(str(root/'opening-mix.wav'),'rb') as src:
  assert (src.getnchannels(),src.getsampwidth(),src.getframerate(),src.getnframes())==(2,2,48000,1680000)
  dest.writeframes(src.readframes(src.getnframes()))
 with wave.open(str(a.narration),'rb') as src:
  assert src.getframerate()==48000 and src.getsampwidth()==2
  src.setpos(18*48000)
  while data:=src.readframes(48000):
   if src.getnchannels()==1:
    samples=array.array('h');samples.frombytes(data);stereo=array.array('h',(v for x in samples for v in (x,x)));data=stereo.tobytes()
   else:assert src.getnchannels()==2
   dest.writeframes(data)
(root/'final.ffconcat').write_text(f"file '{root/'opening-video.mp4'}'\nfile '{root/'body-unchanged.mp4'}'\n")
run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(root/'final.ffconcat'),'-i',str(root/'assembled-narration.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t','477.6','-movflags','+faststart',str(a.output)])
v=vstream(a.output);assert (int(v['nb_frames']),v['width'],v['height'])==(14328,3840,1920)
assert abs(float(probe(a.output)['format']['duration'])-477.6)<.05
oldhash=video_hash(root/'body-unchanged.mp4');newhash=video_hash(a.output,35)
assert oldhash==newhash,(oldhash,newhash)
print('Approved presentation encoded video hash preserved:',oldhash,flush=True)
decode=subprocess.run(['ffmpeg','-v','error','-i',str(a.output),'-f','null','-'],capture_output=True,text=True)
assert decode.returncode==0 and not decode.stderr,decode.stderr
assert a.output.stat().st_size<100*1024*1024
report={'file':a.output.name,'durationSeconds':477.6,'width':3840,'height':1920,'fps':'30/1','frames':14328,'openingSeconds':35,'originalOpeningSeconds':18,'approvedBodyFrames':13278,'approvedBodyVideoBitstreamPreserved':True,'bodyVideoVclHash':oldhash,'fullDecode':'passed','bytes':a.output.stat().st_size,'sha256':hashlib.sha256(a.output.read_bytes()).hexdigest(),'openingNativeRender':[1920,960],'openingStyle':'Approved dark editorial 2.5D; custom Cycles 3D assets, separate moving lid and van, depth-driven camera motion','syntheticVoice':'Opening narrator and confirmation system only'}
pcm_old=hashlib.sha256();pcm_new=hashlib.sha256()
with wave.open(str(a.narration),'rb') as src:
 src.setpos(18*48000)
 while data:=src.readframes(48000):
  if src.getnchannels()==1:
   vals=array.array('h');vals.frombytes(data);data=array.array('h',(y for x in vals for y in (x,x))).tobytes()
  pcm_old.update(data)
with wave.open(str(root/'assembled-narration.wav'),'rb') as src:
 src.setpos(35*48000)
 while data:=src.readframes(48000):pcm_new.update(data)
assert pcm_old.hexdigest()==pcm_new.hexdigest()
report.update({'originalNarrationPcmPreserved':True,'narrationBodyPcmSha256':pcm_old.hexdigest()})
a.output.with_name(a.output.stem+'-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
