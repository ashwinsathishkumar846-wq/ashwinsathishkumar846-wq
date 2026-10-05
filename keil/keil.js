const A=(x,y,h,st='')=>`<div class="a" style="left:${x}px;top:${y}px;${st}">${h}</div>`;
const T=(x,y,t,st='')=>`<div class="t" style="left:${x}px;top:${y}px;${st}">${t}</div>`;
const LOGO='logo.png';
const ico=(k,s=16)=>{const P={
new:`<path d="M3 1h7l3 3v11H3z" fill="#fff" stroke="#6b7f99"/><path d="M10 1v3h3" fill="#dde5ef" stroke="#6b7f99"/>`,
open:`<path d="M1 4h5l1 1h7v9H1z" fill="#f2c94c" stroke="#a17a10"/><path d="M1 7h14l-2 7H1z" fill="#f9dd7a" stroke="#a17a10"/>`,
save:`<rect x="2" y="2" width="12" height="12" fill="#3d6fc2" stroke="#1c428a"/><rect x="4" y="2" width="8" height="5" fill="#eef3fb"/><rect x="5" y="9" width="6" height="5" fill="#c9d6ea"/>`,
saveall:`<rect x="1" y="4" width="10" height="10" fill="#3d6fc2" stroke="#1c428a"/><rect x="5" y="1" width="10" height="10" fill="#3d6fc2" stroke="#1c428a"/><rect x="7" y="1" width="6" height="4" fill="#eef3fb"/>`,
cut:`<path d="M5 1l5 9M11 1L6 10" stroke="#667" stroke-width="1.4"/><circle cx="5" cy="12" r="2.2" fill="none" stroke="#c0392b" stroke-width="1.5"/><circle cx="11" cy="12" r="2.2" fill="none" stroke="#c0392b" stroke-width="1.5"/>`,
copy:`<rect x="2" y="1" width="8" height="10" fill="#fff" stroke="#6b7f99"/><rect x="6" y="5" width="8" height="10" fill="#fff" stroke="#44566e"/><path d="M8 8h4M8 10h4M8 12h3" stroke="#9fb0c5"/>`,
paste:`<rect x="2" y="3" width="10" height="12" fill="#d9b36a" stroke="#8a6a24"/><rect x="5" y="1" width="4" height="3" fill="#7d8591"/><rect x="8" y="7" width="7" height="8" fill="#fff" stroke="#44566e"/>`,
undo:`<path d="M4 6h6a3.5 3.5 0 010 7H6" fill="none" stroke="#2e6bd1" stroke-width="2"/><path d="M1 6l4-4v8z" fill="#2e6bd1"/>`,
redo:`<path d="M12 6H6a3.5 3.5 0 000 7h4" fill="none" stroke="#9aa7b9" stroke-width="2"/><path d="M15 6l-4-4v8z" fill="#9aa7b9"/>`,
back:`<path d="M14 8H3M7 3L2 8l5 5" fill="none" stroke="#9aa7b9" stroke-width="2"/>`,
fwd:`<path d="M2 8h11M9 3l5 5-5 5" fill="none" stroke="#9aa7b9" stroke-width="2"/>`,
flag:`<path d="M4 1v14" stroke="#555" stroke-width="1.5"/><path d="M4 2h9l-2 3 2 3H4z" fill="#2e86de"/>`,
flagg:`<path d="M4 1v14" stroke="#999" stroke-width="1.5"/><path d="M4 2h9l-2 3 2 3H4z" fill="#b8c2d0"/>`,
indent:`<path d="M2 3h12M7 6h7M7 9h7M2 12h12" stroke="#444"/><path d="M2 6l3 1.5L2 9z" fill="#2e86de"/>`,
uind:`<path d="M2 3h12M7 6h7M7 9h7M2 12h12" stroke="#444"/><path d="M5 6L2 7.5 5 9z" fill="#2e86de"/>`,
cmt:`<path d="M2 3h12M2 6h12M2 9h12M2 12h12" stroke="#444"/><path d="M1 5l12 6" stroke="#d33"/>`,
ucmt:`<path d="M2 3h12M2 6h12M2 9h12M2 12h12" stroke="#999"/><path d="M1 11l12-6" stroke="#aaa"/>`,
folderb:`<path d="M1 4h5l1 1h7v9H1z" fill="#f2c94c" stroke="#a17a10"/><rect x="9" y="7" width="6" height="6" fill="#3d6fc2"/>`,
translate:`<path d="M3 1h7l3 3v11H3z" fill="#fff" stroke="#6b7f99"/><path d="M5 9h5M8 6l3 3-3 3" fill="none" stroke="#2e8b3d" stroke-width="1.6"/>`,
build:`<rect x="1" y="2" width="9" height="11" fill="#fff" stroke="#6b7f99"/><path d="M5 8h8M10 5l4 3-4 3" fill="none" stroke="#2e8b3d" stroke-width="1.8"/>`,
batch:`<rect x="1" y="1" width="8" height="7" fill="#fff" stroke="#6b7f99"/><rect x="5" y="6" width="8" height="7" fill="#fff" stroke="#6b7f99"/><path d="M8 11h7" stroke="#2e8b3d" stroke-width="2"/>`,
stop:`<circle cx="8" cy="8" r="6.5" fill="#fff" stroke="#c0392b" stroke-width="1.5"/><rect x="5" y="5" width="6" height="6" fill="#c0392b"/>`,
load:`<rect x="2" y="5" width="12" height="8" fill="#eee" stroke="#667"/><path d="M8 1v7M5 5l3 3 3-3" fill="none" stroke="#2e6bd1" stroke-width="1.6"/><text x="3" y="12" font-size="4" fill="#444">LOAD</text>`,
wand:`<path d="M3 13L11 5" stroke="#555" stroke-width="2"/><path d="M12 2l1 2 2 1-2 1-1 2-1-2-2-1 2-1z" fill="#e6b800"/><circle cx="5" cy="11" r="3" fill="none" stroke="#2e6bd1" stroke-width="1.5"/>`,
comp:`<rect x="1" y="6" width="5" height="5" fill="#d5382d"/><rect x="6" y="2" width="5" height="5" fill="#3ba04a"/><rect x="9" y="8" width="5" height="5" fill="#2f6fd0"/>`,
dbg:`<path d="M1 2h14v9H1z" fill="#fff" stroke="#6b7f99"/><path d="M4 5l3 2-3 2" fill="none" stroke="#c0392b" stroke-width="1.6"/><circle cx="12" cy="13" r="2.5" fill="#c0392b"/>`,
bp:`<circle cx="8" cy="8" r="5.5" fill="#d9262c"/>`,
bpo:`<circle cx="8" cy="8" r="5" fill="#fff" stroke="#999" stroke-width="1.5"/>`,
bpx:`<circle cx="8" cy="8" r="5.5" fill="#fff" stroke="#d9262c" stroke-width="1.8"/><path d="M4 12L12 4" stroke="#d9262c" stroke-width="1.8"/>`,
bpa:`<circle cx="7" cy="9" r="5" fill="#d9262c"/><circle cx="11" cy="5" r="3" fill="#f5b800"/>`,
view:`<rect x="1" y="2" width="14" height="12" fill="#fff" stroke="#444"/><rect x="3" y="4" width="4" height="4" fill="#2e86de"/><path d="M9 5h4M9 8h4M3 11h10" stroke="#777"/>`,
wrench:`<path d="M3 13l6-6" stroke="#666" stroke-width="2.4"/><circle cx="11" cy="5" r="3.2" fill="#8a8f98"/><path d="M12.5 3.5l-2 2" stroke="#fff" stroke-width="1.2"/>`,
file:`<path d="M3 1h7l3 3v11H3z" fill="#fff" stroke="#5c7090"/><path d="M10 1v3h3" fill="#dce4ef" stroke="#5c7090"/><path d="M5 8h6M5 10h6M5 12h4" stroke="#7b97bd"/>`,
folder:`<path d="M1 3h5l1 1.5h8V13H1z" fill="#f2c94c" stroke="#a17a10"/>`,
folderopen:`<path d="M1 3h5l1 1.5h7V7H1z" fill="#f2c94c" stroke="#a17a10"/><path d="M1 7h14l-2 6H1z" fill="#f9dd7a" stroke="#a17a10"/>`,
target:`<rect x="1" y="2" width="14" height="12" rx="1" fill="#dfe8f5" stroke="#4c6a96"/><circle cx="8" cy="8" r="3.5" fill="none" stroke="#2e6bd1" stroke-width="1.5"/><circle cx="8" cy="8" r="1" fill="#2e6bd1"/>`,
proj:`<rect x="1.5" y="1.5" width="13" height="13" fill="#e8eef7" stroke="#4c6a96"/><rect x="3.5" y="3.5" width="4" height="4" fill="#3ba04a"/><rect x="8.5" y="3.5" width="4" height="4" fill="#d5382d"/><rect x="3.5" y="8.5" width="4" height="4" fill="#2f6fd0"/><rect x="8.5" y="8.5" width="4" height="4" fill="#f5b800"/>`,
pin:`<path d="M5 2h6M6 2v5L4 9h8L10 7V2M8 9v5" fill="none" stroke="#223" stroke-width="1.2"/>`,
xred:`<rect x="1" y="1" width="14" height="14" fill="#d9322e"/><path d="M4.5 4.5l7 7M11.5 4.5l-7 7" stroke="#fff" stroke-width="1.8"/>`,
};return `<svg width="${s}" height="${s}" viewBox="0 0 16 16" style="display:block">${P[k]||''}</svg>`};
const I=(k,x,y,s=16)=>A(x,y,ico(k,s));
const SEP=(x,y,h=20)=>A(x,y,'',`width:1px;height:${h}px;background:#c8c8c8`);
const combo=(x,y,w,txt)=>A(x,y,`<div style="padding:0 0 0 4px;line-height:18px;font-size:12px">${txt}</div><div style="position:absolute;right:0;top:0;width:17px;height:18px;border-left:1px solid #c8c8c8"><svg width="17" height="18"><path d="M5 7l3.5 4 3.5-4z" fill="#333"/></svg></div>`,`width:${w}px;height:20px;border:1px solid #7a7a7a;background:#fff;`);
function chrome(o){ // title: window title, project:{tree}, tabs, code, build, status
 let h='';
 h+=A(0,0,'','width:1920px;height:28px;background:#fff');
 h+=A(6,6,`<img src="${LOGO}" width="16" height="16" style="display:block">`);
 h+=T(26,8,o.title,'font-size:12px');
 h+=A(1730,0,`<svg width="190" height="28"><path d="M17 14h12" stroke="#000" stroke-width="1"/><rect x="73" y="9" width="10" height="10" fill="none" stroke="#000"/><path d="M75 9V7h10v10h-2" fill="none" stroke="#000"/><path d="M127 9l11 11M138 9l-11 11" stroke="#000" stroke-width="1.1"/></svg>`);
 // menu
 h+=A(0,28,'','width:1920px;height:22px;background:#fff;border-bottom:1px solid #e5e5e5');
 let mx=[['File',6],['Edit',44],['View',78],['Project',122],['Flash',178],['Debug',226],['Peripherals',272],['Tools',350],['SVCS',394],['Window',440],['Help',492]];
 mx.forEach(([m,x])=>h+=T(x+8,34,m));
 // toolbar rows
 h+=A(0,50,'','width:1920px;height:56px;background:#fdfdfd;border-bottom:1px solid #d8d8d8');
 let x=6; const t1=[['new',0],['open',0],['save',0],['saveall',0],'|',['cut',0],['copy',0],['paste',0],'|',['undo',0],['redo',0],'|',['back',0],['fwd',0],'|',['flag',0],['flagg',0],['flagg',0],['flagg',0],'|',['indent',0],['uind',0],['cmt',0],['ucmt',0],'|',['folderb',0]];
 t1.forEach(it=>{ if(it==='|'){h+=SEP(x+2,54,22);x+=8;} else {h+=I(it[0],x,56);x+=25;}});
 h+=combo(580,54,128,'')+I('view',716,56)+I('wrench',742,56);
 h+=SEP(767,54,22);
 h+=I('dbg',776,56)+A(795,63,'<svg width="8" height="6"><path d="M1 1l3 3 3-3z" fill="#333"/></svg>');
 h+=SEP(814,54,22)+I('bp',822,56)+I('bpo',847,56)+I('bpx',872,56)+I('bpa',897,56)+A(916,63,'<svg width="8" height="6"><path d="M1 1l3 3 3-3z" fill="#333"/></svg>');
 h+=SEP(940,54,22)+A(944,54,'',`width:36px;height:22px;background:#cfe8ff;border:1px solid #6bb0e8`)+I('view',950,57)+A(968,63,'<svg width="8" height="6"><path d="M1 1l3 3 3-3z" fill="#333"/></svg>')+I('wrench',990,56);
 // row2
 x=6; const t2=[['translate'],['build'],['batch'],['load'],'|',['stop'],'|'];
 h+=I('translate',6,81)+I('build',31,81)+I('batch',56,81)+A(76,88,'<svg width="8" height="6"><path d="M1 1l3 3 3-3z" fill="#333"/></svg>')+I('stop',96,81)+SEP(120,79,22)+I('load',130,81);
 h+=combo(184,79,152,'Target 1')+I('wand',342,81)+SEP(366,79,22)+I('comp',374,81)+I('comp',400,81)+I('comp',426,81)+I('comp',452,81);
 // project panel
 const PY=106, PH=o.bo?(o.boY-PY-4):910;
 h+=A(0,PY,'','width:252px;height:'+(1056-PY)+'px;background:#f0f0f0');
 h+=`<div class="hdr" style="left:0;top:${PY+4}px;width:250px">Project</div>`+A(214,PY+6,ico('pin',14))+A(232,PY+6,ico('xred',14));
 h+=A(0,PY+22,'','width:250px;height:'+(o.pH||620)+'px;background:#fff;border:1px solid #c8c8c8');
 if(o.tree) h+=o.tree;
 const pb=PY+22+(o.pH||620);
 h+=A(0,pb,'','width:250px;height:22px;background:#f0f0f0;border-bottom:1px solid #ccc');
 h+=A(2,pb+1,ico('proj',14))+T(18,pb+5,'Project','font-size:11.5px')+A(68,pb+1,'<div style="font-size:11px;color:#555;line-height:14px">{ } Functions &nbsp;&nbsp;0▪ Templates</div>');
 // status bar
 h+=A(0,1058,'','width:1920px;height:22px;background:#f0f0f0;border-top:1px solid #dcdcdc');
 h+=T(1425,1064,'Simulation')+T(1650,1064,o.pos||'L:1 C:1')+A(1760,1062,'<span style="color:#8a8a8a;font-size:10.5px;letter-spacing:.2px;white-space:nowrap">CAP &nbsp;NUM &nbsp;SCRL &nbsp;OVR &nbsp;R/W</span>');
 return h;
}
function tree(rows){ // rows: [indent,kind,label,expand]
 let h='',y=134;
 rows.forEach(r=>{const [ind,kind,label,ex]=r;const x=6+ind*20;
  if(ex) h+=A(x,y+3,`<svg width="9" height="9"><rect x=".5" y=".5" width="8" height="8" fill="#fff" stroke="#8b8b8b"/><path d="M2 4.5h5${ex==='+'?'M4.5 2v5':''}" stroke="#333"/></svg>`);
  h+=A(x+13,y,ico(kind,16))+T(x+33,y+3,label);
  y+=21;});
 return h;
}
const TREE_EMPTY=''; 
const treeFull=(files,startOpen=true)=>tree([[0,'proj','Project: Remote_Data_Logger','-'],[1,'target','Target 1','-'],[2,'folderopen','Source Group 1','-'],...files.map(f=>[3,'file',f,0])]);
// ===== editor =====
function editor(o){ // tabs:[['Startup.s',false],['main.c',true]], lines:[html...], hl line idx, bottom
 const EX=258,EY=106,EW=1654,EB=o.bottom;
 let h=A(EX-2,EY,'',`width:${EW+4}px;height:${EB-EY}px;background:#fff;border:2px solid ${o.focus===false?'#d0d0d0':'#f0d25a'}`);
 h+=A(EX,EY+2,'',`width:${EW}px;height:24px;background:#f0f0f0;border-bottom:1px solid #c8c8c8`);
 let tx=EX+6;
 o.tabs.forEach(([n,on])=>{const w=n.length*7.4+38;h+=`<div class="tab ${on?'on':''}" style="left:${tx}px;top:${EY+5}px;width:${w}px"><span style="position:absolute;left:4px;top:1px">${ico('file',16)}</span>${n}</div>`;tx+=w+3;});
 h+=A(EX+EW-34,EY+10,'<svg width="12" height="8"><path d="M1 1l5 5 5-5z" fill="#222"/></svg>')+A(EX+EW-16,EY+8,'<svg width="10" height="10"><path d="M1 1l8 8M9 1L1 9" stroke="#222" stroke-width="1.5"/></svg>');
 const gx=EX+2,gy=EY+28;
 h+=A(gx,gy,'',`width:62px;height:${EB-gy-18}px;background:#ececec;border-right:1px solid #d6d6d6`);
 const LH=16.7;
 (o.lines||[]).forEach((ln,i)=>{const y=gy+4+i*LH;
  if(o.hl===i) h+=A(gx+63,y-1,'',`width:${EW-66}px;height:${LH}px;background:#e4f8e4`);
  h+=`<div class="t mono" style="left:${gx}px;top:${y}px;width:56px;text-align:right;font-size:13px;color:#333">${i+1}</div>`;
  h+=`<div class="t mono" style="left:${gx+69}px;top:${y}px;font-size:13px">${ln}</div>`;});
 // scrollbars
 h+=A(EX+2,EB-18,'',`width:${EW-4}px;height:16px;background:#f0f0f0`)+A(EX+22,EB-14,'',`width:${o.hs||1100}px;height:8px;background:#c6c6c6;border-radius:1px`);
 return h;
}
function buildOut(o){ // y top, lines
 const y=o.y; let h=`<div class="hdr" style="left:0;top:${y}px;width:1920px">Build Output</div>`+A(1868,y+2,ico('pin',14))+A(1890,y+2,ico('xred',14));
 h+=A(0,y+18,'',`width:1920px;height:${1056-y-18}px;background:#fff;border:1px solid #c8c8c8`);
 (o.lines||[]).forEach((l,i)=>{h+=`<div class="t mono" style="left:6px;top:${y+26+i*15}px;font-size:12px;color:#000">${l}</div>`});
 h+=A(1902,y+18,'',`width:16px;height:${1056-y-34}px;background:#f0f0f0`)+A(1903,y+19,ico('xred',0))+A(0,1040,'',`width:1902px;height:16px;background:#f0f0f0`);
 return h;
}
// code tokenizer
function hl(src){
 const KW=/\b(void|unsigned|int|char|volatile|while|if|else|for|return|static|const|__irq|sbit|define|include)\b/g;
 return src.map(l=>{
  let e=l.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  let cm='';const ci=e.indexOf('/*'); if(ci>=0){cm=e.slice(ci);e=e.slice(0,ci);}
  e=e.replace(/(0x[0-9A-Fa-f]+[uUlL]*|\b\d+[uUlL]*\b)/g,'<span class="n">$1</span>').replace(/^(\s*)(#\w+)/,'$1<span class="k">$2</span>').replace(KW,m=>'<span class="k">'+m+'</span>');
  e=e.replace(/(&lt;[\w.]+&gt;)/,'<span class="s">$1</span>');
  return e+(cm?`<span class="c">${cm}</span>`:'');
 });
}
// ===== dialogs =====
function dlg(x,y,w,h,title,body){return `<div class="dlg" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px"><div class="dt" style="width:${w-2}px"></div>`+A(x+0,0,'')+'';}
function dialog(x,y,w,h,title,body){
 return A(x,y,`<div class="dt">${title}</div><img src="${LOGO}" width="16" height="16" style="position:absolute;left:9px;top:7px"><div style="position:absolute;right:0;top:0;width:46px;height:30px"><svg width="46" height="30"><path d="M18 10l10 10M28 10L18 20" stroke="#000" stroke-width="1.1"/></svg></div>${body}`,`width:${w}px;height:${h}px;background:#f0f0f0;border:1px solid #6f7b8b;box-shadow:0 8px 30px rgba(0,0,0,.4)`);
}
const rel=(x,y,h,st='')=>`<div style="position:absolute;left:${x}px;top:${y}px;white-space:nowrap;${st}">${h}</div>`;
const rbtn=(x,y,w,t,def)=>`<div class="btn ${def?'def':''}" style="left:${x}px;top:${y}px;width:${w}px">${t}</div>`;
const rinp=(x,y,w,t,hh=20,st='')=>`<div class="inp" style="left:${x}px;top:${y}px;width:${w}px;height:${hh}px;${st}">${t}</div>`;
const rcb=(x,y,k,t,st='')=>`<div class="cb ${k?'k':''}" style="left:${x}px;top:${y}px"></div>`+rel(x+19,y-1,t,st);
const rrb=(x,y,k,t)=>`<div class="rb ${k?'k':''}" style="left:${x}px;top:${y}px"></div>`+rel(x+19,y-1,t);
const rcombo=(x,y,w,t)=>rinp(x,y,w,t)+`<div style="position:absolute;left:${x+w-18}px;top:${y+1}px;width:17px;height:18px;background:#e5e5e5;border-left:1px solid #adadad"><svg width="17" height="18"><path d="M4 7l4.5 4.5L13 7" fill="none" stroke="#444" stroke-width="1.3"/></svg></div>`;
