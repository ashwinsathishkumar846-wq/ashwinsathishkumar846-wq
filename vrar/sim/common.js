// draws the gearbox assembly station used in every scene
function machineSVG(opt) {
  opt = opt || {};
  const bolts = [[398, 253], [522, 253], [398, 377], [522, 377]];
  const col = i => opt.done && opt.done.includes(i) ? '#7a8798' : '#b6c0cc';
  return `<svg viewBox="0 0 920 520" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
  <defs>
    <linearGradient id="mt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5b6572"/><stop offset="1" stop-color="#2e353e"/></linearGradient>
    <linearGradient id="hs" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8e99a6"/><stop offset="1" stop-color="#4c5560"/></linearGradient>
    <radialGradient id="bc" cx=".4" cy=".35"><stop offset="0" stop-color="#cfd6de"/><stop offset="1" stop-color="#7d8896"/></radialGradient>
  </defs>
  <rect x="0" y="420" width="920" height="100" fill="url(#mt)"/><rect x="0" y="420" width="920" height="8" fill="#20252b"/>
  <rect x="40" y="440" width="840" height="12" fill="#1b1f24"/>
  ${[80,200,320,440,560,680,800].map(x=>`<circle cx="${x}" cy="446" r="7" fill="#3a424c"/>`).join('')}
  <rect x="210" y="130" width="500" height="300" rx="26" fill="url(#hs)" stroke="#2a3038" stroke-width="4"/>
  <rect x="236" y="156" width="448" height="248" rx="18" fill="#6b7683" stroke="#2a3038" stroke-width="2"/>
  <circle cx="460" cy="315" r="118" fill="#58626e" stroke="#2a3038" stroke-width="4"/>
  <circle cx="460" cy="315" r="96" fill="${opt.cover ? 'url(#bc)' : '#3b424b'}" stroke="#2a3038" stroke-width="3"/>
  ${opt.cover ? '' : '<circle cx="460" cy="315" r="62" fill="#252a30"/><circle cx="460" cy="315" r="30" fill="#8e99a6"/>'}
  <circle cx="460" cy="315" r="${opt.cover ? 34 : 0}" fill="#4d5762" stroke="#2a3038" stroke-width="3"/>
  ${bolts.map((b, i) => opt.cover ? `<g><circle cx="${b[0]}" cy="${b[1]}" r="13" fill="${opt.done && opt.done.includes(i) ? '#98a4b3' : '#c9d0d8'}" stroke="#2a3038" stroke-width="2.5"/><path d="M${b[0]-7} ${b[1]}h14M${b[0]} ${b[1]-7}v14" stroke="#2a3038" stroke-width="2.5"/></g>` : '').join('')}
  <rect x="120" y="270" width="95" height="52" rx="10" fill="#8a95a2" stroke="#2a3038" stroke-width="3"/>
  <rect x="705" y="285" width="130" height="32" rx="8" fill="#9aa5b2" stroke="#2a3038" stroke-width="3"/>
  <rect x="740" y="60" width="26" height="70" fill="#4b545f"/><rect x="722" y="40" width="62" height="28" rx="6" fill="#d59a1b" stroke="#6a4a07" stroke-width="2"/>
  ${opt.part ? `<g transform="translate(${opt.part[0]},${opt.part[1]})"><circle r="70" fill="url(#bc)" stroke="#2a3038" stroke-width="4"/><circle r="26" fill="#4d5762" stroke="#2a3038" stroke-width="3"/>${[[-45,-45],[45,-45],[-45,45],[45,45]].map(p=>`<circle cx="${p[0]}" cy="${p[1]}" r="9" fill="#c9d0d8" stroke="#2a3038" stroke-width="2"/>`).join('')}</g>` : ''}
  </svg>`;
}
const cover = (n) => n;
