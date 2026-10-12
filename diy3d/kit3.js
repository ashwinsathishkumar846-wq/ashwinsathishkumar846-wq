// ===== STUDIO kit: page composition from three.js PBR renders (rend/*.png, 16 px/mm) =====
const RP=n=>`rend/${n}.png`;
// image face (fw × fh in mm); rot: 0 | 90 (cw) | -90 (ccw) | 180
const imgF=(n,rot=0,bg)=>(fw,fh)=>{
  const b=bg?R(0,0,fw,fh,{f:bg}):'';
  if(rot===90) return b+`<image href="${RP(n)}" width="${f(fh)}" height="${f(fw)}" preserveAspectRatio="none" transform="translate(${f(fw)},0) rotate(90)"/>`;
  if(rot===-90) return b+`<image href="${RP(n)}" width="${f(fh)}" height="${f(fw)}" preserveAspectRatio="none" transform="translate(0,${f(fh)}) rotate(-90)"/>`;
  if(rot===180) return b+`<image href="${RP(n)}" width="${f(fw)}" height="${f(fh)}" preserveAspectRatio="none" transform="rotate(180 ${f(fw/2)} ${f(fh/2)})"/>`;
  return b+`<image href="${RP(n)}" width="${f(fw)}" height="${f(fh)}" preserveAspectRatio="none"/>`;
};
const solid=(c,label)=>(fw,fh)=>R(0,0,fw,fh,{f:c})+(label?T(fw/2,fh/2+1,label,{sz:Math.min(3,fh/4),f:'rgba(255,255,255,.35)',ff:RAL,b:1,ls:.3}):'');
// silhouette piece: rendered image + traced cut line (SVG alpha-dilate ring) + optional foot tab
function sil(n,W,H,opt={}){
  const tab=opt.tab||0,tw=opt.tabW||W*.6,tx=(W-tw)/2;
  const im=`<image href="${RP(n)}" width="${f(W)}" height="${f(H)}" preserveAspectRatio="none"/>`;
  const tb=tab?P(`M${f(tx)} ${f(H-1.5)} L${f(tx)} ${f(H+tab-1.2)} Q${f(tx)} ${f(H+tab)} ${f(tx+1.2)} ${f(H+tab)} L${f(tx+tw-1.2)} ${f(H+tab)} Q${f(tx+tw)} ${f(H+tab)} ${f(tx+tw)} ${f(H+tab-1.2)} L${f(tx+tw)} ${f(H-1.5)} Z`,{f:'#e6e6e6'}):'';
  const bg=opt.bg?R(opt.bg[0],opt.bg[1],opt.bg[2],opt.bg[3],{f:opt.bg[4]}):'';
  let s=`<g filter="url(#${opt.tight?'cutT':'cutS'})">${tb}${bg}${im}</g>`+tb+bg+im;
  if(tab){s+=foldLine(tx,H,tx+tw,H)+T(W/2,H+tab/2+1,'glue',{sz:2,f:'#999',ff:RAL})}
  return {w:W,h:H+tab,svg:s};
}
// front | back pair (renders are true back views → no mirroring; glue back-to-back)
function pair(n,W,H,opt={}){
  const a=sil(n+'_front',W,H,opt),b=sil(n+'_back',W,H,opt),g=4;
  return {w:W*2+g,h:a.h,svg:a.svg+`<g transform="translate(${f(W+g)},0)">${b.svg}</g>`+T(W/2,-1.2,'FRONT',{sz:2,f:'#888',ff:RAL,ls:.3})+T(W*1.5+g,-1.2,'BACK',{sz:2,f:'#888',ff:RAL,ls:.3})};
}
function group(items,gap=3){let x=0,h=0,s='';for(const it of items){s+=`<g transform="translate(${f(x)},${f(h?0:0)})">${it.svg}</g>`;x+=it.w+gap;h=Math.max(h,it.h)}return {w:x-gap,h,svg:s}}
function rows(rs,gap=3){let y=0,w=0,s='';for(const r of rs){s+=`<g transform="translate(0,${f(y)})">${r.svg}</g>`;y+=r.h+gap;w=Math.max(w,r.w)}return {w,h:y-gap,svg:s}}
const PX=n=>({w:0,h:0}); // placeholder
// ---------- objects ----------
const O3={};
O3.cloud=oneSided(160,70,cloudArt2,{cut:false});
O3.past=oneSided(90,30,pill2('Past','(Traditional Computing)'),{r:12});
O3.present=oneSided(70,30,pill2('Present','(Digital Era)'),{r:12});
O3.future=oneSided(80,30,pill2('Future','(AI & Beyond)'),{r:12});
for(let i=0;i<5;i++)O3['sb'+i]=sil('sb'+i+'_front',45,15,{tight:1});
O3.imagine=sil('imagine_front',90,18,{tight:1});
O3.abacus=pair('abacus',70,70,{tab:10,tabW:50,bg:[3,3,64,56,'#3a2a20']});
O3.tag=sil('tag_front',30,11,{tight:1});O3.note=sil('note_front',40,26,{tight:1});
O3.binary=sil('binary_front',35,40,{tight:1});O3.quill=sil('quill_front',25,45,{tab:6,tabW:14});
const BK=[['book0','#3b2414','Binary'],['book1','#14223f','Logic'],['book2','#4a1219','Algorithms']];
BK.forEach(([n,c])=>O3[n]=boxNet(40,12,31.2,{front:imgF(n+'_front',0,c),back:imgF(n+'_back',0,'#efe6d2'),top:imgF(n+'_top',0,c),bottom:imgF(n+'_bottom',0,c),left:imgF(n+'_left',0,c),right:imgF(n+'_right',0,c)},{tab:5}));
O3.monitor=pair('monitor',70,50,{tab:6,tabW:28});
O3.keyboard=sil('keyboard_top',60,20,{tight:1});
O3.lid=pair('laptopLid',60,35,{tab:8,tabW:50});
O3.lbase=sil('laptopBase_top',60,40,{tight:1});
O3.tablet=boxNet(45,32,4,{front:imgF('tablet_front',0,'#1b1c20'),back:imgF('tablet_back',0,'#8d9096'),left:imgF('tablet_left',0,'#8d9096'),right:imgF('tablet_right',0,'#8d9096'),top:imgF('tablet_top',0,'#8d9096'),bottom:imgF('tablet_bottom',0,'#8d9096')},{tab:5});
O3.phone=boxNet(18,38,5,{front:imgF('phone_front',0,'#121316'),back:imgF('phone_back',0,'#2a2c31'),left:imgF('phone_left',0,'#3a3c42'),right:imgF('phone_right',0,'#3a3c42'),top:imgF('phone_top',0,'#3a3c42'),bottom:imgF('phone_bottom',0,'#3a3c42')},{tab:5});
O3.robot=pair('robot',30,60,{tab:8,tabW:20});
O3.brain=(()=>{const o=sil('brain_front',65,60,{tab:8,tabW:40,tight:1});return o})();
O3.aiscreen=pair('aiscreen',55,50,{tab:8,tabW:40,tight:1});
O3.aibase=boxNet(55,30,6,{front:imgF('aibase_top'),top:imgF('aibase_back',180),bottom:imgF('aibase_front'),left:imgF('aibase_left',90),right:imgF('aibase_right',-90),back:solid('#0a1430','BOTTOM')},{tab:5});
for(let i=0;i<6;i++)O3['plant'+i]=pair('plant'+i,25,38,{tab:6,tabW:14});
for(let i=0;i<3;i++)O3['fol'+i]=sil('fol'+i+'_front',100,14);
O3.star=sil('star_front',10,10);
const RK=[[16.1,10.4],[12.6,9.2],[10.4,6.9],[18.4,11.5],[8.1,5.8],[13.8,8.1],[11.5,8.1],[6.9,4.6],[14.9,9.2],[9.2,6.9],[17.2,10.4],[5.8,4.6]];
RK.forEach(([w,h],i)=>O3['rock'+i]=sil('rock'+i+'_top',w,h));
// platform sides: the top texture mirrored across each fold so the surface wraps seamlessly, then shaded like a vertical face
let _sid=0;
const sideF=(n,W,D,m,dk)=>(fw,fh)=>{const id='sd'+(_sid++);const mt={b:`matrix(1,0,0,-1,0,${D})`,t:`matrix(1,0,0,-1,0,${fh})`,l:`matrix(-1,0,0,1,${fw},0)`,r:`matrix(-1,0,0,1,${W},0)`}[m];
  const g={b:['0','0','0','1'],t:['0','1','0','0'],l:['1','0','0','0'],r:['0','0','1','0']}[m];
  return `<defs><linearGradient id="${id}" x1="${g[0]}" y1="${g[1]}" x2="${g[2]}" y2="${g[3]}"><stop offset="0" stop-color="#000" stop-opacity="${dk*.55}"/><stop offset="1" stop-color="#000" stop-opacity="${dk*1.5}"/></linearGradient></defs><svg width="${f(fw)}" height="${f(fh)}" overflow="hidden"><image href="${RP(n+'_top')}" width="${W}" height="${D}" preserveAspectRatio="none" transform="${mt}"/></svg>`+R(0,0,fw,fh,{f:`url(#${id})`});};
const plat=(n,W,T_,D,dk)=>boxNet(W,D,T_,{front:imgF(n+'_top'),bottom:sideF(n,W,D,'b',dk),top:sideF(n,W,D,'t',dk),left:sideF(n,W,D,'l',dk),right:sideF(n,W,D,'r',dk)},{noBack:true,noTab:true});
O3.pPast=plat('pPast',140,15,130,.32);O3.pPres=plat('pPres',160,20,150,.3);O3.pFut=plat('pFut',130,20,130,.25);
const fas=(off,w)=>({w,h:50,clip:true,svg:`<g transform="translate(${-off},0)">${fasciaFull2(460,50)}</g>`+cutRect(0,0,w,50)});
O3.fas1=(()=>{const o=fas(0,232);o.svg+=R(228,0,4,50,{f:'rgba(255,255,255,.18)'})+L(228,0,228,50,{s:'#fff',w:.25,d:'1 1'});return o})();
O3.fas2=(()=>{const o=fas(228,232);o.svg+=L(4,0,4,50,{s:'#fff',w:.25,d:'1 1'});return o})();
// ---------- sheets ----------
const SHEETS=[];
const sheet=(title,orient,list,o={})=>SHEETS.push({title,orient,list,...o});
sheet('Title cloud, section headings & signboards','P',[[O3.cloud,'Title cloud','16 × 7 cm',1],[O3.past,'Heading – Past','9 × 3 cm',1],[O3.present,'Heading – Present','7 × 3 cm',1],[O3.future,'Heading – Future','8 × 3 cm',1],[O3.sb0,'Signboard – Generative AI','4.5 × 1.5 cm',1],[O3.sb1,'Signboard – AI Assistants','4.5 × 1.5 cm',1],[O3.sb2,'Signboard – Smart Content','4.5 × 1.5 cm',1],[O3.sb3,'Signboard – Creative Tools','4.5 × 1.5 cm',1],[O3.sb4,'Signboard – Better Tomorrow','4.5 × 1.5 cm',1],[O3.imagine,'Sign – Imagine • Create • Innovate','9 × 1.8 cm',1]]);
sheet('PAST – Traditional Computing','P',[[O3.abacus,'Abacus (front | back)','7 × 7 × 2 cm',1],[O3.quill,'Quill & ink pot','2.5 × 4.5 cm',1],[O3.note,'Note card','4 × 2.6 cm',1],[O3.binary,'Binary code paper','3.5 × 4 cm',1],[O3.tag,'Label – Abacus','3 × 1.1 cm',1]]);
sheet('PAST – Books 1 & 2 (separate box nets)','P',[[O3.book0,'Book 1 – Binary (box net)','4 × 1.2 × 3.1 cm',1],[O3.book1,'Book 2 – Logic (box net)','4 × 1.2 × 3.1 cm',1]]);
sheet('PAST – Book 3  •  PRESENT – Tablet & Smartphone','P',[[O3.book2,'Book 3 – Algorithms (box net)','4 × 1.2 × 3.1 cm',1],[O3.tablet,'Tablet (box net)','4.5 × 3.2 × 0.4 cm',1],[O3.phone,'Smartphone (box net)','1.8 × 3.8 × 0.5 cm',1]]);
sheet('PRESENT – Digital Era','P',[[O3.monitor,'Desktop monitor (front | back)','7 × 5 × 2 cm',1],[O3.keyboard,'Keyboard (top)','6 × 2 cm',1],[O3.lid,'Laptop screen (front | back)','6 × 3.5 cm',1],[O3.lbase,'Laptop base (top)','6 × 4 cm',1]]);
sheet('FUTURE – AI & Beyond','P',[[O3.robot,'Robot (front | back)','3 × 6 × 2.5 cm',1],[O3.brain,'AI brain (neon panel)','6.5 × 6 cm',1],[O3.aiscreen,'AI screen (front | back)','5.5 × 5 cm',1],[O3.aibase,'AI screen base (box net)','5.5 × 3 × 0.6 cm',1]]);
const decor=[];for(let i=0;i<6;i++)decor.push([O3['plant'+i],`Potted plant ${i+1} (front | back)`,'2.5 × 3.8 cm',1]);
for(let i=0;i<3;i++)decor.push([O3['fol'+i],`Foliage strip ${i+1}`,'10 × 1.4 cm',1]);
decor.push([rows([group(Array(12).fill(O3.star),2.2)]),'Stars ×12','1 × 1 cm',1]);
decor.push([rows([group(RK.slice(0,6).map((_,i)=>O3['rock'+i]),2.5),group(RK.slice(6).map((_,i)=>O3['rock'+(i+6)]),2.5)],2.5),'Rocks ×12 (assorted)','0.6–1.8 cm',1]);
sheet('Plants, foliage strips, stars & rocks','P',decor);
sheet('Platform skin – PAST (soil)','P',[[O3.pPast,'Past platform (top + 4 sides)','14 × 1.5 × 13 cm',1]]);
sheet('Platform skin – FUTURE (neon circuit)','P',[[O3.pFut,'Future platform (top + 4 sides)','13 × 2 × 13 cm',1]]);
sheet('Platform skin – PRESENT (concrete)','P',[[O3.pPres,'Present platform (top + 4 sides)','16 × 2 × 15 cm',1]],{mx:5});
sheet('Front fascia – left & right halves (overlap 4 mm)','L',[[O3.fas1,'Fascia LEFT (0–23.2 cm)','23.2 × 5 cm',1],[O3.fas2,'Fascia RIGHT (22.8–46 cm)','23.2 × 5 cm',1]]);
// ---------- packer (centres each row) ----------
function pack(sheet){
  const pw=sheet.orient==='L'?297:210,ph=sheet.orient==='L'?210:297;
  const mx=sheet.mx||9,top=17,bot=9,gap=7,cap=5;
  const pages=[];let cur,x,y,rowH,row;
  const flush=()=>{if(!row.length)return;const used=x-gap-mx,off=(pw-2*mx-used)/2;row.forEach(it=>it.x+=off);row=[]};
  const newPage=()=>{cur={w:pw,h:ph,title:sheet.title,items:[]};pages.push(cur);x=mx;y=top+3;rowH=0;row=[]};
  newPage();
  for(const it of sheet.list){
    const [o,name,dim,qty]=it;const iw=o.w,ih=o.h+(name?cap:0);
    if(x+iw>pw-mx&&x>mx){flush();x=mx;y+=rowH+gap;rowH=0}
    if(y+ih>ph-bot&&cur.items.length){flush();newPage()}
    const e={o,name,dim,qty,x,y};cur.items.push(e);row.push(e);x+=iw+gap;rowH=Math.max(rowH,ih);
  }
  flush();return pages;
}
// ---------- studio cover ----------
function cover3(rowsL){
  const W=210,H=297;
  let s=`<svg width="${W}mm" height="${H}mm" viewBox="0 0 ${W} ${H}" style="position:absolute;left:0;top:0">`;
  s+=`<defs><linearGradient id="cvBg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#060b1e"/><stop offset=".7" stop-color="#0d1a44"/><stop offset="1" stop-color="#16285e"/></linearGradient>
  <radialGradient id="cvGlow" cx=".5" cy=".85" r=".6"><stop offset="0" stop-color="#3fa9ff" stop-opacity=".35"/><stop offset="1" stop-color="#3fa9ff" stop-opacity="0"/></radialGradient>
  <linearGradient id="cvFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".10"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient></defs>`;
  s+=R(0,0,W,100,{f:'url(#cvBg)'})+R(0,0,W,100,{f:'url(#cvGlow)'});
  s+=T(W/2,15,'EVOLUTION OF COMPUTER SCIENCE',{sz:8.4,f:'#fff',b:1,ff:RAL,ls:.5})+T(W/2,22.5,'From Numbers to Neural Networks',{sz:4.6,f:'#9fd8ff',ff:RAL,ls:.3})+T(W/2,28,'STUDIO EDITION  •  3D-rendered actual-size DIY cut-out kit for the 46 × 30 cm model',{sz:2.7,f:'#c9d8ff',ff:RAL,ls:.2});
  // hero line-up (actual renders, scaled)
  const hero=[['abacus_front',70,70,.4],['book1_top',40,31.2,.5],['monitor_front',70,50,.55],['laptopLid_front',60,35,.5],['phone_front',18,38,.55],['robot_front',30,60,.7],['brain_front',65,60,.42]];
  let tw=hero.reduce((a,h)=>a+h[1]*h[3],0)+3*(hero.length-1),hx=(W-tw)/2,base=84;
  s+=R(8,base,W-16,14,{f:'url(#cvFloor)'})+L(8,base,W-8,base,{s:'rgba(255,255,255,.25)',w:.2});
  hero.forEach(([n,w,h,k])=>{const iw=w*k,ih=h*k;s+=`<image href="${RP(n)}" x="${f(hx)}" y="${f(base-ih)}" width="${f(iw)}" height="${f(ih)}" preserveAspectRatio="none"/>`;
    s+=`<image href="${RP(n)}" x="${f(hx)}" y="${f(base)}" width="${f(iw)}" height="${f(ih)}" preserveAspectRatio="none" opacity=".16" transform="translate(0,${f(2*base)}) scale(1,-1)"/>`;hx+=iw+3});
  s+=R(0,base+.3,W,100-base-.3,{f:'url(#cvBg)',op:.55});
  // how to
  s+=T(12,110,'HOW TO BUILD',{sz:4.2,a:'start',b:1,ff:RAL,f:'#0d1a44'});
  const ins=['1.  Print at 100 % ("Actual size", NOT "fit to page") on A4 matt/photo paper, best quality.','2.  Check the scale ruler: it must measure exactly 10 cm.','3.  Cut along the solid black lines; they trace each object’s outline. Fold on dashed lines.','4.  FRONT | BACK pairs: cut both, glue back-to-back on 1–2 mm card; fold the grey foot tab to stand.','5.  Box nets (books, tablet, phone, AI base): score folds, glue tabs inside, pack with card.','6.  Platform skins wrap a foam/card box of the same size; fascia halves overlap 4 mm.','7.  Signboards, headings and the cloud look best mounted on 3 mm foam board.'];
  ins.forEach((t,i)=>s+=T(12,116.5+i*5,t,{sz:2.75,a:'start',ff:RAL,f:'#222'}));
  s+=T(12,155,'SCALE CHECK',{sz:3.2,a:'start',b:1,ff:RAL,f:'#0d1a44'});
  s+=L(12,161,112,161,{s:'#000',w:.4});for(let i=0;i<=100;i++){s+=L(12+i,161,12+i,161-(i%10==0?4:i%5==0?3:2),{s:'#000',w:.25});if(i%10==0)s+=T(12+i,165.5,String(i/10),{sz:2.4,ff:RAL})}
  s+=T(115,162,'cm',{sz:2.6,a:'start',ff:RAL,f:'#444'});
  s+=T(140,155,'LEGEND',{sz:3.2,a:'start',b:1,ff:RAL,f:'#0d1a44'});
  s+=L(140,159,158,159,{s:'#000',w:.3})+T(161,160,'cut',{sz:2.6,a:'start',ff:RAL})+L(140,163.5,158,163.5,{s:'#555',w:.25,d:'1.4 1'})+T(161,164.5,'fold',{sz:2.6,a:'start',ff:RAL})+R(140,166.5,18,3,{f:'#e6e6e6',s:'#000',w:.3})+T(161,169,'glue tab',{sz:2.6,a:'start',ff:RAL});
  // parts list – two columns
  s+=T(12,177,'PARTS LIST',{sz:4.2,a:'start',b:1,ff:RAL,f:'#0d1a44'});
  const half=Math.ceil(rowsL.length/2),cw=91.5,rh=4.15;
  [rowsL.slice(0,half),rowsL.slice(half)].forEach((col,c)=>{const x0=12+c*(cw+3),y0=180.5;
    s+=R(x0,y0,cw,5,{f:'#0d1a44'})+T(x0+2,y0+3.5,'Part',{sz:2.5,a:'start',f:'#fff',b:1,ff:RAL})+T(x0+cw-14,y0+3.5,'Size',{sz:2.5,a:'end',f:'#fff',b:1,ff:RAL})+T(x0+cw-5,y0+3.5,'Sheet',{sz:2.5,f:'#fff',b:1,ff:RAL});
    col.forEach((r,i)=>{const y=y0+5+i*rh;if(i%2)s+=R(x0,y,cw,rh,{f:'#eef1f8'});s+=T(x0+2,y+3,r[0],{sz:2.25,a:'start',ff:RAL})+T(x0+cw-14,y+3,r[1],{sz:2.2,a:'end',ff:RAL,f:'#444'})+T(x0+cw-5,y+3,String(r[2]),{sz:2.25,ff:RAL})})});
  s+=T(W/2,H-6,'All artwork: physically-based (PBR) 3D renders made with three.js, at 16 px/mm. Dimensions are estimates from the project photo – check against your model.',{sz:2.2,f:'#777',ff:RAL});
  s+='</svg>';return `<div style="position:absolute;left:0;top:0;width:${W}mm;height:${H}mm">${s}</div>`;
}
function buildAll(){
  const all=[];SHEETS.forEach(sh=>pack(sh).forEach(p=>all.push(p)));
  const total=all.length+1;const rl=[];
  all.forEach((p,i)=>p.items.forEach(it=>{if(it.name)rl.push([it.name.replace(/ \(.*\)/,''),it.dim,i+2])}));
  rl.push(['Fairy lights (wire)','not printed','–']);
  const out=[{w:210,h:297,html:cover3(rl)}];
  all.forEach((p,i)=>out.push({w:p.w,h:p.h,html:renderPage(p,i+1,total)}));
  return out;
}
