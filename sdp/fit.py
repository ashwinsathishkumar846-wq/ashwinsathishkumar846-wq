import subprocess,re,json,os
N='AJAY_I_-_71812401007_SOFTWARE_DEVELOPMENT_PROCESS'
spc=json.load(open('spacers.json')) if os.path.exists('spacers.json') else {}
for it in range(6):
    json.dump(spc,open('spacers.json','w'))
    subprocess.run(['python3','build_doc.py',N+'.docx'],check=True,capture_output=True)
    subprocess.run(['soffice','--headless','--convert-to','pdf',N+'.docx'],capture_output=True)
    t=subprocess.run(['pdftotext','-bbox-layout',N+'.pdf','-'],capture_output=True,text=True).stdout
    pages=t.split('<page ')[1:]; res=[]
    for i,p in enumerate(pages,1):
        for m in re.finditer(r'<word xMin="[\d.]+" yMin="([\d.]+)"[^>]*>RESULT:</word>',p): res.append((i,float(m.group(1))))
    print(it,len(pages),len(res),[ (a,round(b)) for a,b in res if abs(b-725.16)>3])
    if len(res)!=28: print('count mismatch'); break
    bad=0
    for k,(pg,y) in enumerate(res,1):
        d=725.16-y
        if abs(d)>3:
            bad+=1; spc[str(k)]=max(0,spc.get(str(k),0)+d-1)
    if not bad:break
