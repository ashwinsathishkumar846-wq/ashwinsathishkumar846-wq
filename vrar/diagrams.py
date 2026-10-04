from PIL import Image, ImageDraw, ImageFont
import math
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(s,b=False): return ImageFont.truetype(FB if b else F,s)
BL=(31,78,140); LB=(222,235,250); AM=(180,120,0); LA=(255,247,214); GR=(30,120,60); LG=(222,242,228); RD=(190,40,40); LR=(254,226,226); GY=(70,70,70)
def tc(d,cx,cy,s,f,fill='black'):
    ls=s.split('\n'); lh=f.size+5; y=cy-lh*len(ls)/2
    for l in ls: w=d.textlength(l,font=f); d.text((cx-w/2,y),l,font=f,fill=fill); y+=lh
def box(d,x1,y1,x2,y2,s,fill,line,f,r=10): d.rounded_rectangle([x1,y1,x2,y2],radius=r,fill=fill,outline=line,width=3); tc(d,(x1+x2)/2,(y1+y2)/2,s,f)
def arrow(d,x1,y1,x2,y2,col=GY,w=3):
    d.line([(x1,y1),(x2,y2)],fill=col,width=w); a=math.atan2(y2-y1,x2-x1); L=15
    d.polygon([(x2,y2),(x2-L*math.cos(a-.4),y2-L*math.sin(a-.4)),(x2-L*math.cos(a+.4),y2-L*math.sin(a+.4))],fill=col)
# 1 architecture
im=Image.new('RGB',(1200,760),'white'); d=ImageDraw.Draw(im); f=font(19); fb=font(21,True)
d.rectangle([20,20,330,740],fill=(245,248,253),outline=BL,width=3); tc(d,175,48,'SHOP FLOOR',fb,BL)
box(d,45,80,305,190,'AR device\n(tablet / HoloLens)\ncamera + display + mic',LB,BL,f)
box(d,45,225,305,335,'Torque tool / sensors\n(IoT, MQTT)',LB,BL,f)
box(d,45,370,305,480,'Barcode / QR scanner\nPart bins (pick-to-light)',LB,BL,f)
box(d,45,515,305,625,'Machine PLC / MES\nwork order, station state',LB,BL,f)
d.rectangle([420,20,1180,740],fill=(245,248,253),outline=BL,width=3); tc(d,800,48,'ADAPTIVE WORK INSTRUCTION SERVER',fb,BL)
box(d,450,80,720,190,'Tracking service\nModel Target (CAD) +\nmarker fallback',LG,GR,f)
box(d,880,80,1150,190,'Vision checker\nCNN: part, bolt,\norientation check',LG,GR,f)
box(d,450,260,720,380,'Adaptation engine\nskill score, time, errors\n→ detail level',LA,AM,f)
box(d,880,260,1150,380,'Step manager\nstate machine,\nrules and interlocks',LA,AM,f)
box(d,450,450,720,560,'Instruction database\nCAD, 3D models,\nanimations, text, audio',LB,BL,f)
box(d,880,450,1150,560,'Operator profile DB\nskill, history,\nlanguage',LB,BL,f)
box(d,450,630,1150,720,'Analytics and supervisor dashboard (web)  –  cycle time, errors, yield, training',LR,RD,f)
for y in (135,280,425,570): arrow(d,305,min(y,570),450,min(y,570)) if False else None
arrow(d,305,135,450,135); arrow(d,305,280,450,320); arrow(d,305,425,450,350); arrow(d,305,570,880,330)
arrow(d,720,135,880,135); arrow(d,585,190,585,260); arrow(d,1015,190,1015,260); arrow(d,720,320,880,320); arrow(d,585,450,585,380); arrow(d,1015,450,1015,380); arrow(d,800,560,800,630)
im.save('shots/d1_arch.png')
# 2 adaptive flowchart
W,H=1000,1500; im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im); f=font(19); fs=font(17); fb=font(21,True)
CX=360;BW,BH,DW,DH,GAP=430,62,430,106,32;y=12;prev=None
def oval(s):
    global y
    d.rounded_rectangle([CX-130,y,CX+130,y+50],radius=25,fill=BL); tc(d,CX,y+25,s,fb,'white'); c=y+50; y+=50+GAP; return c
def rb(s,h=BH):
    global y
    d.rectangle([CX-BW//2,y,CX+BW//2,y+h],fill=LB,outline=BL,width=3); tc(d,CX,y+h/2,s,f); c=y+h; y+=h+GAP; return c
def dia(s,side,sl='No'):
    global y
    cy=y+DH/2; pts=[(CX,y),(CX+DW//2,cy),(CX,y+DH),(CX-DW//2,cy)]
    d.polygon(pts,fill=LA,outline=AM); d.line(pts+[pts[0]],fill=AM,width=3); tc(d,CX,cy,s,fs)
    x2=CX+DW//2; arrow(d,x2,cy,730,cy); d.text((x2+8,cy-26),sl,font=fs,fill=RD)
    d.rectangle([730,cy-36,985,cy+36],fill=LR,outline=RD,width=3); tc(d,857,cy,side,fs); c=y+DH; y+=DH+GAP; return c
seq=[('o','START'),('b','Scan work order QR\nand identify operator'),('b','Load operator skill score\nfrom profile database'),
 ('d','Skill score\n>= 0.75 ?','Score < 0.40:\nNOVICE level\n(full detail)'),('b','Show instruction at the\nselected detail level'),
 ('b','Track part with camera;\nread torque / sensor data'),('d','Step result OK\n(vision + torque) ?','Show error, lock\ntool, notify\nsupervisor'),
 ('b','Record step time and errors;\nupdate skill score'),('d','Time > target by 20%\nor 2 errors ?','Keep current\ndetail level'),
 ('b','Step detail level down\n(more help); next step'),('d','More steps\nleft ?','Next step'),('b','Log unit, release to next\nstation, update dashboard'),('o','END')]
for s in seq:
    top=y
    if prev is not None: arrow(d,CX,prev,CX,top)
    if s[0]=='o': prev=oval(s[1])
    elif s[0]=='b': prev=rb(s[1])
    else: prev=dia(s[1],s[2]); d.text((CX+8,prev+1),'Yes',font=fs,fill=GR)
im=im.crop((0,0,W,int(y-GAP+10))); im.save('shots/d2_flow.png'); print(im.size)
# 3 skill levels table image-like (levels)
im=Image.new('RGB',(1200,420),'white'); d=ImageDraw.Draw(im); f=font(19); fb=font(21,True)
cols=[('NOVICE\nscore < 0.40',LR,RD,'3D animation\nfull text steps\nsafety warnings\nvoice help on\nconfirm each step'),('SKILLED\n0.40 - 0.75',LA,AM,'Highlights + key values\nshort text\nwarnings only for\nrisky steps'),('EXPERT\nscore >= 0.75',LG,GR,'Bolt highlight and\ntorque value only\nauto-advance on\nsensor signal')]
for i,(t,fl,ln,b) in enumerate(cols):
    x=20+i*395; d.rounded_rectangle([x,20,x+370,400],radius=12,fill=fl,outline=ln,width=3); tc(d,x+185,75,t,fb,'black'); d.line([(x+20,125),(x+350,125)],fill=ln,width=2); tc(d,x+185,255,b,f)
for i in range(2): arrow(d,390+i*395-0,210,415+i*395,210,GY)
im.save('shots/d3_levels.png')
