"""HonestInterview v5 characters: stick-figure bodies, heads, eyes, brows, glasses, mouths.

Character-local frame (src units): x = facing direction, y down, origin = hip on the seat top.
Measured from the reference (ReviewV5/analysis/ref_shots_00_36.md): head centre ~1.75 head
diameters above the seat, torso = one line from chin to seat, arms leave just below the chin,
forearms rest along the armrest tops with no hand drawn, thighs run forward over the seat to the
cushion front, shins drop almost vertically, feet are short forward strokes.
Library symbols are drawn facing +x in production px; the glasses character uses the same
drawings mirrored by the instance matrix.
"""
import math
from xfl import Path, Shape, Stack
from art import S, INK, PAL, LIMB_W, HEAD_W, P, PP, rot, add, lerp, blob, filled

HEAD_R = 53.0
HEAD_C = (-15.0, -184.0)                           # rest head centre (leans back, as in the reference)
NEAR_REST = [(-58.0, -72.0), (-28.0, -73.0)]       # elbow, wrist on the near (camera-side) armrest
FAR_REST = [(16.0, -70.0), (70.0, -72.0)]          # elbow, wrist along the far armrest top
UPPER, FORE = 60.0, 56.0


def ik2(shoulder, target, l1, l2, bend):
    """2-bone IK.  bend=+1/-1 chooses the elbow side.  Returns elbow, wrist."""
    dx, dy = target[0] - shoulder[0], target[1] - shoulder[1]
    d = math.hypot(dx, dy)
    d = max(min(d, l1 + l2 - 0.5), abs(l1 - l2) + 0.5)
    a = math.atan2(dy, dx)
    cosb = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    b = math.acos(max(-1, min(1, cosb)))
    ea = a + bend * b
    return ((shoulder[0] + l1 * math.cos(ea), shoulder[1] + l1 * math.sin(ea)),
            (shoulder[0] + d * math.cos(a), shoulder[1] + d * math.sin(a)))


class Pose:
    """A held body drawing.

    arm spec:
      ('rest',)                               forearm on its armrest, no hand drawn
      ('pts', elbow, wrist, hand, hand_deg)   explicit joints (local src)
      ('ik', wrist, bend, hand, hand_deg)     IK from the shoulder
    hand kinds: '', 'point', 'finger_up', 'hook', 'palm_up', 'open', 'fist'
    """

    def __init__(self, lean=0.0, head=(0.0, 0.0), tilt=0.0, near=('rest',), far=('rest',), legs='sit'):
        self.lean, self.head, self.tilt = lean, head, tilt
        self.near, self.far, self.legs = near, far, legs

    def copy(self, **kw):
        p = Pose(self.lean, self.head, self.tilt, self.near, self.far, self.legs)
        for k, v in kw.items():
            setattr(p, k, v)
        return p

    def key(self):
        return repr(_r((self.lean, self.head, self.tilt, self.near, self.far, self.legs)))


def _r(v):
    if isinstance(v, (list, tuple)):
        return tuple(_r(x) for x in v)
    if isinstance(v, float):
        return round(v, 2)
    return v


def head_centre(pose):
    c = rot(HEAD_C, pose.lean)
    return (c[0] + pose.head[0], c[1] + pose.head[1])


LEGS = {
    # near leg first: hip, knee, ankle, toe
    'sit': [[(0, 1), (58, 7), (72, 116), (102, 123)], [(5, -1), (82, 2), (98, 104), (126, 107)]],
    'sit_back': [[(0, 1), (58, 7), (62, 117), (92, 124)], [(5, -1), (82, 2), (90, 106), (118, 110)]],
    'sit_wide': [[(0, 1), (55, 10), (58, 118), (86, 128)], [(5, -1), (84, 0), (108, 102), (134, 104)]],
}


def body_geometry(pose):
    hc = head_centre(pose)
    hip = (0.0, 0.0)
    d = (hip[0] - hc[0], hip[1] - hc[1]); L = math.hypot(*d)
    chin = (hc[0] + d[0] / L * (HEAD_R - 2), hc[1] + d[1] / L * (HEAD_R - 2))
    shoulder = lerp(chin, hip, 0.07)
    g = dict(hip=hip, head_c=hc, chin=chin, shoulder=shoulder)
    for side, spec in (('near', pose.near), ('far', pose.far)):
        if spec[0] == 'rest':
            el, wr = (NEAR_REST if side == 'near' else FAR_REST)
            hand, hdeg = '', None
        elif spec[0] == 'pts':
            _, el, wr, hand, hdeg = spec
        else:
            _, target, bend, hand, hdeg = spec
            el, wr = ik2(shoulder, target, UPPER, FORE, bend)
        if hdeg is None:
            hdeg = math.degrees(math.atan2(wr[1] - el[1], wr[0] - el[0]))
        g[side] = (el, wr, hand, hdeg)
    g['legs'] = LEGS[pose.legs]
    return g


def hand_parts(kind, wrist, deg):
    """Black mitten hands, drawn only while gesturing.  Returns (ellipses, polylines)."""
    flip = -1.0 if math.cos(math.radians(deg)) < -0.01 else 1.0   # keep thumbs/fingers "up" when the hand points backward
    def R(x, y):
        return add(wrist, rot((x, y * flip), deg))
    blobs, lines = [], []
    if kind == 'point':
        blobs.append((R(4.5, 1.5), 6.0, 4.6, deg))
        lines.append([R(6, -1.5), R(17, -2.5)])
        lines.append([R(5, -3.5), R(8, -6.5)])
    elif kind == 'finger_up':
        fist = R(3.5, 1.0)
        blobs.append((fist, 5.2, 5.0, deg))
        lines.append([add(fist, (1.5, -3.0)), add(fist, (2.5, -17.0))])
    elif kind == 'hook':
        blobs.append((R(4, 2.5), 5.0, 4.0, deg + 40))
        lines.append([R(6, 3), R(9, 9)])
    elif kind == 'palm_up':
        lines.append([wrist, R(6, 3), R(12, 1), R(15, -4)])
        lines.append([R(8, 3.5), R(12, -1)])
    elif kind == 'open':
        blobs.append((R(4, 0), 5.0, 4.4, deg))
        for a in (-35, -12, 10, 32):
            lines.append([R(6, 0), add(R(6, 0), rot((8, 0), deg + a))])
    elif kind == 'fist':
        blobs.append((R(4, 0), 5.5, 5.0, deg))
    elif kind == 'stop':      # flat "hold on" palm: a single up-turned stroke at the wrist
        lines.append([R(-1, 0), R(3, -2), R(6, -11)])
    elif kind in ('five', 'five_b'):   # solid palm with five splayed rounded fingers (ref 59.56)
        wig = 6 if kind == 'five_b' else 0
        blobs.append((R(6, 0), 8.0, 7.0, deg))
        for a in (-70, -38, -10, 18, 48):
            base = R(9, 0)
            lines.append([base, add(base, rot((14.0 if a not in (-70, 48) else 10.0, 0), deg + a + wig))])
    return blobs, lines


def body_parts(pose):
    """Primitives for one body drawing: ('line', pts, width_factor, group) or
    ('blob', (centre, rx, ry, deg), 1, group); group is 'far', 'body' or 'near'."""
    g = body_geometry(pose)
    out = [('line', [g['hip'], g['chin']], 1.0, 'body')]
    for leg in g['legs']:
        out.append(('line', leg, 1.0, 'body'))
    for side in ('far', 'near'):
        el, wr, hand, hdeg = g[side]
        out.append(('line', [g['shoulder'], el, wr], 1.0, side))
        blobs, lines = hand_parts(hand, wr, hdeg)
        for b in blobs:
            out.append(('blob', b, 1.0, side))
        for l in lines:
            out.append(('line', l, 0.72, side))
    return g, out


# ----------------------------------------------------------------- heads

def head_cap_shapes():
    r = HEAD_R * S
    sh = [filled(Path().ellipse(0, 0, r, r, segs=12), PAL['head'], INK, HEAD_W * S)]
    cap = Shape()
    # dome sitting ON the skull: bulges ~8 above the head top, front edge at the eye tops
    cap.add(Path().smooth(PP([(-52, -20), (-50, -38), (-36, -56), (-12, -63), (14, -62), (36, -52), (49, -38),
                              (53, -27), (40, -30), (10, -29), (-20, -26), (-44, -21)]), close=True),
            fill=PAL['cap'], stroke=PAL['cap'], weight=1.5)
    # bill projecting toward the back of the head (cap worn backwards), ~0.55 head diameter
    cap.add(Path().smooth(PP([(-38, -30), (-60, -31), (-80, -27), (-87, -21), (-80, -16), (-60, -15), (-40, -17)]), close=True),
            fill=PAL['cap'], stroke=PAL['cap'], weight=1.5)
    sh.append(cap)
    fringe = Shape()   # a few hair strands poking out under the front edge
    for (a, b) in [((34, -30), (38, -24)), ((40, -30), (45, -25)), ((46, -29), (50, -24))]:
        fringe.add(Path().poly(PP([a, b])), stroke=INK, weight=1.2 * S)
    sh.append(fringe)
    sh.append(filled(Path().ellipse(*P(20, -44), 3.0 * S, 4.2 * S, math.radians(15)), PAL['button']))
    return sh


def head_glasses_shapes():
    r = HEAD_R * S
    sh = [filled(Path().ellipse(0, 0, r, r, segs=12), PAL['head'], INK, HEAD_W * S)]
    curl = Shape()
    curl.add(Path().move(*P(-14, -52)).quad(*P(-12, -64), *P(-4, -60)).quad(*P(0, -56), *P(-5, -55)), stroke=INK, weight=1.8 * S)
    curl.add(Path().move(*P(-24, -48)).quad(*P(-26, -58), *P(-18, -58)), stroke=INK, weight=1.6 * S)
    sh.append(curl)
    return sh


# ----------------------------------------------------------------- eyes
EYES = ['open', 'wide', 'half', 'half_low', 'closed', 'happy', 'blink', 'look_up', 'squint']


def cap_eye_shape(kind):
    """Solid black vertical oval eye (12x22 px in the reference).  Registration = eye centre."""
    s = Shape()
    rx, ry = 5.8, 10.8
    if kind in ('open', 'look_up'):
        dy = -1.5 if kind == 'look_up' else 0
        s.add(Path().ellipse(0, dy * S, rx * S, ry * S), fill=INK)
    elif kind == 'wide':
        s.add(Path().ellipse(0, -1.5 * S, 6.8 * S, 12.5 * S), fill=INK)
    elif kind in ('half', 'half_low', 'squint'):
        lid = {'half': -1.0, 'half_low': 2.5, 'squint': 3.5}[kind]
        bot = ry if kind != 'squint' else 7.0
        pts = [(-rx - 1.2, lid)]
        for k in range(12, -1, -1):
            a = math.pi * k / 12
            pts.append((rx * math.cos(a), max(lid, bot * math.sin(a))))
        pts.append((rx + 1.2, lid))
        s.add(Path().poly(PP(pts), close=True), fill=INK)
        s.add(Path().poly(PP([(-rx - 2.5, lid), (rx + 2.5, lid)])), stroke=INK, weight=2.6 * S)
    elif kind == 'closed':
        s.add(Path().move(*P(-7, -1)).quad(*P(0, 5), *P(7, -1)), stroke=INK, weight=2.8 * S)
    elif kind == 'happy':
        s.add(Path().move(*P(-7, 3)).quad(*P(0, -5), *P(7, 3)), stroke=INK, weight=2.8 * S)
    elif kind == 'blink':
        s.add(Path().poly(PP([(-7, 1), (7, 1)])), stroke=INK, weight=2.8 * S)
    return s


LENS_R = 12.0


def glasses_eye_shape(kind):
    """Pupil and lids inside a spectacle lens.  Registration = lens centre.  Lens tint and rims
    come from the Glasses symbol drawn above this layer."""
    s = Shape()
    R = LENS_R - 0.6
    pr = 4.6
    lid_cover = None
    if kind in ('open', 'wide', 'look_up'):
        dy = {'open': 0.5, 'wide': 0.0, 'look_up': -3.0}[kind]
        rr = pr * (1.3 if kind == 'wide' else 1.0)
        s.add(Path().ellipse(*P(1.5, dy), rr * S, rr * 1.15 * S), fill=INK)
    elif kind in ('half', 'half_low', 'squint'):
        lid = {'half': -0.5, 'half_low': 2.0, 'squint': 2.5}[kind]
        s.add(Path().ellipse(*P(1.5, lid + 3.2), pr * S, (pr * 0.8) * S), fill=INK)
        lid_cover = lid
    elif kind == 'closed':
        s.add(Path().move(*P(-7, 0)).quad(*P(0, 4.5), *P(7, 0)), stroke=INK, weight=1.9 * S)
    elif kind == 'happy':
        s.add(Path().move(*P(-7, 2)).quad(*P(0, -4), *P(7, 2)), stroke=INK, weight=1.9 * S)
    elif kind == 'blink':
        s.add(Path().poly(PP([(-7, 1), (7, 1)])), stroke=INK, weight=1.9 * S)
    if lid_cover is not None:
        pts = []
        for k in range(0, 13):
            a = math.pi + math.pi * k / 12
            pts.append((R * math.cos(a), min(lid_cover, R * math.sin(a))))
        s.add(Path().poly(PP(pts), close=True), fill=PAL['head'])
        s.add(Path().poly(PP([(-R + 0.5, lid_cover), (R - 0.5, lid_cover)])), stroke=INK, weight=1.8 * S)
        if kind == 'squint':
            s.add(Path().move(*P(-6, 7)).quad(*P(0, 5), *P(6, 7)), stroke=INK, weight=1.2 * S)
    return s


# feature positions, head-local src units (facing +x)
GLASS_L = [(15.0, -10.0), (41.0, -10.0)]
CAP_EYE_L = [(14.0, -13.0), (39.0, -13.0)]
MOUTH_L = (27.0, 21.0)
CAP_BROW_L = [(12.0, -24.0), (39.0, -24.0)]
GL_BROW_L = [(14.0, -30.0), (41.0, -31.0)]


def glasses_shapes():
    sh = []
    tint = Shape()
    for (cx, cy) in GLASS_L:
        tint.add(Path().ellipse(*P(cx, cy), LENS_R * S, LENS_R * S), fill=PAL['lens'], falpha=0.55)
    sh.append(tint)
    low = Shape()
    for (cx, cy) in GLASS_L:
        low.add(Path().move(*P(cx - LENS_R * 0.95, cy + 3)).quad(*P(cx, cy + LENS_R * 1.35), *P(cx + LENS_R * 0.95, cy + 3)).line(*P(cx - LENS_R * 0.95, cy + 3)),
                fill=PAL['lens_low'], falpha=0.45)
    sh.append(low)
    rim = Shape()
    for (cx, cy) in GLASS_L:
        rim.add(Path().ellipse(*P(cx, cy), LENS_R * S, LENS_R * S), stroke=PAL['lens_rim'], weight=1.5 * S)
        rim.add(Path().move(*P(cx - 6, cy - 5)).quad(*P(cx - 3, cy - 8), *P(cx + 1, cy - 8.5)), stroke='#FFFFFF', weight=1.3 * S, salpha=0.9)
    (ax, ay), (bx, by) = GLASS_L
    rim.add(Path().move(*P(ax + LENS_R, ay - 1)).quad(*P((ax + bx) / 2, ay - 4), *P(bx - LENS_R, by - 1)), stroke=PAL['lens_rim'], weight=1.4 * S)
    rim.add(Path().poly(PP([(ax - LENS_R, ay - 1), (ax - LENS_R - 16, ay + 1)])), stroke=PAL['lens_rim'], weight=1.4 * S)
    sh.append(rim)
    return sh


# ----------------------------------------------------------------- brows
BROWS = ['cap_angry', 'cap_raise', 'cap_worry', 'gl_neutral', 'gl_angry', 'gl_raise', 'gl_worry', 'gl_sly']


def brow_shape(kind):
    """One brow drawn for the back eye (inner end at +x); the front brow is the same drawing
    mirrored by its instance matrix so both slant symmetrically about the nose."""
    s = Shape()
    if kind == 'cap_angry':
        s.add(Path().poly(PP([(-7, -3.5), (7, 3.5)])), stroke=INK, weight=2.6 * S)
    elif kind == 'cap_raise':
        s.add(Path().move(*P(-7, 2)).quad(*P(0, -3), *P(7, 1)), stroke=INK, weight=2.4 * S)
    elif kind == 'cap_worry':
        s.add(Path().poly(PP([(-7, 3), (7, -3)])), stroke=INK, weight=2.4 * S)
    elif kind == 'gl_neutral':
        s.add(Path().move(*P(-9, 2.5)).quad(*P(0, -4), *P(9, 2)), stroke=INK, weight=3.4 * S)
    elif kind == 'gl_angry':
        s.add(Path().move(*P(-9, -4)).quad(*P(1, -3), *P(9, 4.5)), stroke=INK, weight=3.6 * S)
    elif kind == 'gl_raise':
        s.add(Path().move(*P(-9, 3)).quad(*P(0, -7), *P(9, 3)), stroke=INK, weight=3.4 * S)
    elif kind == 'gl_worry':
        s.add(Path().move(*P(-9, 4)).quad(*P(-1, -3), *P(9, -4)), stroke=INK, weight=3.4 * S)
    elif kind == 'gl_sly':
        s.add(Path().move(*P(-9, -2)).quad(*P(0, -4.5), *P(9, 3)), stroke=INK, weight=3.4 * S)
    return s


# ----------------------------------------------------------------- mouths
MOUTH_FAMILIES = ['X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
EMOTIONS = ['neutral', 'angry', 'smug', 'sad']


def mouth_shape(fam, emo):
    """Mouth drawing, registration = mouth centre; width ~0.3-0.45 head diameter.
    Interior black, white top-teeth band, maroon tongue.  Emotion changes corners/outline,
    not articulation."""
    s = Stack()
    lw = 2.4 * S
    up = {'neutral': 0.0, 'angry': 0.0, 'smug': -4.0, 'sad': 0.0}[emo]
    droop = {'neutral': 1.5, 'angry': 3.5, 'smug': -1.0, 'sad': 4.0}[emo]
    if fam == 'X':
        if emo == 'smug':
            s.add(Path().move(*P(-11, -1)).quad(*P(-1, 5), *P(11, -5)), stroke=INK, weight=lw)
        elif emo == 'sad':
            s.add(Path().move(*P(-9, 3.5)).quad(*P(0, -3), *P(9, 3.5)), stroke=INK, weight=lw)
        elif emo == 'angry':
            s.add(Path().move(*P(-10, 3)).quad(*P(0, -1.5), *P(10, 3.5)), stroke=INK, weight=lw)
        else:
            s.add(Path().move(*P(-9, 1)).quad(*P(0, -0.5), *P(9, 2.5)), stroke=INK, weight=lw)
        return s
    if fam == 'A':   # pressed lips (M/B/P)
        w = 10.5
        pts = [(-w, droop * 0.5), (-w * 0.5, -1.2), (0, 0.6), (w * 0.5, -1.0), (w, droop * 0.5 + up * 0.5)]
        s.add(Path().smooth(PP(pts)), stroke=INK, weight=lw * 1.15)
        return s
    if fam == 'F':   # puckered: thick black lips around a small red centre (reference pucker)
        s.add(blob(PP([(-6, -2.5), (-3, -6), (3, -6), (6.5, -2.5 + up * 0.3), (6.5, 2.5), (3, 6), (-3, 6), (-6, 2.5)]), 2.4 * S), fill=INK)
        s.add(Path().ellipse(*P(0.3, 0.2), 2.2 * S, 2.6 * S), fill=PAL['tongue'])
        return s
    if fam == 'E':   # small O
        rx, ry = 6.0, 7.0
        s.add(Path().ellipse(*P(0, 0), rx * S, ry * S), fill=PAL['mouth_in'])
        s.add(Path().ellipse(*P(0, ry * 0.55), rx * 0.55 * S, ry * 0.3 * S), fill=PAL['tongue'])
        s.add(Path().ellipse(*P(0, 0), rx * S, ry * S), stroke=INK, weight=lw)
        return s
    hw, hh, tongue = {'B': (12.0, 3.4, False), 'C': (11.5, 6.5, True), 'D': (13.0, 10.0, True),
                      'G': (11.0, 4.5, False), 'H': (11.0, 7.5, True)}[fam]
    if emo == 'sad':
        hw *= 0.88
    if emo == 'smug':
        hw *= 1.08
    lc = (-hw, droop * 0.6)
    fc = (hw, droop * 0.6 + up)
    if emo == 'smug':
        top = [(-hw * 0.55, -hh + 0.5), (hw * 0.55, -hh + up * 0.5)]
        bot = [(hw * 0.5, hh + 1.5), (-hw * 0.5, hh + 1.0)]
    elif emo == 'angry':
        top = [(-hw * 0.8, -hh), (hw * 0.8, -hh)]
        bot = [(hw * 0.8, hh), (-hw * 0.8, hh)]
    elif emo == 'sad':
        top = [(-hw * 0.5, -hh), (hw * 0.5, -hh)]
        bot = [(hw * 0.6, hh * 0.8), (0, hh * 0.9), (-hw * 0.6, hh * 0.8)]
    else:
        top = [(-hw * 0.6, -hh), (hw * 0.6, -hh)]
        bot = [(hw * 0.6, hh), (-hw * 0.6, hh)]
    poly = [lc] + top + [fc] + bot
    outline = blob(PP(poly), 2.0 * S)
    if fam == 'B':   # clenched teeth: white band with a black centre line
        s.add(outline, fill=PAL['teeth'])
        s.add(Path().poly(PP([(-hw + 1.5, (lc[1] + fc[1]) * 0.25), (hw - 1.5, (lc[1] + fc[1]) * 0.25 + up * 0.3)])), stroke=INK, weight=1.3 * S)
        for x in (-hw * 0.45, 0.0, hw * 0.45):
            s.add(Path().poly(PP([(x, -hh + 0.6), (x, hh - 0.6)])), stroke='#555555', weight=0.8 * S)
        s.add(outline, stroke=INK, weight=lw)
        return s
    s.add(outline, fill=PAL['mouth_in'])
    if tongue:
        ty = hh * (0.5 if fam != 'H' else -0.1)
        tr = 0.42 if emo != 'smug' else 0.28
        s.add(Path().ellipse(*P(0, ty + (hh * 0.15 if emo == 'smug' else 0)), hw * 0.55 * S, hh * tr * S), fill=PAL['tongue'] if emo != 'smug' else '#B8404E')
    th = {'C': 2.8, 'D': 3.2, 'G': 4.2, 'H': 2.8}[fam]
    if emo == 'smug':
        th = min(hh * 1.1, th * 1.9)
    s.add(Path().poly(PP([(-hw * 0.72, -hh + 0.3), (hw * 0.72, -hh + 0.3 + up * 0.35), (hw * 0.7, -hh + th + up * 0.35), (-hw * 0.7, -hh + th)]), close=True), fill=PAL['teeth'])
    if fam == 'G':   # F/V: upper teeth resting on the lower lip
        for x in (-6, -2, 2, 6):
            s.add(Path().move(*P(x - 2, -hh + th)).quad(*P(x, -hh + th + 2.2), *P(x + 2, -hh + th)), stroke=INK, weight=0.8 * S)
        s.add(Path().move(*P(-hw * 0.8, hh * 0.3)).quad(*P(0, hh * 1.2), *P(hw * 0.8, hh * 0.3 + up * 0.3)), stroke=INK, weight=lw * 0.8)
    s.add(outline, stroke=INK, weight=lw)
    return s


def mouth_frame_index(fam, emo):
    return EMOTIONS.index(emo) * len(MOUTH_FAMILIES) + MOUTH_FAMILIES.index(fam)
