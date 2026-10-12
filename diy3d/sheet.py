import sys
from PIL import Image
names=sys.argv[2:];out=sys.argv[1]
ims=[Image.open('rend/'+n+'.png').convert('RGBA') for n in names]
rows=[];cur=[];wsum=0
for i in ims:
    if wsum+i.width>3000 and cur: rows.append(cur);cur=[];wsum=0
    cur.append(i);wsum+=i.width+20
rows.append(cur)
W=max(sum(i.width+20 for i in r) for r in rows);H=sum(max(i.height for i in r)+20 for r in rows)
c=Image.new('RGB',(W,H),(235,235,235));y=0
for r in rows:
    x=0
    for i in r:c.paste(i,(x,y),i);x+=i.width+20
    y+=max(i.height for i in r)+20
s=min(1,2400/W);c=c.resize((int(W*s),int(H*s)));c.save(out);print(c.size)
