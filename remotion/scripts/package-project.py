"""Build the portable handoff ZIP, including prepared media, excluding caches/secrets."""
from pathlib import Path
import argparse,zipfile,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT.parent/'teamgari-remotion-project.zip');args=parser.parse_args();out=args.output.resolve();out.parent.mkdir(parents=True,exist_ok=True)
 exclude={'node_modules','.git','.cache','.venv','__pycache__','out'}
 candidates=[p for p in ROOT.rglob('*') if p.is_file() and not any(part in exclude for part in p.relative_to(ROOT).parts) and not p.name.startswith('.env') and p.resolve()!=out]
 proof=ROOT/'out/proof.mp4'
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(candidates):z.write(p,'teamgari-editorial-film/'+p.relative_to(ROOT).as_posix())
  if proof.exists():z.write(proof,'teamgari-editorial-film/out/proof.mp4')
 with zipfile.ZipFile(out) as z:
  bad=z.testzip()
  if bad:raise ValueError('Corrupt archive member: '+bad)
  names=z.namelist()
  for name in ['package-lock.json','README.md','public/generated/manifest.json','public/generated/narration.wav','public/generated/demos/Raj-01.mp4','public/assets/avatars/immad.png']:
   if 'teamgari-editorial-film/'+name not in names:raise ValueError('Missing portable dependency: '+name)
 digest=hashlib.sha256(out.read_bytes()).hexdigest();print(json.dumps({'zip':str(out),'files':len(names),'bytes':out.stat().st_size,'sha256':digest},indent=2))
if __name__=='__main__':main()
