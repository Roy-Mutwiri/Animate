"""Labeled contact sheets from a video at explicit timestamps (seconds).

usage: python sheet.py VIDEO OUT.png COLS WIDTH t0 t1 ...   (or  t0:t1:step)
Frames are decoded with OpenCV by timestamp; each tile is labeled with the
source time and the source frame index so notes stay in source timecode.
"""
import sys, cv2
from PIL import Image, ImageDraw

def parse_times(args):
    out = []
    for a in args:
        if ':' in a:
            a0, a1, st = map(float, a.split(':'))
            t = a0
            while t < a1 - 1e-9:
                out.append(round(t, 4)); t += st
        else:
            out.append(float(a))
    return out

def grab(cap, fps, t):
    idx = int(round(t * fps))
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ok, fr = cap.read()
    if not ok:
        return None, idx
    return Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)), idx

def main():
    video, out, cols, width = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    times = parse_times(sys.argv[5:])
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    tiles = []
    for t in times:
        im, idx = grab(cap, fps, t)
        if im is None:
            continue
        im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        label = f"{t:.2f}s f{idx}"
        d.rectangle([0, 0, 8 * len(label) + 6, 14], fill=(0, 0, 0))
        d.text((3, 1), label, fill=(255, 80, 80))
        tiles.append(im)
    if not tiles:
        sys.exit("no frames")
    w, h = tiles[0].size
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * h), 'white')
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(out)
    print(out, sheet.size, len(tiles), 'tiles')

if __name__ == '__main__':
    main()
