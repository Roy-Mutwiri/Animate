from pathlib import Path
import subprocess
import time

ROOT = Path(r"D:\Animate\Projects\HonestInterview\DesignV3")
SRC = ROOT / "sources"
EXP = ROOT / "exports"
COMP = ROOT / "reference_comparisons"
REF = Path(r"D:\Animate\Projects\HonestInterview\ReferenceStudy\frames")
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

W, H = 1080, 1920


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SVG:
    def __init__(self, w=W, h=H, bg="#f1eadb"):
        self.w, self.h = w, h
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
            '<defs>',
            '<filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#1b1512" flood-opacity=".22"/></filter>',
            '<style>text{font-family:Arial,Helvetica,sans-serif;letter-spacing:0}.label{font-size:28px;fill:#2b211d;font-weight:700}.tiny{font-size:18px;fill:#504842}.note{font-size:22px;fill:#2b211d}</style>',
            '</defs>',
        ]
        if bg:
            self.parts.append(f'<rect width="{w}" height="{h}" fill="{bg}"/>')

    def add(self, s):
        self.parts.append(s)

    def save(self, path):
        self.parts.append("</svg>")
        path.write_text("\n".join(self.parts), encoding="utf-8")


def path(d, fill="none", stroke="#201713", sw=8, cap="round", join="round", extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="{join}" {extra}/>'


def ellipse(cx, cy, rx, ry, fill, stroke="#201713", sw=8, extra=""):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def circle(cx, cy, r, fill, stroke="#201713", sw=6):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, stroke="#201713", sw=9):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"/>'


def text(x, y, s, klass="label", anchor="start"):
    return f'<text x="{x}" y="{y}" class="{klass}" text-anchor="{anchor}">{esc(s)}</text>'


def chair(x, y, scale=1.0, flip=1):
    sx = scale * flip
    back = f"M{x-98*sx},{y-325*scale} C{x-40*sx},{y-370*scale} {x+80*sx},{y-340*scale} {x+108*sx},{y-250*scale} L{x+82*sx},{y-92*scale} L{x-88*sx},{y-88*scale} Z"
    seat = f"M{x-120*sx},{y-118*scale} C{x-40*sx},{y-145*scale} {x+62*sx},{y-135*scale} {x+126*sx},{y-102*scale} L{x+88*sx},{y-24*scale} L{x-118*sx},{y-34*scale} Z"
    arm = f"M{x-154*sx},{y-190*scale} C{x-118*sx},{y-210*scale} {x-76*sx},{y-194*scale} {x-68*sx},{y-154*scale} L{x-75*sx},{y-24*scale} L{x-150*sx},{y-22*scale} Z"
    leg = f"M{x-118*sx},{y-32*scale} L{x+92*sx},{y-22*scale} L{x+78*sx},{y+42*scale} L{x-142*sx},{y+28*scale} Z"
    return "\n".join([
        path(back, "#a89696", sw=5),
        path(seat, "#e6cfd0", sw=5),
        path(arm, "#7a6b69", sw=5),
        path(leg, "#62534f", sw=5),
    ])


def hand(x, y, angle=0, fill="#201713", scale=1):
    # Deliberately asymmetrical simple hand, not a circle.
    d = f"M{-18*scale},0 C{-12*scale},{-18*scale} {12*scale},{-20*scale} {20*scale},{-4*scale} C{28*scale},{12*scale} {12*scale},{26*scale} {-4*scale},{20*scale} C{-18*scale},{15*scale} {-25*scale},{9*scale} {-18*scale},0 Z"
    fingers = "".join([
        line(x-2*scale, y-17*scale, x-8*scale, y-33*scale, fill, 5*scale),
        line(x+8*scale, y-15*scale, x+9*scale, y-33*scale, fill, 5*scale),
        line(x+16*scale, y-7*scale, x+25*scale, y-22*scale, fill, 5*scale),
    ])
    return f'<g transform="translate({x},{y}) rotate({angle})">{path(d, fill, stroke=fill, sw=3)}</g>{fingers}'


def mic(x, y, angle=0, scale=1):
    return f'<g transform="translate({x},{y}) rotate({angle}) scale({scale})">' + \
        path("M-70,0 L6,0", stroke="#201713", sw=9) + \
        '<rect x="0" y="-25" width="58" height="50" rx="8" fill="#333645" stroke="#201713" stroke-width="7"/>' + \
        '<rect x="8" y="-17" width="42" height="34" rx="5" fill="#4c4f62" opacity=".55"/>' + \
        '</g>'


def interviewer_face(x, y, mood="neutral", scale=1, view="three"):
    s = scale
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    # long oval head with small dark cap/hair mass
    if view == "profile":
        g.append(path("M-55,-112 C15,-122 73,-67 70,4 C67,78 18,130 -48,105 C-98,86 -111,10 -94,-52 C-86,-82 -75,-101 -55,-112 Z", "#d8dad4", sw=7))
        g.append(path("M-100,-78 C-56,-128 18,-124 58,-92 C41,-74 -33,-75 -104,-56 Z", "#0c0c0d", sw=6))
    else:
        g.append(path("M-55,-130 C35,-145 98,-78 96,12 C94,103 34,152 -42,126 C-112,102 -128,8 -104,-72 C-94,-104 -79,-122 -55,-130 Z", "#d8dad4", sw=7))
        g.append(path("M-112,-86 C-65,-142 36,-142 86,-96 C44,-75 -25,-78 -122,-56 Z", "#0c0c0d", sw=6))
        g.append(circle(46, -104, 7, "#efe361", stroke="#0c0c0d", sw=3))
    # eyes, lids, brows
    if mood == "skeptical":
        lids = [(-38, -18, -12), (35, -12, 10)]
        mouth = "M-40,62 C-12,50 17,51 45,64"
        brows = [(-62,-55,-5), (22,-58,8)]
    elif mood == "speaking":
        lids = [(-38, -25, -5), (36, -26, 3)]
        mouth = "M-34,54 C-6,35 38,43 48,72 C20,92 -22,82 -34,54 Z"
        brows = [(-62,-62,3), (20,-63,-4)]
    elif mood == "annoyed":
        lids = [(-40, -12, -18), (38, -10, 18)]
        mouth = "M-42,58 C-4,67 25,65 52,55"
        brows = [(-64,-57,-15), (17,-57,15)]
    elif mood == "shock":
        lids = [(-42, -38, 0), (40, -38, 0)]
        mouth = "M-18,50 C5,30 38,44 35,77 C12,95 -18,78 -18,50 Z"
        brows = [(-64,-79,0), (18,-80,0)]
    elif mood == "smug":
        lids = [(-42, -10, -10), (36, -14, 5)]
        mouth = "M-36,58 C-2,78 35,72 55,54"
        brows = [(-62,-58,-5), (18,-60,-8)]
    else:
        lids = [(-38, -26, 0), (36, -26, 0)]
        mouth = "M-35,60 C-2,62 25,62 48,57"
        brows = [(-62,-60,0), (18,-60,0)]
    for ex, ey, rot in lids:
        g.append(f'<g transform="translate({ex},{ey}) rotate({rot})">{ellipse(0, 0, 24, 34, "#f7fbf6", sw=6)}{circle(6, 4, 8, "#111", stroke="#111", sw=2)}{path("M-27,-8 C-8,4 10,4 27,-8", stroke="#201713", sw=6)}</g>')
    for bx, by, rot in brows:
        g.append(f'<g transform="translate({bx},{by}) rotate({rot})">{path("M0,0 C21,-10 44,-8 61,1", stroke="#201713", sw=8)}</g>')
    g.append(path(mouth, "#181018" if mood in ("speaking","shock") else "none", sw=6))
    if mood == "speaking":
        g.append(path("M-17,56 C0,50 22,53 37,62", "#f1e5d8", sw=3))
    if mood == "shock":
        g.append(path("M-11,52 C6,46 22,50 29,61", "#f1e5d8", sw=3))
    g.append("</g>")
    return "\n".join(g)


def respondent_face(x, y, mood="neutral", scale=1, view="three"):
    s = scale
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    if view == "profile":
        g.append(path("M-64,-115 C36,-145 118,-78 107,22 C98,114 18,144 -66,104 C-122,77 -126,-62 -64,-115 Z", "#e8b083", sw=7))
    else:
        g.append(path("M-84,-112 C-12,-164 96,-134 126,-44 C158,52 104,139 4,142 C-95,145 -157,74 -134,-21 C-125,-59 -109,-91 -84,-112 Z", "#e8b083", sw=7))
    g.append(path("M-38,-118 C-10,-154 36,-150 62,-119", stroke="#201713", sw=8))
    g.append(path("M-2,-151 C0,-177 8,-185 14,-151 M25,-148 C31,-174 41,-178 42,-144 M-26,-140 C-32,-162 -23,-177 -14,-147", stroke="#201713", sw=8))
    if mood == "eager":
        eyes = [(-45,-26,31,43,5), (49,-24,31,43,-6)]
        mouth = "M-48,55 C-12,18 53,28 76,60 C47,100 -18,98 -48,55 Z"
        brows = [(-78,-72,-13), (20,-76,10)]
    elif mood == "yes":
        eyes = [(-50,-32,38,51,0), (52,-29,38,51,0)]
        mouth = "M-48,54 C-15,18 59,22 82,58 C56,102 -17,105 -48,54 Z"
        brows = [(-88,-84,-12), (20,-86,12)]
    elif mood == "smug":
        eyes = [(-48,-17,30,31,-5), (50,-20,30,31,4)]
        mouth = "M-58,58 C-15,98 48,90 82,50"
        brows = [(-82,-67,-6), (18,-70,-3)]
    elif mood == "annoyed":
        eyes = [(-48,-15,28,34,-7), (49,-17,28,34,7)]
        mouth = "M-52,60 C-10,60 30,61 72,56"
        brows = [(-88,-72,-18), (18,-72,18)]
    elif mood == "shock":
        eyes = [(-51,-37,43,58,0), (54,-36,43,58,0)]
        mouth = "M-16,43 C21,7 80,35 75,86 C39,128 -23,96 -16,43 Z"
        brows = [(-88,-96,0), (18,-96,0)]
    elif mood == "speaking":
        eyes = [(-45,-24,32,42,2), (49,-24,32,42,-2)]
        mouth = "M-46,58 C-18,33 38,37 69,59 C47,92 -16,91 -46,58 Z"
        brows = [(-82,-72,-8), (20,-73,8)]
    else:
        eyes = [(-45,-22,31,39,2), (48,-22,31,39,-2)]
        mouth = "M-48,62 C-12,68 28,68 68,60"
        brows = [(-82,-70,-4), (22,-71,4)]
    for ex, ey, rx, ry, rot in eyes:
        g.append(f'<g transform="translate({ex},{ey}) rotate({rot})">{ellipse(0,0,rx,ry,"#fbfff9",sw=7)}{circle(8,6,11,"#111",stroke="#111",sw=2)}{circle(12,0,3,"#fff",stroke="#fff",sw=1)}</g>')
    for bx, by, rot in brows:
        g.append(f'<g transform="translate({bx},{by}) rotate({rot})">{path("M0,0 C22,-12 48,-12 72,1", stroke="#201713", sw=8)}</g>')
    g.append(path(mouth, "#1b0f18" if mood in ("eager","yes","shock","speaking") else "none", sw=7))
    if mood in ("eager", "yes", "speaking"):
        g.append(path("M-22,54 C1,45 39,48 58,60", "#f6e8dc", sw=3))
    if mood == "shock":
        g.append(path("M-4,52 C18,43 50,48 64,65", "#f6e8dc", sw=3))
    g.append("</g>")
    return "\n".join(g)


def seated_interviewer(x, y, scale=1, mood="skeptical", prop=True):
    s=scale
    g=[f'<g transform="translate({x},{y}) scale({s})">']
    g.append(chair(0, 390, .86, flip=-1))
    # connected neck, torso, hips
    g.append(path("M-42,20 C-35,86 -50,140 -83,212 C-30,246 42,248 96,214 C67,132 39,75 28,18 Z", "#efe7dd", sw=7))
    g.append(path("M-17,-18 C-18,12 -20,33 -18,54 L25,54 C23,28 22,5 24,-20 Z", "#d8dad4", sw=6))
    g.append(path("M-72,220 C-20,244 50,244 100,218 L120,282 C38,326 -42,322 -112,282 Z", "#cfc2c0", sw=6))
    # seated legs: short thighs on cushion, bent calves to floor.
    g.append(path("M-78,246 C-42,278 10,292 58,286", stroke="#201713", sw=10))
    g.append(path("M44,286 C30,362 18,438 35,516", stroke="#201713", sw=10))
    g.append(path("M42,516 C78,524 105,517 130,500", stroke="#201713", sw=9))
    g.append(path("M42,250 C96,274 142,304 176,350", stroke="#201713", sw=10))
    g.append(path("M176,350 C170,420 188,486 226,532", stroke="#201713", sw=10))
    g.append(path("M226,532 C258,540 284,532 306,512", stroke="#201713", sw=9))
    # arms
    g.append(path("M-62,92 C-126,146 -132,214 -107,278", stroke="#201713", sw=9))
    if prop:
        g.append(path("M62,96 C142,120 198,146 252,164", stroke="#201713", sw=9))
        g.append(hand(252,164,12,scale=.72))
        g.append(mic(332,155,4,.85))
    else:
        g.append(path("M62,96 C132,94 188,70 242,32", stroke="#201713", sw=9))
        g.append(hand(242,32,-24,scale=.72))
    g.append(hand(-107,278,-15,scale=.72))
    # front chair lip to make hip contact explicit.
    g.append(path("M-118,274 C-42,304 62,306 138,276 L142,318 C52,354 -58,348 -142,314 Z", "#6b5d59", sw=5, extra='opacity=".86"'))
    g.append(interviewer_face(-18,-88,mood,1.0))
    g.append("</g>")
    return "\n".join(g)


def seated_respondent(x, y, scale=1, mood="eager", gesture="lap"):
    s=scale
    g=[f'<g transform="translate({x},{y}) scale({s})">']
    g.append(chair(0, 392, .82, flip=1))
    g.append(path("M-72,40 C-50,126 -58,190 -100,258 C-36,296 54,294 116,252 C80,173 54,104 28,42 Z", "#f0e4d7", sw=7))
    g.append(path("M-14,-18 C-22,18 -21,50 -10,68 L39,67 C34,37 30,9 36,-18 Z", "#e8b083", sw=6))
    g.append(path("M-90,254 C-22,284 64,284 124,252 L132,318 C44,354 -44,346 -128,316 Z", "#d7c3bd", sw=6))
    g.append(path("M-90,276 C-48,304 2,318 58,304", stroke="#201713", sw=10))
    g.append(path("M52,304 C38,374 44,448 88,514", stroke="#201713", sw=10))
    g.append(path("M88,514 C122,522 150,514 176,494", stroke="#201713", sw=9))
    g.append(path("M54,276 C112,300 158,330 194,374", stroke="#201713", sw=10))
    g.append(path("M194,374 C188,438 208,488 254,526", stroke="#201713", sw=10))
    g.append(path("M254,526 C288,534 318,524 344,502", stroke="#201713", sw=9))
    if gesture == "yes":
        g.append(path("M-72,120 C-156,82 -198,28 -218,-42", stroke="#201713", sw=9))
        g.append(hand(-218,-42,-36,scale=.78))
        g.append(path("M82,130 C154,158 214,182 270,198", stroke="#201713", sw=9))
        g.append(hand(270,198,10,scale=.72))
    elif gesture == "smug":
        g.append(path("M-70,116 C-138,154 -154,226 -126,286", stroke="#201713", sw=9))
        g.append(path("M78,122 C152,144 186,180 190,242", stroke="#201713", sw=9))
        g.append(hand(-126,286,5,scale=.72)); g.append(hand(190,242,-15,scale=.72))
    else:
        g.append(path("M-70,116 C-118,168 -130,218 -110,278", stroke="#201713", sw=9))
        g.append(path("M82,126 C148,164 174,218 162,282", stroke="#201713", sw=9))
        g.append(hand(-110,278,-10,scale=.72)); g.append(hand(162,282,12,scale=.72))
    g.append(path("M-130,306 C-42,346 80,344 150,310 L142,352 C50,384 -66,376 -154,340 Z", "#6b5d59", sw=5, extra='opacity=".86"'))
    g.append(respondent_face(8,-92,mood,1.0))
    g.append("</g>")
    return "\n".join(g)


def background(svg, floor=True):
    svg.add('<rect x="0" y="0" width="1080" height="1220" fill="#d2d0cc"/>')
    svg.add('<rect x="0" y="1220" width="1080" height="700" fill="#727775"/>')
    if floor:
        for i in range(-5, 10):
            x = i * 180
            svg.add(path(f"M{x},1920 L{x+550},1220", stroke="#555b59", sw=4, extra='opacity=".55"'))
        for j in range(0, 7):
            y = 1220 + j * 115
            svg.add(path(f"M0,{y} C310,{y+30} 760,{y-30} 1080,{y}", stroke="#555b59", sw=4, extra='opacity=".55"'))
    svg.add('<rect x="430" y="150" width="220" height="300" fill="#f9f9f4" stroke="#57514e" stroke-width="8"/>')
    svg.add(line(540,150,540,450,"#57514e",5)); svg.add(line(430,300,650,300,"#57514e",5))
    svg.add('<rect x="405" y="132" width="270" height="28" fill="#57514e"/>')
    svg.add('<ellipse cx="535" cy="1500" rx="420" ry="60" fill="#211814" opacity=".22"/>')
    # small table and plant
    svg.add(path("M455,1048 L626,1048 L658,1258 L420,1258 Z", "#50504b", sw=6))
    svg.add('<rect x="450" y="1086" width="176" height="54" fill="#41423e" stroke="#201713" stroke-width="5"/>')
    svg.add('<rect x="442" y="1164" width="190" height="58" fill="#41423e" stroke="#201713" stroke-width="5"/>')
    svg.add(circle(540,1114,6,"#caa8a4",sw=3)); svg.add(circle(540,1194,6,"#caa8a4",sw=3))
    svg.add(path("M525,1038 L555,1038 L575,1078 L505,1078 Z", "#a57a5d", sw=4))
    for dx in [-42,-20,0,22,42]:
        svg.add(path(f"M540,1042 C{540+dx},994 {520+dx},954 {500+dx},914", stroke="#508c5c", sw=5))
        svg.add(ellipse(500+dx,914,17,28,"#dd8bdb",stroke="#6b5d64",sw=3))


def scene_still():
    svg=SVG()
    background(svg)
    svg.add(seated_interviewer(318,970,.90,"speaking",prop=True))
    svg.add(seated_respondent(768,990,.86,"eager",gesture="lap"))
    svg.add(text(54,70,"DesignV3 original scene still", "label"))
    svg.add(text(54,104,"Seated, connected bodies; reference imagery intentionally excluded", "tiny"))
    svg.save(SRC/"scene_still.svg")


def model_sheet(character):
    svg=SVG(bg="#f1eadb")
    svg.add(text(50,70, f"{character.title()} Model Sheet - Original DesignV3", "label"))
    svg.add(text(50,104, "Large readable drawings, connected seated anatomy, replacement expression targets", "tiny"))
    # large seated pose
    svg.add('<rect x="48" y="135" width="470" height="690" fill="#e6ded0" stroke="#c7bdaf" stroke-width="3"/>')
    svg.add(text(70,178,"seated three-quarter", "note"))
    if character=="interviewer":
        svg.add(seated_interviewer(290,370,.66,"skeptical",prop=True))
        face_func=interviewer_face
    else:
        svg.add(seated_respondent(290,365,.62,"eager",gesture="yes"))
        face_func=respondent_face
    # head views
    svg.add('<rect x="555" y="135" width="475" height="340" fill="#e6ded0" stroke="#c7bdaf" stroke-width="3"/>')
    svg.add(text(580,170,"front / profile heads", "note"))
    svg.add(face_func(690,320,"neutral",.70,view="three"))
    svg.add(face_func(900,320,"neutral",.70,view="profile"))
    # hand prop
    svg.add('<rect x="555" y="500" width="475" height="325" fill="#e6ded0" stroke="#c7bdaf" stroke-width="3"/>')
    svg.add(text(580,543,"prop hand / gesture", "note"))
    if character=="interviewer":
        svg.add(path("M660,660 C735,630 796,625 870,648", stroke="#201713", sw=12))
        svg.add(hand(870,648,8,scale=1.1)); svg.add(mic(965,638,0,1.1))
    else:
        svg.add(path("M650,664 C724,608 812,580 905,590", stroke="#201713", sw=12))
        svg.add(hand(905,590,-28,scale=1.15))
        svg.add(text(615,738,"open confident interruption hand", "tiny"))
    # expressions grid
    moods=["neutral","speaking","skeptical" if character=="interviewer" else "eager","annoyed","smug","shock"]
    labels=["neutral","speaking","skeptical" if character=="interviewer" else "eager","annoyed","smug","custom extreme"]
    x0,y0=70,905
    for i,(m,lbl) in enumerate(zip(moods,labels)):
        col=i%3; row=i//3
        x=x0+col*320; y=y0+row*420
        svg.add(f'<rect x="{x-25}" y="{y-55}" width="280" height="350" fill="#e6ded0" stroke="#c7bdaf" stroke-width="3"/>')
        svg.add(text(x-8,y-18,lbl,"tiny"))
        svg.add(face_func(x+115,y+145,m,.82))
    svg.save(SRC/f"{character}_model_sheet.svg")


def storyboard():
    panels=[
        ("storyboard_01_opening_question.svg","Opening question", "Picture: 0.00-2.44s | Audio question begins at 0.00s", "question"),
        ("storyboard_02_instant_yes.svg","Instant Yes response", "Audio Yes within 0.00-2.72s transcript segment; accent near 2.56s", "yes"),
        ("storyboard_03_held_reaction.svg","Interviewer's held reaction", "Picture cut/hold around source f62 / 2.48s; not a dialogue boundary", "reaction"),
    ]
    for file,title,sub,kind in panels:
        svg=SVG()
        background(svg)
        if kind=="question":
            svg.add(seated_interviewer(315,970,.92,"speaking",prop=True))
            svg.add(seated_respondent(770,992,.88,"eager",gesture="lap"))
        elif kind=="yes":
            svg.add(seated_interviewer(285,976,.90,"shock",prop=True))
            svg.add(seated_respondent(735,950,1.00,"yes",gesture="yes"))
            svg.add(path("M632,570 C675,548 705,536 740,520", stroke="#201713", sw=5, extra='opacity=".55"'))
        else:
            # interviewer-dominant held reaction, respondent out of shot.
            svg.add(seated_interviewer(490,965,1.08,"skeptical",prop=False))
            svg.add('<rect x="805" y="580" width="155" height="95" rx="36" fill="#efe7dd" stroke="#201713" stroke-width="8" opacity=".9"/>')
            svg.add(text(822,638,"offscreen grin","tiny"))
        svg.add(text(54,70,title,"label"))
        svg.add(text(54,106,sub,"tiny"))
        svg.save(SRC/file)


def comparison_sheet():
    svg=SVG(w=1600,h=1200,bg="#f1eadb")
    svg.add(text(40,60,"Internal Reference Comparison - reference versus original artwork","label"))
    refs=[("Reference: Bro f62 / 2.48s", REF/"ref_2p48_yes_cut.png"), ("Reference: Bro f123 / 4.92s", REF/"ref_4p92_object.png")]
    for i,(label,p) in enumerate(refs):
        x=40+i*390
        svg.add(text(x,110,label,"tiny"))
        svg.add(f'<image href="{p.as_uri()}" x="{x}" y="135" width="340" height="602" preserveAspectRatio="xMidYMid meet"/>')
    svg.add(text(840,110,"Original: DesignV3 seated characters","tiny"))
    svg.add('<rect x="840" y="135" width="700" height="940" fill="#d2d0cc"/>')
    svg.add('<rect x="840" y="740" width="700" height="335" fill="#727775"/>')
    svg.add(seated_interviewer(1030,640,.68,"skeptical",prop=True))
    svg.add(seated_respondent(1345,650,.65,"eager",gesture="yes"))
    svg.add(text(840,1130,"Reference images are only in comparison material, not in original scene deliverables.","tiny"))
    svg.save(COMP/"reference_vs_original_comparison.svg")


def render_svg(svg_path, out_path, width, height):
    url = svg_path.resolve().as_uri()
    cmd = [
        str(EDGE),
        "--headless=new",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={out_path}",
        url,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def wait_stable(path, timeout=10):
    deadline = time.time() + timeout
    last = -1
    stable = 0
    while time.time() < deadline:
        if path.exists():
            size = path.stat().st_size
            if size == last and size > 0:
                stable += 1
                if stable >= 2:
                    return True
            else:
                stable = 0
                last = size
        time.sleep(.25)
    return False


if __name__ == "__main__":
    SRC.mkdir(parents=True, exist_ok=True)
    EXP.mkdir(parents=True, exist_ok=True)
    COMP.mkdir(parents=True, exist_ok=True)
    scene_still()
    model_sheet("interviewer")
    model_sheet("respondent")
    storyboard()
    comparison_sheet()
    render_jobs = [
        (SRC/"scene_still.svg", EXP/"scene_still.png", W, H),
        (SRC/"interviewer_model_sheet.svg", EXP/"interviewer_model_sheet.png", W, H),
        (SRC/"respondent_model_sheet.svg", EXP/"respondent_model_sheet.png", W, H),
        (SRC/"storyboard_01_opening_question.svg", EXP/"storyboard_01_opening_question.png", W, H),
        (SRC/"storyboard_02_instant_yes.svg", EXP/"storyboard_02_instant_yes.png", W, H),
        (SRC/"storyboard_03_held_reaction.svg", EXP/"storyboard_03_held_reaction.png", W, H),
        (COMP/"reference_vs_original_comparison.svg", COMP/"reference_vs_original_comparison.png", 1600, 1200),
    ]
    for src, out, w, h in render_jobs:
        render_svg(src, out, w, h)
        if not wait_stable(out):
            raise RuntimeError(f"output did not stabilize: {out}")
        print(out)
