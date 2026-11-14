import React from 'react';
import {planeMatrix} from '../geometry';
import type {Camera,Vec3} from '../types';
export const Plane:React.FC<{width:number;height:number;center:Vec3;camera:Camera;angles?:Vec3;opacity?:number;contain?:{x:number;y:number;width:number;height:number};style?:React.CSSProperties;children:React.ReactNode}> =({width,height,center,camera,angles=[0,0,0],opacity=1,contain,style,children})=>(
 <div style={{position:'absolute',left:0,top:0,width,height,transformOrigin:'0 0',transform:planeMatrix(width,height,center,angles,camera,contain),opacity,zIndex:Math.round(10000+center[2]),backfaceVisibility:'hidden',...style}}>{children}</div>
);
export const Glass:React.FC<{children:React.ReactNode;accent?:string;style?:React.CSSProperties}>=({children,accent='#d6ab69',style})=>(
 <div style={{width:'100%',height:'100%',boxSizing:'border-box',borderRadius:34,background:'linear-gradient(135deg,rgba(218,222,231,.13),rgba(31,35,43,.72))',border:'2px solid rgba(240,240,240,.24)',boxShadow:`inset 0 1px 1px rgba(255,255,255,.22),inset 0 -8px 24px rgba(0,0,0,.3),0 28px 70px rgba(0,0,0,.48),-4px 0 12px ${accent}24`,overflow:'hidden',...style}}>{children}</div>
);
