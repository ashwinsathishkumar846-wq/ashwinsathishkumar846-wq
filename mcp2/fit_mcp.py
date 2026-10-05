import subprocess,re,json,os,fitz
KEYS=['1a','1b','1c','2','3','4','5','6','7','8','9','10','11','12']
spc=json.load(open('spacers.json')) if os.path.exists('spacers.json') else {}
def build():
    json.dump(spc,open('spacers.json','w'))
    env=dict(os.environ,NOPB_OUT='1')
    subprocess.run(['python3','build_mcp.py','mcp_nopb.docx'],check=True,env=env,capture_output=True)
    subprocess.run(['soffice','--headless','--convert-to','pdf','mcp_nopb.docx'],capture_output=True)
def measure():
    d=fitz.open('mcp_nopb.pdf'); starts=[]
    for i,p in enumerate(d):
        m=re.search(r'EXP NO\.\s*(\w+)',p.get_text())
        if m: starts.append((m.group(1),i))
    res={}
    for (k,a),nxt in zip(starts,starts[1:]+[('end',len(d))]):
        b=nxt[1]; last=None
        for pi in range(a,b):
            for x0,y0,x1,y1,t,*_ in d[pi].get_text('words'):
                if re.fullmatch(r'(?i)result:?',t) and 40<y0<800: last=(pi,y0)
        pi=last[0]; ys=[y1 for x0,y0,x1,y1,t,*_ in d[pi].get_text('words') if 40<y0 and y1<806 ]
        res[k]=(pi,last[1],max(ys),len(d[pi].get_text('words')))
    return res,len(d)
for it in range(10):
    build(); res,n=measure(); bad=[]
    for k in KEYS:
        pi,y,bot,_=res[k]; d=796-bot
        top_alone = y<80
        if abs(d)>4:
            spc[k]=max(0,spc.get(k,0)+d-2); bad.append((k,pi+1,round(d)))
    print(it,n,bad)
    if not bad: break
