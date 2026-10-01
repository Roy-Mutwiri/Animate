import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
landmarks = json.loads((ROOT / "camera_landmarks_v4.json").read_text(encoding="utf-8"))["landmarks"]
hc = landmarks["head_center"]
ht = landmarks["head_top"]
hb = landmarks["head_bottom"]
r = max(95, abs(ht[1] - hb[1]) * 0.52)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<g id="head"><ellipse cx="{hc[0]:.1f}" cy="{hc[1]:.1f}" rx="{r:.1f}" ry="{r:.1f}" fill="#d9ddd4" stroke="#181310" stroke-width="7"/></g>
<g id="left_eye"><ellipse cx="{hc[0]-30:.1f}" cy="{hc[1]:.1f}" rx="20" ry="34" fill="#fbfff8" stroke="#181310" stroke-width="5"/><ellipse cx="{hc[0]-15:.1f}" cy="{hc[1]:.1f}" rx="6" ry="11" fill="#181310"/></g>
<g id="right_eye"><ellipse cx="{hc[0]+38:.1f}" cy="{hc[1]-4:.1f}" rx="20" ry="32" fill="#fbfff8" stroke="#181310" stroke-width="5"/><ellipse cx="{hc[0]+53:.1f}" cy="{hc[1]-5:.1f}" rx="6" ry="10" fill="#181310"/></g>
</svg>
"""

out = ROOT / "animate_head_eyes_import_test.svg"
out.write_text(svg, encoding="utf-8")
print(out)
