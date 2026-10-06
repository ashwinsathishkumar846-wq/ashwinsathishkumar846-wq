import re,subprocess,json
def pages(a,b):
    t=subprocess.run(['pdftotext','-f',str(a),'-l',str(b),'-layout','src.pdf','-'],capture_output=True,text=True).stdout
    return t.split('\f')
def parse(txt):
    out=[];cur=None
    for raw in txt.split('\n'):
        l=raw.rstrip()
        if not l.strip(): continue
        if re.fullmatch(r'\s*\d{1,2}\s*',l): continue
        ind=len(l)-len(l.lstrip()); s=re.sub(r'\s+',' ',l.strip())
        is_head = ind<4 and (s.isupper() or re.match(r'^Step \d+:',s) or (s.endswith(':') and s.upper()==s) or re.match(r'^[A-Z][A-Z \-–/&.µ()0-9:]+:?$',s))
        if is_head and len(s)<90:
            if cur: out.append(cur)
            cur=['H',s]; 
            # step headings are followed by paragraph; finalize heading now
            out.append(cur);cur=None;continue
        if ind>=6 and not (cur and cur[0]=='P' and False):
            if cur: out.append(cur)
            cur=['P',s];continue
        if cur is None: cur=['P',s]
        else:
            if cur[1].endswith('-') : cur[1]=cur[1]+s
            else: cur[1]+=' '+s
    if cur: out.append(cur)
    return out
if __name__=='__main__':
    P=pages(4,27)
    res={}
    for i,p in enumerate(P):
        res[i+4]=parse(p)
    json.dump(res,open('parsed.json','w'),indent=1,ensure_ascii=False)
    for k in (4,5,6,7,8,9,27):
        print('=== page',k)
        for t,x in res.get(k,[]): print(t,'|',x[:110])
