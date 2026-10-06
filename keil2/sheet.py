import sys,subprocess,glob,os
from PIL import Image
pdf,out,cols,dpi=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
f0,l0=(sys.argv[5],sys.argv[6]) if len(sys.argv)>6 else (None,None)
os.makedirs('/tmp/sh',exist_ok=True)
for p in glob.glob('/tmp/sh/*'):os.remove(p)
cmd=['pdftoppm','-r',str(dpi),'-png']+(['-f',f0,'-l',l0] if f0 else [])+[pdf,'/tmp/sh/p']
subprocess.run(cmd)
fs=sorted(glob.glob('/tmp/sh/p-*.png'));ims=[Image.open(p) for p in fs];w,h=ims[0].size
rows=(len(ims)+cols-1)//cols
c=Image.new('RGB',(cols*(w+4),rows*(h+4)),'#777')
for i,im in enumerate(ims):c.paste(im,((i%cols)*(w+4),(i//cols)*(h+4)))
c.save(out);print(len(ims),c.size)
