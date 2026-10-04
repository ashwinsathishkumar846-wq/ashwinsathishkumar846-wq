from PIL import Image, ImageDraw, ImageFont
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FM='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
def font(s, b=False): return ImageFont.truetype(FB if b else F, s)
GREEN=(11,93,59); LG=(220,240,228); BLUE=(14,90,150); LB=(219,234,254); AMB=(180,120,0); LA=(255,247,214); RED=(200,30,30); LR=(254,226,226); GREY=(70,70,70)
def tc(d, cx, cy, s, f, fill='black'):
    lines=s.split('\n'); lh=f.size+5; y=cy-lh*len(lines)/2
    for ln in lines:
        w=d.textlength(ln,font=f); d.text((cx-w/2,y),ln,font=f,fill=fill); y+=lh
def box(d, x1,y1,x2,y2, s, fill, line, f, r=10, lw=3, tcol='black'):
    d.rounded_rectangle([x1,y1,x2,y2],radius=r,fill=fill,outline=line,width=lw); tc(d,(x1+x2)/2,(y1+y2)/2,s,f,tcol)
def arrow(d,x1,y1,x2,y2,col=GREY,w=3,label=None,f=None):
    d.line([(x1,y1),(x2,y2)],fill=col,width=w)
    import math
    a=math.atan2(y2-y1,x2-x1); L=16
    d.polygon([(x2,y2),(x2-L*math.cos(a-0.4),y2-L*math.sin(a-0.4)),(x2-L*math.cos(a+0.4),y2-L*math.sin(a+0.4))],fill=col)
    if label: d.text(((x1+x2)/2+6,(y1+y2)/2-22),label,font=f or font(16),fill=col)

# ---------- 1. BLOCK DIAGRAM ----------
im=Image.new('RGB',(1100,720),'white'); d=ImageDraw.Draw(im); f=font(20); fb=font(22,True); fs=font(16)
box(d,30,285,230,415,'LM35\nTemperature\nSensor\n(10 mV / \u00b0C)',LA,AMB,f)
d.rectangle([330,60,800,640],fill=(245,248,255),outline=BLUE,width=4); tc(d,565,88,'LPC2148  (ARM7TDMI-S)',fb,BLUE)
box(d,370,150,760,270,'10-bit ADC0\nchannel AD0.1 (P0.28)\nVREF = 3.3 V',LB,BLUE,f)
box(d,370,320,760,420,'ARM7 CPU\nconvert ADC value to \u00b0C\ncompare with limit',LG,GREEN,f)
box(d,590,470,760,590,'GPIO\nP0.4 - P0.11\nP1.16 - P1.19',LB,BLUE,f)
box(d,370,470,560,590,'UART0\nP0.0 (TXD0)\nP0.1 (RXD0)',LB,BLUE,f)
arrow(d,230,350,300,350,col=AMB); d.line([(300,350),(300,215)],fill=AMB,width=3); arrow(d,300,215,370,215,col=AMB)
d.text((236,318),'analog Vout',font=fs,fill=AMB)
arrow(d,565,270,565,320); arrow(d,465,420,465,470); arrow(d,675,420,675,470)
box(d,880,100,1080,200,'16 x 2 LCD\n(display)',LG,GREEN,f); box(d,880,240,1080,340,'DC Fan\n(via relay)',LG,GREEN,f)
box(d,880,380,1080,480,'Buzzer +\nAlarm LED',LR,RED,f)
d.line([(760,530),(840,530)],fill=GREEN,width=3); d.line([(840,530),(840,150)],fill=GREEN,width=3)
arrow(d,840,150,880,150,col=GREEN); arrow(d,840,290,880,290,col=GREEN); arrow(d,840,430,880,430,col=RED)
box(d,880,545,1080,645,'PC Serial\nTerminal',LB,BLUE,f)
d.line([(465,590),(465,675)],fill=BLUE,width=3); d.line([(465,675),(980,675)],fill=BLUE,width=3); arrow(d,980,675,980,645,col=BLUE)
d.text((600,680),'UART0  9600 bps',font=fs,fill=BLUE)
box(d,30,500,230,600,'3.3 V / 5 V\nPower supply',(240,240,240),GREY,f); arrow(d,130,500,130,415,col=GREY)
im.save('shots/d1_block.png')

# ---------- 2. CIRCUIT CONNECTIONS ----------
im=Image.new('RGB',(1100,820),'white'); d=ImageDraw.Draw(im); f=font(19); fb=font(22,True); fm=ImageFont.truetype(FM,17)
d.rectangle([400,60,700,760],fill=(235,242,252),outline=BLUE,width=4); tc(d,550,95,'LPC2148',font(26,True),BLUE); tc(d,550,128,'(LQFP64)',font(17),BLUE)
left=[('P0.28 / AD0.1',190),('GND / VSSA',250),('VREF / VDDA',310),('P0.0 / TXD0',390),('P0.1 / RXD0',450)]
right=[('P1.16 (D4)',170),('P1.17 (D5)',215),('P1.18 (D6)',260),('P1.19 (D7)',305),('P0.10 (RS)',365),('P0.11 (EN)',410),('P0.8 (FAN)',490),('P0.7 (BUZ)',545),('P0.9 (LED)',600)]
for n,y in left:
    d.line([(340,y),(400,y)],fill='black',width=3); d.text((410,y-11),n,font=fm,fill=BLUE)
for n,y in right:
    d.line([(700,y),(760,y)],fill='black',width=3); w=d.textlength(n,font=fm); d.text((690-w,y-11),n,font=fm,fill=BLUE)
box(d,40,140,250,280,'LM35\n(TO-92)',LA,AMB,f)
d.line([(250,190),(340,190)],fill=AMB,width=4); d.text((262,160),'Vout',font=f,fill=AMB)
d.line([(250,250),(340,250)],fill=GREY,width=3); d.text((262,222),'GND',font=font(16),fill=GREY)
d.line([(250,215),(300,215)],fill=RED,width=3); d.text((262,193-2),'',font=f)
d.text((258,262-0),'',font=f)
tc(d,145,262,'+Vs to +5 V',font(15),RED)
box(d,40,295,250,345,'3.3 V reference',(255,235,235),RED,font(17)); d.line([(250,320),(340,320)],fill=RED,width=3)
d.line([(340,320),(340,310)],fill=RED,width=3); d.line([(340,310),(400,310)],fill=RED,width=3)
# UART
box(d,40,370,250,480,'USB - UART\nconverter\n(to PC)',LB,BLUE,f)
d.line([(250,390),(340,390)],fill=BLUE,width=3); d.line([(250,450),(340,450)],fill=BLUE,width=3)
# LCD
box(d,830,150,1070,430,'16 x 2 LCD\n\nD4 - D7  <- P1.16-19\nRS <- P0.10\nEN <- P0.11\nRW -> GND\nVO -> 10k POT',LG,GREEN,font(18))
for y in (170,215,260,305,365,410): d.line([(760,y),(830,y)],fill=GREEN,width=3)
# loads
box(d,830,460,1070,520,'Relay + DC Fan',LG,GREEN,f); d.line([(760,490),(830,490)],fill=GREEN,width=3)
box(d,830,525,1070,585,'Buzzer (via BC547)',LR,RED,f); d.line([(760,545),(830,545)],fill=RED,width=3)
box(d,830,590,1070,650,'Alarm LED + 330 Ω',LR,RED,f); d.line([(760,600),(830,600)],fill=RED,width=3)
tc(d,550,790,'Supply: 3.3 V for LPC2148 core and I/O, 5 V for LM35, LCD and relay',font(17),GREY)
im.save('shots/d2_circuit.png')

# ---------- 3. FLOWCHART (firmware) ----------
W,Hh=1000,1560; im=Image.new('RGB',(W,Hh),'white'); d=ImageDraw.Draw(im); f=font(20); fs=font(18); fb=font(22,True)
CX=360; BW,BH,DW,DH,GAP=420,64,420,110,34; y=14; prev=None
def oval(s):
    global y
    d.rounded_rectangle([CX-130,y,CX+130,y+52],radius=26,fill=GREEN); tc(d,CX,y+26,s,fb,'white'); c=y+52; y+=52+GAP; return c
def rbox(s,h=BH,fill=LG,line=GREEN):
    global y
    d.rectangle([CX-BW//2,y,CX+BW//2,y+h],fill=fill,outline=line,width=3); tc(d,CX,y+h/2,s,f); c=y+h; y+=h+GAP; return c
def dia(s,side=None,sl='No'):
    global y
    cy=y+DH/2; pts=[(CX,y),(CX+DW//2,cy),(CX,y+DH),(CX-DW//2,cy)]
    d.polygon(pts,fill=LA,outline=AMB); d.line(pts+[pts[0]],fill=AMB,width=3); tc(d,CX,cy,s,fs)
    if side:
        x2=CX+DW//2; arrow(d,x2,cy,720,cy); d.text((x2+8,cy-26),sl,font=fs,fill=RED)
        d.rectangle([720,cy-34,985,cy+34],fill=LR,outline=RED,width=3); tc(d,852,cy,side,fs)
    c=y+DH; y+=DH+GAP; return c
seq=[('o','START'),('b','Initialise PLL, VPBDIV,\nGPIO, LCD and UART0'),('b','Select AD0.1 on P0.28\n(PINSEL1 = 0x01000000)'),
     ('b','Start conversion\nAD0CR = 0x01200302'),('d','DONE bit (bit 31)\nof AD0DR1 = 1 ?','Read AD0DR1\nagain'),
     ('b','Extract 10-bit result\nadc = (AD0DR1 >> 6) & 0x3FF'),('b','Average 8 samples'),
     ('b','temp = adc x 330 / 1023'),('b','Display on LCD and\nsend to UART0'),
     ('d','temp >= 40 °C ?','Fan, buzzer, LED\nOFF if temp <= 38'),('b','Fan ON, buzzer ON,\nalarm LED ON'),('b','Delay 500 ms'),('o','REPEAT')]
for s in seq:
    top=y
    if prev is not None: arrow(d,CX,prev,CX,top)
    if s[0]=='o': prev=oval(s[1])
    elif s[0]=='b': prev=rbox(s[1])
    else:
        prev=dia(s[1],s[2]); d.text((CX+10,prev+2),'Yes',font=fs,fill=(22,101,52))
im=im.crop((0,0,W,int(y-GAP+10))); im.save('shots/d3_flow.png'); print(im.size)
# loop-back arrow note
