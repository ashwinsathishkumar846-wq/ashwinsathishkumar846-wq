import sys,glob
from PIL import Image
ns=[int(a) for a in sys.argv[2:]]
rows=[]
for n in ns:
    o=Image.open(glob.glob(f'../x_ref/word/media/image{n}.*')[0]).convert('RGB'); m=Image.open(f'out/image{n}.png').convert('RGB'); W=900
    a=o.resize((W,int(o.height*W/o.width))); b=m.resize((W,int(m.height*W/m.width))); h=max(a.height,b.height)
    row=Image.new('RGB',(1810,h),'white'); row.paste(a,(0,0)); row.paste(b,(910,0)); rows.append(row)
c=Image.new('RGB',(1810,sum(r.height+8 for r in rows)),'#888'); y=0
for r in rows: c.paste(r,(0,y)); y+=r.height+8
c.save(sys.argv[1])
