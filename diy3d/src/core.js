import * as THREE from 'three';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';
import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';
import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js';
import {OutputPass} from 'three/addons/postprocessing/OutputPass.js';
export {THREE,RoundedBoxGeometry};
export const canvas=document.createElement('canvas');document.body.appendChild(canvas);
export const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true,preserveDrawingBuffer:true});
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.0;renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.setPixelRatio(1);
const pm=new THREE.PMREMGenerator(renderer);
export const ENV=pm.fromScene(new RoomEnvironment(),0.04).texture;
// ---------- noise ----------
function hash(x,y,s){let h=(x*374761393+y*668265263+s*982451653)|0;h=(h^(h>>>13))*1274126177|0;return ((h^(h>>>16))>>>0)/4294967295}
function vnoise(x,y,s){const xi=Math.floor(x),yi=Math.floor(y),xf=x-xi,yf=y-yi;const u=xf*xf*(3-2*xf),v=yf*yf*(3-2*yf);
  const a=hash(xi,yi,s),b=hash(xi+1,yi,s),c=hash(xi,yi+1,s),d=hash(xi+1,yi+1,s);return a+(b-a)*u+(c-a)*v+(a-b-c+d)*u*v}
export function fbm(x,y,oct=4,s=1){let t=0,a=.5,f=1,n=0;for(let i=0;i<oct;i++){t+=a*vnoise(x*f,y*f,s+i*17);n+=a;a*=.5;f*=2}return t/n}
export function canvasFrom(w,h,fn){const c=document.createElement('canvas');c.width=w;c.height=h;const ctx=c.getContext('2d');const im=ctx.createImageData(w,h);
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){const [r,g,b,a]=fn(x,y);const i=(y*w+x)*4;im.data[i]=r;im.data[i+1]=g;im.data[i+2]=b;im.data[i+3]=a===undefined?255:a}
  ctx.putImageData(im,0,0);return c}
export function heightToNormal(hf,w,h,str=2){return canvasFrom(w,h,(x,y)=>{const l=hf(Math.max(0,x-1),y),r=hf(Math.min(w-1,x+1),y),u=hf(x,Math.max(0,y-1)),d=hf(x,Math.min(h-1,y+1));
  let nx=(l-r)*str,ny=(u-d)*str,nz=1;const L=Math.hypot(nx,ny,nz);return [(nx/L*.5+.5)*255,(ny/L*.5+.5)*255,(nz/L*.5+.5)*255]})}
export function tex(c,{srgb=true,rep=[1,1]}={}){const t=new THREE.CanvasTexture(c);if(srgb)t.colorSpace=THREE.SRGBColorSpace;t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(rep[0],rep[1]);t.anisotropy=8;return t}
// cached generic maps
const cache={};
export function brushedMaps(){if(cache.br)return cache.br;const N=512;const hv=new Float32Array(N*N);
  for(let y=0;y<N;y++)for(let x=0;x<N;x++)hv[y*N+x]=fbm(x/180,y/1.2,3,5);
  const rough=canvasFrom(N,N,(x,y)=>{const v=150+hv[y*N+x]*40;return [v,v,v]});
  const nrm=heightToNormal((x,y)=>hv[y*N+x],N,N,1.2);
  return cache.br={rough:tex(rough,{srgb:false,rep:[2,2]}),nrm:tex(nrm,{srgb:false,rep:[2,2]})}}
export function leatherMaps(col){const N=512;const hv=new Float32Array(N*N);
  for(let y=0;y<N;y++)for(let x=0;x<N;x++){const v=fbm(x/5,y/5,3,9);hv[y*N+x]=Math.pow(v,1.4)}
  const cr=(col>>16)&255,cg=(col>>8)&255,cb=col&255;
  const color=canvasFrom(N,N,(x,y)=>{const k=.8+hv[y*N+x]*.4;return [Math.min(255,cr*k),Math.min(255,cg*k),Math.min(255,cb*k)]});
  return {map:tex(color,{rep:[1,1]}),nrm:tex(heightToNormal((x,y)=>hv[y*N+x],N,N,3),{srgb:false})}}
export function woodMaps(base=[150,92,48]){const W=1024,H=512;
  const col=canvasFrom(W,H,(x,y)=>{const n=fbm(x/90,y/6,4,3);const g=Math.sin((y/3.2)+n*9+fbm(x/300,y/40,2,8)*6)*.5+.5;const k=.72+g*.32+(fbm(x/8,y/2,2,4)-.5)*.12;return [base[0]*k,base[1]*k,base[2]*k]});
  const hv=(x,y)=>fbm(x/90,y/6,3,3);
  return {map:tex(col),nrm:tex(heightToNormal(hv,W,H,1.5),{srgb:false})}}
// ---------- materials ----------
export const M={
  alu:(c=0xc9ccd1,r=.34)=>{const b=brushedMaps();return new THREE.MeshPhysicalMaterial({color:c,metalness:.82,roughness:r,roughnessMap:b.rough,normalMap:b.nrm,normalScale:new THREE.Vector2(.08,.08),envMapIntensity:1.1})},
  ti:(c=0x8e9198)=>new THREE.MeshPhysicalMaterial({color:c,metalness:1,roughness:.26,clearcoat:.3,envMapIntensity:1.2}),
  glass:(c=0x050506,r=.04)=>new THREE.MeshPhysicalMaterial({color:c,metalness:0,roughness:r,clearcoat:1,clearcoatRoughness:.03,envMapIntensity:1.0}),
  plastic:(c,r=.4)=>new THREE.MeshPhysicalMaterial({color:c,roughness:r,clearcoat:.4,clearcoatRoughness:.2}),
  gloss:(c,r=.18)=>new THREE.MeshPhysicalMaterial({color:c,roughness:r,clearcoat:1,clearcoatRoughness:.06}),
  emis:(c,i=2)=>new THREE.MeshStandardMaterial({color:0x000000,emissive:c,emissiveIntensity:i}),
  matte:(c,r=.8)=>new THREE.MeshStandardMaterial({color:c,roughness:r}),
};
export function screenMat(texture,refl=.35){const m=new THREE.MeshPhysicalMaterial({color:0x000000,emissive:0xffffff,emissiveMap:texture,roughness:.05,clearcoat:1,clearcoatRoughness:.02,envMapIntensity:refl});m.toneMapped=false;return m}
export function rbox(w,h,d,r,mat,seg=6){return new THREE.Mesh(new RoundedBoxGeometry(w,h,d,seg,Math.min(r,Math.min(w,h,d)/2-1e-3)),mat)}
export function roundRectShape(w,h,r){const s=new THREE.Shape();const x=-w/2,y=-h/2;s.moveTo(x+r,y);s.lineTo(x+w-r,y);s.quadraticCurveTo(x+w,y,x+w,y+r);s.lineTo(x+w,y+h-r);s.quadraticCurveTo(x+w,y+h,x+w-r,y+h);s.lineTo(x+r,y+h);s.quadraticCurveTo(x,y+h,x,y+h-r);s.lineTo(x,y+r);s.quadraticCurveTo(x,y,x+r,y);return s}
export function plateRR(w,h,r,mat){const g=new THREE.ShapeGeometry(roundRectShape(w,h,r),12);// fix UVs 0..1
  const p=g.attributes.position,uv=g.attributes.uv;for(let i=0;i<p.count;i++){uv.setXY(i,p.getX(i)/w+.5,p.getY(i)/h+.5)}return new THREE.Mesh(g,mat)}
// ---------- SVG -> texture ----------
const STRIP=(s)=>s.replace(/^<svg[^>]*>/,'').replace(/<\/svg>$/,'');
export function svgTexture(content,vb,ppm=40){return new Promise(res=>{const [x,y,w,h]=vb;const pw=Math.round(w*ppm),ph=Math.round(h*ppm);
  const svg=`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${pw}" height="${ph}" viewBox="${x} ${y} ${w} ${h}">${STRIP(window.DEFS)}${STRIP(window.DEFS3)}${content}</svg>`;
  const img=new Image();img.onload=()=>{const c=document.createElement('canvas');c.width=pw;c.height=ph;c.getContext('2d').drawImage(img,0,0,pw,ph);res(tex(c))};img.onerror=e=>{console.log('svg err');res(null)};
  img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg)})}
export function textCanvas(w,h,ppm,draw){const c=document.createElement('canvas');c.width=Math.round(w*ppm);c.height=Math.round(h*ppm);const ctx=c.getContext('2d');ctx.scale(ppm,ppm);draw(ctx);return c}
// ---------- rendering ----------
export function makeScene(){const s=new THREE.Scene();s.environment=ENV;s.environmentIntensity=1.35;
  const d=new THREE.DirectionalLight(0xffffff,1.6);d.position.set(-30,60,80);s.add(d);const d2=new THREE.DirectionalLight(0xdfe8ff,.35);d2.position.set(50,-20,40);s.add(d2);return s}
export function viewCam(view,box){ // box: {cx,cy,cz,w,h,d}
  const {cx,cy,cz,w,h,d}=box;let cam,W,H;const far=1000;
  const mk=(hw,hh)=>new THREE.OrthographicCamera(-hw,hw,hh,-hh,.1,far);
  switch(view){
    case 'front':cam=mk(w/2,h/2);cam.position.set(cx,cy,cz+200);cam.up.set(0,1,0);cam.lookAt(cx,cy,cz);W=w;H=h;break;
    case 'back':cam=mk(w/2,h/2);cam.position.set(cx,cy,cz-200);cam.up.set(0,1,0);cam.lookAt(cx,cy,cz);W=w;H=h;break;
    case 'left':cam=mk(d/2,h/2);cam.position.set(cx-200,cy,cz);cam.up.set(0,1,0);cam.lookAt(cx,cy,cz);W=d;H=h;break;
    case 'right':cam=mk(d/2,h/2);cam.position.set(cx+200,cy,cz);cam.up.set(0,1,0);cam.lookAt(cx,cy,cz);W=d;H=h;break;
    case 'top':cam=mk(w/2,d/2);cam.position.set(cx,cy+200,cz);cam.up.set(0,0,-1);cam.lookAt(cx,cy,cz);W=w;H=d;break;
    case 'bottom':cam=mk(w/2,d/2);cam.position.set(cx,cy-200,cz);cam.up.set(0,0,1);cam.lookAt(cx,cy,cz);W=w;H=d;break;
  }
  return {cam,W,H}}
const DIRS={front:[0,0,1],back:[0,0,-1],left:[-1,0,0],right:[1,0,0],top:[0,1,0],bottom:[0,-1,0]};
export function renderView(scene,view,box,ppm,opts={}){
  const {cam,W,H}=viewCam(view,box);
  const q=new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,0,1),new THREE.Vector3(...DIRS[view]));
  if(window.ENVINV) q.invert();
  scene.environmentRotation=new THREE.Euler().setFromQuaternion(q);
  scene.children.forEach(o=>{if(o.isDirectionalLight){if(!o.userData.p0)o.userData.p0=o.position.clone();o.position.copy(o.userData.p0).applyQuaternion(window.ENVINV?q.clone().invert():q)}});const pw=Math.round(W*ppm),ph=Math.round(H*ppm);
  renderer.setSize(pw,ph,false);
  if(opts.bloom){renderer.setClearColor(opts.bg||0x000000,1);const comp=new EffectComposer(renderer);comp.setSize(pw,ph);comp.addPass(new RenderPass(scene,cam));
    comp.addPass(new UnrealBloomPass(new THREE.Vector2(pw,ph),opts.bloom.strength||1.1,opts.bloom.radius||.5,opts.bloom.threshold||.6));comp.addPass(new OutputPass());comp.render();}
  else{renderer.setClearColor(0x000000,0);renderer.render(scene,cam);}
  return canvas.toDataURL('image/png');
}
