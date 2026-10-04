import docx,copy,zipfile,shutil,re,json
from docx.shared import Pt,Inches,Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL, WD_TAB_ALIGNMENT as TA
from docx.oxml.ns import qn
d=docx.Document('tpl.docx'); P=list(d.paragraphs)
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
# CLASS / SEMESTER
p=reset(P[36],AL.LEFT,before=14); p.paragraph_format.tab_stops.add_tab_stop(W,TA.RIGHT)
add(p,'CLASS: B.E. CSE',True); add(p,'\tSEMESTER: V',True)
# certified paragraph (merge 40-42)
p=reset(P[40],AL.JUSTIFY,first=0.5,before=34,ls=1.5)
add(p,'Certified that this is the bonafide record of work done by Mr. '); add(p,'     AJAY.I     ',ul=True); add(p,' in the ')
add(p,'20CS280 SOFTWARE DEVELOPMENT PROCESS LABORATORY',True); add(p,' of this institution for V Semester during the Academic Year 2025–2026.')
# faculty / head
p=reset(P[48],AL.LEFT,before=70); p.paragraph_format.tab_stops.add_tab_stop(W,TA.RIGHT)
add(p,'Faculty In-Charge'); add(p,'\tProfessor & Head')
p=reset(P[49],AL.LEFT,before=16); add(p,'Date: '); add(p,'_'*20)
# roll number
p=reset(P[53],AL.CENTER,before=50); add(p,'ROLL NUMBER',True)
p=reset(P[54],AL.CENTER,before=6); add(p,' '*6+'71812401007'+' '*6,ul=True)
# submitted
p=reset(P[58],AL.JUSTIFY,first=0.5,before=50,ls=1.5)
add(p,'Submitted for the V semester B.E./M.Tech Practical Examination on '); add(p,' '*28,ul=True); add(p,' 2025–2026.')
# examiners
p=reset(P[63],AL.LEFT,before=70); p.paragraph_format.tab_stops.add_tab_stop(W,TA.RIGHT)
add(p,'Internal Examiner',True); add(p,'\tSubject Expert',True)
for i in (37,38,39,41,42,43,44,45,46,47,50,51,52,55,56,57,59,60,61,62):
    e=P[i]._p; assert 'w:sectPr' not in e.xml and 'w:drawing' not in e.xml
    e.getparent().remove(e)
# index
S=json.load(open('../struct.json'))
def title_case(t):
    small={'in','a','and','of','the','to','for'}
    w=t.lower().split(); return ' '.join(x if (i and x in small) else x.capitalize() for i,x in enumerate(w))
starts={1:4,2:9,3:12,4:14,5:16,6:18,7:21,8:23,9:26,10:28,11:30,12:33,13:35,14:37,15:39,16:41,17:43,18:45,19:47,20:49,21:51,22:53,23:57,24:59,25:62,26:65,27:67,28:69,29:71}
def setc(c,t):
    p=c.paragraphs[0]; rs=p.runs
    rs[0].text=t
    for r in rs[1:]: r._r.getparent().remove(r._r)
def dfmt(s):
    a,b,c=s.split('.'); return f'{int(a)}.{int(b)}.20{c}'
T=d.tables[0]
for e in S:
    r=T.rows[e['no']]; setc(r.cells[1],dfmt(e['date'])); 
    ti=title_case(e['title']).replace(' - Part',', Part')
    setc(r.cells[2],ti); setc(r.cells[3],str(starts[e['no']]))
r=T.rows[30]; setc(r.cells[1],'15.9.2026'); setc(r.cells[2],'Introduction to Win Runner'); setc(r.cells[3],'71')
d.save('front_tmp.docx')
# footer patch
zin=zipfile.ZipFile('front_tmp.docx'); zout=zipfile.ZipFile('front.docx','w',zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    b=zin.read(it.filename)
    if it.filename=='word/footer1.xml':
        s=b.decode('utf8')
        s=s.replace('<w:t>71812401021-ASHWIN</w:t>','<w:t>71812401007-AJAY.I</w:t>').replace('<w:t xml:space="preserve"> </w:t>','<w:t></w:t>').replace('<w:t>S</w:t>','<w:t></w:t>')
        b=s.encode('utf8')
    zout.writestr(it,b)
zout.close()
