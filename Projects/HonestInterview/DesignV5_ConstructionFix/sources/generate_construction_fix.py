from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
EXPORTS = ROOT / "exports"
COMPARE = ROOT / "comparison"
W, H = 1080, 1920
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")


def svg(body, w=W, h=H):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <style>
      .line {{ fill:none; stroke:#181310; stroke-width:8; stroke-linecap:round; stroke-linejoin:round; }}
      .limb {{ fill:none; stroke:#181310; stroke-width:8; stroke-linecap:round; stroke-linejoin:round; }}
      .thin {{ fill:none; stroke:#181310; stroke-width:5; stroke-linecap:round; stroke-linejoin:round; }}
      .soft {{ fill:none; stroke:#676b65; stroke-width:4; stroke-linecap:round; stroke-linejoin:round; opacity:.55; }}
      .chair {{ fill:#9b8985; stroke:#181310; stroke-width:6; stroke-linejoin:round; }}
      .chair2 {{ fill:#c5b0ad; stroke:#181310; stroke-width:6; stroke-linejoin:round; }}
      .chairDark {{ fill:#675753; stroke:#181310; stroke-width:6; stroke-linejoin:round; }}
      .skin {{ fill:#d9ddd4; stroke:#181310; stroke-width:7; stroke-linejoin:round; }}
      .shirt {{ fill:#f7efe3; stroke:#181310; stroke-width:6; stroke-linejoin:round; }}
      .eye {{ fill:#fbfff8; stroke:#181310; stroke-width:5; }}
      .skel {{ fill:none; stroke:#0d63c7; stroke-width:6; stroke-linecap:round; stroke-linejoin:round; opacity:.9; }}
      .joint {{ fill:#0d63c7; stroke:#ffffff; stroke-width:3; opacity:.95; }}
      .mark {{ fill:none; stroke:#d64b3f; stroke-width:5; stroke-linecap:round; stroke-linejoin:round; opacity:.9; }}
    </style>
  </defs>
  {body}
</svg>'''


def room():
    return '''
      <rect width="1080" height="1920" fill="#d5d2cc"/>
      <rect x="696" y="126" width="218" height="284" fill="#fbfaf4" stroke="#58524d" stroke-width="7"/>
      <path d="M805 129 L805 408 M699 264 L912 264" class="soft"/>
      <path d="M0 1138 L1080 1138 L1080 1920 L0 1920 Z" fill="#808680"/>
      <path d="M0 1365 C270 1332 760 1332 1080 1365" class="soft"/>
      <path d="M0 1600 C330 1562 780 1564 1080 1602" class="soft"/>
      <path d="M184 1138 L42 1920 M430 1138 L380 1920 M704 1138 L795 1920 M940 1138 L1068 1920" class="soft"/>
    '''


def side_table():
    return '''
      <g transform="translate(742 955)">
        <ellipse cx="64" cy="210" rx="120" ry="30" fill="#5d625d" opacity=".28"/>
        <rect x="0" y="68" width="132" height="160" fill="#444842" stroke="#181310" stroke-width="5"/>
        <rect x="18" y="92" width="96" height="42" fill="#3d413c" stroke="#181310" stroke-width="4"/>
        <rect x="18" y="154" width="96" height="42" fill="#3d413c" stroke="#181310" stroke-width="4"/>
        <circle cx="68" cy="113" r="5" fill="#caa6a0" stroke="#181310" stroke-width="3"/>
        <circle cx="68" cy="175" r="5" fill="#caa6a0" stroke="#181310" stroke-width="3"/>
      </g>
    '''


def chair_parts():
    # Three-quarter armchair. The seat cushion is horizontal enough to show
    # where the pelvis rests, while the arms/base keep the perspective.
    return {
        "shadow": '<ellipse cx="514" cy="1325" rx="285" ry="58" fill="#5f625e" opacity=".34"/>',
        "back": '''
          <path d="M350 620 C414 560 555 546 660 596 C734 632 775 720 766 830 L734 1128 L326 1128 L300 824 C292 736 306 665 350 620 Z" class="chair"/>
          <path d="M354 610 C444 661 607 656 692 616 L707 852 C604 904 451 905 316 850 Z" class="chair2"/>
        ''',
        "seat": '<path d="M348 945 L720 945 L684 1060 L378 1060 Z" fill="#e8cdd0" stroke="#181310" stroke-width="6" stroke-linejoin="round"/>',
        "far_arm": '<path d="M656 850 L772 890 L724 1290 L620 1290 Z" class="chairDark"/>',
        "near_arm": '<path d="M286 858 L394 824 L380 1290 L260 1290 Z" class="chair"/>',
        "base": '<path d="M366 1198 L724 1198 L682 1356 L402 1356 Z" class="chairDark"/>',
        "seat_line": '<path d="M328 1026 C420 998 594 1000 714 1028" class="soft"/>',
    }


def chair_only():
    c = chair_parts()
    return "\n".join([c["shadow"], c["back"], c["seat"], c["far_arm"], c["near_arm"], c["base"], c["seat_line"]])


def skeleton():
    # Joints are named in the report; the image is intentionally uncluttered.
    joints = {
        "head": (520, 596),
        "shoulder_l": (476, 730),
        "shoulder_r": (552, 730),
        "pelvis": (522, 982),
        "hip_l": (474, 986),
        "hip_r": (566, 982),
        "knee_l": (414, 1168),
        "knee_r": (632, 1168),
        "ankle_l": (386, 1308),
        "ankle_r": (664, 1312),
    }
    circles = "\n".join(f'<circle class="joint" cx="{x}" cy="{y}" r="10"/>' for x, y in joints.values())
    feet = '<path class="skel" d="M386 1308 L342 1328 M664 1312 L718 1324"/>'
    return f'''
      <g>
        <circle class="mark" cx="520" cy="596" r="94"/>
        <path class="skel" d="M476 730 L552 730 L522 982 Z"/>
        <path class="skel" d="M474 986 L414 1168 L386 1308"/>
        <path class="skel" d="M566 982 L632 1168 L664 1312"/>
        <path class="skel" d="M476 730 L340 944 L334 1036"/>
        <path class="skel" d="M552 730 L696 932 L718 1018"/>
        <path class="mark" d="M448 944 L596 944"/>
        <path class="mark" d="M474 986 C500 1010 548 1010 566 982"/>
        {feet}
        {circles}
      </g>
    '''


def character(clean=True):
    # Keep the skeleton relationship: head down to shoulders, short tapered
    # torso, pelvis on cushion, thighs forward, calves down.
    return '''
      <g>
        <!-- legs and pelvis, drawn before front chair base for overlap -->
        <path d="M474 986 C442 1038 425 1100 414 1168" class="limb"/>
        <path d="M414 1168 C386 1216 376 1265 386 1308" class="limb"/>
        <path d="M386 1308 C358 1320 344 1328 326 1330" class="limb"/>
        <path d="M566 982 C606 1035 627 1102 632 1168" class="limb"/>
        <path d="M632 1168 C650 1220 658 1268 664 1312" class="limb"/>
        <path d="M664 1312 C690 1322 710 1324 733 1314" class="limb"/>
        <path d="M474 986 C500 1016 548 1016 566 982" class="limb"/>

        <!-- shortened tapered torso touching the head directly -->
        <path d="M486 706 C462 808 450 908 474 986 C496 1002 544 1001 566 982 C574 895 568 798 548 706 C532 716 506 718 486 706 Z" class="shirt"/>

        <!-- bent arms resting on armrests -->
        <path d="M476 730 C410 788 360 864 340 944 C330 970 328 1008 334 1036" class="limb"/>
        <circle cx="334" cy="1036" r="17" fill="#181310"/>
        <path d="M552 730 C618 796 676 878 696 932 C714 964 722 994 718 1018" class="limb"/>
        <ellipse cx="718" cy="1018" rx="20" ry="16" fill="#181310"/>

        <!-- smaller compact head, restrained skeptical gaze offscreen -->
        <g transform="translate(520 596) scale(.92) translate(-520 -596)">
          <path d="M436 516 C468 455 572 438 632 492 C696 550 680 655 618 705 C561 751 470 734 431 668 C398 612 406 564 436 516 Z" class="skin"/>
          <path d="M438 515 C486 462 570 456 632 492 C611 456 542 430 474 456 C442 468 423 494 438 515 Z" fill="#171310" stroke="#181310" stroke-width="6" stroke-linejoin="round"/>
          <circle cx="612" cy="490" r="7" fill="#eee05a"/>
          <ellipse class="eye" cx="505" cy="576" rx="20" ry="34"/>
          <ellipse class="eye" cx="562" cy="572" rx="20" ry="32"/>
          <ellipse cx="520" cy="576" rx="6" ry="11" fill="#181310"/>
          <ellipse cx="577" cy="571" rx="6" ry="10" fill="#181310"/>
          <path d="M472 535 C494 520 516 522 530 538" class="thin"/>
          <path d="M544 532 C570 520 594 526 608 544" class="thin"/>
          <path d="M502 654 C532 648 568 648 598 653" class="thin"/>
        </g>
      </g>
    '''


def construction_scene():
    return svg("\n".join([room(), side_table(), chair_only(), skeleton()]))


def clean_scene():
    c = chair_parts()
    body = [
        room(),
        side_table(),
        c["shadow"],
        c["back"],
        c["seat"],
        c["far_arm"],
        character(),
        c["near_arm"],
        c["base"],
        c["seat_line"],
    ]
    return svg("\n".join(body))


def comparison_scene():
    ref = Path(r"D:\Animate\Projects\HonestInterview\ReferenceStudy\frames\ref_2p48_yes_cut.png").as_uri()
    clean = (EXPORTS / "seated_character_scene_corrected.png").as_uri()
    construction = (EXPORTS / "chair_skeleton_construction.png").as_uri()
    body = f'''
      <rect width="1800" height="1180" fill="#eee9df"/>
      <text x="56" y="66" font-family="Arial" font-size="34" fill="#181310">Reference frame 62 / 2.48s</text>
      <text x="640" y="66" font-family="Arial" font-size="34" fill="#181310">Chair + skeleton construction</text>
      <text x="1220" y="66" font-family="Arial" font-size="34" fill="#181310">Corrected original still</text>
      <image href="{ref}" x="72" y="112" width="360" height="638"/>
      <image href="{construction}" x="602" y="112" width="360" height="640"/>
      <image href="{clean}" x="1210" y="112" width="360" height="640"/>
      <text x="56" y="820" font-family="Arial" font-size="25" fill="#181310">Observed remaining differences: original is more front-facing; head still a little larger and cleaner than the rough source.</text>
      <text x="56" y="862" font-family="Arial" font-size="25" fill="#181310">Corrected: horizontal cushion, pelvis on cushion, visible thighs to knees, feet on floor, forearms on armrests.</text>
    '''
    return svg(body, 1800, 1180)


def render(svg_name, png_name, contents, out_dir=EXPORTS, width=W, height=H):
    svg_path = (SOURCES if out_dir == EXPORTS else COMPARE) / svg_name
    png_path = out_dir / png_name
    svg_path.write_text(contents, encoding="utf-8")
    subprocess.run([
        str(EDGE),
        "--headless",
        "--disable-gpu",
        f"--screenshot={png_path}",
        f"--window-size={width},{height}",
        svg_path.as_uri(),
    ], check=True)
    return png_path


if __name__ == "__main__":
    print(render("chair_skeleton_construction.svg", "chair_skeleton_construction.png", construction_scene()))
    print(render("seated_character_scene_corrected.svg", "seated_character_scene_corrected.png", clean_scene()))
    print(render("reference_side_by_side_review.svg", "reference_side_by_side_review.png", comparison_scene(), COMPARE, 1800, 1180))
