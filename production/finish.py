import os,json,subprocess,glob,shutil
from PIL import Image,ImageDraw,ImageFont
import time
while not (os.path.exists('work/intro_frames/0240.png') and 'Main sections complete.' in open('work/edit.log').read()):time.sleep(2)
from edit import BG,txt,font,ASS,codec,duration,run
# edit.py will have completed all main sections before reaching this file.
os.makedirs('work/endcards',exist_ok=True)
im=BG.copy();d=ImageDraw.Draw(im)
txt(d,(90,70),'Sources & production notes',54,b=True)
refs=[
'Soni et al. (2022) • Frontiers in Digital Health • doi:10.3389/fdgth.2022.954069',
'JMIR Human Factors (2021) • doi:10.2196/25787',
'Xiao et al. (2020) • ACM TOCHI • doi:10.1145/3381804',
'Wei et al. • arXiv:2301.05843 (preprint reference supplied in slides)',
'Amershi et al. (2019) • Guidelines for Human–AI Interaction • CHI 2019',
'W3C • WCAG 2.2 SC 4.1.3 • ARIA23 conversation-log technique',
'Typeform claim via tinycommand.com (2025) • secondhand vendor claim; not tested'
]
y=190
for r in refs:y=txt(d,(100,y),r,27,width=1700)+28
y=txt(d,(100,785),'Original voices & prototype: Team C-10 / teamGARI',27,'#54e3c3')
y=txt(d,(100,y+15),'Opening: synthetic AI narration and a newly rendered 3D parcel-sorter analogy.',25)
txt(d,(100,y+12),'Editing, captions and animation assisted by OpenAI Codex. No live LLM is used in the demo.',25,width=1680)
im.save('work/endcards/references.png')
# Add a large ending title to the true 3D opening after its analogy completes.
title=Image.new('RGBA',(1920,1080),(0,0,0,0));d=ImageDraw.Draw(title)
d.rounded_rectangle((300,290,1620,730),radius=24,fill=(5,15,25,240),outline='#54e3c3',width=3)
txt(d,(390,350),'Confirmed ≠ correct.',76,'#f4f8f8',1200,True)
txt(d,(390,475),'What does the system actually record?',37,'#54e3c3',1150)
txt(d,(390,570),'CHAT-STYLE ONBOARDING × A TRADITIONAL FORM',26,width=1150)
title.save('work/endcards/opening-title.png')
if not os.path.exists('work/clips/intro.mp4'):
 graph="[0:v]setpts=0.65*PTS,fps=24,scale=1920:1080,tpad=stop_mode=clone:stop_duration=8[b];[b][1:v]overlay=enable='gte(t,14)',ass=work/intro.ass,fade=t=in:d=0.4,fade=t=out:st=19.6:d=0.4[v]"
 run(['ffmpeg','-y','-v','warning','-threads','2','-filter_complex_threads','2','-framerate','12','-i','work/intro_frames/%04d.png','-loop','1','-i','work/endcards/opening-title.png','-i','work/intro.mp3','-filter_complex',graph,'-map','[v]','-map','2:a','-af','apad','-t','20']+codec+['work/clips/intro.mp4'],'work/intro-encode.log')
if not os.path.exists('work/clips/references.mp4'):
 run(['ffmpeg','-y','-v','warning','-loop','1','-framerate','24','-i','work/endcards/references.png','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-vf','fade=t=in:d=0.4,fade=t=out:st=11.4:d=0.6','-t','12']+codec+['work/clips/references.mp4'],'work/references.log')
timeline=json.load(open('work/timeline.json'))
clips=['intro']+[r['key'] for r in timeline]+['references']
open('work/final.ffconcat','w').write(''.join("file '/workspace/work/clips/"+k+".mp4'\n" for k in clips))
# Normalize dialogue while preserving the original voices. Video is copied without another lossy pass.
run(['ffmpeg','-y','-v','warning','-f','concat','-safe','0','-i','work/final.ffconcat','-map','0:v','-map','0:a','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-movflags','+faststart','output/C-10-TeamGARI.mp4'],'work/final.log')
srt=open('output/C-10-TeamGARI.srt').read();import re
vtt='WEBVTT\n\n'+re.sub(r'(\d\d:\d\d:\d\d),(\d\d\d)',r'\1.\2',srt)
open('output/C-10-TeamGARI.vtt','w').write(vtt)
run(['ffmpeg','-y','-v','error','-ss','6','-i','output/C-10-TeamGARI.mp4','-frames:v','1','-vf','scale=1280:720','-q:v','2','output/poster.jpg'],'work/poster.log')
print('ASSEMBLED',duration('output/C-10-TeamGARI.mp4'),os.path.getsize('output/C-10-TeamGARI.mp4'),flush=True)
