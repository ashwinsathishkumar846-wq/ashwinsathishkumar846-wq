const cm=(v)=>f(v/10);
// ---- build objects ----
const O={};
O.cloud=oneSided(160,70,cloudArt2,{cut:false});
O.past=oneSided(90,30,pill2('Past','(Traditional Computing)'),{r:12});
O.present=oneSided(70,30,pill2('Present','(Digital Era)'),{r:12});
O.future=oneSided(80,30,pill2('Future','(AI & Beyond)'),{r:12});
O.abacus=flat2(70,70,abacusFront2,abacusBack2,{tab:10,r:2});
O.tag=oneSided(30,11,tagAbacus,{cut:false});O.note=oneSided(40,26,noteCard,{cut:false});O.binary=oneSided(35,40,binaryPaper,{cut:false});O.quill=oneSided(25,45,quillInk,{cut:false});
O.book0=mkBook(BOOKS[0]);O.book1=mkBook(BOOKS[1]);O.book2=mkBook(BOOKS[2]);
O.monitor=flat2(70,50,monitorFront2,monitorBack2,{tab:6,tabW:30,cut:(w,h)=>R(0,0,w,h-14,{s:CUT,w:.3,r:2})+P(`M${w/2-5} ${h-14} L${w/2-7} ${h-3.6} Q${w/2-15} ${h-3} ${w/2-15} ${h-2.2} Q${w/2-15} ${h-.2} ${w/2} ${h-.2} Q${w/2+15} ${h-.2} ${w/2+15} ${h-2.2} Q${w/2+15} ${h-3} ${w/2+7} ${h-3.6} L${w/2+5} ${h-14}`,{s:CUT,w:.3})});
O.keyboard=oneSided(60,20,keyboardTop2,{r:1.8});
O.lscreen=flat2(60,35,laptopScreen2,laptopLid2,{tab:8,tabW:50,r:2});
O.lbase=oneSided(60,40,laptopBase2,{r:2});
O.tablet=boxNet(45,32,4,{front:tabletFront2,back:tabletBack2,left:tabEdge,right:tabEdge,top:tabEdge,bottom:tabEdge});
O.phone=boxNet(18,38,5,{front:phoneFront2,back:phoneBack2,left:phoneSide,right:phoneSideR,top:phoneTop,bottom:phoneBottom},{tab:5});
O.robot=flat2(30,60,robotFront2,robotBack2,{tab:8,tabW:24,cut:(w,h)=>''});
O.brain=flat2(65,60,brainArt2,null,{tab:8,tabW:40,r:7});
O.aiscreen=flat2(55,50,aiScreenArt2,aiScreenBack2,{tab:8,tabW:40,r:2.5});
O.aibase=boxNet(55,30,6,{front:aiBaseTop,back:aiBaseSide,left:aiBaseSide,right:aiBaseSide,top:aiBaseSide,bottom:aiBaseSide});
const sbN=['Generative AI','AI Assistants','Smart Content','Creative Tools','Better Tomorrow'];
sbN.forEach((n,i)=>O['sb'+i]=oneSided(45,15,signboard2(n),{r:1.2}));
O.imagine=oneSided(90,18,imagineSign2,{r:1.5});
O.pPast=boxNet(140,130,15,{front:soilTop2,left:soilSide2,right:soilSide2,top:soilSide2,bottom:soilSide2},{noBack:true,noTab:true});
O.pPres=boxNet(160,150,20,{front:concTop2,left:concSide2,right:concSide2,top:concSide2,bottom:concFront2},{noBack:true,noTab:true});
O.pFut=boxNet(130,130,20,{front:blueTop2,left:blueSide2,right:blueSide2,top:blueSide2,bottom:blueSide2},{noBack:true,noTab:true});
const fas=(off,w)=>{const g=`<g transform="translate(${-off},0)">${fasciaFull2(460,50)}</g>`;return {w,h:50,svg:g+cutRect(0,0,w,50)+(off>0?'':`<g>${P(`M${w} 0 L${w+0} 50`,{})}</g>`)}};
O.fas1=(()=>{const o=fas(0,232);o.svg+=R(228,0,4,50,{f:'rgba(255,255,255,.18)'})+L(228,0,228,50,{s:'#fff',w:.25,d:'1 1'})+T(230,25,'',{});return o})();
O.fas2=(()=>{const o=fas(228,232);o.svg+=L(4,0,4,50,{s:'#fff',w:.25,d:'1 1'});return o})();
const plantsO=flat2(25,38,plantArt2,(w,h)=>plantArt2(w,h).replace(/url\(#gLeaf[ABC]\)/g,'#3c8a40'),{tab:6,tabW:16,cut:(w,h)=>''});
O.plant=plantsO;
O.bush=oneSided(100,14,bushStrip,{cut:false});
O.star=oneSided(8,8,starArt,{cut:false});
// ---- sheet plan ----
const SHEETS=[]; // {title,orient,items:[{o,name,dim,qty,x,y}]}
function sheet(title,orient,list,cols){SHEETS.push({title,orient,list,cols})}
// each list item: [obj,name,dim,qty,count(copies drawn)]
sheet('Title cloud, section headings & signboards','P',[[O.cloud,'Title cloud','16 × 7 cm',1],[O.past,'Heading – Past','9 × 3 cm',1],[O.present,'Heading – Present','7 × 3 cm',1],[O.future,'Heading – Future','8 × 3 cm',1],[O.sb0,'Signboard 1','4.5 × 1.5 cm',1],[O.sb1,'Signboard 2','4.5 × 1.5 cm',1],[O.sb2,'Signboard 3','4.5 × 1.5 cm',1],[O.sb3,'Signboard 4','4.5 × 1.5 cm',1],[O.sb4,'Signboard 5','4.5 × 1.5 cm',1],[O.imagine,'Sign – Imagine • Create • Innovate','9 × 1.8 cm',1]]);
sheet('PAST – Traditional Computing','P',[[O.abacus,'Abacus (front | back)','7 × 7 × 2 cm',1],[O.tag,'Label – Abacus ≈2000 BC','3 × 1.1 cm',1],[O.note,'Note card – From Abacus to Algorithms','4 × 2.6 cm',1],[O.binary,'Binary code paper','3.5 × 4 cm',1],[O.quill,'Quill & ink pot','2.5 × 4.5 cm',1]]);
sheet('PAST – Traditional Computing: the three books','P',[[O.book0,'Book 1 – Binary (box net)','4 × 1.2 × 3 cm',1],[O.book1,'Book 2 – Logic (box net)','4 × 1.2 × 3 cm',1],[O.book2,'Book 3 – Algorithms (box net)','4 × 1.2 × 3 cm',1]]);
sheet('PRESENT – Digital Era','P',[[O.monitor,'Desktop monitor (front | back)','7 × 5 × 2 cm',1],[O.keyboard,'Keyboard (top view)','6 × 2 cm',1],[O.lscreen,'Laptop screen (front | back)','6 × 3.5 cm',1],[O.lbase,'Laptop base (top view)','6 × 4 cm',1],[O.tablet,'Tablet (box net)','4.5 × 3.2 × 0.4 cm',1],[O.phone,'Smartphone (box net)','1.8 × 3.8 × 0.5 cm',1]]);
sheet('FUTURE – AI & Beyond','P',[[O.robot,'Robot (front | back)','3 × 6 × 2.5 cm',1],[O.brain,'AI brain','6.5 × 6 cm',1],[O.aiscreen,'AI screen (front | back)','5.5 × 5 cm',1],[O.aibase,'AI screen base (box net)','5.5 × 3 × 0.6 cm',1]]);
const pl=[];for(let i=0;i<6;i++)pl.push([O.plant,i==0?'Potted plant ×6 (front | back)':'','2.5 × 3.8 cm',1]);

const dec=[[O.bush,'Foliage strip ×3','10 × 1.4 cm',1],[O.bush,'','',0],[O.bush,'','',0]];
for(let i=0;i<12;i++)dec.push([O.star,'','',0]);
[[14,9],[11,8],[9,6],[16,10],[7,5],[12,7],[10,7],[6,4],[13,8],[8,6],[15,9],[5,4]].forEach(([w,h],i)=>dec.push([oneSided(w,h,(a,b)=>rockArt(a,b,i+2),{cut:false}),'','',0]));
sheet('Plants, foliage strips, stars & rocks','P',pl.concat(dec));
sheet('Platform – PAST (soil) skin','P',[[O.pPast,'Past platform (top + 4 sides)','14 × 1.5 × 13 cm',1]]);
sheet('Platform – FUTURE (neon) skin','P',[[O.pFut,'Future platform (top + 4 sides)','13 × 2 × 13 cm',1]]);
sheet('Platform – PRESENT (concrete) skin','L',[[O.pPres,'Present platform (top + 4 sides)','16 × 2 × 15 cm',1]]);
sheet('Front fascia – left half (1/2)','L',[[O.fas1,'Fascia LEFT (0–23.2 cm)','23.2 × 5 cm',1]]);
sheet('Front fascia – right half (2/2)','L',[[O.fas2,'Fascia RIGHT (22.8–46 cm)','23.2 × 5 cm',1]]);
O.fas1.clip=true;O.fas2.clip=true;
