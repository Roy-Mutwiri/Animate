# Lip-sync verification (Animate source: ../xfl/honest_v5b)

Frame policy: global zero-based frame = floor(t*24+0.5); cue covers [F(start), F(end)).

## CAP (cap_rhubarb.json)

- cues: 212, ordered/contiguous: yes (asserted on load), negative/inverted: 0, last end 70.880 s
- jaw pass (loudness-driven B/C/D opening, see jaw.py) changed 350 frames of the raw cue track
- frames where rendered family != planned family (excluding deliberate overrides): **0**
- speech shapes outside own speech windows (excluding overrides): **0** []
- deliberate override frames: 98
- frames inside own speech windows: 920; of those rendered closed/rest X: 80
- family histogram inside speech windows: {'B': 284, 'C': 266, 'D': 89, 'X': 80, 'E': 66, 'A': 54, 'F': 51, 'G': 20, 'H': 10}

## GL (nocap_rhubarb.json)

- cues: 130, ordered/contiguous: yes (asserted on load), negative/inverted: 0, last end 70.880 s
- jaw pass (loudness-driven B/C/D opening, see jaw.py) changed 194 frames of the raw cue track
- frames where rendered family != planned family (excluding deliberate overrides): **0**
- speech shapes outside own speech windows (excluding overrides): **0** []
- deliberate override frames: 87
- frames inside own speech windows: 465; of those rendered closed/rest X: 41
- family histogram inside speech windows: {'C': 142, 'B': 101, 'D': 67, 'F': 46, 'X': 41, 'E': 31, 'A': 20, 'G': 14, 'H': 3}

**Total mapping defects: 0**
