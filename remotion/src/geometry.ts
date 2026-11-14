/** Actual pinhole camera + projective corner pin. All world units are design pixels.
 * +X right, +Y up, +Z toward the viewer. No WebGL or implicit CSS camera state.
 */
import type {Camera,Vec3} from './types';
export type Point=readonly[number,number];
const sub=(a:Vec3,b:Vec3):Vec3=>[a[0]-b[0],a[1]-b[1],a[2]-b[2]];
const dot=(a:Vec3,b:Vec3)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
const cross=(a:Vec3,b:Vec3):Vec3=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const unit=(a:Vec3):Vec3=>{const n=Math.hypot(...a);if(n<1e-9)throw new Error('Degenerate camera');return [a[0]/n,a[1]/n,a[2]/n];};
export function project(p:Vec3,camera:Camera):Point{
 const forward=unit(sub(camera.target,camera.eye)),right=unit(cross(forward,[0,1,0])),up=cross(right,forward),d=sub(p,camera.eye);const depth=dot(d,forward);
 if(depth<100)throw new Error('Layer crossed the camera near plane');
 return [1920+2400*dot(d,right)/depth,960-2400*dot(d,up)/depth];
}
export function rotate(p:Vec3,angles:Vec3):Vec3{
 const [rx,ry,rz]=angles.map(v=>v*Math.PI/180);let [x,y,z]=p;
 [y,z]=[y*Math.cos(rx)-z*Math.sin(rx),y*Math.sin(rx)+z*Math.cos(rx)];
 [x,z]=[x*Math.cos(ry)+z*Math.sin(ry),-x*Math.sin(ry)+z*Math.cos(ry)];
 return [x*Math.cos(rz)-y*Math.sin(rz),x*Math.sin(rz)+y*Math.cos(rz),z];
}
export function homography(w:number,h:number,quad:readonly Point[]):number[]{
 const source:Point[]=[[0,0],[w,0],[w,h],[0,h]],a:number[][]=[];
 source.forEach(([x,y],i)=>{const [u,v]=quad[i];a.push([x,y,1,0,0,0,-u*x,-u*y,u],[0,0,0,x,y,1,-v*x,-v*y,v]);});
 for(let c=0;c<8;c++){
  let p=c;for(let r=c+1;r<8;r++)if(Math.abs(a[r][c])>Math.abs(a[p][c]))p=r;
  [a[c],a[p]]=[a[p],a[c]];const pivot=a[c][c];if(Math.abs(pivot)<1e-10)throw new Error('Degenerate projective quad');
  for(let k=c;k<=8;k++)a[c][k]/=pivot;
  for(let r=0;r<8;r++)if(r!==c){const factor=a[r][c];for(let k=c;k<=8;k++)a[r][k]-=factor*a[c][k];}
 }
 return [...a.map(r=>r[8]),1];
}
export const cssMatrix=(h:number[])=>`matrix3d(${[h[0],h[3],0,h[6],h[1],h[4],0,h[7],0,0,1,0,h[2],h[5],0,1].map(v=>Number(v.toFixed(10))).join(',')})`;
export function planeMatrix(w:number,h:number,center:Vec3,angles:Vec3,camera:Camera,contain?:{x:number;y:number;width:number;height:number}):string{
 const corners:Vec3[]=[[-w/2,h/2,0],[w/2,h/2,0],[w/2,-h/2,0],[-w/2,-h/2,0]];
 const quad=corners.map(p=>{const q=rotate(p,angles);return project([q[0]+center[0],q[1]+center[1],q[2]+center[2]],camera);});
 let fitted=quad;
 if(contain){
  const xs=quad.map(p=>p[0]),ys=quad.map(p=>p[1]),minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys);
  const k=Math.min(1,contain.width/(maxX-minX),contain.height/(maxY-minY));
  const cx=(minX+maxX)/2,cy=(minY+maxY)/2,bw=(maxX-minX)*k,bh=(maxY-minY)*k;
  const tx=Math.min(contain.x+contain.width-bw/2,Math.max(contain.x+bw/2,cx));
  const ty=Math.min(contain.y+contain.height-bh/2,Math.max(contain.y+bh/2,cy));
  fitted=quad.map(([x,y])=>[(x-cx)*k+tx,(y-cy)*k+ty] as Point);
 }
 return cssMatrix(homography(w,h,fitted));
}
