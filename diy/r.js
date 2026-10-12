const {chromium}=require('playwright'),path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
p.on('pageerror',e=>console.log('ERR',e.message));p.on('console',m=>{if(m.type()=='error')console.log('C',m.text())});
await p.goto('file://'+path.resolve('kit.html'));await p.waitForTimeout(500);
console.log('pages',await p.evaluate(()=>window.NPAGES));
await p.pdf({path:'kit.pdf',printBackground:true,preferCSSPageSize:true});
await b.close()})();
