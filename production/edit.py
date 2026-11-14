import os,glob,json,subprocess,math,textwrap,re,difflib
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from content import segments,intro
ROOT='/workspace';W,H=1920,1080
os.makedirs('work/cards',exist_ok=True);os.makedirs('work/clips',exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
def wrap(d,text,f,width):
 words=text.split();lines=[];line=''
 for w in words:
  new=(line+' '+w).strip()
  if d.textlength(new,font=f)>width and line:lines.append(line);line=w
  else:line=new
 if line:lines.append(line)
 return lines
def txt(d,xy,t,size=32,color='#eaf2f5',width=1000,b=False,spacing=1.35):
 x,y=xy
 for line in wrap(d,t,font(size,b),width):d.text((x,y),line,font=font(size,b),fill=color);y+=int(size*spacing)
 return y

def background():
 im=Image.new('RGB',(W,H),'#09121e');d=ImageDraw.Draw(im)
 # Vanishing-point grid defines the virtual stage.
 for xx in range(-1800,3800,150):d.line([(960,480),(xx,1080)],fill='#152a3b',width=2)
 for yy in [560,600,650,715,795,900,1040]:d.line([(0,yy),(W,yy)],fill='#152a3b',width=2)
 # Dimensional architectural blocks behind the floating panels.
 for x,y,a in [(1540,130,180),(1740,260,100),(70,650,90)]:
  d.polygon([(x,y),(x+a,y+40),(x+a,y+40+a),(x,y+a)],fill='#123745')
  d.polygon([(x,y),(x+70,y-40),(x+a+70,y),(x+a,y+40)],fill='#1a4b52')
  d.polygon([(x+a,y+40),(x+a+70,y),(x+a+70,y+a),(x+a,y+40+a)],fill='#0c2537')
 return im
BG=background();BG.save('work/cards/background.png')
def panel(d,box,fill='#122534',accent='#53e0c2'):
 x,y,x2,y2=box
 d.rounded_rectangle((x+12,y+15,x2+12,y2+15),radius=20,fill='#03090f')
 d.polygon([(x2,y+15),(x2+12,y+30),(x2+12,y2+10),(x2,y2)],fill='#244454')
 d.rounded_rectangle(box,radius=20,fill=fill,outline='#2c4858',width=2)
 d.rounded_rectangle((x,y,x+5,y2),radius=2,fill=accent)
def header(d,speaker,chapter,index):
 d.rounded_rectangle((70,50,124,104),radius=14,fill='#54e3c3');d.text((83,53),'G',font=font(34,True),fill='#09202b')
 d.text((145,49),'teamGARI',font=font(27,True),fill='#eef6f6');d.text((145,84),'AHCI • TEAM C-10',font=font(16),fill='#9db6c4')
 d.text((1120,60),chapter.upper(),font=font(22,True),fill='#a6c0cd')
 d.line((70,130,1850,130),fill='#274452',width=2)
 d.text((75,929),speaker,font=font(24,True),fill='#52e1c2')
 d.text((75,965),'CHAT × FORM  /  A STUDY-PLANNER PROFILE',font=font(16),fill='#91a9b7')
 d.text((1755,940),f'{index:02d} / 10',font=font(19),fill='#9bb5c2')
def card(speaker,chapter,index,title,kicker,bullets,path):
 im=BG.copy();d=ImageDraw.Draw(im);header(d,speaker,chapter,index)
 txt(d,(80,208),kicker,22,'#54e3c3',650,True)
 txt(d,(75,273),title,70,'#f1f6f7',650,True,1.16)
 if title=='Meet teamGARI':
  # Deliberately no generated likenesses: original-photo cutouts await source files.
  for j,name in enumerate(bullets):
   x=80+j*450;panel(d,(x,580,x+415,800));txt(d,(x+28,610),f'0{j+1}',25,'#54e3c3');txt(d,(x+28,663),name,36,width=355,b=True)
 else:
  n=len(bullets);height=min(155,int(550/max(n,1)));gap=24;y=220
  for j,b in enumerate(bullets):
   panel(d,(815,y,1815,y+height));d.text((846,y+26),f'{j+1:02d}',font=font(22,True),fill='#54e3c3');txt(d,(902,y+24),b,31,width=870,b=False);y+=height+gap
 im.save(path)
def duration(p):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
def norm(w):return re.sub(r'[^a-z0-9]','',w.lower().replace('’',"'"))
trans=json.load(open('work/transcription.json')) if os.path.exists('work/transcription.json') else {}
def align(p,text,dur):
 words=text.split();rec=[w for seg in trans.get(p,[]) for w in seg['words']];times=[None]*len(words)
 if rec:
  sm=difflib.SequenceMatcher(None,[norm(w) for w in words],[norm(w['word']) for w in rec],autojunk=False)
  for a,b,n in sm.get_matching_blocks():
   for j in range(n):times[a+j]=(rec[b+j]['start'],rec[b+j]['end'])
 # Interpolate only words the speech recognizer did not match to the supplied script.
 anchors=[(-1,0)]+[(i,t[0]) for i,t in enumerate(times) if t]+[(len(words),dur)]
 for (a,ta),(b,tb) in zip(anchors,anchors[1:]):
  for i in range(a+1,b):
   st=ta+(tb-ta)*(i-a)/(b-a);en=ta+(tb-ta)*(i+1-a)/(b-a);times[i]=(st,en)
 return words,times

def ass_time(t):
 c=round(t*100);return f'{c//360000}:{c//6000%60:02d}:{c//100%60:02d}.{c%100:02d}'
def srt_time(t):
 m=round(t*1000);return f'{m//3600000:02d}:{m//60000%60:02d}:{m//1000%60:02d},{m%1000:03d}'
ASS='''[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 0\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,DejaVu Sans,32,&H00FFFFFF,&H00FFFFFF,&H00120C08,&H00120C08,0,0,0,0,100,100,0,0,3,10,0,2,190,190,30,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'''
allcaps=[];timeline=[]
def captions(p,text,dur,key,offset):
 words,times=align(p,text,dur);caps=[];start=0
 while start<len(words):
  end=min(start+10,len(words))
  for k in range(start+5,end):
   if words[k].endswith(('.', '?', '!')):end=k+1;break
  phrase=' '.join(words[start:end]);a=max(0,times[start][0]);b=min(dur,max(a+.5,times[end-1][1]));caps.append((a,b,phrase));allcaps.append((offset+a,offset+b,phrase));start=end
 open(f'work/{key}.ass','w').write(ASS+''.join(f'Dialogue: 0,{ass_time(a)},{ass_time(b)},Default,,0,0,0,,{t}\n' for a,b,t in caps))
 return words,times

def run(args,log):
 with open(log,'w') as f:
  r=subprocess.run(args,stdout=f,stderr=f)
 if r.returncode:raise RuntimeError(log)
codec=['-c:v','libx264','-preset','veryfast','-crf','23','-threads','3','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-movflags','+faststart']
# Intro captions and end-title composited after the Blender frames complete.
captions('work/intro.mp3',intro,20,'intro',0);offset=20
for idx,(key,speaker,chapter,text,cards) in enumerate(segments,1):
 p=glob.glob('/workspace/attachments/*/'+key+'*')[0];dur=duration(p);words,times=captions(p,text,dur,key,offset)
 timeline.append({'key':key,'speaker':speaker,'start':offset,'duration':dur,'chapter':chapter});offset+=dur
 if not cards:continue
 # Card switches follow the narration's paragraph boundaries.
 paragraphs=text.split('\n');parastarts=[];wi=0
 for para in paragraphs:parastarts.append(times[wi][0]);wi+=len(para.split())
 if key=='Awais-01':starts=[0,parastarts[2],parastarts[3]]
 elif key=='Awais-02':starts=[0,parastarts[1]]
 elif key=='Raja-01':starts=[0,parastarts[1]]
 elif key=='Raja-02':starts=[0,parastarts[1],parastarts[2]]
 elif key=='Immad-03':starts=[0,parastarts[1],parastarts[2],parastarts[3]]
 else:starts=[0]+parastarts[1:len(cards)]
 rows=[]
 for j,(title,kicker,bullets) in enumerate(cards):
  imagepath=f'/workspace/work/cards/{key}-{j}.png';card(speaker,chapter,idx,title,kicker,bullets,imagepath)
  length=(starts[j+1] if j+1<len(starts) else dur)-starts[j];rows += [f"file '{imagepath}'",f'duration {length:.6f}']
 rows.append(f"file '{imagepath}'");open(f'work/{key}.ffconcat','w').write('\n'.join(rows)+'\n')
json.dump(timeline,open('work/timeline.json','w'),indent=2)
open('work/all.ass','w').write(ASS+''.join(f'Dialogue: 0,{ass_time(a)},{ass_time(b)},Default,,0,0,0,,{t}\n' for a,b,t in allcaps))
open('output/C-10-TeamGARI.srt','w').write('\n\n'.join(f'{i+1}\n{srt_time(a)} --> {srt_time(b)}\n{t}' for i,(a,b,t) in enumerate(allcaps))+'\n')
if os.getenv('PREPARE_ONLY'):raise SystemExit
# These very small changes of perspective create a floating-panel camera move.
move="perspective=x0='8+5*sin(on/90)':y0=8:x1='W-8':y1='4+4*sin(on/90)':x2=8:y2=H-6:x3=W-8:y3=H-10:sense=destination:eval=frame"
for idx,(key,speaker,chapter,text,cards) in enumerate(segments,1):
 p=glob.glob('/workspace/attachments/*/'+key+'*')[0];dur=duration(p);out=f'work/clips/{key}.mp4'
 if os.path.exists(out):
  try:
   if abs(duration(out)-dur)<.15:continue
  except:pass
 print('Rendering',key,flush=True)
 if cards:
  run(['ffmpeg','-y','-v','warning','-threads','2','-f','concat','-safe','0','-i',f'work/{key}.ffconcat','-i',p,'-vf',f'fps=24,{move},ass=work/{key}.ass,fade=t=in:d=0.35,fade=t=out:st={dur-.3}:d=0.3','-t',str(dur)]+codec+[out],f'work/{key}.log')
 else:
  # Actual scenario recordings. Playback is retimed to the supplied commentary.
  source=glob.glob('/workspace/attachments/*/*Scenario-'+('1' if key=='Raj-01' else '2')+'.mov')[0]
  if key=='Raj-01':a,b,hold=0,41.411,8
  elif key=='Raj-02':a,b,hold=0,22,6
  else:a,b,hold=25,51.506,0
  rate=(dur-hold)/(b-a)
  stage=BG.copy();d=ImageDraw.Draw(stage);header(d,speaker,chapter,idx)
  d.rounded_rectangle((170,160,1755,915),radius=12,fill='#03070d',outline='#3e6977',width=3)
  # Raised evidence labels sit outside the original recording.
  left,right={
   'Raj-01':(['CLEAR INPUT','CS3014 + MT1003','Tuesday + Thursday'],['DISPLAYED TIMES','Chat 8.6 s','Form 12.5 s']),
   'Raj-02':(['SCRIPTED FAILURE','No exact date','Course-code typo'],['TWO VALUES SAVED','Guessed date','Wrong course code']),
   'Raj-03':(['FORM RECOVERY','Date required','Work evenings required'],['DISPLAYED TIME','18.7 seconds','Missing entries blocked'])
  }[key]
  for xx,items in [(65,left),(1535,right)]:
   panel(d,(xx,255,xx+315,660))
   yy=285
   for j,line in enumerate(items):
    yy=txt(d,(xx+22,yy),line,22 if j==0 else 27,'#54e3c3' if j==0 else '#eef5f7',270,j==0)+45
  txt(d,(480,910),'Original prototype recording • retimed to match commentary • scripted chat / n = 1',18,'#9bb4c1',1200)
  stage.save(f'work/cards/{key}-stage.png')
  # Crop the large empty side margins from the source screen recording.
  graph=f"[1:v]trim=start={a}:end={b},setpts={rate}*(PTS-STARTPTS),tpad=start_duration={hold}:start_mode=clone:stop_duration=3:stop_mode=clone,crop=2320:1582:352:0,scale=1100:750:force_original_aspect_ratio=decrease,pad=1100:750:(ow-iw)/2:(oh-ih)/2:color=0x0c171d[demo];[0:v][demo]overlay=410:155,ass=work/{key}.ass,fade=t=in:d=0.35,fade=t=out:st={dur-.3}:d=0.3[v]"
  run(['ffmpeg','-y','-v','warning','-threads','2','-filter_complex_threads','2','-loop','1','-framerate','24','-i',f'work/cards/{key}-stage.png','-i',source,'-i',p,'-filter_complex',graph,'-map','[v]','-map','2:a','-t',str(dur)]+codec+[out],f'work/{key}.log')
print('Main sections complete.',flush=True)
