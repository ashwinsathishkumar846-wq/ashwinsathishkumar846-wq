const sc = (location.hash || '#novice').slice(1), $ = id => document.getElementById(id);
const done = sc === 'expert' ? [0, 1] : sc === 'error' ? [] : [0, 1];
$('mach').innerHTML = machineSVG({ cover: sc !== 'err0', done, part: sc === 'error' ? [740, 520] : null });
// bolt positions on screen (svg 920x520 -> div at 180,130 scale ~0.978)
const P = i => [[398, 253], [522, 253], [398, 377], [522, 377]][i];
const scr = i => { const b = P(i); return [180 + b[0] * 0.978 - 28, 130 + b[1] * 0.978 - 28]; };
let h = '';
h += '<div class="hud" style="left:26px;top:20px"><b>STATION 04 &bull; GEARBOX GB-220</b><br>Line 2 &nbsp;|&nbsp; Shift A &nbsp;|&nbsp; 10:42:18</div>';
h += '<div class="hud" style="right:26px;top:20px;text-align:right">Operator: <b>' + (sc === 'expert' ? 'R. Kumar' : 'S. Meena') + '</b><br>Skill level: <span class="tag ' + (sc === 'expert' ? 'g' : 'o') + '">' + (sc === 'expert' ? 'EXPERT' : 'NOVICE') + '</span> &nbsp;Tracking: <span style="color:#4fffb0">&#9679; locked</span></div>';
h += '<div class="reticle"></div>';
const ring = (i, cls, label) => { const p = scr(i); return '<div class="ring ' + cls + '" style="left:' + p[0] + 'px;top:' + p[1] + 'px">' + label + '</div>'; };
if (sc === 'novice') {
  h += ring(0, 'd', '&#10003;') + ring(1, 'd', '&#10003;') + ring(2, '', '3') + ring(3, '', '4');
  h += '<div class="card" style="left:790px;top:150px;width:400px"><h3>Step 4 of 9: Fix the bearing cover</h3><p><span class="tag">Torque 12 N&middot;m</span><span class="tag">M6 x 20</span><span class="tag o">4 bolts</span></p><p>1. Place the cover on the housing so the dowel pin enters the hole.</p><p>2. Tighten the two <b>highlighted bolts (3 and 4)</b> in a cross pattern.</p><p>3. Use the <b>blue torque wrench</b> and wait for the green tick.</p><p style="color:#ffd27f">&#9888; Wear gloves. Keep fingers away from the gear.</p><span class="btn">&#9654; Show animation</span><span class="btn">&#127908; Say "Next"</span><span class="btn">Help</span></div>';
  h += '<div class="bar"><b>Step 4 / 9</b><div class="prog"><i style="width:44%"></i></div><span>Elapsed 01:12</span><span>Target 01:30</span><span class="tag g">On time</span></div>';
} else if (sc === 'expert') {
  h += ring(0, 'd', '&#10003;') + ring(1, 'd', '&#10003;') + ring(2, '', '3') + ring(3, '', '4');
  h += '<div class="card" style="left:960px;top:150px;width:240px;padding:10px 12px"><h3 style="font-size:15px">Step 4: Cover bolts</h3><p><span class="tag">12 N&middot;m</span><span class="tag">M6</span></p><p style="font-size:12.5px;color:#9fb6cc">Detail hidden for expert level<br>(say "Show details" to expand)</p></div>';
  h += '<div class="bar"><b>Step 4 / 9</b><div class="prog"><i style="width:44%"></i></div><span>Elapsed 00:41</span><span>Target 01:30</span><span class="tag g">Ahead 49 s</span></div>';
} else {
  h += ring(0, 'd', '&#10003;') + ring(1, 'd', '&#10003;') + ring(2, 'r', '!') + ring(3, '', '4');
  h += '<div class="alert">&#9888; Wrong bolt detected: <b>M8 x 25</b> picked &mdash; use <b>M6 x 20</b> (bin B-3)</div>';
  h += '<div class="card" style="left:790px;top:170px;width:400px;border-color:#ff7d73;box-shadow:0 0 22px rgba(255,90,79,.5)"><h3 style="color:#ff9d95">Quality check failed</h3><p>Vision check at bolt 3 found a longer thread than the work order allows.</p><p><span class="tag r">Torque tool locked</span><span class="tag o">Supervisor notified</span></p><p>Return the bolt and take the correct one from <b>bin B-3</b> (arrow shown).</p><span class="btn">Retry check</span><span class="btn">Call supervisor</span></div>';
  h += '<div class="bar" style="border-color:#ff7d73"><b>Step 3 / 9</b><div class="prog"><i style="width:30%;background:#ff7d73"></i></div><span>Errors this shift: 1</span><span class="tag r">Held</span></div>';
}
$('ui').innerHTML = h;
