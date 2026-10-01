# Lip-sync verification (Animate source: ../xfl/honest_v5a)

Frame policy: global zero-based frame = floor(t*24+0.5); cue covers [F(start), F(end)).

## CAP (cap_rhubarb.json)

- cues: 212, ordered/contiguous: yes (asserted on load), negative/inverted: 0, last end 70.880 s
- frames where rendered family != cue family (excluding deliberate overrides): **0**
- speech shapes outside own speech windows (excluding overrides): **0** []
- deliberate override frames: 98
- frames inside own speech windows: 920; of those rendered closed/rest X: 80
- family histogram inside speech windows: {'B': 453, 'C': 152, 'X': 80, 'E': 66, 'A': 54, 'F': 51, 'D': 34, 'G': 20, 'H': 10}

## GL (nocap_rhubarb.json)

- cues: 130, ordered/contiguous: yes (asserted on load), negative/inverted: 0, last end 70.880 s
- frames where rendered family != cue family (excluding deliberate overrides): **0**
- speech shapes outside own speech windows (excluding overrides): **0** []
- deliberate override frames: 84
- frames inside own speech windows: 465; of those rendered closed/rest X: 42
- family histogram inside speech windows: {'B': 216, 'C': 80, 'F': 46, 'X': 42, 'E': 28, 'A': 20, 'D': 16, 'G': 14, 'H': 3}

**Total mapping defects: 0**
