const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const url = 'file://' + process.cwd() + '/index.html';
  const ctx = await b.newContext({ viewport: { width: 1100, height: 480 } });
  const p = await ctx.newPage();
  const snap = n => p.screenshot({ path: `shots/${n}.png`, fullPage: true });
  await p.goto(url);
  await snap('1_login');
  await p.fill('#roll', '71812401006'); await p.fill('#pwd', 'wrong1234');
  await p.click('#loginForm button'); await snap('2_login_error');
  await p.fill('#pwd', 'Srec@2026'); await p.click('#loginForm button');
  await snap('3_catalogue');
  await p.selectOption('#deptFilter', 'AI&DS'); await snap('4_filter');
  await p.selectOption('#deptFilter', 'All'); await p.fill('#search', 'web'); await snap('4b_search');
  await p.fill('#search', '');
  await p.click('text=Register >> nth=0'); await p.waitForTimeout(300); await snap('5_registered');
  // register more (20CS202, 20CS205, 20CS207) via function
  for (const c of ['20CS202', '20CS205', '20CS207']) await p.evaluate(c => registerCourse(c), c);
  await p.evaluate(() => registerCourse('20CS204'));   // clash with 20CS212 (Mon-1)
  await p.waitForTimeout(300); await snap('6_clash');
  await p.click('[data-tab=mine]'); await p.waitForTimeout(500); await p.evaluate(()=>document.getElementById('toast').classList.add('hidden')); await snap('7_mine');
  await p.click('[data-tab=timetable]'); await snap('8_timetable');
  const m = await (await b.newContext({ viewport: { width: 390, height: 800 }, deviceScaleFactor: 2 })).newPage();
  await m.goto(url); await m.fill('#roll', '71812401007'); await m.fill('#pwd', 'Srec@2026'); await m.click('#loginForm button');
  await m.screenshot({ path: 'shots/9_mobile.png', fullPage: false });
  await b.close();
})();
