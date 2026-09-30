set -e
cd /home/user/ashwinsathishkumar846-wq/capstone
N=Capstone_Student_Course_Registration_System
rm -f pages.json
python3 build_cap.py; soffice --headless --convert-to pdf $N.docx >/dev/null 2>&1
python3 - <<'P'
import subprocess,json,re
N='Capstone_Student_Course_Registration_System.pdf'
n=int(re.search(r'Pages:\s+(\d+)',subprocess.run(['pdfinfo',N],capture_output=True,text=True).stdout).group(1))
keys=['STUDENT COURSE REGISTRATION SYSTEM','1. INTRODUCTION','2. LOGIC BUILDING','3. IMPLEMENTATION STEPS','4. CODE AND OUTPUT','5. CONCLUSION']
pg=[]
for k in keys:
    for i in range(4,n+1):
        t=subprocess.run(['pdftotext','-f',str(i),'-l',str(i),N,'-'],capture_output=True,text=True).stdout
        if re.search('^'+re.escape(k),t,re.M): pg.append(i);break
print(pg,n);json.dump(pg,open('pages.json','w'))
P
python3 build_cap.py; soffice --headless --convert-to pdf $N.docx >/dev/null 2>&1
rm -rf pv; mkdir pv; pdftoppm -png -r 40 $N.pdf pv/p
python3 - <<'P'
from PIL import Image;import glob
fs=sorted(glob.glob('pv/p-*.png'));ims=[Image.open(f) for f in fs];w,h=ims[0].size;cols=6;rows=(len(ims)+cols-1)//cols
c=Image.new('RGB',(w*cols,h*rows),'gray')
for i,im in enumerate(ims):c.paste(im,((i%cols)*w,(i//cols)*h))
c.save('/tmp/claude-0/-home-user-ashwinsathishkumar846-wq/cd0e2464-2e83-5cb0-be37-3d5a128c853d/scratchpad/sheet.png')
P
