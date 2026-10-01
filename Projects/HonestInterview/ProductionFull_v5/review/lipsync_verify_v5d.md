# Lip-sync verification (Animate source: ../xfl/honest_v5d)

Frame policy: global zero-based frame = floor(t*24+0.5); cue covers [F(start), F(end)).

## CAP (cap_rhubarb.json)

- cues: 212, ordered/contiguous: yes (asserted on load), negative/inverted: 0, last end 70.880 s
- jaw pass (loudness-driven B/C/D opening, see jaw.py) changed 404 frames of the raw cue track
- frames where rendered family != planned family (excluding deliberate overrides): **0**
- speech shapes outside own speech windows (excluding overrides): **0** []
- deliberate override frames: 98
- frames where this character is off screen (not drawn): 572, of which during own speech: 18
- frames inside own speech windows: 920; of those rendered closed/rest X: 117
- family histogram inside speech windows: {'C': 261, 'B': 242, 'X': 117, 'D': 88, 'E': 56, 'A': 54, 'F': 38, None: 34, 'G': 20, 'H': 10}

## GL (nocap_rhubarb.json)

- cues: 130, ordered/contiguous: yes (asserted on load), negative/inverted: 0, last end 70.880 s
- jaw pass (loudness-driven B/C/D opening, see jaw.py) changed 206 frames of the raw cue track
- frames where rendered family != planned family (excluding deliberate overrides): **0**
- speech shapes outside own speech windows (excluding overrides): **0** []
- deliberate override frames: 87
- frames where this character is off screen (not drawn): 1108, of which during own speech: 4
- frames inside own speech windows: 465; of those rendered closed/rest X: 36
- family histogram inside speech windows: {'C': 141, 'B': 109, 'D': 66, 'X': 36, 'F': 36, 'E': 31, 'A': 19, 'G': 13, None: 11, 'H': 3}

**Total mapping defects: 0**
