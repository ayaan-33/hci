from PIL import Image
import os,time
source=Image.open('/workspace/generated_images/exec-bb191dd2-f192-492c-a14d-3403c3456224.png').convert('RGBA')
centers=[340,720,1100,1480]
for stage,out in [('team-stage.png','team-with-cutouts.png'),('closing-stage.png','closing-with-cutouts.png')]:
 while not os.path.exists('/workspace/work/v3/'+stage):time.sleep(1)
 canvas=Image.open('/workspace/work/v3/'+stage).convert('RGBA')
 for j,cx in enumerate(centers):
  cut=source.crop((round(j*source.width/4),0,round((j+1)*source.width/4),source.height));cut=cut.crop(cut.getbbox())
  h=470;cut=cut.resize((round(cut.width*h/cut.height),h),Image.Resampling.LANCZOS)
  canvas.alpha_composite(cut,(round(cx-cut.width/2),752-h))
 canvas.convert('RGB').save('/workspace/work/v3/'+out)
