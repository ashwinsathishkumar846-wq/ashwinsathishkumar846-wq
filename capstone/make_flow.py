from PIL import Image, ImageDraw, ImageFont
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f = ImageFont.truetype(F, 21); fb = ImageFont.truetype(FB, 22); fs = ImageFont.truetype(F, 19)
W, H = 1000, 1430
im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
CX = 340; BW, BH, DW, DH, GAP = 400, 64, 400, 104, 34
GREEN = (11, 93, 59); LIGHT = (220, 240, 228); RED = (254, 226, 226); REDL = (220, 38, 38)

def text_c(cx, cy, s, font=f, fill='black'):
    lines = s.split('\n'); lh = font.size + 4; y = cy - lh * len(lines) / 2
    for ln in lines:
        w = d.textlength(ln, font=font); d.text((cx - w / 2, y), ln, font=font, fill=fill); y += lh
def arrow(x1, y1, x2, y2, col=(60, 60, 60)):
    d.line([(x1, y1), (x2, y2)], fill=col, width=3)
    if x1 == x2: d.polygon([(x2, y2), (x2 - 8, y2 - 14), (x2 + 8, y2 - 14)], fill=col)
    else:
        s = 1 if x2 > x1 else -1; d.polygon([(x2, y2), (x2 - s * 14, y2 - 8), (x2 - s * 14, y2 + 8)], fill=col)
y = 14; centers = {}
def oval(s):
    global y
    d.rounded_rectangle([CX - 130, y, CX + 130, y + 52], radius=26, fill=GREEN); text_c(CX, y + 26, s, fb, 'white')
    c = y + 52; y += 52 + GAP; return c
def box(s, h=BH):
    global y
    d.rectangle([CX - BW // 2, y, CX + BW // 2, y + h], fill=LIGHT, outline=GREEN, width=3); text_c(CX, y + h / 2, s)
    c = y + h; y += h + GAP; return c
def diamond(s, side_msg, side_label='No'):
    global y
    cy = y + DH / 2
    d.polygon([(CX, y), (CX + DW // 2, cy), (CX, y + DH), (CX - DW // 2, cy)], fill=(255, 247, 214), outline=(180, 120, 0))
    d.line([(CX, y), (CX + DW // 2, cy), (CX, y + DH), (CX - DW // 2, cy), (CX, y)], fill=(180, 120, 0), width=3)
    text_c(CX, cy, s, fs)
    x2 = CX + DW // 2
    arrow(x2, cy, 700, cy); d.text((x2 + 8, cy - 28), side_label, font=fs, fill=REDL)
    d.rectangle([700, cy - 32, 980, cy + 32], fill=RED, outline=REDL, width=3); text_c(840, cy, side_msg, fs)
    c = y + DH; y += DH + GAP; return c
steps = [('oval', 'START'), ('box', 'Student enters roll number\nand password'),
         ('dia', 'Valid login?', 'Show login\nerror message'), ('box', 'Show course catalogue\n(search / filter available)'),
         ('box', 'Student clicks Register\non a course'), ('dia', 'Seats left > 0 ?', 'Show "Course\nis full"'),
         ('dia', 'Credits within\nlimit of 24 ?', 'Show "Credit limit\nexceeded"'), ('dia', 'Time-slot free\n(no clash) ?', 'Show "Time clash"\nmessage'),
         ('box', 'Save registration in\nlocalStorage'), ('box', 'Update seats, credits,\nMy Registrations, Timetable'), ('oval', 'END')]
prev = None
for s in steps:
    top = y
    if prev is not None: arrow(CX, prev, CX, top)
    if s[0] == 'oval': prev = oval(s[1])
    elif s[0] == 'box': prev = box(s[1])
    else:
        lab = s[1]; prev = diamond(lab, s[2], 'No')
        if s[1].startswith('Time'): pass
    # 'Yes' labels
    if s[0] == 'dia': d.text((CX + 10, prev + 2), 'Yes', font=fs, fill=(22, 101, 52))
im = im.crop((0, 0, W, int(y - GAP + 14)))
im.save('shots/flow.png'); print(im.size)
