from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "exports"
SOURCES = ROOT / "sources"
EXPORTS.mkdir(exist_ok=True)

W, H = 1080, 1920
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")


def svg_doc(body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <style>
      .line {{ fill:none; stroke:#211915; stroke-width:10; stroke-linecap:round; stroke-linejoin:round; }}
      .thin {{ fill:none; stroke:#211915; stroke-width:7; stroke-linecap:round; stroke-linejoin:round; }}
      .softline {{ fill:none; stroke:#6f6f67; stroke-width:4; stroke-linecap:round; stroke-linejoin:round; opacity:.55; }}
      .skinI {{ fill:#d9ded6; stroke:#211915; stroke-width:8; stroke-linecap:round; stroke-linejoin:round; }}
      .skinR {{ fill:#efb77f; stroke:#211915; stroke-width:8; stroke-linecap:round; stroke-linejoin:round; }}
      .shirt {{ fill:#f7eddf; stroke:#211915; stroke-width:8; stroke-linecap:round; stroke-linejoin:round; }}
      .chair {{ fill:#8f7a78; stroke:#211915; stroke-width:7; stroke-linejoin:round; }}
      .chairDark {{ fill:#655452; stroke:#211915; stroke-width:7; stroke-linejoin:round; }}
      .dark {{ fill:#211915; }}
      .eye {{ fill:#fbfff8; stroke:#211915; stroke-width:7; }}
      .mouth {{ fill:#120c14; stroke:#211915; stroke-width:6; stroke-linejoin:round; }}
    </style>
  </defs>
  {body}
</svg>'''


def bg(close=False):
    floor_y = 1340 if close else 1260
    window = "" if close else '''
      <rect x="420" y="110" width="260" height="300" fill="#fbfaf3" stroke="#5b5550" stroke-width="8"/>
      <path d="M550 112 L550 408 M422 260 L678 260" class="softline" opacity=".8"/>
    '''
    floor_lines = "" if close else '''
      <path d="M0 1490 C260 1460 740 1460 1080 1490" class="softline"/>
      <path d="M0 1700 C250 1665 780 1665 1080 1705" class="softline"/>
      <path d="M210 1260 L40 1920 M520 1260 L440 1920 M850 1260 L940 1920" class="softline"/>
    '''
    return f'''
      <rect width="1080" height="1920" fill="#d7d4ce"/>
      {window}
      <path d="M0 {floor_y} C300 {floor_y-30} 735 {floor_y-30} 1080 {floor_y}" fill="#858b86"/>
      {floor_lines}
    '''


def chair(cx, cy, scale=1, facing=1):
    # Opaque chair drawn behind body with solid overlap.
    return f'''
      <g transform="translate({cx} {cy}) scale({facing*scale} {scale})">
        <path d="M-150 15 C-168 -105 -125 -206 -18 -222 C96 -239 158 -172 163 -60 L156 132 L-158 132 Z" class="chair"/>
        <path d="M-170 92 L172 92 L142 205 L-144 205 Z" class="chairDark"/>
        <path d="M-136 -42 C-86 -72 -4 -80 92 -59" class="thin" opacity=".35"/>
      </g>
    '''


def interviewer_head(cx, cy, scale=1, reaction=False):
    if not reaction:
        eyes = '''
          <ellipse class="eye" cx="-38" cy="-18" rx="31" ry="45"/>
          <ellipse class="eye" cx="40" cy="-18" rx="31" ry="45"/>
          <ellipse class="dark" cx="-27" cy="-12" rx="8" ry="15"/>
          <ellipse class="dark" cx="27" cy="-12" rx="8" ry="15"/>
          <path d="M-78 -70 C-52 -84 -22 -82 0 -66" class="thin"/>
          <path d="M20 -66 C50 -80 82 -72 96 -54" class="thin"/>
          <path d="M-78 76 C-44 58 6 62 40 86" class="mouth"/>
          <path d="M-56 75 C-25 69 7 73 25 84" fill="none" stroke="#f5eee4" stroke-width="5" stroke-linecap="round"/>
        '''
    else:
        eyes = '''
          <ellipse class="eye" cx="-38" cy="-20" rx="34" ry="43"/>
          <ellipse class="eye" cx="42" cy="-12" rx="32" ry="38"/>
          <ellipse class="dark" cx="-17" cy="-14" rx="8" ry="14"/>
          <ellipse class="dark" cx="63" cy="-7" rx="8" ry="13"/>
          <path d="M-92 -86 C-58 -118 -20 -112 6 -88" class="thin"/>
          <path d="M24 -65 C62 -83 92 -75 112 -43" class="thin"/>
          <path d="M-76 76 C-28 59 30 63 75 79" class="thin"/>
          <path d="M-61 80 C-20 89 25 90 60 82" class="thin"/>
        '''
    return f'''
      <g transform="translate({cx} {cy}) scale({scale})">
        <path d="M-120 -165 C-60 -210 58 -205 108 -136 C158 -65 144 70 92 136 C42 199 -69 186 -112 122 C-155 58 -154 -95 -120 -165 Z" class="skinI"/>
        <path d="M-132 -170 C-68 -216 54 -219 126 -155 C142 -142 150 -127 143 -122 C65 -130 -13 -120 -144 -94 C-150 -123 -148 -148 -132 -170 Z" fill="#090908" stroke="#211915" stroke-width="8" stroke-linejoin="round"/>
        <circle cx="91" cy="-159" r="9" fill="#eee05a"/>
        {eyes}
        <path d="M-38 149 L-35 196 L35 193 L32 145" class="skinI"/>
      </g>
    '''


def respondent_head(cx, cy, scale=1, attentive=True):
    mouth = '<path d="M-42 74 C-5 83 38 82 78 67" class="thin"/>' if attentive else '<path d="M-78 62 C-40 18 30 12 86 50 C42 100 -24 104 -78 62 Z" class="mouth"/><path d="M-45 53 C-7 43 29 47 58 58" fill="none" stroke="#f7eddf" stroke-width="6" stroke-linecap="round"/>'
    return f'''
      <g transform="translate({cx} {cy}) scale({scale})">
        <path d="M-118 -134 C-55 -203 70 -184 123 -101 C171 -27 151 94 75 149 C5 200 -99 162 -136 82 C-173 2 -164 -83 -118 -134 Z" class="skinR"/>
        <path d="M-42 -151 C-34 -191 -20 -193 -13 -151 M-2 -162 C5 -204 20 -204 23 -159 M36 -152 C51 -191 66 -188 64 -141" class="thin"/>
        <ellipse class="eye" cx="-44" cy="-38" rx="39" ry="52"/>
        <ellipse class="eye" cx="48" cy="-34" rx="39" ry="52"/>
        <ellipse class="dark" cx="-30" cy="-28" rx="10" ry="15"/>
        <ellipse class="dark" cx="63" cy="-24" rx="10" ry="15"/>
        <path d="M-83 -105 C-51 -124 -17 -121 8 -104" class="thin"/>
        <path d="M34 -105 C72 -117 103 -102 124 -80" class="thin"/>
        {mouth}
        <path d="M-35 147 L-30 194 L34 190 L30 144" class="skinR"/>
      </g>
    '''


def palm_hand(x, y, rot=0, scale=1, fill="#d9ded6", grip=False):
    fingers = '''
      <path d="M-10 -33 C-20 -65 -5 -73 6 -41" class="thin"/>
      <path d="M10 -37 C8 -73 25 -72 25 -38" class="thin"/>
      <path d="M29 -31 C41 -62 55 -52 43 -24" class="thin"/>
    ''' if not grip else '''
      <path d="M-28 -11 C-54 -17 -54 -39 -27 -36" class="thin"/>
      <path d="M-20 -26 C-46 -43 -35 -62 -10 -41" class="thin"/>
      <path d="M4 -34 C-12 -62 8 -71 19 -41" class="thin"/>
      <path d="M26 -23 C36 -52 55 -43 45 -15" class="thin"/>
    '''
    return f'''
      <g transform="translate({x} {y}) rotate({rot}) scale({scale})">
        <path d="M-31 -20 C-12 -48 37 -43 53 -12 C68 19 42 52 4 50 C-36 49 -52 10 -31 -20 Z" fill="{fill}" stroke="#211915" stroke-width="7" stroke-linejoin="round"/>
        {fingers}
        <path d="M-32 8 C-61 20 -62 46 -28 38" class="thin"/>
      </g>
    '''


def microphone(x, y, rot=0, scale=1):
    return f'''
      <g transform="translate({x} {y}) rotate({rot}) scale({scale})">
        <rect x="-14" y="-74" width="28" height="92" rx="12" fill="#2b2d3b" stroke="#211915" stroke-width="7"/>
        <rect x="-43" y="-128" width="86" height="64" rx="15" fill="#45485e" stroke="#211915" stroke-width="7"/>
        <rect x="-27" y="-113" width="54" height="34" rx="7" fill="#565a72" opacity=".85"/>
      </g>
    '''


def mic_side(x, y, rot=0, scale=1):
    return f'''
      <g transform="translate({x} {y}) rotate({rot}) scale({scale})">
        <rect x="-12" y="-12" width="132" height="25" rx="12" fill="#2b2d3b" stroke="#211915" stroke-width="7"/>
        <rect x="96" y="-38" width="74" height="74" rx="16" fill="#45485e" stroke="#211915" stroke-width="7"/>
        <rect x="112" y="-22" width="40" height="42" rx="8" fill="#565a72" opacity=".85"/>
      </g>
    '''


def opening():
    body = [bg(False)]
    body += [chair(286, 1092, 1.02, 1), chair(805, 1115, .98, -1)]
    # interviewer seated body, thighs, shoulders
    body.append('''
      <path d="M260 861 C230 965 225 1132 268 1258 C316 1306 425 1308 470 1250 C450 1118 420 970 377 858 C343 838 295 836 260 861 Z" class="shirt"/>
      <path d="M279 1246 C244 1305 238 1395 288 1484 L388 1480 C373 1391 372 1303 401 1242 Z" fill="#f4dfe0" stroke="#211915" stroke-width="8"/>
      <path d="M397 1239 C458 1283 489 1370 503 1468 L601 1463 C581 1342 542 1260 475 1217 Z" fill="#6d5b58" stroke="#211915" stroke-width="8"/>
      <path d="M265 904 C226 974 207 1067 218 1160" class="line"/>
      <path d="M380 906 C448 954 502 1018 548 1092" class="line"/>
    ''')
    body.append(interviewer_head(318, 650, .86, False))
    body.append(palm_hand(219, 1175, 8, .72, "#d9ded6", False))
    # Aligned grip: wrist, palm, and mic handle share one direction and stay away from props.
    body.append(mic_side(546, 1088, -24, .92))
    body.append(palm_hand(552, 1090, -18, .78, "#d9ded6", True))
    # respondent seated attentive
    body.append('''
      <path d="M713 865 C664 975 652 1134 699 1260 C750 1311 861 1326 918 1257 C900 1117 870 974 829 866 C793 842 748 842 713 865 Z" class="shirt"/>
      <path d="M702 1242 C647 1312 635 1407 691 1500 L792 1494 C775 1396 781 1325 812 1251 Z" fill="#f4dfe0" stroke="#211915" stroke-width="8"/>
      <path d="M831 1251 C905 1302 945 1387 966 1496 L1067 1495 C1044 1366 995 1273 919 1219 Z" fill="#6d5b58" stroke="#211915" stroke-width="8"/>
      <path d="M710 914 C674 984 657 1052 657 1135" class="line"/>
      <path d="M828 914 C906 973 960 1032 1004 1122" class="line"/>
    ''')
    body.append(respondent_head(768, 642, .9, True))
    body.append(palm_hand(653, 1147, -12, .7, "#efb77f", False))
    body.append(palm_hand(1002, 1126, -25, .72, "#efb77f", False))
    return svg_doc("\n".join(body))


def reaction():
    body = [bg(True)]
    body.append('''
      <g transform="translate(130 1010)">
        <path d="M70 182 C40 39 93 -82 222 -96 C367 -114 449 -20 438 146 L418 368 L84 368 Z" class="chair"/>
        <path d="M62 298 L438 298 L396 443 L104 443 Z" class="chairDark"/>
      </g>
      <path d="M285 1015 C220 1140 205 1324 278 1488 C360 1575 551 1582 651 1490 C637 1326 594 1142 520 1017 C452 970 344 972 285 1015 Z" class="shirt"/>
      <path d="M286 1080 C225 1180 195 1286 211 1400" class="line"/>
      <path d="M526 1075 C628 1138 707 1216 760 1310" class="line"/>
    ''')
    body.append(interviewer_head(420, 665, 1.55, True))
    body.append('<path d="M760 1310 C799 1340 835 1370 866 1404" class="line"/>')
    body.append(mic_side(835, 1397, 25, .86))
    body.append(palm_hand(861, 1414, 14, 1.0, "#d9ded6", True))
    # small recoil arc and eye direction mark without text
    body.append('<path d="M270 520 C236 547 223 588 232 629" class="softline"/>')
    return svg_doc("\n".join(body))


def render(svg_name, png_name, text):
    svg_path = SOURCES / svg_name
    png_path = EXPORTS / png_name
    svg_path.write_text(text, encoding="utf-8")
    if not EDGE.exists():
        raise SystemExit(f"Edge not found at {EDGE}")
    url = svg_path.as_uri()
    cmd = [
        str(EDGE),
        "--headless",
        "--disable-gpu",
        f"--screenshot={png_path}",
        f"--window-size={W},{H}",
        url,
    ]
    subprocess.run(cmd, check=True)
    return png_path


if __name__ == "__main__":
    print(render("opening_conversation.svg", "opening_conversation.png", opening()))
    print(render("interviewer_reaction.svg", "interviewer_reaction.png", reaction()))
