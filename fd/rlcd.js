const {chromium}=require('playwright'),path=require('path');
const J=[['lcd_normal','T:32C G:210','STATUS: NORMAL'],['lcd_warn','T:56C G:240','STATUS: WARNING'],['lcd_temp','T:74C G:250','FLT:OVER TEMP'],['lcd_gas','T:33C G:820','FLT:GAS LEAK'],['lcd_estop','T:32C G:210','FLT:E-STOP'],['lcd_curr','T:34C G:215','FLT:OVER CURRENT'],['lcd_flame','T:35C G:220','FLT:FLAME'],['lcd_boot','FAULT DETECTION','SELF TEST...']];
(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:2,viewport:{width:900,height:400}});
for(const [n,a,c] of J){await p.goto('file://'+path.resolve('lcdpage.html')+'?a='+encodeURIComponent(a)+'&b='+encodeURIComponent(c));await p.waitForTimeout(100);
 await p.locator('#o').screenshot({path:`${n}.png`});console.log(n)}
await b.close()})();
