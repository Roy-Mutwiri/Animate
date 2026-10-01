# Requirements and workflow

## Software

| Requirement | Use |
| --- | --- |
| Windows | Original desktop production environment |
| Adobe Animate 2024 | Opens XFL, renders PNG frames, saves editable FLA; existing records identify version 24.0.15 |
| Python 3.11 | Recommended baseline for running the project generators |
| NumPy | Speaker loudness analysis and jaw pass |
| Pillow, OpenCV Python | Comparison images and review utilities |
| FFmpeg / ffprobe on PATH | Encode frames with original audio; inspect output streams |
| Git | Clone the repository; `python scripts/large_assets.py restore` reconstructs oversized bundled assets from checked-in parts |
| Git Bash | Run `runjsfl.sh`, which uses Bash and `cygpath` |
| Rhubarb Lip Sync | Optional cue regeneration; version 1.14.0 is bundled under `Projects/HonestInterview/tools` |

Adobe Animate must be installed, licensed and able to run interactively. Blender and Moho are historical/optional components, not required for the v5 render route. The recorded Moho test had a demo watermark; do not treat it as an approved final-render route. Installing Python requirements does not install these applications.

From the repository root in PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The requirements list is derived from imports in current v5 scripts. Versions are not pinned because the historical production environment has no lockfile; this is not a claim that a clean install was revalidated during the repository upload. Bundled utilities under `Goal` have their own requirements and documentation.

## How the film is built

1. `assets/dialogue_turns.json`, speaker-specific Rhubarb cues and analysis WAVs define speaker windows and mouth timing. The original MP3 remains the output soundtrack.
2. `script_film.py` and `script_film_tail.py` author acting, shot timing and camera movement. `perf.py`, `poses.py` and `jaw.py` assemble character states and refine jaw opening from speaker loudness.
3. `art.py`, `chars.py`, `scene.py` and `xfl.py` generate vector drawing objects, replacement-symbol libraries and held keyframes in an uncompressed Animate XFL document.
4. `jsfl_render.py` generates a JSFL operation. Animate opens the XFL, exports individual PNG frames, attaches the original MP3 as stream sound when requested, and saves the FLA.
5. FFmpeg encodes the PNG sequence with the original MP3. The working film is 1080 x 1920 at 24 fps, with 1702 frames.
6. Source mapping checks, stream inspection and visual/audio review determine readiness. Existing records distinguish completed technical checks from unperformed perceptual checks.

Each `DOMShape` must remain a drawing object: plain shapes or overlapping same-fill paths can merge/cancel inside Animate. Facial poses use graphic-symbol replacement frames selected through `firstFrame`.

## Rebuild into a new revision

Read the current `STATUS.md` and `ISSUE_LOG.md` first. Use a fresh tag such as `v5g`; never overwrite an existing revision. The commands below assume `v5g` does not exist. Run from the scripts directory in **Git Bash**, with the repository's Python environment:

```bash
cd /d/Animate/Projects/HonestInterview/ProductionFull_v5/scripts
source /d/Animate/.venv/Scripts/activate
python -c "from script_film import frames; from scene import build_document; build_document(frames(), '../xfl/honest_v5g', 'honest_interview_v5g')"
python -c "from jsfl_render import make; from script_film import NFRAMES; make('../xfl/honest_v5g/honest_interview_v5g.xfl', '../frames/full_v5g', list(range(NFRAMES)), fla='../editable/honest_interview_v5g.fla', sound='D:/Animate/Sounds/Bro was so honest.mp3')"
bash runjsfl.sh ../frames/full_v5g/_render.jsfl ../frames/full_v5g/_render_log.txt 1500
```

`runjsfl.sh` expects Animate at `C:/Program Files/Adobe/Adobe Animate 2024/Animate.exe`; adjust that path for another installation. Generated JSFL contains absolute paths and should be regenerated on a relocated checkout. The convenience `build_full.py` generates a render job but does not pass the original audio argument; use the explicit commands above for a source containing stream sound.

The runner waits for a log, not the application process. Read `_render_log.txt` for errors and successful frame export/FLA saving. `DONE` alone is insufficient because the script also logs caught errors. After a timeout, inspect Animate's state and modal dialogs before retrying. Do not close documents belonging to other work.

Encode from the same directory after confirming all frames were exported:

```bash
ffmpeg -n -framerate 24 -start_number 0 -i ../frames/full_v5g/f%06d.png -i '/d/Animate/Sounds/Bro was so honest.mp3' -map 0:v:0 -map 1:a:0 -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart ../exports/honest_interview_v5g.mp4
python verify_lipsync.py ../xfl/honest_v5g ../review/lipsync_verify_v5g.md
ffprobe -v error -count_frames -show_streams -show_format ../exports/honest_interview_v5g.mp4
```

The encode command is a documented rebuild recipe, not a claim of byte-identical reproduction of the archived MP4. It does not time-stretch the audio or shorten the frame sequence. `-n` prevents replacing an existing export.

## Review and handoff

Reopen the saved FLA in Animate and verify timeline length, layers, symbol replacement choices and stream sound. Compare rendered frames with actual `Goal` media. The reference measurements are in `ReviewV5/analysis/ref_shots_00_36.md` and `ref_shots_36_71.md`. Check cuts, gestures, mouth closures, frame transparency, framing and the final iris. Perform normal-speed playback with sound and listening when capability permits; source cue mapping alone does not establish perceptual lip sync.

Update the issue log with shot/timecode, defect, correction and recheck result, then update status and the final report with the precise checks performed and any remaining limitations. Follow the project skills in `.agents/skills` for production work.
