const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1360, height: 800 }, deviceScaleFactor: 1.5 })).newPage();
  for (const [n, h] of [['w1_studio', 'studio'], ['w2_dash', 'dash']]) { await p.goto('file://' + process.cwd() + '/web.html#' + h); await p.reload(); await p.locator('#win').screenshot({ path: '../shots/' + n + '.png' }); }
  await b.close();
})();
