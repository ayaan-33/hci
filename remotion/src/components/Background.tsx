import React from 'react';
import {AbsoluteFill,Img,staticFile} from 'remotion';
import type {Camera} from '../types';
export const Background:React.FC<{camera:Camera;demo?:boolean}>=({camera,demo=false})=>{
 const scale=1.04+(2400-camera.eye[2])*.00002;
 return <AbsoluteFill style={{background:'#101114',overflow:'hidden'}}>
  <Img alt="" src={staticFile(`assets/backgrounds/${demo?'demo':'hero'}.png`)} style={{width:'100%',height:'100%',objectFit:'cover',transform:`translate(${-camera.eye[0]*.12}px,${camera.eye[1]*.10}px) scale(${scale})`,opacity:demo?.20:.44}}/>
  <AbsoluteFill style={{background:demo?'linear-gradient(90deg,rgba(10,11,14,.78),rgba(10,11,14,.15),rgba(10,11,14,.76))':'linear-gradient(90deg,rgba(10,11,14,.86),rgba(10,11,14,.35))'}}/>
  <AbsoluteFill style={{background:'radial-gradient(ellipse at 50% 40%,transparent 30%,rgba(0,0,0,.58) 100%)'}}/>
 </AbsoluteFill>;
};
