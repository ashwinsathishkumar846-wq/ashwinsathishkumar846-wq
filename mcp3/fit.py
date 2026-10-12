import subprocess,re,json,os,fitz
from docx import Document
from docx.oxml.ns import qn
ORDER=['1a','1b','1c','1d','2','3','4','5','6','7','8','9','10','CBS-1','CBS-2','CBS-3']
def init_spc():
    d=Document('rec_nopb.docx');b=list(d.element.body)
    heads=[i for i,e in enumerate(b) if e.tag==qn('w:tbl') and ''.join(t.text or '' for t in e.iter(qn('w:t'))).startswith('EXP NO.')]
    out={}
    for k,(s,e) in zip(ORDER,zip(heads,heads[1:]+[len(b)-1])):
        last=None
        for i in range(s,e):
            el=b[i]
            if el.tag==qn('w:p') and ''.join(t.text or '' for t in el.iter(qn('w:t'))).strip().upper().startswith('RESULT'): last=el
        sp=last.find(qn('w:pPr')+'/'+qn('w:spacing'));out[k]=int(sp.get(qn('w:before')))
    return out
spc=json.load(open('spc.json')) if os.path.exists('spc.json') else None
if spc is None:
    subprocess.run(['python3','make_record.py','nopb','rec_nopb.docx'],check=True,capture_output=True)
    spc=init_spc()
def build():
    json.dump(spc,open('spc.json','w'))
    subprocess.run(['python3','make_record.py','nopb','rec_nopb.docx'],check=True,capture_output=True)
    subprocess.run(['soffice','--headless','--convert-to','pdf','rec_nopb.docx'],capture_output=True)
def measure():
    d=fitz.open('rec_nopb.pdf');starts=[]
    for i,p in enumerate(d):
        m=re.search(r'EXP NO\.\s*([0-9A-Za-z\-]+)',p.get_text())
        if m: starts.append((m.group(1),i))
    res={}
    for (k,a),nxt in zip(starts,starts[1:]+[('end',len(d))]):
        b=nxt[1];last=None
        for pi in range(a,b):
            for x0,y0,x1,y1,t,*_ in d[pi].get_text('words'):
                if re.fullmatch(r'(?i)result:?',t) and 40<y0<800: last=(pi,y0)
        pi=last[0];ys=[y1 for x0,y0,x1,y1,t,*_ in d[pi].get_text('words') if 40<y0 and y1<806]
        res[k]=(pi,last[1],max(ys),b-1-pi)
    return res,len(d),starts
hi={k:v for k,v in spc.items()}
for it in range(14):
    build();res,n,starts=measure();bad=[]
    for k in ORDER:
        pi,y,bot,spill=res[k];dd=790-bot
        if spill>0 or y<80:
            hi[k]=min(hi[k],spc[k]);spc[k]=max(0,int(spc[k]*0.6) if y<80 and spc[k]>3000 else max(0,spc[k]-500));bad.append((k,pi,'TOO BIG'));continue
        if abs(dd)>4:
            spc[k]=max(0,spc[k]+int((dd-2)*20));bad.append((k,pi,round(dd)))
    print(it,n,bad,flush=True)
    if not bad:break
json.dump({k:(res[k][0],) for k in res},open('res.json','w'))
json.dump({k:a for k,a in starts},open('starts.json','w'))
