# HonestInterview ProductionFull_v3 Report

## Deliverables

- Corrected full MP4: `exports\honest_interview_full_v3.mp4`
- Layered keyed Animate timeline: `editable\honest_interview_full_v3_layered_keyed_timeline.fla`
- Editable production script: `scripts\build_v3_assets.py`
- Full render sequence: `frames\honest_v3_000000.png` through `honest_v3_001701.png`
- V2-to-V3 comparison: `previews\reference_v2_v3_comparison.png`
- Opening dialogue review: `previews\opening_dialogue_pose_review.png`
- Full shot contact sheet: `previews\full_v3_shot_contact_sheet.png`
- Issue log: `ISSUE_LOG.md`

## Repairs From V2

- Chair/body overlap:
  - Split close-up chair drawing into back/seat/front-arm passes.
  - Lowered foreground armrest so it no longer hides the torso and shoulder acting.
  - Repositioned pelvis/thigh starts so legs read as emerging from the seated body/cushion.

- Limb performance:
  - Added clearer elbow, wrist, and endpoint changes for pointing and objecting gestures.
  - Kept head/body/shoulder connections stable in the close-up pose system.
  - Preserved planted feet and seated contact in the rendered shots.

- Lip sync:
  - Reused full-length speaker-isolated Rhubarb cues from V2.
  - Added cue cleanup so phrase starts/ends close the mouth and very short chatter cues are suppressed.
  - Mouth drawings remain in the lower face and no longer overlap the neck junction.

- Editable source:
  - V2's FLA was verified as one flattened keyed vector layer.
  - V3 creates a 1702-frame Animate FLA with 7 populated editable vector layers:
    `Mouth`, `Brows_Eyes_Head`, `Arms`, `Body_Legs`, `Chair_Foreground`, `Chair_Back_Seat`, `Background`.
  - Animate MCP inspection verified 26 timed keys per layer.

## Verification

- Final MP4: 1080 x 1920, 24 fps, 1702 frames.
- Audio stream starts at 0.000s and remains 70.889002s.
- Render sequence contains 1702 PNG frames.
- Opening dialogue pose review and V2/V3 comparison were visually inspected after the final armrest fix.

## Remaining Honest Notes

- I could not perform true human real-time listening/playback inside the tools, so lip sync is corrected using Rhubarb, phrase timing, frame inspection, and silence/line-boundary cleanup, not ear-reviewed phoneme perfection.
- The design remains intentionally simple and line-bodied. The V3 repair improves readability and overlap, but it is not indistinguishable from the supplied reference animation.
