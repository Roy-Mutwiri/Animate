# HonestInterview ProductionFull_v5 — status checkpoint

**State: complete (v5f delivered).** See `FINAL_REPORT.md`. Controller: main session (sole mutator of
Animate 24.0.15, driven by JSFL via `scripts/runjsfl.sh`).

## Rebuild / re-render
```
cd scripts
python -c "from script_film import frames; from scene import build_document; build_document(frames(), '../xfl/honest_<tag>', 'honest_interview_<tag>')"
python -c "from jsfl_render import make; from script_film import NFRAMES; make('../xfl/honest_<tag>/honest_interview_<tag>.xfl', '../frames/full_<tag>', list(range(NFRAMES)), fla='../editable/honest_interview_<tag>.fla', sound='D:/Animate/Sounds/Bro was so honest.mp3')"
./runjsfl.sh ../frames/full_<tag>/_render.jsfl ../frames/full_<tag>/_render_log.txt 1500   # ~7 min
python verify_lipsync.py ../xfl/honest_<tag> ../review/lipsync_verify_<tag>.md
```
then encode with ffmpeg + the original MP3 (see FINAL_REPORT).

## Revision history
| Tag | Result |
|---|---|
| stills_v5a-c | art/design against measured reference |
| rep_v5a | representative section 0-19.4 s, reviewed |
| v5a | full film; independent review -> 14 defects |
| v5b | jaw pass, pucker, override trim |
| v5c | review fixes; regression: window erased (overlapping fills), CAP pop at f22 |
| v5d | window fixed; independent recheck: all 14 fixed/retracted, no new defects |
| v5e | GL single reframed instead of hiding CAP |
| v5f | every drawing part its own drawing object (grin teeth grey fix) — FINAL |

## Next (optional improvements)
Hand-picked mouth variety for remaining 7-9 frame rect holds; ending framing at 69.4 s; bigger five-hand.
