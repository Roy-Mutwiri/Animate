"""Every-frame face crops for a phrase, labelled with frame, time, cue family and the word being
spoken (from dialogue_turns.json).  usage: mouth_sheet.py who t0 t1 OUT.png [frames_dir]"""
import sys, os, json
from PIL import Image, ImageDraw
import script_film
from perf import load_cues, cue_track, F
from scene import CAP, GL, Cam
import chars

who, t0, t1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
fdir = sys.argv[5] if len(sys.argv) > 5 else '../frames/full_v5a'
N = script_film.NFRAMES
states = script_film.frames()
turns = json.load(open(os.path.join(script_film.ASSETS, 'dialogue_turns.json'), encoding='utf-8'))['turns']
spk = 'CAP' if who == 'CAP' else 'NOCAP'
cues = cue_track(load_cues(os.path.join(script_film.ASSETS, 'cap_rhubarb.json' if who == 'CAP' else 'nocap_rhubarb.json')), N)


def word_at(t):
    for tr in turns:
        if tr['speaker'] != spk:
            continue
        ws = tr.get('words', [])
        for i, w in enumerate(ws):
            end = ws[i + 1]['start'] if i + 1 < len(ws) else tr['end']
            if w['start'] <= t < end:
                return w['w']
    return ''


tiles = []
for f in range(F(t0), F(t1)):
    st = states[f]
    ch, cs = (CAP, st.cap) if who == 'CAP' else (GL, st.gl)
    hc = chars.head_centre(cs.pose)
    wx, wy = ch.to_world(hc)
    px, py = st.cam.pt(wx, wy)
    r = 80 * st.cam.z * 2.25
    im = Image.open(os.path.join(fdir, 'f%06d.png' % f)).convert('RGB')
    im = im.crop((int(px - r), int(py - r * 0.9), int(px + r), int(py + r * 1.1))).resize((180, 180))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 180, 24], fill=(0, 0, 0))
    d.text((3, 1), 'f%d %.2fs cue %s' % (f, f / 24, cues[f]), fill=(255, 220, 0))
    d.text((3, 12), word_at(f / 24), fill=(120, 255, 120))
    tiles.append(im)
cols = 12
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new('RGB', (cols * 180, rows * 180), 'white')
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % cols) * 180, (i // cols) * 180))
sheet.save(out)
print(out, len(tiles))
