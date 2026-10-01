"""Performance engine: turns a timed acting script into per-frame FrameStates.

Timing policy (stated once, used everywhere): all script times are seconds on the ORIGINAL audio
(= reference video time, offset measured ~0).  A time t maps to the global zero-based production
frame  floor(t * 24 + 0.5).  Cue intervals are converted once from absolute seconds; durations are
never rounded and accumulated.

Acting model (from the reference study):
  * bodies HOLD for seconds; a pose change is 2-4 drawings on ones, then a hold;
  * in-betweens travel on arcs about the shoulder / elbow, with no hand drawn until arrival;
  * eyes, brows and mouth are replacement drawings switched independently of the body;
  * blinks are 1-3 frame closed-lid drawings placed on phrase ends / gesture landings, not on a timer.
"""
import json, math
import chars
from chars import Pose, body_geometry
from poses import POSES, EXPR
from scene import FrameState, CharState, Cam

FPS = 24


def F(t):
    return int(math.floor(t * FPS + 0.5))


# ----------------------------------------------------------------- mouth cues

def load_cues(path):
    d = json.load(open(path, encoding='utf-8'))
    cues = d['mouthCues']
    for a, b in zip(cues, cues[1:]):
        assert a['start'] <= a['end'] and abs(a['end'] - b['start']) < 1e-6, (a, b)
    return cues


def cue_track(cues, nframes):
    """Per-frame Rhubarb shape.  Each cue covers frames [F(start), F(end)).  A cue that collapses
    to zero frames is dropped unless it is a closure (A) or pucker (F), which then takes the frame
    it starts on (closures are what make speech read)."""
    track = ['X'] * nframes
    for c in cues:
        a, b = F(c['start']), F(c['end'])
        v = c['value']
        if b > a:
            for f in range(a, min(b, nframes)):
                track[f] = v
        elif v in ('A', 'F') and a < nframes:
            track[a] = v
    return track


# ----------------------------------------------------------------- pose interpolation

def _arm_joints(pose, side):
    g = body_geometry(pose)
    el, wr, hand, hdeg = g[side]
    return g['shoulder'], el, wr, hand, hdeg


def _polar(o, p):
    return math.atan2(p[1] - o[1], p[0] - o[0]), math.hypot(p[0] - o[0], p[1] - o[1])


def _angle_lerp(a, b, t):
    d = (b - a + math.pi) % (2 * math.pi) - math.pi
    return a + d * t


def blend(p0, p1, t, arrive=False):
    """In-between drawing: body params linear, arms on arcs (shoulder->elbow angle and
    elbow->wrist angle interpolated).  Hands only on the arrival drawing."""
    if t <= 0:
        return p0
    if t >= 1 or arrive:
        return p1
    out = Pose(lean=p0.lean + (p1.lean - p0.lean) * t,
               head=(p0.head[0] + (p1.head[0] - p0.head[0]) * t, p0.head[1] + (p1.head[1] - p0.head[1]) * t),
               tilt=p0.tilt + (p1.tilt - p0.tilt) * t,
               legs=p1.legs if t > 0.5 else p0.legs)
    for side in ('near', 'far'):
        s0, e0, w0, h0, d0 = _arm_joints(p0, side)
        s1, e1, w1, h1, d1 = _arm_joints(p1, side)
        if (e0, w0) == (e1, w1):
            spec = p1.near if side == 'near' else p1.far
        else:
            a0, r0 = _polar(s0, e0); a1, r1 = _polar(s1, e1)
            b0, q0 = _polar(e0, w0); b1, q1 = _polar(e1, w1)
            s = (s0[0] + (s1[0] - s0[0]) * t, s0[1] + (s1[1] - s0[1]) * t)
            a, r = _angle_lerp(a0, a1, t), r0 + (r1 - r0) * t
            e = (s[0] + r * math.cos(a), s[1] + r * math.sin(a))
            b, q = _angle_lerp(b0, b1, t), q0 + (q1 - q0) * t
            w = (e[0] + q * math.cos(b), e[1] + q * math.sin(b))
            # while travelling, the hand is not drawn (reference: 'no hand drawn yet')
            spec = ('pts', e, w, '', None)
        if side == 'near':
            out.near = spec
        else:
            out.far = spec
    return out


def ease_out(t, k=2.0):
    return 1 - (1 - t) ** k


# ----------------------------------------------------------------- character track

class Track:
    """One character's acting script.

    pose(t, name_or_Pose, frames=3, spacing=None, overshoot=None)
        the new pose ARRIVES at t; `frames` in-between drawings precede it (on ones).
        spacing: list of fractions for the in-betweens (default ease-out = fast start, cushion in).
    expr(t, preset) / eyes(t, kind) / brows(t, kind) / emo(t, emotion)
    blink(t, frames=2, kind='closed')
    mouth(t0, t1, fam, emo=None)  -> explicit mouth override (e.g. a held smug smile, an F/V accent)
    look(t, dx)                    -> shifts facial features (gaze/turn)
    """

    def __init__(self, who, cues=None, db=None):
        self.who = who
        self.db = db              # per-frame speaker loudness for the jaw pass (jaw.py)
        self.poses = []
        self.faces = []      # (frame, field, value)
        self.blinks = []
        self.mouths = []
        self.cues = cues

    def pose(self, t, p, frames=3, spacing=None, overshoot=None):
        P = POSES[p] if isinstance(p, str) else p
        self.poses.append((F(t), P, frames, spacing, overshoot))
        return self

    def expr(self, t, preset):
        e, b, emo = EXPR[self.who][preset]
        f = F(t)
        self.faces += [(f, 'eyes', e), (f, 'brows', b), (f, 'emo', emo)]
        return self

    def eyes(self, t, kind):
        self.faces.append((F(t), 'eyes', kind)); return self

    def brows(self, t, kind):
        self.faces.append((F(t), 'brows', kind)); return self

    def emo(self, t, emo):
        self.faces.append((F(t), 'emo', emo)); return self

    def look(self, t, dx):
        self.faces.append((F(t), 'look', dx)); return self

    def blink(self, t, frames=2, kind='closed'):
        self.blinks.append((F(t), frames, kind)); return self

    def jitter(self, t0, t1, offset=(-4.0, -1.0), pattern=(2, 1, 3, 2, 1, 2, 3, 1)):
        """Rage tremble: head/upper torso alternate between two positions irregularly (ref 60.84)."""
        self.jitters = getattr(self, 'jitters', []) + [(F(t0), F(t1), offset, pattern)]
        return self

    def mouth(self, t0, t1, fam, emo=None):
        self.mouths.append((F(t0), F(t1), fam, emo)); return self

    # --------------------------------------------------------- evaluation
    def evaluate(self, nframes):
        # body: resolve pose keys into per-frame drawings
        keys = sorted(self.poses, key=lambda k: k[0])
        body = [POSES['rest']] * nframes
        cur = POSES['rest']
        for i, (f, P, n, spacing, over) in enumerate(keys):
            nxt = keys[i + 1][0] if i + 1 < len(keys) else nframes
            start = max(0, f - n)
            prev = cur
            if spacing is None:
                spacing = [ease_out((k + 1) / (n + 1)) for k in range(n)]
            for k in range(n):
                fr = start + k
                if 0 <= fr < nframes:
                    body[fr] = blend(prev, P, spacing[k])
            for fr in range(max(f, 0), min(nxt - (keys[i + 1][2] if i + 1 < len(keys) else 0), nframes)):
                body[fr] = P
            if over:  # one overshoot drawing on arrival, then settle
                body[f] = blend(prev, P, over) if over < 1 else _extrapolate(prev, P, over)
            cur = P
        for (a, b, off, pat) in getattr(self, 'jitters', []):
            fr, k, on = a, 0, True
            while fr < min(b, nframes):
                n = pat[k % len(pat)]
                if on:
                    for q in range(fr, min(fr + n, b, nframes)):
                        p = body[q]
                        body[q] = p.copy(head=(p.head[0] + off[0], p.head[1] + off[1]))
                fr += n; k += 1; on = not on
        # face fields
        fields = {'eyes': ['open'] * nframes, 'brows': [None] * nframes, 'emo': ['neutral'] * nframes, 'look': [0.0] * nframes}
        for fld in fields:
            ev = sorted([(f, v) for (f, k, v) in self.faces if k == fld], key=lambda x: x[0])
            for j, (f, v) in enumerate(ev):
                end = ev[j + 1][0] if j + 1 < len(ev) else nframes
                for fr in range(max(0, f), min(end, nframes)):
                    fields[fld][fr] = v
        eyes = list(fields['eyes'])
        for (f, n, kind) in self.blinks:
            for fr in range(f, min(f + n, nframes)):
                eyes[fr] = kind
        # mouth
        speech = cue_track(self.cues, nframes) if self.cues else ['X'] * nframes
        if self.db is not None:
            from jaw import jaw_pass
            speech, self.jaw_changed = jaw_pass(speech, self.db)
        self.speech = speech
        mouth = [(speech[f], fields['emo'][f]) for f in range(nframes)]
        for (a, b, fam, emo) in self.mouths:
            for fr in range(a, min(b, nframes)):
                mouth[fr] = (fam, emo or fields['emo'][fr])
        return [CharState(body[f], eyes[f], fields['brows'][f], mouth[f], fields['look'][f]) for f in range(nframes)]


def _extrapolate(p0, p1, k):
    """Overshoot drawing: joints pushed past p1 by factor k (e.g. 1.12)."""
    out = p1.copy()
    for side in ('near', 'far'):
        s0, e0, w0, h0, d0 = _arm_joints(p0, side)
        s1, e1, w1, h1, d1 = _arm_joints(p1, side)
        e = (e1[0] + (e1[0] - e0[0]) * (k - 1), e1[1] + (e1[1] - e0[1]) * (k - 1))
        w = (w1[0] + (w1[0] - w0[0]) * (k - 1), w1[1] + (w1[1] - w0[1]) * (k - 1))
        spec = ('pts', e, w, h1, d1) if (e0, w0) != (e1, w1) else (p1.near if side == 'near' else p1.far)
        if side == 'near':
            out.near = spec
        else:
            out.far = spec
    out.lean = p1.lean + (p1.lean - p0.lean) * (k - 1)
    out.tilt = p1.tilt + (p1.tilt - p0.tilt) * (k - 1)
    return out


# ----------------------------------------------------------------- camera track

class CamTrack:
    """Holds a camera per frame.  cut(t, preset) hard cuts; move(t0, t1, cam) eases between; snap
    (t0, t1, cam) is a fast few-frame move (reference push-in snaps)."""

    def __init__(self):
        self.events = []

    def cut(self, t, cam):
        self.events.append(('cut', F(t), F(t), cam)); return self

    def move(self, t0, t1, cam, curve='inout'):
        self.events.append((curve, F(t0), F(t1), cam)); return self

    def evaluate(self, nframes):
        out = [None] * nframes
        cur = None
        ev = sorted(self.events, key=lambda e: e[1])
        pos = 0
        for i, (kind, a, b, cam) in enumerate(ev):
            for fr in range(pos, min(a, nframes)):
                out[fr] = cur
            if kind == 'cut':
                cur = cam
                pos = a
                continue
            c0 = cur
            for fr in range(a, min(b, nframes)):
                u = (fr - a + 1) / (b - a)
                s = u * u * (3 - 2 * u) if kind == 'inout' else (u if kind == 'lin' else ease_out(u, 2.5))
                out[fr] = Cam(c0.cx + (cam.cx - c0.cx) * s, c0.cy + (cam.cy - c0.cy) * s, c0.z + (cam.z - c0.z) * s)
            cur = cam
            pos = b
        for fr in range(pos, nframes):
            out[fr] = cur
        return out


def assemble(cam_track, cap_track, gl_track, nframes, iris=None):
    cams = cam_track.evaluate(nframes)
    caps = cap_track.evaluate(nframes)
    gls = gl_track.evaluate(nframes)
    return [FrameState(cams[f], caps[f], gls[f], iris(f) if iris else None) for f in range(nframes)]
