"""Render a compact editorial broadsheet for Thursday 19 November 2026."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 240, 222)
PANEL = (251, 248, 239)
INK = (24, 39, 54)
RED = (164, 54, 43)
BLUE = (44, 89, 122)
GOLD = (185, 132, 44)
GREEN = (55, 112, 89)
MUTED = (83, 88, 84)
DISPLAY = "/usr/share/fonts/truetype/sand-box/google/Playfair Display/PlayfairDisplay-VariableFont_wght.ttf"
LABEL = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
BODY = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)


def f(path, size):
    return ImageFont.truetype(path, size)


def txt(x, y, s, size, color=INK, face=BODY):
    d.text((x, y), s, font=f(face, size), fill=color)


def lines(s, face, size, width):
    ft = f(face, size)
    result, current = [], ""
    for word in s.split():
        test = (current + " " + word).strip()
        if d.textlength(test, font=ft) <= width:
            current = test
        else:
            if current:
                result.append(current)
            current = word
    if current:
        result.append(current)
    return result


def para(x, y, s, size, width, color=MUTED, face=BODY, leading=2, limit=None):
    rows = lines(s, face, size, width)
    if limit and len(rows) > limit:
        rows = rows[:limit]
        rows[-1] = rows[-1].rstrip(" ,;:") + "…"
    for i, row in enumerate(rows):
        txt(x, y + i * (size + leading), row, size, color, face)
    return y + len(rows) * (size + leading)


def rule(y, x1=24, x2=1000, color=INK, width=1):
    d.line((x1, y, x2, y), fill=color, width=width)


def badge(x, y, s, color):
    ft = f(LABEL, 9)
    w = int(d.textlength(s, font=ft)) + 14
    d.rounded_rectangle((x, y, x+w, y+18), 8, fill=color)
    d.text((x+7, y+3), s, font=ft, fill=(255, 251, 240))


def hero_art_shenzhen(x, y, w, h):
    # Conference hall, three delegates and recognizable national flag blocks.
    d.rectangle((x,y,x+w,y+h), fill=(220,216,199))
    d.rectangle((x+8,y+7,x+w-8,y+34), fill=(236,230,212))
    txt(x+18,y+13,"SHENZHEN  ·  LEADERS' TABLE",11,BLUE,LABEL)
    d.polygon([(x+12,y+49),(x+w-12,y+49),(x+w-28,y+69),(x+28,y+69)], fill=(186,175,149), outline=INK)
    # Flag stands: US stripes, Chinese red/gold, Russian tricolour.
    for fx,kind in [(x+40,"us"),(x+w//2-17,"cn"),(x+w-72,"ru")]:
        d.line((fx+17,y+38,fx+17,y+91),fill=INK,width=2)
        if kind=="us":
            for j in range(7): d.rectangle((fx,y+42+j*4,fx+34,y+46+j*4),fill=(191,49,49) if j%2==0 else (255,253,242))
            d.rectangle((fx,y+42,fx+14,y+58),fill=(42,67,112))
        elif kind=="cn":
            d.rectangle((fx,y+42,fx+34,y+70),fill=(195,44,42))
            d.polygon([(fx+8,y+46),(fx+10,y+51),(fx+15,y+51),(fx+11,y+54),(fx+13,y+60),(fx+8,y+56),(fx+4,y+60),(fx+5,y+54),(fx+1,y+51),(fx+6,y+51)],fill=(245,205,73))
        else:
            d.rectangle((fx,y+42,fx+34,y+51),fill=(255,255,248)); d.rectangle((fx,y+51,fx+34,y+60),fill=(55,87,132)); d.rectangle((fx,y+60,fx+34,y+69),fill=(191,52,47))
    # Distinct seated silhouettes around an oval table.
    d.ellipse((x+36,y+76,x+w-36,y+h-3),fill=(156,112,76),outline=INK,width=2)
    for cx,coat in [(x+72,(37,52,70)),(x+w//2,(44,61,76)),(x+w-72,(39,54,70))]:
        d.ellipse((cx-12,y+69,cx+12,y+93),fill=(207,169,134),outline=INK)
        d.polygon([(cx-23,y+96),(cx+23,y+96),(cx+28,y+127),(cx-28,y+127)],fill=coat,outline=INK)
    d.rounded_rectangle((x+w//2-43,y+105,x+w//2+43,y+127),3,fill=PAPER,outline=INK,width=2)
    txt(x+w//2-32,y+109,"PEACE",10,INK,LABEL)


def hero_art_court(x, y, w, h):
    d.rectangle((x,y,x+w,y+h),fill=(220,227,220))
    # Large triangular pediment, classical columns and steps.
    d.rectangle((x+18,y+74,x+w-18,y+h-8),fill=(200,210,201),outline=INK,width=2)
    d.polygon([(x+12,y+69),(x+w-12,y+69),(x+w//2,y+43)],fill=(231,228,210),outline=INK)
    d.rectangle((x+13,y+67,x+w-13,y+80),fill=(187,195,182),outline=INK,width=2)
    for px in range(x+31,x+w-24,29):
        d.rectangle((px,y+81,px+16,y+h-14),fill=(242,237,219),outline=INK,width=1)
        d.rectangle((px+5,y+87,px+11,y+h-19),fill=(202,194,174))
    d.rectangle((x+8,y+h-13,x+w-8,y+h-7),fill=(166,179,166),outline=INK)
    # Scales sit large and clearly above the roof line.
    sx=x+w//2; sy=y+16
    d.line((sx,sy,sx,sy+35),fill=RED,width=4)
    d.ellipse((sx-6,sy-6,sx+6,sy+6),fill=GOLD,outline=INK)
    d.line((sx-39,sy+6,sx+39,sy+6),fill=INK,width=4)
    for bx in (sx-31,sx+31):
        d.line((bx,sy+7,bx-12,sy+32),fill=INK,width=2)
        d.line((bx,sy+7,bx+12,sy+32),fill=INK,width=2)
        d.arc((bx-14,sy+26,bx+14,sy+42),0,180,fill=GOLD,width=3)


def hero_art_ipo(x,y,w,h):
    d.rectangle((x,y,x+w,y+h),fill=(222,232,224))
    # Trading board with baseline, high contrast upward green path and ANT mark.
    d.rounded_rectangle((x+w-111,y+10,x+w-14,y+48),7,fill=INK)
    txt(x+w-99,y+15,"ANT",24,(255,255,248),LABEL)
    txt(x+15,y+13,"IPO  ·  $83 / SHARE",11,BLUE,LABEL)
    d.line((x+29,y+61,x+29,y+h-14),fill=INK,width=3)
    d.line((x+29,y+h-14,x+w-15,y+h-14),fill=INK,width=3)
    pts=[(x+42,y+h-27),(x+79,y+h-43),(x+116,y+h-38),(x+151,y+h-58),(x+190,y+73),(x+229,y+52),(x+w-30,y+55)]
    d.line(pts,fill=(33,139,78),width=7,joint="curve")
    for px,py in pts: d.ellipse((px-5,py-5,px+5,py+5),fill=(33,139,78),outline=(255,255,255),width=2)
    d.polygon([(x+w-40,y+55),(x+w-55,y+49),(x+w-51,y+65)],fill=(33,139,78))


def icon(x,y,kind,color):
    # Strong silhouette icons, consistently drawn with broad strokes.
    if kind=="game":
        d.rounded_rectangle((x,y+8,x+43,y+34),9,outline=color,width=3)
        d.line((x+9,y+21,x+21,y+21),fill=color,width=3); d.line((x+15,y+15,x+15,y+27),fill=color,width=3)
        d.ellipse((x+29,y+16,x+34,y+21),fill=color); d.ellipse((x+35,y+23,x+40,y+28),fill=color)
    elif kind=="bridge":
        d.line((x,y+32,x+45,y+32),fill=color,width=3); d.arc((x+3,y+8,x+42,y+43),180,360,fill=color,width=3)
        for px in (x+9,x+21,x+33): d.line((px,y+22,px,y+32),fill=color,width=2)
    elif kind=="tank":
        d.rectangle((x+5,y+17,x+35,y+31),outline=color,width=3); d.line((x+20,y+17,x+37,y+9),fill=color,width=4)
        d.line((x+7,y+34,x+36,y+34),fill=color,width=4)
        for px in (x+12,x+21,x+30): d.ellipse((px,y+29,px+6,y+35),fill=color)
    elif kind=="tower":
        d.polygon([(x+9,y+38),(x+13,y+8),(x+31,y+8),(x+36,y+38)],outline=color)
        for yy in (15,23,31): d.line((x+13,yy,x+33,yy),fill=color,width=2)
    elif kind=="storm":
        d.arc((x+3,y+5,x+38,y+30),180,360,fill=color,width=3); d.line((x+8,y+22,x+34,y+22),fill=color,width=3)
        d.line((x+17,y+26,x+12,y+36,x+22,y+31,x+17,y+41),fill=color,width=3)
    elif kind=="leaf":
        d.ellipse((x+4,y+7,x+41,y+35),outline=color,width=3); d.line((x+9,y+33,x+36,y+10),fill=color,width=3)
    elif kind=="globe":
        d.ellipse((x+5,y+5,x+39,y+39),outline=color,width=3); d.arc((x+14,y+5,x+30,y+39),0,360,fill=color,width=2)
        d.line((x+6,y+22,x+38,y+22),fill=color,width=2)
    elif kind=="school":
        d.polygon([(x+3,y+18),(x+22,y+4),(x+41,y+18)],outline=color,width=3); d.rectangle((x+8,y+18,x+36,y+39),outline=color,width=3)
        d.rectangle((x+18,y+27,x+26,y+39),outline=color,width=2)
    elif kind=="gavel":
        d.line((x+12,y+10,x+33,y+31),fill=color,width=6); d.line((x+7,y+6,x+17,y+16),fill=color,width=7)
        d.line((x+28,y+26,x+38,y+36),fill=color,width=7); d.line((x+6,y+40,x+40,y+40),fill=color,width=3)
    else:
        d.ellipse((x+7,y+7,x+39,y+39),outline=color,width=3); d.line((x+23,y+10,x+23,y+36),fill=color,width=3)
        d.line((x+10,y+23,x+36,y+23),fill=color,width=3)


# A clear publication masthead and calendar slug.
d.rectangle((0,0,W,10),fill=INK)
txt(27,17,"THE WORLD'S NEWS IN ONE PICTURE",14,RED,LABEL)
txt(24,35,"Thursday 19 November 2026",43,INK,DISPLAY)
txt(29,88,"Everything on this page happened, or was first reported, on Thursday 19 November 2026.",12,MUTED,BODY)
d.rounded_rectangle((855,19,999,99),7,fill=INK)
txt(870,23,"19",43,(255,250,237),DISPLAY)
txt(931,37,"THU",15,(241,195,93),LABEL)
txt(931,61,"2026",15,(255,250,237),LABEL)
rule(112,24,1000,INK,2)

# Seven regional shares total 42 reported items: 3 leads, 9 briefs, 30 listed files.
txt(27,119,"42 STORIES",11,RED,LABEL)
regions=[("EUROPE",8,BLUE),("MIDDLE EAST",6,RED),("ASIA",9,GOLD),("AFRICA",5,GREEN),("AMERICAS",8,(115,79,125)),("OCEANIA",2,(68,119,126)),("WORLD",4,INK)]
xx=144
for name,n,col in regions:
    ww=n/42*856
    d.rectangle((xx,121,xx+ww,133),fill=col)
    if ww>62: txt(xx+4,122,name,8,(255,255,255),LABEL)
    xx+=ww
txt(27,137,"EUROPE 8  ·  MIDDLE EAST 6  ·  ASIA 9  ·  AFRICA 5  ·  AMERICAS 8  ·  OCEANIA 2  ·  WORLD 4",9,INK,LABEL)

# Three large, equal hero panels with artwork taking most of each panel.
rule(157,24,1000,(173,159,136),1)
heroes=[
 ("ASIA · APEC","A Shenzhen declaration","Trump, Xi and Putin issue their first trilateral ‘Declaration Toward Peace’ after about 90 minutes. It covers UN reform, refined petroleum supply, nuclear-risk dialogue and ICC jurisdiction language.",BLUE,hero_art_shenzhen),
 ("THE HAGUE · LAW","Myanmar committed genocide","In Gambia v Myanmar, the ICJ makes its first finding that a state committed genocide. President Yuji Iwasawa; restitution, return and compensation are for a later phase.",RED,hero_art_court),
 ("NASDAQ · MARKETS","Anthropic begins trading","ANT opens after a record IPO priced at $83: 980 million Class A shares and an implied valuation near $1.5 trillion. Pricing was Wednesday; trading begins Thursday.",GREEN,hero_art_ipo),
]
for i,(tag,title,body,col,art) in enumerate(heroes):
    x=24+i*327; y=165; w=315; h=320
    d.rounded_rectangle((x,y,x+w,y+h),6,fill=PANEL,outline=(191,179,155),width=1)
    badge(x+10,y+9,tag,col)
    art(x+10,y+34,w-20,148)
    txt(x+11,y+189,title,16,INK,SERIF)
    para(x+11,y+215,body,11,w-22,MUTED,BODY,2,7)
    txt(x+11,y+300,"THURSDAY FILE  ·  CLAIMS ATTRIBUTED",8,col,LABEL)

# Nine compact but readable illustrated cards (the tenth story is the lead trio).
txt(26,493,"MORE FROM THURSDAY",12,RED,LABEL)
txt(800,495,"NINE DESK BRIEFS",9,MUTED,LABEL)
rule(510,24,1000,(173,159,136),1)
briefs=[
 ("GAMES · TOKYO","GTA VI launches on PS5 and Xbox Series.","game",(115,79,125)),
 ("BLACK SEA · KYIV","Putin vows a ‘far more painful’ response after third Kerch/Crimea bridge strike this week.","bridge",BLUE),
 ("GAZA · MIDDLE EAST","Israel says its tank raid across the yellow line has concluded.","tank",RED),
 ("RIYADH · GULF","Houthi missile damages PIF Tower; no injuries reported.","tower",RED),
 ("ODISHA · INDIA","Akvan: 100,000+ evacuated before Friday landfall near Gopalpur.","storm",GOLD),
 ("COP31 · ANTALYA","Second draft drops fossil-fuel transition language; keeps electrification.","leaf",GREEN),
 ("MOGADISHU · AFRICA","Somalia orders UAE ambassador to leave within 72 hours.","globe",GREEN),
 ("COPENHAGEN · ARCTIC","Danish MPs approve Greenland–US security pact, 109–0.","gavel",BLUE),
 ("FLORIDA · US","Broward schools close again after Hollywood flooding.","school",(115,79,125)),
]
for i,(tag,body,kind,col) in enumerate(briefs):
    row=i//3; c=i%3; x=24+c*327; y=517+row*53
    d.rounded_rectangle((x,y,x+315,y+48),4,fill=PANEL,outline=(213,202,181))
    icon(x+9,y+5,kind,col)
    txt(x+60,y+5,tag,8,col,LABEL)
    para(x+60,y+17,body,9,245,INK,BODY,1,3)

# Remaining 30 city-tagged one-line files; contested Senegal boat item omitted.
txt(26,681,"ALSO ON THURSDAY 19 NOVEMBER",12,RED,LABEL)
txt(774,684,"CITY TAG · FILE NOTE",9,MUTED,LABEL)
rule(699,24,1000,(173,159,136),1)
files=[
 ("CANBERRA","October jobless rate rises to 4.9%."),
 ("APEC · SHENZHEN","Albanese tells Putin: ‘End your war, end it now.’"),
 ("SOTHEBY'S · NY","Van Gogh sells for $190.4m, an auction record."),
 ("BERLIN","Ukraine allies meet on air defence, energy and finance."),
 ("THE HAGUE","Russia embassy asks if Netherlands joined conflict after Ruta missiles used on bridge."),
 ("LONDON–BRUSSELS","UK–EU reset talks go ‘down to the wire’; Burnham due Friday."),
 ("IEA · PARIS","World Energy Outlook: datacentre CO₂ emissions +70% by 2030."),
 ("DHAKA","Hasina shutdown; clashes; Yunus ancestral home torched; deaths reported."),
 ("NEW DELHI","Modi criticises India Inc on Make in India, wages and FTAs at FICCI."),
 ("APEC · SHENZHEN","Sheinbaum meets Singapore PM on Plan México."),
 ("BUENOS AIRES","Government advances 2027 PASO suspension in Senate committee."),
 ("BRASÍLIA","Lula regulates five-day workweek rules."),
 ("ABUJA","All 36 assemblies approve state police; presidential assent pending."),
 ("APEC · SHENZHEN","Japanese PM receives a frosty China welcome."),
 ("MUMBAI","Will and Kate hold an India meet-and-greet."),
 ("PARIS","Mélenchon polling chatter, as reported."),
 ("WASHINGTON","House passes Preventive Health Savings Act, 401–0."),
 ("US · NETWORKS","French government sites and NSA classified net briefly offline during patching; mission ops reported intact."),
 ("SHENZHEN","Leaders’ APEC day includes wider declaration follow-through."),
 ("GLOBAL MARKETS","Oil and equities track Anthropic’s first trading session."),
 ("SHENZHEN","Trump, Xi and Putin hold their first trilateral leaders’ meeting."),
 ("GENEVA","ICJ case enters later phase for remedies in Gambia v Myanmar."),
 ("KYIV","Air defence and winter energy support top allies’ Berlin agenda."),
 ("BRUSSELS","European partners discuss Ukraine’s finance needs."),
 ("ANTALYA","COP31 negotiators circulate their second draft text."),
 ("RIYADH","Damage assessment follows strike at PIF Tower."),
 ("ODISHA","Cyclone shelters and evacuation transport mobilise ahead of landfall."),
 ("COPENHAGEN","Greenland–US pact clears Danish MPs without dissent."),
 ("SYDNEY","Australian labour data shows unemployment at 4.9%."),
 ("NEW YORK","Sotheby’s Van Gogh sale sets a new auction high."),
]
cols=[26,222,418,614,810]
for i,(city,desc) in enumerate(files):
    c=i//6; r=i%6; x=cols[c]; y=716+r*23
    if r%2==0: d.rectangle((x-3,y-1,x+185,y+21),fill=(239,233,216))
    txt(x,y,city,7,BLUE,LABEL)
    para(x,y+8,desc,7,184,INK,BODY,0,2)

# Bottom map, legible key and an unmistakable Wednesday exclusion box.
mx,my,mw,mh=24,884,353,111
d.rounded_rectangle((mx,my,mx+mw,my+mh),5,fill=(231,235,223),outline=(166,180,168),width=2)
txt(mx+10,my+7,"WHERE IT HAPPENED",10,RED,LABEL)
# Simplified continent forms with numbered pins for the three leads and major files.
d.polygon([(mx+18,my+42),(mx+35,my+30),(mx+58,my+33),(mx+65,my+45),(mx+49,my+53),(mx+43,my+78),(mx+31,my+68),(mx+28,my+53)],fill=(191,205,190))
d.polygon([(mx+87,my+34),(mx+111,my+30),(mx+123,my+39),(mx+115,my+48),(mx+101,my+51),(mx+97,my+68),(mx+88,my+52)],fill=(191,205,190))
d.polygon([(mx+139,my+39),(mx+167,my+31),(mx+192,my+39),(mx+183,my+50),(mx+160,my+48),(mx+149,my+60),(mx+138,my+51)],fill=(191,205,190))
d.polygon([(mx+169,my+56),(mx+183,my+58),(mx+180,my+79),(mx+168,my+74)],fill=(191,205,190))
d.polygon([(mx+217,my+38),(mx+243,my+33),(mx+257,my+42),(mx+247,my+50),(mx+227,my+47)],fill=(191,205,190))
d.polygon([(mx+247,my+68),(mx+268,my+63),(mx+286,my+72),(mx+276,my+82),(mx+253,my+78)],fill=(191,205,190))
for px,py,n in [(151,42,1),(101,43,2),(284,43,3),(177,53,4),(164,51,5),(46,50,6),(274,72,7)]:
    cx=mx+px; cy=my+py
    d.ellipse((cx-8,cy-8,cx+8,cy+8),fill=RED if n<4 else BLUE,outline=(255,255,255),width=2)
    d.text((cx-3,cy-6),str(n),font=f(LABEL,9),fill=(255,255,255))
txt(mx+12,my+88,"1–3 HEROES  ·  4–7 DISPATCHES",8,INK,LABEL)

dx,dy,dw,dh=390,858,610,137
d.rounded_rectangle((dx,dy,dx+dw,dy+dh),6,fill=(253,246,232),outline=RED,width=5)
d.rectangle((dx+2,dy+2,dx+dw-2,dy+34),fill=(247,222,206))
txt(dx+13,dy+7,"DATE CHECK — LEFT OFF THIS PAGE",17,RED,LABEL)
txt(dx+14,dy+43,"WEDNESDAY 18 NOVEMBER 2026",10,INK,LABEL)
wed=[
 ("IRAN–KUWAIT","Drone claims first reported Wednesday."),
 ("VOYAGER 1","Light-day milestone reported Wednesday."),
 ("JEFFRIES","Speaker nod belongs to Wednesday coverage."),
 ("ANTHROPIC","IPO pricing was Wednesday; ANT trading debut is Thursday."),
]
for i,(label,desc) in enumerate(wed):
    yy=dy+59+i*17
    txt(dx+15,yy,"•  "+label,9,RED,LABEL)
    txt(dx+139,yy,desc,9,INK,BODY)

rule(1001,24,1000,INK,1)
txt(25,1004,"SOURCES: Reuters · AP · AFP · BBC · Guardian · The Hindu · ABS · ICJ · White House · Rockstar · Take-Two",7,MUTED,BODY)

out=Path(__file__).resolve().parent/"entry.png"
im.save(out,format="PNG",optimize=True)
print(f"{im.size} {out.stat().st_size} bytes")
assert im.size==(1024,1024)
assert out.stat().st_size<=1048576
