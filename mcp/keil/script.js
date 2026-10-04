// ---------- scene ----------
const scene = (location.hash || '#debug').slice(1);
const $ = id => document.getElementById(id);
const LINES = SRC.split('\n');
const findLine = t => LINES.findIndex(l => l.includes(t)) + 1;
const L_ADC = findLine('adc  = adc_average();'), L_TEMP = L_ADC + 1, L_FAN = findLine('if (fan_on)  IO0SET'), L_UART = findLine('uart0_puts(line);');
const hex = (n, w) => '0x' + (n >>> 0).toString(16).toUpperCase().padStart(w, '0');
const adcOf = t => Math.round(t * 0.010 / 3.3 * 1023);
const SC = {
  build:  { dbg: false, arrow: 0,      temp: 28 },
  debug:  { dbg: true,  arrow: L_ADC,  temp: 28 },
  adc:    { dbg: true,  arrow: L_TEMP, temp: 28 },
  serial: { dbg: true,  arrow: L_UART, temp: 36 },
  thr:    { dbg: true,  arrow: L_FAN,  temp: 40 },
  alarm:  { dbg: true,  arrow: L_FAN,  temp: 45 },
  cool:   { dbg: true,  arrow: L_UART, temp: 30 }
}[scene];
const adc = adcOf(SC.temp), temp = adc * 330 / 1023, fanOn = (scene === 'alarm' || scene === 'thr') ? 1 : 0;
const secs = (0.58264 + SC.temp / 100).toFixed(8);

// ---------- icons (simple SVG) ----------
const S = (b) => '<svg viewBox="0 0 18 18">' + b + '</svg>';
const ICO = {
  doc:  S('<path d="M4 2h7l3 3v11H4z" fill="#fff" stroke="#6b7a90"/><path d="M11 2v3h3" fill="none" stroke="#6b7a90"/>'),
  open: S('<path d="M2 5h5l1 2h8v8H2z" fill="#f4c542" stroke="#b58a12"/>'),
  save: S('<rect x="3" y="3" width="12" height="12" fill="#3a6fb5"/><rect x="6" y="3" width="6" height="4" fill="#fff"/><rect x="6" y="10" width="6" height="5" fill="#cfd8e6"/>'),
  cut:  S('<path d="M5 3l6 8M13 3l-6 8" stroke="#777" stroke-width="1.5"/><circle cx="5" cy="13" r="2.2" fill="none" stroke="#555"/><circle cx="13" cy="13" r="2.2" fill="none" stroke="#555"/>'),
  copy: S('<rect x="3" y="3" width="8" height="10" fill="#fff" stroke="#777"/><rect x="7" y="6" width="8" height="10" fill="#fff" stroke="#777"/>'),
  paste:S('<rect x="3" y="4" width="10" height="12" fill="#e9c46a" stroke="#8a6d1d"/><rect x="7" y="7" width="8" height="9" fill="#fff" stroke="#777"/>'),
  undo: S('<path d="M5 6l-3 3 3 3M2 9h8a4 4 0 010 8" fill="none" stroke="#8a8f98" stroke-width="1.6"/>'),
  redo: S('<path d="M13 6l3 3-3 3M16 9H8a4 4 0 000 8" fill="none" stroke="#8a8f98" stroke-width="1.6"/>'),
  back: S('<path d="M15 9H4M8 5L4 9l4 4" fill="none" stroke="#8a8f98" stroke-width="1.8"/>'),
  fwd:  S('<path d="M3 9h11M10 5l4 4-4 4" fill="none" stroke="#8a8f98" stroke-width="1.8"/>'),
  flag: S('<path d="M5 2v14M5 3h9l-2 3 2 3H5" fill="#1b9be0" stroke="#0b6aa8"/>'),
  find: S('<circle cx="7.5" cy="7.5" r="4.5" fill="#e8f2ff" stroke="#2a64b0" stroke-width="1.5"/><path d="M11 11l5 5" stroke="#2a64b0" stroke-width="2"/>'),
  indent:S('<path d="M3 4h12M7 8h8M7 12h8M3 16h12" stroke="#555" stroke-width="1.4"/>'),
  build:S('<rect x="2" y="9" width="6" height="6" fill="#3aa655"/><rect x="9" y="9" width="6" height="6" fill="#e04b3a"/><rect x="5" y="2" width="6" height="6" fill="#3a6fb5"/>'),
  bld2: S('<path d="M2 14l6-6 3 3-6 6z" fill="#8a6d1d"/><path d="M9 3l6 6-2 2-6-6z" fill="#3a6fb5"/>'),
  load: S('<rect x="3" y="5" width="12" height="9" fill="#cfd8e6" stroke="#556"/><path d="M9 2v8M6 8l3 3 3-3" stroke="#2a8a3a" stroke-width="1.6" fill="none"/>'),
  opts: S('<circle cx="9" cy="9" r="5" fill="#cfd5dc" stroke="#555"/><circle cx="9" cy="9" r="2" fill="#fff" stroke="#555"/>'),
  dbg:  S('<circle cx="8" cy="9" r="5" fill="#d33"/><path d="M12 4l4-2M12 14l4 2" stroke="#222" stroke-width="1.4"/><rect x="11" y="6" width="5" height="6" fill="#2a64b0"/>'),
  rst:  S('<path d="M14 9a5 5 0 11-2-4" fill="none" stroke="#2a64b0" stroke-width="2"/><path d="M12 2l3 3-4 1z" fill="#2a64b0"/>'),
  run:  S('<path d="M5 3l10 6-10 6z" fill="#2a9a43"/>'),
  stop: S('<rect x="4" y="4" width="10" height="10" fill="#d33"/>'),
  step: S('<path d="M9 2v9M5 8l4 4 4-4" fill="none" stroke="#2a64b0" stroke-width="2"/><circle cx="9" cy="15" r="2" fill="#2a64b0"/>'),
  over: S('<path d="M3 11a6 6 0 0112 0" fill="none" stroke="#2a64b0" stroke-width="2"/><path d="M12 8l3 3 1-4z" fill="#2a64b0"/><circle cx="9" cy="15" r="2" fill="#2a64b0"/>'),
  out:  S('<path d="M9 14V5M5 8l4-4 4 4" fill="none" stroke="#2a64b0" stroke-width="2"/><circle cx="9" cy="16" r="1.6" fill="#2a64b0"/>'),
  cur:  S('<path d="M3 9h10M10 5l4 4-4 4" fill="none" stroke="#2a64b0" stroke-width="2"/><rect x="14" y="3" width="2" height="12" fill="#2a64b0"/>'),
  bp:   S('<circle cx="9" cy="9" r="5" fill="#d9262b"/>'),
  bp0:  S('<circle cx="9" cy="9" r="4.5" fill="#fff" stroke="#777"/>'),
  bpx:  S('<circle cx="9" cy="9" r="5" fill="#fff" stroke="#d9262b" stroke-width="2"/><path d="M5 13L13 5" stroke="#d9262b" stroke-width="2"/>'),
  win:  S('<rect x="2" y="3" width="14" height="12" fill="#eaf2fb" stroke="#2a64b0"/><rect x="2" y="3" width="14" height="3" fill="#2a64b0"/>'),
  reg:  S('<rect x="2" y="3" width="14" height="12" fill="#fff" stroke="#556"/><path d="M5 7h8M5 10h8M5 13h8" stroke="#2a64b0"/>'),
  mem:  S('<rect x="3" y="2" width="12" height="14" fill="#fff" stroke="#556"/><path d="M6 6h6M6 9h6M6 12h6" stroke="#8a2a2a"/>'),
  wat:  S('<ellipse cx="9" cy="9" rx="7" ry="4.5" fill="#fff" stroke="#556"/><circle cx="9" cy="9" r="2.2" fill="#2a64b0"/>'),
  ser:  S('<rect x="2" y="3" width="14" height="12" fill="#101820"/><path d="M4 7h6M4 10h9" stroke="#6f6" stroke-width="1.4"/>')
};
const ico = (n, on) => '<span class="ic' + (on ? ' on' : '') + '">' + ICO[n] + '</span>';
const sep = '<span class="sep"></span>';
$('tb1').innerHTML = ['doc', 'open', 'save', 'save', sep, 'cut', 'copy', 'paste', sep, 'undo', 'redo', sep, 'back', 'fwd', sep, 'flag', 'flag', 'flag', 'flag', sep, 'indent', 'indent', 'indent', 'indent', sep, 'open'].map(i => i === sep ? sep : ico(i)).join('') +
  '<span class="combo wide"></span>' + ico('find') + ico('opts') + sep + ico('find', 1) + sep + ico('bp') + ico('bp0') + ico('bpx') + ico('bp') + sep + ico('win', 1) + sep + ico('opts');
$('tb2').innerHTML = SC.dbg
  ? [ 'rst', 'run', 'stop', sep, 'step', 'over', 'out', 'cur', sep, 'win', 'reg', 'wat', 'mem', 'ser', sep, 'bp', 'bp0', sep, 'dbg'].map(i => i === sep ? sep : ico(i)).join('') + '<span class="combo"></span>' + sep + ico('opts')
  : ['build', 'bld2', 'bld2', 'load', 'load', 'load'].map(ico).join('') + '<span class="combo">Target 1</span>' + ico('opts') + sep + ico('build') + ico('bld2') + ico('load') + ico('opts') + ico('doc');

// ---------- helpers for panes ----------
function pane(x, y, w, h, title, body, extra) {
  const d = document.createElement('div'); d.className = 'pane'; d.style.cssText = `left:${x}px;top:${y}px;width:${w}px;height:${h}px`;
  d.innerHTML = '<div class="ph">' + title + '<i>&#9662;</i><i>&#9633;</i><i class="x">&#10005;</i></div><div class="pb">' + body + '</div>' + (extra || ''); $('main').appendChild(d); return d;
}
const KW = /\b(void|int|unsigned|char|float|while|for|if|else|return|const)\b/g;
function colour(line) {
  let t = line.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'), tail = '';
  const ci = t.indexOf('/*'); if (ci >= 0) { tail = '<span class="c">' + t.slice(ci) + '</span>'; t = t.slice(0, ci); }
  if (/^\s*#/.test(t)) return t.replace(/^(\s*#\w+)(.*)$/, '<span class="pp">$1</span>$2').replace(/(&lt;.*&gt;)/, '<span class="s">$1</span>') + tail;
  t = t.replace(/("[^"]*")/g, '<span class="s">$1</span>').replace(KW, '<span class="k">$1</span>').replace(/\b(0x[0-9A-Fa-f]+u?|\d+(\.\d+)?f?u?)\b(?![^<]*>)/g, '<span class="n">$1</span>');
  return t + tail;
}
function editor(x, y, w, h, top, rows) {
  let hh = '';
  for (let n = top; n < top + rows && n <= LINES.length; n++) {
    const cur = n === SC.arrow;
    const mark = cur ? '<span class="mark arrow">&#10148;</span>' : (SC.dbg && n === L_UART && scene !== 'serial' && scene !== 'cool') ? '<span class="mark bp">&#9679;</span>' : '<span class="mark"></span>';
    hh += '<div class="ln' + (cur ? ' cur' : '') + '"><span class="gut">' + n + '</span>' + mark + '<span class="code">' + colour(LINES[n - 1]) + '</span></div>';
  }
  const e = document.createElement('div'); e.className = 'editor'; e.style.cssText = `left:${x}px;top:${y}px;width:${w}px;height:${h}px`; e.innerHTML = hh + '<div class="hs"></div>'; $('main').appendChild(e);
}
function fileTabs(x, y) {
  const t = document.createElement('div'); t.className = 'ftab'; t.style.cssText = `left:${x}px;top:${y}px`;
  t.innerHTML = '<span class="dtab"><i class="pg"></i>Startup.s</span><span class="dtab act"><i class="pg"></i>main.c</span>'; $('main').appendChild(t);
}

// ---------- main layout ----------
const W = 1398, H = 722;
if (!SC.dbg) {
  const left = pane(0, 0, 182, 442, 'Project', '<div class="tree"><div><span class="bx">-</span>&#128193; Project: TempMonitor</div><div>   <span class="bx">-</span>&#128193; Target 1</div><div>      <span class="bx">-</span>&#128193; Source Group 1</div><div>          &#128196; main.c</div><div>          &#128196; Startup.s</div></div>',
    '<div class="ptabs"><span class="ptab act">Project</span><span class="ptab">{} Functions</span><span class="ptab">Templates</span></div>');
  fileTabs(188, 1); editor(188, 26, W - 188, 414, 1, 24);
  pane(0, 446, W, H - 446, 'Build Output', '<div class="out">Build target \'Target 1\'\ncompiling main.c...\nassembling Startup.s...\nlinking...\nProgram Size: Code=3188 RO-data=340 RW-data=12 ZI-data=612\ncreating hex file from ".\\Objects\\TempMonitor"...\n".\\Objects\\TempMonitor" - 0 Error(s), 0 Warning(s).\nBuild Time Elapsed:  00:00:03</div>');
} else {
  const R = [['R0', adc], ['R1', 0x0000000A], ['R2', 0x0000000F], ['R3', 0xE0028004], ['R4', 0x40000010], ['R5', 0], ['R6', 0], ['R7', 0], ['R8', 0], ['R9', 0], ['R10', 0], ['R11', 0], ['R12', 0x40000200], ['R13 (SP)', 0x40001FD8], ['R14 (LR)', 0x00000234], ['R15 (PC)', 0x00000308 + (SC.arrow % 7) * 4], ['CPSR', 0x6000001F], ['SPSR', 0]];
  pane(0, 0, 200, 442, 'Registers',
    '<table class="t"><tr><th>Register</th><th>Value</th></tr>' + R.map((r, i) => '<tr class="' + (i === 0 ? 'chg' : '') + '"><td>' + r[0] + '</td><td>' + hex(r[1], 8) + '</td></tr>').join('') +
    '<tr><td>Mode</td><td>System</td></tr><tr><td>States</td><td>' + Math.round((0.58264 + SC.temp / 100) * 60e6) + '</td></tr><tr><td>Sec</td><td>' + secs + '</td></tr></table>',
    '<div class="ptabs"><span class="ptab">Project</span><span class="ptab act">Registers</span></div>');
  // disassembly
  const base = 0x00000308 + (SC.arrow % 7) * 4;
  const asm = [['EB000016', 'BL', 'adc_average (0x00000368)'], ['E1A04000', 'MOV', 'R4,R0'], ['E3A0114D', 'MOV', 'R1,#0x40000000'], ['EE070A90', 'MCR', 'p7,0,R0,c0,c0,4'], ['E5910000', 'LDR', 'R0,[R1]'], ['E1500004', 'CMP', 'R0,R4'], ['E3A00000', 'MOV', 'R0,#0x00000000'], ['E59F1030', 'LDR', 'R1,[PC,#0x0030]']];
  let dh = '<div class="out" style="padding:3px 6px;font-size:12px;line-height:15px">' + (SC.arrow >= L_ADC ? '     ' + SC.arrow + ':        ' + LINES[SC.arrow - 1].trim() + '\n' : '') +
    asm.map((a, i) => (i === 0 ? '<span style="background:#ffffa8">&#10148; ' : '  <span>') + hex(base + i * 4, 8) + '  ' + a[0] + '  ' + a[1].padEnd(5) + a[2] + '</span>').join('\n') + '</div>';
  pane(206, 0, W - 206, 150, 'Disassembly', dh);
  const t = document.createElement('div'); fileTabs(206, 154);
  editor(206, 179, W - 206, 262, Math.max(1, SC.arrow - 7), 15);
  // bottom row
  pane(0, 446, 430, H - 446, 'Command', '<div class="out" style="font-size:12px">Load "D:\\LPC2148\\TempMonitor\\Objects\\TempMonitor.axf"\nBS \\\\TempMonitor\\main.c\\' + L_UART + '\nWS 1, `adc, `temp, `fan_on\nLA IO0PIN\n\n</div><div class="out" style="padding-top:60px;font-size:11px;color:#555">ASSIGN BreakDisable BreakEnable BreakKill BreakList BreakSet BreakAccess COVERAGE</div>');
  pane(436, 446, 470, H - 446, 'Call Stack + Locals',
    '<table class="t"><tr><th>Name</th><th>Location/Value</th><th>Type</th></tr><tr><td>main</td><td>0x00000308</td><td>int f()</td></tr>' +
    '<tr class="chg"><td>&nbsp;&nbsp;adc</td><td>' + adc + '</td><td>auto - uint</td></tr><tr class="chg"><td>&nbsp;&nbsp;temp</td><td>' + temp.toFixed(7) + '</td><td>auto - float</td></tr>' +
    '<tr><td>&nbsp;&nbsp;line</td><td>0x40001FB8</td><td>auto - array[32] of char</td></tr><tr class="chg"><td>&nbsp;&nbsp;fan_on</td><td>0x0' + fanOn + '</td><td>auto - uchar</td></tr></table>');
  let wbody;
  if (scene === 'adc') {
    const AD0CR = 0x00200302, GDR = ((1 << 31) >>> 0) + (1 << 24) + (adc << 6);
    const bytes = a => [a & 255, (a >>> 8) & 255, (a >>> 16) & 255, (a >>> 24) & 255].map(b => b.toString(16).toUpperCase().padStart(2, '0')).join(' ');
    const rows = [['E0034000', AD0CR], ['E0034004', GDR], ['E0034008', 0], ['E003400C', 0x100], ['E0034010', 0], ['E0034014', GDR], ['E0034018', 0], ['E003401C', 0]];
    wbody = '<div class="out" style="padding:2px 6px;font-size:12px;line-height:16px">Address: 0xE0034000\n' + rows.map(r => '0x' + r[0] + ': ' + bytes(r[1] >>> 0)).join('\n') + '</div>';
  } else {
    wbody = '<table class="t"><tr><th>Name</th><th>Value</th><th>Type</th></tr><tr class="chg"><td>adc</td><td>' + adc + '</td><td>uint</td></tr><tr class="chg"><td>temp</td><td>' + temp.toFixed(7) + '</td><td>float</td></tr>' +
      '<tr><td>fan_on</td><td>' + fanOn + '</td><td>uchar</td></tr><tr><td>AD0CR</td><td>0x00200302</td><td>ulong</td></tr><tr><td>AD0DR1</td><td>' + hex(((1 << 31) >>> 0) + (1 << 24) + (adc << 6), 8) + '</td><td>ulong</td></tr>' +
      '<tr><td>IO0PIN</td><td>' + (fanOn ? '0x00000380' : '0x00000000') + '</td><td>ulong</td></tr></table>';
  }
  pane(912, 446, W - 912, H - 446, scene === 'adc' ? 'Memory 1' : 'Watch 1', wbody, '<div class="ptabs"><span class="ptab ' + (scene === 'adc' ? '' : 'act') + '">Watch 1</span><span class="ptab ' + (scene === 'adc' ? 'act' : '') + '">Memory 1</span></div>');
}

// ---------- status ----------
$('status').innerHTML = '<span class="l"></span><span class="sp"></span><span>' + (SC.dbg ? 'Simulation' : 'Simulation') + '</span>' + (SC.dbg ? '<span>t1: ' + secs + ' sec</span>' : '') +
  '<span>L:' + (SC.arrow || 14) + ' C:' + (SC.dbg ? 1 : 4) + '</span><span class="keys">CAP&nbsp;&nbsp;NUM&nbsp;&nbsp;SCRL&nbsp;&nbsp;OVR&nbsp;&nbsp;R/W</span>';

// ---------- floating dialogs ----------
const log = []; let fan = 0;
(scene === 'cool' ? [28, 36, 40, 45, 45, 39, 30, 30] : scene === 'serial' ? [28, 28, 28, 36, 36] : scene === 'thr' ? [28, 36, 36, 40, 40] : []).forEach(t => {
  const a = adcOf(t), tt = a * 330 / 1023; if (tt >= 40) fan = 1; else if (tt <= 38) fan = 0;
  log.push('Temp: ' + tt.toFixed(1).padStart(4) + ' C | ADC: 0x' + a.toString(16).toUpperCase().padStart(3, '0') + ' | FAN ' + (fan ? 'ON' : 'OFF'));
});
const serialText = 'LPC2148 Temperature Monitoring System\n' + log.join('\n');
function win(x, y, w, title, body) {
  const d = document.createElement('div'); d.className = 'win'; d.style.cssText = `left:${x}px;top:${y}px;width:${w}px`;
  d.innerHTML = '<div class="wt">' + title + '<i>&#10005;</i></div><div class="wbody">' + body + '</div>'; $('floats').appendChild(d);
}
const cb = on => '<span class="cb">' + (on ? '&#10003;' : '') + '</span>';
const grp = (t, b) => '<div class="grp"><span class="lg">' + t + '</span>' + b + '</div>';
function adcDialog() {
  const GDR = ((1 << 31) >>> 0) + (1 << 24) + (adc << 6);
  win(440, 120, 700, 'A/D Converter 0',
   '<div style="display:flex;gap:12px"><div style="flex:1.1">' +
   grp('AD0CR: 0x00200302', '<span class="fld">SEL <span class="box">0x02</span></span><span class="fld">CLKDIV <span class="box">3</span></span><span class="fld">BURST ' + cb(0) + '</span><br><span class="fld">CLKS <span class="box">0</span></span><span class="fld">PDN ' + cb(1) + '</span><span class="fld">START <span class="box">0</span></span><span class="fld">EDGE ' + cb(0) + '</span>') +
   grp('AD0GDR: ' + hex(GDR, 8), '<span class="fld">V/VREF <span class="box">0x' + adc.toString(16).toUpperCase().padStart(3, '0') + '</span></span><span class="fld">CHN <span class="box">1</span></span><span class="fld">OVERRUN ' + cb(0) + '</span><span class="fld">DONE ' + cb(1) + '</span>') +
   grp('AD0STAT / ADC clock', '<span class="fld">DONE1 ' + cb(1) + '</span><span class="fld">ADINT ' + cb(0) + '</span><span class="fld">ADC clock <span class="box">3.75 MHz</span></span><span class="fld">VREF <span class="box">3.30 V</span></span>') +
   '</div><div style="flex:1">' + grp('Analog inputs', '<table class="t"><tr><th>Pin</th><th>Vin [V]</th><th>AD0DRx</th></tr>' + [0, 1, 2, 3, 4, 5, 6, 7].map(i => '<tr class="' + (i === 1 ? 'chg' : '') + '"><td>AD0.' + i + '</td><td>' + (i === 1 ? (SC.temp / 100).toFixed(2) : '0.00') + '</td><td>' + (i === 1 ? '0x' + adc.toString(16).toUpperCase().padStart(3, '0') : '-') + '</td></tr>').join('') + '</table>') + '</div></div>');
}
function portDialog(x, y) {
  const P = fanOn ? 0x380 : 0; let labs = '', bits = '';
  for (let b = 31; b >= 0; b--) { labs += '<div>' + b + '</div>'; bits += '<div>' + cb((P >> b) & 1) + '</div>'; }
  win(x, y, 800, 'Parallel Port 0',
   '<span class="fld">IODIR <span class="box">0x00000F80</span></span><span class="fld">IOPIN <span class="box">' + hex(P, 8) + '</span></span><span class="fld">IOSET/IOCLR <span class="box">' + hex(P, 8) + '</span></span><div style="height:8px"></div>' +
   grp('Bits', '<div class="cbgrid">' + labs + '</div><div class="cbgrid">' + bits + '</div>') + grp('Pins', '<div class="cbgrid">' + labs + '</div><div class="cbgrid">' + bits + '</div>'));
}
function serialWin(x, y, w) { win(x, y, w, 'UART #1', '<div class="term">' + serialText.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</div>'); }
if (scene === 'adc') adcDialog();
if (scene === 'alarm') portDialog(300, 150);
if (scene === 'serial' || scene === 'thr') serialWin(380, 150, 660);
if (scene === 'cool') { serialWin(230, 110, 560); portDialog(500, 380); }
