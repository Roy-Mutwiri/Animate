---
name: operate-animation-pipeline
description: Operate the HonestInterview Animate/Blender/Moho pipeline — generating editable Animate documents, driving Animate with JSFL, rendering, attaching audio, exports, recovery and checkpoints. Use whenever building, rendering or repairing HonestInterview shot/master timelines, running JSFL against Animate, encoding the film, or deciding which app owns a component, even if the request only says "re-render" or "export".
---

# Operate Animation Pipeline

## Inputs

- Newest production revision (read its `STATUS.md` / `ISSUE_LOG.md` first; v5+: `Projects\HonestInterview\ProductionFull_v5`).
- Original audio `D:\Animate\Sounds\Bro was so honest.mp3` (70.889 s -> 1702 frames at 24 fps).

## Validated route (v5)

1. **Generate, don't hand-paint pixels.** Python writes an uncompressed Animate document (XFL):
   vector drawing objects, graphic-symbol libraries (heads, eyes, brows, glasses, mouths) whose
   internal frames are replacement drawings chosen by `firstFrame`, and keyed layers where a
   repeated state becomes a held keyframe. Why: the render source and the editable source are then
   the same document, so "handoff FLA" mismatches (v1-v4) cannot happen.
2. **Every `DOMShape` must be `isDrawingObject="true"`.** Plain shapes in one frame merge and their
   fill-style tables collide (heads rendered yellow, furniture pink in stills_v5a).
3. **Drive the running Animate with JSFL**: pass a `.jsfl` path to `Animate.exe`; the script runs in
   the open instance and writes a log with `FLfile.write`. Wait for the log file, not for the process.
   `scripts/runjsfl.sh script.jsfl log.txt timeout` does this. Holes in fills (iris) need a single
   keyhole polygon with opposite winding.
4. **Render in Animate**: open XFL -> `exportPNG(uri, true, true)` per frame -> `saveDocument` to FLA.
   Measured cost: ~0.27 s/frame at 1080x1920 (1702 frames ~ 7.5 min). Then mux with ffmpeg using the
   original MP3 (no time-stretch). Attach the MP3 as a stream sound in the FLA with
   `importFile` + `soundLibraryItem`/`soundSync="stream"`; verify the layer span equals the timeline.
5. **Verify before claiming**: reopen/parse the saved document; check frame count, layer list,
   mouth-layer picks (`scripts/verify_lipsync.py`), and decoded MP4 stream durations.

## Rules that still apply

- Preserve prior revisions; new tag per substantial change (`build_full.py v5b`). Never overwrite the MP3,
  `D:\Animate\Goal`, or another revision's outputs.
- One controller mutates Animate/Blender/Moho. Subagents are read-only reviewers/analysts.
- Many unsaved "Untitled" documents may be open in Animate — never close documents you did not open.
- Blender/Moho are optional; Moho (v4 check) rendered 1280x720 with Demo watermark lines — do not use
  it for finals unless its licence/export is re-verified.
- Keep `STATUS.md` current: active source, completed ranges, next action.

## Failure cases

- Log file never appears: inspect Animate's window title/process and any modal dialog before retrying;
  do not relaunch the same mutation blindly.
- If the heredoc/shell mangles backslashes or apostrophes, write scripts with a file tool instead.
