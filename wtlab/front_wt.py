import docx,copy,zipfile,re,json,sys
from docx.shared import Pt,Inches,Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL, WD_TAB_ALIGNMENT as TA
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
PAGES=json.load(open('pagemap.json')) if len(sys.argv)>1 and sys.argv[1]=='pages' else None
INDEX=[('1','29.06.26','Study of HTML Tags'),('2','06.07.26','Simple Blog Webpage Creation Using HTML'),('3','13.07.26','Hotspot Creation'),('4','20.07.26','Registration Form for an Application'),('5','27.07.26','College Webpage Creation Using HTML & CSS'),('6','03.08.26','Shopping Webpage Using CSS (Navigation Bar and Drop-downs)'),('7(a)','24.08.26','Electricity Bill Calculation'),('7(b)','24.08.26','Student Marks Analysis'),('7(c)','24.08.26','ATM PIN Verification'),('7(d)','24.08.26','Shopping Purchase Amount'),('7(e)','24.08.26','Employee Annual Salary'),('8(a)','07.09.26','JavaScript DOM (Hover and Clicks on a Table)'),('8(b)','07.09.26','JavaScript DOM (Real-Time Digital Clock)'),('8(c)','07.09.26','JavaScript DOM (Keyboard Interaction)'),('8(d)','07.09.26','JavaScript DOM (Simple Form with Display)'),('8(e)','07.09.26','JavaScript DOM (Mini Login System)'),('8(f)','07.09.26','JavaScript DOM (Dark/Light Mode)'),('9','21.09.26','Angular JS Form Validation'),('10','28.09.26','React JS: Components, Props, State and Events'),('11','28.09.26','React JS: Component State and Input Handling'),('12','28.09.26','Node.js and MongoDB')]
KEYS=['1','2','3','4','5','6','7(a)','7(b)','7(c)','7(d)','7(e)','8a','8b','8c','8d','8e','8f','9','10','11','12']
def dfmt(s):
    a,b,c=s.split('.'); return f'{int(a)}.{int(b)}.20{c}'
d=docx.Document('ft/tpl.docx'); P=list(d.paragraphs)
def font(r,bold=None,ul=None):
    r.font.name='Times New Roman'; r.font.size=Pt(12); r._r.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Times New Roman')
    if bold is not None: r.bold=bold
    if ul: r.underline=True
def reset(p,align=None,first=0,before=0,after=0,ls=1.0):
    for r in list(p.runs): r._r.getparent().remove(r._r)
    pPr=p._p.get_or_add_pPr()
    for t in pPr.findall(qn('w:tabs')): pPr.remove(t)
    pf=p.paragraph_format; pf.left_indent=Emu(0); pf.right_indent=Emu(0); pf.first_line_indent=Inches(first)
    pf.space_before=Pt(before); pf.space_after=Pt(after); pf.line_spacing=ls
    if align is not None: p.alignment=align
    return p
def add(p,t,bold=False,ul=False):
    r=p.add_run(t); font(r,bold,ul); return r
W=Inches(6.5)
# cover lab title (dup word)
for p in (P[17],):
    ts=[t for t in p._p.iter(qn('w:t'))]
    seen=0
    for t in ts:
        if t.text and 'LABORATORY' in t.text:
            seen+=1
            if seen>1: t.text=''
p=reset(P[36],AL.LEFT,before=14); p.paragraph_format.tab_stops.add_tab_stop(W,TA.RIGHT)
add(p,'CLASS: B.E. CSE',True); add(p,'\tSEMESTER: V',True)
p=reset(P[38],AL.JUSTIFY,first=0.5,before=34,ls=1.5)
add(p,'Certified that this is the bonafide record of work done by Mr. '); add(p,'     AJAY.I     ',ul=True); add(p,' in the ')
add(p,'20CS279 – WEB TECHNOLOGIES LABORATORY',True); add(p,' of this institution for V Semester during the Academic Year 2025–2026.')
p=reset(P[46],AL.LEFT,before=70); p.paragraph_format.tab_stops.add_tab_stop(W,TA.RIGHT)
add(p,'Faculty In-Charge'); add(p,'\tProfessor & Head')
p=reset(P[47],AL.LEFT,before=16); add(p,'Date: '); add(p,'_'*20)
p=reset(P[51],AL.CENTER,before=50); add(p,'ROLL NUMBER',True)
p=reset(P[52],AL.CENTER,before=6); add(p,' '*6+'71812401007'+' '*6,ul=True)
p=reset(P[56],AL.JUSTIFY,first=0.5,before=50,ls=1.5)
add(p,'Submitted for the V semester B.E./M.Tech Practical Examination on '); add(p,'_'*17); add(p,' 2025–2026.')
p=reset(P[61],AL.LEFT,before=70); p.paragraph_format.tab_stops.add_tab_stop(W,TA.RIGHT)
add(p,'Internal Examiner',True); add(p,'\tSubject Expert',True)
for i in list(range(37,38))+[39,40]+list(range(41,46))+[48,49,50,53,54,55,57,58,59,60]:
    e=P[i]._p; assert 'w:sectPr' not in e.xml and 'w:drawing' not in e.xml, i
    e.getparent().remove(e)
# --- index table
T=d.tables[0]; rows=T.rows
proto=copy.deepcopy(rows[1]._tr); avg=rows[-1]._tr; tbl=T._tbl
for r in list(rows[1:-1]): tbl.remove(r._tr)
def setc(c,t,bold=None):
    p=c.paragraphs[0]; rs=p.runs
    if rs:
        rs[0].text=t
        for r in rs[1:]: r._r.getparent().remove(r._r)
    else:
        r=p.add_run(t); font(r,bold)
new=[]
for k,(no,date,title) in enumerate(INDEX):
    tr=copy.deepcopy(proto); avg.addprevious(tr); new.append(tr)
rows=T.rows
for (no,date,title),r,key in zip(INDEX,rows[1:-1],KEYS):
    setc(r.cells[0],no+'.'); setc(r.cells[1],dfmt(date)); setc(r.cells[2],title)
    setc(r.cells[3],str(PAGES[key]) if PAGES else '0')
    # row height + left align title
    trPr=r._tr.get_or_add_trPr()
    for h in trPr.findall(qn('w:trHeight')): trPr.remove(h)
    h=OxmlElement('w:trHeight'); h.set(qn('w:val'),'580'); h.set(qn('w:hRule'),'atLeast'); trPr.append(h)
    for c in r.cells:
        tcPr=c._tc.get_or_add_tcPr()
        for v in tcPr.findall(qn('w:vAlign')): tcPr.remove(v)
        v=OxmlElement('w:vAlign'); v.set(qn('w:val'),'center'); tcPr.append(v)
# header row & avg row height
for r in (rows[0],rows[-1]):
    trPr=r._tr.get_or_add_trPr()
    for h in trPr.findall(qn('w:trHeight')): trPr.remove(h)
    h=OxmlElement('w:trHeight'); h.set(qn('w:val'),'600'); h.set(qn('w:hRule'),'atLeast'); trPr.append(h)
# table width/centering
tblPr=tbl.tblPr
for e in tblPr.findall(qn('w:tblW'))+tblPr.findall(qn('w:jc'))+tblPr.findall(qn('w:tblInd')): tblPr.remove(e)
widths=[0.55,0.95,3.15,0.75,0.7,1.0]
tw=OxmlElement('w:tblW'); tw.set(qn('w:w'),str(int(sum(widths)*1440))); tw.set(qn('w:type'),'dxa')
jc=OxmlElement('w:jc'); jc.set(qn('w:val'),'center')
# schema order: tblStyle,tblpPr,tblOverlap,bidiVisual,tblStyleRowBandSize,tblStyleColBandSize,tblW,jc,tblCellSpacing,tblInd,tblBorders,...
anchor=tblPr.find(qn('w:tblStyle'))
if anchor is not None: anchor.addnext(tw)
else: tblPr.insert(0,tw)
tw.addnext(jc)
grid=tbl.find(qn('w:tblGrid'))
for gc,wd in zip(grid.findall(qn('w:gridCol')),widths): gc.set(qn('w:w'),str(int(wd*1440)))
for r in T.rows:
    for c,wd in zip(r._tr.findall(qn('w:tc')),widths): pass
for r in T.rows:
    tcs=r._tr.findall(qn('w:tc'))
    if len(tcs)==6:
        for tc,wd in zip(tcs,widths):
            tcPr=tc.get_or_add_tcPr(); tcW=tcPr.find(qn('w:tcW'))
            if tcW is None: tcW=OxmlElement('w:tcW'); tcPr.insert(0,tcW)
            tcW.set(qn('w:w'),str(int(wd*1440))); tcW.set(qn('w:type'),'dxa')
    else:
        # AVERAGE row (cells may be merged) : set first tc spans
        pass
# centre cover lab line
p=P[17]; ts=[t.text for t in p._p.iter(qn('w:t'))]
p.alignment=AL.CENTER
p.paragraph_format.left_indent=Emu(0); p.paragraph_format.first_line_indent=Emu(0)
for t in p._p.iter(qn('w:t')):
    if t.text and t.text.startswith(' '): t.text=t.text.strip()
d.save('front_tmp.docx')
zin=zipfile.ZipFile('front_tmp.docx'); zout=zipfile.ZipFile('front.docx','w',zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    b=zin.read(it.filename)
    if it.filename=='word/footer1.xml':
        s=b.decode('utf8'); s=s.replace('<w:t>71812401021-ASHWIN</w:t>','<w:t>71812401007-AJAY.I</w:t>').replace('<w:t xml:space="preserve"> </w:t>','<w:t></w:t>').replace('<w:t>S</w:t>','<w:t></w:t>'); b=s.encode('utf8')
    if it.filename in ('word/header1.xml','word/header2.xml'):
        s=b.decode('utf8'); s=re.sub(r'(<w:t[^>]*>LABORATORY  </w:t>)(.*?)<w:t>LABORATORY</w:t>',lambda m:m.group(1)+m.group(2)+'<w:t></w:t>',s,flags=re.S); b=s.encode('utf8')
    zout.writestr(it,b)
zout.close(); print('front.docx ok')
