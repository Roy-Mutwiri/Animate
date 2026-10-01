---
name: review-animation-deliverables
description: Review HonestInterview renders and sources for reference fit, acting, lip sync, editability, provenance and technical delivery before any completion claim. Use whenever a render, export, FLA or final report is being checked, compared with the reference, or described as finished.
---

# Review Animation Deliverables

## Inputs

Latest MP4, frame PNGs, the Animate source (XFL/FLA), verification reports, reference clip and specs.

## Procedure

1. Technical and artistic checks are separate. Technical: ffprobe the MP4 (1080x1920, 24 fps,
   1702 frames, audio 70.889 s), frame folder count, opaque frames, FLA reopens with expected layers,
   sound layer spans the timeline.
2. Artistic: 1 s overview sheets of the whole film beside the reference at the same timestamps; frame
   level at every cut; every-frame passes for gestures; phrase sheets for lip sync at beginning,
   middle and end; full-res crops of faces/hands/contacts; phone-size (~360 px wide) viewing.
3. Use an independent read-only reviewer that receives the render and reference but not the
   producer's claims; producer then verifies each reported defect before fixing.
4. Log every issue: timecode/frame, defect, evidence image, cause, repair, recheck result
   (`ProductionFull_v5\ISSUE_LOG.md`). No numeric quality grades.
5. If the same defect survives a pass, change the method (redraw, new drawing, new analysis layer).

## Outputs

Issue log, verification reports, comparison images, final report with honest coverage and limits.

## Failure cases

- Do not claim listening, normal-speed playback, perceptual lip-sync approval or artistic approval
  that did not happen. Say exactly what was inspected.
- Do not delete disclosed limitations to make a report look finished.
