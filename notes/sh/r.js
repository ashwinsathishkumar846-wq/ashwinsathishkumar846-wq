const {chromium}=require('playwright'),path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:2,viewport:{width:1000,height:700}});
for(const k of ['dom','node','ng','react','npm','hello','bind','filt','mod','fs']){await p.goto('file://'+path.resolve('shots.html')+'#'+k);await p.reload();await p.waitForTimeout(100);await p.locator('#shot').screenshot({path:`s_${k}.png`});console.log(k)}
await b.close()})();
