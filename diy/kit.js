const cm=(v)=>f(v/10);
// ---- build objects ----
const O={};
O.cloud=oneSided(160,70,cloudArt,{cut:false});O.cloud.svg+=P(`M0 0`,{}) ;
O.past=oneSided(90,30,pill('Past','(Traditional Computing)'),{r:12});
O.present=oneSided(70,30,pill('Present','(Digital Era)'),{r:12});
O.future=oneSided(80,30,pill('Future','(AI & Beyond)'),{r:12});
O.abacus=flat2(70,70,abacusFront,abacusBack,{tab:10,r:2});
O.tag=oneSided(30,11,tagAbacus,{cut:false});O.note=oneSided(40,26,noteCard,{cut:false});O.binary=oneSided(35,40,binaryPaper,{cut:false});O.quill=oneSided(25,45,quillInk,{cut:false});
O.books=boxNet(40,35,30,{front:bookFront,back:bookBack,left:bookSide,right:bookSide,top:bookTop,bottom:bookTop});
O.monitor=flat2(70,50,monitorFront,monitorBack,{tab:6,tabW:30,cut:(w,h)=>R(0,0,w,h-14,{s:CUT,w:.3,r:2})+P(`M${w/2-5} ${h-14} L${w/2-7} ${h-3.6} Q${w/2-15} ${h-3} ${w/2-15} ${h-2.2} Q${w/2-15} ${h-.2} ${w/2} ${h-.2} Q${w/2+15} ${h-.2} ${w/2+15} ${h-2.2} Q${w/2+15} ${h-3} ${w/2+7} ${h-3.6} L${w/2+5} ${h-14}`,{s:CUT,w:.3})});
O.keyboard=oneSided(60,20,keyboardTop,{r:1.4});
O.lscreen=flat2(60,35,laptopScreen,laptopLid,{tab:8,tabW:50,r:2});
O.lbase=oneSided(60,40,laptopBase,{r:2});
O.tablet=boxNet(45,32,4,{front:tabletFront,back:tabletBack,left:edgeSilver,right:edgeSilver,top:(w,h)=>edgeSilver(w,h),bottom:edgeSilver});
O.phone=boxNet(18,38,5,{front:phoneFront,back:phoneBack,left:edgeDark,right:edgeDark,top:edgeDark,bottom:edgeDark},{tab:5});
O.robot=flat2(30,60,robotFront,robotBack,{tab:8,tabW:24,cut:(w,h)=>''});
O.brain=flat2(65,60,brainArt,null,{tab:8,tabW:40,r:7});
O.aiscreen=flat2(55,50,aiScreenArt,aiScreenBack,{tab:8,tabW:40,r:2.5});
O.aibase=boxNet(55,30,6,{front:blueTop,back:blueSide,left:blueSide,right:blueSide,top:blueSide,bottom:blueSide});
const sbN=['Generative AI','AI Assistants','Smart Content','Creative Tools','Better Tomorrow'];
sbN.forEach((n,i)=>O['sb'+i]=oneSided(45,15,signboard(n),{r:1.2}));
O.imagine=oneSided(90,18,imagineSign,{r:1.5});
O.pPast=boxNet(140,130,15,{front:soilTop,left:soilSide,right:soilSide,top:soilSide,bottom:soilSide},{noBack:true,noTab:true});
O.pPres=boxNet(160,150,20,{front:concTop,left:concSide,right:concSide,top:concSide,bottom:concFront},{noBack:true,noTab:true});
O.pFut=boxNet(130,130,20,{front:blueTop,left:blueSide,right:blueSide,top:blueSide,bottom:blueSide},{noBack:true,noTab:true});
const fas=(off,w)=>{const g=`<g transform="translate(${-off},0)">${fasciaFull(460,50)}</g>`;return {w,h:50,svg:g+cutRect(0,0,w,50)+(off>0?'':`<g>${P(`M${w} 0 L${w+0} 50`,{})}</g>`)}};
O.fas1=(()=>{const o=fas(0,232);o.svg+=R(228,0,4,50,{f:'rgba(255,255,255,.18)'})+L(228,0,228,50,{s:'#fff',w:.25,d:'1 1'})+T(230,25,'',{});return o})();
O.fas2=(()=>{const o=fas(228,232);o.svg+=L(4,0,4,50,{s:'#fff',w:.25,d:'1 1'});return o})();
const plantsO=flat2(25,38,plantArt,(w,h)=>plantArt(w,h).replace(/url\(#gLeaf2?\)/g,'#3c8a40'),{tab:6,tabW:16,cut:(w,h)=>''});
O.plant=plantsO;
O.bush=oneSided(100,14,bushStrip,{cut:false});
O.star=oneSided(8,8,starArt,{cut:false});
// ---- sheet plan ----
const SHEETS=[]; // {title,orient,items:[{o,name,dim,qty,x,y}]}
function sheet(title,orient,list,cols){SHEETS.push({title,orient,list,cols})}
// each list item: [obj,name,dim,qty,count(copies drawn)]
sheet('Title cloud, section headings & signboards','P',[[O.cloud,'Title cloud','16 × 7 cm',1],[O.past,'Heading – Past','9 × 3 cm',1],[O.present,'Heading – Present','7 × 3 cm',1],[O.future,'Heading – Future','8 × 3 cm',1],[O.sb0,'Signboard 1','4.5 × 1.5 cm',1],[O.sb1,'Signboard 2','4.5 × 1.5 cm',1],[O.sb2,'Signboard 3','4.5 × 1.5 cm',1],[O.sb3,'Signboard 4','4.5 × 1.5 cm',1],[O.sb4,'Signboard 5','4.5 × 1.5 cm',1],[O.imagine,'Sign – Imagine • Create • Innovate','9 × 1.8 cm',1]]);
sheet('PAST – Traditional Computing','P',[[O.abacus,'Abacus (front | back)','7 × 7 × 2 cm',1],[O.tag,'Label – Abacus ≈2000 BC','3 × 1.1 cm',1],[O.note,'Note card – From Abacus to Algorithms','4 × 2.6 cm',1],[O.binary,'Binary code paper','3.5 × 4 cm',1],[O.quill,'Quill & ink pot','2.5 × 4.5 cm',1],[O.books,'Stack of books (box net)','4 × 3.5 × 3 cm',1]]);
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
