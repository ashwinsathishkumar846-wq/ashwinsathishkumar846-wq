const {chromium}=require('playwright'),path=require('path'),fs=require('fs');
const U=p=>'file://'+path.resolve(p);
const shots=[
 {id:'8a_1',page:'pages/8a.html',w:720,h:330,title:'Student List Events',url:'D:/WT_LAB/Programs/Exp8/exp8a.html',act:async p=>{}},
 {id:'8a_2',page:'pages/8a.html',w:720,h:330,title:'Student List Events',url:'D:/WT_LAB/Programs/Exp8/exp8a.html',act:async p=>{const r=p.locator('#stuTable tr');await r.nth(1).click();await r.nth(3).click();await r.nth(2).hover();}},
 {id:'8b_1',page:'pages/8b.html',w:720,h:300,title:'Live Digital Clock',url:'D:/WT_LAB/Programs/Exp8/exp8b.html',act:async p=>{await p.clock.runFor(3000)}},
 {id:'8c_1',page:'pages/8c.html',w:720,h:420,title:'Keyboard Events',url:'D:/WT_LAB/Programs/Exp8/exp8c.html',act:async p=>{}},
 {id:'8c_2',page:'pages/8c.html',w:720,h:420,title:'Keyboard Events',url:'D:/WT_LAB/Programs/Exp8/exp8c.html',act:async p=>{await p.keyboard.press('g')}},
 {id:'8d_1',page:'pages/8d.html',w:720,h:300,title:'Greeting Form',url:'D:/WT_LAB/Programs/Exp8/exp8d.html',act:async p=>{}},
 {id:'8d_2',page:'pages/8d.html',w:720,h:300,title:'Greeting Form',url:'D:/WT_LAB/Programs/Exp8/exp8d.html',act:async p=>{await p.fill('#nm','Akhilesh Raj P');await p.click('button')}},
 {id:'8e_1',page:'pages/8e.html',w:720,h:420,title:'Mini Login',url:'D:/WT_LAB/Programs/Exp8/exp8e.html',act:async p=>{await p.fill('#u','akhilesh');await p.fill('#p','wrong99');await p.click('button')}},
 {id:'8e_2',page:'pages/8e.html',w:720,h:420,title:'Mini Login',url:'D:/WT_LAB/Programs/Exp8/exp8e.html',act:async p=>{await p.fill('#u','akhilesh');await p.fill('#p','wt@1009');await p.click('button')}},
 {id:'8f_1',page:'pages/8f.html',w:720,h:300,title:'Theme Switcher',url:'D:/WT_LAB/Programs/Exp8/exp8f.html',act:async p=>{}},
 {id:'8f_2',page:'pages/8f.html',w:720,h:300,title:'Theme Switcher',url:'D:/WT_LAB/Programs/Exp8/exp8f.html',act:async p=>{await p.click('#tb');await p.waitForTimeout(500)}},
 {id:'9_1',page:'pages/9.html',w:720,h:560,title:'Course Enrolment',url:'D:/WT_LAB/Programs/Exp9/exp9.html',act:async p=>{await p.fill('input[name=nm]','Ak');await p.fill('input[name=em]','akhilesh@');await p.fill('input[name=ag]','35');await p.fill('input[name=mb]','98765');}},
 {id:'9_2',page:'pages/9.html',w:720,h:560,title:'Course Enrolment',url:'D:/WT_LAB/Programs/Exp9/exp9.html',act:async p=>{await p.fill('input[name=nm]','Akhilesh Raj P');await p.fill('input[name=em]','akhilesh.2401009@srec.ac.in');await p.fill('input[name=ag]','20');await p.fill('input[name=mb]','9876501234');await p.click('button')}},
 {id:'10_1',page:'pages/10.html',w:720,h:560,title:'react-app',url:'localhost:5173',act:async p=>{await p.waitForTimeout(600)}},
 {id:'10_2',page:'pages/10.html',w:720,h:560,title:'react-app',url:'localhost:5173',act:async p=>{await p.waitForTimeout(400);await p.click('text=Change Status');for(let i=0;i<3;i++)await p.click('text=Like');}},
 {id:'11_1',page:'pages/11.html',w:720,h:560,title:'react-app',url:'localhost:5173',act:async p=>{await p.waitForTimeout(400);await p.fill('input[name=name]','Akhilesh Raj P');await p.fill('input[name=email]','akhilesh.2401009@srec.ac.in');await p.selectOption('select','Web Technologies');}},
 {id:'11_2',page:'pages/11.html',w:720,h:640,title:'react-app',url:'localhost:5173',act:async p=>{await p.waitForTimeout(400);await p.fill('input[name=name]','Akhilesh Raj P');await p.fill('input[name=email]','akhilesh.2401009@srec.ac.in');await p.selectOption('select','Web Technologies');await p.fill('input[name=rating]','4');await p.click('button');}},
];
(async()=>{const b=await chromium.launch();const only=process.argv.slice(2);
for(const s of shots){ if(only.length&&!only.some(o=>s.id.startsWith(o)))continue;
 const ctx=await b.newContext({viewport:{width:s.w,height:s.h},deviceScaleFactor:1.5});const p=await ctx.newPage();
 p.on('pageerror',e=>console.log('ERR',s.id,e.message));p.on('dialog',d=>d.dismiss());
 if(s.id.startsWith('8b'))await p.clock.install({time:new Date('2026-09-07T10:42:15')});
 await p.goto(U(s.page));await p.waitForTimeout(500);await s.act(p);await p.waitForTimeout(250);
 await p.screenshot({path:`out/raw_${s.id}.png`});await ctx.close();
 // compose
 const c2=await b.newContext({viewport:{width:s.w,height:s.h+120},deviceScaleFactor:1.5});const q=await c2.newPage();
 await q.goto(U('compose.html')+'#'+encodeURIComponent(JSON.stringify({id:s.id,t:s.title,u:s.url,w:s.w,h:s.h})));await q.waitForTimeout(250);
 await q.locator('#cv').screenshot({path:`out/${s.id}.png`});await c2.close();console.log('ok',s.id);}
await b.close()})();
