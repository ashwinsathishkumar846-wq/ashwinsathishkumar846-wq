import os,sys,re,copy,json
os.environ.update(NAME='AJAY.I',ROLL='71812401007',HDR_L='20CS252 – MICROCONTROLLER AND PROGRAMMING LABORATORY',HDR_R='COURSE INSTRUCTOR: Mrs. M. Amuthasurabi, AP/CSE',LABEL='EXP NO.',LASTRES='1',HDR_SZ='9',IMG_MAXH='3.3',HDR_D='170',FTR_D='60',BOT_M='820',FTR_SP='25')
OUT=sys.argv[1] if len(sys.argv)>1 else 'mcp.docx'
sys.argv=[sys.argv[0],OUT]
import wtbuild as B
from wtbuild import *
B.SUBS.insert(0,('"Amirtha Varshini S"','"AJAY.I"'))
REPL=B.REPL; REPL['ref:image84.jpeg']=os.path.abspath('image84_aj.png')
def settext(p,new):
    ts=list(p.iter(w('t')))
    if not ts: return
    j=''.join(t.text or '' for t in ts)
    pre=''
    m=re.match(r'^\s*(AIM:|RESULT:?)\s*',j)
    if m and len(ts)>1 and ts[0].text.strip() in ('AIM:','RESULT:','AIM','RESULT'): 
        ts[1].text=new
        for t in ts[2:]: t.text=''
    elif m: 
        ts[0].text=m.group(0)+new
        for t in ts[1:]: t.text=''
    else:
        ts[0].text=new
        for t in ts[1:]: t.text=''
    for t in ts: t.set(qn('xml:space'),'preserve')
G={
'Start the program.':'Begin the program.','Include the REG51.H header file.':'Include the header file REG51.H.',
'Declare variables x and y.':'Declare the variables x and y.','Store the hexadecimal number 29H in mb.':'Load the hexadecimal number 29H into the variable mb.',
'Extract the lower nibble using mb & 0x0F.':'Separate the lower nibble using mb & 0x0F.','Add 30H to convert the lower nibble into its ASCII value.':'Add 30H to change the lower nibble into its ASCII value.',
'Display the result through Port 1.':'Send the result to Port 1.','Extract the upper nibble using mb & 0xF0.':'Separate the upper nibble using mb & 0xF0.',
'Shift the upper nibble right by 4 positions.':'Shift the upper nibble four bits to the right.','Add 30H to obtain its ASCII value.':'Add 30H to get its ASCII value.',
'Repeat continuously.':'Repeat the steps continuously.','Define P1.7 as mybit.':'Define P1.7 as the bit mybit.','Create a delay function.':'Write a delay function.',
'Set mybit to 0.':'Clear mybit to 0.','Generate a delay.':'Call the delay function.','Set mybit to 1.':'Make mybit equal to 1.','Generate another delay.':'Call the delay function once more.',
'Repeat the process continuously.':'Repeat this process in an endless loop.','Observe the toggling of Port 1 bit 7.':'Watch Port 1 bit 7 toggle in the simulator.',
'Initialize Port 0, Port 1, Port 2 and Port 3 with 55H.':'Initialize Port 0, Port 1, Port 2 and Port 3 with 33H.',
'Complement the value of Port 0.':'Invert the contents of Port 0.','Complement the value of Port 1.':'Invert the contents of Port 1.','Complement the value of Port 2.':'Invert the contents of Port 2.','Complement the value of Port 3.':'Invert the contents of Port 3.',
'Generate a small delay.':'Add a short delay.','Observe the ports changing between 55H and AAH.':'Observe that the ports alternate between 33H and CCH.',
'Create a new project.':'Open a new project.','Select the microcontroller Atmel → AT89C52.':'Choose the device Atmel → AT89C52.','Enter the source code.':'Type the source code.','Save the program.':'Save the program file.',
'Add the HEX file to the output.':'Enable HEX file creation in the output options.','Compile the program using Project → Build Target / F7.':'Build the program using Project → Build Target or the F7 key.',
'The HEX file will be generated in the project folder.':'The HEX file is created in the project folder.',
'Include the required header file and define the ports for LEDs, switches and beep.':'Include the required header file and define the ports used for the LEDs, switches and beep.',
'Run an infinite while loop for continuous switch monitoring.':'Run an infinite while loop to keep monitoring the switches.','Check whether a particular switch is pressed.':'Check whether a switch is pressed.',
'When a switch is pressed, produce a beep for a short delay and switch ON the corresponding LED.':'When a switch is pressed, sound the beep for a short time and turn ON the matching LED.',
'Include the required header file and define the LCD data port, EN, RS and RW pins.':'Include the required header file and define the LCD data port and the EN, RS and RW pins.',
'Initialize the LCD using the required commands.':'Initialize the LCD with the required commands.','Send the required text to the LCD.':'Send the text to be shown to the LCD.','Run the program continuously.':'Keep the program running continuously.','Stop the program.':'Stop the program.',
'Include the required header file and define LCD, switch, EN, RS, RW and buzzer pins.':'Include the required header file and define the LCD, switch, EN, RS, RW and buzzer pins.',
'Initialize the LCD.':'Initialize the LCD.','Continuously check the switches.':'Keep checking the switches continuously.',
'Select ARM → ARM7.':'Choose ARM → ARM7 as the target.','Add the source code to the target.':'Add the source file to the target.','Compile and build the target.':'Compile the target and build it.','Generate the HEX file.':'Create the HEX file.',
'Add the HEX file to the LPC2000 Flash Utility.':'Load the HEX file into the LPC2000 Flash Utility.','Transfer the HEX file to the ARM processor.':'Download the HEX file to the ARM processor.','End the program.':'Stop the program.',
'Stop the program. MCP record from Exp 7':'Stop the program.','End the program. MCP record from Exp 7':'Stop the program.',
'PHILIPS LPC2000 FLASH UNILITY':'PHILIPS LPC2000 FLASH UTILITY','PHILIPS LPC2000 FLASH UNILITY :':'PHILIPS LPC2000 FLASH UTILITY:','PHILIPS LPC2000 FLASH UNILITY:':'PHILIPS LPC2000 FLASH UTILITY:',
# aims / results
'To write and execute 8051 C programs for ASCII number display through a port, I/O port programming with delay, and toggling between two or more I/O ports.':'To write and execute 8051 C programs that display an ASCII number through a port, perform I/O port programming with a delay, and toggle between two or more I/O ports.',
'To demonstrate the interfacing of LEDs with the 8051 microcontroller and to control/blink the LEDs with a time delay.':'To interface LEDs with the 8051 microcontroller and blink them with a time delay.',
'To control the LEDs using switches connected to the 8051 microcontroller and produce a beep when a switch is pressed.':'To operate the LEDs through switches connected to the 8051 microcontroller and produce a beep whenever a switch is pressed.',
'To interface an LCD with the 8051 microcontroller and display the given text, as well as display different messages on the LCD based on the switch pressed.':'To interface an LCD with the 8051 microcontroller, display the given text, and show different messages on the LCD according to the switch pressed.',
'To interface an LCD with the 8051 microcontroller and display different messages depending on which switch is pressed.':'To interface an LCD with the 8051 microcontroller and show a different message for each switch that is pressed.',
'To demonstrate the interfacing of LED and LCD with the ARM7 LPC2148 processor and to control the LED and display the given text on the LCD.':'To demonstrate the interfacing of an LED and an LCD with the ARM7 LPC2148 processor, to control the LED and to display the given text on the LCD.',
'To interface an LCD with the ARM7 LPC2148 processor and display the given text.':'To interface an LCD with the ARM7 LPC2148 processor and display the given text on it.',
'To demonstrate the process of interfacing a buzzer with the ARM7 processor.':'To demonstrate how a buzzer is interfaced with the ARM7 processor.',
'To demonstrate the process of LED blinking using a Timer with the ARM7 processor.':'To demonstrate LED blinking with the help of a Timer of the ARM7 processor.',
'Thus, the 8051 C programs for ASCII number display, I/O port programming with delay, and toggling between multiple I/O ports were executed successfully, and the expected port outputs were obtained.':'Thus, the 8051 C programs for displaying an ASCII number, I/O port programming with delay and toggling of multiple I/O ports were executed successfully and the expected port outputs were obtained.',
'Thus, the 8051 C programming for LED interfacing was executed and verified successfully.':'Thus, the 8051 C program for LED interfacing was executed and verified successfully.',
'Thus, the 8051 C programming for LCD interfacing and LCD with switch control was executed and verified successfully.':'Thus, the 8051 C programs for LCD interfacing and for LCD with switch control were executed and verified successfully.',
'Thus, the ARM7 LED and LCD interfacing programs were executed and verified successfully.':'Thus, the ARM7 programs for LED and LCD interfacing were executed and verified successfully.',
}
G2={k.strip():v for k,v in G.items()}
UNIT=[None,None]
OPC='MOV|ADDC|ADD|SUBB|MUL|DIV|ANL|ORL|XRL|CPL|RLC|RRC|RL|RR|CLR|SETB|ORG|END|INC|DEC|DJNZ|CJNE|JC|JNC|JZ|JNZ|SJMP|SWAP|XCH|L\\d+:'
def asmsplit(p):
    ts=list(p.iter(w('t'))); j=''.join(t.text or '' for t in ts)
    m=re.match(r'^\s*((?:Program:?|PROGRAM:?|INSTRUCTION:?)\s*)?(.+)$',j,re.S)
    if not m or len(j)>420: return
    body=m.group(2).replace('\n',' ')
    if len(re.findall(r'\b(?:'+OPC+r')\b',body))<2 or re.search(r'[a-z]{3,}',body): return
    body=re.sub(r'(?<=H)(?=(?:'+OPC+r')\b)','\n',body)
    body=re.sub(r'\s+(?=(?:'+OPC+r')\b)','\n',body)
    body=re.sub(r'(L\d+:)\n',r'\1 ',body)
    lines=[x.strip() for x in body.split('\n') if x.strip()]
    if m.group(1):
        if len(ts)<2: return
        ts[0].text=m.group(1).strip()+' '
        for t in ts[2:]: t.text=''
        run=ts[1].getparent(); ts[1].text=lines[0]
    else:
        for t in ts[1:]: t.text=''
        run=ts[0].getparent(); ts[0].text=lines[0]
    for ln in lines[1:]:
        run.append(OxmlElement('w:br')); t=OxmlElement('w:t'); t.text=ln; t.set(qn('xml:space'),'preserve'); run.append(t)
def dosubs2(p):
    B.dosubs0(p)
    if UNIT[0]=='my': asmsplit(p)
    ts=list(p.iter(w('t'))); j=''.join(t.text or '' for t in ts).strip()
    if UNIT[0]=='ref':
        key=re.sub(r'^(AIM:|RESULT:?)\s*','',j).strip()
        if key in G2: settext(p,G2[key])
        elif j in G2: settext(p,G2[j])
        elif key=='Thus, the ARM7 buzzer interfacing program was executed and verified successfully.' and UNIT[1]=='11': settext(p,'Thus, the ARM7 program for buzzer interfacing was executed and verified successfully.')
        elif key=='Thus, the ARM7 buzzer interfacing program was executed and verified successfully.' and UNIT[1]=='12': settext(p,'Thus, the ARM7 program for LED blinking using the Timer was executed and verified successfully.')
B.dosubs=dosubs2

my=B.Src('my.docx'); my.tag='my'; ref=B.Src('ref.docx'); ref.tag='ref'
# exp 12 code replace in ref body
rb=list(ref.body)
newcode=['#include <lpc21xx.h>','void timer0_delay_ms(unsigned int ms)','{','  T0TCR = 0x02;','  T0PR  = 14999;','  T0TCR = 0x01;','  while (T0TC < ms);','  T0TCR = 0x00;','}','int main(void)','{','  IO0DIR = 0x00000080;','  while (1)','  {','    IO0SET = 0x00000080;','    timer0_delay_ms(500);','    IO0CLR = 0x00000080;','    timer0_delay_ms(500);','  }','}']
assert ptext(rb[2185]).strip().startswith('#include')
for n,j in enumerate(range(2185,2207)):
    if n<len(newcode): settext(rb[j],newcode[n])
    else: rb[j].getparent().remove(rb[j])
RU=B.units_of(ref)
import expgen
expgen.TXF=lambda x:G2.get(x.strip(),x)
MY=[('1b','VIRTUAL LABS PROGRAMMING FOR I/O INTERFACING (LED AND SWITCH INTERFACING)',2,118),('1a','VIRTUAL LABS PROGRAMMING FOR DELAY GENERATION AND EFFECT OF CPU CLOCK',120,238),('1c','VIRTUAL LABS PROGRAMMING WITH ON-CHIP TIMERS/COUNTERS',240,354),('2','STUDY OF KEIL SOFTWARE',356,501),('3','ARITHMETIC AND LOGICAL OPERATIONS USING 8051 ASSEMBLY LANGUAGE IN KEIL µVISION',503,1077),('4','8051 ALP FOR DATA TRANSFER BETWEEN MEMORY BLOCKS',1079,1216),('5','LARGEST AND SMALLEST NUMBER IN AN ARRAY USING 8051 ALP',1218,1309),('6','8051 C PROGRAMMING FOR TIMER',1311,len(list(my.body)))]
DATES={'1a':'03.07.26','1b':'03.07.26','1c':'10.07.26','2':'17.07.26','3':'24.07.26','4':'07.08.26','5':'18.09.26','6':'18.09.26','7':'25.09.26','8':'09.10.26','9':'09.10.26','10':'16.10.26','11':'16.10.26','12':'23.10.26'}
order=['1a','1b','1c','2','3','4','5','6']
byno={n:(t,s,e) for n,t,s,e in MY}
UNIT[0]='my'
pass
UNIT[0]='ref'
for (no,date,title),a,b in RU:
    n=re.search(r'EXP NO\.\s*(\w+)',no).group(1) if 'EXP' in no else no
    n=n.strip(); UNIT[1]=n
    if n=='7':
        parts=expgen.exp7(ref)
        expgen.emit_gen(B,ref,n,DATES[n],title,parts,None)
        B.para(after=0,size=4,ls=1.0)
        B.para('RESULT:',bold=True,before=float(B.SPC.get(n,0)),after=3,align=B.AL.LEFT,keep=True)
        B.para(parts[-1]['result'],left=0.3,after=0)
    else: B.emit(ref,n,DATES[n],title,a,b,n)
# save (same order fix as wtbuild main)
ORD=['pStyle','keepNext','keepLines','pageBreakBefore','framePr','widowControl','numPr','suppressLineNumbers','pBdr','shd','tabs','suppressAutoHyphens','kinsoku','wordWrap','overflowPunct','topLinePunct','autoSpaceDE','autoSpaceDN','bidi','adjustRightInd','snapToGrid','spacing','ind','contextualSpacing','mirrorIndents','suppressOverlap','jc','textDirection','textAlignment','textboxTightWrap','outlineLvl','divId','cnfStyle','rPr','sectPr','pPrChange']
def fixp(root):
    for pp in root.iter(w('pPr')):
        kids=list(pp);seen={}
        for k in kids: seen.setdefault(k.tag,k)
        kids2=sorted(seen.values(),key=lambda e:ORD.index(e.tag.split('}')[1]) if e.tag.split('}')[1] in ORD else 99)
        for k in kids: pp.remove(k)
        for k in kids2: pp.append(k)
fixp(B.dest.element); fixp(B.sec.header._element); fixp(B.sec.footer._element)
B.dest.core_properties.title='20CS252 Microcontroller and Programming Laboratory - AJAY.I - 71812401007'
if os.environ.get('NOPB_OUT'):
    for sp_ in B.dest.element.iter(w('sectPr')):
        for pb_ in sp_.findall(w('pgBorders')): sp_.remove(pb_)
B.dest.save(OUT); print('saved',OUT)
