const {chromium}=require('playwright'),path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900}});
for(const [h,o] of [['dlg','out_f9.png'],['run','out_f12.png']]){await p.goto('file://'+path.resolve('isis.html')+'#'+h);await p.reload();await p.waitForTimeout(150);await p.screenshot({path:o});}
await b.close()})();
