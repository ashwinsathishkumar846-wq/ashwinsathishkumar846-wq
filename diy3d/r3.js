const {chromium}=require('playwright'),path=require('path'),fs=require('fs');
(async()=>{const S=parseFloat(process.argv[2]||'1.5');const b=await chromium.launch();
const p=await b.newPage({deviceScaleFactor:S,viewport:{width:1200,height:1200}});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+path.resolve('kit3.html'));await p.waitForTimeout(3000);
const n=await p.evaluate(()=>document.querySelectorAll('.pg').length);fs.mkdirSync('pg',{recursive:true});
for(let i=0;i<n;i++){await p.locator('.pg').nth(i).screenshot({path:`pg/p${String(i+1).padStart(2,'0')}.jpg`,type:'jpeg',quality:93});}
console.log('pages',n);await b.close()})();
