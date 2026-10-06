import re,sys,json
from docx import Document
from docx.shared import Pt,Cm,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pygments import lex
from pygments.lexers import HtmlLexer,JavascriptLexer,CssLexer,BashLexer
from pygments.lexers.javascript import JavascriptLexer
from pygments.token import Token
try:
    from pygments.lexers import JsxLexer
except Exception:
    from pygments.lexers.jsx import JsxLexer
PAGES=json.load(open('pm.json')) if len(sys.argv)>1 else {}
BODY='Calibri';MONO='Consolas'
NAVY='1F3A5F';BLUE='2E6DB4'
d=Document()
st=d.styles['Normal'];st.font.name=BODY;st.font.size=Pt(11)
st.element.rPr.rFonts.set(qn('w:eastAsia'),BODY)
st.paragraph_format.space_after=Pt(0)
s=d.sections[0]
s.page_width=Cm(21);s.page_height=Cm(29.7);s.left_margin=s.right_margin=Cm(2.0);s.top_margin=Cm(2.1);s.bottom_margin=Cm(2.1);s.footer_distance=Cm(1.0)
sp=s._sectPr
pb=OxmlElement('w:pgBorders');pb.set(qn('w:offsetFrom'),'page')
for k in ('top','left','bottom','right'):
    e=OxmlElement('w:'+k);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'10');e.set(qn('w:space'),'22');e.set(qn('w:color'),'000000');pb.append(e)
sp.find(qn('w:pgMar')).addnext(pb)
def fnt(r,size=None,bold=None,italic=None,color=None,name=None):
    nm=name or BODY;r.font.name=nm
    rf=r._r.get_or_add_rPr().find(qn('w:rFonts'))
    for a in ('w:ascii','w:hAnsi','w:cs','w:eastAsia'): rf.set(qn(a),nm)
    if size: r.font.size=Pt(size)
    if bold is not None: r.bold=bold
    if italic is not None: r.italic=italic
    if color: r.font.color.rgb=RGBColor.from_string(color)
def shade_p(p,fill):
    pPr=p._p.get_or_add_pPr();sh=OxmlElement('w:shd');sh.set(qn('w:val'),'clear');sh.set(qn('w:color'),'auto');sh.set(qn('w:fill'),fill);pPr.append(sh)
def shade_c(c,fill):
    tcPr=c._tc.get_or_add_tcPr();sh=OxmlElement('w:shd');sh.set(qn('w:val'),'clear');sh.set(qn('w:color'),'auto');sh.set(qn('w:fill'),fill);tcPr.append(sh)
def cell_borders(c,**kw):
    tcPr=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
    for k in ('top','left','bottom','right'):
        v=kw.get(k)
        e=OxmlElement('w:'+k)
        if v: e.set(qn('w:val'),'single');e.set(qn('w:sz'),str(v[0]));e.set(qn('w:space'),'0');e.set(qn('w:color'),v[1])
        else: e.set(qn('w:val'),'nil')
        b.append(e)
    tcPr.append(b)
def cell_mar(c,top=60,bottom=60,left=140,right=140):
    tcPr=c._tc.get_or_add_tcPr();m=OxmlElement('w:tcMar')
    for k,v in (('top',top),('left',left),('bottom',bottom),('right',right)):
        e=OxmlElement('w:'+k);e.set(qn('w:w'),str(v));e.set(qn('w:type'),'dxa');m.append(e)
    tcPr.append(m)
def tbl_fixed(t,widths):
    t.autofit=False;pr=t._tbl.tblPr;l=OxmlElement('w:tblLayout');l.set(qn('w:type'),'fixed');pr.append(l)
    for row in t.rows:
        for i,c in enumerate(row.cells): c.width=Cm(widths[i])
    for i,g in enumerate(t._tbl.tblGrid.findall(qn('w:gridCol'))): g.set(qn('w:w'),str(int(widths[i]*567)))
def no_split(row):
    row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
EM={'1️⃣':'1.','2️⃣':'2.','3️⃣':'3.','4️⃣':'4.','🔥 ':'','🔥':'','🎯 ':'','🎯':'','🔴':'●','✅':'✔'}
def clean(t):
    for k,v in EM.items(): t=t.replace(k,v)
    return t
def runs(p,text,size=11,bold=False,italic=False,color=None):
    text=clean(text)
    parts=re.split(r'(\*\*.+?\*\*|`[^`]+`|⭐+)',text)
    for x in parts:
        if not x: continue
        if x.startswith('**'): fnt(p.add_run(x[2:-2]),size,True,italic,color)
        elif x.startswith('`'):
            r=p.add_run(' '+x[1:-1]+' ');fnt(r,size-1,False,False,'C7254E',MONO)
            rp=r._r.get_or_add_rPr();sh=OxmlElement('w:shd');sh.set(qn('w:val'),'clear');sh.set(qn('w:color'),'auto');sh.set(qn('w:fill'),'F1F3F5');rp.append(sh)
        elif x.startswith('⭐'): fnt(p.add_run('★'*len(x)),size,False,False,'E0A800',name='DejaVu Sans')
        else: fnt(p.add_run(x),size,bold,italic,color)
def para(text='',size=11,bold=False,italic=False,align=AL.LEFT,after=4,before=0,keep=False,left=0,color=None,line=1.15):
    p=d.add_paragraph();p.alignment=align;pf=p.paragraph_format;pf.space_after=Pt(after);pf.space_before=Pt(before);pf.keep_with_next=keep;pf.line_spacing=line
    if left: pf.left_indent=Cm(left)
    if text: runs(p,text,size,bold,italic,color)
    return p
def pbreak(): d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
def bar(text,fill=NAVY,size=15,color='FFFFFF',after=8,pbb=False):
    t=d.add_table(rows=1,cols=1);t.alignment=WD_TABLE_ALIGNMENT.CENTER;tbl_fixed(t,[17.0]);c=t.rows[0].cells[0];shade_c(c,fill);cell_mar(c,110,110,200,200)
    cell_borders(c);p=c.paragraphs[0];p.paragraph_format.keep_with_next=True
    if pbb: p.paragraph_format.page_break_before=True
    runs(p,text,size,True,False,color);no_split(t.rows[0])
    sp=d.add_paragraph();sp.paragraph_format.space_after=Pt(after);sp.paragraph_format.line_spacing=0.6;sp.paragraph_format.keep_with_next=True
def h1(t):
    p=para(t,14.5,True,after=5,before=10,keep=True,color=NAVY)
    pPr=p._p.get_or_add_pPr();b=OxmlElement('w:pBdr');e=OxmlElement('w:bottom')
    for k,v in (('val','single'),('sz','8'),('space','2'),('color',BLUE)): e.set(qn('w:'+k),v)
    b.append(e);pPr.append(b);return p
def h2(t): return para(t,12.5,True,after=4,before=8,keep=True,color=BLUE)
def h3(t): return para(t,11.5,True,after=3,before=6,keep=True,color='333333')
def bullet(t,lvl=0):
    p=para('',11,after=2,left=0.9+lvl*0.6,line=1.12);p.paragraph_format.first_line_indent=Cm(-0.45)
    fnt(p.add_run('•  '),11,True,color=BLUE);runs(p,t,11);return p
def numitem(n,t):
    p=para('',11,after=2,left=0.9,line=1.12);p.paragraph_format.first_line_indent=Cm(-0.55)
    fnt(p.add_run(f'{n}.  '),11,True,color=BLUE);runs(p,t,11);return p
def quote(lines,green=False):
    t=d.add_table(rows=1,cols=1);t.alignment=WD_TABLE_ALIGNMENT.CENTER;tbl_fixed(t,[17.0]);c=t.rows[0].cells[0]
    fill='E8F5EC' if green else 'EAF2FC';edge='2E9B57' if green else BLUE
    shade_c(c,fill);cell_mar(c,90,90,180,160);cell_borders(c,left=(36,edge))
    first=True
    for ln in lines:
        p=c.paragraphs[0] if first else c.add_paragraph();first=False
        p.paragraph_format.space_after=Pt(2);p.paragraph_format.line_spacing=1.12
        if ln=='': continue
        runs(p,ln,11,False,False,'1B1B1B')
    no_split(t.rows[0]);sp=d.add_paragraph();sp.paragraph_format.space_after=Pt(3);sp.paragraph_format.line_spacing=0.5
def mdtable(rows):
    hdr=rows[0];body=rows[2:]
    n=len(hdr);W=17.0
    lens=[max(len(clean(r[i])) if i<len(r) else 0 for r in [hdr]+body) for i in range(n)]
    tot=sum(max(l,6) for l in lens);ws=[max(2.4,W*max(l,6)/tot) for l in lens];k=W/sum(ws);ws=[w*k for w in ws]
    t=d.add_table(rows=1+len(body),cols=n);t.alignment=WD_TABLE_ALIGNMENT.CENTER;tbl_fixed(t,ws)
    pr=t._tbl.tblPr;b=OxmlElement('w:tblBorders')
    for kk in ('top','left','bottom','right','insideH','insideV'):
        e=OxmlElement('w:'+kk);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'6');e.set(qn('w:space'),'0');e.set(qn('w:color'),'8FA9C8');b.append(e)
    pr.append(b)
    for i,h in enumerate(hdr):
        c=t.rows[0].cells[i];shade_c(c,NAVY);cell_mar(c,70,70,110,110);p=c.paragraphs[0];p.alignment=AL.CENTER;runs(p,h,10.5,True,False,'FFFFFF')
    t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
    for r,row in enumerate(body):
        no_split(t.rows[r+1])
        for i in range(n):
            c=t.rows[r+1].cells[i];cell_mar(c,60,60,110,110)
            if r%2==1: shade_c(c,'EEF3FA')
            p=c.paragraphs[0];p.paragraph_format.line_spacing=1.08;runs(p,row[i] if i<len(row) else '',10.5)
    sp=d.add_paragraph();sp.paragraph_format.space_after=Pt(4);sp.paragraph_format.line_spacing=0.6
# ---------- code
BG='212121';FG='F2F2F2'
COL={Token.Keyword:'F4A6D0',Token.Name.Tag:'7CA9F7',Token.Name.Attribute:'E8D67A',Token.Literal.String:'A5D6A0',Token.Literal.Number:'F0B27A',
Token.Comment:'8A8F98',Token.Name.Function:'B9A2F2',Token.Name.Class:'B9A2F2',Token.Name.Builtin:'B9A2F2',Token.Operator.Word:'F4A6D0',Token.Name.Decorator:'B9A2F2',Token.Name.Namespace:'B9A2F2',Token.Name.Constant:'F0B27A'}
def colour(tt):
    while tt is not None:
        if tt in COL: return COL[tt]
        tt=tt.parent
    return FG
LEX={'html':HtmlLexer(),'javascript':JavascriptLexer(),'jsx':JsxLexer(),'css':CssLexer(),'bash':BashLexer()}
LABEL={'html':'HTML','javascript':'JavaScript','jsx':'JavaScript (JSX)','css':'CSS','bash':'Bash','text':''}
def codeblock(lang,lines):
    while lines and not lines[-1].strip(): lines.pop()
    while lines and not lines[0].strip(): lines.pop(0)
    plain=(lang=='text')
    t=d.add_table(rows=(1 if plain else 2),cols=1);t.alignment=WD_TABLE_ALIGNMENT.CENTER;tbl_fixed(t,[17.0])
    ri=0
    if not plain:
        c=t.rows[0].cells[0];shade_c(c,'2F2F2F');cell_mar(c,50,50,180,120);cell_borders(c)
        p=c.paragraphs[0];p.paragraph_format.keep_with_next=True
        fnt(p.add_run('</>  '),9.5,True,color='D0D0D0',name=MONO);fnt(p.add_run(LABEL[lang]),10.5,True,color='FFFFFF');no_split(t.rows[0])
    c=t.rows[ri+(0 if plain else 1)].cells[0];shade_c(c,BG);cell_mar(c,70,90,180,120);cell_borders(c)
    if len(lines)<=28: no_split(t.rows[-1])
    comp=[]
    for x in lines:
        if not x.strip() and comp and not comp[-1].strip(): continue
        comp.append(x)
    lines=comp
    src='\n'.join(lines)
    toks=list(lex(src,LEX[lang])) if not plain else [(Token.Text,src)]
    # split tokens into lines
    ln=[[]]
    for tt,val in toks:
        parts=val.split('\n')
        for i,pt in enumerate(parts):
            if i>0: ln.append([])
            if pt:
                c_=colour(tt)
                if c_==FG and tt in Token.Name and re.match(r'^([A-Z][A-Za-z]+|use[A-Z]\w+)$',pt) and lang in ('jsx','javascript'): c_='B9A2F2'
                ln[-1].append((c_,pt))
    if ln and not ln[-1]: ln.pop()
    first=True
    for L in ln:
        p=c.paragraphs[0] if first else c.add_paragraph();first=False
        pf=p.paragraph_format;pf.space_after=Pt(0);pf.line_spacing=Pt(12.2)
        if not L: 
            r=p.add_run(' ');fnt(r,8.5,color=FG,name=MONO);continue
        # leading whitespace -> nbsp
        for col,txt in L:
            txt=txt.replace(' ',' ').replace('\t',' '*4)
            fnt(p.add_run(txt),8.5,False,color=col,name=MONO)
    sp=d.add_paragraph();sp.paragraph_format.space_after=Pt(4);sp.paragraph_format.line_spacing=0.6
# ---------- footer
s.footer.is_linked_to_previous=False
fp=s.footer.paragraphs[0];fp.alignment=AL.CENTER
def fld(p,instr):
    r=p.add_run();fnt(r,10,color='555555')
    for k,tx in (('begin',None),('instr',instr),('separate',None),('text','1'),('end',None)):
        if k=='instr': e=OxmlElement('w:instrText');e.set(qn('xml:space'),'preserve');e.text=tx;r._r.append(e)
        elif k=='text': e=OxmlElement('w:t');e.text=tx;r._r.append(e)
        else: e=OxmlElement('w:fldChar');e.set(qn('w:fldCharType'),k);r._r.append(e)
fld(fp,' PAGE ')
# ---------- parse
L=open('notes.txt',encoding='utf-8').read().split('\n')
TOP=[]  # topics collected for toc
def is_topic(t): return re.match(r'^# (\d)(️⃣|\.)\s',t) is not None
# cover
para('',11,after=70)
para('WEB TECHNOLOGIES',34,True,AL.CENTER,after=6,color=NAVY,line=1.0)
para('EXAM STUDY MATERIAL',22,True,AL.CENTER,after=18,color=BLUE,line=1.0)
para('10-Mark Programs  •  2-Mark Short Answers',14,False,AL.CENTER,after=40,color='444444')
para('DOM Event Handling  ·  Node.js + MongoDB CRUD  ·  AngularJS  ·  ReactJS',12,False,AL.CENTER,after=6,color='555555')
para('NPM  ·  REST API  ·  SPA  ·  Directives  ·  Filters  ·  Modules & Controllers  ·  Node.js fs',12,False,AL.CENTER,after=70,color='555555')
para('Clean and organised notes for quick revision',11,False,AL.CENTER,color='777777')
pbreak()
para('CONTENTS',20,True,AL.CENTER,after=14,color=NAVY)
TOC10=[('1','DOM Event Handling Using JavaScript','dom'),('2','Node.js CRUD Operation Using MongoDB','node'),('3','Form Validation Using AngularJS','ng'),('4','ReactJS Application','react'),('','The 4 Programs You Should Memorize','mem4'),('','How to Prepare','prep')]
TOC2=[('1','Installation of NPM — Steps','t1'),('2','Role of REST API','t2'),('3','Traditional Website vs Single Page Application','t3'),('4','AngularJS Directives','t4'),('5','Hello World Using ReactJS','t5'),('6','Two-Way Data Binding in AngularJS','t6'),('7','Filters in AngularJS','t7'),('8','Modules and Controllers in AngularJS','t8'),('9','File Operations in Node.js','t9'),('','Last-Minute Memory Sheet','mem9')]
def toc(title,items):
    bar(title,NAVY,13,after=4)
    t=d.add_table(rows=len(items),cols=3);t.alignment=WD_TABLE_ALIGNMENT.CENTER;tbl_fixed(t,[1.4,13.2,2.4])
    for i,(n,tx,k) in enumerate(items):
        for j,v in enumerate([n,tx,str(PAGES.get(k,'#'))]):
            c=t.rows[i].cells[j];cell_mar(c,55,55,100,100);cell_borders(c,bottom=(4,'C9D3E0'))
            p=c.paragraphs[0];p.alignment=AL.CENTER if j!=1 else AL.LEFT;runs(p,v,12,j==0,False,NAVY if j==0 else None)
    d.add_paragraph().paragraph_format.space_after=Pt(10)
toc('PART A — 10-MARK QUESTIONS',TOC10)
toc('PART B — 2-MARK QUESTIONS',TOC2)
KEYS={'DOM EVENT HANDLING':'dom','NODE.JS CRUD':'node','FORM VALIDATION USING ANGULARJS':'ng','REACTJS APPLICATION':'react','THE 4 PROGRAMS':'mem4','How I would prepare':'prep','YOUR 9 QUESTIONS':'mem9'}
i=0;first_part=True;last_head='';markers=[]
def key_for(t,n):
    if n and t.startswith('# ') :
        m=re.match(r'^# (\d)',t)
        return None
    return None
while i<len(L):
    ln=L[i];s_=ln.rstrip()
    if s_ in ('10-MARK QUESTIONS','2-MARK QUESTIONS'):
        pbreak() if False else None
        bar('PART A — 10-MARK QUESTIONS' if s_.startswith('10') else 'PART B — 2-MARK QUESTIONS',NAVY,20,after=10,pbb=True)
        markers.append(('part',s_));i+=1;continue
    if s_.startswith('```'):
        lang=s_[3:].strip() or 'text';i+=1;buf=[]
        while i<len(L) and not L[i].startswith('```'): buf.append(L[i]);i+=1
        i+=1
        if lang not in LEX: lang='text'
        codeblock(lang,buf);continue
    if not s_.strip(): i+=1;continue
    if s_.strip()=='---': i+=1;continue
    if s_.startswith('|'):
        rows=[];
        while i<len(L) and L[i].startswith('|'):
            rows.append([x.strip() for x in L[i].strip().strip('|').split('|')]);i+=1
        mdtable(rows);continue
    if s_.startswith('>'):
        qs=[];
        while i<len(L) and L[i].startswith('>'):
            x=L[i][1:].strip()
            qs.append(x);i+=1
        # merge soft-wrapped lines: join unless previous raw line ended with two spaces
        out=[];
        for k,x in enumerate(qs):
            out.append(x)
        quote([clean(x) for x in out],green=('2-mark answer' in last_head))
        continue
    m=re.match(r'^(#{1,3}) (.*)',s_)
    if m:
        lv=len(m.group(1));tx=m.group(2).strip();last_head=tx
        if lv==1:
            if is_topic(s_):
                tt=clean(tx);num=re.match(r'^\d',tt)
                bar(clean(tx),BLUE,16,pbb=True)
                markers.append(('topic',clean(tx)))
            else:
                ct=clean(tx)
                if 'THE 4 PROGRAMS' in tx or 'YOUR 9 QUESTIONS' in tx or 'How I would prepare' in tx or 'YOUR 4 MASTER' in tx:
                    bar(ct,'3A6EA5',14,pbb=('YOUR 9 QUESTIONS' in tx or 'THE 4 PROGRAMS' in tx or 'How I would' in tx));markers.append(('topic',ct))
                else: h1(ct)
        elif lv==2: h2(clean(tx))
        else: h3(clean(tx))
        i+=1;continue
    mb=re.match(r'^(\s*)[-*] (.*)',s_)
    if mb: bullet(mb.group(2),1 if len(mb.group(1))>=2 else 0);i+=1;continue
    mn=re.match(r'^(\d+)\. (.*)',s_)
    if mn: numitem(mn.group(1),mn.group(2));i+=1;continue
    # paragraph (merge following non-special lines)
    buf=[s_.strip()];i+=1
    while i<len(L) and L[i].strip() and not re.match(r'^(#|```|\||>|---|[-*] |\d+\. )',L[i]):
        buf.append(L[i].strip());i+=1
    txt=' '.join(buf)
    sz=11
    p=para(txt,sz,after=5)
d.core_properties.title='Web Technologies - Exam Study Material';d.core_properties.author=''
out='Web_Technologies_Exam_Study_Material.docx' if PAGES else 'tmp_notes.docx'
d.save(out);print('saved',out)
