# ---------- footer page numbers, margins, page border ----------
sec = d.sections[0]
sec.bottom_margin = Emu(int(0.6 * 914400)); sec.footer_distance = Emu(int(0.25 * 914400))
fp = sec.footer.paragraphs[0]; fp.alignment = AL.CENTER
def fld(p, instr):
    r = p.add_run(); r.font.size = Pt(10); r.font.name = FONT
    a = OxmlElement('w:fldChar'); a.set(qn('w:fldCharType'), 'begin'); r._r.append(a)
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = instr; r._r.append(it)
    c = OxmlElement('w:fldChar'); c.set(qn('w:fldCharType'), 'separate'); r._r.append(c)
    t = OxmlElement('w:t'); t.text = '1'; r._r.append(t)
    e = OxmlElement('w:fldChar'); e.set(qn('w:fldCharType'), 'end'); r._r.append(e)
fld(fp, 'PAGE')

sp = sect
pb = OxmlElement('w:pgBorders'); pb.set(qn('w:offsetFrom'), 'page')
for side in ('top', 'left', 'bottom', 'right'):
    e = OxmlElement('w:' + side)
    for k_, v in (('val', 'single'), ('sz', '12'), ('space', '20'), ('color', '000000')): e.set(qn('w:' + k_), v)
    pb.append(e)
sp.find(qn('w:pgMar')).addnext(pb)
# section break after page 2: header only on cover + index pages
sig2._p.get_or_add_pPr().append(copy.deepcopy(sp))
last = d.sections[-1]
for hr in last._sectPr.findall(qn('w:headerReference')): last._sectPr.remove(hr)
last.header.is_linked_to_previous = False
for p_ in last.header.paragraphs:
    for r_ in list(p_.runs): r_._r.getparent().remove(r_._r)
last.top_margin = Inches(0.8)
d.core_properties.title = 'Capstone Project Report - Student Course Registration System'
d.save('Capstone_Student_Course_Registration_System.docx')
