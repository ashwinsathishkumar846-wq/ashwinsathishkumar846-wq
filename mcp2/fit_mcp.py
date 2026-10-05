import subprocess,re,json,os,fitz
KEYS=['1a','1b','1c','2','3','4','5','6','7','8','9','10','11','12']
spc=json.load(open('spacers.json')) if os.path.exists('spacers.json') else {}
shr=json.load(open('shrink_mcp.json')) if os.path.exists('shrink_mcp.json') else {}
def build():
    json.dump(spc,open('spacers.json','w')); json.dump(shr,open('shrink_mcp.json','w'))
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
        res[k]=(pi,last[1],max(ys),b-1-pi)
    return res,len(d)
for it in range(10):
    build(); res,n=measure(); bad=[]
    for k in KEYS:
        pi,y,bot,spill=res[k]; d=790-bot
        if spill>0:
            spc[k]=max(0,spc.get(k,0)-30); bad.append((k,pi+1,'SPILL')); continue
        top_alone = y<80
        if y<80 and k in ('4','5','6','7','3'):
            shr[k]=round(shr.get(k,1.0)*0.85,3); spc[k]=0; bad.append((k,pi+1,'SHRINK')); continue
        if abs(d)>4:
            spc[k]=max(0,spc.get(k,0)+d-2); bad.append((k,pi+1,round(d)))
    print(it,n,bad)
    if not bad: break
