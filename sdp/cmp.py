import sys,glob
from PIL import Image
ns=[int(a) for a in sys.argv[2:]]; out=sys.argv[1]; S='/tmp/claude-0/-home-user-ashwinsathishkumar846-wq/cd0e2464-2e83-5cb0-be37-3d5a128c853d/scratchpad/sdp'
rows=[]
for n in ns:
    o=Image.open(glob.glob(f'{S}/x/word/media/image{n}.*')[0]).convert('RGB'); m=Image.open(f'rebuilt/image{n}.png').convert('RGB'); W=1000
    a=o.resize((W,int(o.height*W/o.width))); b=m.resize((W,int(m.height*W/m.width))); h=max(a.height,b.height)
    row=Image.new('RGB',(2010,h),'white'); row.paste(a,(0,0)); row.paste(b,(1010,0)); rows.append(row)
c=Image.new('RGB',(2010,sum(r.height for r in rows)+10*len(rows)),'white'); y=0
for r in rows: c.paste(r,(0,y)); y+=r.height+10
c.save(out)
