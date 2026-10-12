// ===== SIGNS / HEADINGS =====
const signboard2=(txt)=>(w,h)=>{let s=R(0,0,w,h,{f:'#0a2a7a',r:1.4,s:'#1a6bff',w:.5});
  s+=`<rect x=".3" y=".3" width="${w-.6}" height="${h-.6}" rx="1.2" fill="none" stroke="#3fb4ff" stroke-width=".9" filter="url(#gl1)"/>`;
  s+=R(.9,.9,w-1.8,h-1.8,{f:'url(#gHolo)',r:.9,s:'#7fd6ff',w:.2});
  s+=R(.9,.9,w-1.8,(h-1.8)*.5,{f:'rgba(255,255,255,.6)',r:.9});
  s+=T(w/2,h/2+1.5,txt,{sz:4.4,f:'#0d2a78',b:1,ff:RAL,ls:.1});return s};
const signboardBack2=(w,h)=>R(0,0,w,h,{f:'#0a2a7a',r:1.4,s:'#1a6bff',w:.5});
const imagineSign2=(w,h)=>R(0,0,w,h,{f:'#030c26',r:1.6,s:'#2aa6ff',w:.5})+`<rect x=".4" y=".4" width="${w-.8}" height="${h-.8}" rx="1.4" fill="none" stroke="#2aa6ff" stroke-width=".9" filter="url(#gl1)"/>`+R(.9,h-2.1,w-1.8,1.2,{f:'url(#gHoloFrame)',r:.4})+`<text x="${w/2}" y="${h/2+1.3}" font-size="5" font-family="Raleway,sans-serif" font-weight="700" text-anchor="middle" fill="#2aa6ff" opacity=".8" filter="url(#gl1)" letter-spacing=".25">Imagine  •  Create  •  Innovate</text>`+T(w/2,h/2+1.3,'Imagine  •  Create  •  Innovate',{sz:5,f:'#eaf6ff',b:1,ff:RAL,ls:.25});
const paperEdge=(w,h,r)=>`<defs></defs>`;
const cloudArt2=(w,h)=>{
  const d=`M${w*.13} ${h*.7} C${w*.0} ${h*.7} ${w*.0} ${h*.38} ${w*.12} ${h*.36} C${w*.08} ${h*.12} ${w*.3} ${h*.04} ${w*.38} ${h*.16} C${w*.46} ${h*-.02} ${w*.7} ${h*.0} ${w*.74} ${h*.17} C${w*.86} ${h*.06} ${w*.97} ${h*.22} ${w*.9} ${h*.38} C${w*1.02} ${h*.46} ${w*.99} ${h*.7} ${w*.86} ${h*.7} C${w*.84} ${h*.9} ${w*.62} ${h*.97} ${w*.52} ${h*.84} C${w*.4} ${h*.98} ${w*.2} ${h*.92} ${w*.13} ${h*.7} Z`;
  let s=`<path d="${d}" transform="translate(.9,1.2)" fill="rgba(0,0,0,.18)" filter="url(#gl1)"/>`+P(d,{f:'#fbf8ff',s:'#4b2f8f',w:1.1});
  s+=`<clipPath id="cl_c"><path d="${d}"/></clipPath><g clip-path="url(#cl_c)">${R(0,0,w,h,{f:'url(#gPill)',op:.9})}<rect width="${w}" height="${h}" filter="url(#fPaper)" opacity=".35"/></g>`+P(d,{s:'#4b2f8f',w:1.1});
  s+=P(d,{s:'#a98be0',w:.3,op:.9}).replace('d="','transform="translate(0,0) scale(.97) translate('+w*.016+','+h*.016+')" d="');
  s+=T(w*.5+.25,h*.41+.3,'Evolution of',{sz:h*.2,f:'rgba(80,60,130,.35)',b:1,ff:RAL})+T(w*.5,h*.41,'Evolution of',{sz:h*.2,f:'#1d1238',b:1,ff:RAL});
  s+=T(w*.5+.25,h*.67+.3,'Computer Science',{sz:h*.2,f:'rgba(80,60,130,.35)',b:1,ff:RAL})+T(w*.5,h*.67,'Computer Science',{sz:h*.2,f:'#1d1238',b:1,ff:RAL});
  [[.075,.5],[.925,.54]].forEach(([x,y])=>[-1,0,1].forEach(k=>s+=L(w*x,h*y+k*3.2,w*x+(x<.5?-1:1)*(k==0?4:3),h*y+k*3.2+k*1.2,{s:'#4b2f8f',w:.35})));
  return s};
const pill2=(l1,l2)=>(w,h)=>{let s=`<rect x=".6" y=".9" width="${w-.2}" height="${h-.2}" rx="${h*.42}" fill="rgba(0,0,0,.18)" filter="url(#gl1)"/>`+R(0,0,w,h,{f:'#fbf8ff',r:h*.42,s:'#4b2f8f',w:.9});
  s+=R(.5,.5,w-1,h-1,{f:'url(#gPill)',r:h*.4})+tex(.5,.5,w-1,h-1,h*.4,'fPaper',.3)+R(1.4,1.4,w-2.8,h*.35,{f:'rgba(255,255,255,.55)',r:h*.3})+R(0,0,w,h,{f:'none',s:'#4b2f8f',w:.9,r:h*.42});
  s+=T(w/2,l2?h*.46:h*.64,l1,{sz:h*.34,f:'#1d1238',b:1,ff:RAL})+(l2?T(w/2,h*.78,l2,{sz:h*.2,f:'#1d1238',ff:RAL}):'');return s};
const pillBack2=(w,h)=>R(0,0,w,h,{f:'#4b2f8f',r:h*.42});
// ===== PLATFORMS =====
const soilTop2=(w,h)=>R(0,0,w,h,{f:'#5a2c12'})+`<rect width="${w}" height="${h}" filter="url(#fSoil)"/>`+`<rect width="${w}" height="${h}" filter="url(#fSoil2)" opacity=".55"/>`+[...Array(70)].map((_,i)=>{const x=(i*47.3)%w,y=(i*31.7)%h,r=.5+(i%4)*.45;return E_(x,y,r*1.3,r,{f:i%3?'#9a8f84':'#6e6258',rot:i*40})+E_(x-.2,y-.2,r*.5,r*.35,{f:'rgba(255,255,255,.35)'})}).join('')+R(0,0,w,h,{f:'url(#gSheen)',op:.15});
const soilSide2=(w,h)=>R(0,0,w,h,{f:'#4a230e'})+`<rect width="${w}" height="${h}" filter="url(#fSoil)" opacity=".9"/>`+R(0,0,w,h*.18,{f:'rgba(255,255,255,.1)'})+R(0,h*.8,w,h*.2,{f:'rgba(0,0,0,.25)'});
const concTop2=(w,h)=>R(0,0,w,h,{f:'#9a9ca2'})+`<rect width="${w}" height="${h}" filter="url(#fConc)"/>`+`<rect width="${w}" height="${h}" filter="url(#fConc2)" opacity=".5"/>`+R(0,0,w,h,{f:'url(#gSheen)',op:.2})+R(.4,.4,w-.8,h-.8,{f:'none',s:'rgba(255,255,255,.7)',w:.5});
const concSide2=(w,h)=>R(0,0,w,h,{f:'#b7b9be'})+`<rect width="${w}" height="${h}" filter="url(#fConc)" opacity=".85"/>`+R(0,0,w,h*.2,{f:'rgba(255,255,255,.22)'})+R(0,h*.82,w,h*.18,{f:'rgba(0,0,0,.2)'});
const concFront2=(w,h)=>concSide2(w,h)+T(w/2,h/2+1.7,'Computers   →   Laptops   →   Tablets   →   Smartphones',{sz:Math.min(5,h*.28),f:'#1f2733',ff:RAL,b:1});
const blueTop2=(w,h)=>{let s=R(0,0,w,h,{f:'#04123f'});
  s+=`<rect x="0" y="0" width="${w}" height="${h}" fill="url(#pBlue)" opacity=".8"/>`;
  for(let i=0;i<14;i++){const x=(i*37)%w,y=(i*53)%h;s+=P(`M${x} ${y} l${8+(i%4)*4} 0 l5 5 l${6+(i%3)*5} 0`,{s:'#2a9dff',w:.35,op:.8})+C(x,y,.8,{f:'#7fd6ff'})}
  s+=`<rect x="1.5" y="1.5" width="${w-3}" height="${h-3}" fill="none" stroke="#18a8ff" stroke-width="1.6" filter="url(#gl2)"/>`+R(1.6,1.6,w-3.2,h-3.2,{f:'none',s:'#a8e6ff',w:.5})+R(0,0,w,h,{f:'url(#gSheen)',op:.25});return s};
const blueSide2=(w,h)=>R(0,0,w,h,{f:'#0a2a86'})+R(0,0,w,1,{f:'#3fb4ff'})+`<rect y="0" width="${w}" height="1" fill="#3fb4ff" filter="url(#gl1)"/>`;
// ===== FASCIA =====
const fasciaFull2=(total,h)=>{let s=R(0,0,total,h,{f:'#0b0b0e'})+`<rect width="${total}" height="${h}" filter="url(#fLeather)" opacity=".5"/>`+R(0,0,total,h,{f:'url(#gSheen)',op:.12});
  const tr=(x0,y0,dir)=>{let d=`M${x0} ${y0}`;[[14,0],[8,-6],[16,0],[7,7],[12,0]].forEach(([dx,dy])=>{d+=` l${dir*dx} ${dy}`});return `<path d="${d}" fill="none" stroke="#dcdce6" stroke-width=".5"/>`};
  const tr2=(x0,y0,dir)=>{let d=`M${x0} ${y0}`;[[10,0],[6,6],[14,0],[7,-7],[9,0]].forEach(([dx,dy])=>{d+=` l${dir*dx} ${dy}`});return `<path d="${d}" fill="none" stroke="#dcdce6" stroke-width=".5"/>`};
  [[6,10,tr],[12,19,tr2],[6,28,tr],[18,37,tr2],[10,44,tr]].forEach(([x,y,fn])=>{s+=fn(x,y,1)+C(x,y,1,{f:'#0b0b0e',s:'#dcdce6',w:.45})});
  [[total-6,10,tr],[total-12,19,tr2],[total-6,28,tr],[total-18,37,tr2],[total-10,44,tr]].forEach(([x,y,fn])=>{s+=fn(x,y,-1)+C(x,y,1,{f:'#0b0b0e',s:'#dcdce6',w:.45})});
  s+=`<text x="${total/2}" y="${h*.56}" font-size="11" font-family="Raleway,sans-serif" font-weight="700" text-anchor="middle" fill="#9fb4ff" opacity=".35" filter="url(#gl1)" letter-spacing=".4">From Numbers to Neural Networks</text>`+T(total/2,h*.56,'From Numbers to Neural Networks',{sz:11,f:'#f4f4ff',ff:RAL,b:1,ls:.4});
  s+=L(total/2-70,h*.72,total/2+70,h*.72,{s:'#f4f4ff',w:.5});return s};
