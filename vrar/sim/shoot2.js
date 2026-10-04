const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  let p = await (await b.newContext({ viewport: { width: 1400, height: 820 }, deviceScaleFactor: 1.5 })).newPage();
  await p.goto('file://' + process.cwd() + '/unity.html'); await p.locator('#u').screenshot({ path: '../shots/u1_unity.png' });
  p = await (await b.newContext({ viewport: { width: 430, height: 840 }, deviceScaleFactor: 2 })).newPage();
  await p.goto('file://' + process.cwd() + '/mobile.html'); await p.locator('.ph').screenshot({ path: '../shots/m1_mobile.png' });
  await b.close();
})();
