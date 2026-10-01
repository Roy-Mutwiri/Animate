"""HonestInterview v5 artwork: room, chair, stick-figure characters, face libraries.

Units: 'src' units = pixels of the 480x850 reference frame.  Production is
1080x1920, so at camera zoom 1 one src unit = S = 2.25 production px.
Library symbols are drawn in production px around their registration point.
World coordinates (src units): y down; the nightstand occupies x 0..147 and the
characters sit either side of it (cap/respondent left, no-cap/interviewer right).
"""
import math
from xfl import Path, Shape

S = 2.25
INK = '#000000'
LIMB_W = 6.4      # src px: limbs/torso ~6% of head diameter
HEAD_W = 4.4      # src px: head outline ~4% of head diameter
PAL = dict(
    wall='#CCCCCC', wall_light='#D6D4D6', floor_light='#838485', floor_dark='#5A5E60', grout='#4B4E50',
    win_glass='#FCFCFC', win_frame='#524E50',
    head='#CECECE', cap='#000000', button='#F8EB63',
    chair_pink='#ECD7D7', chair_pink_shade='#D9C3C4', chair_mauve='#6F6363', chair_dark='#504542',
    chair_line='#2B2424', seat_red='#8C595A', seat_red_dark='#685758',
    ns_body='#524E4B', ns_drawer='#444441', ns_line='#2A2826', knob='#B3AA9F',
    pot='#A8765A', pot_dark='#8A5E46', soil='#4A3A2E', leaf='#86DB7A', leaf_dark='#4FA24A',
    petal='#F08DFD', petal_dark='#C95CD6', flower_mid='#FFF07A',
    lens='#C3D6D9', lens_low='#8FA3A6', lens_rim='#1A1A1A', mouth_in='#050505', tongue='#8E3B52', teeth='#FFFFFF',
)

# ----------------------------------------------------------------- helpers

def P(x, y):
    """src units -> production px (for symbol-local drawing)."""
    return (x * S, y * S)


def PP(pts):
    return [P(x, y) for x, y in pts]


def rot(v, deg):
    r = math.radians(deg)
    return (v[0] * math.cos(r) - v[1] * math.sin(r), v[0] * math.sin(r) + v[1] * math.cos(r))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def rrect(x0, y0, x1, y1, r):
    """Rounded rectangle path in production px (inputs already in px)."""
    r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
    p = Path().move(x0 + r, y0)
    p.line(x1 - r, y0).quad(x1, y0, x1, y0 + r)
    p.line(x1, y1 - r).quad(x1, y1, x1 - r, y1)
    p.line(x0 + r, y1).quad(x0, y1, x0, y1 - r)
    p.line(x0, y0 + r).quad(x0, y0, x0 + r, y0)
    return p


def blob(pts, rad=6):
    """Closed polygon (px) with rounded corners (quadratic at each corner)."""
    n = len(pts)
    p = Path()
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        la = math.hypot(b[0] - a[0], b[1] - a[1]); lc = math.hypot(c[0] - b[0], c[1] - b[1])
        ra = min(rad, la / 2) / max(la, 1e-6); rc = min(rad, lc / 2) / max(lc, 1e-6)
        p0 = (b[0] + (a[0] - b[0]) * ra, b[1] + (a[1] - b[1]) * ra)
        p1 = (b[0] + (c[0] - b[0]) * rc, b[1] + (c[1] - b[1]) * rc)
        if i == 0:
            p.move(*p0)
        else:
            p.line(*p0)
        p.quad(b[0], b[1], p1[0], p1[1])
    p.line(*p.start)
    return p


def filled(path, fill, stroke=None, w=0, alpha=1.0):
    s = Shape()
    s.add(path, fill=fill, stroke=stroke, weight=w, falpha=alpha)
    return s


# ----------------------------------------------------------------- room

def _proj(gx, gz, vpx, hy, fh):
    return (vpx + fh * gx / gz, hy + fh / gz)


def room_shapes():
    """Background in WORLD src coords * S (registration = world origin).

    Returns a list of Shapes back-to-front.  Covers world x -520..680, y -60..1180.
    """
    X0, X1, Y0, Y1 = -620, 780, -320, 1260
    FLOOR_Y = 516
    shapes = []
    shapes.append(filled(Path().poly(PP([(X0, Y0), (X1, Y0), (X1, FLOOR_Y), (X0, FLOOR_Y)]), close=True), PAL['wall']))
    # soft vertical light falling from the window onto the wall
    for (a, b, al) in [(-60, 240, 0.35), (-20, 200, 0.35)]:
        shapes.append(filled(Path().poly(PP([(a, 280), (b, 280), (b + 40, FLOOR_Y), (a - 40, FLOOR_Y)]), close=True), PAL['wall_light'], alpha=al))
    # skirting shadow line
    shapes.append(filled(Path().poly(PP([(X0, FLOOR_Y - 3), (X1, FLOOR_Y - 3), (X1, FLOOR_Y), (X0, FLOOR_Y)]), close=True), '#9C9C9C'))
    # floor: base + perspective checker (grid rotated in ground plane -> two VPs)
    shapes.append(filled(Path().poly(PP([(X0, FLOOR_Y), (X1, FLOOR_Y), (X1, Y1), (X0, Y1)]), close=True), PAL['floor_light']))
    # 1-point perspective checker (reference: rows ~40px tall at the horizon, ~70px at frame
    # bottom -> weak perspective, vanishing point far above, centred behind the characters)
    vpx, hy = 73.5, 20.0
    K = FLOOR_Y - hy                      # ground depth gz=1 at the wall line
    tx_, tz_ = 0.16, 0.072                # tile size (ground units) -> ~79x34 src px at the wall
    dark = Shape()
    grout = Shape()
    def pr(gx, gz):
        return (vpx + K * gx / gz, hy + K / gz)
    j_max = 0
    rows = []
    gz = 1.0
    while True:
        gz2 = gz - tz_ * gz * gz * 0 - tz_       # constant ground step
        if gz2 <= 0.2:
            break
        rows.append((gz, gz2))
        if hy + K / gz2 > Y1 + 40:
            break
        gz = gz2
    for r, (za, zb) in enumerate(rows):
        for c in range(-60, 61):
            if (r + c) % 2:
                continue
            xa, xb = c * tx_, (c + 1) * tx_
            pts = [pr(xa, za), pr(xb, za), pr(xb, zb), pr(xa, zb)]
            if max(p[0] for p in pts) < X0 - 20 or min(p[0] for p in pts) > X1 + 20:
                continue
            dark.add(Path().poly(PP(pts), close=True), fill=PAL['floor_dark'])
    shapes.append(dark)
    zb = rows[-1][1]
    for c in range(-60, 62):
        a_, b_ = pr(c * tx_, 1.0), pr(c * tx_, zb)
        if max(a_[0], b_[0]) < X0 - 20 or min(a_[0], b_[0]) > X1 + 20:
            continue
        grout.add(Path().poly(PP([a_, b_])), stroke=PAL['grout'], weight=1.4)
    for (za, _) in rows:
        y = hy + K / za
        grout.add(Path().poly(PP([(X0, y), (X1, y)])), stroke=PAL['grout'], weight=1.4)
    shapes.append(grout)
    # window (world x -35..215), header bar and sill
    # glass and each bar are SEPARATE drawing objects: overlapping same-fill paths inside one
    # drawing object cancel (even-odd), which erased the whole window in v5c
    wx0, wx1, wy1 = -35, 215, 276
    shapes.append(filled(Path().poly(PP([(wx0, 6), (wx1, 6), (wx1, wy1), (wx0, wy1)]), close=True), PAL['win_glass']))
    for (a_, b_, c_, d_) in [(wx0 - 1, 2, wx0 + 8, wy1 + 1), (wx1 - 8, 2, wx1 + 1, wy1 + 1), (83, 2, 92, wy1),
                             (wx0 + 4, 144, wx1 - 4, 146.5), (wx0 - 1, wy1 - 5, wx1 + 1, wy1 + 1), (wx0 - 14, -10, wx1 + 14, 8)]:
        shapes.append(filled(Path().poly(PP([(a_, b_), (c_, b_), (c_, d_), (a_, d_)]), close=True), PAL['win_frame']))
    return shapes


def _clip_ground(poly, zmin):
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        ina, inb = a[1] >= zmin, b[1] >= zmin
        if ina:
            out.append(a)
        if ina != inb:
            t = (zmin - a[1]) / (b[1] - a[1])
            out.append((a[0] + (b[0] - a[0]) * t, zmin))
    return out


def nightstand_shapes():
    """Nightstand + potted orchid.  Registration = world origin (x 0..147)."""
    sh = []
    sh.append(filled(Path().ellipse(*P(74, 628), 92 * S, 11 * S), '#2E2E2E', alpha=0.35))
    body = Shape()
    body.add(blob(PP([(2, 510), (145, 510), (145, 624), (2, 624)]), 3), fill=PAL['ns_body'], stroke=PAL['ns_line'], weight=2.2)
    body.add(blob(PP([(-3, 503), (150, 503), (150, 513), (-3, 513)]), 3), fill='#5C5754', stroke=PAL['ns_line'], weight=2.2)
    sh.append(body)
    dr = Shape()
    for (y0, y1) in [(522, 556), (566, 600)]:
        dr.add(blob(PP([(15, y0), (132, y0), (132, y1), (15, y1)]), 3), fill=PAL['ns_drawer'], stroke=PAL['ns_line'], weight=2.2)
    sh.append(dr)
    kn = Shape()
    for y in (539, 583):
        kn.add(Path().ellipse(*P(74, y), 3.2 * S, 3.2 * S), fill=PAL['knob'], stroke=PAL['ns_line'], weight=1.5)
    sh.append(kn)
    # pot
    pot = Shape()
    pot.add(blob(PP([(52, 462), (98, 462), (88, 503), (62, 503)]), 2), fill=PAL['pot'], stroke='#3B2A20', weight=2.2)
    pot.add(Path().poly(PP([(80, 466), (94, 466), (86, 500), (78, 500)]), close=True), fill=PAL['pot_dark'], falpha=0.6)
    pot.add(Path().ellipse(*P(75, 463), 23 * S, 3 * S), fill=PAL['soil'], stroke='#3B2A20', weight=1.6)
    sh.append(pot)
    # stems + leaves
    st = Shape()
    for pts in [[(75, 462), (72, 430), (68, 395), (60, 365)], [(75, 462), (80, 425), (88, 392), (95, 360)],
                [(74, 462), (76, 420), (75, 380), (78, 345)], [(75, 440), (58, 420), (47, 400)], [(76, 430), (96, 410), (104, 392)]]:
        st.add(Path().smooth(PP(pts)), stroke='#3E7A34', weight=2.0)
    sh.append(st)
    lv = Shape()
    for (cx, cy, rx, ry, a) in [(62, 450, 14, 5, 30), (90, 447, 14, 5, -30), (57, 432, 12, 4.5, 50), (94, 430, 12, 4.5, -45),
                                (66, 414, 10, 4, 60), (86, 412, 10, 4, -60), (72, 440, 9, 4, 80)]:
        lv.add(Path().ellipse(*P(cx, cy), rx * S, ry * S, math.radians(a)), fill=PAL['leaf'], stroke='#2F6B2A', weight=1.6)
    sh.append(lv)
    fl = Shape()
    for (cx, cy, r) in [(60, 362, 8), (95, 357, 8), (78, 343, 9), (47, 398, 7), (104, 390, 7), (84, 375, 7), (66, 381, 6.5)]:
        for k in range(5):
            a = 2 * math.pi * k / 5 - math.pi / 2
            px, py = cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55
            fl.add(Path().ellipse(*P(px, py), r * 0.5 * S, r * 0.42 * S, a), fill=PAL['petal'], stroke=PAL['petal_dark'], weight=1.2)
        fl.add(Path().ellipse(*P(cx, cy), r * 0.2 * S, r * 0.2 * S), fill=PAL['flower_mid'])
    # the tall bud at the top
    fl.add(blob(PP([(73, 336), (79, 322), (86, 336), (80, 344)]), 3), fill=PAL['petal'], stroke=PAL['petal_dark'], weight=1.4)
    sh.append(fl)
    return sh


# ----------------------------------------------------------------- chair

def chair_shapes():
    """Armchair seen front-left, facing screen-right.  Registration = sitter's hip.

    Drawn for the cap character; the no-cap chair is the same symbol mirrored.
    """
    L = PAL['chair_line']; w = 2.4
    sh = []
    sh.append(filled(Path().ellipse(*P(-18, 110), 125 * S, 13 * S), '#262626', alpha=0.35))
    # chair back (pillowy top) with mauve left edge
    back = Shape()
    back.add(blob(PP([(-131, -128), (-110, -142), (-60, -147), (-30, -140), (-20, -128), (-20, -60), (-131, -60)]), 10),
             fill=PAL['chair_pink'], stroke=L, weight=w)
    back.add(blob(PP([(-133, -128), (-119, -138), (-116, -60), (-131, -60)]), 5), fill=PAL['chair_mauve'], stroke=L, weight=w)
    sh.append(back)
    # far armrest: inner pink face + top rim + front face
    far = Shape()
    far.add(blob(PP([(-22, -74), (78, -76), (86, -70), (86, 36), (-22, 36)]), 6), fill=PAL['chair_pink'], stroke=L, weight=w)
    far.add(blob(PP([(-22, -76), (80, -78), (88, -71), (84, -64), (-22, -63)]), 5), fill=PAL['chair_pink_shade'], stroke=L, weight=w)
    far.add(blob(PP([(70, -70), (86, -70), (86, 34), (70, 34)]), 5), fill=PAL['chair_pink_shade'], stroke=L, weight=w)
    sh.append(far)
    # seat cushion (top + front face) with the worn red seat patch
    seat = Shape()
    seat.add(blob(PP([(-22, -6), (74, -8), (86, 4), (86, 34), (-22, 36)]), 6), fill=PAL['chair_pink'], stroke=L, weight=w)
    seat.add(blob(PP([(-22, 12), (86, 10), (86, 36), (-22, 38)]), 5), fill=PAL['chair_pink_shade'], stroke=L, weight=w)
    seat.add(Path().poly(PP([(-8, -3), (58, -5), (62, 6), (-4, 8)]), close=True), fill=PAL['seat_red'], stroke=PAL['seat_red_dark'], weight=1.4)
    sh.append(seat)
    # base
    base = Shape()
    base.add(blob(PP([(-132, 22), (-24, 30), (-24, 112), (-128, 104)]), 6), fill=PAL['chair_dark'], stroke=L, weight=w)
    base.add(blob(PP([(-24, 30), (86, 26), (86, 104), (-24, 112)]), 6), fill=PAL['chair_mauve'], stroke=L, weight=w)
    sh.append(base)
    # near armrest block (outer side, mauve) with pink rim on top and front
    near = Shape()
    near.add(blob(PP([(-134, -70), (-40, -78), (-24, -72), (-24, 38), (-132, 30)]), 8), fill=PAL['chair_mauve'], stroke=L, weight=w)
    near.add(blob(PP([(-134, -72), (-40, -80), (-22, -74), (-30, -66), (-132, -60)]), 5), fill=PAL['chair_pink'], stroke=L, weight=w)
    near.add(blob(PP([(-34, -70), (-22, -74), (-20, 38), (-32, 38)]), 4), fill=PAL['chair_pink'], stroke=L, weight=w)
    sh.append(near)
    return sh


