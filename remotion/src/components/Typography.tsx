import React from 'react';
import {clamp,enterEase} from '../motion';
export const KineticText:React.FC<{text:string;frame:number;delay?:number;size?:number;style?:React.CSSProperties;accent?:string}>=({text,frame,delay=12,size=112,style,accent})=>(
 <div style={{fontSize:size,lineHeight:1.07,fontWeight:650,letterSpacing:'-.035em',color:accent??'#f4f1eb',...style}}>
  {text.split(' ').map((word,i)=>{const p=enterEase(clamp((frame-delay-i*3)/10));return <React.Fragment key={`${i}-${word}`}><span style={{display:'inline-block',opacity:p,transform:`translateY(${24*(1-p)}px)`}}>{word}</span>{' '}</React.Fragment>;})}
 </div>
);
export const Eyebrow:React.FC<{children:React.ReactNode;accent:string;style?:React.CSSProperties}>=({children,accent,style})=><div style={{fontSize:32,fontWeight:600,letterSpacing:'.12em',textTransform:'uppercase',color:accent,...style}}>{children}</div>;
