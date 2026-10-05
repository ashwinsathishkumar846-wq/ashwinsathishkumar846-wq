import content,re,os
E=content.E
os.makedirs('pages',exist_ok=True)
for k in ['8a','8b','8c','8d','8e','8f']:
    code=E[k]['code'][0][1]
    open(f'pages/{k}.html','w').write(code)
# angular
code=E['9']['code'][0][1].replace('https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js','../node_modules/angular/angular.min.js')
open('pages/9.html','w').write(code)
REACTCSS10='''*{box-sizing:border-box}body{margin:0;background:#f4f6fb;font-family:Segoe UI,Inter,Arial,sans-serif}
.page{max-width:520px;margin:0 auto;padding:30px 0;text-align:center}h1{color:#1e2a4a;font-size:34px;margin:0 0 22px}
.card{background:#fff;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,.15);padding:18px 22px;margin-bottom:18px;text-align:left}
.card h2{margin:0;color:#2f5fcf;font-size:22px}.role{color:#6b7280;margin:4px 0 8px}ul{color:#444;padding-left:22px;line-height:1.7}
.on{color:#1d7a35;font-weight:600}.off{color:#c2410c;font-weight:600}button{background:#3f6fd1;color:#fff;border:0;border-radius:5px;padding:8px 16px;font-size:14px;cursor:pointer}
.small{text-align:center}'''
REACTCSS11='''*{box-sizing:border-box}body{margin:0;background:#eef1f7;font-family:Segoe UI,Inter,Arial,sans-serif}
.wrap{max-width:430px;margin:26px auto;background:#fff;padding:22px 26px;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,.15)}
h2{text-align:center;color:#1e2a4a;margin:0 0 12px}label{display:block;font-weight:600;font-size:13px;margin:12px 0 4px;color:#333}
input,select{width:100%;padding:9px;border:1px solid #c5cad6;border-radius:5px;font-size:14px}
button{margin-top:16px;width:100%;padding:10px;background:#3f6fd1;color:#fff;border:0;border-radius:5px;font-size:15px;cursor:pointer}
.live{font-size:13px;color:#555;background:#f3f5fa;padding:8px;border-radius:5px;margin-top:14px}
.done{margin-top:14px;padding:12px;background:#e7f6ea;color:#1d6b32;border-radius:6px;font-weight:600}'''
def react(k,fn,css,comp,extra=''):
    src=E[k]['code'][0][1]
    src=re.sub(r'import \{ useState \} from "react";','const {useState}=React;',src)
    src=re.sub(r'import "\./App.css";\n','',src)
    src=src.replace('export default function','function')
    html=f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>react-app</title><style>{css}</style>
<script src="../node_modules/react/umd/react.development.js"></script><script src="../node_modules/react-dom/umd/react-dom.development.js"></script>
<script src="../node_modules/@babel/standalone/babel.min.js"></script></head><body><div id="root"></div>
<script type="text/babel">
{src}
ReactDOM.createRoot(document.getElementById("root")).render(<{comp} />);
</script></body></html>'''
    open(f'pages/{fn}.html','w').write(html)
react('10','10',REACTCSS10,'App')
react('11','11',REACTCSS11,'FeedbackForm')
print(os.listdir('pages'))
