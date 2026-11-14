"""The complete 35-second birthday-cake analogy, with authored 3D layer motion.
Native assets: 1920x960 Cycles renders. Composite: 30 fps, output: 3840x1920.
"""
from pathlib import Path
import os,subprocess,math,json,wave
import numpy as np
import cv2
from PIL import Image,ImageDraw,ImageFont,ImageFilter
BASE=Path(__file__).parent;ROOT=Path(os.environ.get('EDITORIAL_WORK',str(BASE/'build')));WORK=ROOT/'full';W,H=1920,960
FONT=BASE/'assets/Inter.ttf';OIDN=os.environ.get('OIDN',str(ROOT/'oidn-2.5.1.x86_64.linux/bin/oidnDenoise'))

def font(size,weight=450):
 f=ImageFont.truetype(str(FONT),size)
 try:f.set_variation_by_axes([weight if b'Weight' in ax['name'] else ax['default'] for ax in f.get_variation_axes()])
 except (ValueError,OSError):pass
 return f

def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def pfmwrite(path,arr):
 with open(path,'wb') as f:f.write(f'PF\n{arr.shape[1]} {arr.shape[0]}\n-1.0\n'.encode());np.flipud(arr).astype('<f4').tofile(f)
def pfmread(path):
 with open(path,'rb') as f:
  assert f.readline().strip()==b'PF';w,h=map(int,f.readline().split());scale=float(f.readline());return np.flipud(np.frombuffer(f.read(),dtype='<f4' if scale<0 else '>f4').reshape(h,w,3))
def clean(name,folder=WORK):
 raw=folder/f'{name}.png';out=folder/f'{name}-clean.png'
 if out.exists() and out.stat().st_mtime>=raw.stat().st_mtime:return np.array(Image.open(out).convert('RGBA'))
 im=Image.open(raw).convert('RGBA');arr=np.array(im);a=arr[:,:,3].copy()
 pfmwrite(WORK/'denoise-in.pfm',arr[:,:,:3].astype(np.float32)/255)
 subprocess.run([OIDN,'--ldr',str(WORK/'denoise-in.pfm'),'--srgb','--threads','2','-o',str(WORK/'denoise-out.pfm')],stdout=subprocess.DEVNULL,check=True)
 rgb=np.uint8(np.clip(pfmread(WORK/'denoise-out.pfm')*255,0,255));rgba=np.dstack([rgb,a]);Image.fromarray(rgba).save(out);return rgba

def track(d,pos,word,size=17,color='#a9b7c5',spacing=2.4):
 x,y=pos;f=font(size,500)
 for c in word:d.text((x,y),c,font=f,fill=color);x+=d.textlength(c,font=f)+spacing

def glass(im,xy,title,value,color='#aee9dc',alpha=1,height=176):
 if alpha<=0:return
 x,y=map(int,xy);width=560;lay=Image.new('RGBA',im.size);crop=im.crop((x,y,x+width,y+height)).filter(ImageFilter.GaussianBlur(18)).convert('RGBA');crop.alpha_composite(Image.new('RGBA',crop.size,(13,22,34,170)));mask=Image.new('L',crop.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,width-1,height-1),radius=23,fill=255);lay.paste(crop,(x,y),mask);d=ImageDraw.Draw(lay);d.rounded_rectangle((x,y,x+width,y+height),radius=23,outline=(180,211,220,80),width=1);d.line((x+23,y+1,x+width-23,y+1),fill=(220,239,240,105))
 track(d,(x+27,y+25),title,15,'#a6b3c2',2)
 vals=value if isinstance(value,list) else [value]
 for j,line in enumerate(vals):
  size=34
  while d.textlength(line,font=font(size,460))>505:size-=1
  d.text((x+27,y+78+j*44),line,font=font(size,460),fill=color)
 lay.putalpha(lay.getchannel('A').point(lambda a:int(a*alpha)));im.alpha_composite(lay)

def heading(im,lines,phase):
 lay=Image.new('RGBA',im.size);d=ImageDraw.Draw(lay);e=ease(phase/.65)
 for i,line in enumerate(lines):d.text((88,175+i*78+round(20*(1-e))),line,font=font(64,530),fill=(235,239,244,round(e*255)) if i==0 else (221,182,123,round(e*255)))
 im.alpha_composite(lay)

ASSETS={}
for name in ['cake','packing-background','packing-lid','journey-background','journey-van','party']:
 ASSETS[name]=clean(name);print('READY',name,flush=True)
for name in ['dispatch','confirmation','reveal']:ASSETS[name]=clean(name,ROOT)
X,Y=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
DEPTH={}
for name in ['cake','packing-background','journey-background','party','dispatch','confirmation','reveal']:
 folder=ROOT if name in ['dispatch','confirmation','reveal'] else WORK
 dep=cv2.imread(str(folder/f'{name}-depth-0120.png'),cv2.IMREAD_UNCHANGED);assert dep is not None
 DEPTH[name]=cv2.GaussianBlur(1-np.clip(dep.astype(np.float32)/65535,0,1),(0,0),1.2)

def parallax(name,u,direction=1):
 pan=direction*(-20+40*ease(u));tilt=7*math.sin(u*math.pi);near=DEPTH[name];base=ASSETS[name][:,:,:3];arr=cv2.remap(base,X-pan*(.25+.75*near),Y-tilt*near,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
 mat=cv2.getRotationMatrix2D((W*.58,H*.55),0,1.025+.030*ease(u));return cv2.warpAffine(arr,mat,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)

def overlay(im,name,dx=0,dy=0,scale=1,angle=0,alpha=1,shadow=False):
 rgba=ASSETS[name];mt=cv2.getRotationMatrix2D((W*.55,H*.55),angle,scale);mt[0,2]+=dx;mt[1,2]+=dy
 warped=cv2.warpAffine(rgba,mt,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
 lay=Image.fromarray(warped)
 if shadow:
  mask=lay.getchannel('A').filter(ImageFilter.GaussianBlur(13));sh=Image.new('RGBA',im.size,(0,0,0,0));sh.putalpha(mask.point(lambda a:int(a*.22)));im.alpha_composite(sh,(0,19))
 if alpha<1:lay.putalpha(lay.getchannel('A').point(lambda a:int(a*alpha)))
 im.alpha_composite(lay)

SHOTS=[(0,3,'cake'),(3,5,'packing-background'),(5,10,'dispatch'),(10,15,'confirmation'),(15,23,'journey-background'),(23,29,'reveal'),(29,32,'party'),(32,35,'confirmation')]
CAPS=[(.45,3.9,'Imagine sending a birthday cake across town.'),(5.15,8.6,'But the delivery system records the wrong address.'),(10.3,13,'Someone confirms it without noticing.'),(13.3,14.6,'“Confirmed!”'),(15.2,18.3,'Now everything runs beautifully.'),(18.3,21.7,'Sorted. Dispatched. Right on schedule.'),(23.4,25.3,'“Delivery successful!”'),(27.8,30,'The delivery was confirmed.'),(30,32,'The address was still wrong.'),(32,34.8,'What happens when an interface makes the same mistake?')]

def render(t):
 idx=next(i for i,(a,b,n) in enumerate(SHOTS) if a<=t<b);a,b,name=SHOTS[idx];local=t-a;u=local/(b-a)
 # Hold the packing environment camera still so the separately rendered lid lands exactly.
 bg=ASSETS[name][:,:,:3] if idx==1 else parallax(name,u,(-1 if idx in [2,5] else 1))
 im=Image.fromarray(bg).convert('RGBA')
 if idx==1:
  close=ease((local-.15)/1.45);overlay(im,'packing-lid',dx=22*(1-close),dy=-165*(1-close),angle=-3*(1-close),shadow=True)
 elif idx==4:
  # Distinct van layer follows the road, rather than moving with the background.
  travel=ease(u);overlay(im,'journey-van',dx=190-430*travel,dy=35-95*travel,scale=1.04-.08*travel,angle=.3*math.sin(u*math.pi),shadow=True)
 # Editorial negative space is deliberately quiet and carries the comparison.
 shade=np.zeros((H,W,4),np.uint8);shade[:,:,3]=np.uint8(np.clip(1-np.arange(W)[None,:]/1050,0,1)*85);im.alpha_composite(Image.fromarray(shade));d=ImageDraw.Draw(im)
 track(d,(88,68),'TEAM C-10  /  teamGARI',18,'#a9b5c2',2)
 if idx in [0,1]:
  heading(im,['A birthday.','A simple request.'],t)
  glass(im,(88,488),'FOR MAYA','14 Maple Street',alpha=ease((t-.65)/.6))
 elif idx==2:
  heading(im,['One address.','One wrong record.'],local)
  glass(im,(88,413),'ON THE ORIGINAL GIFT CARD','14 Maple Street',alpha=ease((local-.25)/.5))
  glass(im,(88,614),'RECORDED BY THE SYSTEM','14 Beacon Point','#e6b77f',ease((local-1.25)/.6))
 elif idx==3:
  heading(im,['A single click.','No correction.'],local)
  glass(im,(88,488),'CONFIRM DELIVERY TO','14 Beacon Point','#e6b77f',ease(local/.4))
  d=ImageDraw.Draw(im);confirmed=t>=13.3
  d.rounded_rectangle((88,699,648,766),radius=17,fill='#b1e6d5' if confirmed else '#d9e6e6')
  word='✓  CONFIRMED' if confirmed else 'Confirm';ft=font(26,550);tw=d.textlength(word,font=ft);d.text(((88+648-tw)/2,717),word,font=ft,fill='#14272a')
  if 11.6<t<13.9:
   p=ease((t-11.6)/1.65);cx=704-315*p;cy=799-65*p
   d.polygon([(cx,cy),(cx+3,cy+32),(cx+12,cy+24),(cx+21,cy+36),(cx+28,cy+32),(cx+19,cy+20),(cx+31,cy+19)],fill='#f8fafb',outline='#132b32',width=2)
  if 13.3<=t<13.9:
   q=(t-13.3)/.6;lay=Image.new('RGBA',im.size);ld=ImageDraw.Draw(lay);r=18+65*q;ld.ellipse((389-r,734-r,389+r,734+r),outline=(177,230,213,round(150*(1-q))),width=2);im.alpha_composite(lay)
 elif idx==4:
  heading(im,['Sorted.','Dispatched.'] if local<3.6 else ['Right on','schedule.'],local if local<3.6 else local-3.6)
  glass(im,(88,488),'NAVIGATION','→  Beacon Point',alpha=ease((local-.4)/.6))
  d=ImageDraw.Draw(im)
  for j,(cue,line) in enumerate([(1,'Sorted'),(3,'Dispatched'),(5,'On schedule')]):
   if local>=cue:d.text((103,704+j*36),'✓  '+line,font=font(24,460),fill='#aee9dc')
 elif idx==5:
  if local<2.4:
   heading(im,['Delivery','successful.'],local);glass(im,(88,488),'STATUS','✓  Delivered',alpha=ease((local-.4)/.5))
  else:
   heading(im,['To the','wrong place.'],local-2.4);glass(im,(88,488),'ACTUAL DESTINATION','Beacon Point · lighthouse','#e6b77f',ease((local-2.4)/.6))
 elif idx==6:
  heading(im,['Meanwhile,','at Maple Street.'],local)
  glass(im,(88,488),'THE INTENDED DESTINATION','14 Maple Street',alpha=ease(local/.5))
  ImageDraw.Draw(im).text((92,704),'The birthday is ready. The cake is missing.',font=font(25,440),fill='#bac5d1')
 else:
  im.alpha_composite(Image.new('RGBA',im.size,(12,15,20,round(110*ease(local/1.2)))))
  heading(im,['Confirmed.','Still wrong.'],local)
  glass(im,(88,463),'PROFILE SUMMARY',['Courses','Exam dates','Work evenings'],alpha=ease((local-.4)/.6),height=255)
 d=ImageDraw.Draw(im);d.text((88,894),'CONFIRMED ≠ CORRECT',font=font(17,500),fill='#8b9aa9')
 for ca,cb,line in CAPS:
  if ca<=t<cb:
   ft=font(25,450);ww=d.textlength(line,font=ft);x=(W-ww)/2;d.rounded_rectangle((x-20,819,x+ww+20,866),radius=13,fill=(9,14,22,238));d.text((x,829),line,font=ft,fill='#f0f3f7')
 if t>34.65:im.alpha_composite(Image.new('RGBA',im.size,(16,17,20,round(255*ease((t-34.65)/.32)))))
 return im.convert('RGB')

# Save meaningful review frames before encoding.
for t in [1.8,3.2,4.9,7.5,12.5,13.6,19,24,26.5,30.5,33.5]:render(t).save(WORK/f'review-{t:04.1f}.jpg',quality=95)
output=WORK/'birthday-opening.mp4'
cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x960','-r','30','-i','pipe:0','-i',str(WORK/'opening-mix.wav'),'-map','0:v','-map','1:a','-vf','scale=3840:1920:flags=lanczos','-c:v','libx264','-threads','2','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-video_track_timescale','15360','-t','35','-movflags','+faststart',str(output)]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for f in range(1050):
 proc.stdin.write(render(f/30).tobytes())
 if f%150==0:print('COMPOSITE FRAME',f,'/ 1050',flush=True)
proc.stdin.close();assert proc.wait()==0
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(output)]));v=next(s for s in meta['streams'] if s['codec_type']=='video');assert int(v['nb_frames'])==1050 and abs(float(meta['format']['duration'])-35)<.01
print('OPENING COMPLETE',str(output),flush=True)
