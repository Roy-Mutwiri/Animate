"""Minimal XFL (Animate uncompressed document) writer.

Produces real editable Animate content: vector DOMShapes (stroked/filled
edges in twips), graphic symbols with multiple internal frames (used as
replacement-drawing libraries, frame-picked via firstFrame), and keyed layers
with optional classic motion tweens.  Coordinates passed in are pixels.
"""
import math, os, shutil
from xml.sax.saxutils import quoteattr, escape

TW = 20  # twips per pixel


def _n(v):
    return str(int(round(v * TW)))


class Path:
    """A pen path in pixel units.  Segments are lines and quadratic curves."""

    def __init__(self):
        self.cmds = []

    def move(self, x, y):
        self.cmds.append('!%s %s' % (_n(x), _n(y)))
        self.cur = (x, y); self.start = (x, y)
        return self

    def line(self, x, y):
        self.cmds.append('|%s %s' % (_n(x), _n(y)))
        self.cur = (x, y)
        return self

    def quad(self, cx, cy, x, y):
        self.cmds.append('[%s %s %s %s' % (_n(cx), _n(cy), _n(x), _n(y)))
        self.cur = (x, y)
        return self

    def cubic(self, c1x, c1y, c2x, c2y, x, y, n=4):
        """Approximate a cubic with n quadratics (midpoint approximation)."""
        x0, y0 = self.cur
        def pt(t):
            u = 1 - t
            return (u**3*x0 + 3*u*u*t*c1x + 3*u*t*t*c2x + t**3*x,
                    u**3*y0 + 3*u*u*t*c1y + 3*u*t*t*c2y + t**3*y)
        def d(t):
            u = 1 - t
            return (3*u*u*(c1x-x0) + 6*u*t*(c2x-c1x) + 3*t*t*(x-c2x),
                    3*u*u*(c1y-y0) + 6*u*t*(c2y-c1y) + 3*t*t*(y-c2y))
        for i in range(n):
            t0, t1 = i / n, (i + 1) / n
            p0, p1 = pt(t0), pt(t1)
            d0, d1 = d(t0), d(t1)
            # intersect tangents for control point
            den = d0[0]*d1[1] - d0[1]*d1[0]
            if abs(den) < 1e-9:
                c = ((p0[0]+p1[0])/2, (p0[1]+p1[1])/2)
            else:
                s = ((p1[0]-p0[0])*d1[1] - (p1[1]-p0[1])*d1[0]) / den
                c = (p0[0] + s*d0[0], p0[1] + s*d0[1])
                # guard against runaway control points
                if math.hypot(c[0]-p0[0], c[1]-p0[1]) > 3*math.hypot(p1[0]-p0[0], p1[1]-p0[1]) + 1:
                    c = pt((t0+t1)/2)
                    c = (2*c[0] - (p0[0]+p1[0])/2, 2*c[1] - (p0[1]+p1[1])/2)
            self.quad(c[0], c[1], p1[0], p1[1])
        return self

    def poly(self, pts, close=False):
        self.move(*pts[0])
        for p in pts[1:]:
            self.line(*p)
        if close:
            self.line(*pts[0])
        return self

    def smooth(self, pts, close=False):
        """Quadratic B-spline through midpoints (smooth freehand-like line)."""
        if len(pts) < 3:
            return self.poly(pts, close)
        if close:
            m = [((pts[i][0]+pts[(i+1) % len(pts)][0])/2, (pts[i][1]+pts[(i+1) % len(pts)][1])/2) for i in range(len(pts))]
            self.move(*m[-1])
            for i in range(len(pts)):
                self.quad(pts[i][0], pts[i][1], m[i][0], m[i][1])
        else:
            self.move(*pts[0])
            for i in range(1, len(pts) - 1):
                mx, my = (pts[i][0]+pts[i+1][0])/2, (pts[i][1]+pts[i+1][1])/2
                if i == len(pts) - 2:
                    mx, my = pts[-1]
                self.quad(pts[i][0], pts[i][1], mx, my)
        return self

    def ellipse(self, cx, cy, rx, ry, rot=0.0, segs=8):
        ca, sa = math.cos(rot), math.sin(rot)
        def P(a, k=1.0):
            x, y = rx * k * math.cos(a), ry * k * math.sin(a)
            return cx + x*ca - y*sa, cy + x*sa + y*ca
        k = 1 / math.cos(math.pi / segs)
        self.move(*P(0))
        for i in range(segs):
            a0 = 2*math.pi*i/segs; a1 = 2*math.pi*(i+1)/segs
            c = P((a0+a1)/2, k); e = P(a1)
            self.quad(c[0], c[1], e[0], e[1])
        return self

    def s(self):
        return ''.join(self.cmds)


def signed_area(pts):
    return 0.5 * sum(pts[i][0]*pts[(i+1) % len(pts)][1] - pts[(i+1) % len(pts)][0]*pts[i][1] for i in range(len(pts)))


class Shape:
    """Vector artwork.  Every add() is written as its OWN drawing object (DOMShape with
    isDrawingObject), stacked in call order.  Overlapping same- or different-fill paths inside one
    drawing object cancel in Animate (window erased in v5c, grin teeth grey in v5d), so parts are
    never merged.  Each object is still an ordinary editable Animate drawing object."""

    def __init__(self):
        self.items = []   # (path_string, fill_key or None, stroke_key or None, fill_side)

    def add(self, path, fill=None, stroke=None, weight=3.0, falpha=1.0, salpha=1.0, fill_side=1, caps='round'):
        fk = ('f', fill, falpha) if fill else None
        sk = ('s', stroke, weight, salpha, caps, 'round') if stroke else None
        self.items.append((path.s(), fk, sk, fill_side))
        return self

    @property
    def edges(self):
        return self.items

    @staticmethod
    def _one(pstr, fk, sk, side):
        out = ['<DOMShape isDrawingObject="true">']
        attrs = []
        if fk:
            _, c, a = fk
            al = '' if a >= 1 else ' alpha="%.3f"' % a
            out.append('<fills><FillStyle index="1"><SolidColor color="%s"%s/></FillStyle></fills>' % (c, al))
            attrs.append('fillStyle%d="1"' % side)
        if sk:
            _, c, w, a, caps, j = sk
            al = '' if a >= 1 else ' alpha="%.3f"' % a
            capattr = '' if caps == 'round' else ' caps="%s"' % caps
            out.append('<strokes><StrokeStyle index="1"><SolidStroke scaleMode="normal" weight="%.2f"%s joints="round"><fill><SolidColor color="%s"%s/></fill></SolidStroke></StrokeStyle></strokes>' % (w, capattr, c, al))
            attrs.append('strokeStyle="1"')
        out.append('<edges><Edge %s edges="%s"/></edges></DOMShape>' % (' '.join(attrs), pstr))
        return ''.join(out)

    def xml(self):
        return '\n'.join(self._one(*it) for it in self.items)


class Stack:
    """A list of drawing objects built through the Shape.add interface: every add() becomes its own
    drawing object, stacked in order.  Used where fills overlap (mouths), because overlapping paths
    inside ONE drawing object cancel in Animate (grin teeth rendered head-grey in v5d)."""

    def __init__(self):
        self.parts = []

    def add(self, *a, **k):
        s = Shape()
        s.add(*a, **k)
        self.parts.append(s)
        return self

    def xml(self):
        return '\n'.join(p.xml() for p in self.parts)


def matrix_xml(tx=0.0, ty=0.0, sx=1.0, sy=1.0, rot=0.0):
    r = math.radians(rot)
    a, b = sx*math.cos(r), sx*math.sin(r)
    c, d = -sy*math.sin(r), sy*math.cos(r)
    return '<matrix><Matrix a="%.6f" b="%.6f" c="%.6f" d="%.6f" tx="%.2f" ty="%.2f"/></matrix>' % (a, b, c, d, tx, ty)


class Instance:
    def __init__(self, name, tx=0, ty=0, sx=1, sy=1, rot=0, first=0, loop='single frame', reg=(0, 0), alpha=None):
        self.name, self.tx, self.ty, self.sx, self.sy, self.rot = name, tx, ty, sx, sy, rot
        self.first, self.loop, self.reg, self.alpha = first, loop, reg, alpha

    def xml(self):
        s = '<DOMSymbolInstance libraryItemName=%s symbolType="graphic" firstFrame="%d" loop="%s">' % (quoteattr(self.name), self.first, self.loop)
        # Symbol registration point is its local origin; tx,ty place that origin.
        s += matrix_xml(self.tx, self.ty, self.sx, self.sy, self.rot)
        s += '<transformationPoint><Point x="%.2f" y="%.2f"/></transformationPoint>' % self.reg
        if self.alpha is not None:
            s += '<color><Color alphaMultiplier="%.3f"/></color>' % self.alpha
        s += '</DOMSymbolInstance>'
        return s


class Frame:
    def __init__(self, index, duration=1, elements=None, tween=False, ease=0, label=None):
        self.index, self.duration, self.elements = index, duration, elements or []
        self.tween, self.ease, self.label = tween, ease, label

    def xml(self):
        attrs = 'index="%d"' % self.index
        if self.duration > 1:
            attrs += ' duration="%d"' % self.duration
        if self.label:
            attrs += ' name=%s labelType="name"' % quoteattr(self.label)
        if self.tween:
            attrs += ' tweenType="motion" motionTweenSnap="true" keyMode="22017"'
            if self.ease:
                attrs += ' acceleration="%d"' % self.ease
        else:
            attrs += ' keyMode="9728"'
        return '<DOMFrame %s><elements>%s</elements></DOMFrame>' % (attrs, '\n'.join(e.xml() for e in self.elements))


class Layer:
    def __init__(self, name, color='#4F80FF', layer_type=None, parent=None, visible=True):
        self.name, self.color, self.frames = name, color, []
        self.layer_type, self.parent, self.visible = layer_type, parent, visible

    def key(self, index, duration, elements, tween=False, ease=0, label=None):
        self.frames.append(Frame(index, duration, elements, tween, ease, label))
        return self

    def xml(self):
        extra = '' if self.visible else ' visible="false"'
        if self.layer_type:
            extra += ' layerType="%s"' % self.layer_type
        fr = sorted(self.frames, key=lambda f: f.index)
        # sanity: no overlaps / gaps
        for a, b in zip(fr, fr[1:]):
            assert a.index + a.duration <= b.index, (self.name, a.index, a.duration, b.index)
        return '<DOMLayer name=%s color="%s"%s><frames>%s</frames></DOMLayer>' % (quoteattr(self.name), self.color, extra, '\n'.join(f.xml() for f in fr))


class Timeline:
    def __init__(self, name):
        self.name, self.layers = name, []

    def layer(self, name, **kw):
        L = Layer(name, **kw)
        self.layers.append(L)
        return L

    def xml(self):
        # Animate lists layers top-first
        return '<DOMTimeline name=%s><layers>%s</layers></DOMTimeline>' % (quoteattr(self.name), '\n'.join(l.xml() for l in self.layers))


class Symbol:
    def __init__(self, name, folder=None):
        self.name, self.folder = name, folder
        self.timeline = Timeline(name.split('/')[-1])

    def xml(self):
        return ('<DOMSymbolItem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://ns.adobe.com/xfl/2008/" '
                'name=%s symbolType="graphic"><timeline>%s</timeline></DOMSymbolItem>' % (quoteattr(self.name), self.timeline.xml()))


class Document:
    def __init__(self, width, height, fps, bg='#FFFFFF'):
        self.width, self.height, self.fps, self.bg = width, height, fps, bg
        self.symbols, self.scenes, self.folders = [], [], set()

    def symbol(self, name):
        s = Symbol(name)
        if '/' in name:
            parts = name.split('/')[:-1]
            for i in range(len(parts)):
                self.folders.add('/'.join(parts[:i+1]))
        self.symbols.append(s)
        return s

    def scene(self, name):
        t = Timeline(name)
        self.scenes.append(t)
        return t

    def write(self, folder, stem):
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        os.makedirs(os.path.join(folder, 'LIBRARY'))
        os.makedirs(os.path.join(folder, 'META-INF'))
        with open(os.path.join(folder, stem + '.xfl'), 'w') as f:
            f.write('PROXY-CS5')
        inc = []
        for s in self.symbols:
            fn = s.name + '.xml'
            p = os.path.join(folder, 'LIBRARY', *fn.split('/'))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'w', encoding='utf-8') as f:
                f.write(s.xml())
            inc.append('<Include href=%s loadImmediate="false"/>' % quoteattr(fn))
        folders = ''.join('<DOMFolderItem name=%s isExpanded="false"/>' % quoteattr(n) for n in sorted(self.folders))
        doc = ('<DOMDocument xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://ns.adobe.com/xfl/2008/" '
               'backgroundColor="%s" width="%d" height="%d" frameRate="%d" currentTimeline="1" xflVersion="22.02" '
               'creatorInfo="Adobe Animate" platform="Windows" versionInfo="Saved by Animate Windows 24.0 build 15" '
               'majorVersion="24" buildNumber="15" playOptionsPlayLoop="false" playOptionsPlayPages="false" playOptionsPlayFrameActions="false">'
               '<folders>%s</folders><symbols>%s</symbols><timelines>%s</timelines></DOMDocument>') % (
            self.bg, self.width, self.height, self.fps, folders, ''.join(inc), ''.join(t.xml() for t in self.scenes))
        with open(os.path.join(folder, 'DOMDocument.xml'), 'w', encoding='utf-8') as f:
            f.write(doc)
        return os.path.join(folder, stem + '.xfl')
