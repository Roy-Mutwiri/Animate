# DesignV3 Character Design Proof Review

## Scope

This pass creates original design proof artwork only. It does not extend the HonestInterview animation and does not replace the production rig.

The design direction follows the reference-study findings: oversized readable heads and eyes, connected neck/shoulder/torso construction, thin flexible limbs, clear seated staging, restrained palette, and sparse backgrounds. The artwork avoids the failed V2 clothing-led direction and keeps the supplied reference imagery out of the original scene deliverable.

## Deliverables

- Finished seated scene still: `DesignV3/exports/scene_still.png`
- Interviewer model sheet: `DesignV3/exports/interviewer_model_sheet.png`
- Respondent model sheet: `DesignV3/exports/respondent_model_sheet.png`
- Opening storyboard panel: `DesignV3/exports/storyboard_01_opening_question.png`
- Instant Yes storyboard panel: `DesignV3/exports/storyboard_02_instant_yes.png`
- Held reaction storyboard panel: `DesignV3/exports/storyboard_03_held_reaction.png`
- Editable SVG sources: `DesignV3/sources/*.svg`
- Generation source: `DesignV3/sources/generate_design_v3.py`
- Internal reference comparison: `DesignV3/reference_comparisons/reference_vs_original_comparison.png`

## Export Inspection

All six primary artwork exports are 1080 x 1920 PNGs with fully opaque alpha.

- `scene_still.png`: 1080 x 1920, alpha 255-255.
- `interviewer_model_sheet.png`: 1080 x 1920, alpha 255-255.
- `respondent_model_sheet.png`: 1080 x 1920, alpha 255-255.
- `storyboard_01_opening_question.png`: 1080 x 1920, alpha 255-255.
- `storyboard_02_instant_yes.png`: 1080 x 1920, alpha 255-255.
- `storyboard_03_held_reaction.png`: 1080 x 1920, alpha 255-255.

The reference comparison sheet is 1600 x 1200 and is kept in `reference_comparisons`, separate from original scene deliverables.

## Design Decisions

Interviewer:
- Taller long-oval head with drooping eyelids and narrow skeptical brows.
- Muted grey-green skin, black cap/hair silhouette, simple pale shirt.
- Rectangular microphone prop integrated into the seated hand.
- Stiff seated posture with chair, hips, shoulders, neck, and torso all present.

Respondent:
- Shorter broad bean-like head with tiny hair tuft.
- Huge white eyes with pupils, cheek marks, and asymmetrical mouth shapes.
- Flexible torso and eager open-hand acting.
- Confident seated pose designed to snap forward on the interruption beat.

Scene:
- Quiet cream/grey room, simple window, floor plane, chairs, and low table.
- Characters share one physical space with visible hip/chair contact and room for hand gestures.

## Visual Issues Fixed During This Pass

- The first proof pass looked too upright and leggy for a seated interview. It was revised with chair seats, hip contact, bent legs, and clearer grounded seating.
- Model-sheet layout was adjusted to prevent label and drawing collisions.
- Heads are now visibly connected to necks, shoulders, torsos, hips, arms, and chairs.
- Eyes now use readable whites, pupils, eyelids, and brows instead of hollow dots or flat bars.

## Remaining Design Risks

- These are editable SVG proof drawings, not Moho production rigs.
- Hands and prop contact are improved but still need more production cleanup before rigging.
- Extreme expressions are custom drawings, but they should be redrawn again inside the final Moho/Animate asset structure.
- The storyboard panels communicate staging and timing beats, not final animation arcs or lip sync.

