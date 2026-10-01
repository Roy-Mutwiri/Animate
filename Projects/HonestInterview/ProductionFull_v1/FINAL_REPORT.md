# HonestInterview Full V1 Report

## Deliverables

- Full-length MP4 with supplied audio: `exports\honest_interview_full_v1.mp4`
- Editable Animate source asset: `editable\honest_interview_full_v1_animate_asset.fla`
- Copied starting FLA: `editable\honest_interview_full_v1_source_bodyfix.fla`
- Editable production renderer: `scripts\render_full_animation.py`
- Shot/dialogue timeline: `assets\full_timeline.json`
- Render sequence: `frames\honest_full_000000.png` through `honest_full_001701.png`
- Shot contact sheet: `review\honest_interview_full_shot_contact_sheet.png`
- Timing check sheet: `review\honest_interview_full_timing_check_sheet.png`
- Decoded MP4 check sheet: `review\mp4_checks\mp4_decoded_check_sheet.png`

## Verification

- Source audio duration: 70.889070 seconds.
- Production frame count: 1,702 frames at 24 fps.
- Final video stream: 1080 x 1920, 24 fps, 1,702 frames, 70.916667 seconds.
- Final audio stream: starts at 0.000s, duration 70.889002 seconds.
- Video duration exceeds audio by about 0.028s, which is the expected rounding to a whole 24 fps frame.
- All PNG frames are present and 1080 x 1920.
- Frame-diff checks confirmed the sequence is not frozen.
- Decoded MP4 frames were checked at the start, major cuts, late dialogue, and ending.

## Production Notes

- The full animation uses the simplified line-body direction from the reference study: seated characters, sparse room, armchairs, large readable eyes, held reactions, and cut-driven comedy timing.
- Speaking is separated by character. Listener mouths stay closed or restrained during the other character's lines.
- The first interruption follows the verified structure: setup two-shot, abrupt respondent close-up for "Yes", held silence, then interviewer objection.
- Later dialogue alternates close-ups and two-shot pauses to keep the long audio readable.

## Limitations

- No local Whisper or Rhubarb tool was available, so lip sync is approximate and timing-based, not phoneme-perfect.
- Moho was not used because previous checks found demo/watermark and dimension issues.
- The full render is generated from the editable production Python project using the Animate-derived bodyfix design. The FLA is an editable source asset, not a full 1,702-frame keyed Animate timeline.
- Artwork is coherent and complete for a full pass, but still simpler than the strongest references: linework, hands, and mouth shapes can be polished further in a future revision.
