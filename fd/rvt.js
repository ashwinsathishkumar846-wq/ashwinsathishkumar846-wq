const {chromium}=require('playwright'),path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1.5});
await p.goto('file://'+path.resolve('isis2.html')+'#vterm_full');await p.reload();await p.waitForTimeout(200);
await p.locator('#vtw').screenshot({path:'vt_full.png'});
await p.goto('file://'+path.resolve('isis2.html')+'#vterm');await p.reload();await p.waitForTimeout(200);await p.screenshot({path:'p_vterm.png'});
await b.close()})();
