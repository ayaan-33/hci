import os,glob,json,subprocess
R='/workspace/work/v3';codec=['-c:v','libx264','-preset','veryfast','-crf','23','-threads','2','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-movflags','+faststart']
move="perspective=x0='12+8*sin(on/100)':y0=10:x1='W-12':y1='8+6*sin(on/100)':x2=12:y2=H-8:x3=W-12:y3=H-12:sense=destination:eval=frame"
def run(cmd,log):
 with open(R+'/'+log,'w') as f:r=subprocess.run(cmd,stdout=f,stderr=f)
 if r.returncode:raise RuntimeError(log)
for key,dur,old,new in [('Immad-01',40.5,'/workspace/work/v2/slides/Immad-01-1.png',R+'/team-with-cutouts.png'),('Immad-03',60.9,'/workspace/work/v2/slides/Immad-03-3.png',R+'/closing-with-cutouts.png')]:
 txt=open('/workspace/work/v2/'+key+'.ffconcat').read().replace(old,new);open(R+'/'+key+'.ffconcat','w').write(txt);audio=glob.glob('/workspace/attachments/*/'+key+'*')[0]
 print('ENCODING',key,flush=True)
 run(['ffmpeg','-y','-v','warning','-filter_threads','2','-f','concat','-safe','0','-i',R+'/'+key+'.ffconcat','-i',audio,'-vf',f'fps=24,{move},ass=/workspace/work/{key}.ass,fade=t=in:d=0.35,fade=t=out:st={dur-.3}:d=0.3','-t',str(dur)]+codec+[R+'/'+key+'.mp4'],key+'.log')
for key in ['Immad-01','Immad-03']:
 data=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=start_time,duration','-of','json',R+'/'+key+'.mp4']))['streams'][0]
 assert float(data['start_time'])<.05 and float(data['duration'])>39,data
listing=open('/workspace/work/v2/final.ffconcat').read()
for key in ['Immad-01','Immad-03']:listing=listing.replace('/workspace/work/v2/clips/'+key+'.mp4',R+'/'+key+'.mp4')
open(R+'/final.ffconcat','w').write(listing)
run(['ffmpeg','-y','-v','warning','-f','concat','-safe','0','-i',R+'/final.ffconcat','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-movflags','+faststart',R+'/C-10-TeamGARI.mp4'],'final.log')
print('V3 ASSEMBLED',flush=True)
