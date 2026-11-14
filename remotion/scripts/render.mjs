#!/usr/bin/env node
/** Resumable, bounded-concurrency rendering. Video-only chunks + ONE PCM/AAC mux
 * prevent AAC encoder-delay accumulation at chunk boundaries. No API keys. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {bundle} from '@remotion/bundler';
import {openBrowser,renderMedia,selectComposition} from '@remotion/renderer';
import {root,validateAssets} from './validate-assets.mjs';
function argsOf(argv){const o={};for(let i=0;i<argv.length;i++){const a=argv[i];if(!a.startsWith('--'))throw new Error(`Unexpected argument ${a}`);if(argv[i+1]&&!argv[i+1].startsWith('--'))o[a.slice(2)]=argv[++i];else o[a.slice(2)]=true;}return o;}
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).sort((a,b)=>a.name.localeCompare(b.name)).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):[path.join(dir,e.name)]);}
function findBrowser(explicit){
 if(explicit)return path.resolve(String(explicit));if(process.env.REMOTION_BROWSER_EXECUTABLE)return process.env.REMOTION_BROWSER_EXECUTABLE;
 const candidates=process.platform==='darwin'?['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome']:process.platform==='win32'?[path.join(process.env.PROGRAMFILES??'C:/Program Files','Google/Chrome/Application/chrome.exe')]:['/usr/bin/chromium','/usr/bin/chromium-browser','/usr/bin/google-chrome'];
 return candidates.find(p=>fs.existsSync(p));
}
function validChunk(file,frames,width,height){
 if(!fs.existsSync(file))return false;
 try{const d=JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-of','json',file],{encoding:'utf8'}));const v=d.streams.find(s=>s.codec_type==='video');return !!v&&Number(v.nb_frames)===frames&&v.width===width&&v.height===height&&!d.streams.some(s=>s.codec_type==='audio');}catch{return false;}
}
let browser;
process.once('SIGINT',async()=>{console.error('Interrupted; complete chunks are reusable.');if(browser)await browser.close({silent:true});process.exit(130);});
try{
 process.chdir(root);const args=argsOf(process.argv.slice(2));const allowed=new Set(['quality','composition','scale','chunk','concurrency','browser','frames','output']);
 for(const k of Object.keys(args))if(!allowed.has(k))throw new Error(`Unknown option --${k}`);
 const manifest=validateAssets();const id=args.composition??'Film';if(!['Film','Proof'].includes(id))throw new Error('composition must be Film or Proof');
 const quality=args.quality??'preview';if(!['preview','final'].includes(quality))throw new Error('quality must be preview or final');
 const scale=Number(args.scale??(quality==='final'?1:.5));if(![.25,.5,1].includes(scale))throw new Error('scale must be .25, .5, or 1');
 const chunkFrames=Number(args.chunk??900),concurrency=Number(args.concurrency??2);
 if(!Number.isInteger(chunkFrames)||chunkFrames<30)throw new Error('chunk must be an integer >=30');
 if(!Number.isInteger(concurrency)||concurrency<1||concurrency>8)throw new Error('concurrency must be 1..8');
 const fingerprint=crypto.createHash('sha256');
 for(const f of [...walk(path.join(root,'src')),...walk(path.join(root,'public')),path.join(root,'package-lock.json'),path.join(root,'scripts/render.mjs'),path.join(root,'remotion.config.ts')]){fingerprint.update(path.relative(root,f));fingerprint.update(fs.readFileSync(f));}
 fingerprint.update(JSON.stringify({id,scale,quality,chunkFrames}));const cacheKey=fingerprint.digest('hex').slice(0,18);
 const cacheDir=path.join(root,'.cache/render',cacheKey);fs.mkdirSync(cacheDir,{recursive:true});fs.mkdirSync(path.join(root,'out'),{recursive:true});
 const browserExecutable=findBrowser(args.browser);const chromiumOptions={};
 console.log('Bundling local project (assets and font are offline)…');
 const serveUrl=await bundle({entryPoint:path.join(root,'src/index.ts'),publicDir:path.join(root,'public')});
 browser=await openBrowser('chrome',{browserExecutable,chromiumOptions});
 const composition=await selectComposition({serveUrl,id,puppeteerInstance:browser,chromiumOptions});
 const range=args.frames?String(args.frames).split('-').map(Number):[0,composition.durationInFrames-1];
 if(range.length!==2||range.some(v=>!Number.isInteger(v))||range[0]<0||range[1]>=composition.durationInFrames||range[1]<range[0])throw new Error('--frames must be an inclusive valid START-END range');
 const start=range[0],end=range[1]+1;const files=[];const width=composition.width*scale,height=composition.height*scale;
 for(let from=start;from<end;from+=chunkFrames){
  const to=Math.min(end,from+chunkFrames);const file=path.join(cacheDir,`${String(from).padStart(6,'0')}-${String(to).padStart(6,'0')}.mp4`);files.push(file);
  if(validChunk(file,to-from,width,height)){console.log(`Resume: ${from}–${to-1}`);continue;}
  console.log(`Rendering ${id}: frames ${from}–${to-1} at ${width}×${height}`);let logged=-1;
  await renderMedia({composition,serveUrl,puppeteerInstance:browser,chromiumOptions,codec:'h264',outputLocation:file,frameRange:[from,to-1],scale,concurrency,muted:true,imageFormat:'jpeg',jpegQuality:95,crf:quality==='final'?18:21,x264Preset:'veryfast',pixelFormat:'yuv420p',offthreadVideoThreads:2,offthreadVideoCacheSizeInBytes:256*1024*1024,mediaCacheSizeInBytes:256*1024*1024,timeoutInMilliseconds:120000,onProgress:p=>{const n=Math.floor(p.progress*10);if(n!==logged){logged=n;console.log(`  ${n*10}%`);}}});
  if(!validChunk(file,to-from,width,height))throw new Error(`Incomplete chunk: ${file}. Re-run to retry it.`);
 }
 const list=path.join(cacheDir,'chunks.ffconcat');const q=p=>p.replaceAll('\\','/').replaceAll("'","'\\''");fs.writeFileSync(list,files.map(f=>`file '${q(f)}'`).join('\n')+'\n');
 const audio=path.join(root,'public/generated',id==='Proof'?'proof.wav':'narration.wav');
 const suffix=args.frames?`-${start}-${end-1}`:'';const output=path.resolve(root,String(args.output??`out/${id.toLowerCase()}-${quality}-${width}x${height}${suffix}.mp4`));fs.mkdirSync(path.dirname(output),{recursive:true});
 console.log('Muxing one continuous audio track…');
 execFileSync('ffmpeg',['-y','-v','error','-f','concat','-safe','0','-i',list,'-ss',String(start/30),'-i',audio,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',String((end-start)/30),'-movflags','+faststart',output],{stdio:'inherit'});
 console.log(`DONE: ${output}`);
}catch(e){console.error(e.stack??e);process.exitCode=1;}finally{if(browser)await browser.close({silent:true});}
