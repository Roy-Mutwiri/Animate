from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
W, H = 1080, 1920


def svg_doc(body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <style>
      .line {{ fill:none; stroke:#181310; stroke-width:8; stroke-linecap:round; stroke-linejoin:round; }}
      .thin {{ fill:none; stroke:#181310; stroke-width:5; stroke-linecap:round; stroke-linejoin:round; }}
      .chair {{ fill:#9b8985; stroke:#181310; stroke-width:7; stroke-linejoin:round; }}
      .chair2 {{ fill:#c5b0ad; stroke:#181310; stroke-width:7; stroke-linejoin:round; }}
      .darkchair {{ fill:#675753; stroke:#181310; stroke-width:7; stroke-linejoin:round; }}
      .skin {{ fill:#d9ddd4; stroke:#181310; stroke-width:7; stroke-linejoin:round; }}
      .shirt {{ fill:#f7efe3; stroke:#181310; stroke-width:6; stroke-linejoin:round; }}
      .eye {{ fill:#fbfff8; stroke:#181310; stroke-width:5; }}
    </style>
  </defs>
  {body}
</svg>'''


def still():
    return svg_doc('''
    <g id="Background">
      <rect width="1080" height="1920" fill="#d6d3cd"/>
      <rect x="690" y="126" width="225" height="286" fill="#fbfaf4" stroke="#58524d" stroke-width="7"/>
      <path d="M803 130 L803 408 M694 264 L912 264" stroke="#a7a9a1" stroke-width="3"/>
      <rect x="0" y="1138" width="1080" height="782" fill="#808680"/>
      <path d="M0 1365 C270 1332 760 1332 1080 1365" stroke="#676b65" stroke-width="4" opacity=".5" fill="none"/>
      <path d="M184 1138 L42 1920 M430 1138 L380 1920 M704 1138 L795 1920 M940 1138 L1068 1920" stroke="#676b65" stroke-width="4" opacity=".5"/>
    </g>
    <g id="Chair_Backrest">
      <path class="chair" d="M312 590 C382 548 640 548 735 602 C782 675 772 805 746 1122 L318 1122 C290 820 276 668 312 590 Z"/>
      <path class="chair2" d="M352 604 C438 658 620 657 700 610 L710 880 C610 930 444 930 326 880 Z"/>
    </g>
    <g id="Seat_Cushion">
      <path d="M292 930 L758 930 L725 1088 L318 1088 Z" fill="#e8cdd0" stroke="#181310" stroke-width="7" stroke-linejoin="round"/>
    </g>
    <g id="Far_Armrest">
      <path class="darkchair" d="M665 840 L780 900 L730 1318 L620 1318 Z"/>
    </g>
    <g id="Chair_Base">
      <path class="darkchair" d="M360 1240 L735 1240 L706 1364 L388 1364 Z"/>
    </g>
    <g id="Character_Legs">
      <path class="line" d="M476 996 C438 1056 418 1124 405 1174"/>
      <path class="line" d="M405 1174 C384 1230 372 1285 368 1330"/>
      <path class="line" d="M368 1330 C342 1338 326 1341 310 1338"/>
      <path class="line" d="M566 996 C606 1056 628 1122 640 1174"/>
      <path class="line" d="M640 1174 C655 1235 664 1288 668 1330"/>
      <path class="line" d="M668 1330 C700 1338 728 1332 744 1320"/>
    </g>
    <g id="Character_Torso">
      <path class="shirt" d="M486 706 C464 804 454 918 476 996 C502 1018 540 1018 566 996 C574 910 566 806 548 706 C530 720 504 720 486 706 Z"/>
    </g>
    <g id="Character_Arms">
      <path class="line" d="M476 730 C420 790 375 870 342 945"/>
      <path class="line" d="M342 945 C330 980 328 1010 336 1036"/>
      <circle cx="336" cy="1036" r="17" fill="#181310"/>
      <path class="line" d="M552 730 C610 790 665 874 696 935"/>
      <path class="line" d="M696 935 C716 970 722 998 718 1020"/>
      <ellipse cx="718" cy="1020" rx="20" ry="16" fill="#181310"/>
    </g>
    <g id="Near_Armrest">
      <path class="chair" d="M258 840 L398 814 L385 1318 L250 1318 Z"/>
    </g>
    <g id="Character_Head">
      <path class="skin" d="M436 516 C468 455 572 438 632 492 C696 550 680 655 618 705 C561 751 470 734 431 668 C398 612 406 564 436 516 Z"/>
      <path d="M438 515 C486 462 570 456 632 492 C611 456 542 430 474 456 C442 468 423 494 438 515 Z" fill="#171310" stroke="#181310" stroke-width="6" stroke-linejoin="round"/>
      <circle cx="612" cy="490" r="7" fill="#eee05a"/>
    </g>
    <g id="Face_Eyes_Brows_Mouth">
      <ellipse class="eye" cx="505" cy="576" rx="20" ry="34"/>
      <ellipse class="eye" cx="562" cy="572" rx="20" ry="32"/>
      <ellipse cx="520" cy="576" rx="6" ry="11" fill="#181310"/>
      <ellipse cx="577" cy="571" rx="6" ry="10" fill="#181310"/>
      <path class="thin" d="M472 535 C494 520 516 522 530 538"/>
      <path class="thin" d="M544 532 C570 520 594 526 608 544"/>
      <path class="thin" d="M502 654 C532 648 568 648 598 653"/>
    </g>
    ''')


if __name__ == "__main__":
    svg_path = ROOT / "honest_interview_clean_2d_still.svg"
    png_path = ROOT / "honest_interview_clean_2d_still.png"
    svg_path.write_text(still(), encoding="utf-8")
    subprocess.run([
        str(EDGE),
        "--headless",
        "--disable-gpu",
        f"--screenshot={png_path}",
        f"--window-size={W},{H}",
        svg_path.as_uri(),
    ], check=True)
    print(svg_path)
    print(png_path)
