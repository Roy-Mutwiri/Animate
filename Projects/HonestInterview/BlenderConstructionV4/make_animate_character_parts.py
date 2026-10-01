from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "animate_character_parts"
OUT.mkdir(exist_ok=True)
W, H = 1080, 1920

landmarks = json.loads((ROOT / "camera_landmarks_v4.json").read_text(encoding="utf-8"))["landmarks"]
faces = json.loads((ROOT / "chair_projected_faces_v4.json").read_text(encoding="utf-8"))["faces"]


def p(name):
    return tuple(landmarks[name])


def face(obj, name):
    for item in faces[obj]:
        if item["face"] == name:
            return [tuple(pt) for pt in item["points"]]
    raise KeyError(f"{obj}.{name}")


def doc(body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<style>
.line{{fill:none;stroke:#181310;stroke-width:8;stroke-linecap:round;stroke-linejoin:round}}
.thin{{fill:none;stroke:#181310;stroke-width:5;stroke-linecap:round;stroke-linejoin:round}}
.chairBack{{fill:#9b8985;stroke:#181310;stroke-width:7;stroke-linejoin:round}}
.chairSeat{{fill:#c5b0ad;stroke:#181310;stroke-width:7;stroke-linejoin:round}}
.chairDark{{fill:#675753;stroke:#181310;stroke-width:7;stroke-linejoin:round}}
.chairSide{{fill:#766863;stroke:#181310;stroke-width:7;stroke-linejoin:round}}
.skin{{fill:#d9ddd4;stroke:#181310;stroke-width:7;stroke-linejoin:round}}
.eye{{fill:#fbfff8;stroke:#181310;stroke-width:5}}
</style>
</defs>
{body}
</svg>
"""


def poly(points, cls):
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in points) + " Z"
    return f'<path class="{cls}" d="{d}"/>'


def line(a, b, cls="line"):
    return f'<path class="{cls}" d="M {a[0]:.1f} {a[1]:.1f} L {b[0]:.1f} {b[1]:.1f}"/>'


def box(obj, face_classes):
    return "\n".join(poly(face(obj, n), c) for n, c in face_classes)


hc = p("head_center")
ht, hb = p("head_top"), p("head_bottom")
head_r = max(95, abs(ht[1] - hb[1]) * 0.52)
ls, rs = p("l_shoulder"), p("r_shoulder")
le, re = p("l_elbow"), p("r_elbow")
lw, rw = p("l_wrist"), p("r_wrist")
lh, rh = p("l_hip"), p("r_hip")
lk, rk = p("l_knee"), p("r_knee")
la, ra = p("l_ankle"), p("r_ankle")
lf, rf = p("l_foot"), p("r_foot")
pelvis, spine = p("pelvis"), p("spine")

neck_y = hb[1] - 3
l_attach = (ls[0] + 24, neck_y)
r_attach = (rs[0] - 24, neck_y)
torso = [
    (hc[0] - 45, neck_y - 2),
    (hc[0] + 58, neck_y),
    (pelvis[0] + 28, pelvis[1] + 22),
    (pelvis[0] - 26, pelvis[1] + 17),
]

parts = {
    "00_background.svg": doc("\n".join([
        '<rect width="1080" height="1920" fill="#d6d3cd"/>',
        '<rect x="690" y="126" width="225" height="286" fill="#fbfaf4" stroke="#58524d" stroke-width="7"/>',
        '<path d="M803 130 L803 408 M694 264 L912 264" stroke="#a7a9a1" stroke-width="3"/>',
        '<rect x="0" y="1138" width="1080" height="782" fill="#808680"/>',
        '<path d="M0 1365 C270 1332 760 1332 1080 1365" stroke="#676b65" stroke-width="4" opacity=".5" fill="none"/>',
    ])),
    "01_chair_back_base.svg": doc("\n".join([
        box("backrest", [("back", "chairSide"), ("right", "chairSide"), ("front", "chairBack"), ("top", "chairSeat")]),
        box("base", [("back", "chairSide"), ("right", "chairSide"), ("front", "chairDark"), ("top", "chairDark")]),
        box("far_armrest", [("right", "chairSide"), ("front", "chairDark"), ("top", "chairDark")]),
        box("seat_cushion", [("back", "chairSide"), ("right", "chairSide"), ("front", "chairSeat"), ("top", "chairSeat")]),
    ])),
    "02_body.svg": doc("\n".join([
        poly(torso, "skin"),
        line((spine[0], neck_y), pelvis, "thin"),
        line(lh, lk),
        line(lk, la),
        line(la, lf),
        line(rh, rk),
        line(rk, ra),
        line(ra, rf),
    ])),
    "03_arms.svg": doc("\n".join([
        line(l_attach, le),
        line(le, lw),
        line(r_attach, re),
        line(re, rw),
        f'<circle cx="{lw[0]:.1f}" cy="{lw[1]:.1f}" r="13" fill="#181310"/>',
        f'<ellipse cx="{rw[0]:.1f}" cy="{rw[1]:.1f}" rx="16" ry="12" fill="#181310"/>',
    ])),
    "04_chair_foreground.svg": doc(box("near_armrest", [("left", "chairSide"), ("front", "chairBack"), ("top", "chairSeat")])),
    "05_head.svg": doc("\n".join([
        f'<ellipse class="skin" cx="{hc[0]:.1f}" cy="{hc[1]:.1f}" rx="{head_r:.1f}" ry="{head_r:.1f}"/>',
        f'<path d="M {hc[0]-80:.1f} {hc[1]-74:.1f} C {hc[0]-36:.1f} {hc[1]-128:.1f} {hc[0]+70:.1f} {hc[1]-120:.1f} {hc[0]+96:.1f} {hc[1]-52:.1f} C {hc[0]+32:.1f} {hc[1]-72:.1f} {hc[0]-40:.1f} {hc[1]-60:.1f} {hc[0]-86:.1f} {hc[1]-34:.1f} Z" fill="#171310" stroke="#181310" stroke-width="6"/>',
        f'<circle cx="{hc[0]+76:.1f}" cy="{hc[1]-70:.1f}" r="7" fill="#eee05a"/>',
    ])),
    "06_eyes.svg": doc("\n".join([
        f'<ellipse class="eye" cx="{hc[0]-30:.1f}" cy="{hc[1]+0:.1f}" rx="20" ry="34"/>',
        f'<ellipse class="eye" cx="{hc[0]+38:.1f}" cy="{hc[1]-4:.1f}" rx="20" ry="32"/>',
        f'<ellipse cx="{hc[0]-15:.1f}" cy="{hc[1]+0:.1f}" rx="6" ry="11" fill="#181310"/>',
        f'<ellipse cx="{hc[0]+53:.1f}" cy="{hc[1]-5:.1f}" rx="6" ry="10" fill="#181310"/>',
    ])),
    "07_brows.svg": doc("\n".join([
        f'<path class="thin" d="M {hc[0]-64:.1f} {hc[1]-42:.1f} C {hc[0]-42:.1f} {hc[1]-57:.1f} {hc[0]-20:.1f} {hc[1]-55:.1f} {hc[0]-6:.1f} {hc[1]-39:.1f}"/>',
        f'<path class="thin" d="M {hc[0]+8:.1f} {hc[1]-45:.1f} C {hc[0]+34:.1f} {hc[1]-57:.1f} {hc[0]+58:.1f} {hc[1]-51:.1f} {hc[0]+72:.1f} {hc[1]-33:.1f}"/>',
    ])),
    "08_mouth.svg": doc(f'<path class="thin" d="M {hc[0]-20:.1f} {hc[1]+76:.1f} C {hc[0]+10:.1f} {hc[1]+70:.1f} {hc[0]+46:.1f} {hc[1]+70:.1f} {hc[0]+76:.1f} {hc[1]+75:.1f}"/>'),
}

for name, content in parts.items():
    (OUT / name).write_text(content, encoding="utf-8")
    print(OUT / name)
