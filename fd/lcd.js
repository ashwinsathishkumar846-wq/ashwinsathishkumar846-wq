// 5x7 font, columns (bit0 = top row)
const F5={' ':'0000000000','!':'00005F0000','-':'0808080808','.':'0000606000','/':'2010080402',':':'0000140000','*':'2A1C7F1C2A','_':'4040404040',
'0':'3E5149453E','1':'00427F4000','2':'7249494946','3':'2141494D33','4':'1814127F10','5':'2745454539','6':'3C4A494931','7':'4121110907','8':'3649494936','9':'464949291E',
'A':'7C1211127C','B':'7F49494936','C':'3E41414122','D':'7F4141413E','E':'7F49494941','F':'7F09090901','G':'3E4151 73'.replace(' ',''),'H':'7F0808087F','I':'00417F4100','J':'2040413F01','K':'7F08142241','L':'7F40404040','M':'7F021C027F','N':'7F0408107F','O':'3E4141413E','P':'7F09090906','Q':'3E4151215E','R':'7F09192946','S':'2649494932','T':'03017F0103','U':'3F4040403F','V':'1F2040201F','W':'3F4038403F','X':'6314081463','Y':'0304780403','Z':'6159494D43'};
function glyph(ch){const h=F5[ch]||F5[' '];const cols=[];for(let i=0;i<5;i++)cols.push(parseInt(h.substr(i*2,2),16));return cols}
// returns svg string. mode 'module' (photo style) or 'isis'
function lcdSVG(l1,l2,o={}){
 const mode=o.mode||'module', P=o.px||5.2, G=0.9; // pixel size
 const cw=5*P+4*0+ (P*1.0), ch=8*P+ P*1.4; // cell pitch
 const cellW=6*P+0.8, cellH=8*P+1.2;
 const gw=16*cellW+ P*1.2, gh=2*cellH+ P*2.6;
 let s='';
 const lit=mode==='isis'?'#1c2a05':'#14210a', unlit=mode==='isis'?'rgba(60,80,10,.16)':'rgba(30,60,0,.13)';
 const bg=mode==='isis'?'#a8bd2c':null;
 let body='';
 [l1,l2].forEach((line,r)=>{
  const txt=(line+'                ').slice(0,16);
  for(let c=0;c<16;c++){
   const cols=glyph(txt[c]);
   const ox=P*0.9+c*cellW, oy=P*1.1+r*(cellH+P*0.6);
   for(let x=0;x<5;x++)for(let y=0;y<8;y++){
     const on=y<7&&((cols[x]>>y)&1);
     const px=ox+x*P*1.0, py=oy+y*P*1.0;
     if(y===7 && !on){ body+=`<rect x="${px.toFixed(2)}" y="${py.toFixed(2)}" width="${(P-G*0.6).toFixed(2)}" height="${(P-G*0.6).toFixed(2)}" fill="${unlit}"/>`; continue}
     body+=`<rect x="${px.toFixed(2)}" y="${py.toFixed(2)}" width="${(P-G*0.6).toFixed(2)}" height="${(P-G*0.6).toFixed(2)}" fill="${on?lit:unlit}"${on?` opacity=".93"`:''}/>`;
   }
  }
 });
 if(mode==='isis'){
  return {w:gw,h:gh,svg:`<g><rect width="${gw}" height="${gh}" fill="${bg}"/>${body}</g>`};
 }
 // module (photo-like)
 const padL=86,padT=58,W=gw+padL*2-40+0, H=gh+padT*2+40; // board 
 const bw=gw+120, bh=gh+110; // total board
 const gx=60, gy=52; // glass offset in board
 let o2=`<svg xmlns="http://www.w3.org/2000/svg" width="${bw}" height="${bh+4}" viewBox="0 0 ${bw} ${bh+4}">
 <defs>
  <linearGradient id="pcb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1f7a3a"/><stop offset="1" stop-color="#145a2a"/></linearGradient>
  <linearGradient id="bez" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfe3e8"/><stop offset=".5" stop-color="#b8bec7"/><stop offset="1" stop-color="#8d949d"/></linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c6e04a"/><stop offset=".55" stop-color="#b3d03a"/><stop offset="1" stop-color="#9dbb2c"/></linearGradient>
  <radialGradient id="bl" cx=".5" cy=".5" r=".75"><stop offset="0" stop-color="#e3f56a" stop-opacity=".55"/><stop offset="1" stop-color="#7a9a14" stop-opacity=".0"/></radialGradient>
  <linearGradient id="refl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <radialGradient id="hole" cx=".4" cy=".4" r=".7"><stop offset="0" stop-color="#e9e0b0"/><stop offset="1" stop-color="#9d8f4c"/></radialGradient>
  <filter id="sh" x="-5%" y="-5%" width="110%" height="115%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-opacity=".45"/></filter>
 </defs>
 <rect x="2" y="2" width="${bw-4}" height="${bh-4}" rx="5" fill="url(#pcb)" stroke="#0b3d1b" stroke-width="2" filter="url(#sh)"/>`;
 // PCB texture traces
 for(let i=0;i<9;i++) o2+=`<path d="M${8+i*3} ${bh-6} V${bh-30-(i%3)*5} H${40+i*28}" fill="none" stroke="#2a9a50" stroke-opacity=".35" stroke-width="1.4"/>`;
 // mounting holes
 [[16,16],[bw-16,16],[16,bh-16],[bw-16,bh-16]].forEach(([x,y])=>o2+=`<circle cx="${x}" cy="${y}" r="7" fill="url(#hole)" stroke="#6c6030"/><circle cx="${x}" cy="${y}" r="3.6" fill="#0d3a1a"/>`);
 // bezel
 const bx=gx-14,by=gy-14,bW=gw+28,bH=gh+28+4;
 o2+=`<rect x="${bx}" y="${by}" width="${bW}" height="${bH}" rx="3" fill="url(#bez)" stroke="#5d646d"/>`;
 o2+=`<rect x="${bx+5}" y="${by+5}" width="${bW-10}" height="${bH-10}" fill="#2b2f33"/>`;
 o2+=`<rect x="${gx-5}" y="${gy-5}" width="${gw+10}" height="${gh+14}" fill="url(#glass)" stroke="#51661a"/>`;
 o2+=`<rect x="${gx-5}" y="${gy-5}" width="${gw+10}" height="${gh+14}" fill="url(#bl)"/>`;
 o2+=`<g transform="translate(${gx},${gy+2})">${body}</g>`;
 o2+=`<path d="M${gx-5} ${gy-5} h${(gw+10)*0.55} l-${(gw+10)*0.25} ${gh+14} h-${(gw+10)*0.3}z" fill="url(#refl)"/>`;
 // screws on bezel
 [[bx+10,by+bH/2]].forEach(()=>{});
 // header pins
 for(let i=0;i<16;i++){const x=bx+12+i*((bW-24)/15), y=bh-30;
   o2+=`<circle cx="${x}" cy="${y}" r="5.2" fill="#c9a23a" stroke="#6a5214"/><circle cx="${x}" cy="${y}" r="2.1" fill="#233"/>`;
   o2+=`<text x="${x}" y="${y+16}" font-size="7.5" fill="#d8efe0" text-anchor="middle" font-family="DejaVu Sans,sans-serif">${['VSS','VDD','VO','RS','RW','E','D0','D1','D2','D3','D4','D5','D6','D7','A','K'][i]}</text>`;}
 o2+=`<text x="${bw-34}" y="21" font-size="9" fill="#cfe9d8" text-anchor="end" font-family="DejaVu Sans,sans-serif" font-weight="bold">LCD 16x2 · HD44780</text>`;
 o2+='</svg>';
 return {w:bw,h:bh+4,svg:o2,full:true};
}
