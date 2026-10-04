const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [h, out] of [['', 'u1_unity.png'], ['#play', 'u2_play.png']]) {
    const p = await (await b.newContext({ viewport: { width: 1500, height: 860 }, deviceScaleFactor: 1.5 })).newPage();
    await p.goto('file://' + process.cwd() + '/unity.html' + h); await p.reload(); await p.locator('#u').screenshot({ path: '../shots/' + out });
  }
  await b.close();
})();
