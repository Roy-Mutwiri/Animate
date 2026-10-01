from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
EXPORTS = ROOT / "exports"
COMPARE = ROOT / "reference_comparison"
EXPORTS.mkdir(exist_ok=True)
COMPARE.mkdir(exist_ok=True)

W, H = 1080, 1920
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")


def svg(body, w=W, h=H):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <style>
      .outline {{ fill:none; stroke:#181310; stroke-width:8; stroke-linecap:round; stroke-linejoin:round; }}
      .limb {{ fill:none; stroke:#181310; stroke-width:9; stroke-linecap:round; stroke-linejoin:round; }}
      .thin {{ fill:none; stroke:#181310; stroke-width:6; stroke-linecap:round; stroke-linejoin:round; }}
      .soft {{ fill:none; stroke:#696c66; stroke-width:4; stroke-linecap:round; stroke-linejoin:round; opacity:.55; }}
      .chair {{ fill:#9a8985; stroke:#181310; stroke-width:6; stroke-linejoin:round; }}
      .chairDark {{ fill:#675955; stroke:#181310; stroke-width:6; stroke-linejoin:round; }}
      .skin {{ fill:#d9ddd4; stroke:#181310; stroke-width:7; stroke-linejoin:round; }}
      .eye {{ fill:#f8fff4; stroke:#181310; stroke-width:5; }}
    </style>
  </defs>
  {body}
</svg>'''


def room():
    return '''
      <rect width="1080" height="1920" fill="#d5d2cc"/>
      <rect x="690" y="110" width="238" height="300" fill="#fbfaf4" stroke="#58524d" stroke-width="7"/>
      <path d="M809 113 L809 407 M693 263 L926 263" class="soft"/>
      <path d="M0 1128 L1080 1128 L1080 1920 L0 1920 Z" fill="#7f8580"/>
      <path d="M0 1340 C265 1312 733 1312 1080 1342" class="soft"/>
      <path d="M0 1570 C300 1538 760 1540 1080 1572" class="soft"/>
      <path d="M190 1128 L35 1920 M430 1128 L384 1920 M700 1128 L780 1920 M940 1128 L1070 1920" class="soft"/>
      <g transform="translate(710 950)">
        <ellipse cx="70" cy="232" rx="140" ry="34" fill="#5b605b" opacity=".35"/>
        <rect x="0" y="52" width="146" height="176" fill="#444842" stroke="#181310" stroke-width="5"/>
        <rect x="20" y="78" width="106" height="48" fill="#3d413c" stroke="#181310" stroke-width="4"/>
        <rect x="20" y="148" width="106" height="48" fill="#3d413c" stroke="#181310" stroke-width="4"/>
        <circle cx="74" cy="102" r="6" fill="#caa6a0" stroke="#181310" stroke-width="3"/>
        <circle cx="74" cy="172" r="6" fill="#caa6a0" stroke="#181310" stroke-width="3"/>
      </g>
    '''


def armchair():
    # Chair first, body later: opaque surfaces make overlap explicit.
    return '''
      <g transform="translate(244 742)">
        <ellipse cx="246" cy="580" rx="260" ry="56" fill="#5f625e" opacity=".35"/>
        <path d="M126 102 C168 40 286 16 388 56 C462 86 500 168 490 274 L456 610 L102 610 L72 282 C62 205 78 146 126 102 Z" class="chair"/>
        <path d="M118 76 C202 124 366 117 438 82 L450 276 C360 323 214 320 88 277 Z" fill="#bdaaa6" stroke="#181310" stroke-width="6" stroke-linejoin="round"/>
        <path d="M50 324 L154 295 L150 620 L42 620 Z" class="chair"/>
        <path d="M442 292 L532 330 L494 620 L412 620 Z" class="chairDark"/>
        <path d="M126 548 L456 548 L420 680 L158 680 Z" class="chairDark"/>
        <path d="M98 412 C178 382 331 382 450 414" class="soft"/>
      </g>
    '''


def character():
    # Compact original character, influenced by the source construction but not traced.
    return '''
      <g transform="translate(0 0)">
        <!-- narrow torso is its own small shape; the larger pink form is chair back. -->
        <path d="M471 742 C438 850 410 1040 420 1214 C454 1237 516 1240 550 1215 C559 1044 554 864 527 742 C508 758 488 758 471 742 Z" fill="#f7efe3" stroke="#181310" stroke-width="7" stroke-linejoin="round"/>

        <!-- pelvis and thin seated legs -->
        <path d="M422 1252 C386 1292 370 1372 390 1450" class="limb"/>
        <path d="M390 1450 C426 1461 464 1458 500 1435" class="limb"/>
        <path d="M486 1246 C543 1295 580 1371 596 1463" class="limb"/>
        <path d="M596 1463 C628 1478 674 1475 708 1450" class="limb"/>
        <path d="M385 1230 C430 1262 498 1260 548 1229" fill="none" stroke="#181310" stroke-width="10" stroke-linecap="round"/>

        <!-- arms, simple endpoint hands -->
        <path d="M466 812 C392 880 346 975 330 1074" class="limb"/>
        <circle cx="330" cy="1074" r="18" fill="#181310"/>
        <path d="M532 810 C604 864 668 936 724 1016" class="limb"/>
        <ellipse cx="724" cy="1016" rx="22" ry="17" fill="#181310"/>

        <!-- compact head with modest accessory and restrained offscreen gaze -->
        <path d="M389 486 C434 401 570 386 636 458 C708 535 682 668 603 724 C530 776 423 745 382 660 C350 594 354 539 389 486 Z" class="skin"/>
        <path d="M398 485 C450 421 548 405 626 456 C609 414 535 375 451 403 C406 417 381 452 398 485 Z" fill="#171310" stroke="#181310" stroke-width="6" stroke-linejoin="round"/>
        <circle cx="607" cy="455" r="7" fill="#eee05a"/>
        <ellipse class="eye" cx="500" cy="564" rx="25" ry="42"/>
        <ellipse class="eye" cx="566" cy="558" rx="23" ry="39"/>
        <ellipse cx="516" cy="562" rx="7" ry="13" fill="#181310"/>
        <ellipse cx="582" cy="555" rx="7" ry="12" fill="#181310"/>
        <path d="M462 513 C486 499 510 502 526 519" class="thin"/>
        <path d="M542 508 C566 493 594 499 610 520" class="thin"/>
        <path d="M494 646 C526 660 569 657 601 636" class="thin"/>
      </g>
    '''


def scene():
    return svg("\n".join([room(), armchair(), character()]))


def comparison():
    ref = Path(r"D:\Animate\Projects\HonestInterview\ReferenceStudy\frames\ref_2p48_yes_cut.png").as_uri()
    original = (EXPORTS / "seated_character_scene.png").as_uri()
    body = f'''
      <rect width="1600" height="1100" fill="#eee9df"/>
      <text x="60" y="72" font-family="Arial" font-size="36" fill="#181310">Reference: source frame 62 / 2.48s</text>
      <text x="840" y="72" font-family="Arial" font-size="36" fill="#181310">Original DesignV5 still</text>
      <image href="{ref}" x="90" y="120" width="470" height="833"/>
      <image href="{original}" x="820" y="120" width="470" height="833"/>
      <text x="60" y="1015" font-family="Arial" font-size="25" fill="#181310">Checked: compact head scale, direct narrow torso, thin limbs, opaque armchair overlap, pelvis on cushion, feet on floor.</text>
    '''
    return svg(body, 1600, 1100)


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
    print(render("seated_character_scene.svg", "seated_character_scene.png", scene()))
    print(render("reference_comparison.svg", "reference_comparison.png", comparison(), COMPARE, 1600, 1100))
