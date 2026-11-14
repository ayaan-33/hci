import numpy as np,wave,subprocess
sr=48000;t=np.arange(sr*20)/sr
fx=(np.sin(2*np.pi*85*t)+.4*np.sin(2*np.pi*170*t))*.009*np.minimum(t,1)*np.clip((13-t)/2,0,1)
def tone(start,dur,f0,f1,amp):
 n=int(sr*dur);q=np.arange(n)/sr;sig=np.sin(2*np.pi*(f0*q+(f1-f0)*q*q/(2*dur)))*np.sin(np.pi*q/dur)**2*amp;i=int(start*sr);fx[i:i+n]+=sig
for st in [3.2,3.65]:tone(st,.18,1100,2000,.055)
tone(5.5,.13,900,900,.05);tone(5.7,.17,1350,1350,.05)
tone(9.7,.28,550,230,.07)
tone(14,.32,180,700,.04)
with wave.open('/workspace/work/v2/effects.wav','wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(fx,-1,1)*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-y','-v','error','-i','/workspace/work/intro.mp3','-i','/workspace/work/v2/effects.wav','-filter_complex','[0:a][1:a]amix=inputs=2:duration=longest:normalize=0[a]','-map','[a]','-c:a','pcm_s16le','-ar','48000','/workspace/work/v2/intro-soundtrack.wav'],check=True)
