import React from 'react';
import {AbsoluteFill,Img,staticFile} from 'remotion';
import {SPEAKERS,STORYBOARD,speakerId,REFERENCES} from '../data/config';
import {beatAt,cameraAt,clamp,enterEase,POSES,voiceAt} from '../motion';
import {Avatar} from './Avatar';
import {Background} from './Background';
import {DemoScreen} from './DemoScreen';
import {EditorialPanels} from './EditorialPanels';
import {Eyebrow,KineticText} from './Typography';
import {Glass,Plane} from './Plane';
import type {Manifest,Section,Voice,SpeakerId} from '../types';
const SILENT:Voice={amplitude:0,low:0,mid:0,high:0,onsets:[],localFrame:0};
const Team:React.FC<{localFrame:number;globalFrame:number;voice:Voice;active:SpeakerId}>=({localFrame})=>{
 const order:SpeakerId[]=['raja','raj','awais','immad'];
 return <div style={{position:'absolute',left:220,top:550,display:'flex',gap:210,zIndex:21000}}>{order.map((id,i)=>{const e=enterEase((localFrame-i*5)/24);return <div key={id} style={{width:640,opacity:e,transform:`translateY(${60*(1-e)}px)`}}><Img src={staticFile(`assets/portraits/${id}.png`)} alt={SPEAKERS[id].name} style={{width:640,height:900,objectFit:'contain',display:'block'}}/><div style={{textAlign:'center',fontSize:43,fontWeight:550,color:'#e9e5dd',marginTop:35}}>{SPEAKERS[id].name}</div></div>;})}</div>;
};
const Captions:React.FC<{section:Section;frame:number}>=({section,frame})=>{
 const t=frame/30-section.audioStartSamples/48000;const cue=section.captions.find(c=>t>=c.start&&t<c.end);
 if(!cue)return null;
 return <div style={{position:'absolute',left:560,right:560,bottom:55,textAlign:'center',zIndex:50000,fontSize:54,lineHeight:1.27,color:'#f5f3ee'}}><span style={{background:'rgba(7,9,12,.88)',boxDecorationBreak:'clone',WebkitBoxDecorationBreak:'clone',padding:'14px 26px',borderRadius:18}}>{cue.text}</span></div>;
};
export const Scene:React.FC<{manifest:Manifest;section:Section;globalFrame:number}>=({manifest,section,globalFrame})=>{
 const local=globalFrame-section.startFrame;const length=section.endFrame-section.startFrame;const beat=beatAt(STORYBOARD[section.id],local);const phase=local-beat.start;const camera=cameraAt(beat,local,length);const id=speakerId(section.id),voice=voiceAt(section,globalFrame),accent=SPEAKERS[id].accent;const isDemo=beat.kind==='demo';
 const sidebarX=isDemo&&camera.target[0]>100?3240:180;
 const contentOpacity=clamp(local/12)*clamp((length-local)/12);
 return <AbsoluteFill style={{fontFamily:'Inter,sans-serif',color:'#f4f1eb',overflow:'hidden'}}>
  <Background camera={camera} demo={isDemo}/>
  <div style={{position:'absolute',left:180,right:180,top:90,display:'flex',justifyContent:'space-between',fontSize:29,fontWeight:550,letterSpacing:'.1em',color:'#b9bec8',zIndex:40000}}><span>teamGARI <span style={{color:accent}}>/ C-10</span></span><span>{section.title.toUpperCase()}</span></div>
  <AbsoluteFill style={{opacity:contentOpacity}}>
   {isDemo?<DemoScreen section={section} localFrame={local} camera={camera} manifest={manifest}/>:beat.kind==='team'?<Team localFrame={phase} globalFrame={globalFrame} voice={voice} active={id}/>:<EditorialPanels beat={beat} frame={local} camera={camera} accent={accent}/>}
   <div style={{position:'absolute',left:isDemo?sidebarX:220,top:isDemo?350:285,width:isDemo?440:1440,zIndex:26000}}>
    <Eyebrow accent={accent} style={{fontSize:isDemo?26:32,marginBottom:isDemo?30:46}}>{beat.eyebrow}</Eyebrow>
    <KineticText key={`${section.id}-${beat.start}`} text={beat.headline} frame={phase} delay={beat.textDelay??12} size={isDemo?57:112} style={beat.kind==='team'?{width:3100}:undefined}/>
    {isDemo?<div style={{marginTop:46,fontSize:39,lineHeight:1.4,color:'#c4c9d0'}}>{beat.lines.map((v,i)=><div key={v} style={{marginTop:24,opacity:enterEase((phase-(beat.linesDelay??30)-i*12)/18)}}>{v}</div>)}</div>:null}
   </div>
   {beat.kind!=='team'?<div style={{position:'absolute',left:180,top:1480,zIndex:30000}}><Avatar speaker={id} voice={voice} frame={globalFrame} size={205} reading={isDemo}/></div>:null}
   {!isDemo&&['disclosure','metrics','timing','errors','control'].includes(beat.kind)?<div style={{position:'absolute',left:1880,top:1440,width:1650,fontSize:30,color:'#c6b28f',zIndex:26000}}>Scripted simulation · one team member’s illustrative run · n = 1</div>:null}
  </AbsoluteFill>
  <Captions section={section} frame={globalFrame}/>
 </AbsoluteFill>;
};
export const ColdOpen:React.FC<{frame:number}>=({frame})=>{
 const stage=frame<90?0:frame<240?1:frame<420?2:3;const starts=[0,90,240,420],phase=frame-starts[stage];
 const camera={...POSES.N,eye:[0,0,2680-420*enterEase(Math.min(frame,420)/420)] as const};
 const headlines=['A conversation.','Confirmed.','But is it correct?','Chat or form?'];
 return <AbsoluteFill style={{fontFamily:'Inter,sans-serif',background:'#101114'}}><Background camera={camera}/>
  <div style={{position:'absolute',left:220,top:300,width:1600,zIndex:30000}}><Eyebrow accent="#d6ab69" style={{marginBottom:55}}>A TOOL TALK ABOUT STRUCTURED INFORMATION</Eyebrow><KineticText key={stage} text={headlines[stage]} frame={phase} size={144}/><div style={{marginTop:60,fontSize:45,lineHeight:1.4,color:'#b6bcc6',opacity:enterEase((phase-28)/30)}}>{stage===2?'A saved record can still contain the wrong information.':stage===3?'Time. Information. Control.':' '}</div></div>
  <Plane width={1320} height={1000} center={[650,30,140]} angles={[5,-8,-2]} camera={camera}><Glass accent="#d6ab69"><div style={{height:'100%',display:'grid',placeItems:'center',position:'relative'}}><svg width="510" height="510" viewBox="0 0 100 100" style={{opacity:stage===2?.26:.92,transform:`scale(${1+.025*Math.sin(frame/45)})`}}><circle cx="50" cy="50" r="40" fill="none" stroke="#d6ab6940" strokeWidth="1"/><path d="M27 50 43 66 75 32" fill="none" stroke={stage===2?'#d6ab69':'#dfded5'} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>{stage===2?<div style={{position:'absolute',bottom:120,left:100,right:100,textAlign:'center',fontSize:54,color:'#ddb876'}}>What did the system record?</div>:null}</div></Glass></Plane>
  <div style={{position:'absolute',left:220,bottom:140,fontSize:34,letterSpacing:'.08em',color:'#a6adb7'}}>TEAM C-10 / teamGARI</div>
 </AbsoluteFill>;
};
export const Credits:React.FC<{frame:number}>=({frame})=>{
 const second=frame>=120;const refs=second?REFERENCES.slice(4):REFERENCES.slice(0,4);const fade=clamp((240-frame)/18);
 return <AbsoluteFill style={{fontFamily:'Inter,sans-serif',background:'#101114'}}><Background camera={POSES.N}/><AbsoluteFill style={{padding:'190px 220px',boxSizing:'border-box',opacity:fade}}><Eyebrow accent="#d6ab69">SOURCES & PRODUCTION</Eyebrow><div style={{fontSize:105,fontWeight:600,letterSpacing:'-.03em',color:'#f0ede5',marginTop:45}}>References</div><div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:70,marginTop:85}}>{refs.map(([title,sub])=><div key={title} style={{borderTop:'1px solid #ffffff30',paddingTop:32,minHeight:190}}><div style={{fontSize:43,lineHeight:1.3,color:'#ede8df'}}>{title}</div><div style={{fontSize:33,lineHeight:1.4,color:'#aeb6c2',marginTop:24}}>{sub}</div></div>)}</div><div style={{position:'absolute',left:220,right:220,bottom:130,fontSize:31,lineHeight:1.6,color:'#aab2bf'}}>Original narration and prototype: Team C-10 / teamGARI.<br/>Concept images, editing and animation assisted by OpenAI tools. Speaker portraits use the team-approved cutout assets.</div></AbsoluteFill></AbsoluteFill>;
};
