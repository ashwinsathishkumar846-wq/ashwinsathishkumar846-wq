// ===== helpers (all units = mm) =====
const f=n=>Math.round(n*100)/100;
const R=(x,y,w,h,o={})=>`<rect x="${f(x)}" y="${f(y)}" width="${f(w)}" height="${f(h)}" rx="${o.r||0}" fill="${o.f||'none'}" stroke="${o.s||'none'}" stroke-width="${o.w||.2}" ${o.d?`stroke-dasharray="${o.d}"`:''} ${o.op?`opacity="${o.op}"`:''}/>`;
const C=(x,y,r,o={})=>`<circle cx="${f(x)}" cy="${f(y)}" r="${f(r)}" fill="${o.f||'none'}" stroke="${o.s||'none'}" stroke-width="${o.w||.2}" ${o.op?`opacity="${o.op}"`:''}/>`;
const E_=(x,y,rx,ry,o={})=>`<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(rx)}" ry="${f(ry)}" fill="${o.f||'none'}" stroke="${o.s||'none'}" stroke-width="${o.w||.2}" ${o.rot?`transform="rotate(${o.rot} ${x} ${y})"`:''}/>`;
const P=(d,o={})=>`<path d="${d}" fill="${o.f||'none'}" stroke="${o.s||'none'}" stroke-width="${o.w||.2}" ${o.d?`stroke-dasharray="${o.d}"`:''} stroke-linecap="round" stroke-linejoin="round" ${o.op?`opacity="${o.op}"`:''}/>`;
const L=(x1,y1,x2,y2,o={})=>`<line x1="${f(x1)}" y1="${f(y1)}" x2="${f(x2)}" y2="${f(y2)}" stroke="${o.s||'#000'}" stroke-width="${o.w||.2}" ${o.d?`stroke-dasharray="${o.d}"`:''} stroke-linecap="round"/>`;
const T=(x,y,s,o={})=>`<text x="${f(x)}" y="${f(y)}" font-size="${o.sz||3}" font-family="${o.ff||'Carlito,Calibri,sans-serif'}" font-weight="${o.b?700:400}" ${o.i?'font-style="italic"':''} fill="${o.f||'#000'}" text-anchor="${o.a||'middle'}" ${o.ls?`letter-spacing="${o.ls}"`:''} ${o.rot?`transform="rotate(${o.rot} ${x} ${y})"`:''}>${s}</text>`;
const G=(x,y,c,o={})=>`<g transform="translate(${f(x)},${f(y)})${o.rot?` rotate(${o.rot})`:''}${o.sx?` scale(${o.sx},${o.sy||1})`:''}">${c}</g>`;
const CUT='#000',FOLD='#555';
const cutRect=(x,y,w,h,o={})=>R(x,y,w,h,{s:CUT,w:.3,r:o.r||0,f:o.f||'none'});
const foldLine=(x1,y1,x2,y2)=>L(x1,y1,x2,y2,{s:FOLD,w:.25,d:'1.4 1'});
const cutLine=(x1,y1,x2,y2)=>L(x1,y1,x2,y2,{s:CUT,w:.3});
const RAL="Raleway,Carlito,sans-serif",MONO="'DejaVu Sans Mono',monospace",HAND="'DejaVu Serif',serif";
// ===== box net : faces = {front,back,left,right,top,bottom} each (w,h)=>svg
function boxNet(W,H,D,fc,opt={}){
  const t=opt.tab||5,ox=Math.max(0,t-D),oy=opt.noTab?0:t;
  const nb=!!opt.noBack; const w=ox*2+D*2+W; const h=nb?oy+D+H+D:oy+D+H+D+H;
  let s='';
  const face=(fn,x,y,fw,fh,rot)=>{ if(!fn) return R(x,y,fw,fh,{f:'#ddd'}); const g=fn(fw,fh); return rot?`<g transform="translate(${f(x+fw)},${f(y+fh)}) rotate(180)">${g}</g>`:`<g transform="translate(${f(x)},${f(y)})">${g}</g>`};
  const xF=ox+D, yT=oy, yFr=oy+D, yB=oy+D+H, yK=oy+D+H+D;
  s+=face(fc.top,xF,yT,W,D);s+=face(fc.front,xF,yFr,W,H);s+=face(fc.left,ox,yFr,D,H);s+=face(fc.right,xF+W,yFr,D,H);s+=face(fc.bottom,xF,yB,W,D);if(!nb)s+=face(fc.back,xF,yK,W,H,true);
  // glue tabs
  const tabc='#e8e8e8';
  const tabH=(x,y,len,dir)=>{ // horizontal tab above top strip
    return P(`M${x} ${y} L${x+1.5} ${y-t} L${x+len-1.5} ${y-t} L${x+len} ${y} Z`,{f:tabc,s:CUT,w:.3})};
  if(!opt.noTab)s+=tabH(xF,yT,W);
  const tabV=(x,y,len,side)=>{const sg=side==='L'?-1:1;return P(`M${x} ${y} L${x+sg*t} ${y+1.5} L${x+sg*t} ${y+len-1.5} L${x} ${y+len} Z`,{f:tabc,s:CUT,w:.3})};
  if(!nb)s+=tabV(xF,yK,H,'L')+tabV(xF+W,yK,H,'R');
  // fold lines
  s+=foldLine(xF,yFr,xF+W,yFr)+foldLine(xF,yB,xF+W,yB)+(nb?'':foldLine(xF,yK,xF+W,yK))+foldLine(xF,yFr,xF,yB)+foldLine(xF+W,yFr,xF+W,yB)+foldLine(xF,yT,xF+W,yT);
  if(!nb)s+=foldLine(xF,yK,xF,yK+H)+foldLine(xF+W,yK,xF+W,yK+H);
  // exposed cuts
  s+=cutLine(xF,yT,xF,yFr)+cutLine(xF+W,yT,xF+W,yFr);if(opt.noTab)s+=cutLine(xF,yT,xF+W,yT);
  s+=cutLine(ox,yFr,xF,yFr)+cutLine(ox,yFr,ox,yB)+cutLine(ox,yB,xF,yB);
  s+=cutLine(xF+W,yFr,xF+W+D,yFr)+cutLine(xF+W+D,yFr,xF+W+D,yB)+cutLine(xF+W,yB,xF+W+D,yB);
  s+=cutLine(xF,yB,xF,yK)+cutLine(xF+W,yB,xF+W,yK);
  s+=nb?cutLine(xF,yK,xF+W,yK):cutLine(xF,yK+H,xF+W,yK+H);
  s+=T(xF+W/2,yT-t-1.2,'',{});
  return {w,h,svg:s};
}
// ===== flat double-sided piece with fold tab: art(w,h) front; back(w,h) optional; tabH = foot tab height
function flat2(W,H,front,back,opt={}){
  const tab=opt.tab===undefined?10:opt.tab,gap=6,m=0;
  const tw=opt.tabW||W*0.7,cut=opt.cut||((w,h)=>cutRect(0,0,w,h,{r:opt.r||0}));
  const piece=(art,mirror)=>{
    let g='';
    g+=art(W,H)+cut(W,H);
    if(tab>0){const x=(W-tw)/2;g+=P(`M${x} ${H} L${x} ${H+tab} L${x+tw} ${H+tab} L${x+tw} ${H}`,{f:'#ececec',s:CUT,w:.3})+foldLine(x,H,x+tw,H);}
    return mirror?`<g transform="translate(${f(W)},0) scale(-1,1)">${g}</g>`:g;
  };
  let s=piece(front,false);
  let w=W,h=H+tab;
  if(back!==null){
    const bk=back||((w_,h_)=>R(0,0,w_,h_,{f:'#d9d9d9'})+T(w_/2,h_/2,'BACK',{sz:Math.min(6,W/6),f:'#999',b:1}));
    s+=`<g transform="translate(${f(W+gap)},0)">${piece(bk,true)}</g>`;w=W*2+gap;
  }
  return {w,h,svg:s};
}
function oneSided(W,H,art,opt={}){return {w:W,h:H,svg:art(W,H)+(opt.cut===false?'':cutRect(0,0,W,H,{r:opt.r||0}))}}
