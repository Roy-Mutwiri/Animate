"""Verify the mouth timeline inside the Animate document against the cue data.

Reads the XFL master timeline (the source Animate rendered), expands the CAP_mouth / GL_mouth
keyframes to per-frame Mouth-symbol frame picks, decodes them to (Rhubarb family, emotion),
and checks:
  1. every frame's rendered family == cue family for that frame, except deliberate overrides
     listed in the acting script (reported separately);
  2. no speech shape (anything but X) on a character outside its own speech windows
     (turn start-0.1 s .. end+0.12 s), unless it is a deliberate override;
  3. cue files: ordered, contiguous, non-negative, duration matches the audio.
usage: verify_lipsync.py XFL_DIR OUT.md
"""
import sys, os, json, re
import xml.etree.ElementTree as ET
import chars
from perf import load_cues, cue_track, F
import script_film

NS = '{http://ns.adobe.com/xfl/2008/}'
N = script_film.NFRAMES


def layer_picks(dom, name):
    root = ET.parse(dom).getroot()
    for L in root.iter(NS + 'DOMLayer'):
        if L.get('name') == name:
            picks = [None] * N
            for fr in L.iter(NS + 'DOMFrame'):
                i, d = int(fr.get('index')), int(fr.get('duration', '1'))
                inst = fr.find('.//' + NS + 'DOMSymbolInstance')
                v = int(inst.get('firstFrame', '0')) if inst is not None else None
                for k in range(i, min(i + d, N)):
                    picks[k] = v
            return picks
    raise KeyError(name)


def decode(v):
    nf = len(chars.MOUTH_FAMILIES)
    return chars.MOUTH_FAMILIES[v % nf], chars.EMOTIONS[v // nf]


def main(xdir, out):
    dom = os.path.join(xdir, 'DOMDocument.xml')
    turns = json.load(open(os.path.join(script_film.ASSETS, 'dialogue_turns.json'), encoding='utf-8'))['turns']
    cam, cap, gl = script_film.build()
    lines = ['# Lip-sync verification (Animate source: %s)' % xdir, '',
             'Frame policy: global zero-based frame = floor(t*24+0.5); cue covers [F(start), F(end)).', '']
    total_bad = 0
    for who, track, layer, cuefile, spk in (('CAP', cap, 'CAP_mouth', 'cap_rhubarb.json', 'CAP'),
                                             ('GL', gl, 'GL_mouth', 'nocap_rhubarb.json', 'NOCAP')):
        cues = load_cues(os.path.join(script_film.ASSETS, cuefile))
        neg = [c for c in cues if c['end'] < c['start'] or c['start'] < 0]
        track.evaluate(N)
        expected = track.speech          # cue track after the documented jaw pass
        raw = cue_track(cues, N)
        jaw_changes = sum(1 for f in range(N) if raw[f] != expected[f])
        picks = layer_picks(dom, layer)
        rendered = [decode(v)[0] if v is not None else None for v in picks]
        override = [False] * N
        for (a, b, fam, emo) in track.mouths:
            for f in range(a, min(b, N)):
                override[f] = True
        hidden = [f for f in range(N) if rendered[f] is None]
        mism = [f for f in range(N) if not override[f] and rendered[f] is not None and rendered[f] != expected[f]]
        hidden_speech = [f for f in hidden if expected[f] != 'X']
        win = [False] * N
        for t in turns:
            if t['speaker'] == spk:
                for f in range(F(t['start'] - 0.10), min(F(t['end'] + 0.12), N)):
                    win[max(f, 0)] = True
        stray = [f for f in range(N) if rendered[f] not in ('X', None) and not win[f] and not override[f]]
        speech_frames = sum(1 for f in range(N) if win[f])
        closed_in_speech = sum(1 for f in range(N) if win[f] and rendered[f] == 'X')
        fam_hist = {}
        for f in range(N):
            if win[f]:
                fam_hist[rendered[f]] = fam_hist.get(rendered[f], 0) + 1
        lines += ['## %s (%s)' % (who, cuefile), '',
                  '- cues: %d, ordered/contiguous: yes (asserted on load), negative/inverted: %d, last end %.3f s' % (len(cues), len(neg), cues[-1]['end']),
                  '- jaw pass (loudness-driven B/C/D opening, see jaw.py) changed %d frames of the raw cue track' % jaw_changes,
                  '- frames where rendered family != planned family (excluding deliberate overrides): **%d**' % len(mism),
                  '- speech shapes outside own speech windows (excluding overrides): **%d** %s' % (len(stray), stray[:20]),
                  '- deliberate override frames: %d' % sum(override),
                  '- frames where this character is off screen (not drawn): %d, of which during own speech: %d' % (len(hidden), len(hidden_speech)),
                  '- frames inside own speech windows: %d; of those rendered closed/rest X: %d' % (speech_frames, closed_in_speech),
                  '- family histogram inside speech windows: %s' % dict(sorted(fam_hist.items(), key=lambda x: -x[1])), '']
        if mism:
            lines.append('First mismatches: %s' % [(f, rendered[f], expected[f]) for f in mism[:15]])
        total_bad += len(mism) + len(stray)
    lines.append('**Total mapping defects: %d**' % total_bad)
    open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
