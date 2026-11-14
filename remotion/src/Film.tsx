import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,cancelRender,continueRender,delayRender,Sequence,staticFile,useCurrentFrame} from 'remotion';
import {FPS,FILM_FRAMES,PROOF_CLIPS} from './data/config';
import {ColdOpen,Credits,Scene} from './components/Scene';
import type {Manifest} from './types';
const useManifest=():Manifest|null=>{
 const [handle]=useState(()=>delayRender('Load local manifest and Inter font'));
 const [manifest,setManifest]=useState<Manifest|null>(null);
 useEffect(()=>{
  let disposed=false;const controller=new AbortController();
  const loadFont=async()=>{const f=new FontFace('Inter',`url(${staticFile('assets/fonts/InterVariable.woff2')})`,{weight:'100 900'});await f.load();document.fonts.add(f);await document.fonts.ready;};
  const load=async()=>{const r=await fetch(staticFile('generated/manifest.json'),{signal:controller.signal});if(!r.ok)throw new Error('Run python scripts/prepare.py before opening Studio or rendering.');return await r.json() as Manifest;};
  Promise.all([load(),loadFont()]).then(([m])=>{
   if(disposed)return;
   if(m.schemaVersion!==1||m.fps!==FPS||m.durationFrames!==FILM_FRAMES)throw new Error('Prepared manifest differs from the authored timeline. Re-run prepare.py and validate.');
   setManifest(m);continueRender(handle);
  }).catch((e:unknown)=>{if(!disposed)cancelRender(e instanceof Error?e:new Error(String(e)));});
  return()=>{disposed=true;controller.abort();};
 },[handle]);return manifest;
};
const AtFrame:React.FC<{manifest:Manifest;frame:number}>=({manifest,frame})=>{
 if(frame<540)return <ColdOpen frame={frame}/>;
 const section=manifest.sections.find(s=>frame>=s.startFrame&&frame<s.endFrame);
 if(section)return <Scene manifest={manifest} section={section} globalFrame={frame}/>;
 return <Credits frame={frame-(manifest.durationFrames-240)}/>;
};
export const Film:React.FC=()=>{
 const frame=useCurrentFrame(),manifest=useManifest();if(!manifest)return null;
 return <AbsoluteFill style={{background:'#101114'}}><Audio src={staticFile(manifest.narration)}/><AtFrame manifest={manifest} frame={frame}/></AbsoluteFill>;
};
const ProofShot:React.FC<{manifest:Manifest;start:number}>=({manifest,start})=>{const frame=useCurrentFrame();return <AtFrame manifest={manifest} frame={start+frame}/>;};
export const Proof:React.FC=()=>{
 const manifest=useManifest();if(!manifest)return null;let cursor=0;
 return <AbsoluteFill style={{background:'#101114'}}><Audio src={staticFile('generated/proof.wav')}/>{PROOF_CLIPS.map((clip,i)=>{const from=cursor;cursor+=clip.frames;return <Sequence key={i} from={from} durationInFrames={clip.frames}><ProofShot manifest={manifest} start={clip.start}/></Sequence>;})}</AbsoluteFill>;
};
