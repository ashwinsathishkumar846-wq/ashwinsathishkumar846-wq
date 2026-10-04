const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1400, height: 850 }, deviceScaleFactor: 1.5 })).newPage();
  for (const [name, hash] of [['k1_build', 'build'], ['k2_debug', 'debug'], ['k3_adc', 'adc'], ['k4_serial', 'serial'], ['k5_thr', 'thr'], ['k5_alarm', 'alarm'], ['k6_cool', 'cool']]) {
    await p.goto('file://' + process.cwd() + '/index.html#' + hash); await p.reload();
    await p.locator('#app').screenshot({ path: `../shots/${name}.png` });
  }
  await b.close();
})();
