import test from 'node:test';
import assert from 'node:assert/strict';
import script from '../src/data/script.json';
import maps from '../src/data/demo-map.json';
import {FILM_FRAMES,STORYBOARD} from '../src/data/config';
import {cameraAt,featureAt} from '../src/motion';

test('all ten sections have continuous frame coverage and exact decoded sample totals',()=>{
 let samples=18*48000,frame=540;
 for(const s of script){assert.equal(Math.round(samples/48000*30),frame);const end=Math.round((samples+s.samples)/48000*30);let f=0;for(const b of STORYBOARD[s.id]){assert.equal(b.start,f);assert.ok(b.end>b.start);assert.ok(b.camera.length===2);f=b.end;}assert.equal(f,end-frame);samples+=s.samples;frame=end;}
 assert.equal(FILM_FRAMES,13818);assert.equal(frame+240,FILM_FRAMES);assert.equal(samples-18*48000,20860536);
});
test('Raj maps retain all frames and their verified first-visible source states',()=>{
 for(const map of Object.values(maps)){let f=0;for(const p of map.pieces){assert.equal(p.from,f);assert.ok(p.to>p.from);f=p.to;}assert.equal(f,map.frames);}
 assert.equal(maps['Raj-01'].pieces[3].holdFrame,373);
 assert.equal(maps['Raj-01'].pieces[5].holdFrame,1050);
 assert.equal(maps['Raj-02'].pieces[4].holdFrame,687);
 assert.equal(maps['Raj-03'].pieces[1].holdFrame,1164);
 assert.equal(maps['Raj-03'].pieces[4].holdFrame,1856);
});
test('camera output is independent of rendering order and returns neutral at cuts',()=>{
 const beat=STORYBOARD['Raj-01'][2];const a=cameraAt(beat,600,1516);cameraAt(beat,790,1516);assert.deepEqual(cameraAt(beat,600,1516),a);
 const last=STORYBOARD['Raj-01'].at(-1)!;const neutral=cameraAt(last,1515,1516);assert.ok(Math.abs(neutral.eye[2]-2400)<.01);
});
test('voice sampling is bounded and interpolated without mutable animation state',()=>{
 const f={hopSamples:1600,windowSamples:4096,bandsHz:[],values:[[0,0,0,0],[1,.8,.6,.4]],onsets:[]};
 assert.deepEqual(featureAt(f,-1),[0,0,0,0]);assert.deepEqual(featureAt(f,.5),[.5,.4,.3,.2]);assert.deepEqual(featureAt(f,999),[1,.8,.6,.4]);
});
