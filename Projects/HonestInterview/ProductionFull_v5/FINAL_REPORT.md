# HonestInterview — ProductionFull_v5 final report (2026-09-28)

## Deliverables

| Item | Path (under `ProductionFull_v5\`) |
|---|---|
| Final film (1080x1920, 24 fps, 1702 frames, original audio 70.889 s) | `exports\HonestInterview_v5_final.mp4` (= `exports\honest_interview_v5f.mp4`) |
| Editable Animate source — the document Animate rendered the film from | `editable\HonestInterview_v5_final.fla` (= `editable\honest_interview_v5f.fla`) |
| Same document, uncompressed | `xfl\honest_v5f\` |
| Rendered frames (Animate `exportPNG`) | `frames\full_v5f\f000000.png` … `f001701.png` |
| Generator + acting script | `scripts\` (art.py, chars.py, poses.py, perf.py, jaw.py, scene.py, script_film.py, script_film_tail.py, xfl.py) |
| Cue data / dialogue turns | `assets\` |
| Reference comparisons | `previews\ref_vs_v5_final_28beats.png`, `review\cmp_*.png`, `review\v5c_fixes_cmp.png` |
| Lip-sync verification | `review\lipsync_verify_v5f.md` |
| Issue log / status | `ISSUE_LOG.md`, `STATUS.md` |

Earlier revisions (v1–v4, and v5a–v5e intermediates) are preserved untouched.

## What changed from v4 (method)

- v4's picture came from a Python raster generator; its FLA was a "handoff" that did not match the render.
  v5's picture is rendered **by Animate from the delivered document**. The FLA holds 17 layers: room,
  nightstand, both chairs, per-character body / head / eyes / brows / glasses / mouth layers, an iris
  layer and the original MP3 as a stream sound. Faces use graphic-symbol replacement libraries
  (Mouth_Cap / Mouth_Glasses: 9 Rhubarb families × 4 emotions, frame-labelled; Eyes 9; Brows 8)
  picked per keyframe. Holds are real held keyframes (e.g. 232 CAP body drawings across 1702 frames).
- Design was rebuilt from measured reference frames: stick bodies with ~6%-of-head limb lines,
  backwards cap, round glasses, mauve/pink armchairs, orchid nightstand, window, checker floor, the
  reference's two mirrored single set-ups, the opening two-shot move, the three snap push-ins on
  "ten / billion / dollars", and the final push-in plus soft iris-out.
- Acting follows the reference's gesture log and the corrected dialogue turns: instant "Yes" with a
  head jut; the interviewer's expectation collapsing in stages; the cut-in "Listen here" with the arm
  already out; finger / point / push-point; the lounging drape and shrug on "take my grandma";
  "hey hey hey" stop-arm dropped in one frame; folded arms and turn-away on "I don't want to guess";
  five-hand wag; rage tremble on "Five billion?"; a deadpan "Thousand."; the first smile, cocky brows
  and steeple on "entrepreneur".

## Verification actually performed

- **Technical:** ffprobe of the final MP4 (1080x1920, 24/1, 1702 video frames, 70.9167 s video,
  70.889 s audio); alpha scan of all 1702 PNGs (0 frames with transparency); the FLA was reopened in
  Animate and inspected by JSFL (`logs\inspect_v5f.txt`: 1702 frames, 17 layers, library contents,
  stream-sound layer spanning 1702 frames, sample mouth picks).
- **Lip-sync mapping (inside the source document):** `verify_lipsync.py` decoded every mouth
  keyframe of the FLA's XFL: 0 frames differ from the planned cue+jaw track, 0 speech shapes outside
  each speaker's windows. Frame policy: frame = floor(t·24+0.5), cues cover [F(start), F(end)).
- **Frame-level visual review by me:** stills vs reference, representative section 0–19.4 s, 1 s
  overview of every revision, every cut (c-1..c+1), per-frame mouth sheets for three phrases, fixed
  regions, phone size (360 px).
- **Independent reviewer (read-only subagent, no access to my claims):** v5a full review (0.25 s
  overview of the whole film vs reference, every cut ±2 frames, every-frame strips over 10 dialogue /
  gesture passages, full-res crops, phone size) → 14 defects; v5d recheck → all 14 fixed or retracted,
  no new defects. Two later producer-found issues (a pop created by one fix; grin teeth rendering grey
  from overlapping fills) were fixed in v5e/v5f and checked by me, not re-reviewed independently.
- **Reference study:** subagents viewed every distinct drawing of the matching reference
  (0–71 s; held duplicates verified by pixel diff) and the other nine Goal videos at 0.5 s plus
  every-frame passages (`ReviewV5\analysis\`).

## Not done / remaining limitations

- **No listening and no normal-speed playback with sound** was possible in this environment. Sync is
  verified by cue data, speaker loudness, word timings and frame inspection only — not perceptually.
- Mouth articulation is less varied than the reference's hand-picked drawings; a few clenched-teeth
  holds of 7–9 frames remain (11.25–11.62, 21.08–21.29, 10.12–10.42 s).
- The final push-in follows the reference's measured scale table, which has small speed kinks; at
  ~69.4 s my framing is a little tighter than the reference and the steepled hands sit lower in frame.
- The interviewer single is framed ~13 reference px wider than the reference (head x≈267 vs 275–290)
  so the off-screen respondent's foot cannot leak into frame.
- The five-hand is still smaller than the reference's; chair construction and face drawings are
  simplified relative to the reference artist's.
- The acting is authored in the Python script and generated into the FLA. The FLA is fully editable
  in Animate, but hand edits made in the FLA do not flow back into the script.
- Blender and Moho were not used: the reference style is flat 2D in locked set-ups, and the earlier
  Moho test rendered 1280x720 with a demo watermark.
- `D:\Animate\HONEST_INTERVIEW_PRODUCTION_DIRECTIVE.md` does not exist on disk; the directive was
  supplied inline in the session.
