const TITLE='D:\\Projects\\DC_Motor_PWM\\DC_Motor_PWM.uvprojx - µVision [Non-Commercial Use License]';
const SC={};
const FILES_ST=['Startup.s'];
function main(o){return chrome({title:o.title||TITLE,pos:o.pos,tree:o.tree,bo:o.bo,boY:o.boY,pH:o.pH});}
const mdi=(b)=>A(258,106,'',`width:1654px;height:${b-106}px;background:#ababab`);
// Fig2: create project
SC.f2=()=>{
 let h=main({title:'µVision [Non-Commercial Use License]',pH:600,tree:''})+mdi(780)+buildOut({y:784,lines:[]});
 let b='';
 b+=rel(14,40,`<svg width="22" height="16"><path d="M9 3L3 8l6 5M3 8h14" fill="none" stroke="#777" stroke-width="1.6"/></svg>`)+rel(44,40,`<svg width="22" height="16"><path d="M5 3l6 5-6 5" fill="none" stroke="#bbb" stroke-width="1.6"/></svg>`)+rel(72,40,`<svg width="14" height="16"><path d="M3 12V6M0 8l3-4 3 4" fill="none" stroke="#777" stroke-width="1.5"/></svg>`);
 b+=rinp(100,36,600,'',24)+rel(108,42,'<span style="color:#444">›</span> &nbsp;This PC &nbsp;<span style="color:#444">›</span> &nbsp;Local Disk (D:) &nbsp;<span style="color:#444">›</span> &nbsp;Projects &nbsp;<span style="color:#444">›</span> &nbsp;DC_Motor_PWM',"font-size:12px")+rel(680,40,'<svg width="16" height="16"><path d="M12 5A5 5 0 103 9M12 2v4H8" fill="none" stroke="#666" stroke-width="1.4"/></svg>');
 b+=rinp(718,36,242,'<span style="color:#767676">Search DC_Motor_PWM</span>',24);
 b+=rel(16,74,'<b style="font-weight:600">Organize</b> ▾',"font-size:12px")+rel(100,74,'<b style="font-weight:600">New folder</b>')+rel(910,76,'<svg width="40" height="16"><rect x="1" y="2" width="12" height="12" fill="none" stroke="#555"/><path d="M4 6h6M4 9h6" stroke="#555"/><rect x="24" y="1" width="12" height="14" fill="#e3eefb" stroke="#4a7bb5"/></svg>');
 // nav pane
 b+=A(0,100,'','');
 const nav=[['Quick access',0,1],['Desktop',1],['Downloads',1],['Documents',1],['Pictures',1],['This PC',0,1],['Desktop',1],['Documents',1],['Downloads',1],['Local Disk (C:)',1],['Local Disk (D:)',1,0,1],['Network',0,1]];
 nav.forEach((r,i)=>{b+=rel(r[1]?32:16,110+i*21,(r[2]?'':'')+`<span style="display:inline-block;width:14px;height:11px;background:${r[0].includes('Disk')?'#8fa3bd':'#f0c75e'};vertical-align:-1px;margin-right:6px;border-radius:1px"></span>`+r[0],r[3]?'background:#cce8ff;padding:3px 40px 3px 2px;margin-left:-2px':(r[2]?'color:#1e3a8a':''))});
 b+=A(182,100,'','position:absolute;left:182px;top:100px;width:1px;height:320px;background:#e5e5e5');
 b+=rel(206,104,'Name',"color:#4c607a")+rel(552,104,'Date modified',"color:#4c607a")+rel(704,104,'Type',"color:#4c607a")+rel(880,104,'Size',"color:#4c607a");
 b+=A(188,122,'','width:640px;height:1px;background:#e5e5e5');
 b+=rel(490,200,'This folder is empty.',"color:#6d6d6d");
 b+=rel(18,430,'File <u>n</u>ame:')+rinp(100,426,710,'DC_Motor_PWM',24)+rel(18,462,'Save as <u>t</u>ype:')+rinp(100,458,710,'Project Files (*.uvprojx)',24)+A(0,0,'')+rel(790,462,'<svg width="14" height="14"><path d="M2 4l5 6 5-6" fill="none" stroke="#333" stroke-width="1.5"/></svg>');
 b+=rbtn(838,424,100,'<u>S</u>ave',1)+rbtn(838,456,100,'Cancel');
 b+=rel(14,500,'<svg width="14" height="14"><path d="M2 9l5-6 5 6" fill="none" stroke="#333" stroke-width="1.5"/></svg>&nbsp; Hide Folders',"font-size:12px");
 return h+dialog(300,170,960,540,'Create New Project',b);
};
// Fig3: select device
SC.f3=()=>{
 let h=main({tree:tree([[0,'proj','Project: DC_Motor_PWM','-'],[1,'target','Target 1','-'],[2,'folderopen','Source Group 1','+']])})+mdi(780)+buildOut({y:784,lines:[]});
 let b='';
 b+=rel(8,38,'',''); b+=`<div style="position:absolute;left:8px;top:40px;width:120px;height:22px;background:#fff;border:1px solid #a5acb8;border-bottom:0;line-height:21px;padding-left:10px;font-size:12px">Device</div><div style="position:absolute;left:128px;top:42px;width:120px;height:20px;background:#ececec;border:1px solid #c5c9d1;border-bottom:0;line-height:19px;padding-left:10px;font-size:12px">Software Packs</div>`;
 b+=A(8,62,'','width:924px;height:488px;background:#fff;border:1px solid #a5acb8');
 b+=rel(8,64,'',''); 
 // device tree
 b+=A(16,70,'','width:536px;height:476px;background:#fff;border:1px solid #828790');
 b+=A(17,71,'','width:534px;height:19px;background:#f6f7f9;border-bottom:1px solid #d4d7dd');
 b+=rel(24,74,'Device')+rel(412,74,'Vendor')+A(398,71,'','width:1px;height:19px;background:#d4d7dd');
 const rows=[[0,'– NXP (founded by Philips)'],[1,'– LPC2000'],[2,'LPC2141'],[2,'LPC2142'],[2,'LPC2144'],[2,'LPC2146'],[2,'LPC2148',1],[2,'LPC2194'],[1,'+ LPC2100'],[1,'+ LPC2200'],[1,'+ LPC2300'],[1,'+ LPC2400'],[0,'+ ST-Ericsson'],[0,'+ Texas Instruments']];
 rows.forEach((r,i)=>{const y=96+i*21; if(r[2]) b+=A(18,y-3,'',`width:530px;height:20px;background:#3399ff`)+rel(412,y+1,'NXP','color:#fff');
   b+=rel(24+r[0]*22+(r[1].startsWith('–')||r[1].startsWith('+')?0:16),y+1,r[1],r[2]?'color:#fff':'');});
 // right info
 b+=rel(572,78,'Vendor:')+rel(650,78,'<b style="font-weight:600">NXP (founded by Philips)</b>')+rel(572,104,'Device:')+rel(650,104,'<b style="font-weight:600">LPC2148</b>')+rel(572,130,'Toolset:')+rel(650,130,'<b style="font-weight:600">ARM</b>')+rel(572,160,'Search:')+rinp(650,156,172,'LPC2148');
 b+=rel(572,196,'Description:');
 b+=A(572,214,'','width:344px;height:316px;background:#fff;border:1px solid #828790');
 ['ARM7TDMI-S based high-performance 32-bit RISC','Microcontroller with Thumb extension, 512 kB on-chip','Flash ROM with ISP/IAP, 32 kB RAM + 8 kB USB RAM,','USB 2.0 Full-speed device controller,','Two 10-bit A/D converters with 14 channels in total,','10-bit D/A converter,','Two 32-bit timers/counters (with four capture and','four compare channels each), PWM unit (six outputs),','Real-Time Clock, Watchdog,','Two UARTs (16C550), two I2C, SPI and SSP,','Vectored Interrupt Controller,','Up to 45 fast GPIO lines, CPU clock up to 60 MHz.'].forEach((l,i)=>b+=rel(582,224+i*23,l));
 b+=rel(14,572,'Select a device from the database',"color:#444");
 b+=rbtn(742,566,92,'OK',1)+rbtn(844,566,92,'Cancel')+rbtn(0,0,0,'');
 return h+dialog(486,150,944,618,"Select Device for Target 'Target 1'...",b);
};
// Fig4: add new item
SC.f4=()=>{
 let h=main({tree:treeFull(FILES_ST)})+mdi(780)+buildOut({y:784,lines:[]});
 let b='';
 const items=[['C','C File (.c)',1],['C','C++ File (.cpp)'],['A','Asm File (.s)'],['H','Header File (.h)'],['T','Text File (.txt)'],['I','Image File (.*)']];
 b+=A(10,44,'','width:310px;height:252px;background:#fff;border:1px solid #828790');
 items.forEach((it,i)=>{const y=48+i*36; if(it[2]) b+=A(12,y,'','width:306px;height:34px;background:#3399ff'); b+=A(20,y+7,`<div style="width:20px;height:20px;border:1.5px solid ${it[2]?'#fff':'#3067b3'};background:#fff;color:#3067b3;font-weight:700;font-size:11px;text-align:center;line-height:17px;border-radius:2px">${it[0]}</div>`)+rel(52,y+9,it[1],it[2]?'color:#fff':'');});
 b+=A(332,44,'','width:332px;height:252px;background:#fff;border:1px solid #828790');
 b+=rel(344,60,'Creates a file with the C language<br>source code (.c).','line-height:20px;white-space:normal');
 b+=rel(10,322,'<u>N</u>ame:')+rinp(70,318,594,'main',22)+rel(10,360,'<u>L</u>ocation:')+rinp(70,356,538,'D:\\Projects\\DC_Motor_PWM\\',22)+rbtn(620,355,44,'...');
 b+=rbtn(420,420,112,'Add',1)+rbtn(550,420,112,'Close');
 return h+dialog(570,230,676,486,"Add New Item to Group 'Source Group 1'",b);
};
const CODE=hl(window.CODE_RAW);
// Fig5: editor
SC.f5=()=>main({tree:treeFull(['Startup.s','main.c']),pos:'L:1 C:1'})+editor({tabs:[['Startup.s',0],['main.c',1]],lines:CODE.slice(0,40),hl:null,bottom:812,hs:900})+buildOut({y:816,lines:[]});
// Fig6: options target
SC.f6=()=>{
 let h=main({tree:treeFull(['Startup.s','main.c'])})+editor({tabs:[['Startup.s',0],['main.c',1]],lines:CODE.slice(0,40),hl:null,bottom:812,hs:900,focus:false})+buildOut({y:816,lines:[]});
 return h+optionsDlg('target');
};
function optionsDlg(tab){
 const tabs=['Device','Target','Output','Listing','User','C/C++','Asm','Linker','Debug','Utilities'];
 const tw=[58,58,58,58,50,58,50,56,56,64];
 let b=''; let x=10;
 tabs.forEach((t,i)=>{const on=(t.toLowerCase()===tab); b+=`<div style="position:absolute;left:${x}px;top:${on?40:42}px;width:${tw[i]}px;height:${on?25:23}px;background:${on?'#fff':'#f0f0f0'};border:1px solid #a5acb8;border-bottom:${on?'1px solid #fff':'1px solid #a5acb8'};text-align:center;line-height:${on?24:22}px;font-size:12px;z-index:${on?3:1}">${t}</div>`; x+=tw[i]-1;});
 b+=A(10,64,'','width:786px;height:460px;background:#fff;border:1px solid #a5acb8;z-index:2');
 if(tab==='target'){
  b+=`<div style="position:absolute;left:0;top:0;z-index:4">`;
  b+=rel(20,78,'<b style="font-weight:600">NXP LPC2148</b>')+rel(250,104,'Xtal (MHz):')+rinp(330,100,56,'12.0',22)+'';
  b+=rel(20,140,'Operating system:')+rcombo(130,136,90,'None')+rel(20,172,'System Viewer File:')+rcombo(140,168,225,'LPC214x.SFR');
  b+=rcb(20,208,0,'Use Cross-Module Optimization')+rcb(20,230,1,'Use MicroLIB')+rcb(20,252,0,'Big Endian');
  b+=A(416,88,'','width:372px;height:128px;border:1px solid #bbb')+rel(424,80,'Code Generation',"background:#fff;padding:0 3px")+rel(424,112,'ARM Compiler:')+rcombo(510,108,270,'Use default compiler version 5')+rel(424,148,'Mode:')+rrb(480,148,1,'ARM')+rrb(570,148,0,'Thumb');
  const ro=(y,l,ch,st,sz,sr)=>rel(42,y,l)+rcb(20,y+1,ch,'')+rcb(100,y+1,0,'')+rinp(150,y-3,70,st||'',22)+rinp(230,y-3,70,sz||'',22)+`<div class="rb ${sr?'k':''}" style="left:338px;top:${y+1}px"></div>`;
  b+=rel(20,300,'<b style="font-weight:600">Read/Only Memory Areas</b>')+rel(20,326,'default',"font-size:11px")+rel(76,326,'off-chip',"font-size:11px")+rel(166,326,'Start')+rel(250,326,'Size')+rel(316,326,'Startup');
  ['ROM1:','ROM2:','ROM3:','IROM1:','IROM2:'].forEach((l,i)=>{const y=350+i*30; const ir=i===3; b+=rcb(20,y+1,ir,'')+rel(42,y,l)+rcb(100,y+1,0,'')+rinp(150,y-3,70,ir?'0x0':'',22)+rinp(226,y-3,70,ir?'0x80000':'',22)+`<div class="rb ${ir?'k':''}" style="left:330px;top:${y+1}px"></div>`;});
  b+=rel(416,300,'<b style="font-weight:600">Read/Write Memory Areas</b>')+rel(416,326,'default',"font-size:11px")+rel(470,326,'off-chip',"font-size:11px")+rel(560,326,'Start')+rel(646,326,'Size')+rel(724,326,'NoInit');
  ['RAM1:','RAM2:','RAM3:','IRAM1:','IRAM2:'].forEach((l,i)=>{const y=350+i*30; const ir=i===3; b+=rcb(416,y+1,ir,'')+rel(438,y,l)+rcb(496,y+1,0,'')+rinp(536,y-3,86,ir?'0x40000000':'',22)+rinp(628,y-3,70,ir?'0x8000':'',22)+`<div class="cb" style="left:736px;top:${y+1}px"></div>`;});
  b+='</div>';
 }
 if(tab==='output'){
  b+=`<div style="position:absolute;left:0;top:0;z-index:4">`;
  b+=rbtn(20,82,200,'Select Folder for Objects...')+rel(240,86,'Name of Executable:')+rinp(360,82,300,'DC_Motor_PWM',22);
  b+=rrb(20,128,1,'Create Executable:')+rinp(180,124,420,'.\\Objects\\DC_Motor_PWM',22);
  b+=rcb(44,162,1,'Debug Information')+rcb(250,162,1,'Create HEX File')+rel(440,162,'HEX Format:')+rcombo(520,158,130,'HEX-80')+rcb(44,190,1,'Browse Information');
  b+=rrb(20,226,0,'Create Library:')+rinp(180,222,420,'.\\Objects\\DC_Motor_PWM.lib',22)+rcb(20,262,0,'Create Batch File');
  b+=A(12,300,'','width:770px;height:1px;background:#d0d0d0');
  b+=rel(20,312,'<b style="font-weight:600">After Build/Rebuild</b>')+rcb(20,340,0,'Beep When Complete')+rcb(20,368,0,'Start Debugging')+rcb(20,396,0,'Run #1')+rinp(110,392,420,'',22)+rbtn(540,391,40,'...')+rcb(20,424,0,'Run #2')+rinp(110,420,420,'',22)+rbtn(540,419,40,'...')+rcb(600,396,0,'Run Independent')+rcb(600,424,0,'Run Independent');
  b+='</div>';
 }
 b+=rbtn(430,540,100,'OK',1)+rbtn(542,540,100,'Cancel')+rbtn(654,540,100,'Defaults')+rbtn(766,540,40,'Help');
 return dialog(560,118,816,596,"Options for Target 'Target 1'",b);
}
const BUILD1=["Build target 'Target 1'","compiling main.c...","assembling Startup.s...","linking...","Program Size: Code=3112 RO-data=424 RW-data=48 ZI-data=1256","\".\\Objects\\DC_Motor_PWM.axf\" - 0 Error(s), 0 Warning(s).","Build Time Elapsed:  00:00:03"];
SC.f7=()=>main({tree:treeFull(['Startup.s','main.c']),boY:660,pH:520})+editor({tabs:[['Startup.s',0],['main.c',1]],lines:CODE.slice(0,24),hl:null,bottom:662,hs:900})+buildOut({y:666,lines:BUILD1});
SC.f8=()=>main({tree:treeFull(['Startup.s','main.c'])})+editor({tabs:[['Startup.s',0],['main.c',1]],lines:CODE.slice(0,40),hl:null,bottom:812,hs:900,focus:false})+buildOut({y:816,lines:BUILD1.slice(0,5).concat(['creating hex file from ".\\Objects\\DC_Motor_PWM.axf"...','".\\Objects\\DC_Motor_PWM.axf" - 0 Error(s), 0 Warning(s).','Build Time Elapsed:  00:00:04'])})+optionsDlg('output');
