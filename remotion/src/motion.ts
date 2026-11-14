import type {Beat,Camera,FeatureSet,PoseId,Vec3,Voice,Section} from './types';
export const clamp=(v:number,min=0,max=1)=>Math.min(max,Math.max(min,v));
export const mix=(a:number,b:number,t:number)=>a+(b-a)*t;
export const mix3=(a:Vec3,b:Vec3,t:number):Vec3=>[mix(a[0],b[0],t),mix(a[1],b[1],t),mix(a[2],b[2],t)];
/** Invert cubic Bezier x(t) before evaluating y(t), matching AE/CSS timing curves. */
export const bezierEase=(u:number,x1=.42,y1=0,x2=.58,y2=1)=>{
 const x=clamp(u);let lo=0,hi=1;
 const B=(t:number,a:number,b:number)=>3*(1-t)**2*t*a+3*(1-t)*t*t*b+t*t*t;
 for(let i=0;i<18;i++){const t=(lo+hi)/2;if(B(t,x1,x2)<x)lo=t;else hi=t;}
 return B((lo+hi)/2,y1,y2);
};
export const enterEase=(u:number)=>bezierEase(u,.16,1,.3,1);
export const POSES:Record<PoseId,Camera>={
 N:{eye:[0,0,2400],target:[0,0,0]},H:{eye:[0,0,2240],target:[0,100,80]},
 W:{eye:[0,0,2680],target:[0,0,0]},L:{eye:[-120,25,2340],target:[-360,0,100]},
 R:{eye:[120,25,2340],target:[360,0,100]},G:{eye:[0,75,2360],target:[0,80,120]},A:{eye:[0,0,2540],target:[0,0,0]},
};
const cubic3=(a:Vec3,p:Vec3,q:Vec3,b:Vec3,t:number):Vec3=>[0,1,2].map(i=>(1-t)**3*a[i]+3*(1-t)**2*t*p[i]+3*(1-t)*t*t*q[i]+t**3*b[i]) as unknown as Vec3;
export const cameraAt=(beat:Beat,localFrame:number,sectionLength:number):Camera=>{
 const a=POSES[beat.camera[0]],b=POSES[beat.camera[1]];const t=bezierEase((localFrame-beat.start)/Math.max(1,beat.sweep-1));
 const direction=Math.sign(b.eye[0]-a.eye[0]);const bulge:Vec3=[direction*40,-12*direction,0];
 const p=mix3(a.eye,b.eye,1/3).map((v,i)=>v+bulge[i]) as unknown as Vec3;
 const q=mix3(a.eye,b.eye,2/3).map((v,i)=>v+bulge[i]) as unknown as Vec3;
 const eye=cubic3(a.eye,p,q,b.eye,t),target=mix3(a.target,b.target,t);
 const exit=bezierEase((localFrame-(sectionLength-18))/17);
 return {eye:mix3(eye,POSES.N.eye,exit),target:mix3(target,POSES.N.target,exit)};
};
export const beatAt=(beats:Beat[],frame:number):Beat=>beats.find(b=>frame>=b.start&&frame<b.end)??beats[beats.length-1];
export const featureAt=(features:FeatureSet,index:number):number[]=>{
 if(index<0||features.values.length===0)return [0,0,0,0];
 const i=Math.min(Math.floor(index),features.values.length-1),j=Math.min(i+1,features.values.length-1),t=clamp(index-i);
 return features.values[i].map((v,k)=>mix(v,features.values[j][k],t));
};
export const voiceAt=(section:Section,globalFrame:number):Voice=>{
 const f=(globalFrame/30-section.audioStartSamples/48000)*30;
 const [amplitude,low,mid,high]=featureAt(section.features,f);
 return {amplitude,low,mid,high,localFrame:f,onsets:section.features.onsets};
};
export const fade=(frame:number,start:number,end:number,fadeFrames=15)=>clamp((frame-start)/fadeFrames)*clamp((end-frame)/fadeFrames);
