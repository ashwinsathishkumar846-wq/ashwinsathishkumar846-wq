import subprocess,re,json,os
KEYS=['8a','8b','8c','8d','8e','8f','9','10','11','12']
spc={};shr={}
def measure():
    t=subprocess.run(['pdftotext','-bbox-layout','ak.pdf','-'],capture_output=True,text=True).stdout
    res=[]
    for i,p in enumerate(t.split('<page ')[1:],1):
        ys=[(float(a),float(b),c) for a,b,c in re.findall(r'<word xMin="[\d.]+" yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)">([^<]*)</word>',p)]
        for a,b,c in ys:
            if c=='RESULT:': res.append((i,a,max(y1 for y0,y1,_ in ys if y1<790)))
    return res
for it in range(8):
    json.dump(spc,open('spacers_ak.json','w'));json.dump(shr,open('shrink_ak.json','w'))
    subprocess.run(['python3','build_ak.py','ak.docx'],check=True,capture_output=True)
    subprocess.run(['soffice','--headless','--convert-to','pdf','ak.docx'],capture_output=True)
    res=measure()
    if len(res)!=len(KEYS): print('count',len(res));break
    bad=[]
    for k,(pg,y,bot) in zip(KEYS,res):
        d=779.0-bot
        if y<110: shr[k]=round(shr.get(k,1.0)*0.9,3);spc[k]=0;bad.append((k,pg,'SHRINK'))
        elif abs(d)>2.5: spc[k]=max(0,spc.get(k,0)+d-1);bad.append((k,pg,round(d)))
    print(it,bad)
    if not bad:break
