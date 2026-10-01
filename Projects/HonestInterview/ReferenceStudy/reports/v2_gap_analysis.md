# HonestInterview V2 Gap Analysis

Reviewed rendered outputs:
- `D:\Animate\Projects\HonestInterview\honest_interview_v2.mp4`
- `D:\Animate\Projects\HonestInterview\v2_png_sequence\honest_interview_v2_0062.png`
- `D:\Animate\Projects\HonestInterview\v2_png_sequence\honest_interview_v2_0108.png`
- Comparison image: `v2_gap_side_by_side.jpg`

## Observed Defects

1. Heads appear disconnected from bodies.
   - In V2 frames 62 and 108, both heads float above rectangular torsos with no neck/shoulder continuity.
   - Reference frames around `Bro was so honest.mp4` 2.48s and 4.92s show seated body, neck, torso, chair, and limb integration.
   - Cause: artwork/construction, not export.

2. Torsos are plain rectangles.
   - V2 bodies read as placeholder blocks, not seated characters.
   - Reference torsos are simple but posed: seated hips, shoulders, knees, chair arms, feet.
   - Cause: artwork and rig design.

3. Contours are too heavy and doubled.
   - V2 respondent head has stacked dark contour bands from patch layers.
   - Reference outlines are bold but cleaner; internal detail is lighter.
   - Cause: layering/render correction from the previous black-fill fix.

4. Eye design lacks expressive white/pupil structure.
   - V2 uses dark circular rings that read as hollow eyes at the “Yes” hit.
   - References use large white eye shapes, pupils, eyelids, and gaze changes.
   - Cause: artwork and facial system.

5. Eyebrows are rigid bars.
   - V2 eyebrows float as horizontal slabs and do not interact with eyelids.
   - References use brow/eyelid combinations to show suspicion, surprise, annoyance, and smugness.
   - Cause: artwork and replacement drawing design.

6. Hands and arms have weak silhouettes.
   - V2 hands are mostly circles/lines; microphone contact is unclear.
   - References simplify hands, but the gesture direction remains readable.
   - Cause: artwork and posing.

7. Limited custom expression drawings.
   - V2 mostly swaps mouth/eye parts on the same base construction.
   - References use custom extreme face drawings for shock, shouting, and reaction.
   - Cause: art direction and rig/replacement library.

8. Staging misses the reference reaction cut.
   - V2 keeps a static two-shot through the interruption and objection.
   - The primary reference cuts to interviewer-only reaction around 2.48s and lets the pause breathe.
   - Cause: shot plan and camera/editing, not just character art.

9. Lip-sync is secondary to acting here.
   - V2 used Rhubarb cues, but the facial construction is too weak for the mouth timing to matter.
   - The reference uses mouth shape, eye direction, and held reactions together.
   - Cause: performance design and mouth library.

## Conclusion

V2 should not be polished. The defects are foundational: character construction, facial system, body integration, and shot design. The next pass should start from a new model sheet and shot plan, not from the V2 assets.
