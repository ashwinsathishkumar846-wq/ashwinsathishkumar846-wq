// ===== MONITOR (70 x 50 incl. stand) =====
const KW={kw:'#c586c0',fn:'#dcdcaa',str:'#ce9178',cm:'#6a9955',pl:'#d4d4d4',ty:'#4ec9b0',bl:'#569cd6',nm:'#b5cea8'};
const monitorFront2=(w,h)=>{
  const hh=h-14;let s='';
  // stand
  s+=P(`M${w/2-6} ${hh-.3} L${w/2+6} ${hh-.3} L${w/2+8.5} ${h-3.3} L${w/2-8.5} ${h-3.3} Z`,{f:'url(#gAlV)',s:'#7d8086',w:.25})+R(w/2-8.5,h-3.5,17,.5,{f:'rgba(0,0,0,.18)'});
  s+=P(`M${w/2-17} ${h-2.3} Q${w/2-17} ${h-3.6} ${w/2-12} ${h-3.8} L${w/2+12} ${h-3.8} Q${w/2+17} ${h-3.6} ${w/2+17} ${h-2.3} Q${w/2+17} ${h-.4} ${w/2+12} ${h-.3} L${w/2-12} ${h-.3} Q${w/2-17} ${h-.4} ${w/2-17} ${h-2.3} Z`,{f:'url(#gAlV)',s:'#7d8086',w:.25});
  s+=R(w/2-14,h-3.3,28,.35,{f:'rgba(255,255,255,.7)',r:.17});
  // body
  s+=R(0,0,w,hh,{f:'url(#gAl)',r:2,s:'#6c6f75',w:.3})+brushed(0,0,w,hh,2,.35);
  s+=R(.8,.8,w-1.6,hh-1.6,{f:'#050506',r:1.5});
  const sx=1.5,sy=1.5,sw=w-3,sh=hh-4.5;
  let c=R(sx,sy,sw,sh,{f:'#1e1e1e'});
  // title bar
  c+=R(sx,sy,sw,2.4,{f:'#323233'});[0,1,2].forEach(i=>c+=C(sx+1.6+i*1.5,sy+1.2,.42,{f:['#ff5f57','#febc2e','#28c840'][i]}));c+=T(sx+sw/2,sy+1.65,'hello.py — project — Visual Studio Code',{sz:.95,f:'#9d9d9d',ff:UI});
  // activity bar
  c+=R(sx,sy+2.4,3.6,sh-2.4-1.9,{f:'#333333'});[0,1,2,3].forEach(i=>c+=R(sx+1,sy+4+i*3.4,1.6,1.6,{f:'none',s:i==0?'#fff':'#858585',w:.2,r:.3}));
  // sidebar
  c+=R(sx+3.6,sy+2.4,13,sh-2.4-1.9,{f:'#252526'})+T(sx+5,sy+4.4,'EXPLORER',{sz:.75,a:'start',f:'#bbb',ff:UI})+T(sx+5,sy+6.4,'▾ PROJECT',{sz:.75,a:'start',f:'#ccc',b:1,ff:UI})+T(sx+6.2,sy+8.1,'hello.py',{sz:.8,a:'start',f:'#e8e8a8',ff:UI})+R(sx+3.6,sy+7.1,13,1.6,{f:'rgba(255,255,255,.07)'})+T(sx+6.2,sy+9.8,'main.c',{sz:.8,a:'start',f:'#ccc',ff:UI})+T(sx+6.2,sy+11.5,'README.md',{sz:.8,a:'start',f:'#ccc',ff:UI});
  // tabs
  c+=R(sx+16.6,sy+2.4,sw-16.6,2.4,{f:'#2d2d2d'})+R(sx+16.6,sy+2.4,9,2.4,{f:'#1e1e1e'})+T(sx+17.6,sy+4.05,'hello.py',{sz:.85,a:'start',f:'#fff',ff:UI});
  // editor lines
  const ex=sx+16.6,ey=sy+6.1;const lh=1.75;
  const code=[[['cm','# Evolution of Computer Science']],[['kw','def '],['fn','main'],['pl','():']],[['pl','    '],['fn','print'],['pl','('],['str','"Hello, World!"'],['pl',')']],[],[['kw','if '],['pl','__name__ == '],['str','"__main__"'],['pl',':']],[['pl','    '],['fn','main'],['pl','()']]];
  code.forEach((ln,i)=>{c+=T(ex+3.4,ey+i*lh,String(i+1),{sz:.9,a:'end',f:'#6e7681',ff:MONO});let x=ex+4.6;ln.forEach(([k,t])=>{c+=`<text x="${f(x)}" y="${f(ey+i*lh)}" font-size="1.1" font-family="${MONO}" fill="${KW[k]}" xml:space="preserve">${t.replace(/ /g,'\u00A0')}</text>`;x+=t.length*.66})});
  c+=R(ex+4.6,ey+2*lh-1.2,.12,1.6,{f:'#aeafad'});
  // </> watermark
  c+=T(sx+sw-11,sy+sh*.52,'&lt;/&gt;',{sz:7,f:'rgba(255,255,255,.1)',ff:MONO,b:1});
  // minimap
  c+=R(sx+sw-6,sy+4.8,6,sh-8,{f:'#242424'});[...Array(10)].forEach((_,i)=>c+=R(sx+sw-5.4,sy+5.6+i*.9,2.5+((i*7)%3),.35,{f:['#c586c0','#dcdcaa','#ce9178'][i%3],op:.6}));
  // terminal
  const ty=sy+sh-10.5;c+=R(ex,ty,sw-16.6,10.5-1.9,{f:'#1e1e1e'})+L(ex,ty,sx+sw,ty,{s:'#3c3c3c',w:.2})+T(ex+1,ty+1.6,'TERMINAL',{sz:.75,a:'start',f:'#e7e7e7',ff:UI})+T(ex+1.4,ty+3.7,'$ python hello.py',{sz:.95,a:'start',f:'#cccccc',ff:MONO})+T(ex+1.4,ty+5.4,'Hello, World!',{sz:.95,a:'start',f:'#6cdb7a',ff:MONO});
  // status bar
  c+=R(sx,sy+sh-1.9,sw,1.9,{f:'#007acc'})+T(sx+1.2,sy+sh-.55,'⎇ main   ✓ 0  ⚠ 0',{sz:.8,a:'start',f:'#fff',ff:UI})+T(sx+sw-1.2,sy+sh-.55,'Ln 3, Col 25    Python 3.12',{sz:.8,a:'end',f:'#fff',ff:UI});
  s+=inClip(sx,sy,sw,sh,.5,c);s+=sheen(sx,sy,sw,sh,.5,.8);
  s+=logoRing(w/2,hh-1.6,.55,'#7d8086');
  return s};
const monitorBack2=(w,h)=>{const hh=h-14;let s='';
  s+=P(`M${w/2-6} ${hh-.3} L${w/2+6} ${hh-.3} L${w/2+8.5} ${h-3.3} L${w/2-8.5} ${h-3.3} Z`,{f:'url(#gAlV)',s:'#7d8086',w:.25});
  s+=P(`M${w/2-17} ${h-2.3} Q${w/2-17} ${h-3.6} ${w/2-12} ${h-3.8} L${w/2+12} ${h-3.8} Q${w/2+17} ${h-3.6} ${w/2+17} ${h-2.3} Q${w/2+17} ${h-.4} ${w/2+12} ${h-.3} L${w/2-12} ${h-.3} Q${w/2-17} ${h-.4} ${w/2-17} ${h-2.3} Z`,{f:'url(#gAlV)',s:'#7d8086',w:.25});
  s+=R(0,0,w,hh,{f:'url(#gAl)',r:2,s:'#6c6f75',w:.3})+brushed(0,0,w,hh,2,.5);
  s+=logoRing(w/2,hh*.45,3.6,'#9a9da4');
  s+=R(w/2-5,hh-5,10,3,{f:'#2a2c31',r:.6,s:'#6c6f75',w:.2});[0,1,2,3].forEach(i=>s+=R(w/2-4+i*2.2,hh-4.2,1.4,1.2,{f:'#0a0a0c',r:.3}));
  s+=T(w/2,hh-7,'27-inch Display   •   4K UHD',{sz:1.1,f:'#7d8086',ff:UI});
  s+=sheen(0,0,w,hh,2,.8);return s};
// ===== KEYBOARD (60 x 20) =====
const legends=[['esc','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','⏏'],['`','1','2','3','4','5','6','7','8','9','0','-','=','⌫'],['⇥','Q','W','E','R','T','Y','U','I','O','P','[',']','\\'],['⇪','A','S','D','F','G','H','J','K','L',';',"'",'⏎'],['⇧','Z','X','C','V','B','N','M',',','.','/','⇧']];
const keyboardTop2=(w,h)=>{
  let s=R(0,0,w,h,{f:'url(#gAl)',r:1.8,s:'#7b7e84',w:.3})+brushed(0,0,w,h,1.8,.4);
  s+=R(1,1,w-2,h-2,{f:'#111214',r:1.2});
  const rows=legends.length;const gap=.35;const kh=(h-3.4-gap*(rows))/(rows+0.15);
  legends.forEach((row,r)=>{const n=row.length;
    const wt=row.map((t,i)=>{let k=1;if(r==1&&i==n-1)k=1.45;if(r==2&&i==0)k=1.35;if(r==3&&i==0)k=1.6;if(r==3&&i==n-1)k=1.5;if(r==4&&(i==0||i==n-1))k=2.1;return k});
    const unit=(w-3.4-gap*(n-1))/wt.reduce((p,q)=>p+q,0);let x=1.7;
    row.forEach((t,i)=>{const ww=unit*wt[i];const y=1.7+r*(kh+gap);
      s+=R(x,y,ww,kh,{f:'url(#gGraph)',r:.45,s:'#000',w:.1})+R(x+.2,y+.15,ww-.4,kh*.4,{f:'rgba(255,255,255,.1)',r:.35});
      s+=T(x+ww/2,y+kh*.66,t,{sz:r==0?.7:Math.min(1.5,ww*.4),f:'#d6d8dc',ff:UI,b:r>0});x+=ww+gap});
  });
  return s};
// ===== LAPTOP =====
const laptopScreen2=(w,h)=>{
  let s=R(0,0,w,h,{f:'url(#gAl)',r:1.8,s:'#6c6f75',w:.3});
  s+=R(.5,.5,w-1,h-1,{f:'#050506',r:1.4});
  const sx=1.2,sy=1.2,sw=w-2.4,sh=h-2.4;
  let c=wallBloom(sx,sy,sw,sh,'blue');
  c+=R(sx,sy,sw,2.2,{f:'rgba(255,255,255,.22)'})+T(sx+3.6,sy+1.55,'Finder   File   Edit   View   Go   Window   Help',{sz:.85,a:'start',f:'#fff',ff:UI});c+=T(sx+sw-1.5,sy+1.55,'Mon 12 Oct  10:24',{sz:.85,a:'end',f:'#fff',b:1,ff:UI});
  c+=R(sx+sw/2-5.8,sy-.1,11.6,2.3,{f:'#050506',r:1}) ;
  c+=P(`M${sx+4} ${sy+sh*.62} C${sx+sw*.3} ${sy+sh*.35} ${sx+sw*.5} ${sy+sh*.9} ${sx+sw*.9} ${sy+sh*.5}`,{s:'rgba(255,255,255,.18)',w:3});
  c+=R(sx+sw/2-14.5,sy+sh-5.8,29,5,{f:'rgba(255,255,255,.28)',r:1.7,s:'rgba(255,255,255,.4)',w:.12});
  ['safari','mail','messages','maps','photos','calendar','notes','music','settings'].forEach((k,i)=>c+=appIcon(k,sx+sw/2-13.6+i*3.1,sy+sh-5.3,2.7));
  s+=inClip(sx,sy,sw,sh,.6,c);s+=sheen(sx,sy,sw,sh,.6,.9);
  return s};
const laptopLid2=(w,h)=>R(0,0,w,h,{f:'url(#gAl)',r:1.8,s:'#6c6f75',w:.3})+brushed(0,0,w,h,1.8,.5)+R(.6,.6,w-1.2,h-1.2,{f:'none',s:'rgba(255,255,255,.65)',w:.25,r:1.4})+logoRing(w/2,h/2,3.3,'#9a9da4')+sheen(0,0,w,h,1.8,.8);
const laptopBase2=(w,h)=>{
  let s=R(0,0,w,h,{f:'url(#gAl)',r:2,s:'#6c6f75',w:.3})+brushed(0,0,w,h,2,.4);
  s+=R(0,0,w,1.1,{f:'rgba(0,0,0,.18)'});
  // speaker grills
  [4,w-4-8].forEach(x=>{for(let r=0;r<4;r++)for(let c=0;c<18;c++)s+=C(x+c*.45+.2,3.1+r*.7,.15,{f:'#3b3d42'})});
  // keys
  const kx=3.5,ky=7.2,kw_=w-7,kh_=17.5;s+=R(kx-.6,ky-.6,kw_+1.2,kh_+1.2,{f:'#17181b',r:.8});
  const L2=legends.slice(1);const rows=L2.length+1;const gap=.3;const kh=(kh_-gap*(rows-1))/rows;
  const all=[legends[0].map(()=>'')].concat(L2);
  all.forEach((row,r)=>{const n=row.length;
    const wt=row.map((t,i)=>{let k=1;if(r==2&&i==n-1)k=1.45;if(r==3&&i==0)k=1.35;if(r==4&&i==0)k=1.6;if(r==4&&i==n-1)k=1.5;if(r==5&&(i==0||i==n-1))k=2.1;return k});
    const unit=(kw_-gap*(n-1))/wt.reduce((p,q)=>p+q,0);let x=kx;
    row.forEach((t,i)=>{const ww=unit*wt[i];const y=ky+r*(kh+gap);
      s+=R(x,y,ww,kh,{f:'#0d0e10',r:.4,s:'#000',w:.08})+R(x+.15,y+.1,ww-.3,kh*.45,{f:'rgba(255,255,255,.07)',r:.3});s+=T(x+ww/2,y+kh*.65,t,{sz:Math.min(1.3,ww*.38),f:'#cfd2d6',ff:UI});x+=ww+gap})});
  // trackpad
  s+=R(w/2-10,ky+kh_+2,20,h-ky-kh_-3.6,{f:'rgba(0,0,0,.04)',r:1,s:'#9da1a8',w:.2})+R(w/2-10,ky+kh_+2,20,.5,{f:'rgba(255,255,255,.5)',r:.25});
  s+=sheen(0,0,w,h,2,.5);return s};
// ===== BOOKS (3 separate) =====
function bookSet(title,base,dark,foil){
  const leather=(w,h,op=.55)=>tex(0,0,w,h,0,'fLeather',op);
  const cover=(w,h,withTitle)=>{let s=R(0,0,w,h,{f:base})+leather(w,h)+R(0,0,w,h,{f:'url(#gSheen)',op:.5});
    s+=R(1.6,1.6,w-3.2,h-3.2,{f:'none',s:foil,w:.35})+R(2.3,2.3,w-4.6,h-4.6,{f:'none',s:foil,w:.15});
    // corner ornaments
    [[2.8,2.8,1],[w-2.8,2.8,-1],[2.8,h-2.8,1],[w-2.8,h-2.8,-1]].forEach(([x,y,d])=>s+=P(`M${x} ${y} q${d*1.6} 0 ${d*1.6} ${y<h/2?1.6:-1.6}`,{s:foil,w:.2}));
    if(withTitle){s+=T(w/2+.15,h*.46+.15,title.toUpperCase(),{sz:3.8,f:'rgba(0,0,0,.55)',ff:'Raleway,serif',b:1,ls:.3})+T(w/2,h*.46,title.toUpperCase(),{sz:3.8,f:foil,ff:'Raleway,serif',b:1,ls:.3});s+=L(w*.22,h*.56,w*.78,h*.56,{s:foil,w:.2})+C(w/2,h*.56,.6,{f:foil});s+=T(w/2,h*.8,'COMPUTER SCIENCE',{sz:1.25,f:foil,ff:UI,ls:.4})}
    return s};
  const spine=(w,h)=>{let s=R(0,0,w,h,{f:base})+leather(w,h)+R(0,0,w,h*.5,{f:'rgba(255,255,255,.1)'})+R(0,h*.7,w,h*.3,{f:'rgba(0,0,0,.28)'});
    [3.4,w-3.4,6.3,w-6.3].forEach((x,i)=>s+=R(x-.35,0,.7,h,{f:i<2?foil:'none',s:i<2?'none':foil,w:.15,op:.95}));
    s+=R(8.6,h*.18,w-17.2,h*.64,{f:'none',s:foil,w:.2});
    s+=T(w/2+.12,h*.66+.1,title,{sz:Math.min(h*.46,(w-18)/title.length*1.7),f:'rgba(0,0,0,.5)',ff:'Raleway,serif',b:1,ls:.25})+T(w/2,h*.66,title,{sz:Math.min(h*.46,(w-18)/title.length*1.7),f:foil,ff:'Raleway,serif',b:1,ls:.25});
    s+=R(0,0,w,.5,{f:'rgba(255,255,255,.25)'});return s};
  const pages=(w,h,sideways)=>{let s=R(0,0,w,h,{f:'#f3ead3'});const n=Math.floor(h/.28);for(let i=0;i<n;i++)s+=L(0,i*.28+.14,w,i*.28+.14,{s:'rgba(150,130,90,.35)',w:.08});
    s+=R(0,0,w,h,{f:'url(#gSheen)',op:.35});
    s+=R(0,0,w,1.1,{f:base})+R(0,h-1.1,w,1.1,{f:base})+leather(w,h,.0)+tex(0,0,w,1.1,0,'fLeather',.5)+tex(0,h-1.1,w,1.1,0,'fLeather',.5);return s};
  const foreedge=(w,h)=>{let s=pages(w,h);s+=R(2,h*.08,.6,h*.84,{f:'none'});return s};
  const head=(w,h)=>{let s=pages(w,h);s+=R(0,0,2,h,{f:base})+tex(0,0,2,h,0,'fLeather',.5)+R(.5,h*.5-.1,.3,.2,{f:foil});s+=R(w-1.2,1.1,.5,h-2.2,{f:'#c0392b',op:.0});return s};
  return {spine,cover,back:(w,h)=>R(0,0,w,h,{f:base})+tex(0,0,w,h,0,'fLeather',.55)+R(0,0,w,h,{f:'url(#gSheen)',op:.4})+R(1.6,1.6,w-3.2,h-3.2,{f:'none',s:foil,w:.3}),foreedge,head,
    plain:(w,h)=>R(0,0,w,h,{f:base})+tex(0,0,w,h,0,'fLeather',.55)};
}
const BOOKS=[bookSet('Binary','#5a3a22','#2c1a0e','url(#gGold)'),bookSet('Logic','#1e3257','#0d1a30','url(#gSilverFoil)'),bookSet('Algorithms','#6a1f2a','#350c14','url(#gGold)')];
const mkBook=(b)=>boxNet(40,12,30,{front:b.spine,top:(w,h)=>b.cover(w,h,true),bottom:b.back,left:b.head,right:b.head,back:b.foreedge});
