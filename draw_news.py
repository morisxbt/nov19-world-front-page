from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFont


W = H = 1024
PAPER = (246, 240, 222)
INK = (24, 39, 54)
MUTED = (87, 91, 88)
RED = (164, 54, 43)
BLUE = (44, 89, 122)
GOLD = (185, 132, 44)
GREEN = (55, 112, 89)
PURPLE = (115, 79, 125)
DISPLAY = "/usr/share/fonts/truetype/sand-box/google/Playfair Display/PlayfairDisplay-VariableFont_wght.ttf"
LABEL = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
BODY = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)


def font(path, size):
    return ImageFont.truetype(path, size)


def text(x, y, s, size=12, color=INK, face=BODY):
    d.text((x, y), s, font=font(face, size), fill=color)


def wrap(s, f, width):
    lines, line = [], ""
    for word in s.split():
        trial = (line + " " + word).strip()
        if d.textlength(trial, font=f) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def paragraph(x, y, s, size, width, color=INK, face=BODY, leading=2, max_lines=None):
    f = font(face, size)
    lines = wrap(s, f, width)
    if max_lines:
        lines = lines[:max_lines]
        if len(wrap(s, f, width)) > max_lines:
            lines[-1] = lines[-1].rstrip(".,;:") + "…"
    for i, line in enumerate(lines):
        d.text((x, y + i * (size + leading)), line, font=f, fill=color)
    return y + len(lines) * (size + leading)


def rule(y, x1=24, x2=1000, color=INK, width=1):
    d.line((x1, y, x2, y), fill=color, width=width)


def pill(x, y, label, color):
    f = font(LABEL, 9)
    w = int(d.textlength(label, font=f)) + 14
    d.rounded_rectangle((x, y, x + w, y + 17), radius=7, fill=color)
    d.text((x + 7, y + 3), label, font=f, fill=(255, 252, 243))


def globe_icon(cx, cy, r, color):
    d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=color, width=2)
    d.arc((cx-r//2, cy-r, cx+r//2, cy+r), 0, 360, fill=color, width=1)
    d.arc((cx-r, cy-r//2, cx+r, cy+r//2), 0, 360, fill=color, width=1)
    d.line((cx-r, cy, cx+r, cy), fill=color, width=1)


def art_table(x, y, w, h):
    d.rectangle((x, y, x+w, y+h), fill=(224, 215, 191))
    d.rectangle((x+5,y+5,x+w-5,y+23),fill=(236,230,213))
    text(x+11,y+8,"SHENZHEN · TRILATERAL TALKS",8,INK,LABEL)
    d.ellipse((x+10, y+25, x+w-10, y+h-1), fill=(173, 130, 89), outline=INK, width=2)
    # Distinct US, China and Russia flag panels anchor the three delegates.
    delegates=[(x+53,(38,53,67),"US"),(x+w//2,(49,68,81),"CN"),(x+w-53,(37,52,69),"RU")]
    for cx,coat,country in delegates:
        d.ellipse((cx-11,y+25,cx+11,y+47),fill=(210,174,139),outline=INK)
        d.polygon([(cx-18,y+50),(cx+18,y+50),(cx+24,y+80),(cx-24,y+80)],fill=coat,outline=INK)
        fx=cx-16; fy=y+51
        if country=="US":
            for stripe in range(5):
                d.rectangle((fx,fy+stripe*3,fx+32,fy+stripe*3+2),fill=(190,48,48) if stripe%2==0 else (255,255,245))
            d.rectangle((fx,fy,fx+12,fy+8),fill=(43,69,113))
        elif country=="CN":
            d.rectangle((fx,fy,fx+32,fy+15),fill=(195,45,43))
            d.polygon([(fx+7,fy+2),(fx+9,fy+6),(fx+13,fy+6),(fx+10,fy+9),(fx+11,fy+13),(fx+7,fy+10),(fx+3,fy+13),(fx+4,fy+9),(fx+1,fy+6),(fx+5,fy+6)],fill=(245,205,74))
        else:
            d.rectangle((fx,fy,fx+32,fy+5),fill=(255,255,248)); d.rectangle((fx,fy+5,fx+32,fy+10),fill=(53,86,133)); d.rectangle((fx,fy+10,fx+32,fy+15),fill=(190,53,48))
    d.rounded_rectangle((x+w//2-39,y+61,x+w//2+39,y+78), radius=2, fill=PAPER, outline=INK)
    text(x+w//2-29,y+64,"PEACE",8,INK,LABEL)


def art_court(x, y, w, h):
    d.rectangle((x, y, x+w, y+h), fill=(220, 226, 221))
    # Symmetric neoclassical court with a prominent, balanced scale.
    d.rectangle((x+8,y+61,x+w-8,y+h-5),fill=(205,214,207))
    d.polygon([(x+13,y+43),(x+w-13,y+43),(x+w//2,y+25)],fill=(186,197,188),outline=INK)
    d.rectangle((x+14,y+43,x+w-14,y+52),fill=(218,220,204),outline=INK)
    for px in range(x+26,x+w-20,22):
        d.rectangle((px,y+52,px+11,y+h-10),fill=(238,234,216),outline=INK,width=1)
        d.rectangle((px+3,y+57,px+8,y+h-14),fill=(203,195,174))
    d.rectangle((x+7,y+h-10,x+w-7,y+h-5),fill=(156,170,158),outline=INK)
    sx=x+w//2; sy=y+9
    d.line((sx,sy,sx,sy+30),fill=RED,width=3)
    d.ellipse((sx-4,sy-4,sx+4,sy+4),fill=GOLD,outline=INK)
    d.line((sx-27,sy+8,sx+27,sy+8),fill=INK,width=3)
    for scx in (sx-22,sx+22):
        d.line((scx,sy+8,scx-8,sy+24),fill=INK,width=2)
        d.line((scx,sy+8,scx+8,sy+24),fill=INK,width=2)
        d.arc((scx-9,sy+19,scx+9,sy+31),0,180,fill=GOLD,width=3)


def art_market(x, y, w, h):
    d.rectangle((x,y,x+w,y+h), fill=(221,229,224))
    d.line((x+13,y+h-13,x+w-12,y+h-13), fill=INK, width=2)
    d.line((x+13,y+12,x+13,y+h-13), fill=INK, width=2)
    text(x+18,y+8,"$83",10,INK,LABEL)
    pts=[(x+23,y+h-23),(x+48,y+h-34),(x+68,y+h-29),(x+91,y+45),(x+116,y+28)]
    d.line(pts, fill=(36,137,81), width=5, joint="curve")
    for px,py in pts:
        d.ellipse((px-4,py-4,px+4,py+4), fill=(36,137,81),outline=(255,255,255),width=1)
    d.rounded_rectangle((x+w-79,y+8,x+w-9,y+34), radius=4, fill=INK)
    text(x+w-70,y+10,"ANT",16,(255,255,255),LABEL)
    text(x+56,y+9,"FIRST DAY",8,BLUE,LABEL)


def mini_icon(x, y, kind, color):
    if kind == "controller":
        d.rounded_rectangle((x,y+4,x+34,y+24),radius=8,outline=color,width=2)
        d.line((x+8,y+14,x+17,y+14),fill=color,width=2); d.line((x+12,y+10,x+12,y+18),fill=color,width=2)
        d.ellipse((x+24,y+10,x+27,y+13),fill=color); d.ellipse((x+28,y+15,x+31,y+18),fill=color)
    elif kind == "bridge":
        d.line((x,y+23,x+36,y+23),fill=color,width=2); d.arc((x+3,y+8,x+33,y+31),180,360,fill=color,width=2)
        for xx in (x+7,x+17,x+27): d.line((xx,y+15,xx,y+23),fill=color,width=1)
    elif kind == "storm":
        d.arc((x+2,y+3,x+27,y+25),180,350,fill=color,width=2); d.line((x+12,y+21,x+8,y+29,x+16,y+25,x+12,y+32),fill=color,width=2)
    elif kind == "tower":
        d.rectangle((x+8,y+3,x+26,y+30),outline=color,width=2)
        for yy in (9,16,23): d.line((x+11,yy,x+23,yy),fill=color,width=1)
        d.line((x+3,y+28,x+32,y+28),fill=color,width=2)
    elif kind == "leaf":
        d.ellipse((x+3,y+4,x+31,y+25),outline=color,width=2); d.line((x+7,y+23,x+27,y+6),fill=color,width=2)
    elif kind == "globe":
        globe_icon(x+17,y+17,13,color)
    elif kind == "school":
        d.polygon([(x+2,y+14),(x+17,y+3),(x+32,y+14)],outline=color,fill=None)
        d.rectangle((x+5,y+14,x+29,y+30),outline=color,width=2); d.rectangle((x+14,y+20,x+20,y+30),outline=color)
    elif kind == "gavel":
        d.line((x+8,y+7,x+24,y+23),fill=color,width=4); d.line((x+4,y+3,x+12,y+11),fill=color,width=5); d.line((x+20,y+19,x+28,y+27),fill=color,width=5); d.line((x+7,y+30,x+30,y+30),fill=color,width=2)
    else:
        d.ellipse((x+5,y+5,x+29,y+29),outline=color,width=2)
        d.line((x+17,y+7,x+17,y+27),fill=color,width=2); d.line((x+7,y+17,x+27,y+17),fill=color,width=2)


# Masthead
d.rectangle((0,0,W,9), fill=INK)
text(25,17,"THE WORLD'S NEWS IN ONE PICTURE",13,RED,LABEL)
text(24,34,"Thursday 19 November 2026",39,INK,DISPLAY)
paragraph(27,83,"Everything on this page happened, or was first reported, on Thursday 19 November 2026.",12,690,MUTED,BODY)
d.rounded_rectangle((841,20,999,104),radius=5,fill=INK)
text(855,27,"19",41,(255,249,233),DISPLAY)
text(914,40,"THU",15,(239,194,99),LABEL)
text(914,62,"2026",14,(255,249,233),LABEL)
text(28,113,"A SINGLE DAY, ACROSS SEVEN DESKS",9,BLUE,LABEL)
rule(130,24,1000,INK,2)

# Region desk count totals 44
text(26,137,"44 DISPATCHES",10,RED,LABEL)
counts=[("EUROPE",8,BLUE),("MIDDLE EAST",7,RED),("ASIA",9,GOLD),("AFRICA",5,GREEN),("AMERICAS",8,PURPLE),("OCEANIA",2,(68,119,126)),("WORLD",5,INK)]
bx=159
for name,n,col in counts:
    ww=(n/44)*825
    d.rectangle((bx,139,bx+ww,150),fill=col)
    if ww>67: text(bx+4,139,name,8,(255,255,255),LABEL)
    bx+=ww
text(26,154,"EUROPE 8  ·  MIDDLE EAST 7  ·  ASIA 9  ·  AFRICA 5  ·  AMERICAS 8  ·  OCEANIA 2  ·  WORLD 5",9,INK,LABEL)

# Day in numbers strip
rule(172)
text(26,178,"THE DAY IN NUMBERS",10,RED,LABEL)
figures=[("90","MINUTES · SHENZHEN TALKS"),("1st","ICJ STATE GENOCIDE FINDING"),("$83","ANT IPO PRICE / SHARE"),("$1.5T","ANT IMPLIED VALUE"),("100k+","ODISHA EVACUATED"),("4.9%","AUSTRALIA JOBLESS RATE")]
xx=25
for i,(num,cap) in enumerate(figures):
    width=162
    text(xx,190,num,23,INK,DISPLAY)
    paragraph(xx,215,cap,8,width,BLUE,LABEL,1,2)
    if i<5: d.line((xx+151,188,xx+151,230),fill=(196,185,161),width=1)
    xx+=163
rule(237)

# Three lead stories with original hand-drawn scenes
leads=[
    ("ASIA · APEC", "A Shenzhen declaration", "Trump, Xi and Putin issue their first trilateral ‘Declaration Toward Peace’ after about 90 minutes. It covers UN reform, refined petroleum supply, nuclear-risk dialogue and ICC jurisdiction language.", "LEAD 01 · SHENZHEN", BLUE, art_table),
    ("THE HAGUE · LAW", "ICJ finds Myanmar committed genocide", "In Gambia v Myanmar, the court makes its first finding that a state committed genocide. President Yuji Iwasawa; restitution, return and compensation addressed in a later phase.", "LEAD 02 · ROHINGYA", RED, art_court),
    ("NASDAQ · MARKETS", "Anthropic begins trading", "ANT opens after a record IPO priced at $83: 980 million Class A shares and an implied valuation near $1.5 trillion. The pricing was Wednesday; trading begins Thursday.", "LEAD 03 · NEW YORK", GREEN, art_market),
]
for i,(tag,headline,body,kicker,col,art) in enumerate(leads):
    x=24+i*327; y=245; w=315; h=202
    d.rounded_rectangle((x,y,x+w,y+h),radius=4,fill=(251,248,238),outline=(198,187,164),width=1)
    pill(x+9,y+8,tag,col)
    art(x+9,y+34,w-18,78)
    text(x+10,y+116,headline,15,INK,SERIF)
    paragraph(x+10,y+137,body,10,w-20,MUTED,BODY,2,4)
    text(x+10,y+186,kicker,8,col,LABEL)

# Secondary desk: 12 illustrated briefs
text(25,454,"THE REST OF THE DAY",11,RED,LABEL)
text(800,454,"12 ILLUSTRATED BRIEFS",9,MUTED,LABEL)
rule(469,24,1000,(183,171,148),1)
briefs=[
 ("GAMES · TOKYO","GTA VI launches on PS5 and Xbox Series.","controller",PURPLE),
 ("BLACK SEA · KYIV","Putin vows a ‘far more painful’ response after a third Kerch/Crimea bridge strike this week.","bridge",BLUE),
 ("GAZA · MIDDLE EAST","Israel says its tank raid across the yellow line has concluded.","gavel",RED),
 ("RIYADH · GULF","Houthi missile damages PIF Tower; no injuries reported.","tower",RED),
 ("ODISHA · INDIA","Cyclone Akvan: 100,000+ evacuated ahead of Friday landfall near Gopalpur.","storm",GOLD),
 ("COP31 · ANTALYA","Second draft drops fossil-fuel transition language; electrification remains.","leaf",GREEN),
 ("MOGADISHU · AFRICA","Somalia orders UAE ambassador to leave within 72 hours.","globe",GREEN),
 ("COPENHAGEN · ARCTIC","Danish MPs approve Greenland–US security pact, 109–0.","globe",BLUE),
 ("FLORIDA · US","Broward schools close again after Hollywood flooding.","school",PURPLE),
 ("CANBERRA · AUSTRALIA","October jobless rate jumps to 4.9%.","globe",(68,119,126)),
 ("APEC · SHENZHEN","Albanese tells Putin: ‘End your war, end it now.’","gavel",GOLD),
 ("SOTHEBY'S · NEW YORK","Van Gogh’s Châtaigniers en fleurs sells for $190.4m, an auction record.","leaf",GREEN),
]
for i,(tag,body,kind,col) in enumerate(briefs):
    row=i//3; c=i%3; x=24+c*327; y=477+row*55; w=315
    d.rounded_rectangle((x,y,x+w,y+50),radius=3,fill=(250,247,237),outline=(218,208,187))
    mini_icon(x+8,y+9,kind,col)
    text(x+48,y+5,tag,8,col,LABEL)
    paragraph(x+48,y+17,body,9,w-57,MUTED,BODY,1,3)

# Also-on-Thursday list. All items are framed as reported developments.
text(25,704,"ALSO ON THURSDAY 19 NOVEMBER",11,RED,LABEL)
text(761,704,"CITY TAG · ONE-LINE FILE",8,MUTED,LABEL)
rule(719,24,1000,(183,171,148),1)
also=[
 ("BERLIN","Ukraine allies meet on air defence, energy and finance."),
 ("THE HAGUE","Russian embassy asks whether Netherlands joined conflict after Ruta missiles hit bridge."),
 ("LONDON–BRUSSELS","UK–EU reset talks go ‘down to the wire’; Burnham due Friday."),
 ("IEA · PARIS","Outlook projects data-centre CO₂ emissions +70% by 2030."),
 ("DHAKA","Awami League shutdown; clashes; Yunus ancestral home torched; deaths reported."),
 ("NEW DELHI","Modi criticises India Inc on Make in India, wages and FTAs at FICCI."),
 ("APEC · SHENZHEN","Sheinbaum and Singapore PM discuss Plan México."),
 ("BUENOS AIRES","Government advances 2027 PASO primary suspension in Senate committee."),
 ("BRASÍLIA","Lula regulates rules for a five-day, two-day-off workweek."),
 ("ABUJA","All 36 Nigerian state assemblies approve state police; assent pending."),
 ("YENNE · SENEGAL","Migrant boat capsizes; dozens reported missing, search continues."),
 ("APEC · SHENZHEN","Japanese PM receives a frosty welcome from China."),
 ("MUMBAI","Will and Kate hold an India meet-and-greet."),
 ("PARIS","French political polling chatter around Mélenchon, as reported."),
 ("WASHINGTON","House passes Preventive Health Savings Act, 401–0."),
 ("US · NETWORKS","French government sites and NSA classified network briefly offline during patching; operations reported intact."),
 ("SHENZHEN","Leaders’ APEC day includes wider follow-through on the declaration."),
 ("GLOBAL MARKETS","Oil and equities track Anthropic’s first trading session."),
 ("SHENZHEN","Trump, Xi and Putin complete their first three-way leaders’ talks."),
 ("GENEVA","ICJ opens the next phase on remedies in the Gambia–Myanmar case."),
 ("KYIV","Allies put air-defence systems and winter energy repairs on the agenda."),
 ("BRUSSELS","European diplomats weigh Ukraine finance options alongside weapons."),
 ("ANTALYA","COP31 negotiators circulate a revised draft text."),
 ("RIYADH","Authorities assess damage at the Public Investment Fund tower."),
 ("ODISHA","Emergency shelters and evacuation transport mobilised before landfall."),
 ("COPENHAGEN","Greenland agreement clears the Danish parliament without dissent."),
 ("SYDNEY","Australian labour data shows unemployment at its highest since 2021."),
 ("NEW YORK","Sotheby’s evening sale sets a Van Gogh auction benchmark."),
 ("ABUJA","State-police measure moves to the president after assembly approvals."),
]
colx=[26,222,418,614,810]
for i,(city,desc) in enumerate(also):
    c=i//6; r=i%6; x=colx[c]; y=728+r*30
    if i%2==0: d.rounded_rectangle((x-3,y-1,x+187,y+27),radius=2,fill=(239,233,216))
    text(x,y,city,7,BLUE,LABEL)
    paragraph(x,y+9,desc,7,184,INK,BODY,0,2)

# Map and prominent date-check box
map_x,map_y,map_w,map_h=24,916,369,78
d.rounded_rectangle((map_x,map_y,map_x+map_w,map_y+map_h),radius=4,fill=(232,235,222),outline=(179,188,174))
text(map_x+9,map_y+5,"WHERE IT HAPPENED",9,RED,LABEL)
# Simplified world silhouettes and route-like latitude lines
d.polygon([(map_x+18,map_y+30),(map_x+35,map_y+21),(map_x+55,map_y+25),(map_x+62,map_y+35),(map_x+48,map_y+43),(map_x+44,map_y+59),(map_x+33,map_y+53),(map_x+29,map_y+42)],fill=(195,207,190))
d.polygon([(map_x+86,map_y+27),(map_x+105,map_y+23),(map_x+119,map_y+31),(map_x+112,map_y+40),(map_x+101,map_y+41),(map_x+98,map_y+56),(map_x+89,map_y+48)],fill=(195,207,190))
d.polygon([(map_x+139,map_y+28),(map_x+165,map_y+23),(map_x+182,map_y+32),(map_x+175,map_y+39),(map_x+158,map_y+37),(map_x+148,map_y+48),(map_x+138,map_y+41)],fill=(195,207,190))
d.polygon([(map_x+168,map_y+44),(map_x+181,map_y+48),(map_x+177,map_y+64),(map_x+166,map_y+60)],fill=(195,207,190))
d.polygon([(map_x+212,map_y+28),(map_x+235,map_y+24),(map_x+248,map_y+31),(map_x+240,map_y+39),(map_x+225,map_y+37)],fill=(195,207,190))
d.polygon([(map_x+249,map_y+50),(map_x+269,map_y+47),(map_x+285,map_y+55),(map_x+276,map_y+62),(map_x+255,map_y+59)],fill=(195,207,190))
pins=[(151,32,1),(93,36,2),(286,33,3),(177,44,4),(168,42,5),(154,31,6),(44,39,7),(275,55,8)]
for px,py,n in pins:
    cx=map_x+px; cy=map_y+py
    d.ellipse((cx-6,cy-6,cx+6,cy+6),fill=RED if n<4 else BLUE,outline=(255,255,255),width=1)
    d.text((cx-3,cy-5),str(n),font=font(LABEL,8),fill=(255,255,255))
text(map_x+298,map_y+22,"1–3 LEADS",7,INK,LABEL)
text(map_x+298,map_y+34,"4–8 FILES",7,INK,LABEL)
text(map_x+298,map_y+49,"NOT TO SCALE",6,MUTED,BODY)

cx,cy,cw,ch=406,904,594,90
d.rounded_rectangle((cx,cy,cx+cw,cy+ch),radius=4,fill=(252,246,231),outline=RED,width=4)
d.rectangle((cx+1,cy+1,cx+cw-1,cy+21),fill=(249,225,210))
text(cx+10,cy+5,"DATE CHECK · LEFT OFF THIS PAGE",11,RED,LABEL)
paragraph(cx+10,cy+27,"Not Thursday’s news: Wednesday 18 Nov Iran–Kuwait drone claims; Voyager 1 light-day; Jeffries speaker nod; Bangladesh factory-shutdown figures first reported Wednesday. Anthropic IPO pricing was Wednesday; its trading debut is Thursday. No Nov 17 Sudan school strike without a Thursday first report.",9,cw-20,INK,BODY,1,6)

# Footer credits and explicit sourcing/attribution note
rule(1000,24,1000,INK,1)
text(25,1002,"SOURCES: Reuters · AP · AFP · BBC · Guardian · The Hindu · ABS · ICJ · White House · Rockstar · Take-Two",7,MUTED,BODY)
text(25,1012,"All 44 items happened or were first reported Thursday 19 Nov 2026; claims attributed. Original drawings.",7,INK,LABEL)

# Reproducibility guard: use only deterministic vector drawing; seed reserved for later texture work.
random.seed(19112026)
out = Path(__file__).resolve().parent / "entry.png"
im.save(out, format="PNG", optimize=True)
print(f"{im.size} {out.stat().st_size} bytes")
assert im.size == (1024, 1024)
assert out.stat().st_size <= 1048576

