# HonestInterview ProductionFull_v4 Report

## Deliverables

- Full MP4 with original audio: `exports\honest_interview_full_v4.mp4`
- Full PNG sequence: `frames\honest_v4_000000.png` through `frames\honest_v4_001701.png`
- Main editable Animate source: `editable\honest_interview_full_v4_layered_keyed_timeline.fla`
- Preserved one-layer V4 source attempt: `editable\honest_interview_full_v4_keyed_timeline.fla`
- V4 production script: `scripts\build_v4_assets.py`
- Layered Animate JSFL source: `scripts\create_v4_layered_keyed_timeline.jsfl`
- Review sheets:
  - `previews\opening_dialogue_pose_review.png`
  - `previews\full_v4_shot_contact_sheet.png`
  - `previews\sample_v4_review_sheet.png`
- Cue/timeline data: `assets\v4_timeline_and_lipsync.json`

## What Changed From V3

- Regenerated Rhubarb cue JSONs into V4 so their metadata points at V4-local analysis WAVs.
- Switched production frame conversion to the explicit nearest-frame policy: `floor(seconds * 24 + 0.5)`.
- Extended three speech tails that waveform/cue evidence showed were ending early in V3: respondent family block, interviewer "$1,000" line, and final "entrepreneur" line.
- Rebuilt mouth drawings into smaller, lower-face shapes mapped more faithfully to Rhubarb `A/B/C/D/E/F/G/H/X` families.
- Lowered and bent respondent gesture arms so they do not slice through the mouth/eye area in close-ups.
- Created a layered Animate handoff FLA instead of relying on a single-layer V4 source.

## Verification

- `ffprobe` reports `honest_interview_full_v4.mp4` as 1080 x 1920, 24 fps, 1702 video frames, 70.916667s video duration, and 70.889002s audio duration.
- The frame folder contains 1702 PNG frames.
- Animate MCP inspected `honest_interview_full_v4_layered_keyed_timeline.fla` as 1080 x 1920 at 24 fps with 7 populated layers.
- Reference inspection was performed through actual frames from `Bro was so honest.mp4` and by read-only subagent review; no direct real-time listening was available in this environment.

## Remaining Limitations

- The V4 film is improved over V3 but still visibly simpler than the supplied reference, especially in body appeal, chair perspective, and repeated close-up staging.
- Lip sync was corrected from Rhubarb cues, waveform/timing evidence, and rendered frame inspection. I did not perform perceptual ear-reviewed lip-sync playback.
- The layered Animate FLA reports 1703 frames even after two trim attempts; the exported/rendered production deliverables are 1702 frames.
- The final render is generated from the V4 production script and PNG sequence, with an editable Animate source provided as a keyed layered handoff. The FLA is not a frame-perfect reproduction of every rendered pixel.

