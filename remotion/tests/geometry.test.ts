import test from 'node:test';
import assert from 'node:assert/strict';
import {homography,planeMatrix,project} from '../src/geometry';
import {POSES} from '../src/motion';

test('neutral pinhole projection preserves centre and the correct depth scale',()=>{
 assert.deepEqual(project([0,0,0],POSES.N),[1920,960]);
 assert.deepEqual(project([100,100,0],POSES.N),[2020,860]);
 const p=project([100,0,120],POSES.N);assert.ok(Math.abs(p[0]-(1920+100*2400/2280))<1e-8);
});
test('projective corner pin maps every corner to its destination, not an affine approximation',()=>{
 const q=[[100,80],[980,20],[1080,720],[20,650]] as const;const h=homography(1000,700,q);const corners=[[0,0],[1000,0],[1000,700],[0,700]];
 corners.forEach(([x,y],i)=>{const d=h[6]*x+h[7]*y+1;assert.ok(Math.abs((h[0]*x+h[1]*y+h[2])/d-q[i][0])<1e-6);assert.ok(Math.abs((h[3]*x+h[4]*y+h[5])/d-q[i][1])<1e-6);});
});
test('near-plane failures are explicit and the reading-safe transform remains finite',()=>{
 assert.throws(()=>project([0,0,2390],POSES.N));
 const matrix=planeMatrix(2160,1498,[0,45,120],[0,0,0],POSES.H,{x:720,y:195,width:2400,height:1510});assert.ok(matrix.startsWith('matrix3d('));assert.ok(!matrix.includes('NaN'));
});
