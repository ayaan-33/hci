import React from 'react';
import {Img,staticFile} from 'remotion';
import {SPEAKERS} from '../data/config';
import {clamp} from '../motion';
import type {SpeakerId,Voice} from '../types';
export const Avatar:React.FC<{speaker:SpeakerId;voice:Voice;frame:number;reading?:boolean;size?:number;showName?:boolean}>=({speaker,voice,frame,reading=false,size=300,showName=true})=>{
 const {accent,name}=SPEAKERS[speaker];const intensity=reading?.35:1;
 const scale=1+intensity*(.02*voice.amplitude+.006*voice.low);
 const bob=voice.low*(speaker==='immad'?9:5)*intensity;
 const twist=(speaker==='raj'?.8:speaker==='awais'?.4:0)*voice.mid*intensity;
 const halo=.10+voice.mid*.20*intensity;
 const live=reading?[]:voice.onsets.filter(n=>voice.localFrame>=n&&voice.localFrame<n+18).slice(-2);
 return <div style={{position:'relative',width:size,height:size+80,textAlign:'center'}}>
  <div style={{position:'absolute',inset:'12% 5% 15%',background:`radial-gradient(ellipse,${accent},transparent 68%)`,opacity:halo,filter:'blur(32px)',transform:`scale(${1+voice.low*.08})`}}/>
  <div style={{width:size,height:size,transform:`translateY(${-bob}px) scale(${scale}) rotate(${twist}deg)`,transformOrigin:'50% 88%'}}>
   <Img alt={`${name}'s abstract geometric avatar`} src={staticFile(`assets/avatars/${speaker}.png`)} style={{width:'100%',height:'100%',objectFit:'contain',filter:`drop-shadow(0 0 ${6+voice.high*14*intensity}px ${accent}40)`}}/>
  </div>
  {live.flatMap(n=>[0,1].map(i=>{const t=clamp((voice.localFrame-n)/18),sign=i?1:-1;return <div key={`${n}-${i}`} style={{position:'absolute',left:size/2+sign*(35+t*45),top:size*.45-t*75,width:5*(1-t),height:5*(1-t),borderRadius:'50%',background:accent,opacity:.35*(1-t)}}/>;}))}
  {showName?<div style={{position:'relative',fontSize:34,fontWeight:600,color:'#f2eee6',marginTop:8}}>{name}</div>:null}
 </div>;
};
