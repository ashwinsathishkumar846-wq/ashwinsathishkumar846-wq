const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const job = async (f, sel, vw, vh, out, scale=1.5) => { const p = await (await b.newContext({ viewport: { width: vw, height: vh }, deviceScaleFactor: scale })).newPage(); await p.goto('file://' + process.cwd() + '/' + f); await p.locator(sel).screenshot({ path: '../shots/' + out }); };
  await job('unity.html', '#u', 1500, 880, 'u1_unity.png');
  await job('grafana.html', '#w', 1500, 860, 'w2_dash.png');
  await job('mtg.html', '#a', 1400, 800, 'w1_mtg.png');
  await job('mobile.html', '.ph', 430, 880, 'm1_mobile.png', 2);
  await b.close();
})();
