const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }).catch(async()=>chromium.launch());
  const url = 'file://' + process.cwd() + '/registration.html';
  const p = await b.newPage({ viewport: { width: 1000, height: 800 } });
  await p.goto(url);
  await p.screenshot({ path: 'shots/1_empty.png', fullPage: true });
  await p.click('button[type=submit]');
  await p.screenshot({ path: 'shots/2_errors.png', fullPage: true });
  await p.click('button[type=reset]');
  await p.fill('#fullname', 'Ajay Iyanraj');
  await p.fill('#dob', '2012-05-10');
  await p.fill('#email', 'ajay.iyanraj@');
  await p.fill('#phone', '12345');
  await p.check('#male');
  await p.fill('#password', 'abc123');
  await p.fill('#confirm', 'abc124');
  await p.fill('#profile', 'linkedin.com/in/ajay');
  await p.click('#address');
  await p.screenshot({ path: 'shots/3_invalid.png', fullPage: true });
  await p.click('button[type=reset]');
  const v = { '#fullname':'Aishwarya U', '#dob':'2005-08-14', '#email':'aishwarya.u@example.com', '#phone':'9876543210',
    '#password':'Learn@2026', '#confirm':'Learn@2026', '#course':'Full Stack Web Development',
    '#startdate':'2026-10', '#experience':'1', '#profile':'https://www.linkedin.com/in/aishwarya-u',
    '#address':'12, Gandhi Street, Coimbatore - 641022' };
  for (const k in v) await p.fill(k, v[k]);
  await p.check('#female'); await p.selectOption('#qualification','Undergraduate');
  await p.fill('#hours','20'); await p.check('#terms');
  await p.click('#address');
  await p.screenshot({ path: 'shots/4_filled.png', fullPage: true });
  await p.click('button[type=submit]');
  await p.waitForTimeout(800);
  await p.evaluate(()=>window.scrollTo(0,0));
  await p.screenshot({ path: 'shots/5_success.png', fullPage: true });
  const m = await b.newPage({ viewport: { width: 390, height: 800 }, deviceScaleFactor: 2 });
  await m.goto(url);
  await m.screenshot({ path: 'shots/6_mobile.png', fullPage: true });
  await b.close();
})();
