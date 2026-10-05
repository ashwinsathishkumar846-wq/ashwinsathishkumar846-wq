import subprocess,os,fitz
env=dict(os.environ,NOPB_OUT='1')
subprocess.run(['python3','build_mcp.py','mcp_nopb.docx'],check=True,env=env,capture_output=True)
subprocess.run(['soffice','--headless','--convert-to','pdf','mcp_nopb.docx'],capture_output=True)
d=fitz.open('mcp_nopb.pdf')
for pg in d:
    r=pg.rect; 
    pg.draw_rect(fitz.Rect(28,28,r.width-28,r.height-28),color=(0,0,0),width=1.5,fill=None)
d.save('mcp_final.pdf',garbage=3,deflate=True); print(len(d),'pages')
