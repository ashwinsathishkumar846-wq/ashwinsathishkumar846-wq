const {chromium}=require('playwright'),path=require('path'),fs=require('fs');
const only=process.argv.slice(2);
(async()=>{const b=await chromium.launch();
const pg=await b.newPage();await pg.goto('file://'+path.resolve('page.html'));
const keys=await pg.evaluate(()=>Object.keys(SC));
for(const k of keys){ if(only.length&&!only.includes(k.slice(1)))continue;
 const info=await pg.evaluate(k=>({w:SC[k].w,h:SC[k].h,d:SC[k].dsf}),k);
 const ctx=await b.newContext({viewport:{width:info.w,height:info.h},deviceScaleFactor:info.d});const p=await ctx.newPage();
 p.on('pageerror',e=>console.log('ERR',k,e.message));
 await p.goto('file://'+path.resolve('page.html')+'#'+k);await p.reload();await p.waitForTimeout(80);
 await p.locator('#cv').screenshot({path:`out/image${k.slice(1)}.png`});await ctx.close();console.log('ok',k);}
await b.close()})();
