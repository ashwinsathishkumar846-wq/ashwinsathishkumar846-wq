const $=(s)=>s;
const GLOBE=(c='#f2f2f2',s=34)=>`<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="${c}" stroke-width="1.5"><circle cx="12" cy="12" r="9.5"/><ellipse cx="12" cy="12" rx="4" ry="9.5"/><path d="M2.5 12h19M4.5 7h15M4.5 17h15"/></svg>`;
const XI=(c='#f2f2f2',s=26)=>`<svg width="${s}" height="${s}" viewBox="0 0 24 24" stroke="${c}" stroke-width="2.2" stroke-linecap="round"><path d="M5 5l14 14M19 5L5 19"/></svg>`;
const PLUS=(s=34)=>`<svg width="${s}" height="${s}" viewBox="0 0 24 24" stroke="#f2f2f2" stroke-width="2" stroke-linecap="round"><path d="M12 4v16M4 12h16"/></svg>`;
const CHEV=(s=30)=>`<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="#f2f2f2" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 9l7 7 7-7"/></svg>`;
const BACK=(s=40)=>`<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="#f2f2f2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12H5M11 5l-7 7 7 7"/></svg>`;
const RELOAD=(s=38)=>`<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="#f2f2f2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12a8 8 0 1 1-2.5-5.8"/><path d="M20 4v5h-5"/></svg>`;
const INFO=(s=34)=>`<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="#cfcfcf" stroke-width="1.7"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5" stroke-linecap="round"/></svg>`;
// Edge dark chrome: scale k applies to whole chrome
function edge(title,url,k=1,tabw=520,fav=GLOBE(),ex=0){
 return `<div class="edge" style="transform-origin:0 0;transform:scale(${k});width:${100/k}%"><div class="tabs"><div class="dd">${CHEV()}</div><div class="tab" style="width:${tabw}px">${fav}<span>${title}</span><span style="margin-left:auto">${XI()}</span></div><div class="abs" style="left:${78+tabw+34}px;top:18px">${PLUS()}</div></div><div class="tool" style="height:${62+ex/k}px"><div class="abs" style="left:18px;top:${10+ex/(2*k)}px">${BACK()}</div><div class="abs" style="left:90px;top:${12+ex/(2*k)}px">${RELOAD()}</div><div class="pill" style="top:${6+ex/(2*k)}px">${INFO()}<b style="color:#bbb;font-weight:600">File</b><span style="margin-left:10px">${url}</span></div></div></div>`;
}
const chromeH=(k,ex=0)=>134*k+ex;
// page wrapper with edge chrome and white content zoomed
function edgePage(o){const k=o.k||1,z=o.z||1;return edge(o.title,o.url,k,o.tabw||520,GLOBE(),o.ex||0)+`<div class="abs" style="left:0;top:${chromeH(k,o.ex||0)-2}px;right:0;bottom:0;background:#fff"><div style="zoom:${z};padding:${o.pad||'20px'}">${o.body}</div></div>`}
const FORMFONT='font-family:Arial,"Liberation Sans",sans-serif';
const SC={};
const mk=(n,w,h,dsf,fn)=>SC['i'+n]={w,h,dsf,html:fn};

// ---- 38 terminal
const term=(lines)=>`<div class="abs mono" style="left:6px;top:6px;right:0;bottom:0;background:#0c0c0c;color:#f0f0f0;font-size:30px;line-height:37.4px;white-space:pre;padding:0 4px;letter-spacing:-0.2px">${lines}</div>`;
mk(38,843,826,1,()=>term(`S:\\SEM 5\\WT LAB\\PROGRAM\\EXP7>node EXP7E.js
Enter employee name: AJAY I
Enter monthly salary: 100000
Enter employee name: BHAVNA S
Enter monthly salary: 100001
Enter employee name: ASHWINN
Enter monthly salary: 200000

Employee Details
-----------------------
Employee Name: AJAY I
Monthly Salary: ₹100000
Annual Salary: ₹1200000
-----------------------
Employee Name: BHAVNA S
Monthly Salary: ₹100001
Annual Salary: ₹1200012
-----------------------
Employee Name: ASHWINN
Monthly Salary: ₹200000
Annual Salary: ₹2400000
-----------------------`));
const SER="font-family:'Liberation Serif','Times New Roman',serif";
const tbl=(hl)=>`<div style="${SER}"><div style="font-size:49px;font-weight:700;margin:24px 0 40px 4px">Table Mouse Events</div><table style="border-collapse:collapse;width:100%;font-size:30px"><tr style="background:#b8d6e6"><th style="border:2px solid #222;height:76px;width:50%">Name</th><th style="border:2px solid #222">Department</th></tr>${[['Ajay','CSE'],['Bhavna','CA'],['Kabilesh','CHEM']].map((r,i)=>`<tr style="${hl&&i==0?'background:#8c8c8c':''}"><td style="border:2px solid #222;height:76px;padding-left:14px">${r[0]}</td><td style="border:2px solid #222;padding-left:14px">${r[1]}</td></tr>`).join('')}</table></div>`;
mk(39,1066,654,1,()=>edgePage({title:'Table Mouse Events',url:'S:/SEM%205/WT%20LAB/PROGRAM/EXP%208/exp8a.html',k:1.0,ex:22,tabw:520,body:tbl(false),pad:'8px 20px 0 22px'}));
mk(40,1078,658,1,()=>edgePage({title:'Table Mouse Events',url:'S:/SEM%205/WT%20LAB/PROGRAM/EXP%208/exp8a.html',k:1.0,ex:22,tabw:520,body:tbl(true),pad:'8px 26px 0 22px'}));
const sf=(msg)=>`<div style="padding:92px 0 0 62px;${FORMFONT}"><div style="font-size:46px;font-weight:700;margin-bottom:30px">Simple Form</div><div style="display:flex;gap:8px;align-items:center"><div style="width:372px;height:78px;border:3px solid #2a4a9a;background:#e8f0fe;padding:0 20px;font-size:23px;line-height:72px">Ajay I</div><div style="width:118px;height:78px;border:1px solid #767676;background:#efefef;border-radius:5px;font-size:23px;text-align:center;line-height:76px">Submit</div></div>${msg?`<div style="font-size:27px;font-weight:700;margin-top:32px">You entered: Ajay I</div>`:''}</div>`;
mk(44,932,512,1,()=>edgePage({title:'Simple Form',url:'S:/SEM%205/WT%20LAB/PROGRAM/EXP%208/exp8d',k:1.0,ex:52,tabw:520,body:sf(false),pad:'0'}));
mk(45,804,582,1,()=>edgePage({title:'Simple Form',url:'S:/SEM%205/WT%20LAB/PROGRAM/EXP%208/exp8d.html',k:1.0,ex:46,tabw:520,body:sf(true),pad:'0'}));
const ml=(w)=>`<div style="padding:84px 0 0 66px;${FORMFONT}"><div style="font-size:49px;font-weight:700;margin-bottom:36px;white-space:nowrap">Mini Login System</div><div style="width:368px;height:76px;border:2px solid #888;border-radius:5px;background:#e8f0fe;padding:0 24px;font-size:26px;line-height:72px;margin-bottom:22px">ajay</div><div style="width:368px;height:76px;border:4px solid #000;border-radius:8px;padding:0 22px;margin-bottom:22px;display:flex;justify-content:space-between;align-items:center"><span style="letter-spacing:3px;font-size:26px">••••••</span><svg width="36" height="30" viewBox="0 0 24 20" fill="none" stroke="#111" stroke-width="2"><path d="M1 10C4 4 8 2 12 2s8 2 11 8c-3 6-7 8-11 8S4 16 1 10z"/><circle cx="12" cy="10" r="3.5"/></svg></div><div style="width:122px;height:76px;border:1px solid #767676;background:#efefef;border-radius:5px;font-size:26px;text-align:center;line-height:74px">Login</div>${w?`<div style="font-size:36px;font-weight:700;margin-top:40px">Welcome</div>`:''}</div>`;
mk(46,714,670,1,()=>edgePage({title:'Mini Login System',url:'S:/SEM%205/WT%20LAB/PROGRAM',k:1.0,ex:28,tabw:520,body:ml(false),pad:'0'}));
mk(47,642,738,1,()=>edgePage({title:'Mini Login System',url:'S:/SEM%205/WT%20LAB/PRO',k:1.0,ex:28,tabw:520,body:ml(true),pad:'0'}));
const rf=(ok,top)=>`<div style="padding:${top}px 0 0 62px;${FORMFONT}"><div style="font-size:52px;font-weight:700;margin-bottom:30px">Student Registration Form</div><div style="width:880px;border:4px solid #111;padding:34px 34px 36px"><div style="font-size:30px;margin-bottom:8px">Name:</div><div style="height:76px;border:1.5px solid #777;background:#e8f0fe;padding:0 20px;font-size:27px;line-height:73px;margin-bottom:8px">Ajay I</div><div style="font-size:30px;margin-bottom:8px">Email:</div><div style="height:76px;border:1.5px solid #777;background:#e8f0fe;padding:0 20px;font-size:27px;line-height:73px;margin-bottom:8px">ajay.2401007@srec.ac.in</div><div style="font-size:30px;margin-bottom:8px">Mobile Number:</div><div style="height:76px;border:1.5px solid #777;padding:0 20px;font-size:27px;line-height:73px;margin-bottom:8px">9025467813</div><div style="font-size:30px;margin-bottom:8px">Password:</div><div style="height:76px;border:4px solid #000;padding:0 20px;font-size:27px;line-height:66px;margin-bottom:30px;letter-spacing:2px">•••••••••••</div><div style="width:150px;height:68px;border:1px solid #767676;background:#e6e6e6;border-radius:4px;font-size:27px;text-align:center;line-height:66px">Register</div></div>${ok?`<div style="font-size:29px;font-weight:700;color:#2e7d1c;margin-top:40px">Registration Successful!</div>`:''}</div>`;
mk(50,1108,1168,1,()=>edgePage({title:'Student Registration Form',url:'S:/SEM%205/WT%20LAB/PROGRAM/EXP%209/exp9.html',k:1.0,ex:34,tabw:560,body:rf(false,70),pad:'0'}));
mk(51,1092,1000,1,()=>`<div class="abs" style="inset:0;background:#fff">${rf(true,40)}</div>`);
