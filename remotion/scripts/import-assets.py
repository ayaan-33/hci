"""Copy the supplied TeamGARI files into portable canonical paths; never read credentials."""
from pathlib import Path
import argparse, shutil, json
ROOT=Path(__file__).resolve().parents[1]
KEYS=['Immad-01','Immad-02','Raj-01','Raj-02','Raj-03','Awais-01','Awais-02','Raja-01','Raja-02','Immad-03']
def main():
 p=argparse.ArgumentParser();p.add_argument('--from',dest='source',type=Path,required=True);p.add_argument('--art',type=Path);args=p.parse_args();files=list(args.source.rglob('*'))
 for key in KEYS:
  hits=[f for f in files if f.is_file() and f.suffix.lower()=='.ogg' and f.name.startswith(key)]
  if len(hits)!=1:raise SystemExit(f'Expected exactly one {key} OGG, found {len(hits)}')
  dst=ROOT/'public/assets/audio'/f'{key}.ogg';dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(hits[0],dst)
 for n in [1,2]:
  hits=[f for f in files if f.name==f'C-10-TeamGARI-ToolTalk-Scenario-{n}.mov']
  if len(hits)!=1:raise SystemExit(f'Missing scenario {n}')
  dst=ROOT/'public/assets/demos'/f'scenario-{n}.mov';dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(hits[0],dst)
 for f in files:
  if f.is_file() and f.name.startswith('C-10-TeamGARI') and f.suffix.lower() in ['.html','.pptx','.pdf']:
   dst=ROOT/'public/assets/reference'/f.name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dst)
 if args.art:
  mapping={'exec-77cf4363-c1f2-4a0c-82fd-ae3ff3eef198.png':'hero.png','exec-cbc75a02-da07-4eb1-a264-ab8370b28ed8.png':'demo.png','exec-0fe1d81f-deb3-4a31-b1bb-b052611a17b4.png':'avatar-reference.png'}
  for src,dst in mapping.items():shutil.copy2(args.art/src,ROOT/'public/assets/backgrounds'/dst)
 print('Imported ten recordings, two demos and original reference documents.')
if __name__=='__main__':main()
