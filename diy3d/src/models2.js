import {THREE,M,rbox,plateRR,screenMat,svgTexture,textCanvas,tex,makeScene,leatherMaps,woodMaps,fbm,canvasFrom,heightToNormal} from './core.js';
import {SVGLoader} from 'three/addons/loaders/SVGLoader.js';
import {FontLoader} from 'three/addons/loaders/FontLoader.js';
import {TextGeometry} from 'three/addons/geometries/TextGeometry.js';
const PI=Math.PI;
const cyl=(r,h,mat,seg=40)=>{const m=new THREE.Mesh(new THREE.CylinderGeometry(r,r,h,seg),mat);return m};
let FONT=null;async function font(){if(FONT)return FONT;FONT=await new FontLoader().loadAsync('./node_modules/three/examples/fonts/helvetiker_bold.typeface.json');return FONT}
function goldMat(alphaCanvas,col=0xd9ab4c){const t=new THREE.CanvasTexture(alphaCanvas);return new THREE.MeshPhysicalMaterial({color:col,metalness:.55,roughness:.38,alphaMap:t,transparent:true,envMapIntensity:.5})}
function halo(x,y,z,size,col){const c=document.createElement('canvas');c.width=c.height=128;const g=c.getContext('2d');const gr=g.createRadialGradient(64,64,0,64,64,64);gr.addColorStop(0,col);gr.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=gr;g.fillRect(0,0,128,128);
  const s=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(c),transparent:true,depthWrite:false}));s.scale.set(size,size,1);s.position.set(x,y,z);return s}
// ================= BOOK =================
export function book(title,col,foilCol){return async()=>{
  const s=makeScene();s.environmentIntensity=.55;s.children.forEach(o=>{if(o.isDirectionalLight)o.intensity*=.6});const W=40,T=12,D=30;const lm=leatherMaps(col);
  const lmat=new THREE.MeshPhysicalMaterial({color:0xffffff,map:lm.map,normalMap:lm.nrm,normalScale:new THREE.Vector2(.7,.7),roughness:.68,clearcoat:.12,clearcoatRoughness:.5,envMapIntensity:.55});
  [1,-1].forEach(sd=>{const b=rbox(W+.6,1.1,D+.4,.45,lmat,4);b.position.set(0,sd*(T/2-.55),-.2);s.add(b)});
  // page block
  const pc=canvasFrom(256,256,(x,y)=>{const v=236-((y%4)<1?28:0)-fbm(x/40,y/3,2,3)*14;return [v,v-8,v-30]});
  const pmat=new THREE.MeshStandardMaterial({map:tex(pc,{rep:[1,3]}),roughness:.85});
  const pb=new THREE.Mesh(new THREE.BoxGeometry(W-.4,T-2.2,D-.6),pmat);pb.position.set(0,0,-.5);s.add(pb);
  // spine (rounded)
  const sp=new THREE.Mesh(new THREE.CylinderGeometry(T/2,T/2,W+.6,64,1,false,-PI/2,PI),lmat);sp.rotation.z=PI/2;sp.scale.set(1,1,.22);sp.position.set(0,0,D/2-.4);
  sp.rotation.set(0,0,PI/2);const spg=new THREE.Group();spg.add(sp);sp.rotation.set(0,0,PI/2);s.add(spg);
  // ensure spine faces +z : cylinder thetaStart -PI/2 length PI covers +z side after rotation
  // gold text on spine
  const fc=textCanvas(W,T,40,(c)=>{c.fillStyle='#fff';c.strokeStyle='#fff';c.lineWidth=.3;[3.4,6.3].forEach(x=>{c.fillRect(x-.35,.2,.7,T-.4);c.fillRect(W-x-.35,.2,.7,T-.4)});
    c.strokeRect(8.6,T*.18,W-17.2,T*.64);const fs=Math.min(T*.46,(W-19)/title.length*1.75);c.font=`bold ${fs}px Raleway`;c.textAlign='center';c.textBaseline='middle';c.fillText(title,W/2,T/2+.2)});
  const gt=new THREE.Mesh(new THREE.PlaneGeometry(W,T),goldMat(fc,foilCol));gt.position.set(0,0,D/2-.4+T/2*.22+.05);s.add(gt);
  // gold on cover
  const cc=textCanvas(W,D,30,(c)=>{c.strokeStyle='#fff';c.fillStyle='#fff';c.lineWidth=.35;c.strokeRect(1.8,1.8,W-3.6,D-3.6);c.lineWidth=.15;c.strokeRect(2.6,2.6,W-5.2,D-5.2);
    c.font=`bold ${Math.min(4.2,(W-8)/title.length*1.6)}px Raleway`;c.textAlign='center';c.fillText(title.toUpperCase(),W/2,D*.47);c.fillRect(W*.25,D*.55,W*.5,.22);c.beginPath();c.arc(W/2,D*.553,.55,0,7);c.fill();c.font='1.3px Liberation Sans';c.fillText('COMPUTER SCIENCE',W/2,D*.72);
    [[3.4,3.4],[W-3.4,3.4],[3.4,D-3.4],[W-3.4,D-3.4]].forEach(([x,y])=>{c.beginPath();c.arc(x,y,.7,0,7);c.fill()})});
  const gc=new THREE.Mesh(new THREE.PlaneGeometry(W,D),goldMat(cc,foilCol));gc.rotation.x=-PI/2;gc.position.set(0,T/2+.01,-.2);s.add(gc);
  // ribbon
  const rb=rbox(1.6,.2,4,.08,M.gloss(0xa8222c,.4));rb.position.set(W*.28,-T/2+1.6,-D/2-1.2);
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:T,d:D+1.2},views:['front','back','left','right','top','bottom']}}}
// ================= ABACUS =================
export async function abacus(){
  const s=makeScene();const wm=woodMaps();const wood=new THREE.MeshPhysicalMaterial({map:wm.map,normalMap:wm.nrm,normalScale:new THREE.Vector2(.5,.5),roughness:.45,clearcoat:.6,clearcoatRoughness:.25});
  const W=70,H=70,frameH=59,fy=H/2-frameH/2;
  const bar=(w,h,d,x,y,z)=>{const m=rbox(w,h,d,.8,wood,4);m.position.set(x,y,z);s.add(m);return m};
  bar(W,4.6,9,0,H/2-2.3,0);bar(W,4.6,9,0,H/2-frameH+2.3,0);bar(4.6,frameH+6,9,-W/2+2.3,fy-3,0);bar(4.6,frameH+6,9,W/2-2.3,fy-3,0);
  bar(W,11,18,0,-H/2+5.5,0);bar(5,6,6,-W/2+8,-H/2+8.6,0).visible=false;
  // back panel (dark)
  const bp=new THREE.Mesh(new THREE.PlaneGeometry(W-9,frameH-9),M.matte(0x1d120a,.9));bp.position.set(0,fy,-3.8);s.add(bp);
  const rows=8,iy0=H/2-4.6,ih=frameH-9.2,rh=ih/rows;
  const rod=new THREE.MeshPhysicalMaterial({color:0xc9a248,metalness:1,roughness:.25});
  const prof=[];for(let i=0;i<=24;i++){const t=i/24;const y=-2.6+t*5.2;const r=.45+2.75*Math.pow(Math.sin(t*PI),.85);prof.push(new THREE.Vector2(r,y))}
  const beadG=new THREE.LatheGeometry(prof,48);
  const dark=new THREE.MeshPhysicalMaterial({color:0x3a160c,roughness:.22,clearcoat:1,clearcoatRoughness:.05});
  const light=new THREE.MeshPhysicalMaterial({color:0xd8a865,roughness:.3,clearcoat:1,clearcoatRoughness:.06,map:wm.map});
  const nLs=[5,3,4,5,2,4,3,5];
  for(let r=0;r<rows;r++){const y=iy0-rh*(r+.5);const rd=cyl(.42,W-6,rod,24);rd.rotation.z=PI/2;rd.position.set(0,y,0);s.add(rd);
    const iw=W-9.2,bw=5.5,nL=nLs[r];
    for(let b=0;b<9;b++){const left=b<nL;const x=left?-iw/2+bw*(b+.5):iw/2-bw*(9-b-.5);const bd=new THREE.Mesh(beadG,left?dark:light);bd.rotation.z=PI/2;bd.scale.set(1,1.02,1);
      const sc=Math.min(1,(rh*.86)/6.4);bd.scale.set(sc,1.0,sc);bd.position.set(x,y,0);s.add(bd)}}
  // label plaque
  const lc=await svgTexture(`<rect width="20" height="5" fill="#efe2c2"/><text x="10" y="2.6" font-size="2" text-anchor="middle" font-family="Raleway" font-weight="700" fill="#4a2c10">ABACUS</text><text x="10" y="4.2" font-size="1.1" text-anchor="middle" font-family="DejaVu Serif" font-style="italic" fill="#4a2c10">c. 2000 BC</text>`,[0,0,20,5],40);
  const pl=rbox(20,5,.6,.3,new THREE.MeshStandardMaterial({map:lc,roughness:.7}));pl.position.set(0,-H/2+5,9.2);s.add(pl);
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:H,d:20},views:['front','back']}}
// ================= ROBOT =================
export async function robot(){
  const s=makeScene();const white=new THREE.MeshPhysicalMaterial({color:0xf3f5f9,roughness:.22,clearcoat:1,clearcoatRoughness:.08});
  const dark=new THREE.MeshPhysicalMaterial({color:0x2a3142,roughness:.35,clearcoat:.6});const cyan=M.emis(0x34d6ff,2.4);
  const add=(m,x,y,z)=>{m.position.set(x,y,z);s.add(m);return m};
  // head
  add(rbox(21,16.5,15,6.6,white,8),0,18.6,0);
  add(rbox(17,12,2,5.2,M.glass(0x050914,.05),8),0,18.4,6.9);
  [-1,1].forEach(sd=>{const e=new THREE.Mesh(new THREE.SphereGeometry(1,32,16),cyan);e.scale.set(1.75,2.2,.35);add(e,sd*3.5,19,7.95);s.add(halo(sd*3.5,19,8.3,7,'rgba(70,220,255,.85)'));
    const hl=new THREE.Mesh(new THREE.SphereGeometry(.45,16,8),M.emis(0xffffff,3));hl.scale.z=.3;add(hl,sd*3.5-.5,19.8,8.25)});
  const mo=new THREE.Mesh(new THREE.TorusGeometry(1.8,.22,8,32,PI*.8),cyan);mo.rotation.z=PI+PI*.1;add(mo,0,16,8.0);
  [-1,1].forEach(sd=>{const er=cyl(2.4,2.6,white,32);er.rotation.z=PI/2;add(er,sd*11.2,18.6,0);const ec=cyl(1.4,2.8,dark,32);ec.rotation.z=PI/2;add(ec,sd*11.5,18.6,0)});
  add(cyl(.35,3.6,dark,12),0,28.4,0);add(new THREE.Mesh(new THREE.SphereGeometry(1.2,24,16),cyan),0,30.2,0);s.add(halo(0,30.2,1.5,5,'rgba(70,220,255,.8)'));
  // neck + torso
  add(cyl(2.7,3.4,dark,32),0,8.9,0);
  const tor=new THREE.Mesh(new THREE.SphereGeometry(9,64,32),white);tor.scale.set(1,1.05,.78);add(tor,0,-1.6,0);
  add(new THREE.Mesh(new THREE.TorusGeometry(3.4,.45,16,64),dark),0,-0.6,7.2);
  const core=cyl(3,1,cyan,48);core.rotation.x=PI/2;add(core,0,-.6,6.9);s.add(halo(0,-.6,7.8,11,'rgba(60,210,255,.75)'));
  add(new THREE.Mesh(new THREE.SphereGeometry(.9,16,8),M.emis(0xffffff,3)),-.9,.3,7.6).scale.z=.3;
  add(rbox(12,1.3,9,.6,dark),0,-9.2,0);
  // arms
  [-1,1].forEach(sd=>{add(new THREE.Mesh(new THREE.SphereGeometry(2.6,32,16),white),sd*9.6,3.6,0);
    const a=new THREE.Mesh(new THREE.CapsuleGeometry(1.7,8,8,24),white);a.rotation.z=sd*.32;add(a,sd*11.6,-2.5,0);
    add(new THREE.Mesh(new THREE.SphereGeometry(1.4,24,12),dark),sd*12.9,-7.6,0);
    add(new THREE.Mesh(new THREE.SphereGeometry(2.2,32,16),white),sd*13.3,-9.6,.4)});
  // legs
  [-1,1].forEach(sd=>{add(new THREE.Mesh(new THREE.CapsuleGeometry(2.3,6,8,24),white),sd*3.9,-16.6,0);add(cyl(2.2,1.2,dark,32),sd*3.9,-21.2,0);
    const ft=rbox(6.8,3.2,8.6,1.5,white,6);add(ft,sd*4.1,-25.3,1.2)});
  return {scene:s,box:{cx:0,cy:1,cz:0,w:30,h:60,d:25},views:['front','back']}}
// ================= AI BRAIN =================
function svgPathPoints(d,n=400){const data=new SVGLoader().parse(`<svg xmlns="http://www.w3.org/2000/svg"><path d="${d}"/></svg>`);const sh=data.paths[0].toShapes(true)[0];return sh.getSpacedPoints(n)}
function inPoly(p,poly){let c=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];if(((a.y>p.y)!=(b.y>p.y))&&(p.x<(b.x-a.x)*(p.y-a.y)/(b.y-a.y)+a.x))c=!c}return c}
function tube(pts,r,mat,closed=false){const c=new THREE.CatmullRomCurve3(pts.map(p=>new THREE.Vector3(p.x,p.y,p.z||0)),closed);return new THREE.Mesh(new THREE.TubeGeometry(c,Math.max(32,pts.length*3),r,10,closed),mat)}
export async function brain(){
  const s=makeScene();const W=65,H=60;
  s.add(rbox(W,H,3,6,new THREE.MeshPhysicalMaterial({color:0x020611,roughness:.12,clearcoat:1})));
  const neon=M.emis(0x1aa3ff,1.6),neonL=M.emis(0x3fb6ff,.8),white=M.emis(0xd8f6ff,1.4);
  // edge glow
  const rr=[];const rx=W/2-1.6,ry=H/2-1.6,rc=5;for(let i=0;i<=200;i++){const t=i/200*PI*2;const cx=Math.cos(t),cy=Math.sin(t);rr.push({x:Math.sign(cx)*Math.min(Math.abs(cx)*1e9,1)*0,y:0})}
  const shp=new THREE.Shape();const w2=W/2-1.5,h2=H/2-1.5,r=4.6;shp.moveTo(-w2+r,-h2);shp.lineTo(w2-r,-h2);shp.quadraticCurveTo(w2,-h2,w2,-h2+r);shp.lineTo(w2,h2-r);shp.quadraticCurveTo(w2,h2,w2-r,h2);shp.lineTo(-w2+r,h2);shp.quadraticCurveTo(-w2,h2,-w2,h2-r);shp.lineTo(-w2,-h2+r);shp.quadraticCurveTo(-w2,-h2,-w2+r,-h2);
  const ep=shp.getSpacedPoints(300).map(p=>({x:p.x,y:p.y,z:1.6}));s.add(tube(ep,.28,neon,true));
  const bp=svgPathPoints(brainPath(W,H),360).map(p=>({x:p.x-W/2,y:H/2-p.y}));
  s.add(tube(bp.map(p=>({...p,z:1.8})),.5,neon,true));
  // gyri
  for(let i=0;i<10;i++){const y0=H*(.12+i*.07);let seg=[];for(let k=0;k<=120;k++){const x=W*.05+k*W*.9/120;const y=y0+Math.sin(k*.42+i)*H*.025+Math.sin(k*.11+i*2)*H*.015;const p={x:x-W/2,y:H/2-y,z:1.75};
      if(inPoly(p,bp)){seg.push(p)}else{if(seg.length>6)s.add(tube(seg,.16,neonL));seg=[]}} if(seg.length>6)s.add(tube(seg,.16,neonL))}
  // midline
  s.add(tube([{x:0,y:H/2-H*.18,z:1.8},{x:-1,y:H/2-H*.34,z:1.8},{x:1,y:H/2-H*.5,z:1.8},{x:0,y:H/2-H*.7,z:1.8}],.3,neon));
  const nodes=[[.22,.45],[.34,.32],[.4,.5],[.34,.62],[.62,.4],[.66,.56],[.72,.36],[.6,.24],[.4,.22],[.78,.5],[.52,.62],[.3,.2],[.7,.22]].map(([x,y])=>({x:x*W-W/2,y:H/2-y*H,z:2.1}));
  nodes.forEach((a,i)=>{const b=nodes[(i*3+2)%nodes.length];s.add(tube([a,b],.12,neonL));const n=new THREE.Mesh(new THREE.SphereGeometry(.7,16,8),white);n.position.set(a.x,a.y,2.2);s.add(n)});
  // AI text
  const f=await font();const tg=new TextGeometry('AI',{font:f,size:11,depth:1,bevelEnabled:true,bevelThickness:.25,bevelSize:.2,bevelSegments:3});tg.computeBoundingBox();const bb=tg.boundingBox;tg.translate(-(bb.max.x+bb.min.x)/2,-(bb.max.y+bb.min.y)/2,0);
  const tm=new THREE.Mesh(tg,[new THREE.MeshPhysicalMaterial({color:0x0a2a6a,emissive:0x4fc8ff,emissiveIntensity:.6,roughness:.1,clearcoat:1}),M.emis(0x1aa3ff,1.6)]);tm.position.set(1,H/2-H*.45,2.2);s.add(tm);
  // stem
  [[0,.76,.9],[-.08,.76,.9],[.08,.76,.9]].forEach(([dx,a,b],i)=>{const x=dx*W*(i?1.6:1);const pts=[{x:dx*W*.6,y:H/2-H*a,z:1.8},{x:dx*W*.6,y:H/2-H*.84,z:1.8},{x:x,y:H/2-H*b,z:1.8}];s.add(tube(pts,.28,neon));const n=new THREE.Mesh(new THREE.SphereGeometry(1.2,16,8),white);n.position.set(x,H/2-H*(b+.02),2);s.add(n)});
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:H,d:6},views:['front'],opts:{bloom:{strength:.6,radius:.4,threshold:.72},bg:0x020611}}}
// ================= AI SCREEN =================
export async function aiscreen(){
  const s=makeScene();const W=55,H=50;
  s.add(rbox(W,H,2.6,2.2,new THREE.MeshPhysicalMaterial({color:0x061638,roughness:.08,clearcoat:1})));
  const t=await svgTexture(aiScreenArt2(W,H),[3.4,3.4,W-6.8,H-6.8],30);
  const sm=screenMat(t,.25);sm.emissiveIntensity=.8;const sc=plateRR(W-6.8,H-6.8,1.2,sm);sc.position.z=1.32;s.add(sc);
  const shp=[];const w2=W/2-1.4,h2=H/2-1.4;[[-w2,-h2],[w2,-h2],[w2,h2],[-w2,h2]];
  const sh=new THREE.Shape();const r=1.6;sh.moveTo(-w2+r,-h2);sh.lineTo(w2-r,-h2);sh.quadraticCurveTo(w2,-h2,w2,-h2+r);sh.lineTo(w2,h2-r);sh.quadraticCurveTo(w2,h2,w2-r,h2);sh.lineTo(-w2+r,h2);sh.quadraticCurveTo(-w2,h2,-w2,h2-r);sh.lineTo(-w2,-h2+r);sh.quadraticCurveTo(-w2,-h2,-w2+r,-h2);
  s.add(tube(sh.getSpacedPoints(300).map(p=>({x:p.x,y:p.y,z:1.4})),.3,M.emis(0x2aa6ff,1.8),true));
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:H,d:4},views:['front','back'],opts:{bloom:{strength:.45,radius:.35,threshold:.9},bg:0x020611}}}
export async function aibase(){
  const s=makeScene();const W=55,D=30,T=6;
  s.add(rbox(W,T,D,1.2,new THREE.MeshPhysicalMaterial({color:0x07154a,roughness:.15,clearcoat:1})));
  const sh=new THREE.Shape();const w2=W/2-2,h2=D/2-2,r=1.2;sh.moveTo(-w2+r,-h2);sh.lineTo(w2-r,-h2);sh.quadraticCurveTo(w2,-h2,w2,-h2+r);sh.lineTo(w2,h2-r);sh.quadraticCurveTo(w2,h2,w2-r,h2);sh.lineTo(-w2+r,h2);sh.quadraticCurveTo(-w2,h2,-w2,h2-r);sh.lineTo(-w2,-h2+r);sh.quadraticCurveTo(-w2,-h2,-w2+r,-h2);
  const tb=tube(sh.getSpacedPoints(240).map(p=>({x:p.x,y:T/2+.05,z:p.y})),.35,M.emis(0x2aa6ff,3),true);s.add(tb);
  const st=tube([{x:-W/2+1,y:-T/2+2.2,z:D/2+.05},{x:W/2-1,y:-T/2+2.2,z:D/2+.05}],.3,M.emis(0x2aa6ff,3));s.add(st);
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:T,d:D},views:['top','front','back','left','right'],opts:{bloom:{strength:.9,radius:.4,threshold:.5},bg:0x07154a}}}
// ================= SIGNBOARDS =================
export function sign(txt,W=45,H=15,dark=false){return async()=>{
  const s=makeScene();
  s.add(rbox(W,H,3,1.4,new THREE.MeshPhysicalMaterial({color:dark?0x030c26:0xdcefff,roughness:.1,clearcoat:1,envMapIntensity:.7})));
  const c=textCanvas(W,H,40,(g)=>{if(!dark){const gr=g.createLinearGradient(0,0,0,H);gr.addColorStop(0,'#f4faff');gr.addColorStop(1,'#bfe0ff');g.fillStyle=gr;g.fillRect(.8,.8,W-1.6,H-1.6)}
    g.fillStyle=dark?'#eaf6ff':'#0d2a78';g.font=`bold ${dark?5:4.4}px Raleway`;g.textAlign='center';g.textBaseline='middle';g.fillText(txt,W/2,H/2+.2);if(dark){g.fillStyle='#2aa6ff';g.fillRect(1,H-2,W-2,.9)}});
  const p=new THREE.Mesh(new THREE.PlaneGeometry(W,H),new THREE.MeshPhysicalMaterial({map:tex(c),transparent:true,roughness:.15,clearcoat:1,emissive:dark?0x000000:0x223355,emissiveIntensity:.05}));p.position.z=1.51;s.add(p);
  const sh=new THREE.Shape();const w2=W/2-.5,h2=H/2-.5,r=1.1;sh.moveTo(-w2+r,-h2);sh.lineTo(w2-r,-h2);sh.quadraticCurveTo(w2,-h2,w2,-h2+r);sh.lineTo(w2,h2-r);sh.quadraticCurveTo(w2,h2,w2-r,h2);sh.lineTo(-w2+r,h2);sh.quadraticCurveTo(-w2,h2,-w2,h2-r);sh.lineTo(-w2,-h2+r);sh.quadraticCurveTo(-w2,-h2,-w2+r,-h2);
  s.add(tube(sh.getSpacedPoints(200).map(q=>({x:q.x,y:q.y,z:1.5})),.28,M.emis(0x1f8bff,2.6),true));
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:H,d:4},views:['front']}}}
