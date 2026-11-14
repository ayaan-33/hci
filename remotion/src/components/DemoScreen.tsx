import React from 'react';
import {OffthreadVideo,Sequence,staticFile,useCurrentFrame} from 'remotion';
import {enterEase} from '../motion';
import {Plane,Glass} from './Plane';
import type {Camera,Manifest,Section,Vec3} from '../types';
/** Negative Sequence offsets also align video correctly in the non-linear proof montage. */
const SyncedVideo:React.FC<{src:string;localFrame:number}>=({src,localFrame})=>{
 const contextFrame=useCurrentFrame();
 return <Sequence from={contextFrame-localFrame} layout="none"><OffthreadVideo src={staticFile(src)} muted style={{width:'100%',height:'100%',objectFit:'fill',display:'block'}}/></Sequence>;
};
export const DemoScreen:React.FC<{section:Section;localFrame:number;camera:Camera;manifest:Manifest}>=({section,localFrame,camera,manifest})=>{
 const p=enterEase(localFrame/24);const center:Vec3=[0,45-180*(1-p),120-300*(1-p)];
 const file=manifest.demos[section.id];if(!file)throw new Error(`Missing conformed video for ${section.id}. Run scripts/prepare.py.`);
 return <>
  <Plane width={2160} height={1498} center={center} angles={[7*(1-p),-9*(1-p),0]} camera={camera} opacity={.3+.7*p} contain={{x:720,y:195,width:2400,height:1510}}>
   <Glass accent="#82a9e7" style={{padding:40,borderRadius:42,background:'linear-gradient(130deg,rgba(210,218,232,.18),rgba(18,23,29,.94))'}}>
    <div style={{width:2080,height:1418,overflow:'hidden',borderRadius:16,background:'#0c171d'}}><SyncedVideo src={file.file} localFrame={localFrame}/></div>
   </Glass>
  </Plane>
  <div style={{position:'absolute',left:180,top:1180,width:440,fontSize:28,lineHeight:1.45,color:'#aeb4bc',zIndex:25000}}>
   Original prototype recording<br/>Playback retimed to narration<br/>Displayed timers are original<br/><span style={{color:'#d6ab69'}}>Scripted chat · illustrative n = 1</span>
  </div>
 </>;
};
