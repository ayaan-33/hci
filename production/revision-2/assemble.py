import os,time,json,subprocess,glob
from PIL import Image,ImageDraw,ImageFont
ROOT='/workspace/work/v2'
codec=['-c:v','libx264','-preset','veryfast','-crf','23','-threads','2','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-movflags','+faststart']
def run(cmd,log):
 with open(log,'w') as f:r=subprocess.run(cmd,stdout=f,stderr=f)
 if r.returncode:raise RuntimeError(log)
def ready(paths):
 while True:
  try:
   log=open(ROOT+'/slides-render.log').read()
   if all(f"Saved: '{p}'" in log for p in paths):
    for p in paths:
     with Image.open(p) as im:im.load()
    return
  except Exception:pass
  time.sleep(2)
move="perspective=x0='12+8*sin(on/100)':y0=10:x1='W-12':y1='8+6*sin(on/100)':x2=12:y2=H-8:x3=W-12:y3=H-12:sense=destination:eval=frame"
timeline=json.load(open('/workspace/work/timeline.json'))
sections=json.load(open(ROOT+'/slide_content.json'))
for section in sections:
 key=section['key'];out=f'{ROOT}/clips/{key}.mp4'
 if os.path.exists(out):continue
 ready([f'{ROOT}/slides/{key}-{j}.png' for j in range(len(section['cards']))])
 source=open(f'/workspace/work/{key}.ffconcat').read().replace('/workspace/work/cards/',ROOT+'/slides/');open(ROOT+'/'+key+'.ffconcat','w').write(source)
 p=glob.glob('/workspace/attachments/*/'+key+'*')[0];dur=next(t['duration'] for t in timeline if t['key']==key)
 print('ENCODING',key,flush=True)
 run(['ffmpeg','-y','-v','warning','-filter_threads','2','-f','concat','-safe','0','-i',ROOT+'/'+key+'.ffconcat','-i',p,'-vf',f'fps=24,{move},ass=/workspace/work/{key}.ass,fade=t=in:d=0.35,fade=t=out:st={dur-.3}:d=0.3','-t',str(dur)]+codec+[out],ROOT+'/'+key+'.log')
# Keep the title vivid as the analogy resolves.
im=Image.new('RGBA',(1920,1080));d=ImageDraw.Draw(im);d.rounded_rectangle((240,285,1680,735),radius=30,fill=(24,30,92,245),outline='#18f0d2',width=5)
d.rounded_rectangle((240,285,1680,308),radius=10,fill='#ffb52e')
for x,y,t,n,b,c in [(340,350,'Confirmed ≠ correct.',80,True,'#fff9f0'),(340,480,'What does the system actually record?',38,False,'#54fff0'),(340,585,'CHAT-STYLE ONBOARDING × A TRADITIONAL FORM',27,False,'#ffce54')]:
 f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else '')+'.ttf',n);d.text((x,y),t,font=f,fill=c)
im.save(ROOT+'/opening-title.png')
while 'Blender quit' not in open(ROOT+'/intro-render.log').read():time.sleep(2)
print('ENCODING intro',flush=True)
graph=f"[0:v]setpts=0.65*PTS,fps=24,scale=1920:1080,tpad=stop_mode=clone:stop_duration=8[b];[b][1:v]overlay=enable='gte(t,14)',ass=/workspace/work/intro.ass,fade=t=in:d=0.4,fade=t=out:st=19.6:d=0.4[v]"
run(['ffmpeg','-y','-v','warning','-filter_complex_threads','2','-framerate','12','-i',ROOT+'/intro_frames/%04d.png','-loop','1','-i',ROOT+'/opening-title.png','-i',ROOT+'/intro-soundtrack.wav','-filter_complex',graph,'-map','[v]','-map','2:a','-af','apad','-t','20']+codec+[ROOT+'/clips/intro.mp4'],ROOT+'/intro-encode.log')
ready([ROOT+'/slides/references.png'])
run(['ffmpeg','-y','-v','warning','-filter_threads','2','-loop','1','-framerate','24','-i',ROOT+'/slides/references.png','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-vf',move+',fade=t=in:d=0.4,fade=t=out:st=11.4:d=0.6','-t','12']+codec+[ROOT+'/clips/references.mp4'],ROOT+'/references.log')
keys=['intro']+[t['key'] for t in timeline]+['references'];open(ROOT+'/final.ffconcat','w').write(''.join(f"file '{ROOT}/clips/{key}.mp4'\n" for key in keys))
run(['ffmpeg','-y','-v','warning','-f','concat','-safe','0','-i',ROOT+'/final.ffconcat','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-movflags','+faststart',ROOT+'/C-10-TeamGARI.mp4'],ROOT+'/final.log')
run(['ffmpeg','-y','-v','error','-ss','6','-i',ROOT+'/C-10-TeamGARI.mp4','-frames:v','1','-vf','scale=1280:720','-q:v','2',ROOT+'/poster.jpg'],ROOT+'/poster.log')
print('V2 ASSEMBLED',flush=True)
