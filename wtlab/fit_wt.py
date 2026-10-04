import subprocess,re,json,os
N=os.environ.get('OUTN','merged')
spc=json.load(open('spacers.json')) if os.path.exists('spacers.json') else {}
shr=json.load(open('shrink.json')) if os.path.exists('shrink.json') else {}
keys=None
def measure():
    t=subprocess.run(['pdftotext','-bbox-layout',N+'.pdf','-'],capture_output=True,text=True).stdout
    pages=t.split('<page ')[1:]; res=[]
    for i,p in enumerate(pages,1):
        words=[(float(a),float(b),float(c)) for a,b,c in re.findall(r'<word xMin="[\d.]+" yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)"[^>]*>([^<]*)</word>',p) and []] if False else []
        ws=re.findall(r'<word xMin="[\d.]+" yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)">([^<]*)</word>',p)
        ys=[(float(a),float(b),c) for a,b,c in ws]
        for a,b,c in ys:
            if re.fullmatch(r'RESULT:?',c): 
                body=[y1 for y0,y1,_ in ys if y1<790]
                res.append((i,a,max(body)))
    return res
for it in range(8):
    json.dump(spc,open('spacers.json','w')); json.dump(shr,open('shrink.json','w'))
    subprocess.run(['python3','wtbuild.py',N+'.docx'],check=True,capture_output=True)
    subprocess.run(['soffice','--headless','--convert-to','pdf',N+'.docx'],capture_output=True)
    res=measure()
    ukeys=['1','2','3','4','5','6','7(a)','7(b)','7(c)','7(d)','7(e)','8a','8b','8c','8d','8e','8f','9','10','11','12']
    if len(res)!=21: print('count',len(res)); break
    bad=[]
    for k,(pg,y,bot) in zip(ukeys,res):
        d=779.0-bot
        flag=''
        if y<110 and k not in('1',):   # result alone at top of page -> shrink
            shr[k]=round(shr.get(k,1.0)*0.9,3); flag='SHRINK'; spc[k]=0
        elif abs(d)>2.5:
            spc[k]=max(0,spc.get(k,0)+d-1)
        else: continue
        bad.append((k,pg,round(y),round(bot),flag))
    print(it,bad)
    if not bad: break
