const {chromium}=require('playwright'),fs=require('fs'),path=require('path');
const specs=JSON.parse(fs.readFileSync('specs.json','utf8')); const only=process.argv.slice(2).map(Number);
(async()=>{const b=await chromium.launch();
for(const sp of specs){ if(only.length&&!only.includes(sp.n))continue;
 const ctx=await b.newContext({viewport:{width:Math.ceil(sp.W/sp.s),height:Math.ceil(sp.H/sp.s)},deviceScaleFactor:sp.s}); const p=await ctx.newPage();
 p.on('pageerror',e=>console.log('ERR',sp.n,e.message));
 await p.goto('file://'+path.resolve('ui/page.html')+'#'+encodeURIComponent(sp.scene)); await p.reload(); await p.waitForTimeout(60);
 const ext=sp.n<20?'jpeg':'png';
 await p.locator('#cv').screenshot({path:`rebuilt/image${sp.n}.png`}); await ctx.close(); console.log('ok',sp.n);}
await b.close();})();
