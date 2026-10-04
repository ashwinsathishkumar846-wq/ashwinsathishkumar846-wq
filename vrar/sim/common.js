// photo-style gearbox assembly station (SVG with lighting, noise and depth)
function machineSVG(opt) {
  opt = opt || {};
  const bolts = [[398, 253], [522, 253], [398, 377], [522, 377]];
  const done = opt.done || [];
  const hex = (x, y, r, dn) => {
    const pts = [0, 1, 2, 3, 4, 5].map(i => (x + r * Math.cos(Math.PI / 3 * i + .26)).toFixed(1) + ',' + (y + r * Math.sin(Math.PI / 3 * i + .26)).toFixed(1)).join(' ');
    return `<ellipse cx="${x + 3}" cy="${y + 5}" rx="${r + 3}" ry="${r}" fill="rgba(0,0,0,.45)"/><polygon points="${pts}" fill="url(#${dn ? 'bz' : 'bs'})" stroke="#1d2126" stroke-width="2"/><circle cx="${x}" cy="${y}" r="${r * .55}" fill="none" stroke="rgba(0,0,0,.45)" stroke-width="2"/><circle cx="${x - r * .25}" cy="${y - r * .3}" r="${r * .22}" fill="rgba(255,255,255,.55)"/>`;
  };
  return `<svg viewBox="0 0 920 520" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
  <defs>
    <linearGradient id="bench" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b949e"/><stop offset=".08" stop-color="#5d666f"/><stop offset="1" stop-color="#262b31"/></linearGradient>
    <linearGradient id="hs" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c3ccd6"/><stop offset=".35" stop-color="#8a95a2"/><stop offset=".7" stop-color="#5b6672"/><stop offset="1" stop-color="#3b434c"/></linearGradient>
    <linearGradient id="in" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4a535d"/><stop offset="1" stop-color="#7d8996"/></linearGradient>
    <radialGradient id="cv" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="#eef2f6"/><stop offset=".35" stop-color="#b8c1cc"/><stop offset=".75" stop-color="#7d8896"/><stop offset="1" stop-color="#4f5863"/></radialGradient>
    <radialGradient id="bs" cx=".35" cy=".3"><stop offset="0" stop-color="#f4f6f8"/><stop offset=".6" stop-color="#aab3be"/><stop offset="1" stop-color="#606a75"/></radialGradient>
    <radialGradient id="bz" cx=".35" cy=".3"><stop offset="0" stop-color="#cfd5dc"/><stop offset=".6" stop-color="#8b95a1"/><stop offset="1" stop-color="#4a525c"/></radialGradient>
    <radialGradient id="hub" cx=".4" cy=".35"><stop offset="0" stop-color="#d9dfe6"/><stop offset="1" stop-color="#5e6873"/></radialGradient>
    <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 .22 0"/></filter>
    <filter id="soft"><feGaussianBlur stdDeviation="3"/></filter>
  </defs>
  <rect x="0" y="418" width="920" height="102" fill="url(#bench)"/>
  <rect x="0" y="418" width="920" height="6" fill="#aab2bb" opacity=".7"/>
  <g opacity=".5">${[0,1,2,3,4,5,6,7,8,9,10,11].map(i=>`<rect x="${i*80}" y="440" width="2" height="80" fill="#000" opacity=".25"/>`).join('')}</g>
  <ellipse cx="460" cy="428" rx="330" ry="22" fill="#000" opacity=".5" filter="url(#soft)"/>
  <rect x="120" y="270" width="95" height="52" rx="10" fill="url(#hs)" stroke="#1d2126" stroke-width="3"/>
  <rect x="700" y="285" width="140" height="34" rx="8" fill="url(#hs)" stroke="#1d2126" stroke-width="3"/>
  <rect x="210" y="130" width="500" height="296" rx="24" fill="url(#hs)" stroke="#1d2126" stroke-width="4"/>
  <rect x="214" y="134" width="492" height="16" rx="8" fill="#fff" opacity=".28"/>
  <rect x="238" y="158" width="444" height="244" rx="16" fill="url(#in)" stroke="#1d2126" stroke-width="2.5"/>
  ${[260,300,340].map(x=>`<rect x="${x}" y="176" width="12" height="206" rx="4" fill="#000" opacity=".12"/>`).join('')}
  ${[620,640,660].map(x=>`<rect x="${x}" y="176" width="12" height="206" rx="4" fill="#fff" opacity=".1"/>`).join('')}
  ${[[232,148],[688,148],[232,408],[688,408]].map(p=>hex(p[0],p[1],10,0)).join('')}
  <circle cx="460" cy="315" r="122" fill="#2c3238" stroke="#1d2126" stroke-width="4"/>
  <circle cx="460" cy="315" r="116" fill="none" stroke="#9aa4af" stroke-width="2" opacity=".7"/>
  ${opt.cover ? `<circle cx="460" cy="315" r="104" fill="url(#cv)" stroke="#1d2126" stroke-width="3"/>
  <circle cx="460" cy="315" r="86" fill="none" stroke="#000" stroke-width="1.5" opacity=".35"/><circle cx="460" cy="315" r="84" fill="none" stroke="#fff" stroke-width="1.5" opacity=".5"/>
  <circle cx="460" cy="315" r="56" fill="none" stroke="#000" stroke-width="1.5" opacity=".3"/><circle cx="460" cy="315" r="54" fill="none" stroke="#fff" stroke-width="1.5" opacity=".45"/>
  <circle cx="460" cy="315" r="34" fill="url(#hub)" stroke="#1d2126" stroke-width="3"/><circle cx="460" cy="315" r="14" fill="#1b1f24"/><rect x="456" y="296" width="8" height="8" fill="#1b1f24"/>
  <path d="M365 262 A104 104 0 0 1 520 232" fill="none" stroke="#fff" stroke-width="5" opacity=".35"/>` :
  `<circle cx="460" cy="315" r="96" fill="#1c2025"/><circle cx="460" cy="315" r="60" fill="url(#hub)" stroke="#1d2126" stroke-width="3"/><circle cx="460" cy="315" r="26" fill="#14171b"/>`}
  ${opt.cover ? bolts.map((b, i) => hex(b[0], b[1], 14, done.includes(i))).join('') : ''}
  <rect x="740" y="60" width="26" height="72" fill="#3b434c"/><rect x="722" y="38" width="62" height="30" rx="7" fill="#d9a21b" stroke="#5a3f05" stroke-width="2"/><rect x="726" y="42" width="54" height="8" rx="4" fill="#fff" opacity=".35"/>
  ${opt.part ? `<g transform="translate(${opt.part[0]},${opt.part[1]})"><ellipse cx="6" cy="10" rx="76" ry="70" fill="rgba(0,0,0,.45)"/><circle r="72" fill="url(#cv)" stroke="#1d2126" stroke-width="4"/><circle r="52" fill="none" stroke="#000" stroke-width="1.5" opacity=".3"/><circle r="26" fill="url(#hub)" stroke="#1d2126" stroke-width="3"/>${[[-46,-46],[46,-46],[-46,46],[46,46]].map(p=>hex(p[0],p[1],9,0)).join('')}</g>` : ''}
  <rect width="920" height="520" filter="url(#grain)" opacity=".55"/>
  </svg>`;
}
