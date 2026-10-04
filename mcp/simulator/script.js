// ---------------- constants (same values as the C program) ----------------
const VREF = 3.3, ADC_MAX = 1023, SAMPLES = 8, HYST = 2.0;
const CHANNEL = 1;                                   // AD0.1 -> P0.28
const AD0CR = (1 << 1) | (3 << 8) | (1 << 21) | (1 << 24);   // SEL, CLKDIV, PDN, START now
const $ = id => document.getElementById(id);

const st = { amb: 28, thr: 40, running: true, fan: false, buzzer: false, time: 0, hist: [], log: [], seed: 7 };

// small deterministic random generator so the output is repeatable
function rnd() { st.seed = (st.seed * 16807) % 2147483647; return st.seed / 2147483647; }

// ---------------- LM35 + ADC model ----------------
function convertOnce() {
  const vin = st.amb * 0.010 + (rnd() - 0.5) * 0.004;           // 10 mV per degree C, +/- 2 mV noise
  const code = Math.min(ADC_MAX, Math.max(0, Math.round(vin / VREF * ADC_MAX)));
  return { vin, code };
}
function readAdc() {                                              // average of 8 conversions
  let sum = 0, vin = 0;
  for (let i = 0; i < SAMPLES; i++) { const c = convertOnce(); sum += c.code; vin += c.vin; }
  return { code: Math.round(sum / SAMPLES), vin: vin / SAMPLES };
}
const hex = (n, w) => '0x' + n.toString(16).toUpperCase().padStart(w, '0');

// ---------------- one pass of the main() loop ----------------
function tick() {
  const { code, vin } = readAdc();
  const temp = code * 330.0 / ADC_MAX;                            // temp = ADC x 3.3 x 100 / 1023
  if (temp >= st.thr) { st.fan = true; st.buzzer = true; }
  else if (temp <= st.thr - HYST) { st.fan = false; st.buzzer = false; }
  st.time += 0.5;
  st.hist.push(temp); if (st.hist.length > 60) st.hist.shift();
  const level = st.buzzer ? 'alarm' : temp >= st.thr - 5 ? 'warn' : '';
  const line = 'Temp: ' + temp.toFixed(1).padStart(5) + ' C | ADC: ' + hex(code, 3) + ' | FAN ' + (st.fan ? 'ON ' : 'OFF') + (st.buzzer ? ' ALARM' : '');
  st.log.push({ t: st.time, text: line, level }); if (st.log.length > 14) st.log.shift();
  render(code, vin, temp);
}

// ---------------- drawing ----------------
function pad(s, n) { return (s + ' '.repeat(n)).slice(0, n); }
function drawLcd(r1, r2) {
  $('lcd').innerHTML = [r1, r2].map(r => '<div>' + [...pad(r, 16)].map(c => '<span>' + (c === ' ' ? '&nbsp;' : c) + '</span>').join('') + '</div>').join('');
}
function setState(id, on, label, cls) { $(id + 'Txt').textContent = label; $(id + 'Txt').className = on ? cls : 'off'; }

function render(code, vin, temp) {
  drawLcd('Temp: ' + temp.toFixed(1) + ' ' + '\u00B0' + 'C',
          st.buzzer ? 'ALERT! FAN ON' : 'ADC:' + hex(code, 3).slice(2) + ' FAN:' + (st.fan ? 'ON' : 'OFF'));
  $('clock').textContent = st.time.toFixed(1);
  $('fan').classList.toggle('spin', st.fan); setState('fan', st.fan, st.fan ? 'ON' : 'OFF', 'on');
  $('buz').classList.toggle('on', st.buzzer); setState('buz', st.buzzer, st.buzzer ? 'BEEP' : 'OFF', 'alarm');
  $('led').classList.toggle('on', st.buzzer); setState('led', st.buzzer, st.buzzer ? 'ON' : 'OFF', 'alarm');

  $('vin').textContent = vin.toFixed(3) + ' V';
  $('adcDec').textContent = code; $('adcHex').textContent = hex(code, 3);
  $('adcBin').textContent = code.toString(2).padStart(10, '0');
  $('ad0cr').textContent = hex(AD0CR, 8);
  const dr = ((1 << 31) >>> 0) + (CHANNEL << 24) + (code << 6);          // DONE | CHN | V/VREF
  $('ad0dr1').textContent = hex(dr >>> 0, 8);
  const bin = (dr >>> 0).toString(2).padStart(32, '0');
  $('bits').innerHTML = [...bin].map((b, i) => '<span class="' + (i === 0 ? 'done' : b === '1' ? 'one' : '') + '">' + b + '</span>').join('');
  $('formula').innerHTML =
    'Vin &nbsp;= ADC x VREF / 1023<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= ' + code + ' x 3.3 / 1023 = <b>' + (code * VREF / ADC_MAX).toFixed(3) + ' V</b><br>' +
    'Temp = Vin / 10 mV per &deg;C<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= <b>' + temp.toFixed(1) + ' &deg;C</b> &nbsp; (resolution 0.32 &deg;C / count)';

  $('term').innerHTML = st.log.map(l => '<div class="' + l.level + '">[' + l.t.toFixed(1).padStart(6) + ' s] ' + l.text + '</div>').join('');
  drawChart();
}

function drawChart() {
  const c = $('chart'), g = c.getContext('2d'), W = c.width, H = c.height, L = 38, B = 22, T = 10;
  g.clearRect(0, 0, W, H);
  const yMax = 80, y = v => T + (H - T - B) * (1 - v / yMax);
  g.font = '10px Consolas'; g.fillStyle = '#94a3b8'; g.strokeStyle = '#1e293b'; g.lineWidth = 1;
  for (let v = 0; v <= yMax; v += 20) { g.beginPath(); g.moveTo(L, y(v)); g.lineTo(W - 6, y(v)); g.stroke(); g.fillText(v + '', 8, y(v) + 3); }
  g.fillText('time (samples)', W / 2 - 30, H - 6);
  g.setLineDash([6, 4]); g.strokeStyle = '#ef4444'; g.beginPath(); g.moveTo(L, y(st.thr)); g.lineTo(W - 6, y(st.thr)); g.stroke();
  g.setLineDash([]); g.fillStyle = '#ef4444'; g.fillText('limit ' + st.thr + ' C', W - 80, y(st.thr) - 4);
  if (!st.hist.length) return;
  const stepX = (W - L - 8) / 59;
  g.strokeStyle = '#38bdf8'; g.lineWidth = 2; g.beginPath();
  st.hist.forEach((v, i) => { const x = L + i * stepX; i ? g.lineTo(x, y(v)) : g.moveTo(x, y(v)); }); g.stroke();
  const last = st.hist[st.hist.length - 1]; g.fillStyle = last >= st.thr ? '#ef4444' : '#22c55e';
  g.beginPath(); g.arc(L + (st.hist.length - 1) * stepX, y(last), 4, 0, 7); g.fill();
}

// ---------------- conversion table ----------------
(function buildTable() {
  let h = '<tr><th>Temperature (&deg;C)</th><th>LM35 voltage (mV)</th><th>ADC value (dec)</th><th>ADC value (hex)</th><th>Binary</th></tr>';
  [0, 10, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 100].forEach(t => {
    const v = t * 10, a = Math.round(v / 1000 / VREF * ADC_MAX);
    h += '<tr class="' + (t === 40 ? 'hl' : '') + '"><td>' + t + '</td><td>' + v + '</td><td>' + a + '</td><td>' + hex(a, 3) + '</td><td>' + a.toString(2).padStart(10, '0') + '</td></tr>';
  });
  $('conv').innerHTML = h;
})();

// ---------------- controls ----------------
$('amb').addEventListener('input', e => { st.amb = +e.target.value; $('ambVal').textContent = st.amb.toFixed(1); });
document.querySelectorAll('.presets button').forEach(b => b.addEventListener('click', () => setAmbient(+b.dataset.t)));
$('thr').addEventListener('change', e => { st.thr = +e.target.value; });
$('runBtn').addEventListener('click', () => {
  st.running = !st.running; $('runBtn').textContent = st.running ? 'Pause' : 'Resume';
  $('runTxt').textContent = st.running ? 'RUNNING' : 'PAUSED'; $('runLed').classList.toggle('on', st.running);
});
function setAmbient(t) { st.amb = t; $('amb').value = t; $('ambVal').textContent = t.toFixed(1); }
// run n loop passes at once (used to prepare the screenshots)
function runFast(n) { for (let i = 0; i < n; i++) tick(); }

setInterval(() => { if (st.running) tick(); }, 500);
tick();
