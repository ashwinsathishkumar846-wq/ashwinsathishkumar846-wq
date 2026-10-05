import docx,copy,io,re,zipfile
from lxml import etree
from docx.oxml.ns import qn,nsmap
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
WP='http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
def w(t): return '{%s}%s'%(W,t)
class Src:
    def __init__(s,path):
        s.doc=docx.Document(path); s.body=s.doc.element.body
        pkg=s.doc.part.package
        s.styles=s.doc.styles.element
        s.smap={st.get(w('styleId')):st for st in s.styles.findall(w('style'))}
        s.dd=s.styles.find(w('docDefaults'))
        s.rels=s.doc.part.rels
        num=s.doc.part.numbering_part.element if s.doc.part._rels and any('numbering' in r.reltype for r in s.rels.values()) else None
        s.num=num; s.counters={}
        s.default_pstyle=next((i for i,st in s.smap.items() if st.get(w('type'))=='paragraph' and st.get(w('default'))=='1'),None)
    def chain(s,sid):
        out=[]; seen=set()
        while sid and sid in s.smap and sid not in seen:
            seen.add(sid); st=s.smap[sid]; out.append(st); b=st.find(w('basedOn')); sid=b.get(w('val')) if b is not None else None
        return out[::-1]
    # ---- effective run props (dict tag -> element) ----
    def eff_r(s,pstyle,rstyle,rpr):
        d={}
        def merge(rp):
            if rp is None: return
            for c in rp:
                d[c.tag]=c
        merge(s.dd.find(w('rPrDefault')).find(w('rPr')) if s.dd is not None and s.dd.find(w('rPrDefault')) is not None else None)
        for st in s.chain(s.default_pstyle): merge(st.find(w('rPr')))
        for st in s.chain(pstyle): merge(st.find(w('rPr')))
        for st in s.chain(rstyle): merge(st.find(w('rPr')))
        merge(rpr)
        return d
    def eff_p(s,pstyle,ppr):
        d={}
        def merge(pp):
            if pp is None: return
            for c in pp:
                if c.tag in (w('spacing'),w('ind')) and c.tag in d:
                    n=copy.deepcopy(d[c.tag])
                    for k,v in c.attrib.items(): n.set(k,v)
                    d[c.tag]=n
                else: d[c.tag]=c
        merge(s.dd.find(w('pPrDefault')).find(w('pPr')) if s.dd is not None and s.dd.find(w('pPrDefault')) is not None else None)
        for st in s.chain(s.default_pstyle): merge(st.find(w('pPr')))
        for st in s.chain(pstyle): merge(st.find(w('pPr')))
        merge(ppr)
        return d
    # ---- numbering ----
    def num_marker(s,numid,ilvl):
        if s.num is None: return None,None
        numel=next((n for n in s.num.findall(w('num')) if n.get(w('numId'))==str(numid)),None)
        if numel is None: return None,None
        aid=numel.find(w('abstractNumId')).get(w('val'))
        ab=next(a for a in s.num.findall(w('abstractNum')) if a.get(w('abstractNumId'))==aid)
        lv=next((l for l in ab.findall(w('lvl')) if l.get(w('ilvl'))==str(ilvl)),None)
        if lv is None: return None,None
        # override start
        fmt=lv.find(w('numFmt')).get(w('val')); txt=lv.find(w('lvlText')).get(w('val'))
        start=int(lv.find(w('start')).get(w('val'))) if lv.find(w('start')) is not None else 1
        key=(numid,); c=s.counters.setdefault(key,{})
        c[ilvl]=c.get(ilvl,start-1)+1
        for k in list(c):
            if k>ilvl: del c[k]
        def fmtnum(n,f):
            if f=='decimal': return str(n)
            if f=='lowerLetter': return chr(96+(n-1)%26+1)
            if f=='upperLetter': return chr(64+(n-1)%26+1)
            if f=='lowerRoman': return ['i','ii','iii','iv','v','vi','vii','viii','ix','x'][min(n-1,9)]
            if f=='upperRoman': return ['I','II','III','IV','V','VI','VII','VIII','IX','X'][min(n-1,9)]
            return str(n)
        if fmt=='bullet':
            m='•' if ilvl==0 else '–'
        else:
            m=txt
            for l in range(0,ilvl+1):
                lf=next((x for x in ab.findall(w('lvl')) if x.get(w('ilvl'))==str(l)),None)
                f=lf.find(w('numFmt')).get(w('val')) if lf is not None else 'decimal'
                m=m.replace('%%%d'%(l+1),fmtnum(c.get(l,1),f))
        ind=lv.find(w('pPr')).find(w('ind')) if lv.find(w('pPr')) is not None else None
        return m,ind
def ptext(p): return ''.join(t.text or '' for t in p.iter(w('t')))
