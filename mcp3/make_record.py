import copy,re,sys,json,os
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
W=qn
PAGES=json.load(open('pages.json')) if os.path.exists('pages.json') else {}
SPC=json.load(open('spc.json')) if os.path.exists('spc.json') else {}
NOPB=len(sys.argv)>1 and sys.argv[1]=='nopb'
OUT=sys.argv[2] if len(sys.argv)>2 else ('rec_nopb.docx' if NOPB else 'rec.docx')
d=Document('old.docx');body=d.element.body;els=list(body);final=els[-1]
def txt(el): return ''.join(t.text or '' for t in el.iter(W('w:t'))).strip()
H=[1,57,111,168,260,358,409,449,502,554,681,891,1039,1090]
names=['1a','1b','1c','2','3','4','5','6','7','8','9','10','11','12']
bounds=[h-1 for h in H]+[len(els)-1]
OLD={n:els[s:e] for n,s,e in zip(names,bounds,bounds[1:])}
def settext(p,new):
    ts=list(p.iter(W('w:t')))
    ts[0].text=new
    for t in ts[1:]: t.text=''
    ts[0].set(qn('xml:space'),'preserve')
def hdr(seg,exp,title,date):
    tbl=seg[1]; cells=list(tbl.iter(W('w:tc')))
    ps=[c.find(W('w:p')) for c in cells]
    settext(ps[0],'EXP NO.'+exp); settext(ps[1],title); settext(ps[2],'DATE: '+date)
# ---- fix stray text
for n,seg in OLD.items():
    for el in seg:
        if el.tag==W('w:p') and 'MCP record from Exp 7' in txt(el):
            for t in el.iter(W('w:t')):
                if t.text and 'MCP record from Exp 7' in t.text: t.text=t.text.replace(' MCP record from Exp 7','').replace('MCP record from Exp 7','')
for n,seg in OLD.items():
    for el in list(seg):
        if el.tag==W('w:p') and txt(el)=='\\':
            for t in el.iter(W('w:t')): t.text=''
# ---- split old 3
s3=OLD['3'];pb=s3[0];tbl_h=s3[1];sp0=s3[2]
idx={txt(e):i for i,e in enumerate(s3) if e.tag==W('w:p')}
aim_h=s3[3];aim_t=s3[4];desc_h=s3[5];desc1=s3[6];desc2=s3[7];sub_arith=s3[8]
assert txt(aim_h)=='AIM:' and txt(desc_h)=='DESCRIPTION:' and txt(sub_arith)=='ARITHMETIC OPERATIONS',[txt(x) for x in s3[3:9]]
sub_logic=[e for e in s3 if e.tag==W('w:p') and txt(e)=='LOGICAL OPERATIONS'][0]
empty=[e for e in s3 if e.tag==W('w:p') and txt(e)=='' and e.find(W('w:pPr')+'/'+W('w:pageBreakBefore')) is None][0]
res_h=[e for e in s3 if e.tag==W('w:p') and txt(e)=='RESULT:'][0]
res_t=s3[s3.index(res_h)+1]
# blocks
blocks={}
cur=None
for e in s3[9:]:
    if e.tag==W('w:p'):
        m=re.match(r'^(\d) \((i+v?|iv|v|vi|vii|viii|ix)\) (.*)$',txt(e))
        if m: cur=(m.group(1),m.group(2));blocks[cur]=[e];continue
    if cur: blocks[cur].append(e)
def blk(key,label,title=None):
    els_=[copy.deepcopy(x) for x in blocks[key]]
    # drop trailing result/spacer elements: keep until last tbl + one empty p
    out=[];tb=0
    for x in els_:
        out.append(x)
        if x.tag==W('w:tbl'): tb+=1
        if tb==2 and x.tag==W('w:p'): break
    t=txt(out[0]);m=re.match(r'^\d \(\w+\) (.*)$',t)
    settext(out[0],label+' '+(title or m.group(1)))
    return out
def mk(exp,title,date,aim,d2,sub,blist,resulttext):
    seg=[copy.deepcopy(pb),copy.deepcopy(tbl_h),copy.deepcopy(sp0),copy.deepcopy(aim_h),copy.deepcopy(aim_t),copy.deepcopy(desc_h),copy.deepcopy(desc1),copy.deepcopy(desc2),copy.deepcopy(sub)]
    hdr(seg,exp,title,date);settext(seg[4],aim);settext(seg[7],d2)
    for b_ in blist: seg+=b_
    seg+=[copy.deepcopy(empty),copy.deepcopy(empty),copy.deepcopy(res_h),copy.deepcopy(res_t)]
    settext(seg[-1],resulttext)
    return seg
NEW={}
NEW['1a']=mk('1a','ADDITION AND SUBTRACTION OF TWO 8 BIT NUMBERS','10.07.26',
 'To develop and simulate 8051 Assembly language programs for the addition and subtraction of two 8 bit numbers using Keil µVision IDE.',
 'In this experiment, the ADD and SUBB instructions of the 8051 were used to add and subtract two 8 bit hexadecimal numbers, with and without carry or borrow. The simulator was used to verify the results by monitoring the accumulator, registers and the carry flag.',sub_arith,
 [blk(('1','i'),'(i)'),blk(('1','ii'),'(ii)'),blk(('2','i'),'(iii)'),blk(('2','ii'),'(iv)')],
 'Thus, the addition and subtraction of two 8 bit numbers were successfully implemented and verified using 8051 Assembly Language in Keil µVision IDE.')
NEW['1b']=mk('1b','MULTIPLICATION AND DIVISION OF TWO 8 BIT NUMBERS','10.07.26',
 'To develop and simulate 8051 Assembly language programs for the multiplication and division of two 8 bit numbers using Keil µVision IDE.',
 'In this experiment, the MUL AB and DIV AB instructions of the 8051 were used to multiply and divide two 8 bit hexadecimal numbers. The product is obtained as a 16-bit result in registers B and A, while division gives the quotient in the accumulator and the remainder in register B. The simulator was used to verify the results.',sub_arith,
 [blk(('3','i'),'(i)'),blk(('3','ii'),'(ii)'),blk(('4','i'),'(iii)'),blk(('4','ii'),'(iv)')],
 'Thus, the multiplication and division of two 8 bit numbers were successfully implemented and verified using 8051 Assembly Language in Keil µVision IDE.')
NEW['1c']=mk('1c','LOGICAL AND & OR OF TWO 8 BIT NUMBERS','10.07.26',
 'To develop and simulate 8051 Assembly language programs for the logical AND and OR operations on two 8 bit numbers using Keil µVision IDE.',
 'In this experiment, the ANL and ORL instructions of the 8051 were used to perform the bitwise AND and OR operations on two 8 bit hexadecimal numbers. The simulator was used to verify the results by monitoring the accumulator and registers.',sub_logic,
 [blk(('5','i'),'(i)'),blk(('5','ii'),'(ii)')],
 'Thus, the logical AND and OR operations on two 8 bit numbers were successfully implemented and verified using 8051 Assembly Language in Keil µVision IDE.')
NEW['1d']=mk('1d','LOGICAL NOT & XOR OF TWO 8 BIT NUMBERS','10.07.26',
 'To develop and simulate 8051 Assembly language programs for the logical NOT and XOR operations on 8 bit numbers using Keil µVision IDE.',
 'In this experiment, the CPL instruction of the 8051 was used to find the complement (NOT) of an 8 bit number, and the XRL instruction was used to perform the bitwise XOR operation on two 8 bit hexadecimal numbers. The simulator was used to verify the results by monitoring the accumulator and registers.',sub_logic,
 [blk(('5','iv'),'(i)','Logical NOT (Complement)'),blk(('5','iii'),'(ii)','Logical XOR')],
 'Thus, the logical NOT and XOR operations on 8 bit numbers were successfully implemented and verified using 8051 Assembly Language in Keil µVision IDE.')
def moved(old,exp,title,date):
    seg=[copy.deepcopy(x) for x in OLD[old]];hdr(seg,exp,title,date);return seg
NEW['2']=moved('4','2','8051 ALP FOR DATA TRANSFER BETWEEN MEMORY BLOCKS','17.07.26')
NEW['3']=moved('5','3','8051 ALP TO FIND THE LARGEST / SMALLEST IN A GIVEN ARRAY','24.07.26')
NEW['4']=moved('6','4','8051 C PROGRAMMING FOR DELAY TIMER','31.07.26')
NEW['5']=moved('7','5','8051 C PROGRAMMING FOR PORT HANDLING OPERATIONS','07.08.26')
NEW['6']=moved('8','6','8051 C PROGRAMMING FOR INTERFACING ACTUATORS AND SENSORS','14.08.26')
NEW['7']=moved('9','7','8051 C PROGRAMMING FOR INTERFACING OUTPUT UNIT','21.08.26')
NEW['8']=moved('10','8','ARM7 PROGRAMMING TO INTERFACE LED AND LCD','28.08.26')
NEW['9']=moved('11','9','ARM7 PROGRAMMING FOR BUZZER INTERFACE','11.09.26')
NEW['10']=moved('12','10','ARM7 PROGRAMMING FOR TIMER CONTROLLING OPERATION','25.09.26')
NEW['CBS-1']=moved('1a','CBS-1','VIRTUAL LABS PROGRAMMING FOR DELAY GENERATION AND EFFECT OF CPU CLOCK','27.06.26')
NEW['CBS-2']=moved('1b','CBS-2','VIRTUAL LABS PROGRAMMING FOR I/O INTERFACING (LED AND SWITCH INTERFACING)','03.07.26')
NEW['CBS-3']=moved('1c','CBS-3','VIRTUAL LABS PROGRAMMING WITH ON-CHIP TIMERS/COUNTERS','03.07.26')
ORDER=['1a','1b','1c','1d','2','3','4','5','6','7','8','9','10','CBS-1','CBS-2','CBS-3']
# apply spacer overrides
def last_result(seg):
    c=[e for e in seg if e.tag==W('w:p') and txt(e).upper().startswith('RESULT')]
    return c[-1] if c else None
for k in ORDER:
    r=last_result(NEW[k])
    if k in SPC and r is not None:
        sp=r.find(W('w:pPr')+'/'+W('w:spacing'));sp.set(W('w:before'),str(int(SPC[k])))
# ---- rebuild body
for e in els[:-1]: body.remove(e)
# index section
def P(text='',bold=False,size=24,align='left',before=0,after=0):
    p=OxmlElement('w:p');pPr=OxmlElement('w:pPr');sp=OxmlElement('w:spacing');sp.set(W('w:before'),str(before));sp.set(W('w:after'),str(after));pPr.append(sp)
    jc=OxmlElement('w:jc');jc.set(W('w:val'),align);pPr.append(jc);p.append(pPr)
    if text:
        r=OxmlElement('w:r');rPr=OxmlElement('w:rPr');rf=OxmlElement('w:rFonts')
        for a in ('w:ascii','w:hAnsi','w:eastAsia','w:cs'): rf.set(W(a),'Times New Roman')
        rPr.append(rf)
        if bold: rPr.append(OxmlElement('w:b'))
        sz=OxmlElement('w:sz');sz.set(W('w:val'),str(size));rPr.append(sz);r.append(rPr)
        t=OxmlElement('w:t');t.text=text;t.set(qn('xml:space'),'preserve');r.append(t);p.append(r)
    return p
COLW=[700,1280,4400,1100,1000,1600]
def cell(text,w,bold=False,align='left',span=1,shade=None,sz=24,vm=None):
    tc=OxmlElement('w:tc');pr=OxmlElement('w:tcPr');tw=OxmlElement('w:tcW');tw.set(W('w:w'),str(w));tw.set(W('w:type'),'dxa');pr.append(tw)
    if span>1: gs=OxmlElement('w:gridSpan');gs.set(W('w:val'),str(span));pr.append(gs)
    bd=OxmlElement('w:tcBorders')
    for s in ('top','left','bottom','right'):
        e=OxmlElement('w:'+s);e.set(W('w:val'),'single');e.set(W('w:sz'),'6');e.set(W('w:space'),'0');e.set(W('w:color'),'000000');bd.append(e)
    pr.append(bd)
    if shade: sh=OxmlElement('w:shd');sh.set(W('w:val'),'clear');sh.set(W('w:color'),'auto');sh.set(W('w:fill'),shade);pr.append(sh)
    mar=OxmlElement('w:tcMar')
    for s,v in (('left',80),('right',80)):
        e=OxmlElement('w:'+s);e.set(W('w:w'),str(v));e.set(W('w:type'),'dxa');mar.append(e)
    pr.append(mar)
    va=OxmlElement('w:vAlign');va.set(W('w:val'),'center');pr.append(va)
    tc.append(pr)
    lines=text.split('\n') if text else ['']
    for ln in lines:
        p=P(ln,bold,sz,align,0,0);tc.append(p)
    return tc
def row(cells,h=520,header=False):
    tr=OxmlElement('w:tr');pr=OxmlElement('w:trPr');cs=OxmlElement('w:cantSplit');pr.append(cs)
    th=OxmlElement('w:trHeight');th.set(W('w:val'),str(h));th.set(W('w:hRule'),'atLeast');pr.append(th)
    if header: pr.append(OxmlElement('w:tblHeader'))
    tr.append(pr)
    for c in cells: tr.append(c)
    return tr
def pg(k):
    v=PAGES.get(k);return str(v) if v else ''
INDEX=[('1','8051 ALP to apply various addressing modes for arithmetic and logical functions',None,[
  ('a','10.07.2026','Addition & Subtraction of two 8 bit numbers','1a'),('b','10.07.2026','Multiplication & Division of two 8 bit numbers','1b'),
  ('c','10.07.2026','Logical AND & OR of two 8 bit numbers','1c'),('d','10.07.2026','Logical NOT & XOR of two 8 bit numbers','1d')]),
 ('2','8051 ALP for data transfer between memory blocks',None,[('a','17.07.2026','Transfer the block of data between two Memory locations','2'),('b','17.07.2026','Exchange the block of data between locations','2')]),
 ('3','8051 ALP to find the Largest / Smallest in a given array',None,[('a','24.07.2026','ALP Program for finding largest number of given N numbers','3'),('b','24.07.2026','ALP Program for finding smallest number of given N numbers','3')]),
 ('4','8051 C programming for delay timer',None,[('a','31.07.2026','8051 programming for timer mode 1 and enable/disable a port pin with a delay','4'),('b','31.07.2026','8051 programming with timer-based interrupt to toggle an output pin at a fixed time interval','4'),('c','31.07.2026','Universal Asynchronous Receiver Transmitter (UART) programming using 8051','4')]),
 ('5','8051 C programming for port handling operations',None,[('a','07.08.2026','To display ASCII number in a port','5'),('b','07.08.2026','I/O port programming with delay','5'),('c','07.08.2026','I/O port programming to toggle between two or more ports','5')]),
 ('6','8051 C programming for interfacing actuators and sensors',None,[('a','14.08.2026','Blinking the LED with some delay','6'),('b','14.08.2026','8051 programming to interface with LED with switch control','6')]),
 ('7','8051 C programming for interfacing output unit',None,[('a','21.08.2026','Display the input text in LCD','7'),('b','21.08.2026','LCD with switch control','7')]),
]
# sub-experiment page numbers inside multi-part experiments: use sub page map if provided
SUBP=PAGES.get('_sub',{})
tbl=OxmlElement('w:tbl');tp=OxmlElement('w:tblPr');tw=OxmlElement('w:tblW');tw.set(W('w:w'),str(sum(COLW)));tw.set(W('w:type'),'dxa');tp.append(tw)
jc=OxmlElement('w:jc');jc.set(W('w:val'),'center');tp.append(jc);lay=OxmlElement('w:tblLayout');lay.set(W('w:type'),'fixed');tp.append(lay);tbl.append(tp)
grid=OxmlElement('w:tblGrid')
for w_ in COLW:
    g=OxmlElement('w:gridCol');g.set(W('w:w'),str(w_));grid.append(g)
tbl.append(grid)
tbl.append(row([cell('Exp.\nNo.',COLW[0],True,'center'),cell('Date',COLW[1],True,'center'),cell('Name of the Experiment',COLW[2],True,'center'),cell('Page no.',COLW[3],True,'center'),cell('Marks',COLW[4],True,'center'),cell('Signature',COLW[5],True,'center')],700,True))
for num,title,_,subs in INDEX:
    tbl.append(row([cell(num+'.',COLW[0],True),cell('',COLW[1]),cell(title,sum(COLW[2:]),True,'center',span=4)],520))
    for letter,date,name,key in subs:
        pgv=str(SUBP.get(f'{key}{letter}') or pg(key))
        tbl.append(row([cell(letter+'.',COLW[0],False,'right'),cell(date,COLW[1],False,'center'),cell(name,COLW[2]),cell(pgv,COLW[3],False,'center'),cell('',COLW[4]),cell('',COLW[5])],560))
for num,date,name,key in (('8','28.08.2026','ARM7 programming to interface LED and LCD','8'),('9','11.09.2026','ARM7 programming for buzzer interface','9'),('10','25.09.2026','ARM7 programming for Timer controlling operation','10')):
    tbl.append(row([cell(num+'.',COLW[0]),cell(date,COLW[1],False,'center'),cell(name,COLW[2]),cell(pg(key),COLW[3],False,'center'),cell('',COLW[4]),cell('',COLW[5])],560))
tbl.append(row([cell('Content Beyond the Syllabus',sum(COLW),True,'center',span=6,shade='EDEDED')],520))
tbl.append(row([cell('CBS',COLW[0],True),cell('27.06.2026',COLW[1],False,'center'),cell('Virtual Lab\nProgramming for Delay Generation and Effect of CPU Clock',COLW[2]),cell(pg('CBS-1'),COLW[3],False,'center'),cell('',COLW[4]),cell('',COLW[5])],760))
tbl.append(row([cell('',COLW[0]),cell('03.07.2026',COLW[1],False,'center'),cell('Virtual Lab\nProgramming for I/O Interfacing (LED and Switch Interfacing)\nProgramming with On-Chip Timers/Counters',COLW[2]),cell((pg('CBS-2')+', '+pg('CBS-3')) if pg('CBS-2') else '',COLW[3],False,'center'),cell('',COLW[4]),cell('',COLW[5])],1100))
# average row
tbl.append(row([cell('',COLW[0]+COLW[1]+COLW[2],span=3),cell('Average',COLW[3],True,'center'),cell('',COLW[4]),cell('',COLW[5])],520))
# sectPr for index (copy of final sectPr minus header/footer)
sp_idx=copy.deepcopy(final)
for t in ('w:headerReference','w:footerReference'):
    for x in sp_idx.findall(W(t)): sp_idx.remove(x)
idx_p=P('INDEX',True,24,'center',0,240)
brk=OxmlElement('w:p');pPr=OxmlElement('w:pPr');pPr.append(sp_idx);brk.append(pPr)
top_sp=P('',False,24,'left',0,0)
newbody=[idx_p,tbl,brk]
pos=0
for e in newbody: body.insert(pos,e);pos+=1
for k in ORDER:
    for e in NEW[k]:
        body.insert(pos,e);pos+=1
# final sectPr: restart page numbers at 1
fs=body.find(W('w:sectPr'))
pn=fs.find(W('w:pgNumType'))
if pn is None:
    pn=OxmlElement('w:pgNumType');fs.find(W('w:pgBorders')).addnext(pn)
pn.set(W('w:start'),'1')
if NOPB:
    for sp in body.iter(W('w:sectPr')):
        for x in sp.findall(W('w:pgBorders')): sp.remove(x)
d.save(OUT);print('saved',OUT)
json.dump({'order':ORDER},open('order.json','w'))
