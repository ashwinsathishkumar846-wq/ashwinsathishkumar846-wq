const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const names=process.argv.slice(3);const ppm=parseFloat(process.argv[2]);
const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage();p.on('console',m=>console.log('C',m.text()));p.on('pageerror',e=>console.log('E',e.message));
await p.goto('http://localhost:8765/diy3d/studio.html');await p.waitForFunction(()=>window.READY,{timeout:60000});
fs.mkdirSync('rend',{recursive:true});
for(const n of names){const t=Date.now();const out=await p.evaluate(([n,ppm])=>window.renderPiece(n,ppm),[n,ppm]);
  for(const [v,url] of Object.entries(out)){fs.writeFileSync(`rend/${n}_${v}.png`,Buffer.from(url.split(',')[1],'base64'))}
  console.log(n,Object.keys(out).join(','),(Date.now()-t)+'ms')}
await b.close()})();
