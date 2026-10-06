const {chromium}=require('playwright'),path=require('path');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1920,height:1080}});const p=await ctx.newPage();
p.on('pageerror',e=>console.log('ERR',e.message));
for(const k of (process.argv.slice(2).length?process.argv.slice(2):['f2','f3','f4','f5','f6','f7','f8'])){
 await p.goto('file://'+path.resolve('page.html')+'#'+k);await p.reload();await p.waitForTimeout(150);
 await p.locator('#cv').screenshot({path:`out_${k}.png`});console.log('ok',k)}
await b.close()})();
