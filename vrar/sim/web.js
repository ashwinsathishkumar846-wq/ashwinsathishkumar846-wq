const sc=(location.hash||'#studio').slice(1), $=id=>document.getElementById(id);
const chrome=(title,url)=>`<div class="tabs"><div class="tab"><i class="fav"></i>${title}<span style="margin-left:auto">&#10005;</span></div><div class="tab o">New Tab</div><span class="wc"><i>&#8212;</i><i>&#10064;</i><i>&#10005;</i></span></div><div class="nav"><b>&#8592;</b><b>&#8594;</b><b>&#8635;</b><div class="url"><span>&#128274;</span> ${url}</div><b>&#9734;</b><b>&#8942;</b></div>`;
function line(w,h,pts,col,fill){const mx=Math.max(...pts.flat().map(p=>p)),n=pts.length;return ''}
function svgLine(arr,col,max,min,w,h){const dx=w/(arr.length-1);return arr.map((v,i)=>(i?'L':'M')+(i*dx).toFixed(1)+' '+(h-(v-min)/(max-min)*h).toFixed(1)).join(' ')}
let html='';
if(sc==='studio'){
 html=chrome('Assembly Work Instruction Studio','https://wi-studio.plant.local/projects/GB-220/editor')+
 `<div class="app"><div class="side"><div class="lg">&#9638; WI Studio</div><div class="i">Dashboard</div><div class="i a">Instruction Editor</div><div class="i">Part Library</div><div class="i">Operator Profiles</div><div class="i">Adaptation Rules</div><div class="i">Publish &amp; Devices</div></div>
 <div class="mainc"><div class="topb"><h2>Gearbox GB-220 &mdash; Station 04</h2><span class="pill">Draft v1.7</span><span style="margin-left:auto" class="btnl">Preview in AR</span><span class="btnp">Publish to Line 2</span></div>
 <div style="display:flex;gap:12px;padding:12px;flex:1;min-height:0">
  <div class="card" style="width:270px"><h4>Steps (9)</h4>
   ${['Pick housing and place on jig','Insert shaft into housing','Press bearing on shaft','Fix the bearing cover','Fit gear wheel and key','Apply grease (5 g)','Close side plate','Final torque check','Scan QR and release'].map((s,i)=>`<div class="step ${i===3?'sel':''}"><span class="num" style="${i<3?'background:#188038':''}">${i<3?'&#10003;':i+1}</span><div>${s}<br><small style="color:#778">${[8,12,15,25,18,12,20,10,5][i]*1} s &middot; ${['vision','vision','press','torque','vision','dispenser','vision','torque','scanner'][i]} check</small></div></div>`).join('')}
  </div>
  <div class="card" style="flex:1;display:flex;flex-direction:column"><h4>3D preview &mdash; Step 4: Fix the bearing cover <span class="pill" style="float:right">Anchor: Model Target (CAD)</span></h4>
   <div style="flex:1;position:relative;background:linear-gradient(#e9eef6,#cfd8e6);overflow:hidden"><div style="position:absolute;inset:20px 40px" id="m"></div>
   <div style="position:absolute;left:12px;top:12px;background:#fff;border:1px solid #c5d0df;border-radius:6px;padding:5px 9px;font-size:12px">&#9654; Play &nbsp; Orbit &nbsp; Wireframe</div>
   <div style="position:absolute;right:16px;bottom:12px;background:#0f2b4d;color:#fff;border-radius:6px;padding:6px 10px;font-size:12px">Arrow: bolts 3,4 &nbsp;|&nbsp; Ghost part: cover</div></div></div>
  <div class="card" style="width:290px;padding-bottom:10px"><h4>Step properties</h4><div style="padding:4px 14px">
   <div class="fld"><label>Title</label><div>Fix the bearing cover</div></div>
   <div class="fld"><label>Tool</label><div>Torque wrench TW-12 (IoT)</div></div>
   <div class="fld"><label>Torque / Fastener</label><div>12 N&middot;m &nbsp;|&nbsp; M6 x 20 &times; 4</div></div>
   <div class="fld"><label>Completion check</label><div>Torque signal + vision (cover seated)</div></div>
   <div class="fld"><label>Detail level shown</label><div class="seg"><i class="on">Novice</i><i>Skilled</i><i>Expert</i></div></div>
   <div class="fld"><label>Novice content</label><div style="font-size:12px">3D animation, 3 text lines, safety warning, voice help</div></div>
   <div class="fld"><label>Expert content</label><div style="font-size:12px">Torque value and bolt highlight only</div></div>
   <div class="fld"><label>Time target</label><div>25 s (adaptive &plusmn;20%)</div></div></div></div>
 </div></div></div>`;
} else {
 const ct=[96,94,95,92,90,91,88,86,87,84,82,83,80,79,78,77,76,74,73,72,71,70,70,69];
 html=chrome('Line 2 Supervisor Dashboard','https://wi-studio.plant.local/dashboard/line-2')+
 `<div class="app"><div class="side"><div class="lg">&#9638; WI Studio</div><div class="i a">Dashboard</div><div class="i">Instruction Editor</div><div class="i">Part Library</div><div class="i">Operator Profiles</div><div class="i">Adaptation Rules</div><div class="i">Publish &amp; Devices</div></div>
 <div class="mainc"><div class="topb"><h2>Line 2 &mdash; Gearbox Assembly (Shift A)</h2><span class="pill">Live &#9679;</span><span style="margin-left:auto" class="btnl">Last 4 weeks</span><span class="btnl">Export CSV</span></div>
 <div style="padding:12px;display:flex;flex-direction:column;gap:12px;flex:1">
  <div style="display:flex;gap:12px">
   <div class="card kpi"><small>Average cycle time</small><b>71 s</b><span class="ok">&#9660; 26% vs 96 s (paper)</span></div>
   <div class="card kpi"><small>Assembly errors / 1000 units</small><b>4.2</b><span class="ok">&#9660; 68% vs 13.1</span></div>
   <div class="card kpi"><small>First pass yield</small><b>98.4%</b><span class="ok">&#9650; 3.1 pts</span></div>
   <div class="card kpi"><small>New operator training time</small><b>1.5 days</b><span class="ok">&#9660; from 4 days</span></div>
  </div>
  <div style="display:flex;gap:12px;flex:1">
   <div class="card" style="flex:1.3"><h4>Average cycle time per day (s)</h4><svg viewBox="0 0 640 230" style="width:100%;height:230px"><g stroke="#e5eaf2">${[0,1,2,3,4].map(i=>`<line x1="40" x2="630" y1="${20+i*45}" y2="${20+i*45}"/>`).join('')}</g><g fill="#667" font-size="11">${[100,85,70,55,40].map((v,i)=>`<text x="6" y="${24+i*45}">${v}</text>`).join('')}</g>
    <g transform="translate(40,20)"><path d="${svgLine(ct,0,100,40,590,180)}" fill="none" stroke="#0b6bcb" stroke-width="3"/><line x1="0" x2="590" y1="${180-(96-40)/60*180}" y2="${180-(96-40)/60*180}" stroke="#c5221f" stroke-dasharray="6 4"/><text x="440" y="${180-(96-40)/60*180-6}" fill="#c5221f" font-size="11">paper baseline 96 s</text></g></svg></div>
   <div class="card" style="flex:1"><h4>Errors by step (last 4 weeks)</h4><svg viewBox="0 0 440 230" style="width:100%;height:230px">${[['S1',3],['S2',4],['S3',6],['S4',18],['S5',7],['S6',5],['S7',4],['S8',2],['S9',1]].map((d,i)=>`<rect x="${24+i*45}" y="${200-d[1]*9}" width="30" height="${d[1]*9}" fill="${d[0]==='S4'?'#0b6bcb':'#8fb8e8'}"/><text x="${28+i*45}" y="218" font-size="11" fill="#667">${d[0]}</text><text x="${30+i*45}" y="${194-d[1]*9}" font-size="11" fill="#334">${d[1]}</text>`).join('')}</svg></div>
  </div>
  <div class="card"><h4>Stations &mdash; live status</h4><table class="t"><tr><th>Station</th><th>Operator</th><th>Skill level</th><th>Current step</th><th>Cycle (s)</th><th>Errors today</th><th>Status</th></tr>
   <tr><td>ST-03 Housing</td><td>V. Anand</td><td>Expert</td><td>Step 6 / 8</td><td>58</td><td>0</td><td class="ok"><span class="st" style="background:#188038"></span>Running</td></tr>
   <tr><td>ST-04 Gearbox GB-220</td><td>S. Meena</td><td>Novice</td><td>Step 3 / 9 (held)</td><td>83</td><td>1</td><td class="bad"><span class="st" style="background:#c5221f"></span>Quality hold</td></tr>
   <tr><td>ST-05 Final test</td><td>R. Kumar</td><td>Expert</td><td>Step 2 / 5</td><td>64</td><td>0</td><td class="ok"><span class="st" style="background:#188038"></span>Running</td></tr>
   <tr><td>ST-06 Packing</td><td>A. Nisha</td><td>Skilled</td><td>Waiting part</td><td>71</td><td>0</td><td class="warn"><span class="st" style="background:#e8a500"></span>Waiting</td></tr></table></div>
 </div></div></div>`;
}
$('win').innerHTML=html; if($('m')) $('m').innerHTML=machineSVG({cover:true,done:[0,1]});
