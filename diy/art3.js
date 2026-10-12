// ======== REALISM LAYER ========
let _u=0;const uid=()=>'u'+(++_u);
const DEFS3=`<svg width="0" height="0" style="position:absolute"><defs>
<filter id="fBrush" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.015 1.6" numOctaves="2" seed="4"/><feColorMatrix type="matrix" values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  1.6 0 0 0 -.35"/></filter>
<filter id="fSoil" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.55" numOctaves="4" seed="2"/><feColorMatrix type="matrix" values=".95 0 0 0 .13  .45 0 0 0 .06  .2 0 0 0 .02  0 0 0 0 1"/></filter>
<filter id="fSoil2" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.08" numOctaves="3" seed="9"/><feColorMatrix type="matrix" values="0 0 0 0 .1  0 0 0 0 .04  0 0 0 0 0  1.4 0 0 0 -.45"/></filter>
<filter id="fConc" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" seed="5"/><feColorMatrix type="matrix" values=".55 0 0 0 .38  .55 0 0 0 .38  .56 0 0 0 .4  0 0 0 0 1"/></filter>
<filter id="fConc2" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="3" seed="3"/><feColorMatrix type="matrix" values="0 0 0 0 .2  0 0 0 0 .2  0 0 0 0 .22  1.2 0 0 0 -.45"/></filter>
<filter id="fLeather" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="3" seed="7"/><feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1.5 0 0 0 -.6"/></filter>
<filter id="fWood" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.03 0.9" numOctaves="3" seed="11"/><feColorMatrix type="matrix" values="0 0 0 0 .25  0 0 0 0 .12  0 0 0 0 .03  1.7 0 0 0 -.55"/></filter>
<filter id="fPaper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="3" seed="1"/><feColorMatrix type="matrix" values="0 0 0 0 .3  0 0 0 0 .22  0 0 0 0 .1  1 0 0 0 -.35"/></filter>
<filter id="gl1" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation=".35"/></filter>
<filter id="gl2" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation=".9"/></filter>
<filter id="gl3" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="2.6"/></filter>
<filter id="blurB" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="blurM" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.4"/></filter>
<linearGradient id="gTi" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5b5e63"/><stop offset=".08" stop-color="#d6d8dc"/><stop offset=".2" stop-color="#8b8e94"/><stop offset=".5" stop-color="#c9ccd1"/><stop offset=".85" stop-color="#7d8086"/><stop offset=".95" stop-color="#e6e8ec"/><stop offset="1" stop-color="#5b5e63"/></linearGradient>
<linearGradient id="gAl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9ebee"/><stop offset=".35" stop-color="#cfd2d7"/><stop offset=".7" stop-color="#bcc0c6"/><stop offset="1" stop-color="#d9dce0"/></linearGradient>
<linearGradient id="gAlV" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9ea2a9"/><stop offset=".12" stop-color="#eceef1"/><stop offset=".5" stop-color="#c6c9ce"/><stop offset=".88" stop-color="#eceef1"/><stop offset="1" stop-color="#9ea2a9"/></linearGradient>
<linearGradient id="gGraph" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a3d44"/><stop offset=".5" stop-color="#25272c"/><stop offset="1" stop-color="#16171a"/></linearGradient>
<linearGradient id="gSheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".42" stop-color="#fff" stop-opacity=".05"/><stop offset=".43" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="gLens" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6c7078"/><stop offset=".5" stop-color="#1b1c20"/><stop offset="1" stop-color="#8a8e96"/></linearGradient>
<radialGradient id="gLensIn" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#6a7aa8"/><stop offset=".25" stop-color="#1c2340"/><stop offset=".6" stop-color="#0a0b12"/><stop offset="1" stop-color="#000"/></radialGradient>
<linearGradient id="gGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff0b0"/><stop offset=".35" stop-color="#e0b24a"/><stop offset=".55" stop-color="#a97918"/><stop offset=".8" stop-color="#e8c466"/><stop offset="1" stop-color="#8a5f10"/></linearGradient>
<linearGradient id="gSilverFoil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".4" stop-color="#b8bcc4"/><stop offset=".6" stop-color="#8f949c"/><stop offset="1" stop-color="#e6e8ec"/></linearGradient>
<radialGradient id="gBeadDR" cx=".32" cy=".28" r=".85"><stop offset="0" stop-color="#9a6b52"/><stop offset=".25" stop-color="#5a2e20"/><stop offset=".7" stop-color="#2b120b"/><stop offset="1" stop-color="#120604"/></radialGradient>
<radialGradient id="gBeadLR" cx=".32" cy=".28" r=".85"><stop offset="0" stop-color="#fff0d0"/><stop offset=".3" stop-color="#e3b87c"/><stop offset=".75" stop-color="#b4814a"/><stop offset="1" stop-color="#7a5128"/></radialGradient>
<linearGradient id="gRod" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4e2a8"/><stop offset=".5" stop-color="#b58d3a"/><stop offset="1" stop-color="#6a4c14"/></linearGradient>
<linearGradient id="gShell" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#e3e8f1"/><stop offset="1" stop-color="#aab4c8"/></linearGradient>
<radialGradient id="gShellR" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#e1e6f0"/><stop offset="1" stop-color="#9aa6bd"/></radialGradient>
<linearGradient id="gVisor" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1b2b52"/><stop offset=".5" stop-color="#0a1226"/><stop offset="1" stop-color="#03060f"/></linearGradient>
<radialGradient id="gEye" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#e8fdff"/><stop offset=".4" stop-color="#58e0ff"/><stop offset="1" stop-color="#0a8adb"/></radialGradient>
<linearGradient id="gHoloFrame" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7fe3ff"/><stop offset=".5" stop-color="#1a7bff"/><stop offset="1" stop-color="#6f5bff"/></linearGradient>
<linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b7bd8"/><stop offset=".6" stop-color="#9ad6ff"/><stop offset="1" stop-color="#ffe7b8"/></linearGradient>
<linearGradient id="gLeafA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a6e068"/><stop offset=".5" stop-color="#4fae3b"/><stop offset="1" stop-color="#1f6f2b"/></linearGradient>
<linearGradient id="gLeafB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6fcf5a"/><stop offset=".5" stop-color="#2f9a3c"/><stop offset="1" stop-color="#145a28"/></linearGradient>
<linearGradient id="gLeafC" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c3ec7a"/><stop offset=".5" stop-color="#78c04a"/><stop offset="1" stop-color="#2c8a30"/></linearGradient>
<linearGradient id="gPotC" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6d6f75"/><stop offset=".25" stop-color="#d5d7db"/><stop offset=".55" stop-color="#a9acb2"/><stop offset="1" stop-color="#5e6066"/></linearGradient>
<radialGradient id="gBloom1" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#8fd8ff"/><stop offset="1" stop-color="#8fd8ff" stop-opacity="0"/></radialGradient>
<radialGradient id="gBloom2" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ff6aa8"/><stop offset="1" stop-color="#ff6aa8" stop-opacity="0"/></radialGradient>
<radialGradient id="gBloom3" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#7a5cff"/><stop offset="1" stop-color="#7a5cff" stop-opacity="0"/></radialGradient>
<radialGradient id="gBloom4" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffb347"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
</defs></svg>`;
// --- helpers ---
const clipR=(x,y,w,h,r)=>{const id=uid();return {id,def:`<clipPath id="${id}"><rect x="${f(x)}" y="${f(y)}" width="${f(w)}" height="${f(h)}" rx="${r}"/></clipPath>`}};
const inClip=(x,y,w,h,r,content)=>{const c=clipR(x,y,w,h,r);return `<defs>${c.def}</defs><g clip-path="url(#${c.id})">${content}</g>`};
const brushed=(x,y,w,h,r,op=.35)=>inClip(x,y,w,h,r,`<rect x="${f(x)}" y="${f(y)}" width="${f(w)}" height="${f(h)}" filter="url(#fBrush)" opacity="${op}"/>`);
const sheen=(x,y,w,h,r,op=1)=>inClip(x,y,w,h,r,`<rect x="${f(x)}" y="${f(y)}" width="${f(w)}" height="${f(h)}" fill="url(#gSheen)" opacity="${op}"/>`);
const tex=(x,y,w,h,r,filter,op=1)=>inClip(x,y,w,h,r,`<rect x="${f(x)}" y="${f(y)}" width="${f(w)}" height="${f(h)}" filter="url(#${filter})" opacity="${op}"/>`);
const UI="Liberation Sans,Carlito,Arial,sans-serif";
const logoRing=(cx,cy,r,col='#8f949b')=>C(cx,cy,r,{f:'none',s:col,w:r*.18})+C(cx,cy,r*.5,{f:col,op:.55});
// wallpaper: layered blurred blooms
const wallBloom=(x,y,w,h,kind)=>{
  const bl=(cx,cy,rw,rh,g,rot)=>`<ellipse cx="${f(x+cx*w)}" cy="${f(y+cy*h)}" rx="${f(rw*w)}" ry="${f(rh*h)}" fill="url(#${g})" transform="rotate(${rot} ${f(x+cx*w)} ${f(y+cy*h)})" filter="url(#blurM)"/>`;
  if(kind==='blue') return R(x,y,w,h,{f:'#0a1c5a'})+bl(.5,.55,.55,.45,'gBloom1',-20)+bl(.25,.3,.45,.3,'gBloom3',30)+bl(.78,.7,.4,.35,'gBloom2',-30)+bl(.55,.25,.35,.25,'gBloom1',10)+`<path d="M${x} ${y+h*.72} C${x+w*.3} ${y+h*.5} ${x+w*.55} ${y+h*.95} ${x+w} ${y+h*.55} L${x+w} ${y+h} L${x} ${y+h} Z" fill="rgba(10,20,80,.35)"/>`;
  if(kind==='sunset') return R(x,y,w,h,{f:'#1b1f5e'})+bl(.5,.95,.9,.55,'gBloom4',0)+bl(.3,.7,.7,.4,'gBloom2',20)+bl(.7,.35,.6,.4,'gBloom3',-15)+bl(.4,.15,.5,.3,'gBloom1',0)+R(x,y,w,h,{f:'rgba(0,0,0,.06)'});
  return R(x,y,w,h,{f:'#222'});
};
// ---- app icons with glyphs ----
function appIcon(k,x,y,s){
  const r=s*.23;let g='';const c=s/2;
  const base=(a,b)=>{const id=uid();return `<defs><linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></linearGradient></defs>`+R(x,y,s,s,{f:`url(#${id})`,r})+R(x,y,s,s*.5,{f:'rgba(255,255,255,.14)',r})};
  const gx=(d)=>G(x,y,d);
  switch(k){
   case 'camera': g=base('#9a9ea6','#4b4e55')+gx(R(s*.17,s*.3,s*.66,s*.46,{f:'#1b1c20',r:s*.08})+C(c,s*.53,s*.17,{f:'#2f3138',s:'#9a9ea6',w:s*.025})+C(c,s*.53,s*.09,{f:'#0b0c10'})+R(s*.3,s*.22,s*.14,s*.08,{f:'#1b1c20',r:s*.02})); break;
   case 'photos': g=base('#ffffff','#e9ecf3')+gx([['#ff5a5f',0],['#ffb400',45],['#ffe14d',90],['#6bd66b',135],['#38b6ff',180],['#7a6bff',225],['#d86bff',270],['#ff6ba8',315]].map(([col,a])=>`<ellipse cx="${f(c+Math.cos(a*Math.PI/180)*s*.16)}" cy="${f(c+Math.sin(a*Math.PI/180)*s*.16)}" rx="${f(s*.17)}" ry="${f(s*.09)}" fill="${col}" opacity=".78" transform="rotate(${a} ${f(c+Math.cos(a*Math.PI/180)*s*.16)} ${f(c+Math.sin(a*Math.PI/180)*s*.16)})"/>`).join('')); break;
   case 'mail': g=base('#4fb3ff','#1a6fe0')+gx(R(s*.18,s*.28,s*.64,s*.44,{f:'#fff',r:s*.05})+P(`M${s*.18} ${s*.32} L${c} ${s*.56} L${s*.82} ${s*.32}`,{s:'#1a6fe0',w:s*.04})); break;
   case 'notes': g=base('#ffe56a','#f5c400')+gx(R(0,0,s,s*.22,{f:'#fff6c2',r:r})+[0,1,2,3].map(i=>L(s*.16,s*.38+i*s*.14,s*.84,s*.38+i*s*.14,{s:'#d0a800',w:s*.02,op:.7})).join('')); break;
   case 'music': g=base('#ff6a88','#e0224a')+gx(P(`M${s*.4} ${s*.7} L${s*.4} ${s*.28} L${s*.7} ${s*.22} L${s*.7} ${s*.62}`,{s:'#fff',w:s*.05})+E_(s*.34,s*.7,s*.09,s*.07,{f:'#fff'})+E_(s*.64,s*.62,s*.09,s*.07,{f:'#fff'})); break;
   case 'maps': g=base('#7bd86f','#2fae4a')+gx(P(`M0 ${s*.65} L${s} ${s*.35}`,{s:'#fff',w:s*.1,op:.9})+P(`M${s*.45} ${s*.18} a${s*.12} ${s*.12} 0 1 1 .01 0 L${s*.45} ${s*.55} Z`,{f:'#ff3b30'})+C(s*.45,s*.3,s*.045,{f:'#fff'})); break;
   case 'safari': g=base('#6bd0ff','#1773e8')+gx(C(c,c,s*.34,{f:'none',s:'#fff',w:s*.04})+P(`M${s*.62} ${s*.3} L${s*.54} ${s*.54} L${s*.3} ${s*.7} L${s*.46} ${s*.46} Z`,{f:'#ff3b30'})+P(`M${s*.3} ${s*.7} L${s*.46} ${s*.46} L${s*.54} ${s*.54} Z`,{f:'#fff'})); break;
   case 'settings': g=base('#a3a7ae','#5b5f66')+gx(C(c,c,s*.27,{f:'#d9dce1',s:'#6b6f76',w:s*.02})+[...Array(8)].map((_,i)=>`<rect x="${f(c-s*.045)}" y="${f(c-s*.36)}" width="${f(s*.09)}" height="${f(s*.14)}" fill="#d9dce1" transform="rotate(${i*45} ${f(c)} ${f(c)})"/>`).join('')+C(c,c,s*.1,{f:'#5b5f66'})); break;
   case 'clock': g=base('#1c1c1e','#000')+gx(C(c,c,s*.36,{f:'#fff'})+[...Array(12)].map((_,i)=>L(c+Math.sin(i*Math.PI/6)*s*.3,c-Math.cos(i*Math.PI/6)*s*.3,c+Math.sin(i*Math.PI/6)*s*.34,c-Math.cos(i*Math.PI/6)*s*.34,{s:'#222',w:s*.015})).join('')+L(c,c,c,s*.3,{s:'#111',w:s*.04})+L(c,c,s*.68,c+s*.04,{s:'#111',w:s*.03})+L(c,c-s*.02,c-s*.18,c+s*.14,{s:'#ff9500',w:s*.015})); break;
   case 'calendar': g=base('#ffffff','#f1f1f4')+gx(T(c,s*.3,'MON',{sz:s*.17,f:'#ff3b30',b:1,ff:UI})+T(c,s*.72,'12',{sz:s*.42,f:'#111',ff:UI})); break;
   case 'messages': g=base('#6be07a','#1fb83b')+gx(E_(c,s*.46,s*.32,s*.24,{f:'#fff'})+P(`M${s*.3} ${s*.62} L${s*.24} ${s*.78} L${s*.44} ${s*.66}`,{f:'#fff'})); break;
   case 'phone': g=base('#6be07a','#1fb83b')+gx(P(`M${s*.32} ${s*.26} q${s*.1} -${s*.06} ${s*.14} .01 l${s*.04} ${s*.12} q-${s*.05} ${s*.06} -${s*.02} ${s*.12} q${s*.06} ${s*.1} ${s*.14} ${s*.14} q${s*.06} -${s*.03} ${s*.11} -${s*.02} l${s*.12} ${s*.05} q.02 ${s*.06} -${s*.04} ${s*.12} q-${s*.1} ${s*.1} -${s*.33} -${s*.12} q-${s*.22} -${s*.26} -${s*.17} -${s*.49}z`,{f:'#fff'})); break;
   default: g=base('#bbb','#777');
  }
  return g;
}
