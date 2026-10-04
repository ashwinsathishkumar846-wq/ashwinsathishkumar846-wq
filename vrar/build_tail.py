
sec = d.sections[0]
for s_ in d.sections:
    s_.footer.is_linked_to_previous = False
def fld(p, instr):
    r = p.add_run(); r.font.size = Pt(10); r.font.name = FONT
    a = OxmlElement('w:fldChar'); a.set(qn('w:fldCharType'), 'begin'); r._r.append(a)
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = instr; r._r.append(it)
    c = OxmlElement('w:fldChar'); c.set(qn('w:fldCharType'), 'separate'); r._r.append(c)
    t = OxmlElement('w:t'); t.text = '1'; r._r.append(t)
    e = OxmlElement('w:fldChar'); e.set(qn('w:fldCharType'), 'end'); r._r.append(e)
for s_ in d.sections:
    fp = s_.footer.paragraphs[0]; fp.alignment = AL.CENTER; fld(fp, 'PAGE')
d.sections[-1].bottom_margin = Inches(0.8); d.sections[-1].footer_distance = Inches(0.3)
d.core_properties.title = 'ALM Report - Adaptive AR Work Instructions for Machine Assembly Lines'
d.save('ALM_Adaptive_AR_Work_Instructions.docx')
