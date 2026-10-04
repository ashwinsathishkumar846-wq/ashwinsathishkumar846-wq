
# ---------- footer page numbers, margins ----------
sec = d.sections[0]
sec.bottom_margin = Inches(0.8); sec.footer_distance = Inches(0.3)
fp = sec.footer.paragraphs[0]; fp.alignment = AL.CENTER
def fld(p, instr):
    r = p.add_run(); r.font.size = Pt(10); r.font.name = FONT
    a = OxmlElement('w:fldChar'); a.set(qn('w:fldCharType'), 'begin'); r._r.append(a)
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = instr; r._r.append(it)
    c = OxmlElement('w:fldChar'); c.set(qn('w:fldCharType'), 'separate'); r._r.append(c)
    t = OxmlElement('w:t'); t.text = '1'; r._r.append(t)
    e = OxmlElement('w:fldChar'); e.set(qn('w:fldCharType'), 'end'); r._r.append(e)
fld(fp, 'PAGE')

# header only on pages 1-3 (cover, index, contents): section break after the contents table
tbl_el = t1._tbl
tail_p = tbl_el.getnext()
while tail_p is not None and tail_p.tag != qn('w:p'): tail_p = tail_p.getnext()
tail_p.getparent()  # paragraph after contents table
Paragraph(tail_p, d).paragraph_format.page_break_before = False
tail_p.get_or_add_pPr().append(copy.deepcopy(sect))
drop_blanks_after(tail_p)
last = d.sections[-1]
for hr in last._sectPr.findall(qn('w:headerReference')): last._sectPr.remove(hr)
last.header.is_linked_to_previous = False
for p_ in last.header.paragraphs:
    for r_ in list(p_.runs): r_._r.getparent().remove(r_._r)
last.top_margin = Inches(0.75)
d.core_properties.title = 'ALM Report - Temperature Monitoring System using LPC2148'
d.save('ALM_Temperature_Monitoring_LPC2148.docx')
