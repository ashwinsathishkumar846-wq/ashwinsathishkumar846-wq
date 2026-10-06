const {chromium}=require('playwright'),path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+path.resolve('r.html'));await p.waitForTimeout(300);
console.log(await p.evaluate(()=>Math.max(...[...document.body.children].map(e=>e.getBoundingClientRect().bottom))),'of 1122');
await p.pdf({path:'out.pdf',format:'A4',printBackground:true});await b.close()})();
