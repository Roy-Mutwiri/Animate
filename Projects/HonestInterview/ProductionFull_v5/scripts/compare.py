"""Side-by-side comparison sheets: reference frame (left) vs production frame (right), same
display height, no stretching.  usage: compare.py OUT.png ref_t:prod_png [...] [--h 640]"""
import sys, cv2
from PIL import Image, ImageDraw

REF = 'D:/Animate/Goal/Bro was so honest.mp4'


def ref_frame(t):
    cap = cv2.VideoCapture(REF)
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * 25)))
    ok, f = cap.read()
    return Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))


def flat(p):
    im = Image.open(p).convert('RGBA')
    bg = Image.new('RGBA', im.size, 'white')
    bg.alpha_composite(im)
    return bg.convert('RGB')


def fit(im, h):
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def main():
    args = sys.argv[1:]
    h = 640
    if '--h' in args:
        i = args.index('--h'); h = int(args[i + 1]); del args[i:i + 2]
    out, pairs = args[0], args[1:]
    tiles = []
    for pr in pairs:
        t, p = pr.split('=', 1)
        a = fit(ref_frame(float(t)), h) if t != '-' else None
        b = fit(flat(p), h)
        w = (a.width if a else 0) + b.width + 6
        tile = Image.new('RGB', (w, h + 18), 'white')
        if a:
            tile.paste(a, (0, 18))
        tile.paste(b, ((a.width + 6) if a else 0, 18))
        d = ImageDraw.Draw(tile)
        d.text((4, 3), 'REF %ss' % t if a else '', fill=(200, 0, 0))
        d.text(((a.width + 10) if a else 4, 3), p.replace('\\', '/').split('/')[-1], fill=(0, 0, 200))
        tiles.append(tile)
    W = sum(t.width for t in tiles) + 8 * (len(tiles) - 1)
    sheet = Image.new('RGB', (W, h + 18), (90, 90, 90))
    x = 0
    for t in tiles:
        sheet.paste(t, (x, 0)); x += t.width + 8
    sheet.save(out)
    print(out, sheet.size)


if __name__ == '__main__':
    main()
