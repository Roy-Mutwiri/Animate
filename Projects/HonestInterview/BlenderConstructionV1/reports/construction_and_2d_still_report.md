# Blender Construction And 2D Still Report

## Scope

This pass preserves all previous DesignV versions. It does not animate and does not continue iterating the current chair SVG by eye.

## Blender Construction

Editable Blender file:

- `D:\Animate\Projects\HonestInterview\BlenderConstructionV1\honest_interview_construction_v1.blend`

Rendered construction views:

- Camera-view construction image: `D:\Animate\Projects\HonestInterview\BlenderConstructionV1\camera_construction_chosen.png`
- Side-view pose diagnostic: `D:\Animate\Projects\HonestInterview\BlenderConstructionV1\side_pose_diagnostic.png`

Both renders are 1080 x 1920 opaque PNGs.

What Blender performed:

- Built the armchair from separate solids: seat cushion, backrest, two armrests, and base.
- Built the pose mannequin from a sphere head, torso block, joint spheres, and thin limb cylinders.
- Set the pelvis on the cushion, thighs forward, knees bent, shins downward, and feet on the floor.
- Bent elbows and placed forearms on the armrests.
- Turned the chair/mannequin about 30 degrees toward the offscreen partner.
- Compared mild perspective and orthographic framing. Orthographic was kept because it better matched the flat spatial relationships of the reference; mild perspective pushed the chair too aggressively toward camera.
- Created a side diagnostic render with blocking chair pieces hidden only for that diagnostic, so the seat/pelvis/thigh/knee relationship is visible.

Inspection notes:

- Backrest remains below the head, matching the reference relationship.
- The pelvis is supported by the cushion rather than floating.
- Feet contact the floor.
- Forearms contact the armrests.
- Remaining difference: the camera-view construction is still more front-facing and symmetrical than `ref_2p48_yes_cut.png`, which is a looser side-facing seated pose.

## Adobe Animate Step

Animate file:

- `D:\Animate\Projects\HonestInterview\BlenderConstructionV1\animate_still\honest_interview_clean_still_from_blender_underlay.fla`

What Animate performed:

- Created a new 1080 x 1920, 24 fps document.
- Imported the Blender camera render as an underlay.
- Created named layers for chair and character parts.
- Saved the FLA successfully.

Animate limitation observed:

- Animate's PNG export produced `honest_interview_clean_still_from_blender_underlay.png`, but the exported image still showed the Blender underlay instead of the intended clean vector drawing, even after the underlay layer was hidden and locked in the timeline. I am preserving that file as evidence of the failed export, not presenting it as the final cartoon still.

## Clean 2D Still

Clean final 2D still:

- `D:\Animate\Projects\HonestInterview\BlenderConstructionV1\animate_still\honest_interview_clean_2d_still.png`

Editable source:

- `D:\Animate\Projects\HonestInterview\BlenderConstructionV1\animate_still\honest_interview_clean_2d_still.svg`

Generator:

- `D:\Animate\Projects\HonestInterview\BlenderConstructionV1\animate_still\generate_clean_2d_still.py`

What produced the final still:

- The final clean PNG was rendered from the editable grouped SVG using Microsoft Edge headless.
- The SVG uses the Blender camera render as the locked underlay/reference coordinate source.
- Character and chair parts are separated into named SVG groups for later Moho rig planning.

Inspection notes:

- The clean still keeps the simple visual direction: compact head, direct torso/head connection, thin limbs, simple hands, restrained skeptical expression, and flat colors.
- Legs remain visible over the chair base; the base no longer acts as a foreground panel swallowing the shins.
- Remaining difference: the clean still is still more front-facing and centered than the reference frame. It should be treated as a pose/perspective aid translated into 2D, not a final approved character design.

