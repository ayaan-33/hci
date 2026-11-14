"""Render the new narrative assets; reuse the approved three beauty renders."""
import subprocess,os,json,time
from pathlib import Path
base=Path(__file__).parent;root=Path(os.environ.get('EDITORIAL_WORK',str(base/'build')))/'full';root.mkdir(parents=True,exist_ok=True)
jobs=[('cake','all','cake'),('packing','background','packing-background'),('packing','lid','packing-lid'),('journey','background','journey-background'),('journey','van','journey-van'),('party','all','party')]
for scene,layer,name in jobs:
 output=root/f'{name}.png'
 if output.exists() and (root/f'{name}-depth-0120.png').exists():print('REUSE',name,flush=True);continue
 print('RENDER',name,flush=True)
 with open(root/f'{name}.log','w') as log:
  subprocess.run(['blender','-b','-t','3','--python',str(base/'full-scene.py'),'--','--scene',scene,'--layer',layer,'--out',str(output),'--size','1920','--samples','32','--engine','CYCLES'],stdout=log,stderr=subprocess.STDOUT,check=True)
 assert output.exists(),f'Render failed: {name}'
 print('DONE',name,flush=True)
(root/'assets-complete.json').write_text(json.dumps({'newAssets':[j[2] for j in jobs],'nativeResolution':[1920,960]}))
