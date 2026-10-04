import json,re,glob,sys
from PIL import Image,ImageDraw,ImageFont
S='/tmp/claude-0/-home-user-ashwinsathishkumar846-wq/cd0e2464-2e83-5cb0-be37-3d5a128c853d/scratchpad/sdp'
ocr=json.load(open(S+'/ocr.json'))
FR='/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'; FB='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
def keep(m,r): 
    s=m.group(0); return r.upper() if s.isupper() else (r.title() if s[0].isupper() and not s.isupper() else r)
RULES=[
 (r'amirthavarshini\.?24010\d\d','ajay.2401007'),
 (r'AMIRTHA\s*VARSHINI\s*S?','AJAY.I'),(r'AMIRIHAWARSHINI\s*S?','AJAY.I'),(r'amirthavarshini\.?2401015','ajay.2401007'),(r'amirthavarshinX?','ajay.2401007'),
 (r'alden\.?2401014','rohit.2401012'),(r'ashwin\.?2401021','vimal.2401022'),(r'DHAKSHITHA\s*S\s*CSE','NAVEEN K CSE'),(r'DHAKSHITHAA?\s*S?','NAVEEN K'),(r'DHANISHKAA\s*D','KARTHIK D'),(r'BHAVNA\s*S','MEGHA R'),
 (r'Dhakshithaa\'?s\s*Team','Naveen\'s Team'),(r'\bAshwin\b','Vimal'),(r'BANK\s*MANAGEMENT','LIBRARY MANAGEMENT'),(r'Bank\s*Manang?ement','Library Management'),(r'Bank\s*Administration','Library Administration'),
 (r"Amirtha's","Ajay's"),(r"AMIRTHA'S","AJAY'S"),(r'Amirtha|Amirths|Amirth\.*','Ajay'),(r'AMIRTHA','AJAY'),(r'amirtha','ajay'),(r'\bBMBA\b','LMBA'),
 (r'BALANCE\s*ENQUIRY','BOOK SEARCH'),(r'DEPOSIT\s*MONEY\s*FEATURE','ISSUE BOOK FEATURE'),(r'WITH\s*DRAW\s*MONEY\s*FEATURE','RETURN BOOK FEATURE'),(r'CREATE\s*CUSTOMER\s*DATABASE','CREATE MEMBER DATABASE'),
 (r'ACCOUNT\s*MANAGEMENT','CATALOG MANAGEMENT'),(r'Customer\s*Management','Member Management'),(r'Balance\s*Enquiry\s*Feature','Book Search Feature'),(r'balance\s*enquiry','book search'),
 (r'ANALYSIS\s*OF\s*PAYMENT\s*PAGE','ANALYSIS OF BOOK FINES'),(r'REGISTRATION\s*PAGE','MEMBER REGISTRATION'),(r'CHECK\s*ACCOUNT\s*BALANCE|Check account balance','Check book availability'),(r'Display transaction history','Display borrowing history'),(r'Send balance alert','Send due-date alert'),
 (r'CREDIT','FINE'),(r'DEBIT','ISSUE'),(r'MINIMUM\s*1\s*RS','MINIMUM 1 BOOK'),(r'DEBIST<=CREDIT','ISSUE<=LIMIT'),
]
def matches(t):
    taken=[]; out=[]
    for p,r in RULES:
        for m in re.finditer(p,t,flags=re.I):
            if any(m.start()<e and m.end()>st for st,e,_ in taken) or m.end()==m.start(): continue
            rep=r.upper() if (r.isalpha() and m.group(0).isupper()) else (r if not r.isalpha() else keep(m,r))
            if r in('AJAY.I',) : rep=r
            taken.append((m.start(),m.end(),rep))
    return sorted(taken)
def sub(t):
    o=t
    for st,e,r in reversed(matches(t)): o=o[:st]+r+o[e:]
    return o
def ident(t): return bool(matches(t))
def avatar_fix(tok):  # single-initial avatar bubbles
    return {'AS':'AI','DC':'NC','DS':'NK','BS':'MR','A':'R'}.get(tok.strip())
def stats(im,bx):
    x0,y0,x1,y1=bx; reg=im.crop(bx); px=list(reg.getdata()); w,h=reg.size
    border=[reg.getpixel((x,0)) for x in range(w)]+[reg.getpixel((x,h-1)) for x in range(w)]
    bg=tuple(sorted(c[i] for c in border)[len(border)//2] for i in range(3))
    far=max(px,key=lambda c:sum(abs(c[i]-bg[i]) for i in range(3)))
    dens=sum(1 for c in px if sum(abs(c[i]-bg[i]) for i in range(3))>150)/len(px)
    return bg,far,dens
import numpy as np, cv2
def avatars(im):
    a=np.array(im); hsv=cv2.cvtColor(a,cv2.COLOR_RGB2HSV)
    # avatar blue (~#3657cb): hue ~ 112-122 (opencv), strong saturation
    m=cv2.inRange(hsv,(105,140,150),(125,255,235)); m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE); d=ImageDraw.Draw(im); n=0
    for c in cs:
        x,y,w,h=cv2.boundingRect(c)
        if not(10<=w<=70 and 0.85<w/h<1.18): continue
        if cv2.contourArea(c)/(np.pi*(w/2)*(h/2))<0.75: continue
        patch=im.crop((x,y,x+w,y+h)); white=sum(1 for p in patch.getdata() if min(p)>200)
        if white<w*h*0.03: continue
        bg=tuple(int(v) for v in np.median(a[y+2:y+4,x+w//2-1:x+w//2+2].reshape(-1,3),axis=0)) if False else (54,87,203)
        # repaint the letters: fill interior with avatar colour then write AI
        d.ellipse([x+w*0.12,y+h*0.12,x+w*0.88,y+h*0.88],fill=bg)
        size=max(6,int(h*0.40)); f=ImageFont.truetype(FB,size); d.text((x+w/2,y+h/2),'AI',font=f,fill=(255,255,255),anchor='mm'); n+=1
    return n
def process(n,path):
    im=Image.open(path).convert('RGB'); d=ImageDraw.Draw(im); ch=0
    for txt,quad,conf in ocr[str(n)]:
        xs=[p[0] for p in quad]; ys=[p[1] for p in quad]
        pad=1; bx=(max(0,min(xs)-pad),max(0,min(ys)-pad),min(im.width,max(xs)+pad),min(im.height,max(ys)+pad)); w=bx[2]-bx[0]; h=bx[3]-bx[1]
        if h<5 or w<5: continue
        segs=None
        a_=avatar_fix(txt) if len(txt.strip())<=2 and re.fullmatch(r'[A-Z]{1,2}',txt.strip()) and w<h*2.2 else None
        if a_:
            bg,far,_=stats(im,bx)
            if max(bg)-min(bg)<40: continue
            segs=[(0,len(txt),a_)]
        else:
            segs=matches(txt)
        if not segs: continue
        L=max(1,len(txt)); bg,far,dens=stats(im,bx); fp=FB if dens>0.30 else FR
        reg=im.crop(bx); rw,rh=reg.size
        def ink(c): return sum(abs(c[i]-bg[i]) for i in range(3))>90
        cols=[any(ink(reg.getpixel((x,y))) for y in range(rh)) for x in range(rw)]
        rows=[y for y in range(rh) if any(ink(reg.getpixel((x,y))) for x in range(rw))]
        if not rows: continue
        it,ib=bx[1]+rows[0],bx[1]+rows[-1]+1; inkh=ib-it
        gaps=[]; x=0
        while x<rw:
            if not cols[x]:
                x2=x
                while x2<rw and not cols[x2]: x2+=1
                if x2-x>=max(3,inkh*0.22) and x>0 and x2<rw: gaps.append(bx[0]+(x+x2)//2)
                x=x2
            else: x+=1
        def snap(v,edge):
            c=[g for g in gaps if abs(g-v)<=max(10,w*0.08)]
            return min(c,key=lambda g:abs(g-v)) if c else v
        full=sub(txt) if not a_ else a_
        if ' ' not in txt and len(txt)>12 and not a_:
            full=re.sub(r'([A-Z]{2,})([A-Z][a-z])',r'\1 \2',full); full=re.sub(r'([a-z])([A-Z])',r'\1 \2',full); full=re.sub(r'([A-Za-z])(\d)',r'\1 \2',full); full=re.sub(r'(\d)([A-Za-z])',r'\1 \2',full)
            full=re.sub(r'([a-z])(\()',r'\1 \2',full); full=re.sub(r'(\))([A-Za-z])',r'\1 \2',full); full=re.sub(r'dates','dates',re.sub(r'Adddates','Add dates',full))
            full=re.sub(r'(?i)(work)(item)',r'\1 \2',full)
        # main text line only (largest contiguous run of ink rows)
        runs=[];cur=[]
        for y in rows:
            if cur and y!=cur[-1]+1: runs.append(cur);cur=[]
            cur.append(y)
        runs.append(cur); main=max(runs,key=len); it,ib=bx[1]+main[0],bx[1]+main[-1]+1; inkh=ib-it
        size=20
        for _ in range(3):
            f=ImageFont.truetype(fp,size); bb=f.getbbox(txt,anchor='ls'); hh=bb[3]-bb[1]; size=max(6,round(size*inkh/max(1,hh)))
        f=ImageFont.truetype(fp,size); base=it-f.getbbox(txt,anchor='ls')[1]
        tw=d.textlength(full,font=f)
        while tw>w*1.2 and size>6: size-=1; f=ImageFont.truetype(fp,size); tw=d.textlength(full,font=f)
        x=bx[0] if not a_ else bx[0]+(w-tw)/2
        d.rectangle([bx[0],bx[1],max(bx[2],bx[0]+tw+2),bx[3]],fill=bg)
        d.text((x,base),full,font=f,fill=far,anchor='ls'); ch+=1
    ch+=avatars(im)
    return im,ch
if __name__=='__main__':
    import os; os.makedirs('new',exist_ok=True)
    for n in range(1,87):
        p=glob.glob(f'{S}/x/word/media/image{n}.*')[0]
        im,ch=process(n,p); ext=p.rsplit('.',1)[1]
        im.save(f'new/image{n}.{ext}',quality=95) if ext=='jpeg' else im.save(f'new/image{n}.{ext}')
        if ch: print(n,ch,end=' | ')
