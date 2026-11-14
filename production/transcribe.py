from faster_whisper import WhisperModel
import glob,json,os,subprocess,numpy as np
m=WhisperModel('tiny.en',device='cpu',compute_type='int8',download_root='work/models',cpu_threads=3)
result={}
for p in sorted(glob.glob('/workspace/attachments/*/*.ogg'))+['work/intro.mp3']:
 segs,info=m.transcribe(np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',p,'-f','f32le','-ac','1','-ar','16000','-']),dtype=np.float32),word_timestamps=True,beam_size=3)
 result[p]=[{'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word} for w in s.words]} for s in segs]
 print(os.path.basename(p),flush=True);json.dump(result,open('work/transcription.json','w'),indent=2)
