const {chromium}=require('playwright'),fs=require('fs'),path=require('path');
const tr=JSON.parse(fs.readFileSync('tr7.json'));
(async()=>{const b=await chromium.launch();
for(const k in tr){for(let i=0;i<tr[k].length;i++){
 const txt=tr[k][i].replace(/&/g,'&amp;').replace(/</g,'&lt;');const n=txt.split('\n').length;
 const ctx=await b.newContext({viewport:{width:760,height:n*30+60},deviceScaleFactor:1.5});const p=await ctx.newPage();
 await p.setContent(`<style>@font-face{font-family:IC;src:url(file://${path.resolve('inconsolata-latin-400-normal.woff2')})}body{margin:0;background:#0c0c0c}pre{margin:0;padding:16px 18px;color:#f0f0f0;font:25px/30px "DejaVu Sans Mono","Liberation Mono",monospace;white-space:pre}</style><pre id=t>${txt}</pre>`);
 await p.waitForTimeout(100);await p.locator('#t').screenshot({path:`out/t${k}_${i+1}.png`});await ctx.close();}}
await b.close()})();
