import subprocess,re,json,os
N='CBS'
spc=json.load(open('spacers_cbs.json')) if os.path.exists('spacers_cbs.json') else {}
for it in range(6):
    json.dump(spc,open('spacers_cbs.json','w'))
    subprocess.run(['python3','build_cbs.py',N+'.docx'],check=True,capture_output=True)
    subprocess.run(['soffice','--headless','--convert-to','pdf',N+'.docx'],capture_output=True)
    t=subprocess.run(['pdftotext','-bbox-layout',N+'.pdf','-'],capture_output=True,text=True).stdout
    pages=t.split('<page ')[1:]; res=[]
    for i,p in enumerate(pages,1):
        for m in re.finditer(r'<word xMin="[\d.]+" yMin="([\d.]+)"[^>]*>RESULT:</word>',p): res.append((i,float(m.group(1))))
    print(it,len(pages),len(res),[ (a,round(b)) for a,b in res if abs(b-725.16)>3])
    if len(res)!=1: print('count mismatch'); break
    bad=0
    for k,(pg,y) in enumerate(res,1):
        d=725.16-y
        if abs(d)>3:
            bad+=1; spc['29']=max(0,spc.get('29',0)+d-1)
    if not bad:break
