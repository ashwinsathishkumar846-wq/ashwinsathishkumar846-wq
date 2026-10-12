// ===== PHONE =====
const statusIcons=(w,y,col='#fff')=>{ // right side: signal, wifi, battery
  let s='';const x0=w-8.2;
  [0,1,2,3].forEach(i=>s+=R(x0+i*.75,y+1.15-i*.28,.5,.35+i*.28,{f:col,r:.12}));
  s+=P(`M${x0+3.6} ${y+1.3} q.9 -.9 1.8 0 M${x0+3.95} ${y+1.65} q.55 -.5 1.1 0`,{s:col,w:.2});s+=C(x0+4.5,y+1.95,.14,{f:col});
  s+=R(x0+6,y+.55,1.9,1,{f:'none',s:col,w:.14,r:.28})+R(x0+6.12,y+.67,1.35,.76,{f:col,r:.15})+R(x0+7.92,y+.85,.14,.4,{f:col,r:.05});
  return s};
const phoneFront2=(w,h)=>{
  let s='';
  // titanium frame
  s+=R(0,0,w,h,{f:'url(#gTi)',r:3.4,s:'#2a2c30',w:.25});
  s+=R(.55,.55,w-1.1,h-1.1,{f:'#050506',r:2.9});
  const sx=.95,sy=.95,sw=w-1.9,sh=h-1.9;
  const wp=wallBloom(sx,sy,sw,sh,'sunset');
  s+=inClip(sx,sy,sw,sh,2.5,wp);
  // content clipped
  let c='';
  c+=T(sx+2.3,sy+2.9,'10:24',{sz:1.05,a:'start',f:'#fff',b:1,ff:UI});
  c+=statusIcons(sx+sw+0.6,sy+1.7);
  c+=R(w/2-2.9,sy+1.1,5.8,1.65,{f:'#000',r:.83});c+=C(w/2+1.7,sy+1.92,.34,{f:'#10162b'});
  c+=T(w/2,sy+7.6,'Monday 12 October',{sz:1.15,f:'rgba(255,255,255,.85)',ff:UI});
  c+=T(w/2,sy+13.8,'10:24',{sz:6.4,f:'#fff',ff:UI,b:1,ls:-.1});
  c+=R(sx+2.2,sy+17.6,sw-4.4,3.1,{f:'rgba(255,255,255,.22)',r:1.1})+T(sx+3.2,sy+19.1,'●',{sz:1,a:'start',f:'#fff'})+T(sx+4.6,sy+18.9,'Today',{sz:.85,a:'start',f:'#fff',b:1,ff:UI})+T(sx+4.6,sy+19.9,'No events',{sz:.7,a:'start',f:'rgba(255,255,255,.8)',ff:UI});
  c+=C(sx+3.2,sy+sh-4.2,1.5,{f:'rgba(20,20,40,.45)'})+C(sx+sw-3.2,sy+sh-4.2,1.5,{f:'rgba(20,20,40,.45)'});
  c+=R(sx+2.45,sy+sh-5.1,1.5,1.9,{f:'none',s:'#fff',w:.15,r:.4});c+=R(sx+sw-3.95,sy+sh-5,1.5,1.5,{f:'none',s:'#fff',w:.15,r:.3})+C(sx+sw-3.2,sy+sh-4.25,.4,{f:'none',s:'#fff',w:.15});
  c+=R(w/2-3,sy+sh-1.2,6,.45,{f:'#fff',r:.22});
  s+=inClip(sx,sy,sw,sh,2.5,c);
  s+=sheen(sx,sy,sw,sh,2.5,.9);
  return s};
const phoneBack2=(w,h)=>{
  let s=R(0,0,w,h,{f:'url(#gTi)',r:3.4,s:'#2a2c30',w:.25});
  s+=R(.5,.5,w-1,h-1,{f:'url(#gGraph)',r:2.95});
  s+=tex(.5,.5,w-1,h-1,2.95,'fBrush',.1);
  // camera plateau
  const px=1.8,py=1.8,pw=9.2,ph=9.4;
  s+=R(px,py,pw,ph,{f:'#202226',r:2.3,s:'#6b6e75',w:.3})+R(px+.25,py+.25,pw-.5,ph-.5,{f:'#15161a',r:2.1});
  [[px+3,py+3],[px+3,py+6.6],[px+6.4,py+4.8]].forEach(([cx,cy])=>{s+=C(cx,cy,2.05,{f:'url(#gLens)',s:'#0c0d10',w:.15})+C(cx,cy,1.55,{f:'#0b0c10',s:'#4b4e56',w:.1})+C(cx,cy,1.15,{f:'url(#gLensIn)'})+C(cx-.35,cy-.4,.28,{f:'#fff',op:.55})+C(cx+.35,cy+.4,.12,{f:'#8aa0ff',op:.5})});
  s+=C(px+7.2,py+1.8,.55,{f:'#f2e3b0',s:'#6b6e75',w:.1})+C(px+7.2,py+8,.35,{f:'#0a0a0c',s:'#555',w:.1})+C(px+5.6,py+1.8,.25,{f:'#0a0a0c'});
  s+=logoRing(w/2,h*.56,2.4,'#9a9da4');
  s+=T(w/2,h-4.2,'Designed in Coimbatore',{sz:.7,f:'#7e8188',ff:UI});
  s+=sheen(.5,.5,w-1,h-1,2.95,.8);
  return s};
const phoneSide=(w,h)=>R(0,0,w,h,{f:'url(#gTi)',s:'#2a2c30',w:.15})+tex(0,0,w,h,0,'fBrush',.25)+R(w*.5-.7,h*.15,1.4,3,{f:'#8f9298',r:.5})+R(w*.5-.7,h*.27,1.4,5,{f:'#7d8086',r:.5})+R(w*.5-.7,h*.43,1.4,5,{f:'#7d8086',r:.5});
const phoneSideR=(w,h)=>R(0,0,w,h,{f:'url(#gTi)',s:'#2a2c30',w:.15})+tex(0,0,w,h,0,'fBrush',.25)+R(w*.5-.7,h*.28,1.4,8.5,{f:'#7d8086',r:.5});
const phoneBottom=(w,h)=>R(0,0,w,h,{f:'url(#gTi)',s:'#2a2c30',w:.15})+R(w/2-2.2,h/2-.6,4.4,1.2,{f:'#0c0c0e',r:.6})+[...Array(6)].map((_,i)=>C(w/2-7.5+i*.9,h/2,.28,{f:'#16171a'})).join('')+[...Array(6)].map((_,i)=>C(w/2+3.1+i*.9,h/2,.28,{f:'#16171a'})).join('');
const phoneTop=(w,h)=>R(0,0,w,h,{f:'url(#gTi)',s:'#2a2c30',w:.15})+tex(0,0,w,h,0,'fBrush',.25);
// ===== TABLET =====
const tabletFront2=(w,h)=>{
  let s=R(0,0,w,h,{f:'url(#gAlV)',r:3.2,s:'#7b7e84',w:.25});
  s+=R(.55,.55,w-1.1,h-1.1,{f:'#050506',r:2.7});
  const sx=1.9,sy=1.9,sw=w-3.8,sh=h-3.8;
  let c=wallBloom(sx,sy,sw,sh,'blue');
  c+=T(sx+2.5,sy+2.7,'10:24  Mon 12 Oct',{sz:1.05,a:'start',f:'#fff',b:1,ff:UI});c+=statusIcons(sx+sw+.4,sy+1.6);
  // widgets
  c+=R(sx+3,sy+4.6,10.5,7.6,{f:'url(#gSky)',r:1.6})+T(sx+4,sy+7.6,'Coimbatore',{sz:.9,a:'start',f:'#fff',b:1,ff:UI})+T(sx+4,sy+11.6,'30°',{sz:3.2,a:'start',f:'#fff',ff:UI})+T(sx+4,sy+13.1,'Partly Cloudy',{sz:.7,a:'start',f:'#fff',ff:UI});
  c+=R(sx+14.5,sy+4.6,10.5,7.6,{f:'rgba(255,255,255,.88)',r:1.6})+T(sx+15.5,sy+7.2,'OCTOBER',{sz:.85,a:'start',f:'#ff3b30',b:1,ff:UI})+['M','T','W','T','F','S','S'].map((d,i)=>T(sx+16.2+i*1.3,sy+8.7,d,{sz:.6,f:'#555',ff:UI})).join('')+[...Array(21)].map((_,i)=>T(sx+16.2+(i%7)*1.3,sy+9.9+Math.floor(i/7)*1.25,String(i+5),{sz:.62,f:i+5==12?'#fff':'#222',ff:UI})).join('')+C(sx+16.2+4*1.3,sy+9.9+.55*1.25+1.25-.3,.62,{f:'#ff3b30',op:.0});
  c+=R(sx+26,sy+4.6,10.5,7.6,{f:'#0c0c10',r:1.6})+C(sx+31.25,sy+9.5,3.4,{f:'#fff'})+L(sx+31.25,sy+9.5,sx+31.25,sy+7,{s:'#111',w:.2})+L(sx+31.25,sy+9.5,sx+32.9,sy+10.3,{s:'#111',w:.2})+L(sx+31.25,sy+9.5,sx+30.6,sy+11.2,{s:'#ff9500',w:.1});
  // icon grid
  const kinds=['messages','mail','phone','safari','photos','camera','maps','calendar','clock','notes','music','settings'];
  kinds.forEach((k,i)=>{const col=i%6,row=Math.floor(i/6);const x=sx+3.4+col*5.9,y=sy+13.6+row*5.0;c+=appIcon(k,x,y,3.6)+T(x+1.8,y+4.45,k[0].toUpperCase()+k.slice(1),{sz:.58,f:'#fff',ff:UI})});
  c+=R(sx+sw/2-14.5,sy+sh-5.4,29,4.4,{f:'rgba(255,255,255,.3)',r:1.6});['phone','safari','messages','music','mail'].forEach((k,i)=>c+=appIcon(k,sx+sw/2-13.2+i*5.3,sy+sh-4.9,3.5));
  c+=R(sx+sw/2-3.5,sy+sh-.7,7,.35,{f:'#fff',r:.17});
  s+=inClip(sx,sy,sw,sh,1.2,c);s+=sheen(sx,sy,sw,sh,1.2,.9);
  s+=C(w/2,1.25,.38,{f:'#12141c',s:'#2d3140',w:.1});
  return s};
const tabletBack2=(w,h)=>{
  let s=R(0,0,w,h,{f:'url(#gAl)',r:3.2,s:'#7b7e84',w:.25})+brushed(0,0,w,h,3.2,.5);
  s+=R(2.6,2.6,9,9,{f:'url(#gAlV)',r:2.6,s:'#8d9097',w:.3})+C(7.1,7.1,3,{f:'url(#gLens)',s:'#4a4d54',w:.2})+C(7.1,7.1,2.3,{f:'#0b0c10',s:'#666',w:.12})+C(7.1,7.1,1.7,{f:'url(#gLensIn)'})+C(6.5,6.4,.45,{f:'#fff',op:.55})+C(10.3,3.9,.4,{f:'#e8e0b0',s:'#8d9097',w:.1});
  s+=logoRing(w/2,h/2,3.2,'#9a9da4');
  s+=T(w/2,h-6.4,'Tablet  •  Wi-Fi',{sz:1.2,f:'#8a8d93',ff:UI});s+=T(w/2,h-4.6,'Model  A-2026   S/N  CBE0000TAB26',{sz:.75,f:'#9a9da4',ff:UI});
  s+=sheen(0,0,w,h,3.2,.9);return s};
const tabEdge=(w,h)=>R(0,0,w,h,{f:'url(#gAlV)',s:'#7b7e84',w:.12})+tex(0,0,w,h,0,'fBrush',.25);
