const {chromium}=require('playwright'),path=require('path'),fs=require('fs');
(async()=>{const specs=JSON.parse(fs.readFileSync('specs.json'));
const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:2,viewport:{width:600,height:900}});
await p.goto('file://'+path.resolve('dg.html'));
for(const sp of specs){await p.evaluate(s=>render(s),sp);await p.waitForTimeout(40);await p.locator('#dg').screenshot({path:`dg/${sp.id}.png`})}
console.log(specs.length);await b.close()})();
