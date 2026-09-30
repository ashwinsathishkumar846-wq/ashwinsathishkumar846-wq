set -e
cd /home/user/ashwinsathishkumar846-wq/alm
rm -f pages.json
python3 build.py; soffice --headless --convert-to pdf ALM_Student_Registration_Form.docx >/dev/null 2>&1
python3 - <<'P'
import subprocess,json,re
n=int(re.search(r'Pages:\s+(\d+)',subprocess.run(['pdfinfo','ALM_Student_Registration_Form.pdf'],capture_output=True,text=True).stdout).group(1))
keys=['1. SCENARIO','2. ICT TOOL','3. ACTIVITY PROC','4. STUDENT ACTIVITY','5. EXPECTED OUTPUT']
pg=[]
for k in keys:
    for i in range(1,n+1):
        t=subprocess.run(['pdftotext','-f',str(i),'-l',str(i),'ALM_Student_Registration_Form.pdf','-'],capture_output=True,text=True).stdout
        if re.search('^'+re.escape(k),t,re.M): pg.append(i);break
print(pg,n);json.dump(pg,open('pages.json','w'))
P
python3 build.py; soffice --headless --convert-to pdf ALM_Student_Registration_Form.docx >/dev/null 2>&1
rm -rf pv; mkdir pv; pdftoppm -png -r 40 ALM_Student_Registration_Form.pdf pv/p
python3 - <<'P'
from PIL import Image;import glob
fs=sorted(glob.glob('pv/p-*.png'));ims=[Image.open(f) for f in fs];w,h=ims[0].size;cols=6;rows=(len(ims)+cols-1)//cols
c=Image.new('RGB',(w*cols,h*rows),'gray')
for i,im in enumerate(ims):c.paste(im,((i%cols)*w,(i//cols)*h))
c.save('/tmp/claude-0/-home-user-ashwinsathishkumar846-wq/cd0e2464-2e83-5cb0-be37-3d5a128c853d/scratchpad/sheet.png')
P
