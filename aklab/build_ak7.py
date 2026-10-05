import os,sys,json
os.environ['NAME']='AKHILESH RAJ P'; os.environ['ROLL']='71812401009'
sys.argv=[sys.argv[0],sys.argv[1] if len(sys.argv)>1 else 'ak7.docx']
OUT=sys.argv[1]
import wtbuild as B
from wtbuild import *
import content7 as content
from PIL import Image,ImageChops
E=content.E
SP=json.load(open('spacers_ak7.json')) if os.path.exists('spacers_ak7.json') else {}
SH=json.load(open('shrink_ak7.json')) if os.path.exists('shrink_ak7.json') else {}
def crop(path,key):
    im=Image.open(path).convert('RGB'); W,H=im.size
    if key.startswith('m') or key.startswith('t'): return im
    bg=im.getpixel((8,H-8)); rows=0
    px=im.load()
    y=H-1
    while y>0 and all(px[x,y]==bg for x in range(0,W,3)): y-=1
    return im.crop((0,0,W,min(H,y+int(H*0.04)+14)))
def addimg(key,cap,sc=1.0):
    p=f'out/{key}.png'; im=crop(p,key)
    tmp=f'out/_c_{key}.png'; im.save(tmp)
    W,H=im.size; w=min(6.0,3.9*W/H)*sc
    if key.startswith('t'): w=min(5.2,W/160)*sc
    if key.startswith('m'): w=min(6.1,3.6*W/H)*sc*{'m59':0.8,'m60':0.8,'m57':0.9,'m61':1.0}.get(key,1)
    cp=para(cap,bold=True,size=11,align=AL.CENTER,before=8,after=3,keep=True)
    q=para(align=AL.CENTER,before=0,after=6,ls=1.0)
    q.add_run().add_picture(tmp,width=Inches(w)); q.paragraph_format.keep_together=True
    # border around screenshot
OUTS={'7a':[('t7a_1','Output')],'7b':[('t7b_1','Output')],'7c':[('t7c_1','Output - correct PIN on the second attempt'),('t7c_2','Output - card blocked after three wrong attempts')],'7d':[('t7d_1','Output - total below Rs. 2000 (no discount)'),('t7d_2','Output - total of Rs. 2000 or more (10% discount)')],'7e':[('t7e_1','Output')]}
def hd(t): return para(t,bold=True,before=8,after=3,align=AL.LEFT,keep=True)
for k in content.KEYS:
    e=E[k]
    pbp=para(after=0,ls=1.0); pbp.paragraph_format.page_break_before=True
    ppr=pbp._p.get_or_add_pPr(); rp=OxmlElement('w:rPr'); rp.append(mkel('sz',val=2)); ppr.append(rp)
    title_table(k,e['date'],e['title']); para(after=2,ls=1.0,size=4)
    hd('AIM:'); para(e['aim'],left=0.3,after=4)
    hd('ALGORITHM:')
    for i,s_ in enumerate(e['steps'],1):
        p=para(left=0.55,first=-0.3,after=2.5,ls=1.1); p.paragraph_format.tab_stops.add_tab_stop(Inches(0.55))
        runx(p,f'{i}.\t',bold=True); runx(p,s_)
    hd('CODE:')
    for lab,code in e['code']:
        if lab: para(lab+':',bold=True,size=11,align=AL.LEFT,before=4,after=2,left=0.3,keep=True)
        lines=code.split('\n')
        for ln in lines:
            p=para(align=AL.LEFT,after=0,ls=1.0,left=0.3)
            r=p.add_run(ln.replace(' ',' ') if ln.strip() else ' ')
            r.font.name='Courier New'; r.font.size=Pt(9); r._r.get_or_add_rPr().rFonts.set(qn('w:hAnsi'),'Courier New'); r._r.get_or_add_rPr().rFonts.set(qn('w:cs'),'Courier New')
            p.paragraph_format.widow_control=True
    hd('OUTPUT:')
    for key,cap in OUTS[k]: addimg(key,cap,SH.get(k,1.0))
    h=hd('RESULT:'); h.paragraph_format.space_before=Pt(SP.get(k,0)); h.paragraph_format.keep_with_next=True
    q=para(e['result'],left=0.3,after=0); q.paragraph_format.keep_together=True
# schema-order fix for pPr and save (reuse module helper if present)
ORD=['pStyle','keepNext','keepLines','pageBreakBefore','framePr','widowControl','numPr','suppressLineNumbers','pBdr','shd','tabs','suppressAutoHyphens','kinsoku','wordWrap','overflowPunct','topLinePunct','autoSpaceDE','autoSpaceDN','bidi','adjustRightInd','snapToGrid','spacing','ind','contextualSpacing','mirrorIndents','suppressOverlap','jc','textDirection','textAlignment','textboxTightWrap','outlineLvl','divId','cnfStyle','rPr','sectPr','pPrChange']
def fixp(root):
    for pp in root.iter(w('pPr')):
        kids=list(pp); seen={}
        for k in kids: seen.setdefault(k.tag,k)
        kids2=sorted(seen.values(),key=lambda e:ORD.index(e.tag.split('}')[1]) if e.tag.split('}')[1] in ORD else 99)
        for k in kids: pp.remove(k)
        for k in kids2: pp.append(k)
fixp(B.dest.element); fixp(B.sec.header._element); fixp(B.sec.footer._element)
B.dest.core_properties.title='20CS279 Web Technologies Laboratory - Akhilesh Raj P - 71812401009'
B.dest.save(OUT); print('saved',OUT)
