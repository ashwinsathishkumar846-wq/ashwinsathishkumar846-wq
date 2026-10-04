import docx,re,json
from docx.text.paragraph import Paragraph
from docx.table import Table
S='/tmp/claude-0/-home-user-ashwinsathishkumar846-wq/cd0e2464-2e83-5cb0-be37-3d5a128c853d/scratchpad/sdp'
d=docx.Document('AJAY_I_-_71812401007_SOFTWARE_DEVELOPMENT_PROCESS.docx')
rels=d.part.rels
HEADS=r'(ADVANTAGES OF USING JIRA BACKLOG|ACTIVITIES PERFORMED USING THE JIRA BACKLOG|CREATING A BACKLOG IN JIRA|FEATURES OF JIRA GADGETS|ALGORITHM\s*/\s*PROCEDURE|DESCRIPTION|PROCEDURE|ADVANTAGES|APPLICATIONS|OUTPUT|RESULT|AIM)'
exps=[]; cur=None
def blk(t,**k): cur['b'].append(dict(t=t,**k))
for e in d.element.body:
    if e.tag.endswith('}tbl'):
        tb=Table(e,d); cells=[c.text.strip() for r in tb.rows for c in r.cells]
        txt=' '.join(cells)
        m=re.search(r'EX\.?\s*NO\.?\s*(\d+)',txt); dt=re.search(r'DATE:\s*([\d\.]+)',txt)
        title=[c for c in cells if c and not re.search(r'EX\.?\s*NO|DATE',c)]
        cur=dict(no=int(m.group(1)),date=dt.group(1),title=re.sub(r'\s+',' ',title[0]).strip(),b=[]); exps.append(cur); continue
    if not e.tag.endswith('}p') or cur is None: continue
    p=Paragraph(e,d); t=p.text.replace(' ',' ')
    imgs=[int(re.search(r'image(\d+)',rels[r].target_ref).group(1)) for r in re.findall(r'r:embed="(rId\d+)"',e.xml) if r in rels]
    isli = p.style.name=='List Paragraph' or 'w:numPr' in e.xml
    for line_i,raw in enumerate([x for x in re.split(r'\n',t)]):
        s=raw.strip()
        if not s: continue
        m=re.match(r'^'+HEADS+r'\s*:?\s*(.*)$',s)
        if m and (s.upper().startswith(m.group(1)) ) and (m.group(1)!=m.group(1).title()):
            blk('h',text=m.group(1).replace(' ','').replace('/',' / ') if False else re.sub(r'\s+',' ',m.group(1))+':')
            if m.group(2).strip(): blk('p',text=m.group(2).strip())
            continue
        if s.upper()==s and len(s)<60 and not isli and not s.endswith(':') and not re.match(r'^\d',s): blk('sh',text=s); continue
        if re.match(r'^[A-Z]\.\s',s) and len(s)<40: blk('sh',text=s); continue
        if s.endswith(':') and len(s)<70 and not isli: blk('cap',text=s); continue
        if isli: blk('li',text=re.sub(r'^\d+\.\s*','',s))
        else: blk('p',text=s)
    for n in imgs: blk('img',n=n)
json.dump(exps,open('struct.json','w'),indent=0,ensure_ascii=False)
for x in exps:
    print(x['no'],x['date'],x['title'],len(x['b']),[b['t'] for b in x['b']][:40] if x['no'] in(1,9) else '')
