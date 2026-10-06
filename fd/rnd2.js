const {chromium}=require('playwright'),path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900}});
const L=process.argv.slice(2).length?process.argv.slice(2):['design','prog','normal','warn','temp','gas','estop','curr','flame'];
for(const h of L){await p.goto('file://'+path.resolve('isis2.html')+'#'+h);await p.reload();await p.waitForTimeout(200);await p.screenshot({path:`p_${h}.png`});console.log(h)}
p.on('pageerror',e=>console.log('ERR',e.message));
await b.close()})();
