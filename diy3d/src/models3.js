import {THREE,M,rbox,plateRR,screenMat,svgTexture,textCanvas,tex,makeScene,fbm,canvasFrom,heightToNormal} from './core.js';
const PI=Math.PI;
function rng(seed){let x=seed*9301+49297;return()=>{x=(x*9301+49297)%233280;return x/233280}}
// leaf texture
function leafTex(hue){const c=canvasFrom(128,256,(x,y)=>{const u=x/127,v=y/255;const mid=Math.abs(u-.5);const vein=mid<.018?1:0;const lat=(Math.abs(((v*10+mid*6)%1)-.5)<.03&&mid<.45)?1:0;
  const base=[60+v*60,140+v*50,40+v*20];const k=1-mid*.6;const r=base[0]*k+vein*90+lat*30,g=base[1]*k+vein*80+lat*25,b=base[2]*k+vein*40+lat*10;return [r*hue[0],g*hue[1],b*hue[2]]});return tex(c)}
function leafGeom(len,wid,curl,twist){const g=new THREE.PlaneGeometry(wid,len,8,24);const p=g.attributes.position;
  for(let i=0;i<p.count;i++){let x=p.getX(i),y=p.getY(i)+len/2;const t=y/len;const prof=Math.sin(Math.min(1,t*1.05)*PI)*(1-t*.15);x*=prof;const z=curl*t*t*len*.35-Math.abs(x)*.25;p.setXYZ(i,x+Math.sin(t*PI)*twist,y,z)}g.computeVertexNormals();return g}
// ================= PLANT =================
export function plant(seed){return async()=>{
  const s=makeScene();const r=rng(seed);const W=25,H=38;
  const potH=10;
  const prof=[[0,0],[5.4,0],[6.2,.4],[7.6,potH-.8],[8.2,potH-.6],[8.3,potH],[7.8,potH+.2],[0,potH+.2]].map(([a,b])=>new THREE.Vector2(a,b));
  const potMat=new THREE.MeshPhysicalMaterial({color:seed%2?0xd9dbe0:0xb7bac0,roughness:.35,clearcoat:.7});
  const pot=new THREE.Mesh(new THREE.LatheGeometry(prof,64),potMat);pot.position.y=-H/2;s.add(pot);
  const soilC=canvasFrom(128,128,(x,y)=>{const v=fbm(x/6,y/6,3,seed);return [60+v*50,36+v*28,20+v*14]});
  const soil=new THREE.Mesh(new THREE.CircleGeometry(7.6,48),new THREE.MeshStandardMaterial({map:tex(soilC),roughness:1}));soil.rotation.x=-PI/2;soil.position.y=-H/2+potH-.1;s.add(soil);
  const mats=[leafTex([1,1,1]),leafTex([.8,.95,.8]),leafTex([1.15,1.08,.9])].map(t=>new THREE.MeshPhysicalMaterial({map:t,side:THREE.DoubleSide,roughness:.45,clearcoat:.35,clearcoatRoughness:.3}));
  const n=20+Math.floor(r()*6);
  for(let i=0;i<n;i++){const a=(i/n)*PI*2*1.6+r()*.5;const tilt=.35+r()*.95;const len=13+r()*9*(1-tilt*.3);const L=new THREE.Mesh(leafGeom(len,4.6+r()*2.4,.6+r()*.8,(r()-.5)*1.4),mats[i%3]);
    const g=new THREE.Group();g.add(L);L.rotation.x=-tilt;g.rotation.y=a;g.position.set(0,-H/2+potH-.3,0);s.add(g)}
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:H,d:30},views:['front','back']}}}
// ================= ROCK =================
export function rock(seed,w,h){return async()=>{
  const s=makeScene();const g=new THREE.IcosahedronGeometry(1,5);const p=g.attributes.position;const v=new THREE.Vector3();
  for(let i=0;i<p.count;i++){v.fromBufferAttribute(p,i);const n=fbm(v.x*1.6+seed,v.y*1.6+seed*2,4,seed)*.55+fbm(v.z*4+seed,v.x*4,2,seed+3)*.12;v.multiplyScalar(.7+n);p.setXYZ(i,v.x*w/2,v.y*Math.min(w,h)*.3,v.z*h/2)}
  g.computeVertexNormals();
  const c=canvasFrom(256,256,(x,y)=>{const n=fbm(x/12+seed,y/12,4,seed);const k=60+n*80;return [k*1.05,k,k*.95]});
  const m=new THREE.Mesh(g,new THREE.MeshStandardMaterial({map:tex(c),roughness:.92,color:0xffffff}));s.add(m);
  return {scene:s,box:{cx:0,cy:0,cz:0,w:w*1.15,h:5,d:h*1.15},views:['top']}}}
// ================= STAR =================
export async function star(){const s=makeScene();const sh=new THREE.Shape();const R=4,r=1.1;for(let i=0;i<8;i++){const a=i*PI/4-PI/2;const rr=i%2?r:R;const x=Math.cos(a)*rr,y=-Math.sin(a)*rr;i?sh.lineTo(x,y):sh.moveTo(x,y)}sh.closePath();
  const g=new THREE.ExtrudeGeometry(sh,{depth:.4,bevelEnabled:true,bevelThickness:.6,bevelSize:.5,bevelSegments:4});g.center();
  s.add(new THREE.Mesh(g,new THREE.MeshPhysicalMaterial({color:0xf2c14e,metalness:1,roughness:.22,clearcoat:.6})));return {scene:s,box:{cx:0,cy:0,cz:0,w:10,h:10,d:4},views:['front']}}
// ================= FOLIAGE STRIP =================
export function foliage(seed){return async()=>{const s=makeScene();const r=rng(seed);const W=100,H=14;
  const mats=[leafTex([1,1,1]),leafTex([.75,.9,.75]),leafTex([1.2,1.1,.85])].map(t=>new THREE.MeshPhysicalMaterial({map:t,side:THREE.DoubleSide,roughness:.5,clearcoat:.2}));
  for(let i=0;i<70;i++){const x=-W/2+2+r()*(W-4);const len=7+r()*7;const L=new THREE.Mesh(leafGeom(len,1.6+r()*1.6,.5+r(),(r()-.5)),mats[i%3]);const g=new THREE.Group();g.add(L);L.rotation.x=-(r()*.5);g.rotation.z=(r()-.5)*.9;g.rotation.y=(r()-.5)*2;g.position.set(x,-H/2+.5,(r()-.5)*4);s.add(g)}
  const base=rbox(W,1.6,6,.6,M.matte(0x2b4a1f,.9));base.position.y=-H/2+.8;s.add(base);
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:H,d:12},views:['front']}}}
// ================= INK + QUILL =================
export async function quill(){const s=makeScene();const W=25,H=45;
  const prof=[[0,0],[5.4,0],[5.8,.6],[5.8,5.2],[4.6,6.6],[2.4,7.2],[2.4,8.6],[3,8.9],[3,9.6],[0,9.6]].map(([a,b])=>new THREE.Vector2(a,b));
  const bottle=new THREE.Mesh(new THREE.LatheGeometry(prof,64),new THREE.MeshPhysicalMaterial({color:0x0c1024,roughness:.04,clearcoat:1,metalness:.1,envMapIntensity:1.6}));bottle.position.set(-4,-H/2,0);s.add(bottle);
  const lab=textCanvas(8,3,40,(g)=>{g.fillStyle='#efe2c2';g.fillRect(0,0,8,3);g.fillStyle='#3a2a15';g.font='italic 1.4px DejaVu Serif';g.textAlign='center';g.fillText('INK',4,2)});
  const lb=new THREE.Mesh(new THREE.CylinderGeometry(5.82,5.82,3,48,1,true,-.7,1.4),new THREE.MeshStandardMaterial({map:tex(lab),roughness:.8}));lb.position.set(-4,-H/2+2.8,0);s.add(lb);
  // feather
  const fc=canvasFrom(96,512,(x,y)=>{const u=x/95,v=y/511;const mid=Math.abs(u-.5);if(mid<.012)return [210,200,180,255];const w=Math.sin(Math.min(1,v*1.1)*PI)*.5*(v<.15?v/.15:1);if(mid>w)return [0,0,0,0];
    const barb=(Math.sin((v*180+mid*60))*.5+.5);const k=200+barb*40-mid*90;return [k,k*.95,k*.85,255]});
  const fg=new THREE.PlaneGeometry(11,36,12,40);const p=fg.attributes.position;for(let i=0;i<p.count;i++){const y=p.getY(i);p.setZ(i,Math.pow((y+17)/34,2)*3+Math.abs(p.getX(i))*.3)}fg.computeVertexNormals();
  const fm=new THREE.Mesh(fg,new THREE.MeshStandardMaterial({map:tex(fc),transparent:true,alphaTest:.3,side:THREE.DoubleSide,roughness:.8}));fm.rotation.z=-.42;fm.position.set(4.3,6.5,1);s.add(fm);
  const shaft=new THREE.Mesh(new THREE.CylinderGeometry(.18,.12,12,12),M.matte(0x9c9078,.6));shaft.rotation.z=-.42;shaft.position.set(-2.4,-13,1.2);s.add(shaft);
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:H,d:14},views:['front']}}
// ================= PAPER ITEMS (SVG art on curled paper) =================
export function paper(fnName,W,H,curl=.6){return async()=>{const s=makeScene();const t=await svgTexture(window[fnName]?window[fnName](W,H):eval(fnName)(W,H),[0,0,W,H],30);
  const g=new THREE.PlaneGeometry(W,H,30,30);const p=g.attributes.position;for(let i=0;i<p.count;i++){const x=p.getX(i),y=p.getY(i);p.setZ(i,Math.pow(Math.abs(x)/(W/2),2)*curl+fbm(x*.3,y*.3,2,4)*.3)}g.computeVertexNormals();
  s.add(new THREE.Mesh(g,new THREE.MeshStandardMaterial({map:t,transparent:true,alphaTest:.05,roughness:.9})));return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:H,d:6},views:['front']}}}
// ================= PLATFORM TOPS =================
export function platform(kind,W,T,D){return async()=>{const s=makeScene();
  let topMat,sideMat;const N=1024;
  if(kind==='soil'){
    const hv=(x,y)=>fbm(x/14,y/14,5,3)*.7+fbm(x/3,y/3,3,7)*.3;
    const peb=[];{const r=rng(11);for(let i=0;i<260;i++)peb.push([r()*N,r()*N,2+r()*7,1.5+r()*4,r()*3,.25+r()*.25])}
    const pebAt=(x,y)=>{for(const [px,py,rx,ry,a,l] of peb){const dx=(x-px)/rx,dy=(y-py)/ry;const d=dx*dx+dy*dy;if(d<1)return [l,d,dx,dy]}return null};
    const col=canvasFrom(N,N,(x,y)=>{const p=pebAt(x,y);if(p){const [l,d,dx,dy]=p;const sh=1-d*.5-(dx+dy)*.18;const v=255*l*sh*(1+(fbm(x/2,y/2,2,5)-.5)*.3);return [v*1.05,v,v*.92]}const h=hv(x,y);const k=.38+h*.5;return [112*k,52*k,28*k]});
    topMat=new THREE.MeshStandardMaterial({map:tex(col),normalMap:tex(heightToNormal((x,y)=>{const p=pebAt(x,y);return hv(x,y)+(p?(1-p[1])*.6:0)},N,N,6),{srgb:false}),roughness:1});
    sideMat=new THREE.MeshStandardMaterial({map:tex(canvasFrom(512,128,(x,y)=>{const k=.5+fbm(x/6,y/6,4,2)*.6;return [100*k,48*k,24*k]})),roughness:1});
  } else if(kind==='conc'){
    const hv=(x,y)=>fbm(x/2,y/2,4,5);const col=canvasFrom(N,N,(x,y)=>{const k=.7+fbm(x/40,y/40,3,2)*.18+(hv(x,y)-.5)*.2;return [178*k,180*k,186*k]});
    topMat=new THREE.MeshStandardMaterial({map:tex(col),normalMap:tex(heightToNormal(hv,N,N,2),{srgb:false}),roughness:.9});sideMat=new THREE.MeshStandardMaterial({color:0xe2e3e6,roughness:.8});
  } else {
    topMat=new THREE.MeshPhysicalMaterial({color:0x06144a,roughness:.15,clearcoat:1});sideMat=new THREE.MeshPhysicalMaterial({color:0x0b2a86,roughness:.2,clearcoat:1});
  }
  const box=new THREE.Mesh(new THREE.BoxGeometry(W,T,D),[sideMat,sideMat,topMat,sideMat,sideMat,sideMat]);s.add(box);

  if(kind==='neon'){const emi=M.emis(0x1aa3ff,2.6);const r=rng(3);const lines=[];for(let i=0;i<22;i++){let x=(r()-.5)*W*.85,z=(r()-.5)*D*.85;const pts=[[x,z]];for(let k=0;k<4;k++){if(k%2==0)x+=(r()-.5)*30;else z+=(r()-.5)*30;x=Math.max(-W/2+4,Math.min(W/2-4,x));z=Math.max(-D/2+4,Math.min(D/2-4,z));pts.push([x,z])}
      for(let k=0;k<pts.length-1;k++){const a=pts[k],b=pts[k+1];const L=Math.hypot(b[0]-a[0],b[1]-a[1]);if(L<.5)continue;const m=new THREE.Mesh(new THREE.CylinderGeometry(.18,.18,L,8),emi);m.position.set((a[0]+b[0])/2,T/2+.1,(a[1]+b[1])/2);m.rotation.set(PI/2,0,-Math.atan2(b[0]-a[0],b[1]-a[1]));m.rotation.order='YXZ';m.rotation.set(PI/2,Math.atan2(b[0]-a[0],b[1]-a[1]),0);s.add(m)}
      const n=new THREE.Mesh(new THREE.CylinderGeometry(.7,.7,.3,16),M.emis(0xbfefff,3));n.position.set(pts[0][0],T/2+.1,pts[0][1]);s.add(n)}
    const fr=new THREE.Mesh(new THREE.TorusGeometry(1,1,4,4),emi);
    [[-W/2+2,0,.35,D-4],[W/2-2,0,.35,D-4],[0,-D/2+2,W-4,.35],[0,D/2-2,W-4,.35]].forEach(([x,z,w,d])=>{const b=new THREE.Mesh(new THREE.BoxGeometry(w,.3,d),emi);b.position.set(x,T/2+.1,z);s.add(b)});
    const st=new THREE.Mesh(new THREE.BoxGeometry(W,.6,.3),emi);st.position.set(0,T/2-.6,D/2+.1);s.add(st);}
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:T,d:D},views:['top','front','back','left','right'],opts:kind==='neon'?{bloom:{strength:1,radius:.45,threshold:.5},bg:0x06144a}:{}}}}
