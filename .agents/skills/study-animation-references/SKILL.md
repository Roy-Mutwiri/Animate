---
name: study-animation-references
description: Study the HonestInterview Goal reference clips and diagnose reference mismatch — framing, construction, palette, gesture timing, expressions, mouth sets, holds, camera moves. Use whenever inspecting D:\Animate\Goal, comparing a render to the reference, choosing acting examples, or measuring proportions, even for a single frame question.
---

# Study Animation References

## Inputs

- `D:\Animate\Goal` (the key clip `Bro was so honest.mp4` animates the SAME audio, 25 fps, offset ~0).
- Existing measured specs: `ReviewV5\analysis\ref_shots_00_36.md`, `ref_shots_36_71.md`.

## Procedure

1. Open the media. Filename lists, transcripts, reports and contact sheets are navigation aids.
2. Efficient full coverage: pixel-diff consecutive frames to find distinct drawings, then view every
   distinct drawing in labelled sheets (`ReviewV5\sheet.py VIDEO OUT COLS W t0:t1:step`). Report which
   frames were viewed vs verified as held duplicates by diff.
3. Measure from full-resolution, gridded zoom crops (2x with source-pixel grid) — not from thumbnails.
   Earlier estimates were wrong until measured (limb line 6-7 px, not 3; eye centres at y-13 not y-20;
   cap sits on top of the skull; lenses low on the face).
4. Work in source seconds; convert to 24 fps production frames once.
5. Compare reference and production at the same timestamp and display height, never stretched
   (`ProductionFull_v5\scripts\compare.py OUT ref_t=prod.png ...`).
6. Feed findings straight into production: each note should change a drawing, pose, timing or camera.

## Key facts already established (verify if in doubt)

- Two locked mirrored single set-ups + opening two-shot move (0.08-1.48 s), stepped push-in snaps on
  "ten / billion / dollars" (16.52, 17.40, 18.24), final push-in from 67.52 s about a point above the
  brim, iris-out centred on frame from ~69.1 s with a very soft purple edge.
- Bodies hold for seconds; gestures are 2-4 drawings then holds; faces are instant replacement swaps.

## Failure cases

- If media cannot be decoded or audio cannot be heard, state the exact limitation.
- Do not infer speaker identity from filenames; use mouths in the reference plus voice evidence.
