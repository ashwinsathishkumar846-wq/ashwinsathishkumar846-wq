// ---------- scene selection ----------
const scene = (location.hash || '#debug').slice(1);
const $ = id => document.getElementById(id);
const LINES = SRC.split('\n');
const findLine = t => LINES.findIndex(l => l.includes(t)) + 1;
const L_ADC = findLine('adc  = adc_average();'), L_FAN = findLine('if (fan_on)  IO0SET'), L_UART = findLine('uart0_puts(line);');

const hex = (n, w) => '0x' + (n >>> 0).toString(16).toUpperCase().padStart(w, '0');
const adcOf = t => Math.round(t * 0.010 / 3.3 * 1023);
const SC = {
  build:  { dbg: false, top: 1,  arrow: 0,      temp: 28 },
  debug:  { dbg: true,  top: 124, arrow: L_ADC,  temp: 28 },
  adc:    { dbg: true,  top: 124, arrow: L_ADC + 1, temp: 28 },
  serial: { dbg: true,  top: 129, arrow: L_UART, temp: 36 },
  thr:    { dbg: true,  top: 129, arrow: L_FAN,  temp: 40 },
  alarm:  { dbg: true,  top: 129, arrow: L_FAN,  temp: 45 },
  cool:   { dbg: true,  top: 129, arrow: L_UART, temp: 30 }
}[scene];
const adc = adcOf(SC.temp), temp = adc * 330 / 1023, fanOn = (scene === 'alarm' || scene === 'thr') ? 1 : 0;

// ---------- toolbar ----------
const buildIcons = ['&#128193;', '&#128190;', '&#9986;', '&#128203;', '|', '&#8630;', '&#8631;', '|', '&#128269;', '|', '&#9881;', '&#9654;', '&#9654;&#9654;', '&#9632;', '|', '&#10004;'];
const dbgIcons = ['&#8635;', '&#9654;', '&#9632;', '&#8658;', '&#8595;', '&#8593;', '&#8594;', '|', '&#128308;', '&#9940;', '|', '&#128202;', '&#128190;', '&#128221;', '&#9881;'];
$('toolbar').innerHTML = (SC.dbg ? dbgIcons : buildIcons).map(i => i === '|' ? '<span class="ic sep"></span>' : '<span class="ic">' + i + '</span>').join('') +
  '<span class="tsel">Target 1 &#9662;</span>' + (SC.dbg ? '<span class="ic hl">&#128030;</span>' : '<span class="ic hl">&#9874;</span>');

// ---------- editor with simple C highlighting ----------
const KW = /\b(void|int|unsigned|char|float|while|for|if|else|return|const|define|include)\b/g;
function colour(line) {
  let t = line.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const ci = t.indexOf('/*'); let tail = '';
  if (ci >= 0) { tail = '<span class="c">' + t.slice(ci) + '</span>'; t = t.slice(0, ci); }
  if (/^\s*#/.test(t)) return '<span class="k">' + t.replace(/&lt;(.*)&gt;/, '&lt;<span class="s">$1</span>&gt;') + '</span>' + tail;
  t = t.replace(/("[^"]*")/g, '<span class="s">$1</span>').replace(KW, '<span class="k">$1</span>');
  return t + tail;
}
function drawEditor() {
  let h = '';
  for (let n = SC.top; n < SC.top + 26 && n <= LINES.length; n++) {
    const cur = n === SC.arrow;
    const mark = cur ? '<span class="arrow">&#10148;</span>' : (SC.dbg && n === L_UART && scene !== 'serial' && scene !== 'cool') ? '<span class="bp">&#9679;</span>' : '';
    h += '<div class="ln' + (cur ? ' cur' : '') + '"><span class="gut">' + n + '</span><span class="mark">' + mark + '</span><span class="code">' + colour(LINES[n - 1]) + '</span></div>';
  }
  $('editor').innerHTML = h;
}
drawEditor();

// ---------- left panel ----------
function panel(id, title, body) { $(id).innerHTML = '<div class="ph">' + title + '</div><div class="pb">' + body + '</div>'; }
if (!SC.dbg) {
  panel('leftPanel', 'Project', '<div class="tree"><div>&#9660; &#128193; Target 1</div><div>     &#9660; &#128193; Source Group 1</div><div class="sel">          &#128196; main.c</div><div>          &#128196; Startup.s</div><div>     &#128193; Output</div></div>');
} else {
  const R = [['R0', adc], ['R1', 0x0000000A], ['R2', 0x0000000F], ['R3', 0xE0028004], ['R4', 0x40000010], ['R5', 0], ['R6', 0], ['R7', 0], ['R8', 0], ['R9', 0], ['R10', 0], ['R11', 0], ['R12', 0x40000200], ['R13 (SP)', 0x40001FD8], ['R14 (LR)', 0x00000234], ['R15 (PC)', 0x00000308 + (SC.arrow % 7) * 4], ['CPSR', 0x6000001F], ['SPSR', 0]];
  let t = '<table class="reg"><tr><td><b>Register</b></td><td><b>Value</b></td></tr>' +
    R.map((r, i) => '<tr class="' + (i === 0 ? 'chg' : '') + '"><td>' + (i < 13 ? '&#9656; ' : '') + r[0] + '</td><td>' + hex(r[1], 8) + '</td></tr>').join('') +
    '<tr><td>Mode</td><td>System</td></tr><tr><td>State</td><td>ARM</td></tr><tr><td>Sec</td><td>' + (0.58264 + SC.temp / 100).toFixed(8) + '</td></tr></table>';
  panel('leftPanel', 'Registers', t);
}

// ---------- bottom panels ----------
const log = [];
const seq = scene === 'cool' ? [28, 36, 40, 45, 45, 39, 30, 30] : scene === 'serial' ? [28, 28, 28, 36, 36] : scene === 'thr' ? [28, 36, 36, 40, 40] : [28];
let fan = 0;
seq.forEach(t => { const a = adcOf(t), tt = a * 330 / 1023; if (tt >= 40) fan = 1; else if (tt <= 38) fan = 0; log.push('Temp: ' + tt.toFixed(1).padStart(4) + ' C | ADC: 0x' + a.toString(16).toUpperCase().padStart(3, '0') + ' | FAN ' + (fan ? 'ON' : 'OFF')); });
const serialText = 'LPC2148 Temperature Monitoring System\n' + log.join('\n');

if (!SC.dbg) {
  panel('bl', 'Build Output',
   '<div class="bout">Build target \'Target 1\'\ncompiling main.c...\nassembling Startup.s...\nlinking...\nProgram Size: Code=3188 RO-data=340 RW-data=12 ZI-data=612\ncreating hex file from "TempMonitor"...\n"TempMonitor" - 0 Error(s), 0 Warning(s).</div>');
  $('br').style.display = 'none'; $('bl').style.flex = '1';
} else {
  panel('bl', 'Call Stack + Locals',
   '<table class="w"><tr><th>Name</th><th>Location/Value</th><th>Type</th></tr>' +
   '<tr><td>&#9660; main</td><td>0x00000308</td><td>int f()</td></tr>' +
   '<tr class="chg"><td>&nbsp;&nbsp;adc</td><td>0x' + adc.toString(16).toUpperCase().padStart(8, '0') + '</td><td>auto - uint</td></tr>' +
   '<tr class="chg"><td>&nbsp;&nbsp;temp</td><td>' + temp.toFixed(7) + '</td><td>auto - float</td></tr>' +
   '<tr><td>&nbsp;&nbsp;line</td><td>0x40001FB8</td><td>auto - array[32] of char</td></tr>' +
   '<tr class="chg"><td>&nbsp;&nbsp;fan_on</td><td>0x0' + fanOn + '</td><td>auto - uchar</td></tr></table>' +
   '<div class="cmd" style="margin-top:14px"><b>Command</b>\nLoad "D:\\LPC2148\\TempMonitor\\TempMonitor.axf"\nBS \\\\TempMonitor\\main.c\\' + L_UART + '\nWS 1, adc, temp, fan_on\n&gt;</div>');
  if (scene === 'adc') {
    const AD0CR = 0x00200302, GDR = ((1 << 31) >>> 0) + (1 << 24) + (adc << 6);
    const bytes = a => [a & 255, (a >>> 8) & 255, (a >>> 16) & 255, (a >>> 24) & 255].map(b => b.toString(16).toUpperCase().padStart(2, '0')).join(' ');
    const rows = [['E0034000', AD0CR], ['E0034004', GDR], ['E0034008', 0], ['E003400C', 0x100], ['E0034010', 0], ['E0034014', GDR], ['E0034018', 0], ['E003401C', 0]];
    panel('br', 'Memory 1', '<div class="cmd">Address: 0xE0034000\n' + rows.map(r => '0x' + r[0] + ': ' + bytes(r[1] >>> 0) + ' ').join('\n') + '</div>');
  } else {
    panel('br', 'Watch 1',
     '<table class="w"><tr><th>Name</th><th>Value</th><th>Type</th></tr>' +
     '<tr class="chg"><td>&#9656; adc</td><td>' + adc + '</td><td>uint</td></tr>' +
     '<tr class="chg"><td>&#9656; temp</td><td>' + temp.toFixed(7) + '</td><td>float</td></tr>' +
     '<tr><td>&#9656; fan_on</td><td>' + fanOn + '</td><td>uchar</td></tr>' +
     '<tr><td>&#9656; AD0CR</td><td>0x00200302</td><td>ulong</td></tr>' +
     '<tr><td>&#9656; AD0DR1</td><td>' + hex(((1 << 31) >>> 0) + (1 << 24) + (adc << 6), 8) + '</td><td>ulong</td></tr>' +
     '<tr><td>&#9656; IO0PIN</td><td>' + (fanOn ? '0x00000380' : '0x00000000') + '</td><td>ulong</td></tr></table>');
  }
}

// ---------- status bar ----------
$('status').innerHTML = (SC.dbg ? '<span>Simulation</span><span>t1: ' + (0.58264 + SC.temp / 100).toFixed(8) + ' sec</span>' : '<span>Ready</span>') +
  '<span>L:' + (SC.arrow || 1) + ' C:1</span><b>CAP&nbsp;&nbsp;NUM&nbsp;&nbsp;SCRL&nbsp;&nbsp;OVR&nbsp;&nbsp;R/W</b>';

// ---------- floating windows ----------
function win(x, y, w, title, body) {
  const d = document.createElement('div'); d.className = 'win'; d.style.cssText = 'left:' + x + 'px;top:' + y + 'px;width:' + w + 'px';
  d.innerHTML = '<div class="wt">' + title + '<i>&#10005;</i></div><div class="wbody">' + body + '</div>'; $('floats').appendChild(d);
}
const cb = on => '<span class="cb">' + (on ? '&#10003;' : '') + '</span>';
function adcDialog() {
  const GDR = ((1 << 31) >>> 0) + (1 << 24) + (adc << 6);
  win(430, 90, 700, 'A/D Converter 0',
   '<div style="display:flex;gap:10px"><div style="flex:1.1">' +
   '<div class="grp"><legend>AD0CR - A/D Control Register: 0x00200302</legend>' +
   '<span class="fld">SEL <span class="box">0x02</span></span><span class="fld">CLKDIV <span class="box">3</span></span>' +
   '<span class="fld">BURST ' + cb(0) + '</span><span class="fld">CLKS <span class="box">0</span></span><br>' +
   '<span class="fld">PDN ' + cb(1) + '</span><span class="fld">START <span class="box">0</span></span><span class="fld">EDGE ' + cb(0) + '</span></div>' +
   '<div class="grp"><legend>AD0GDR - Global Data Register: ' + hex(GDR, 8) + '</legend>' +
   '<span class="fld">V/VREF <span class="box">0x' + adc.toString(16).toUpperCase().padStart(3, '0') + '</span></span><span class="fld">CHN <span class="box">1</span></span>' +
   '<span class="fld">OVERRUN ' + cb(0) + '</span><span class="fld">DONE ' + cb(1) + '</span></div>' +
   '<div class="grp"><legend>AD0STAT / ADC clock</legend><span class="fld">DONE1 ' + cb(1) + '</span><span class="fld">ADINT ' + cb(0) + '</span>' +
   '<span class="fld">ADC clock <span class="box">3.75 MHz</span></span><span class="fld">VREF <span class="box">3.30 V</span></span></div></div>' +
   '<div style="flex:1"><div class="grp"><legend>Analog inputs</legend><table class="w" style="width:100%"><tr><th>Pin</th><th>Vin [V]</th><th>AD0DRx</th></tr>' +
   [0, 1, 2, 3, 4, 5, 6, 7].map(i => '<tr class="' + (i === 1 ? 'chg' : '') + '"><td>AD0.' + i + '</td><td>' + (i === 1 ? (SC.temp / 100).toFixed(2) : '0.00') + '</td><td>' + (i === 1 ? '0x' + adc.toString(16).toUpperCase().padStart(3, '0') : '-') + '</td></tr>').join('') +
   '</table></div></div></div>');
}
function portDialog(x, y) {
  const P = fanOn ? 0x380 : 0;
  let labs = '', bits = '', pins = '';
  for (let b = 31; b >= 0; b--) { labs += '<div>' + b + '</div>'; const on = (P >> b) & 1; bits += '<div>' + cb(on) + '</div>'; pins += '<div>' + cb(on) + '</div>'; }
  win(x, y, 800, 'Parallel Port 0',
   '<div class="fld">IODIR <span class="box">0x00000F80</span></div><div class="fld">IOPIN <span class="box">' + hex(P, 8) + '</span></div><div class="fld">IOSET/IOCLR <span class="box">' + hex(P, 8) + '</span></div>' +
   '<div class="grp" style="margin-top:6px"><legend>Bits</legend><div class="cbgrid">' + labs + '</div><div class="cbgrid">' + bits + '</div></div>' +
   '<div class="grp"><legend>Pins</legend><div class="cbgrid">' + labs + '</div><div class="cbgrid">' + pins + '</div></div>');
}
function serialWin(x, y, w) {
  win(x, y, w, 'UART #1', '<div class="term">' + serialText.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</div>');
}
if (scene === 'adc') adcDialog();
if (scene === 'alarm') portDialog(330, 120);
if (scene === 'serial' || scene === 'thr') serialWin(380, 120, 660);
if (scene === 'cool') { serialWin(250, 70, 560); portDialog(520, 360); }
