from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parent
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
W, H = 1080, 1920

LANDMARKS = json.loads((ROOT / "camera_landmarks_v4.json").read_text(encoding="utf-8"))["landmarks"]
CHAIR_FACES = json.loads((ROOT / "chair_projected_faces_v4.json").read_text(encoding="utf-8"))["faces"]


def p(name):
    return tuple(LANDMARKS[name])


def face(obj, name):
    for item in CHAIR_FACES[obj]:
        if item["face"] == name:
            return [tuple(pt) for pt in item["points"]]
    raise KeyError(f"{obj}.{name}")


def svg_doc(body):
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
.shirt{{fill:#f7efe3;stroke:#181310;stroke-width:6;stroke-linejoin:round}}
.eye{{fill:#fbfff8;stroke:#181310;stroke-width:5}}
</style>
</defs>
{body}
</svg>"""


def path_poly(points, cls, close=True):
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in points)
    if close:
        d += " Z"
    return f'<path class="{cls}" d="{d}"/>'


def line(a, b, cls="line"):
    return f'<path class="{cls}" d="M {a[0]:.1f} {a[1]:.1f} L {b[0]:.1f} {b[1]:.1f}"/>'


def draw_chair_box(obj, group_id, face_classes):
    parts = [f'<g id="{group_id}">']
    for face_name, cls in face_classes:
        parts.append(path_poly(face(obj, face_name), cls))
    parts.append("</g>")
    return "\n".join(parts)


def artwork():
    hc = p("head_center")
    ht = p("head_top")
    hb = p("head_bottom")
    pelvis = p("pelvis")
    spine = p("spine")
    ls, rs = p("l_shoulder"), p("r_shoulder")
    le, re = p("l_elbow"), p("r_elbow")
    lw, rw = p("l_wrist"), p("r_wrist")
    lh, rh = p("l_hip"), p("r_hip")
    lk, rk = p("l_knee"), p("r_knee")
    la, ra = p("l_ankle"), p("r_ankle")
    lf, rf = p("l_foot"), p("r_foot")

    head_r = max(95, abs(ht[1] - hb[1]) * 0.52)
    neck_y = hb[1] - 4
    torso_top_y = neck_y
    l_attach = (ls[0] + 24, torso_top_y)
    r_attach = (rs[0] - 24, torso_top_y)
    torso = [
        l_attach,
        r_attach,
        (rh[0] + 10, rh[1] + 2),
        (pelvis[0] + 18, pelvis[1] + 21),
        (lh[0] - 6, lh[1] + 4),
    ]

    body = [
        '<rect width="1080" height="1920" fill="#d6d3cd"/>',
        '<rect x="690" y="126" width="225" height="286" fill="#fbfaf4" stroke="#58524d" stroke-width="7"/>',
        '<path d="M803 130 L803 408 M694 264 L912 264" stroke="#a7a9a1" stroke-width="3"/>',
        '<rect x="0" y="1138" width="1080" height="782" fill="#808680"/>',
        '<path d="M0 1365 C270 1332 760 1332 1080 1365" stroke="#676b65" stroke-width="4" opacity=".5" fill="none"/>',
    ]

    body.append(draw_chair_box("backrest", "Chair_Backrest", [
        ("back", "chairSide"),
        ("right", "chairSide"),
        ("front", "chairBack"),
        ("top", "chairSeat"),
    ]))
    body.append(draw_chair_box("base", "Chair_Base", [
        ("back", "chairSide"),
        ("right", "chairSide"),
        ("front", "chairDark"),
        ("top", "chairDark"),
    ]))
    body.append(draw_chair_box("far_armrest", "Far_Armrest", [
        ("right", "chairSide"),
        ("front", "chairDark"),
        ("top", "chairDark"),
    ]))
    body.append('<g id="Far_Hand_On_Armrest">')
    body.append(f'<ellipse cx="{rw[0]:.1f}" cy="{rw[1]:.1f}" rx="18" ry="14" fill="#181310"/>')
    body.append("</g>")
    body.append(draw_chair_box("seat_cushion", "Seat_Cushion", [
        ("back", "chairSide"),
        ("right", "chairSide"),
        ("front", "chairSeat"),
        ("top", "chairSeat"),
    ]))

    body.append('<g id="Character_Legs">')
    for a, b in [(lh, lk), (lk, la), (la, lf), (rh, rk), (rk, ra), (ra, rf)]:
        body.append(line(a, b))
    body.append("</g>")

    body.append('<g id="Character_Torso">')
    body.append(path_poly(torso, "shirt"))
    body.append(line((spine[0], neck_y), pelvis, "thin"))
    body.append("</g>")

    body.append('<g id="Character_Arms">')
    for a, b in [(l_attach, le), (le, lw), (r_attach, re), (re, rw)]:
        body.append(line(a, b))
    body.append("</g>")

    body.append('<g id="Near_Hand_Behind_Armrest">')
    body.append(f'<circle cx="{lw[0]:.1f}" cy="{lw[1]:.1f}" r="17" fill="#181310"/>')
    body.append("</g>")

    body.append(draw_chair_box("near_armrest", "Near_Armrest", [
        ("left", "chairSide"),
        ("front", "chairBack"),
        ("top", "chairSeat"),
    ]))

    body.append('<g id="Character_Head">')
    body.append(f'<ellipse class="skin" cx="{hc[0]:.1f}" cy="{hc[1]:.1f}" rx="{head_r:.1f}" ry="{head_r:.1f}"/>')
    body.append(
        f'<path d="M {hc[0]-80:.1f} {hc[1]-74:.1f} '
        f'C {hc[0]-36:.1f} {hc[1]-128:.1f} {hc[0]+70:.1f} {hc[1]-120:.1f} {hc[0]+96:.1f} {hc[1]-52:.1f} '
        f'C {hc[0]+32:.1f} {hc[1]-72:.1f} {hc[0]-40:.1f} {hc[1]-60:.1f} {hc[0]-86:.1f} {hc[1]-34:.1f} Z" '
        f'fill="#171310" stroke="#181310" stroke-width="6"/>'
    )
    body.append(f'<circle cx="{hc[0]+76:.1f}" cy="{hc[1]-70:.1f}" r="7" fill="#eee05a"/>')
    body.append("</g>")

    body.append('<g id="Face_Eyes_Brows_Mouth">')
    body.append(f'<ellipse class="eye" cx="{hc[0]-30:.1f}" cy="{hc[1]+0:.1f}" rx="20" ry="34"/>')
    body.append(f'<ellipse class="eye" cx="{hc[0]+38:.1f}" cy="{hc[1]-4:.1f}" rx="20" ry="32"/>')
    body.append(f'<ellipse cx="{hc[0]-15:.1f}" cy="{hc[1]+0:.1f}" rx="6" ry="11" fill="#181310"/>')
    body.append(f'<ellipse cx="{hc[0]+53:.1f}" cy="{hc[1]-5:.1f}" rx="6" ry="10" fill="#181310"/>')
    body.append(f'<path class="thin" d="M {hc[0]-64:.1f} {hc[1]-42:.1f} C {hc[0]-42:.1f} {hc[1]-57:.1f} {hc[0]-20:.1f} {hc[1]-55:.1f} {hc[0]-6:.1f} {hc[1]-39:.1f}"/>')
    body.append(f'<path class="thin" d="M {hc[0]+8:.1f} {hc[1]-45:.1f} C {hc[0]+34:.1f} {hc[1]-57:.1f} {hc[0]+58:.1f} {hc[1]-51:.1f} {hc[0]+72:.1f} {hc[1]-33:.1f}"/>')
    body.append(f'<path class="thin" d="M {hc[0]-20:.1f} {hc[1]+76:.1f} C {hc[0]+10:.1f} {hc[1]+70:.1f} {hc[0]+46:.1f} {hc[1]+70:.1f} {hc[0]+76:.1f} {hc[1]+75:.1f}"/>')
    body.append("</g>")

    return svg_doc("\n".join(body))


def comparison(art_svg_name):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1180" viewBox="0 0 1800 1180">
<rect width="1800" height="1180" fill="#eee9df"/>
<text x="54" y="64" font-family="Arial" font-size="32">Corrected Blender camera</text>
<text x="644" y="64" font-family="Arial" font-size="32">Landmarks overlay</text>
<text x="1234" y="64" font-family="Arial" font-size="32">2D artwork from projection</text>
<image href="camera_construction_v4.png" x="60" y="105" width="430" height="765"/>
<image href="camera_landmark_overlay_v4.svg" x="650" y="105" width="430" height="765"/>
<image href="{art_svg_name}" x="1240" y="105" width="430" height="765"/>
<text x="54" y="940" font-family="Arial" font-size="25">Alignment is derived from camera_landmarks_v4.json and chair_projected_faces_v4.json. Chair depth uses projected Blender faces.</text>
</svg>"""


if __name__ == "__main__":
    art_svg = ROOT / "projected_2d_artwork_v4.svg"
    art_png = ROOT / "projected_2d_artwork_v4.png"
    art_svg.write_text(artwork(), encoding="utf-8")
    comp_svg = ROOT / "projection_alignment_comparison_v4.svg"
    comp_png = ROOT / "projection_alignment_comparison_v4.png"
    comp_svg.write_text(comparison(art_svg.name), encoding="utf-8")
    outputs = [
        (ROOT / "camera_landmark_overlay_v4.svg", ROOT / "camera_landmark_overlay_v4.png", 1080, 1920),
        (art_svg, art_png, 1080, 1920),
        (comp_svg, comp_png, 1800, 1180),
    ]
    for svg_path, png_path, w, h in outputs:
        subprocess.run(
            [str(EDGE), "--headless", "--disable-gpu", f"--screenshot={png_path}", f"--window-size={w},{h}", svg_path.as_uri()],
            check=True,
        )
        print(png_path)
