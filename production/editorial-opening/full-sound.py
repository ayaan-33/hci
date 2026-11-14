"""Original restrained ambient score, narration, and literal delivery foley."""
from pathlib import Path
import os,wave,json
import numpy as np
BASE=Path(__file__).parent;ROOT=Path(os.environ.get('EDITORIAL_WORK',str(BASE/'build')))/'full';ROOT.mkdir(parents=True,exist_ok=True);AUDIO=BASE/'assets/audio';R=48000;D=35;out=np.zeros((R*D,2),np.float64);rng=np.random.default_rng(10)
def add(at,arr,gain=1,pan=0):
 k=round(at*R);n=min(len(arr),len(out)-k)
 if arr.ndim==1:arr=np.column_stack((arr*np.sqrt((1-pan)/2),arr*np.sqrt((1+pan)/2)))
 out[k:k+n]+=arr[:n]*gain

def tone(freq,duration=.7):
 t=np.arange(round(duration*R))/R;return (np.sin(2*np.pi*freq*t)+.15*np.sin(2*np.pi*2*freq*t))*np.minimum(1,t/.008)*np.exp(-t*6)
# Warm, quiet harmonic bed; silence at the reveal makes room for the satire.
t=np.arange(R*D)/R;env=np.minimum(1,t/1.1)*np.minimum(1,(D-t)/.4);env*=np.where((t>23)&(t<27.6),0,1)
pad=(np.sin(2*np.pi*130.8128*t)+.35*np.sin(2*np.pi*196*t)+.20*np.sin(2*np.pi*329.6276*t))*.014*env;add(0,pad)
for i in range(19):
 at=.8+i*1.16;f=[523.251,659.255,783.991,987.767][i%4];add(at,tone(f,1.1),.025,(-.25 if i%2 else .25))
# Lid close; scanning; confirmation.
tt=np.arange(round(.22*R))/R;add(4.55,rng.normal(0,1,len(tt))*np.exp(-tt*29),.023)
tt=np.arange(round(.85*R))/R;add(6.1,np.sin(2*np.pi*(490*tt+330*tt*tt))*np.sin(np.pi*tt/.85)**2,.018,-.2)
for at,f in [(13.3,880),(13.43,1320),(23.35,1046.50),(23.49,1318.51),(23.63,1567.98)]:add(at,tone(f,.6),.050)
# Quiet van/tyre sound. No loud engine competes with narration.
tt=np.arange(8*R)/R;add(15,(np.sin(2*np.pi*78*tt)*.007+rng.normal(0,1,len(tt))*.002)*np.minimum(1,tt/.5)*np.minimum(1,(8-tt)/.6),1)
# Sea air and a short gull call punctuate the failed delivery.
tt=np.arange(5*R)/R;add(23,rng.normal(0,1,len(tt)),.003)
for at in [25.55,25.91]:
 tt=np.arange(round(.27*R))/R;add(at,np.sin(2*np.pi*(1350*tt-1050*tt*tt))*np.sin(np.pi*tt/.27)**2,.038,-.35)
# Opening voices only; the body keeps the team's original continuous narration.
lines=[(.45,0),(5.15,1),(10.3,2),(15.2,3),(23.4,4),(27.8,5),(13.3,6)]
for at,i in lines:
 with wave.open(str(AUDIO/f'line-{i}.wav'),'rb') as w:
  assert w.getframerate()==R;arr=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float64)/32768
 gain=.16/max(.001,np.sqrt(np.mean(arr*arr)));add(at,arr,min(3,gain))
out[-round(.15*R):]*=np.linspace(1,0,round(.15*R))[:,None];out*=min(1,.94/np.max(np.abs(out)))
with wave.open(str(ROOT/'opening-mix.wav'),'wb') as w:w.setparams((2,2,R,0,'NONE','not compressed'));w.writeframes(np.int16(out*32767).tobytes())
print('SOUND COMPLETE; peak',round(float(np.max(np.abs(out))),4))
