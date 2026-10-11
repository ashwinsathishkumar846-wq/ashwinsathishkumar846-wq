const {chromium}=require('playwright'),path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:3,viewport:{width:500,height:700}});
await p.goto('file://'+path.resolve('dg.html'));
const names=await p.evaluate(()=>window.NAMES);
for(const n of names){await p.evaluate(x=>draw(x),n);await p.locator('#o').screenshot({path:`dg/${n}.png`})}
console.log(names.join(' '));await b.close()})();
