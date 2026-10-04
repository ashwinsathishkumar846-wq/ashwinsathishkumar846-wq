import docx,json,re,glob
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn
S='/tmp/claude-0/-home-user-ashwinsathishkumar846-wq/cd0e2464-2e83-5cb0-be37-3d5a128c853d/scratchpad/sdp'
d=docx.Document(S+'/sdp.docx'); body=d.element.body
items=json.load(open('items.json')); rw={}
for l in open('rw.txt',encoding='utf8'):
    l=l.rstrip('\n')
    if '|' in l: k,t=l.split('|',1); rw[int(k)]=t
kids=list(body)
ok=0
for k,(i,pre,orig) in enumerate(items):
    if k not in rw: continue
    p=Paragraph(kids[i],d); t=p.text
    lw=orig[:len(orig)-len(orig.lstrip())]
    if pre: keep=0
    else:
        first=orig.split('\n')[0]
        keep=(len(first)+1) if ('\n' in orig and first.strip() and first.strip().isupper() and len(first)<60) else 0
        if keep: keep+= len(orig[keep:])-len(orig[keep:].lstrip())
    start=t.index(orig) if orig in t else 0
    keep+=start
    keep_ws=len(lw) if not pre and keep==start else 0
    keep+=keep_ws
    # numbered steps keep text as written
    new=rw[k]
    pos=0; done=False
    for r in p.runs:
        rt=r.text; end=pos+len(rt)
        if done: r.text=''
        elif end>keep or (end==keep and not rt and False):
            if pos<keep: r.text=rt[:keep-pos]+new
            else: r.text=new
            done=True
        pos=end
    if not done:  # boundary at very end: append to last run
        if p.runs: p.runs[-1].text=p.runs[-1].text+new
    ok+=1
print('rewritten',ok)
# footer
for s in d.sections:
    for p in s.footer._element.iter(qn('w:p')):
        ts=list(p.iter(qn('w:t')))
        i=0
        while i<len(ts):
            if ts[i].text=='AMIRTHA' and i+4<len(ts):
                ts[i].text='AJAY.I'
                for j in range(i+1,i+5): ts[j].text=''
                i+=5
            else:
                if ts[i].text=='71812401015': ts[i].text='71812401007'
                i+=1
# images
import os
n=0
for rel in d.part.rels.values():
    if 'image' in rel.reltype:
        part=rel.target_part; m=re.search(r'image(\d+)\.(\w+)$',str(part.partname))
        f=glob.glob(f'new/image{m.group(1)}.*')
        if f: part._blob=open(f[0],'rb').read(); n+=1
print('images',n)
cp=d.core_properties; cp.author='Ajay I'; cp.last_modified_by='Ajay I'
d.save('AJAY_I_-_71812401007_SOFTWARE_DEVELOPMENT_PROCESS.docx')
