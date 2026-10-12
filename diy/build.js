// packer + page renderer
function pack(sheet){
  const pw=sheet.orient==='L'?297:210,ph=sheet.orient==='L'?210:297;
  const mx=9,top=16,bot=9,gap=6,cap=5;
  const pages=[];let cur=null,x,y,rowH;
  const newPage=()=>{cur={w:pw,h:ph,title:sheet.title,items:[]};pages.push(cur);x=mx;y=top;rowH=0};
  newPage();
  for(const it of sheet.list){
    const [o,name,dim,qty]=it;const iw=o.w,ih=o.h+(name?cap:0);
    if(x+iw>pw-mx&&x>mx){x=mx;y+=rowH+gap;rowH=0}
    if(y+ih>ph-bot){ if(cur.items.length){newPage()} }
    cur.items.push({o,name,dim,qty,x,y});x+=iw+gap;rowH=Math.max(rowH,ih);
  }
  return pages;
}
function renderPage(pg,idx,total){
  const W=pg.w,H=pg.h;
  let body=`<div style="position:absolute;left:0;top:0;width:${W}mm;height:${H}mm;">`;
  body+=`<svg width="${W}mm" height="${H}mm" viewBox="0 0 ${W} ${H}" style="position:absolute;left:0;top:0">`;
  body+=T(9,9,'EVOLUTION OF COMPUTER SCIENCE – DIY CUT-OUT KIT',{sz:3.6,a:'start',b:1,ff:RAL,f:'#222'})+T(W-9,9,`Sheet ${idx+1} / ${total}`,{sz:3.2,a:'end',ff:RAL,f:'#555'})+T(9,13.2,pg.title,{sz:3.2,a:'start',ff:RAL,f:'#555',i:1});
  body+=L(9,14.2,W-9,14.2,{s:'#999',w:.2});
  body+=T(W/2,H-4,'PRINT AT 100 % (Actual size – do not “fit to page”)   |   ——— cut line     - - - fold line     grey tab = glue',{sz:2.4,f:'#777',ff:RAL});
  for(const it of pg.items){
    body+=it.o.clip?`<svg x="${f(it.x)}" y="${f(it.y)}" width="${it.o.w}" height="${it.o.h}" viewBox="0 0 ${it.o.w} ${it.o.h}" overflow="hidden">${it.o.svg}</svg><g transform="translate(${f(it.x)},${f(it.y)})">`:`<g transform="translate(${f(it.x)},${f(it.y)})">${it.o.svg}`;
    if(it.name)body+=T(0,it.o.h+3.6,`${it.name}  –  ${it.dim}${it.qty>1?'  ×'+it.qty:''}`,{sz:2.5,a:'start',f:'#333',ff:RAL});
    body+='</g>';
  }
  body+='</svg></div>';
  return body;
}
function cover(rows){
  const W=210,H=297;
  let s=`<svg width="${W}mm" height="${H}mm" viewBox="0 0 ${W} ${H}" style="position:absolute;left:0;top:0">`;
  s+=R(0,0,W,38,{f:'url(#gNavy)'})+T(W/2,17,'EVOLUTION OF COMPUTER SCIENCE',{sz:9,f:'#fff',b:1,ff:RAL,ls:.3})+T(W/2,26,'From Numbers to Neural Networks  •  DIY Cut-out Kit',{sz:4.6,f:'#9fd8ff',ff:RAL})+T(W/2,33,'Actual-size printable templates for the 46 × 30 cm project model',{sz:3,f:'#cfe3ff',ff:RAL});
  s+=T(12,48,'HOW TO USE',{sz:4.4,a:'start',b:1,ff:RAL});
  const ins=['1.  Print every sheet at 100 % scale (A4, "Actual size"). Use matt/photo paper at the highest quality setting.','2.  Check the 100 mm ruler below – it must measure exactly 10 cm. If not, switch off “fit to page”.','3.  Cut along the solid black lines. Fold along the dashed lines. Grey tabs are glue tabs.','4.  “front | back” pieces: cut both, glue back-to-back around thin card (1–2 mm); fold the foot tab and glue it to the platform.','5.  Box nets (books, tablet, phone, AI base): fold, glue tabs inside, stuff with card/foam for rigidity.','6.  Platform skins: wrap round a card/foam box of the same size; fascia halves overlap by 4 mm at the join.','7.  Stick the signboards on 3 mm foam-board, stack them with small gaps, and attach to the model.'];
  ins.forEach((t,i)=>s+=T(12,55+i*5.6,t,{sz:2.9,a:'start',ff:RAL,f:'#222'}));
  // ruler
  s+=T(12,98,'SCALE CHECK',{sz:3.4,a:'start',b:1,ff:RAL});
  s+=L(12,104,112,104,{s:'#000',w:.4});for(let i=0;i<=100;i+=1){s+=L(12+i,104,12+i,104-(i%10==0?4:i%5==0?3:2),{s:'#000',w:.25});if(i%10==0)s+=T(12+i,109,String(i/10),{sz:2.6,ff:RAL})}
  s+=T(116,105,'cm  (must be exactly 10 cm)',{sz:2.6,a:'start',ff:RAL,f:'#444'});
  // legend
  s+=T(140,98,'LEGEND',{sz:3.4,a:'start',b:1,ff:RAL});
  s+=L(140,103,160,103,{s:'#000',w:.3})+T(163,104,'cut',{sz:2.8,a:'start',ff:RAL})+L(140,108,160,108,{s:'#555',w:.25,d:'1.4 1'})+T(163,109,'fold',{sz:2.8,a:'start',ff:RAL})+R(140,111,20,3,{f:'#e8e8e8',s:'#000',w:.3})+T(163,113.4,'glue tab',{sz:2.8,a:'start',ff:RAL});
  // table
  s+=T(12,122,'PARTS LIST',{sz:4.4,a:'start',b:1,ff:RAL});
  const y0=126;s+=R(12,y0,186,5.5,{f:'#1f2d5a'})+T(14,y0+3.8,'Part',{sz:2.8,a:'start',f:'#fff',b:1,ff:RAL})+T(112,y0+3.8,'Size (W × H × D)',{sz:2.8,a:'start',f:'#fff',b:1,ff:RAL})+T(165,y0+3.8,'Sheet',{sz:2.8,a:'start',f:'#fff',b:1,ff:RAL});
  rows.forEach((r,i)=>{const y=y0+5.5+i*4.55;if(i%2)s+=R(12,y,186,4.55,{f:'#f1f3f9'});s+=T(14,y+3.2,r[0],{sz:2.6,a:'start',ff:RAL})+T(112,y+3.2,r[1],{sz:2.6,a:'start',ff:RAL})+T(168,y+3.2,String(r[2]),{sz:2.6,a:'middle',ff:RAL})});
  s+=T(W/2,H-6,'Dimensions are estimates from the project photo – check against your model before cutting.  Fairy lights & backdrop are not printed.',{sz:2.4,f:'#777',ff:RAL});
  s+='</svg>';return `<div style="position:absolute;left:0;top:0;width:${W}mm;height:${H}mm">${s}</div>`;
}
function buildAll(){
  const all=[];SHEETS.forEach(sh=>pack(sh).forEach(p=>all.push(p)));
  const total=all.length+1;
  const rows=[];all.forEach((p,i)=>p.items.forEach(it=>{if(it.name)rows.push([it.name,it.dim,i+2])}));
  rows.push(['Fairy lights (wire, ~100–140 cm)','not printed','–']);
  const out=[];out.push({w:210,h:297,html:cover(rows)});
  all.forEach((p,i)=>out.push({w:p.w,h:p.h,html:renderPage(p,i+1,total)}));
  return out;
}
