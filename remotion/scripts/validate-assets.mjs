import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
export const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
export function validateAssets({sourcesOnly=false}={}){
 const script=JSON.parse(fs.readFileSync(path.join(root,'src/data/script.json'),'utf8'));
 const board=JSON.parse(fs.readFileSync(path.join(root,'src/data/storyboard.json'),'utf8'));
 const required=[...script.map(s=>`assets/audio/${s.id}.ogg`),'assets/demos/scenario-1.mov','assets/demos/scenario-2.mov','assets/backgrounds/hero.png','assets/backgrounds/demo.png','assets/fonts/InterVariable.woff2',...['immad','raj','awais','raja'].map(x=>`assets/avatars/${x}.png`)];
 if(!sourcesOnly)required.push('generated/manifest.json','generated/narration.wav','generated/proof.wav',...['Raj-01','Raj-02','Raj-03'].map(x=>`generated/demos/${x}.mp4`));
 const missing=required.filter(f=>!fs.existsSync(path.join(root,'public',f)));
 if(missing.length)throw new Error(`Missing assets:\n${missing.join('\n')}\nSee README.md; run scripts/import-assets.py then scripts/prepare.py.`);
 const integrity=JSON.parse(fs.readFileSync(path.join(root,'src/data/source-integrity.json'),'utf8'));
 for(const [relative,expected] of Object.entries(integrity))if(hash(path.join(root,'public',relative))!==expected)throw new Error(`Original source changed: ${relative}. Re-author the cue map before replacing a take.`);
 if(sourcesOnly)return null;
 const manifest=JSON.parse(fs.readFileSync(path.join(root,'public/generated/manifest.json'),'utf8'));
 if(manifest.schemaVersion!==1||manifest.fps!==30||manifest.width!==3840||manifest.height!==1920)throw new Error('Unsupported prepared manifest.');
 if(manifest.sections.length!==script.length)throw new Error('Missing narrated sections.');
 let cursor=540;
 for(const section of manifest.sections){
  if(section.startFrame!==cursor)throw new Error(`Gap before ${section.id}`);cursor=section.endFrame;
  const beats=board[section.id];let local=0;
  for(const beat of beats){if(!Array.isArray(beat.camera)||beat.camera.length!==2||beat.camera.some(p=>!['N','H','W','L','R','G','A'].includes(p))||!Number.isInteger(beat.sweep)||beat.sweep<=0||beat.sweep>beat.end-beat.start||beat.start!==local||beat.end<=beat.start)throw new Error(`Invalid beat coverage in ${section.id}`);local=beat.end;}
  if(local!==section.endFrame-section.startFrame)throw new Error(`Storyboard does not cover ${section.id}`);
  if(!section.features.values.length||section.features.values.some(a=>a.length!==4||a.some(v=>!Number.isFinite(v)||v<0||v>1)))throw new Error(`Invalid voice data: ${section.id}`);
 }
 if(manifest.durationFrames!==cursor+240)throw new Error('Invalid ending duration.');
 for(const [key,info] of Object.entries(manifest.demos)){
  const file=path.join(root,'public',info.file);if(hash(file)!==info.sha256)throw new Error(`Conformed demo has changed: ${key}. Re-run preparation.`);
  const meta=JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-of','json',file],{encoding:'utf8'}));const video=meta.streams.find(s=>s.codec_type==='video');
  if(!video||Number(video.nb_frames)!==info.frames||Math.abs(Number(video.start_time??0))>.001||video.width!==2320||video.height!==1582)throw new Error(`Invalid conformed video: ${key}`);
  if(meta.streams.some(s=>s.codec_type==='audio'))throw new Error(`Demo audio must be muted/removed: ${key}`);
 }
 const audio=JSON.parse(execFileSync('ffprobe',['-v','error','-select_streams','a:0','-show_entries','stream=sample_rate,duration_ts','-of','json',path.join(root,'public/generated/narration.wav')],{encoding:'utf8'})).streams[0];
 if(Number(audio.sample_rate)!==48000||Number(audio.duration_ts)!==manifest.masterSamples)throw new Error('Master audio is not sample-aligned to the film.');
 return manifest;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 try{const m=validateAssets({sourcesOnly:process.argv.includes('--sources-only')});console.log(m?`Validated ${m.sections.length} sections, ${m.durationFrames} frames, 3 source-aligned demos.`:'Source assets are complete.');}
 catch(e){console.error(e.message);process.exitCode=1;}
}
