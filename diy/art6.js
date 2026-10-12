// ===== ABACUS =====
const abacusFront2=(w,h)=>{
  let s=R(0,0,w,h,{f:'url(#gWoodV)',r:1.6,s:'#4a2c10',w:.35})+tex(0,0,w,h,1.6,'fWood',.8)+R(0,0,w,h,{f:'url(#gSheen)',r:1.6,op:.5});
  // frame bevel
  s+=R(1,1,w-2,h-2,{f:'none',s:'rgba(255,230,180,.55)',w:.3,r:1.2})+R(4.6,4.6,w-9.2,h-15,{f:'#24150b',r:.5,s:'#e6bf84',w:.35});
  s+=R(4.9,4.9,w-9.8,h-15.6,{f:'none',s:'#000',w:.5,r:.4,op:.7});
  const ix=5.6,iw=w-11.2,iy=5.6,ih=h-16.6,rows=8,rh=ih/rows;
  for(let r=0;r<rows;r++){
    const y=iy+rh*(r+.5);
    s+=R(ix-.8,y-.28,iw+1.6,.56,{f:'url(#gRod)'})+R(ix-.8,y-.28,iw+1.6,.18,{f:'rgba(255,255,255,.55)'});
    const nL=[5,3,4,5,2,4,3,5][r];const bw=iw/10.3;
    for(let b=0;b<9;b++){const left=b<nL;const xx=left?ix+.2+b*bw:ix+iw-.2-(9-b)*bw;const cx=xx+bw/2;
      s+=`<ellipse cx="${f(cx+.18)}" cy="${f(y+.2)}" rx="${f(bw*.5)}" ry="${f(rh*.4)}" fill="rgba(0,0,0,.35)"/>`;
      s+=E_(cx,y,bw*.5,rh*.4,{f:left?'url(#gBeadDR)':'url(#gBeadLR)',s:left?'#0c0503':'#6b4318',w:.1});
      s+=E_(cx-bw*.14,y-rh*.16,bw*.17,rh*.1,{f:'#fff',}).replace('fill="#fff"','fill="#fff" opacity=".55"');
    }
  }
  // base plate + label
  s+=R(w/2-9,h-9.6,18,5.4,{f:'#f0e3c4',s:'#6b4a1e',w:.3,r:.5})+tex(w/2-9,h-9.6,18,5.4,.5,'fPaper',.4)+T(w/2,h-6.4,'ABACUS',{sz:2.1,f:'#4a2c10',ff:'Raleway,serif',b:1,ls:.3})+T(w/2,h-5,'c. 2000 BC',{sz:1.1,f:'#4a2c10',ff:HAND,i:1});
  return s};
const abacusBack2=(w,h)=>R(0,0,w,h,{f:'url(#gWoodV)',r:1.6,s:'#4a2c10',w:.35})+tex(0,0,w,h,1.6,'fWood',.9)+R(4,4,w-8,h-8,{f:'none',s:'rgba(60,30,10,.6)',w:.5,r:1})+R(1,1,w-2,h-2,{f:'none',s:'rgba(255,230,180,.5)',w:.3,r:1.2});
// ===== ROBOT =====
const robotFront2=(w,h)=>{
  let s='';const cx=w/2;
  const shadow=(d)=>d;
  // legs
  s+=R(cx-6.6,h*.7,5.2,h*.2,{f:'url(#gShell)',s:'#7d889f',w:.25,r:2.2})+R(cx+1.4,h*.7,5.2,h*.2,{f:'url(#gShell)',s:'#7d889f',w:.25,r:2.2});
  s+=R(cx-6.8,h*.86,5.6,1.4,{f:'#2c3446',r:.6})+R(cx+1.2,h*.86,5.6,1.4,{f:'#2c3446',r:.6});
  s+=P(`M${cx-7.8} ${h*.93} Q${cx-7.8} ${h*.88} ${cx-4} ${h*.88} Q${cx-.4} ${h*.88} ${cx-.4} ${h*.93} L${cx-.4} ${h*.97} L${cx-7.8} ${h*.97} Z`,{f:'url(#gShellR)',s:'#7d889f',w:.3})+P(`M${cx+.4} ${h*.93} Q${cx+.4} ${h*.88} ${cx+4} ${h*.88} Q${cx+7.8} ${h*.88} ${cx+7.8} ${h*.93} L${cx+7.8} ${h*.97} L${cx+.4} ${h*.97} Z`,{f:'url(#gShellR)',s:'#7d889f',w:.3});
  // torso
  s+=P(`M${cx-9} ${h*.4} Q${cx-11.2} ${h*.58} ${cx-6.4} ${h*.74} L${cx+6.4} ${h*.74} Q${cx+11.2} ${h*.58} ${cx+9} ${h*.4} Z`,{f:'url(#gShellR)',s:'#7d889f',w:.35});
  s+=P(`M${cx-8.4} ${h*.44} Q${cx-10} ${h*.58} ${cx-6.2} ${h*.71}`,{s:'rgba(255,255,255,.9)',w:.7});
  s+=P(`M${cx+9} ${h*.5} Q${cx+10.4} ${h*.6} ${cx+6.4} ${h*.73}`,{s:'rgba(80,95,125,.35)',w:1.4});
  s+=R(cx-7,h*.68,14,.5,{f:'#8c98b0'})+R(cx-6,h*.715,12,1.2,{f:'#2c3446',r:.4});
  s+=C(cx,h*.54,3.7,{f:'#18233f',s:'#8c98b0',w:.35})+C(cx,h*.54,2.9,{f:'url(#gEye)'})+C(cx,h*.54,3.7,{f:'none',s:'#58e0ff',w:.2,op:.7})+C(cx-.8,h*.54-.8,.8,{f:'#fff',op:.8});
  s+=`<circle cx="${cx}" cy="${h*.54}" r="3.6" fill="#58e0ff" opacity=".35" filter="url(#gl2)"/>`;
  // arms
  const arm=(sg)=>{const sx=cx+sg*9.2,sy=h*.45;let a='';a+=C(sx,sy,2.4,{f:'url(#gShellR)',s:'#7d889f',w:.3});
    a+=P(`M${sx} ${sy+1} Q${sx+sg*5} ${sy+3} ${sx+sg*4.4} ${h*.6}`,{s:'#7d889f',w:3.6})+P(`M${sx} ${sy+1} Q${sx+sg*5} ${sy+3} ${sx+sg*4.4} ${h*.6}`,{s:'#e6ebf4',w:2.9})+P(`M${sx} ${sy+.4} Q${sx+sg*4.8} ${sy+2.4} ${sx+sg*4} ${h*.59}`,{s:'#fff',w:.6,op:.8});
    a+=C(sx+sg*4.4,h*.61,1.5,{f:'#2c3446'})+C(sx+sg*4.4,h*.64,2.1,{f:'url(#gShellR)',s:'#7d889f',w:.3});return a};
  s+=arm(-1)+arm(1);
  // neck
  s+=R(cx-2.6,h*.36,5.2,h*.06,{f:'#2c3446',r:.8});
  // head
  s+=R(cx-10.4,h*.07,20.8,h*.3,{f:'url(#gShellR)',s:'#7d889f',w:.4,r:8.8});
  s+=P(`M${cx-8.6} ${h*.12} Q${cx-9.4} ${h*.2} ${cx-8.4} ${h*.3}`,{s:'rgba(255,255,255,.95)',w:.8});
  s+=R(cx-8.4,h*.11,16.8,h*.22,{f:'url(#gVisor)',s:'#0a1226',w:.4,r:6.6});
  s+=P(`M${cx-7.4} ${h*.125} Q${cx} ${h*.105} ${cx+7.4} ${h*.125}`,{s:'rgba(255,255,255,.28)',w:.5});
  [-1,1].forEach(sg=>{const ex=cx+sg*3.5,ey=h*.225;s+=`<ellipse cx="${ex}" cy="${ey}" rx="2.2" ry="2.7" fill="#2fd0ff" opacity=".5" filter="url(#gl2)"/>`+E_(ex,ey,1.75,2.2,{f:'url(#gEye)'})+E_(ex-.5,ey-.7,.55,.75,{f:'#fff'})});
  s+=P(`M${cx-1.8} ${h*.285} q1.8 1.2 3.6 0`,{s:'#58e0ff',w:.5});
  s+=R(cx-12.6,h*.17,2.4,5.4,{f:'url(#gShellR)',s:'#7d889f',w:.3,r:1.1})+R(cx+10.2,h*.17,2.4,5.4,{f:'url(#gShellR)',s:'#7d889f',w:.3,r:1.1});
  s+=L(cx,h*.07,cx,h*.025,{s:'#7d889f',w:.5})+C(cx,h*.022,1.3,{f:'url(#gEye)'});
  return s};
const robotBack2=(w,h)=>{let s=robotFront2(w,h);return s.replace(/url\(#gEye\)/g,'#9aa6bd').replace(/url\(#gVisor\)/g,'#c3cbdb').replace(/#58e0ff/g,'#8c98b0').replace(/#2fd0ff/g,'#8c98b0')};
// ===== AI BRAIN =====
const brainPath=(w,h)=>`M${w*.27} ${h*.6} C${w*.1} ${h*.58} ${w*.08} ${h*.34} ${w*.25} ${h*.3} C${w*.24} ${h*.12} ${w*.46} ${h*.07} ${w*.5} ${h*.18} C${w*.56} ${h*.05} ${w*.8} ${h*.1} ${w*.77} ${h*.3} C${w*.93} ${h*.34} ${w*.92} ${h*.58} ${w*.75} ${h*.6} C${w*.77} ${h*.74} ${w*.6} ${h*.78} ${w*.52} ${h*.7} C${w*.42} ${h*.8} ${w*.27} ${h*.74} ${w*.27} ${h*.6} Z`;
const brainArt2=(w,h)=>{
  let s=R(0,0,w,h,{f:'#030816',r:6,s:'#1a8cff',w:.5});
  s+=`<rect x="0" y="0" width="${w}" height="${h}" rx="6" fill="none" stroke="#18a8ff" stroke-width="1.6" opacity=".6" filter="url(#gl2)"/>`;
  const bp=brainPath(w,h);
  s+=`<path d="${bp}" fill="rgba(24,120,255,.12)" stroke="#18a8ff" stroke-width="2.2" filter="url(#gl2)"/>`;
  const cid=uid();s+=`<defs><clipPath id="${cid}"><path d="${bp}"/></clipPath></defs><g clip-path="url(#${cid})">`;
  // gyri
  for(let i=0;i<9;i++){const y=h*(.14+i*.07);let d=`M${w*.05} ${y}`;for(let k=0;k<9;k++){d+=` q${w*.05} ${(k%2?-1:1)*h*.045} ${w*.1} 0`}s+=`<path d="${d}" fill="none" stroke="#3cc4ff" stroke-width=".5" opacity=".6"/>`}
  for(let i=0;i<7;i++){const x=w*(.18+i*.09);let d=`M${x} ${h*.1}`;for(let k=0;k<7;k++){d+=` q${(k%2?-1:1)*w*.035} ${h*.05} 0 ${h*.1}`}s+=`<path d="${d}" fill="none" stroke="#18a8ff" stroke-width=".4" opacity=".45"/>`}
  s+='</g>';
  s+=`<path d="${bp}" fill="none" stroke="#8fe1ff" stroke-width=".7"/>`;
  s+=`<path d="M${w*.5} ${h*.18} C${w*.46} ${h*.34} ${w*.54} ${h*.5} ${w*.5} ${h*.7}" fill="none" stroke="#8fe1ff" stroke-width=".5" opacity=".8"/>`;
  const nodes=[[.22,.45],[.34,.32],[.4,.5],[.34,.62],[.62,.4],[.66,.56],[.72,.36],[.6,.24],[.4,.22],[.8,.5],[.52,.62],[.3,.2],[.7,.22]];
  nodes.forEach((a,i)=>{const b=nodes[(i*3+2)%nodes.length];s+=L(a[0]*w,a[1]*h,b[0]*w,b[1]*h,{s:'#6fd4ff',w:.35,op:.75})});
  nodes.forEach(a=>{s+=`<circle cx="${f(a[0]*w)}" cy="${f(a[1]*h)}" r="1.4" fill="#18a8ff" opacity=".6" filter="url(#gl1)"/>`+C(a[0]*w,a[1]*h,.55,{f:'#e6f9ff'})});
  s+=`<text x="${w*.5}" y="${h*.5}" font-size="${w*.2}" font-family="Raleway,sans-serif" font-weight="700" text-anchor="middle" fill="#18a8ff" opacity=".7" filter="url(#gl2)">AI</text>`;
  s+=`<text x="${w*.5}" y="${h*.5}" font-size="${w*.2}" font-family="Raleway,sans-serif" font-weight="700" text-anchor="middle" fill="#0a2a6a" stroke="#c8f1ff" stroke-width=".45">AI</text>`;
  // circuit stem
  s+=P(`M${w*.5} ${h*.74} L${w*.5} ${h*.9} M${w*.42} ${h*.76} L${w*.42} ${h*.84} L${w*.34} ${h*.9} M${w*.58} ${h*.76} L${w*.58} ${h*.84} L${w*.66} ${h*.9}`,{s:'#58c8ff',w:.5});
  [[.5,.92],[.34,.91],[.66,.91]].forEach(([x,y])=>{s+=`<circle cx="${x*w}" cy="${y*h}" r="1.6" fill="#18a8ff" filter="url(#gl1)"/>`+C(x*w,y*h,.7,{f:'#e6f9ff'})});
  return s};
// ===== AI SCREEN =====
const aiScreenArt2=(w,h)=>{
  let s=R(0,0,w,h,{f:'#04112f',r:2.2,s:'#2aa6ff',w:.6});
  s+=`<rect x=".3" y=".3" width="${w-.6}" height="${h-.6}" rx="2" fill="none" stroke="url(#gHoloFrame)" stroke-width="1.1" filter="url(#gl1)"/>`+R(1.4,1.4,w-2.8,h-2.8,{f:'none',s:'url(#gHoloFrame)',w:.5,r:1.4});
  const x=3.4,y=3.4,iw=w-6.8,ih=h-6.8;
  let c=R(x,y,iw,ih,{f:'#0c1b3d'});
  c+=R(x,y,iw,4,{f:'rgba(80,140,255,.25)'});[0,1,2].forEach(i=>c+=C(x+2+i*1.8,y+2,.55,{f:['#ff5f57','#febc2e','#28c840'][i]}));c+=T(x+iw/2,y+2.5,'AI Studio',{sz:1.2,f:'#bcd6ff',ff:UI});
  // image
  const px=x+3,py=y+6.2,pw=iw*.5,ph=ih*.46;
  c+=R(px,py,pw,ph,{f:'url(#gSky)',r:.8,s:'#6fb2ff',w:.25})+C(px+pw*.74,py+ph*.28,2.4,{f:'#fff6c0'})+`<circle cx="${px+pw*.74}" cy="${py+ph*.28}" r="3.4" fill="#fff1a8" opacity=".55" filter="url(#gl2)"/>`;
  c+=P(`M${px} ${py+ph} L${px} ${py+ph*.7} L${px+pw*.28} ${py+ph*.42} L${px+pw*.5} ${py+ph*.68} L${px+pw*.7} ${py+ph*.5} L${px+pw} ${py+ph*.74} L${px+pw} ${py+ph} Z`,{f:'#27508f'})+P(`M${px} ${py+ph} L${px} ${py+ph*.84} L${px+pw*.36} ${py+ph*.6} L${px+pw*.62} ${py+ph*.86} L${px+pw} ${py+ph*.78} L${px+pw} ${py+ph} Z`,{f:'#183868'});
  c+=R(px,py,pw,ph,{f:'none',s:'#9bc8ff',w:.25,r:.8});
  // right panel
  for(let i=0;i<4;i++)c+=R(px+pw+3,py+i*3.6,iw*.34-(i%2)*4,1.1,{f:'#5aa7e6',r:.5,op:.8});
  c+=R(px+pw+3,py+ph-4.4,iw*.3,4.4,{f:'url(#gHoloFrame)',r:1.2})+T(px+pw+3+iw*.15,py+ph-1.4,'Generate',{sz:1.5,f:'#fff',b:1,ff:UI});
  c+=R(px,py+ph+3,iw-6,1.1,{f:'#5aa7e6',r:.5,op:.85})+R(px,py+ph+6,(iw-6)*.7,1.1,{f:'#5aa7e6',r:.5,op:.7})+R(px,py+ph+9,(iw-6)*.85,1.1,{f:'#5aa7e6',r:.5,op:.7});
  s+=inClip(x,y,iw,ih,1.2,c);s+=sheen(x,y,iw,ih,1.2,.9);return s};
const aiScreenBack2=(w,h)=>R(0,0,w,h,{f:'#04112f',r:2.2,s:'#2aa6ff',w:.6})+R(1.4,1.4,w-2.8,h-2.8,{f:'none',s:'url(#gHoloFrame)',w:.5,r:1.4})+`<text x="${w/2}" y="${h/2+3}" font-size="11" font-family="Raleway,sans-serif" font-weight="700" text-anchor="middle" fill="#2aa6ff" opacity=".8" filter="url(#gl1)">AI</text>`+T(w/2,h/2+3,'AI',{sz:11,f:'#bfe8ff',b:1,ff:RAL});
const aiBaseTop=(w,h)=>R(0,0,w,h,{f:'#06143a'})+`<rect x="1" y="1" width="${w-2}" height="${h-2}" fill="none" stroke="#2aa6ff" stroke-width="1" filter="url(#gl1)"/>`+R(1.6,1.6,w-3.2,h-3.2,{f:'none',s:'#7fd6ff',w:.3})+P(`M4 ${h/2} L${w*.35} ${h/2} L${w*.4} ${h*.3} L${w*.6} ${h*.7} L${w*.65} ${h/2} L${w-4} ${h/2}`,{s:'#58c8ff',w:.45});
const aiBaseSide=(w,h)=>R(0,0,w,h,{f:'#0b2470'})+R(0,0,w,.8,{f:'#2aa6ff'});
// ===== PLANT =====
const veinLeaf=(x,y,len,ang,g,wd=.3)=>`<g transform="translate(${f(x)},${f(y)}) rotate(${ang})">${P(`M0 0 C${len*.25} ${-len*wd} ${len*.75} ${-len*wd*.9} ${len} 0 C${len*.75} ${len*wd*.9} ${len*.25} ${len*wd} 0 0 Z`,{f:`url(#${g})`,s:'#0f4a1c',w:.18})}${P(`M0 0 L${len*.94} 0`,{s:'rgba(230,255,200,.75)',w:.22})}${[.2,.35,.5,.65,.8].map(t=>P(`M${len*t} 0 l${len*.1} ${-len*.09} M${len*t} 0 l${len*.1} ${len*.09}`,{s:'rgba(230,255,200,.35)',w:.12})).join('')}${P(`M${len*.1} ${-len*.1} C${len*.4} ${-len*.28} ${len*.7} ${-len*.2} ${len*.9} ${-len*.02}`,{s:'rgba(255,255,255,.28)',w:.3})}</g>`;
const plantArt2=(w,h)=>{let s='';const cx=w/2,pot=h*.27,by=h-pot-.6;
  const ls=[[-100,.5,'gLeafB'],[100,.5,'gLeafB'],[-72,.7,'gLeafA'],[72,.7,'gLeafA'],[-45,.9,'gLeafC'],[45,.9,'gLeafC'],[-20,1,'gLeafA'],[20,1,'gLeafB'],[0,.95,'gLeafC']];
  ls.forEach(([a,k,g])=>{s+=veinLeaf(cx,by,(h-pot)*.88*k,a-90,g,.26+k*.04)});
  s+=P(`M${cx-w*.36} ${h-pot} L${cx+w*.36} ${h-pot} L${cx+w*.27} ${h} L${cx-w*.27} ${h} Z`,{f:'url(#gPotC)',s:'#505258',w:.25})+inClip(cx-w*.36,h-pot,w*.72,pot,0,R(cx-w*.36,h-pot,w*.72,pot,{f:'none'})+`<rect x="${cx-w*.36}" y="${h-pot}" width="${w*.72}" height="${pot}" filter="url(#fConc)" opacity=".18"/>`);
  s+=R(cx-w*.39,h-pot-1.2,w*.78,1.9,{f:'url(#gPotC)',s:'#505258',w:.25,r:.7})+R(cx-w*.36,h-pot-1.1,w*.72,.5,{f:'rgba(255,255,255,.7)',r:.25});
  s+=E_(cx,h-pot-.6,w*.33,.7,{f:'#3d2412'});return s};
