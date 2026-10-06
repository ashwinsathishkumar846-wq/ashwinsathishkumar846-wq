s=open('build_notes.py').read()
def R(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
R("st.font.size=Pt(11)","st.font.size=Pt(8.3)")
R("s.left_margin=s.right_margin=Cm(2.0);s.top_margin=Cm(2.1);s.bottom_margin=Cm(2.1);s.footer_distance=Cm(1.0)","s.left_margin=s.right_margin=Cm(1.1);s.top_margin=Cm(1.2);s.bottom_margin=Cm(1.4);s.footer_distance=Cm(0.45)")
R("e.set(qn('w:space'),'22')","e.set(qn('w:space'),'14')")
s=s.replace("17.0","W")
R("BODY='Calibri';MONO='Consolas'","BODY='Calibri';MONO='Consolas';W=9.2")
R("def runs(p,text,size=11,","def runs(p,text,size=8.3,")
R("def para(text='',size=11,bold=False,italic=False,align=AL.LEFT,after=4,before=0,keep=False,left=0,color=None,line=1.15):","def para(text='',size=8.3,bold=False,italic=False,align=AL.LEFT,after=2,before=0,keep=False,left=0,color=None,line=1.0):")
R("p=para(t,14.5,True,after=5,before=10,keep=True,color=NAVY)","p=para(t,10.2,True,after=3,before=6,keep=True,color=NAVY)")
R("def h2(t): return para(t,12.5,True,after=4,before=8,keep=True,color=BLUE)","def h2(t): return para(t,9.3,True,after=2,before=5,keep=True,color=BLUE)")
R("def h3(t): return para(t,11.5,True,after=3,before=6,keep=True,color='333333')","def h3(t): return para(t,8.7,True,after=1.5,before=3,keep=True,color='333333')")
a=s.index('def bullet');b=s.index('def quote')
s=s[:a]+'''def bullet(t,lvl=0):
    p=para('',8.3,after=1,left=0.5+lvl*0.4,line=1.0);p.paragraph_format.first_line_indent=Cm(-0.32)
    fnt(p.add_run('•\\u00A0'),8.3,True,color=BLUE);runs(p,t,8.3);return p
def numitem(n,t):
    p=para('',8.3,after=1,left=0.55,line=1.0);p.paragraph_format.first_line_indent=Cm(-0.4)
    fnt(p.add_run(f'{n}.\\u00A0'),8.3,True,color=BLUE);runs(p,t,8.3);return p
'''+s[b:]
R("shade_c(c,fill);cell_mar(c,90,90,180,160);cell_borders(c,left=(36,edge))","shade_c(c,fill);cell_mar(c,40,40,100,90);cell_borders(c,left=(30,edge))")
R("p.paragraph_format.space_after=Pt(2);p.paragraph_format.line_spacing=1.12\n        if ln=='': continue\n        runs(p,ln,11,False,False,'1B1B1B')","p.paragraph_format.space_after=Pt(1);p.paragraph_format.line_spacing=1.0\n        if ln=='': continue\n        runs(p,ln,8.3,False,False,'1B1B1B')")
R("sp=d.add_paragraph();sp.paragraph_format.space_after=Pt(3);sp.paragraph_format.line_spacing=0.5","sp=d.add_paragraph();sp.paragraph_format.space_after=Pt(0);sp.paragraph_format.line_spacing=Pt(3)")
R("def bar(text,fill=NAVY,size=15,color='FFFFFF',after=8,pbb=False):","def bar(text,fill=NAVY,size=15,color='FFFFFF',after=8,pbb=False):\n    size=size*0.62;after=3;pbb=False")
R("cell_mar(c,110,110,200,200)","cell_mar(c,45,45,110,110)")
R("sp=d.add_paragraph();sp.paragraph_format.space_after=Pt(after);sp.paragraph_format.line_spacing=0.6;sp.paragraph_format.keep_with_next=True","sp=d.add_paragraph();sp.paragraph_format.space_after=Pt(0);sp.paragraph_format.line_spacing=Pt(3);sp.paragraph_format.keep_with_next=True")
R("fnt(r,size-1,False,False,'C7254E',MONO)","fnt(r,size-0.8,False,False,'B03060',MONO)")
R("ws=[max(2.4,W*max(l,6)/tot) for l in lens]","ws=[max(1.3,W*max(l,6)/tot) for l in lens]")
R("cell_mar(c,70,70,110,110);p=c.paragraphs[0];p.alignment=AL.CENTER;runs(p,h,10.5,True,False,'FFFFFF')","cell_mar(c,30,30,70,70);p=c.paragraphs[0];p.alignment=AL.CENTER;runs(p,h,7.8,True,False,'FFFFFF')")
R("cell_mar(c,60,60,110,110)\n            if r%2==1","cell_mar(c,25,25,70,70)\n            if r%2==1")
R("p.paragraph_format.line_spacing=1.08;runs(p,row[i] if i<len(row) else '',10.5)","p.paragraph_format.line_spacing=1.0;runs(p,row[i] if i<len(row) else '',7.8)")
R("sp=d.add_paragraph();sp.paragraph_format.space_after=Pt(4);sp.paragraph_format.line_spacing=0.6\n# ---------- code","sp=d.add_paragraph();sp.paragraph_format.space_after=Pt(0);sp.paragraph_format.line_spacing=Pt(3)\n# ---------- code")
R("BG='212121';FG='F2F2F2'","BG='F3F3F3';FG='1A1A1A'")
a=s.index("COL={");b=s.index("def colour")
s=s[:a]+"""COL={Token.Keyword:'9B2D8B',Token.Name.Tag:'2F4B8F',Token.Name.Attribute:'7A5A12',Token.Literal.String:'2E7D32',Token.Literal.Number:'9C4A6B',
Token.Comment:'7A7F87',Token.Name.Function:'6A3FB5',Token.Name.Class:'6A3FB5',Token.Name.Builtin:'6A3FB5',Token.Operator.Word:'9B2D8B',Token.Name.Decorator:'6A3FB5',Token.Name.Namespace:'6A3FB5',Token.Name.Constant:'9C4A6B'}
"""+s[b:]
R("c_='B9A2F2'","c_='6A3FB5'")
R("shade_c(c,'2F2F2F');cell_mar(c,50,50,180,120);cell_borders(c)","shade_c(c,BG);cell_mar(c,30,10,110,80);cell_borders(c)")
R("fnt(p.add_run('</>  '),9.5,True,color='D0D0D0',name=MONO);fnt(p.add_run(LABEL[lang]),10.5,True,color='FFFFFF')","fnt(p.add_run('</>  '),6.8,True,color='222222',name=MONO);fnt(p.add_run(LABEL[lang]),7.6,True,color='111111')")
R("cell_mar(c,70,90,180,120);cell_borders(c)\n    if len(lines)","cell_mar(c,20,50,110,80);cell_borders(c)\n    if len(lines)")
import re as _re
_m=_re.search(r"pf=p\.paragraph_format;pf\.space_after=Pt\(0\);pf\.line_spacing=Pt\(12\.2\)\n        if not L: \n            r=p\.add_run\('.'\);fnt\(r,8\.5,color=FG,name=MONO\);continue",s)
assert _m
s=s[:_m.start()]+"pf=p.paragraph_format;pf.space_after=Pt(0);pf.line_spacing=Pt(7.6)\n        if not L:\n            pf.line_spacing=Pt(3.4);r=p.add_run('\\u00A0');fnt(r,3,color=FG,name=MONO);continue"+s[_m.end():]
R("fnt(p.add_run(txt),8.5,False,color=col,name=MONO)","fnt(p.add_run(txt),6.3,False,color=col,name=MONO)")
R("sp=d.add_paragraph();sp.paragraph_format.space_after=Pt(4);sp.paragraph_format.line_spacing=0.6\n# ---------- footer","sp=d.add_paragraph();sp.paragraph_format.space_after=Pt(0);sp.paragraph_format.line_spacing=Pt(3)\n# ---------- footer")
open('build_notes2.py','w').write(s)
