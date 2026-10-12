import fitz,re,json
d=fitz.open('rec_nopb.pdf');st=json.load(open('starts.json'))
order=['1a','1b','1c','1d','2','3','4','5','6','7','8','9','10','CBS-1','CBS-2','CBS-3']
rng={k:(st[k],st[nk] if nk else len(d)) for k,nk in zip(order,order[1:]+[None])}
pats={'2b':('2',r'^B\) Exchange \(Swap\)'),'3b':('3',r'^\(b\) Smallest Number in an Array'),'4b':('4',r'^\(b\) Timer-Based Interrupt to Toggle'),'4c':('4',r'^\(c\) UART Programming Using'),'5b':('5',r'^\(b\) I/O Port Programming with Delay'),'5c':('5',r'^\(c\) 8051 I/O Port Programming to Toggle'),'6b':('6',r'^B\. LED with Switch Control'),'7b':('7',r'^B\. LCD WITH SWITCH CONTROL')}
sub={}
for key,(e,pat) in pats.items():
    a,b=rng[e]
    for pi in range(a,b):
        if re.search(pat,d[pi].get_text(),re.M|re.I): sub[key]=pi-1;break
pg={k:v-1 for k,v in st.items()};pg['_sub']=sub
json.dump(pg,open('pages.json','w'));print(len(d),pg)
