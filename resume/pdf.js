const {chromium}=require('playwright'),path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+path.resolve('resume.html'));await p.waitForTimeout(300);
const h=await p.evaluate(()=>{const b=document.body;return [b.scrollHeight,document.documentElement.scrollHeight,Math.max(...[...document.body.children].map(e=>e.getBoundingClientRect().bottom))]});console.log('content bottom px',h);
await p.pdf({path:'resume.pdf',format:'A4',printBackground:true,margin:{top:0,right:0,bottom:0,left:0}});await b.close()})();
