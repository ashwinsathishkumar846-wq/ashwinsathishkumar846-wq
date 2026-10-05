const {chromium}=require('playwright'),path=require('path');
(async()=>{const b=await chromium.launch();const pg=await b.newPage();await pg.goto('file://'+path.resolve('page3.html'));
const keys=await pg.evaluate(()=>Object.keys(SC));
for(const k of keys){const info=await pg.evaluate(k=>({w:SC[k].w,h:SC[k].h}),k);
const ctx=await b.newContext({viewport:{width:info.w,height:info.h}});const p=await ctx.newPage();p.on('pageerror',e=>console.log('ERR',k,e.message));
await p.goto('file://'+path.resolve('page3.html')+'#'+k);await p.reload();await p.waitForTimeout(150);await p.locator('#cv').screenshot({path:`out/m${k.slice(1)}.png`});await ctx.close();console.log('ok',k)}
await b.close()})();
