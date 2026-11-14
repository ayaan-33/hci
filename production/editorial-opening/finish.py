"""Denoise the authored 3D assets and render a genuine depth-driven 2.5D study."""
from pathlib import Path
import os,sys,subprocess,wave,json,math
import numpy as np
import cv2
from PIL import Image,ImageDraw,ImageFont,ImageFilter
BASE=Path(__file__).parent;ROOT=Path(os.environ.get('EDITORIAL_WORK',str(BASE/'build')));OUT=BASE/'review';OUT.mkdir(exist_ok=True)
FONT=BASE/'assets/Inter.ttf';W,H=1920,960
OIDN=Path(os.environ.get('OIDN',str(ROOT/'oidn-2.5.1.x86_64.linux/bin/oidnDenoise')))
def font(size,weight=450):
 f=ImageFont.truetype(str(FONT),size)
 try:f.set_variation_by_axes([weight if b'Weight' in ax['name'] else ax['default'] for ax in f.get_variation_axes()])
 except (ValueError,OSError):pass
 return f

def pfm_write(path,im):
 with open(path,'wb') as f:f.write(f'PF\n{im.shape[1]} {im.shape[0]}\n-1.0\n'.encode());np.flipud(im).astype('<f4').tofile(f)
def pfm_read(path):
 with open(path,'rb') as f:
  assert f.readline().strip()==b'PF';w,h=map(int,f.readline().split());scale=float(f.readline());arr=np.frombuffer(f.read(),dtype='<f4' if scale<0 else '>f4').reshape(h,w,3);return np.flipud(arr)
def clean(scene):
 raw=ROOT/f'{scene}.png';target=ROOT/f'{scene}-clean.png'
 if target.exists() and target.stat().st_mtime>=raw.stat().st_mtime:return Image.open(target).convert('RGB')
 im=np.asarray(Image.open(raw).convert('RGB'),np.float32)/255;pfm_write(ROOT/f'{scene}.pfm',im)
 subprocess.run([str(OIDN),'--ldr',str(ROOT/f'{scene}.pfm'),'--srgb','--threads','2','-o',str(ROOT/f'{scene}-clean.pfm')],check=True,stdout=subprocess.DEVNULL)
 arr=pfm_read(ROOT/f'{scene}-clean.pfm');Image.fromarray(np.uint8(np.clip(arr*255,0,255))).save(target)
 return Image.open(target).convert('RGB')
def ease(t):t=np.clip(t,0,1);return float(t*t*(3-2*t))
def tracked(d,xy,word,size=20,color='#a4b6c6',spacing=3):
 x,y=xy;f=font(size,550)
 for c in word:d.text((x,y),c,font=f,fill=color);x+=d.textlength(c,font=f)+spacing

def glass(im,xy,title,value,accent='#aee9dc',opacity=1):
 x,y=map(int,xy);width,height=560,181
 if opacity<=0:return
 panel=Image.new('RGBA',im.size);d=ImageDraw.Draw(panel)
 # Real backdrop blur under a restrained, translucent smoked-glass fill.
 crop=im.crop((x,y,x+width,y+height)).filter(ImageFilter.GaussianBlur(20))
 blurred=crop.convert('RGBA');blurred.alpha_composite(Image.new('RGBA',blurred.size,(12,22,34,175)));mask=Image.new('L',(width,height));ImageDraw.Draw(mask).rounded_rectangle((0,0,width-1,height-1),radius=24,fill=255);panel.paste(blurred,(x,y),mask);d=ImageDraw.Draw(panel);d.rounded_rectangle((x,y,x+width,y+height),radius=24,outline=(156,180,196,88),width=1)
 d.line((x+26,y+1,x+width-26,y+1),fill=(215,236,239,110),width=1)
 tracked(d,(x+28,y+28),title,16,'#a5b2c4',2)
 d.text((x+28,y+83),value,font=font(35,470),fill=accent)
 panel.putalpha(panel.getchannel('A').point(lambda a:int(a*opacity)));im.alpha_composite(panel)

def treatment(image,scene,t=None):
 im=image.convert('RGBA');shade=Image.new('RGBA',im.size);arr=np.zeros((H,W,4),np.uint8);arr[:,:,3]=np.uint8(np.clip((1-np.arange(W)[None,:]/1050),0,1)*105);shade=Image.fromarray(arr);im.alpha_composite(shade)
 d=ImageDraw.Draw(im);tracked(d,(88,68),'TEAM C-10  /  teamGARI',18,'#a9b5c2',2)
 if t is None:
  titles={'dispatch':('One address.','One simple task.'),'confirmation':('A perfect process.','A wrong record.'),'reveal':('Delivered.','To the wrong place.')};lines=titles[scene];phase=1
 else:
  lines=('One address.','One wrong record.') if t<4.6 else ('Confirmed.','Still wrong.');phase=ease((t if t<4.6 else t-4.6)/.65)
 typelayer=Image.new('RGBA',im.size);td=ImageDraw.Draw(typelayer)
 for i,line in enumerate(lines):
  td.text((88,180+i*80+int(20*(1-phase))),line,font=font(65,530),fill=(235,239,244,int(255*phase)) if i==0 else (221,182,123,int(255*phase)))
 im.alpha_composite(typelayer);d=ImageDraw.Draw(im)
 if scene=='dispatch':
  d.text((92,377),'A birthday cake for Maya.',font=font(28),fill='#adb9c7');glass(im,(88,488),'THE ORIGINAL ADDRESS','14 Maple Street')
 elif scene=='confirmation':
  if t is None:glass(im,(88,488),'REQUEST  →  RECORDED','Maple Street  →  Beacon Point','#e6b77f')
  else:
   p=ease((t-.65)/.75);misread=t>2.7
   glass(im,(88,488),'RECORDED ADDRESS' if misread else 'YOUR REQUEST','14 Beacon Point' if misread else '14 Maple Street','#e6b77f' if misread else '#aee9dc',p)
   if t>6.35:
    d=ImageDraw.Draw(im);p=ease((t-6.35)/.4);d.rounded_rectangle((89,700,421,759),radius=16,fill=(123,225,193,int(245*p)));d.text((112,715),'✓  CONFIRMED',font=font(23,600),fill='#132b2b')
 else:glass(im,(88,488),'ACTUAL DESTINATION','Beacon Point · lighthouse','#e6b77f')
 d=ImageDraw.Draw(im);d.text((90,891),'CONFIRMED ≠ CORRECT',font=font(17,500),fill='#8794a4')
 tracked(d,(1530,891),'OPENING STUDY',14,'#82909f',2)
 return im.convert('RGB')

images={}
for scene in ['dispatch','confirmation','reveal']:
 images[scene]=clean(scene);treatment(images[scene],scene).save(OUT/f'{scene}.png');print('STYLE FRAME',scene,flush=True)
# Depth comes from the same authored camera as the confirmation beauty render.
depth=cv2.imread(str(ROOT/'confirmation-depth-0120.png'),cv2.IMREAD_UNCHANGED)
assert depth is not None
depth=depth.astype(np.float32)/65535;assert depth.shape==(H,W)
# The PNG depth transform is colour-managed. It remains monotonic; use a gentle
# bounded foreground weighting for a restrained screen-space camera move.
near=1-np.clip(depth,0,1);near=cv2.GaussianBlur(near,(0,0),1.2)
x,y=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32));base=np.asarray(images['confirmation']);D=8;R=48000
sound=np.zeros((D*R,2),np.float64);rng=np.random.default_rng(10)
def add(at,arr,gain=1):
 k=round(at*R);n=min(len(arr),len(sound)-k)
 if arr.ndim==1:arr=np.repeat(arr[:,None],2,axis=1)
 sound[k:k+n]+=arr[:n]*gain
# Quiet original ambient bed, with a restrained confirmation transient.
t=np.arange(D*R)/R;env=np.minimum(1,t/1.2)*np.minimum(1,(D-t)/.4)
pad=(np.sin(2*np.pi*130.8128*t)+.45*np.sin(2*np.pi*196*t)+.2*np.sin(2*np.pi*261.6256*t))*.012*env;add(0,pad)
voice_root=Path(os.environ.get('EDITORIAL_AUDIO',str(BASE/'assets/audio')))
for at,i in [(.55,1),(4.0,2),(6.65,6)]:
 with wave.open(str(voice_root/f'line-{i}.wav'),'rb') as w:arr=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
 add(at,arr,min(2,.14/max(.001,np.sqrt(np.mean(arr*arr)))))
for at,hz in [(2.7,660),(6.55,1046.5),(6.68,1567.98)]:
 tt=np.arange(int(.3*R))/R;add(at,np.sin(2*np.pi*hz*tt)*np.exp(-tt*18)*np.minimum(1,tt/.008),.045)
sound[-int(.18*R):]*=np.linspace(1,0,int(.18*R))[:,None];sound*=min(1,.94/np.max(np.abs(sound)))
with wave.open(str(ROOT/'study-audio.wav'),'wb') as w:w.setparams((2,2,R,0,'NONE','not compressed'));w.writeframes(np.int16(sound*32767).tobytes())
output=OUT/'C-10-TeamGARI_Editorial-Motion-Test.mp4'
cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x960','-r','30','-i','pipe:0','-i',str(ROOT/'study-audio.wav'),'-c:v','libx264','-threads','2','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t','8','-movflags','+faststart',str(output)]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for f in range(240):
 t=f/30;u=ease(t/8);pan=-18+36*u;tilt=8*math.sin(t*math.pi/8)
 mx=x-pan*(.3+.7*near);my=y-tilt*near
 warped=cv2.remap(base,mx,my,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
 scale=1.035+.025*u;matrix=cv2.getRotationMatrix2D((W*.58,H*.56),0,scale);warped=cv2.warpAffine(warped,matrix,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
 frame=treatment(Image.fromarray(warped),'confirmation',t)
 # Frame-accurate captions for the excerpt; typography remains crisp over 3D.
 d=ImageDraw.Draw(frame);caption=''
 if .55<=t<3.82:caption='But the delivery system records the wrong address.'
 elif 4<=t<6.65:caption='Someone confirms it without noticing.'
 elif 6.65<=t<7.95:caption='“Confirmed!”'
 if caption:
  ft=font(24,450);ww=d.textlength(caption,font=ft);xx=(W-ww)/2;d.rounded_rectangle((xx-20,819,xx+ww+20,866),radius=13,fill='#0b1019');d.text((xx,828),caption,font=ft,fill='#eaf0f5')
 proc.stdin.write(frame.tobytes())
 if f in [60,180]:frame.save(OUT/f'motion-frame-{f}.jpg',quality=95)
proc.stdin.close();assert proc.wait()==0
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(output)]));v=next(s for s in meta['streams'] if s['codec_type']=='video');assert int(v['nb_frames'])==240 and float(meta['format']['duration'])==8
subprocess.run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'],check=True)
(OUT/'verification.json').write_text(json.dumps({'duration':8,'frames':240,'resolution':[W,H],'fps':30,'fullDecode':'passed','method':'Custom Cycles 3D beauty assets; OIDN denoise; actual camera-depth-driven 2.5D parallax; vector-like Inter type and frosted overlays','scope':'Visual study, not replacement of the published final video'},indent=2))
print('MOTION TEST COMPLETE',flush=True)
