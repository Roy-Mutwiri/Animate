"""Jaw pass: refine Rhubarb's lip-shape track with the speaker's own loudness envelope.

Rhubarb (pocketSphinx + transcript) labels many vowel frames 'B' (teeth nearly closed), which held
for 6-10 frames reads as a frozen mouth.  Jaw opening is reviewed separately from lip shape:
  * per-frame level (dB) from the speaker-isolated analysis WAV (other speaker silenced, original
    timing), measured over a 1/24 s window centred on the frame time f/24;
  * level relative to the phrase-local peak (max over +-0.5 s) decides the jaw:
        within 4 dB of the peak -> big open (D, or C for already-open cues)
        within 11 dB            -> open (C)
        below                   -> near-closed (B)
  * only the open/teeth families B/C/D are re-opened or closed.  Closures (A), rounds (E, F),
    F/V (G), tongue (H) and rest (X) keep the recogniser's label, so contacts are preserved;
  * a syllable dip (a local minimum >= 3 dB below both neighbours' peaks) inside an open run
    is closed to B, so vowels separate.
"""
import wave
import numpy as np


def frame_db(wav_path, nframes, fps=24):
    w = wave.open(wav_path)
    sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    h = int(sr / (2 * fps))
    db = np.full(nframes, -120.0)
    for f in range(nframes):
        c = int(round(f / fps * sr))
        seg = x[max(0, c - h):c + h]
        if len(seg):
            db[f] = 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-6)
    return db


def jaw_pass(track, db, win=12):
    out = list(track)
    n = len(track)
    changed = 0
    for f in range(n):
        v = track[f]
        if v not in ('X', 'A') and db[f] < -50.0:
            out[f] = 'X'
            changed += 1
            continue
        if v not in ('B', 'C', 'D'):
            continue
        lo, hi = max(0, f - win), min(n, f + win + 1)
        rel = db[f] - db[lo:hi].max()
        if rel > -4.0:
            new = 'D' if v in ('C', 'D') else 'C'
            if v == 'B' and db[f] > -22:
                new = 'D' if rel > -1.5 else 'C'
        elif rel > -11.0:
            new = 'C' if v != 'D' else 'D'
        else:
            new = 'B'
        # syllable dip: local minimum clearly below the surrounding peaks -> near-closed
        if 1 <= f < n - 1 and new in ('C', 'D'):
            l = db[max(0, f - 3):f].max() if f > 0 else db[f]
            r = db[f + 1:min(n, f + 4)].max()
            if db[f] <= db[f - 1] and db[f] <= db[f + 1] and db[f] < l - 3 and db[f] < r - 3:
                new = 'B'
        if new != v:
            changed += 1
        out[f] = new
    changed += _relax_long_holds(out, db)
    return out, changed


def _relax_long_holds(out, db, onset=3):
    """Long unchanged holds read as a frozen mouth.  After a short onset:
      * a quiet sustained B (nasal/hum, >= 9 frames, >= 6 dB under the phrase peak) relaxes to rest X;
      * a pucker/O held >= 7 frames (e.g. the hissed 's' tail of "yes") becomes teeth B."""
    n, changed, f = len(out), 0, 0
    while f < n:
        g = f
        while g < n and out[g] == out[f]:
            g += 1
        v, L = out[f], g - f
        if v == 'B' and L >= 9:
            peak = db[max(0, f - 12):min(n, g + 12)].max()
            if db[f:g].max() < peak - 6:
                for k in range(f + onset, g):
                    out[k] = 'X'; changed += 1
        elif v in ('E', 'F') and L >= 7:
            for k in range(f + onset, g):
                out[k] = 'B'; changed += 1
        f = g
    return changed
