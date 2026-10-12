import {THREE,M,rbox,plateRR,screenMat,svgTexture,textCanvas,tex,makeScene} from './core.js';
const PI=Math.PI;
function cyl(r,h,mat,seg=48){const m=new THREE.Mesh(new THREE.CylinderGeometry(r,r,h,seg),mat);m.rotation.x=PI/2;return m}
function lens(x,y,z,R,dir=-1){const g=new THREE.Group();
  const ring=cyl(R,.9,M.ti(0x9fa3aa));g.add(ring);
  const inner=cyl(R*.8,.95,M.glass(0x050608));g.add(inner);
  const dome=new THREE.Mesh(new THREE.SphereGeometry(R*.62,48,24,0,PI*2,0,PI/2),new THREE.MeshPhysicalMaterial({color:0x0a0d1c,roughness:.02,clearcoat:1,iridescence:1,iridescenceIOR:1.6,iridescenceThicknessRange:[200,500],envMapIntensity:1.4}));
  dome.rotation.x=dir<0?-PI/2:PI/2;dome.scale.set(1,.45,1);dome.position.z=dir*.45;g.add(dome);
  const tor=new THREE.Mesh(new THREE.TorusGeometry(R*.92,R*.08,16,64),M.ti(0xc7cbd2));tor.position.z=dir*.46;g.add(tor);
  g.position.set(x,y,z);return g}
function logo(x,y,z,R,dir=-1){const g=new THREE.Group();const t=new THREE.Mesh(new THREE.TorusGeometry(R,R*.13,24,96),new THREE.MeshPhysicalMaterial({color:0xd7dade,metalness:1,roughness:.08}));
  const d=cyl(R*.5,.05,new THREE.MeshPhysicalMaterial({color:0xe4e6ea,metalness:1,roughness:.05}));g.add(t,d);g.position.set(x,y,z);return g}
function textPlane(w,h,draw,ppm=40){const c=textCanvas(w,h,ppm,draw);const t=tex(c);const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshStandardMaterial({map:t,transparent:true,roughness:.6}));return m}
// ===== PHONE 18x38x5 =====
export async function phone(){
  const s=makeScene();const W=18,H=38,D=5;
  const body=rbox(W,H,D-.3,2.4,M.ti(0x8c9097),8);s.add(body);
  const fg=plateRR(W-.6,H-.6,2.7,M.glass());fg.position.z=(D-.3)/2+.01;s.add(fg);
  const t=await svgTexture(phoneFront2(W,H),[.95,.95,W-1.9,H-1.9],40);
  const sc=plateRR(W-1.9,H-1.9,2.45,screenMat(t,.3));sc.position.z=(D-.3)/2+.02;s.add(sc);
  const bg=plateRR(W-.6,H-.6,2.7,new THREE.MeshPhysicalMaterial({color:0x5a5e66,roughness:.62,clearcoat:.5,clearcoatRoughness:.35,sheen:.3}));bg.rotation.y=PI;bg.position.z=-(D-.3)/2-.01;s.add(bg);
  const pcx=W/2-1.8-4.6,pcy=H/2-1.8-4.7,bz=-(D-.3)/2;
  const pl=rbox(9.2,9.4,1,2.2,new THREE.MeshPhysicalMaterial({color:0x6a6e76,roughness:.12,clearcoat:1}));pl.position.set(pcx,pcy,bz-.4);s.add(pl);
  [[-2.15,2],[-2.15,-2],[2.15,0]].forEach(([u,v])=>s.add(lens(pcx-u,pcy+v,bz-1,1.85,-1)));
  const fl=cyl(.55,.3,new THREE.MeshStandardMaterial({color:0xf3e9c6,emissive:0x443c20,roughness:.3}));fl.position.set(pcx-2.2,pcy+3.6,bz-.95);s.add(fl);
  s.add(logo(0,-2,bz-.03,2.1));
  // buttons
  const bm=M.ti(0x7f838a);[[-1,13.2,2.2],[-1,8.6,4.2],[-1,3.6,4.2],[1,6.4,7.4]].forEach(([sd,y,l])=>{const b=rbox(.8,l,1.7,.38,bm);b.position.set(sd*(W/2+.12),y,0);s.add(b)});
  const usb=rbox(4.6,1,1.3,.5,M.matte(0x0b0b0c));usb.position.set(0,-H/2+.45,0);s.add(usb);
  [-1,1].forEach(sd=>{for(let i=0;i<6;i++){const h=cyl(.26,.3,M.matte(0x111113),16);h.rotation.x=0;h.position.set(sd*(4+i*.85),-H/2+.2,0);s.add(h)}});
  const box={cx:0,cy:0,cz:0,w:W,h:H,d:D};return {scene:s,box,views:['front','back','left','right','top','bottom']}}
// ===== TABLET 45x32x4 =====
export async function tablet(){
  const s=makeScene();const W=45,H=32,D=4;
  s.add(rbox(W,H,D-.2,2.9,M.alu(0xd2d5da),8));
  const fg=plateRR(W-.6,H-.6,3,M.glass());fg.position.z=(D-.2)/2+.01;s.add(fg);
  const t=await svgTexture(tabletFront2(W,H),[1.9,1.9,W-3.8,H-3.8],32);
  const sc=plateRR(W-3.8,H-3.8,1.3,screenMat(t,.28));sc.position.z=(D-.2)/2+.02;s.add(sc);
  const cam=new THREE.Mesh(new THREE.SphereGeometry(.4,24,12),M.glass(0x101418));cam.position.set(0,H/2-1.2,(D-.2)/2+.03);cam.scale.z=.2;s.add(cam);
  const bz=-(D-.2)/2;const bx=W/2-2.4-4.3,by=H/2-2.4-4.3;
  const bump=rbox(8.6,8.6,.9,2.4,M.alu(0xc8cbd0,.28));bump.position.set(bx,by,bz-.25);s.add(bump);
  s.add(lens(bx+.0,by,bz-.7,2.6,-1));
  const fl=cyl(.45,.3,new THREE.MeshStandardMaterial({color:0xf3e9c6,emissive:0x302a14}));fl.position.set(bx-3,by+3,bz-.7);s.add(fl);
  s.add(logo(0,0,bz-.03,3));
  const lab=textPlane(34,3,(c)=>{c.fillStyle='rgba(110,114,122,.9)';c.font='bold 1.2px Liberation Sans';c.textAlign='center';c.fillText('Tablet  •  Wi-Fi  •  256 GB',17,1.3);c.font='.75px Liberation Sans';c.fillText('Model A2026   •   Designed for the Evolution of Computer Science project',17,2.5)});
  lab.rotation.y=PI;lab.position.set(0,-H/2+5,bz-.03);s.add(lab);
  const bm=M.alu(0xb8bcc2);[[ -10,1],[ -6,1]].forEach(([x])=>{const b=rbox(3,.8,1.4,.35,bm);b.position.set(x+W/2,H/2-.35,0);s.add(b)});
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:H,d:D},views:['front','back','left','right','top','bottom']}}
// ===== MONITOR (70 x 50 incl. stand) =====
export async function monitor(){
  const s=makeScene();const W=70,HT=50;const bodyH=36,by=HT/2-bodyH/2;
  const body=rbox(W,bodyH,3.2,1.9,M.alu(0xd0d3d8),8);body.position.y=by;s.add(body);
  const fg=plateRR(W-1.2,bodyH-1.2,1.4,M.glass());fg.position.set(0,by,1.61);s.add(fg);
  const t=await svgTexture(monitorFront2(W,HT),[1.5,1.5,W-3,bodyH-4.5],24);
  const sc=plateRR(W-3,bodyH-4.5,.35,screenMat(t,.25));sc.position.set(0,HT/2-1.5-(bodyH-4.5)/2,1.62);s.add(sc);
  // chin logo
  s.add(Object.assign(logo(0,HT/2-bodyH+1.55,1.63,.5,1)));
  // neck
  const shp=new THREE.Shape();shp.moveTo(-6,0);shp.lineTo(6,0);shp.lineTo(8.6,-12.4);shp.lineTo(-8.6,-12.4);shp.closePath();
  const neck=new THREE.Mesh(new THREE.ExtrudeGeometry(shp,{depth:2.2,bevelEnabled:true,bevelSize:.5,bevelThickness:.5,bevelSegments:4}),M.alu(0xcfd2d7));neck.position.set(0,HT/2-bodyH+.6,-3.6);s.add(neck);
  const base=rbox(34,3.4,16,1.6,M.alu(0xd3d6db),8);base.position.set(0,-HT/2+1.7,-3);s.add(base);
  // ports on back
  const pb=rbox(10,3,.6,.5,M.matte(0x1d1f23,.5));pb.position.set(0,by-bodyH/2+5,-1.7);s.add(pb);
  for(let i=0;i<4;i++){const p=rbox(1.6,1.1,.4,.3,M.matte(0x050506));p.position.set(-3.4+i*2.3,by-bodyH/2+5,-2);s.add(p)}
  s.add(logo(0,by+3,-1.62,3.4));
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:HT,d:20},views:['front','back']}}
// ===== KEYS helper (top view, keyboard lies in XZ plane, top at y) =====
function keyField(g,rows,x0,z0,w,h,yTop,opts){
  const gap=opts.gap||.32,n=rows.length;const kh=(h-gap*(n-1))/n;
  const keyMat=opts.keyMat||new THREE.MeshPhysicalMaterial({color:0x111214,roughness:.55,clearcoat:.25,clearcoatRoughness:.4});
  const labels=[];
  rows.forEach((row,r)=>{const wt=row.map((t,i)=>opts.wt?opts.wt(r,i,row.length):1);const unit=(w-gap*(row.length-1))/wt.reduce((a,b)=>a+b,0);let x=x0;
    row.forEach((t,i)=>{const kw=unit*wt[i];const k=rbox(kw,.9,kh,.32,keyMat,4);k.position.set(x+kw/2,yTop+.45,z0+r*(kh+gap)+kh/2);g.add(k);labels.push([x+kw/2,z0+r*(kh+gap)+kh/2,t,kw,kh]);x+=kw+gap})});
  // legend overlay
  const ppm=40,c=textCanvas(w+2,h+2,ppm,(ctx)=>{ctx.fillStyle=opts.legend||'#d9dbe0';ctx.textAlign='center';ctx.textBaseline='middle';labels.forEach(([x,z,t,kw,kh])=>{if(!t)return;ctx.font=`${Math.min(1.25,kw*.36,kh*.5)}px Liberation Sans`;ctx.fillText(t,x-x0+1,z-z0+1)})});
  const pl=new THREE.Mesh(new THREE.PlaneGeometry(w+2,h+2),new THREE.MeshBasicMaterial({map:tex(c),transparent:true}));pl.rotation.x=-PI/2;pl.position.set(x0+w/2,yTop+.92,z0+h/2);g.add(pl);
}
const WT1=(r,i,n)=>{let k=1;if(r==1&&i==n-1)k=1.45;if(r==2&&i==0)k=1.35;if(r==3&&i==0)k=1.6;if(r==3&&i==n-1)k=1.5;if(r==4&&(i==0||i==n-1))k=2.1;return k};
export async function keyboard(){
  const s=makeScene();const W=60,D=20;
  const b=rbox(W,2.4,D,1.6,M.alu(0x4a4d54,.38),6);s.add(b);
  const well=new THREE.Mesh(new THREE.PlaneGeometry(W-2,D-2),M.matte(0x0d0e10,.9));well.rotation.x=-PI/2;well.position.y=1.21;s.add(well);
  keyField(s,legends.concat([['fn','⌃','⌥','⌘','','⌘','⌥','◀','▼','▶']]),-W/2+1.6,-D/2+1.4,W-3.2,D-2.8,1.0,{wt:(r,i,n)=>{if(r==5){return i==4?6:1}return WT1(r,i,n)}});
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:2.4,d:D},views:['top']}}
export async function laptopLid(){
  const s=makeScene();const W=60,H=35;
  s.add(rbox(W,H,1.3,1.8,M.alu(0xcfd2d7),8));
  const fg=plateRR(W-.8,H-.8,1.5,M.glass());fg.position.z=.66;s.add(fg);
  const t=await svgTexture(laptopScreen2(W,H),[1.2,1.2,W-2.4,H-2.4],30);
  const sc=plateRR(W-2.4,H-2.4,.6,screenMat(t,.3));sc.position.z=.67;s.add(sc);
  s.add(logo(0,0,-.66,3.4));
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:H,d:2},views:['front','back']}}
export async function laptopBase(){
  const s=makeScene();const W=60,D=40;
  s.add(rbox(W,3,D,1.9,M.alu(0xcfd2d7),8));
  const kx=-W/2+3.5,kz=-D/2+7.2,kw=W-7,kd=17.5;
  const well=new THREE.Mesh(new THREE.PlaneGeometry(kw+1.2,kd+1.2),M.matte(0x16171a,.85));well.rotation.x=-PI/2;well.position.set(0,1.505,kz+kd/2);s.add(well);
  keyField(s,[legends[0].map(t=>t.startsWith('F')||t=='esc'?t:'')].concat(legends.slice(1)),kx,kz,kw,kd,1.1,{wt:(r,i,n)=>r==0?1:WT1(r,i,n),gap:.3});
  // speaker grills
  const gc=textCanvas(9,3.4,40,(c)=>{c.fillStyle='#2b2d32';for(let r=0;r<5;r++)for(let k=0;k<20;k++){c.beginPath();c.arc(.25+k*.44,.3+r*.68,.14,0,7);c.fill()}});
  [-1,1].forEach(sd=>{const g=new THREE.Mesh(new THREE.PlaneGeometry(9,3.4),new THREE.MeshBasicMaterial({map:tex(gc),transparent:true}));g.rotation.x=-PI/2;g.position.set(sd*(W/2-8.5),1.51,-D/2+3.2);s.add(g)});
  const tp=rbox(21,.25,10,.9,new THREE.MeshPhysicalMaterial({color:0xc2c5ca,roughness:.22,clearcoat:.6,metalness:.4}));tp.position.set(0,1.45,kz+kd+2+5);s.add(tp);
  const lip=rbox(10,.5,1.2,.4,M.alu(0xb9bcc2));lip.position.set(0,1.3,D/2-.3);s.add(lip);
  return {scene:s,box:{cx:0,cy:0,cz:0,w:W,h:3,d:D},views:['top']}}
