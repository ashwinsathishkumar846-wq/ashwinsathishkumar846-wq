// ---------- ROBOT (30 x 60) ----------
const robotFront=(w,h)=>{let s='';const cx=w/2;
  // legs
  s+=R(cx-7,h*.74,5.4,h*.2,{f:'url(#gRobot)',s:'#8e98ab',w:.25,r:2})+R(cx+1.6,h*.74,5.4,h*.2,{f:'url(#gRobot)',s:'#8e98ab',w:.25,r:2});
  s+=R(cx-8,h*.92,7.2,h*.07,{f:'#8f9bb3',s:'#6b778d',w:.25,r:2})+R(cx+.8,h*.92,7.2,h*.07,{f:'#8f9bb3',s:'#6b778d',w:.25,r:2});
  // body
  s+=P(`M${cx-9.5} ${h*.42} Q${cx-11} ${h*.62} ${cx-7} ${h*.77} L${cx+7} ${h*.77} Q${cx+11} ${h*.62} ${cx+9.5} ${h*.42} Z`,{f:'url(#gRobot)',s:'#8e98ab',w:.3});
  s+=C(cx,h*.56,3.3,{f:'#0f2d6b',s:'#8e98ab',w:.3})+C(cx,h*.56,2,{f:'#3fd0ff'})+C(cx,h*.56,.9,{f:'#e6fbff'});
  s+=R(cx-6,h*.67,12,.5,{f:'#b4bfd2'});
  // arms
  s+=P(`M${cx-9.5} ${h*.45} Q${cx-15} ${h*.5} ${cx-13.5} ${h*.65}`,{s:'#8e98ab',w:4.4})+P(`M${cx-9.5} ${h*.45} Q${cx-15} ${h*.5} ${cx-13.5} ${h*.65}`,{s:'url(#gRobot)',w:3.6});
  s+=P(`M${cx+9.5} ${h*.45} Q${cx+15} ${h*.5} ${cx+13.5} ${h*.65}`,{s:'#8e98ab',w:4.4})+P(`M${cx+9.5} ${h*.45} Q${cx+15} ${h*.5} ${cx+13.5} ${h*.65}`,{s:'url(#gRobot)',w:3.6});
  s+=C(cx-13.5,h*.67,2.1,{f:'#dfe5f1',s:'#8e98ab',w:.3})+C(cx+13.5,h*.67,2.1,{f:'#dfe5f1',s:'#8e98ab',w:.3});
  // neck + head
  s+=R(cx-2.5,h*.37,5,h*.06,{f:'#9aa5ba'});
  s+=R(cx-10,h*.08,20,h*.3,{f:'url(#gRobot)',s:'#8e98ab',w:.35,r:8});
  s+=R(cx-8,h*.12,16,h*.21,{f:'url(#gNavy)',s:'#18356f',w:.3,r:6});
  s+=E_(cx-3.4,h*.225,1.9,2.3,{f:'#4fdcff'})+E_(cx+3.4,h*.225,1.9,2.3,{f:'#4fdcff'})+E_(cx-3.4,h*.215,.7,.9,{f:'#fff'})+E_(cx+3.4,h*.215,.7,.9,{f:'#fff'});
  s+=P(`M${cx-2} ${h*.285} q2 1.2 4 0`,{s:'#4fdcff',w:.5});
  s+=R(cx-12,h*.17,2.2,5,{f:'#b8c3d7',s:'#8e98ab',w:.25,r:1})+R(cx+9.8,h*.17,2.2,5,{f:'#b8c3d7',s:'#8e98ab',w:.25,r:1});
  s+=L(cx,h*.08,cx,h*.03,{s:'#8e98ab',w:.5})+C(cx,h*.028,1.2,{f:'#4fdcff'});
  return s};
const robotBack=(w,h)=>robotFront(w,h).replace(/#4fdcff/g,'#8e98ab').replace(/url\(#gNavy\)/g,'#a9b4c8');
// ---------- AI BRAIN ----------
const brainArt=(w,h)=>{let s=R(0,0,w,h,{f:'url(#gNavy)',r:7,s:'#18a8ff',w:.5});
  const bp=`M${w*.22} ${h*.6} C${w*.06} ${h*.55} ${w*.08} ${h*.3} ${w*.24} ${h*.28} C${w*.26} ${h*.1} ${w*.48} ${h*.06} ${w*.52} ${h*.17} C${w*.6} ${h*.04} ${w*.82} ${h*.1} ${w*.8} ${h*.3} C${w*.96} ${h*.34} ${w*.95} ${h*.58} ${w*.78} ${h*.6} C${w*.8} ${h*.76} ${w*.6} ${h*.78} ${w*.52} ${h*.7} C${w*.42} ${h*.8} ${w*.24} ${h*.76} ${w*.22} ${h*.6} Z`;
  s+=P(bp,{s:'#18a8ff',w:2.2,op:.45})+P(bp,{f:'rgba(20,120,255,.18)',s:'#6fd4ff',w:.7});
  const nodes=[[.24,.5],[.34,.35],[.44,.5],[.38,.64],[.52,.4],[.6,.55],[.68,.36],[.74,.5],[.5,.25],[.3,.22],[.62,.22],[.52,.62]];
  nodes.forEach((a,i)=>{const b=nodes[(i*5+3)%nodes.length],c=nodes[(i*7+1)%nodes.length];s+=L(a[0]*w,a[1]*h,b[0]*w,b[1]*h,{s:'#58c8ff',w:.3,op:.7})+L(a[0]*w,a[1]*h,c[0]*w,c[1]*h,{s:'#58c8ff',w:.2,op:.5})});
  nodes.forEach(a=>{s+=C(a[0]*w,a[1]*h,.8,{f:'#d8f4ff'})+C(a[0]*w,a[1]*h,1.6,{f:'#18a8ff',op:.25})});
  s+=T(w*.52,h*.52,'AI',{sz:w*.2,f:'#ffffff',b:1,ff:RAL});s+=T(w*.52,h*.52,'AI',{sz:w*.2,f:'none',b:1,ff:RAL}).replace('fill="none"','fill="none" stroke="#18a8ff" stroke-width=".5"');
  s+=P(`M${w*.5} ${h*.78} L${w*.5} ${h*.9} M${w*.4} ${h*.78} L${w*.38} ${h*.9} M${w*.6} ${h*.78} L${w*.62} ${h*.9}`,{s:'#58c8ff',w:.6});
  s+=C(w*.5,h*.92,1.3,{f:'#18a8ff'})+C(w*.38,h*.92,1,{f:'#18a8ff'})+C(w*.62,h*.92,1,{f:'#18a8ff'});
  return s};
// ---------- AI SCREEN ----------
const aiScreenArt=(w,h)=>{let s=R(0,0,w,h,{f:'#0a1e7a',r:2.5,s:'#18a8ff',w:.7});s+=R(2,2,w-4,h-4,{f:'url(#gNeon)',r:1.6,op:.35});
  s+=R(3.5,3.5,w-7,h-7,{f:'#d9f2ff',r:1.2,s:'#7fd6ff',w:.4});s+=R(3.5,3.5,w-7,6.5,{f:'url(#gHolo)',r:1.2});
  [0,1,2].forEach(i=>s+=C(6+i*2.4,6.7,.7,{f:['#ff5f57','#febc2e','#28c840'][i]}));
  s+=R(6,12.5,w*.52,w*.34,{f:'#9fdcff',r:1,s:'#2a7fff',w:.4});s+=P(`M${6+0.5} ${12.5+w*.34-.8} l${w*.12} -${w*.15} l${w*.1} ${w*.08} l${w*.08} -${w*.1} l${w*.18} ${w*.17} Z`,{f:'#2a7fff'})+C(6+w*.38,12.5+w*.1,2.1,{f:'#fff59a'});
  for(let i=0;i<5;i++)s+=R(w*.62,12.5+i*5.2,w*.28-(i%2)*4,1.1,{f:'#5aa7e6',r:.5});
  s+=R(6,12.5+w*.34+4,w-12,1.1,{f:'#5aa7e6',r:.5})+R(6,12.5+w*.34+7.5,(w-12)*.7,1.1,{f:'#5aa7e6',r:.5})+R(6,12.5+w*.34+11,(w-12)*.85,1.1,{f:'#5aa7e6',r:.5});
  return s};
const aiScreenBack=(w,h)=>R(0,0,w,h,{f:'#0a1e7a',r:2.5,s:'#18a8ff',w:.7})+R(3,3,w-6,h-6,{f:'none',s:'#3d7bff',w:.5,r:1.5})+T(w/2,h/2+2,'AI',{sz:10,f:'#58c8ff',b:1,ff:RAL});
// ---------- SIGNBOARDS ----------
const signboard=(txt)=>(w,h)=>R(0,0,w,h,{f:'#e9f2ff',r:1.2,s:'#2f6bff',w:.7})+R(.9,.9,w-1.8,h-1.8,{f:'none',s:'#7fb0ff',w:.3,r:.8})+R(0,0,w,h*.45,{f:'rgba(255,255,255,.55)',r:1.2})+T(w/2,h/2+1.4,txt,{sz:4.2,f:'#14307e',b:1,ff:RAL});
const signboardBack=(w,h)=>R(0,0,w,h,{f:'#2f6bff',r:1.2,s:'#14307e',w:.5});
const imagineSign=(w,h)=>R(0,0,w,h,{f:'url(#gNavy)',r:1.5,s:'#18a8ff',w:.8})+R(.8,h-1.8,w-1.6,1,{f:'#18a8ff'})+T(w/2,h/2+1.2,'Imagine  •  Create  •  Innovate',{sz:5,f:'#eaf6ff',b:1,ff:RAL,ls:.25});
// ---------- HEADINGS ----------
const cloudArt=(w,h)=>{
  const d=`M${w*.13} ${h*.7} C${w*.0} ${h*.7} ${w*.0} ${h*.38} ${w*.12} ${h*.36} C${w*.08} ${h*.12} ${w*.3} ${h*.04} ${w*.38} ${h*.16} C${w*.46} ${h*-.02} ${w*.7} ${h*.0} ${w*.74} ${h*.17} C${w*.86} ${h*.06} ${w*.97} ${h*.22} ${w*.9} ${h*.38} C${w*1.02} ${h*.46} ${w*.99} ${h*.7} ${w*.86} ${h*.7} C${w*.84} ${h*.9} ${w*.62} ${h*.97} ${w*.52} ${h*.84} C${w*.4} ${h*.98} ${w*.2} ${h*.92} ${w*.13} ${h*.7} Z`;
  let s=P(d,{f:'url(#gPill)',s:'#4a2c8a',w:.9});s+=P(d,{s:'#4a2c8a',w:.3}).replace('stroke-width="0.3"','stroke-width=".3" transform="translate(0,0)"');
  s+=T(w*.5,h*.4,'Evolution of',{sz:h*.2,f:'#1d1238',b:1,ff:RAL})+T(w*.5,h*.66,'Computer Science',{sz:h*.2,f:'#1d1238',b:1,ff:RAL});
  [[.07,.5],[.93,.55]].forEach(([x,y])=>{s+=L(w*x,h*y-3,w*x,h*y+3,{s:'#4a2c8a',w:.4})});
  return s};
const pill=(l1,l2)=>(w,h)=>R(0,0,w,h,{f:'url(#gPill)',r:h*.42,s:'#4a2c8a',w:.8})+R(1,1,w-2,h-2,{f:'none',s:'#b9a0e6',w:.25,r:h*.4})+T(w/2,l2?h*.45:h*.62,l1,{sz:h*.34,f:'#1d1238',b:1,ff:RAL})+(l2?T(w/2,h*.78,l2,{sz:h*.22,f:'#1d1238',ff:RAL}):'');
const pillBack=(w,h)=>R(0,0,w,h,{f:'#4a2c8a',r:h*.42});
// ---------- PLATFORMS ----------
const soilTop=(w,h)=>R(0,0,w,h,{f:'url(#pSoil)',s:'#000',w:.2})+[...Array(26)].map((_,i)=>E_((i*37)%w,(i*53)%h,1.8+(i%3),1.1,{f:'#5a2810',rot:i*20})).join('');
const soilSide=(w,h)=>R(0,0,w,h,{f:'#6b3418'})+R(0,0,w,1.6,{f:'#8a4a26'})+[...Array(Math.floor(w/4))].map((_,i)=>C(i*4+1.5,h*.6,.45,{f:'#4a210d'})).join('');
const concTop=(w,h)=>R(0,0,w,h,{f:'url(#pConc)'})+[...Array(18)].map((_,i)=>E_((i*41)%w,(i*29)%h,2.2,1.2,{f:'rgba(255,255,255,.35)',rot:i*30})).join('')+R(0,0,w,h,{f:'none',s:'#fff',w:.6});
const concSide=(w,h)=>R(0,0,w,h,{f:'#e4e5e8',s:'#c8cace',w:.2});
const concFront=(w,h)=>R(0,0,w,h,{f:'#f2f2f5',s:'#c8cace',w:.2})+T(w/2,h/2+1.5,'Computers   →   Laptops   →   Tablets   →   Smartphones',{sz:Math.min(4.6,h*.3),f:'#27303d',ff:RAL,b:1});
const blueTop=(w,h)=>R(0,0,w,h,{f:'url(#pBlue)'})+R(2,2,w-4,h-4,{f:'none',s:'#4c9bff',w:.5})+R(1,1,w-2,h-2,{f:'none',s:'#18a8ff',w:1,op:.5});
const blueSide=(w,h)=>R(0,0,w,h,{f:'#14308f'})+R(0,0,w,1,{f:'#18a8ff'});
// ---------- FASCIA ----------
const fasciaArt=(w,h,off,total)=>{
  let s=R(0,0,w,h,{f:'url(#gBlack)'});
  const trace=(x0,y0,dir)=>{let d=`M${x0} ${y0}`;[[12,0],[8,-6],[14,0],[6,6],[10,0]].forEach(([dx,dy])=>{d+=` l${dir*dx} ${dy}`});return P(d,{s:'#e8e8ee',w:.5,op:.9})};
  [[8,14],[14,23],[8,32],[20,40]].forEach(([x,y],i)=>{s+=trace(x,y,1)+C(x,y,1,{f:'none',s:'#e8e8ee',w:.5})});
  [[total-8,14],[total-14,23],[total-8,32],[total-20,40]].forEach(([x,y])=>{s+=trace(x,y,-1)+C(x,y,1,{f:'none',s:'#e8e8ee',w:.5})});
  return `<g transform="translate(${-off},0)">${s}</g>`;
};
const fasciaFull=(total,h)=>{let s='';s+=R(0,0,total,h,{f:'url(#gBlack)'});
  const tr=(x0,y0,dir)=>{let d=`M${x0} ${y0}`;[[14,0],[8,-6],[16,0],[7,7],[12,0]].forEach(([dx,dy])=>{d+=` l${dir*dx} ${dy}`});return P(d,{s:'#dcdce6',w:.45,op:.9})};
  [[6,12],[12,21],[6,30],[20,38]].forEach(([x,y])=>{s+=tr(x,y,1)+C(x,y,1,{f:'none',s:'#dcdce6',w:.45})});
  [[total-6,12],[total-12,21],[total-6,30],[total-20,38]].forEach(([x,y])=>{s+=tr(x,y,-1)+C(x,y,1,{f:'none',s:'#dcdce6',w:.45})});
  s+=T(total/2,h*.55,'From Numbers to Neural Networks',{sz:11,f:'#f4f4ff',ff:RAL,b:1,ls:.4});
  s+=L(total/2-70,h*.72,total/2+70,h*.72,{s:'#f4f4ff',w:.5});
  return s};
// ---------- PLANTS / STARS / ROCKS ----------
const leaf=(x,y,len,ang,col)=>`<g transform="translate(${x},${y}) rotate(${ang})">${P(`M0 0 C${len*.3} ${-len*.28} ${len*.8} ${-len*.2} ${len} 0 C${len*.8} ${len*.2} ${len*.3} ${len*.28} 0 0 Z`,{f:col,s:'#124d1e',w:.2})}${L(0,0,len*.9,0,{s:'#c9f0a4',w:.2,op:.7})}</g>`;
const plantArt=(w,h)=>{let s='';const cx=w/2,pot=h*.28;
  const ls=[[-80,.55],[-55,.8],[-30,.95],[0,1],[30,.95],[55,.8],[80,.55],[-110,.4],[110,.4]];
  ls.forEach(([a,k],i)=>{s+=leaf(cx,h-pot-1,(h-pot)*.8*k,a-90,i%2?'url(#gLeaf2)':'url(#gLeaf)')});
  s+=P(`M${cx-w*.34} ${h-pot} L${cx+w*.34} ${h-pot} L${cx+w*.26} ${h} L${cx-w*.26} ${h} Z`,{f:'url(#gPot)',s:'#5d5f64',w:.3})+R(cx-w*.37,h-pot-1.4,w*.74,1.6,{f:'#d9dbe0',s:'#5d5f64',w:.3,r:.6});
  s+=E_(cx,h-pot-.5,w*.3,.7,{f:'#4a2a14'});return s};
const bushStrip=(w,h)=>{let s='';for(let i=0;i<Math.floor(w/3.2);i++){const x=i*3.2+1.6;s+=leaf(x,h,h*(.55+((i*7)%5)/10),-90+((i*37)%70)-35,i%2?'url(#gLeaf2)':'url(#gLeaf)')}s+=R(0,h-1.2,w,1.2,{f:'#2a5a22'});return s};
const starArt=(w,h)=>P(`M${w/2} 0 Q${w/2+.7} ${h/2-.7} ${w} ${h/2} Q${w/2+.7} ${h/2+.7} ${w/2} ${h} Q${w/2-.7} ${h/2+.7} 0 ${h/2} Q${w/2-.7} ${h/2-.7} ${w/2} 0 Z`,{f:'#f4c04a',s:'#a87b10',w:.25});
const rockArt=(w,h,seed)=>{const pts=[];const n=9;for(let i=0;i<n;i++){const a=i/n*Math.PI*2,r=.82+((i*seed*13)%7)/38;pts.push([w/2+Math.cos(a)*w/2*r,h/2+Math.sin(a)*h/2*r])}
  return P('M'+pts.map(p=>f(p[0])+' '+f(p[1])).join(' L')+' Z',{f:'url(#gStone)',s:'#444',w:.25})+P(`M${w*.25} ${h*.35} L${w*.5} ${h*.25} L${w*.62} ${h*.45}`,{s:'rgba(255,255,255,.5)',w:.3})};
