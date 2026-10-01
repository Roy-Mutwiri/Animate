"""Scene composition for HonestInterview v5.

World (src units, y down): nightstand x 0..147; CAP (respondent) hip at CAP_HIP facing +x;
GLASSES (interviewer) hip mirrored about the nightstand centre, facing -x.
A camera (cx, cy, zoom) maps world (cx, cy) to the frame centre; 1 world unit = S*zoom px.

Every production frame gets a FrameState; the XFL writer turns runs of identical element
lists into held keyframes, so holds stay holds in the Animate timeline.
"""
import math
import art, chars
from art import S
from xfl import Document, Layer, Shape, Path, Instance

W, H, FPS = 1080, 1920, 24
MID = 73.5
CAP_HIP = (-120.0, 543.0)
GL_HIP = (2 * MID - CAP_HIP[0], 543.0)

# camera presets measured from the reference framing
MOUTH_SC = 1.45                     # reference mouths are ~0.35 head diameter wide
CAM_TWO = (78.0, 413.0, 0.84)       # two-shot: CAP head x~66, GLASSES x~398, nightstand centred
CAM_CAP = (-112.0, 425.0, 1.0)      # CAP single: head x~220
CAM_GL = (252.0, 425.0, 1.0)        # GLASSES single: head x~267; wide enough that the off-screen CAP foot stays out of frame


class Cam:
    def __init__(self, cx, cy, z):
        self.cx, self.cy, self.z = cx, cy, z

    def pt(self, x, y):
        k = S * self.z
        return (W / 2 + (x - self.cx) * k, H / 2 + (y - self.cy) * k)

    def key(self):
        return (round(self.cx, 3), round(self.cy, 3), round(self.z, 5))


def mat(a, b, c, d, tx, ty):
    return dict(a=a, b=b, c=c, d=d, tx=tx, ty=ty)


class Inst(Instance):
    """Instance with a raw 2x2 matrix."""

    def __init__(self, name, m, first=0):
        super().__init__(name, first=first)
        self.m = m

    def xml(self):
        m = self.m
        s = '<DOMSymbolInstance libraryItemName="%s" symbolType="graphic" firstFrame="%d" loop="single frame">' % (self.name, self.first)
        s += '<matrix><Matrix a="%.6f" b="%.6f" c="%.6f" d="%.6f" tx="%.2f" ty="%.2f"/></matrix>' % (m['a'], m['b'], m['c'], m['d'], m['tx'], m['ty'])
        s += '<transformationPoint><Point/></transformationPoint></DOMSymbolInstance>'
        return s

    def sig(self):
        m = self.m
        return (self.name, self.first) + tuple(round(m[k], 4) for k in ('a', 'b', 'c', 'd')) + (round(m['tx'], 2), round(m['ty'], 2))


def world_inst(name, cam, wx, wy, mx=1.0, first=0):
    """Symbol drawn in production px at zoom 1 around world point (wx, wy)."""
    tx, ty = cam.pt(wx, wy)
    return Inst(name, mat(cam.z * mx, 0, 0, cam.z, tx, ty), first)


# ----------------------------------------------------------------- character placement

class Char:
    def __init__(self, name, hip, mx):
        self.name, self.hip, self.mx = name, hip, mx

    def to_world(self, p):
        return (self.hip[0] + self.mx * p[0], self.hip[1] + p[1])


CAP = Char('CAP', CAP_HIP, 1.0)
GL = Char('GL', GL_HIP, -1.0)


class CharState:
    """Everything needed to draw one character on one frame."""

    def __init__(self, pose, eyes='open', brows=None, mouth=('X', 'neutral'), look=0.0):
        self.pose, self.eyes, self.brows, self.mouth, self.look = pose, eyes, brows, mouth, look


def head_matrix(ch, cam, pose, sc=1.0, rot_deg=0.0, hl=(0.0, 0.0), flip=1.0):
    """Matrix for a symbol drawn head-local (facing +x) at head-local point hl."""
    hc = chars.head_centre(pose)
    t = -math.radians(pose.tilt)            # + tilt = head juts toward the listener (clockwise for a +x facer, ref 2.64s)
    # head-local -> char-local: rotate by -tilt (back tilt rotates counter-clockwise for +x facer)
    rx = hl[0] * math.cos(-t) - hl[1] * math.sin(-t)
    ry = hl[0] * math.sin(-t) + hl[1] * math.cos(-t)
    lp = (hc[0] + rx, hc[1] + ry)
    wx, wy = ch.to_world(lp)
    tx, ty = cam.pt(wx, wy)
    ang = -t + math.radians(rot_deg)
    z = cam.z * sc
    # M = diag(mx,1) * R(ang) * diag(flip,1)
    ca, sa = math.cos(ang), math.sin(ang)
    a, c = ch.mx * ca * flip, ch.mx * -sa
    b, d = sa * flip, ca
    return mat(z * a, z * b, z * c, z * d, tx, ty)


def body_shape(ch, cam, pose):
    g, parts = chars.body_parts(pose)
    s = Shape()
    k = S * cam.z
    for kind, data, wf, grp in parts:
        if kind == 'line':
            pts = [cam.pt(*ch.to_world(p)) for p in data]
            path = Path().poly(pts) if len(pts) == 2 else Path().smooth(pts) if wf < 1 else _limb_path(pts)
            s.add(path, stroke=art.INK, weight=art.LIMB_W * k * wf)
        else:
            (cx, cy), rx, ry, deg = data
            wx, wy = ch.to_world((cx, cy))
            px, py = cam.pt(wx, wy)
            dd = deg if ch.mx > 0 else 180 - deg
            s.add(Path().ellipse(px, py, rx * k, ry * k, math.radians(dd)), fill=art.INK)
    return s


def _limb_path(pts):
    """Limb through its joints with slightly rounded bends (single uniform line)."""
    p = Path().move(*pts[0])
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        la = math.hypot(b[0] - a[0], b[1] - a[1]); lc = math.hypot(c[0] - b[0], c[1] - b[1])
        r = min(la, lc) * 0.18
        p0 = (b[0] + (a[0] - b[0]) * r / max(la, 1e-6), b[1] + (a[1] - b[1]) * r / max(la, 1e-6))
        p1 = (b[0] + (c[0] - b[0]) * r / max(lc, 1e-6), b[1] + (c[1] - b[1]) * r / max(lc, 1e-6))
        p.line(*p0).quad(b[0], b[1], p1[0], p1[1])
    p.line(*pts[-1])
    return p


def char_elements(ch, cam, st):
    """Returns dict layer-suffix -> list of elements for one character state."""
    pose = st.pose
    is_cap = ch is CAP
    out = {}
    out['body'] = [body_shape(ch, cam, pose)]
    out['head'] = [Inst('HEAD/Head_Cap' if is_cap else 'HEAD/Head_Glasses', head_matrix(ch, cam, pose))]
    look = st.look                                   # shifts features toward camera (-) / away (+)
    eyes_lib = 'FACE/Eyes_Cap' if is_cap else 'FACE/Eyes_Glasses'
    epos = chars.CAP_EYE_L if is_cap else chars.GLASS_L
    ei = chars.EYES.index(st.eyes)
    out['eyes'] = [Inst(eyes_lib, head_matrix(ch, cam, pose, hl=(x + look, y)), ei) for (x, y) in epos]
    if not is_cap:
        out['glasses'] = [Inst('FACE/Glasses', head_matrix(ch, cam, pose, hl=(look, 0)))]
    br = []
    if st.brows:
        bpos = chars.CAP_BROW_L if is_cap else chars.GL_BROW_L
        bi = chars.BROWS.index(st.brows)
        br.append(Inst('FACE/Brows', head_matrix(ch, cam, pose, hl=(bpos[0][0] + look, bpos[0][1])), bi))
        br.append(Inst('FACE/Brows', head_matrix(ch, cam, pose, hl=(bpos[1][0] + look, bpos[1][1]), flip=-1.0), bi))
    out['brows'] = br
    fam, emo = st.mouth
    mlib = 'MOUTH/Mouth_Cap' if is_cap else 'MOUTH/Mouth_Glasses'
    out['mouth'] = [Inst(mlib, head_matrix(ch, cam, pose, sc=MOUTH_SC, hl=(chars.MOUTH_L[0] + look, chars.MOUTH_L[1])), chars.mouth_frame_index(fam, emo))]
    return out


# ----------------------------------------------------------------- library

def build_library(doc):
    def single(name, shapes):
        sym = doc.symbol(name)
        L = sym.timeline.layer('art')
        L.key(0, 1, shapes)
        return sym
    single('SET/Room', art.room_shapes())
    single('SET/Nightstand', art.nightstand_shapes())
    single('SET/Armchair', art.chair_shapes())
    single('HEAD/Head_Cap', chars.head_cap_shapes())
    single('HEAD/Head_Glasses', chars.head_glasses_shapes())
    single('FACE/Glasses', chars.glasses_shapes())
    for name, fn in (('FACE/Eyes_Cap', chars.cap_eye_shape), ('FACE/Eyes_Glasses', chars.glasses_eye_shape)):
        sym = doc.symbol(name)
        L = sym.timeline.layer('eye')
        for i, k in enumerate(chars.EYES):
            L.key(i, 1, [fn(k)], label=k)
    sym = doc.symbol('FACE/Brows')
    L = sym.timeline.layer('brow')
    for i, k in enumerate(chars.BROWS):
        L.key(i, 1, [chars.brow_shape(k)], label=k)
    for name in ('MOUTH/Mouth_Cap', 'MOUTH/Mouth_Glasses'):
        sym = doc.symbol(name)
        L = sym.timeline.layer('mouth')
        for emo in chars.EMOTIONS:
            for fam in chars.MOUTH_FAMILIES:
                L.key(chars.mouth_frame_index(fam, emo), 1, [chars.mouth_shape(fam, emo)], label='%s_%s' % (emo, fam))


# ----------------------------------------------------------------- frame states -> layers

LAYER_ORDER = [  # top first
    ('FX_Iris', '#000000'),
    ('GL_mouth', '#FF4040'), ('GL_glasses', '#40A0FF'), ('GL_brows', '#FF40FF'), ('GL_eyes', '#40FFFF'), ('GL_head', '#FFFF40'), ('GL_body', '#40FF40'),
    ('CAP_mouth', '#FF4040'), ('CAP_brows', '#FF40FF'), ('CAP_eyes', '#40FFFF'), ('CAP_head', '#FFFF40'), ('CAP_body', '#40FF40'),
    ('SET_Chair_GL', '#9933CC'), ('SET_Chair_CAP', '#9933CC'), ('SET_Nightstand', '#996633'), ('SET_Room', '#808080'),
]


class FrameState:
    def __init__(self, cam, cap, gl, iris=None):
        self.cam, self.cap, self.gl, self.iris = cam, cap, gl, iris


def frame_elements(fs):
    cam = fs.cam
    E = {}
    E['SET_Room'] = [world_inst('SET/Room', cam, 0, 0)]
    E['SET_Nightstand'] = [world_inst('SET/Nightstand', cam, 0, 0)]
    E['SET_Chair_CAP'] = [world_inst('SET/Armchair', cam, CAP_HIP[0], CAP_HIP[1], 1.0)]
    E['SET_Chair_GL'] = [world_inst('SET/Armchair', cam, GL_HIP[0], GL_HIP[1], -1.0)]
    for ch, st, pre in ((CAP, fs.cap, 'CAP_'), (GL, fs.gl, 'GL_')):
        # singles show one character; the other is hidden rather than left to leak in at the edge
        if ch is GL and cam.cx < -40:     # GL is never in frame on CAP singles/push-ins
            continue
        for k, v in char_elements(ch, cam, st).items():
            E[pre + k] = v
    E['FX_Iris'] = iris_elements(fs.iris) if fs.iris else []
    return E


def _keyhole(cx, cy, r, R=None, n=72):
    """Black region outside a circle (or an annulus r..R) as ONE simple polygon joined by a
    zero-width slit, so the fill is unambiguous."""
    circ = [(cx + r * math.cos(-2 * math.pi * k / n), cy + r * math.sin(-2 * math.pi * k / n)) for k in range(n + 1)]
    if R is None:
        outer = [(W + 400, cy), (W + 400, H + 400), (-400, H + 400), (-400, -400), (W + 400, -400), (W + 400, cy)]
    else:
        outer = [(cx + R * math.cos(2 * math.pi * k / n), cy + R * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]
    return Path().poly(outer + circ, close=True)


def iris_elements(iris):
    """Iris-out centred on the frame with a very soft (~86 px) dusky-purple edge (ref 69.08-70.88)."""
    cx, cy, r = iris
    out = []
    s = Shape(); s.add(_keyhole(cx, cy, r + 86), fill='#000000'); out.append(s)
    steps = 22
    for k in range(steps):
        a = r + 86.0 * k / steps
        b = r + 86.0 * (k + 1) / steps
        u = (k + 0.5) / steps
        al = 0.04 + 0.93 * u * u * (3 - 2 * u)
        f = Shape(); f.add(_keyhole(cx, cy, a, b), fill='#140A1E', falpha=min(al, 0.97)); out.append(f)
    return out


def _sig(el):
    if isinstance(el, Inst):
        return ('I',) + el.sig()
    return ('S', el.xml())


def build_document(states, out_dir, stem, label_frames=None):
    """states: list of FrameState per production frame."""
    doc = Document(W, H, FPS, '#FFFFFF')
    build_library(doc)
    sc = doc.scene('Scene 1')
    layers = {}
    for name, color in LAYER_ORDER:
        layers[name] = sc.layer(name, color=color)
    n = len(states)
    prev = {name: None for name, _ in LAYER_ORDER}
    runs = {name: [] for name, _ in LAYER_ORDER}
    for f, fs in enumerate(states):
        E = frame_elements(fs)
        for name, _ in LAYER_ORDER:
            els = E.get(name, [])
            sig = tuple(_sig(e) for e in els)
            if prev[name] is not None and prev[name][0] == sig:
                prev[name][2] += 1
            else:
                if prev[name] is not None:
                    runs[name].append(prev[name])
                prev[name] = [sig, f, 1, els]
    for name, _ in LAYER_ORDER:
        if prev[name] is not None:
            runs[name].append(prev[name])
        for sig, start, dur, els in runs[name]:
            layers[name].key(start, dur, els)
    if label_frames:
        lab = Layer('LABELS', color='#000000')
        sc.layers.insert(0, lab)
        for (start, dur, text) in label_frames:
            lab.key(start, dur, [], label=text)
    return doc.write(out_dir, stem)
