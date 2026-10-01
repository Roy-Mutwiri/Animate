# DesignV5 Construction Fix Review

## Scope

This is a versioned correction of DesignV5. Earlier DesignV5 files are preserved. No animation, rigging, or full redesign was created.

## Delivered Files

- Chair plus skeleton construction PNG: `exports/chair_skeleton_construction.png`
- Clean corrected scene PNG: `exports/seated_character_scene_corrected.png`
- Editable construction SVG: `sources/chair_skeleton_construction.svg`
- Editable clean SVG: `sources/seated_character_scene_corrected.svg`
- Generator source: `sources/generate_construction_fix.py`
- Side-by-side reference review: `comparison/reference_side_by_side_review.png`

Both requested storyboard images are 1080 x 1920 opaque PNGs.

## Construction Corrections

- Chair was rebuilt first with distinct backrest, visible horizontal seat cushion, near and far armrests, solid front base, and a simple three-quarter perspective.
- A temporary skeleton establishes head center, shoulders, pelvis, hips, knees, ankles, and feet.
- The pelvis point now visibly sits on the pink cushion plane instead of being hidden behind a broad torso/chair-back shape.
- Thigh segments extend from hips to knees before the lower legs drop to the floor.
- The torso was shortened and narrowed to fit the seated skeleton.
- The clean drawing preserves chair/body overlap: chair back behind the character, far arm partly behind, near arm and front base overlapping the body/legs.
- Forearms are bent and placed onto the armrests.
- Head scale was reduced from the prior DesignV5 pass.
- The expression was changed from friendly to restrained skeptical, with pupils aimed toward the offscreen partner.

## Actual Remaining Differences

- The corrected original is still more front-facing and centered than `ref_2p48_yes_cut.png`, which is more side-on.
- The chair is clearer and more geometric than the rough source chair; this helps construction but is less loose than the reference.
- The head is still slightly larger and cleaner than the source proportion, though reduced from the previous pass.
- The torso remains a light filled shape rather than the reference's almost line-only body. For rigging, keep it narrow and avoid adding clothing bulk.
- The floor and side table remain simplified staging, not a one-to-one match.

## Conclusion

The previous seated-construction failure is corrected enough to demonstrate the pelvis on the cushion, visible thighs to knees, feet meeting the floor, and consistent chair overlap. It should still be treated as a construction proof, not final rig approval.

