const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.5 })).newPage();
  for (const [n, h] of [['ar1_novice', 'novice'], ['ar2_expert', 'expert'], ['ar3_error', 'error']]) {
    await p.goto('file://' + process.cwd() + '/ar.html#' + h); await p.reload(); await p.locator('#view').screenshot({ path: '../shots/' + n + '.png' });
  }
  await b.close();
})();
