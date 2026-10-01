# DesignV5 Reference Correction And Still Review

## Corrected Reference Interpretation

The newly inspected source frames override earlier briefs that pushed the design toward broad torsos, detached neck blocks, bulky legs, microphones, and elaborate finger construction.

Neutral source identifiers:

- Cap-wearing character: visible in `ref_2p48_yes_cut.png`, `ref_3p04_freeze.png`, and `ref_7p68_point_hold.png`.
- No-cap character: visible in `ref_4p92_object.png`.

Source timing and audio:

- Source video: `D:\Animate\Goal\Bro was so honest.mp4`, 480 x 850, 25 fps, 71.000s video, 70.960s audio.
- Production soundtrack: `D:\Animate\Sounds\Bro was so honest.mp3`, 70.889s.
- Audio offset check over the opening measured MP3-minus-source-video at about +0.001s. That is effectively zero for dialogue placement, but source frame numbers are still 25 fps and must not be transferred directly to the 24 fps production timeline.

Visible/audio-supported opening read:

- 0.00-2.44s source time: no-cap character visibly speaks in the two-shot while the cap-wearing character listens.
- 2.48s source time, frame 62: cut to cap-wearing character. This is a picture cut, not automatically a dialogue boundary.
- About 2.56-2.92s source time: cap-wearing character mouth opens, aligning with "Yes" in the source audio.
- 2.92-4.85s source time: silence detected in source audio; cap-wearing character holds/reconfigures reaction.
- About 4.85-7.74s source time: source audio resumes; no-cap character is visible speaking.
- 7.68s source time: cap-wearing character appears in pointed hold with extended arm.

## DesignV5 Still

Delivered:

- Clean PNG: `DesignV5/exports/seated_character_scene.png`
- Editable SVG: `DesignV5/sources/seated_character_scene.svg`
- Generator source: `DesignV5/sources/generate_design_v5.py`
- Reference comparison: `DesignV5/reference_comparison/reference_comparison.png`
- Editable comparison SVG: `DesignV5/reference_comparison/reference_comparison.svg`

Measured still output:

- `seated_character_scene.png`: 1080 x 1920, opaque PNG.

## Drawing Choices

- No microphone was added because none is visible in the supplied reference frames.
- The character uses a compact rounded head and a modest dark cap/hair accessory to remain distinguishable without adding clothing complexity.
- The torso is a narrow tapered form meeting the head directly, without a detached neck block.
- Limbs are thin black lines with visible elbow/knee bends.
- Hands are simple black endpoints because this still does not require a specific hand pose.
- The opaque armchair is drawn behind the body with clear back, arms, cushion, front apron, and body overlap.
- The pelvis sits on the cushion; thighs lead to knees; feet meet the floor.
- Facial features are restrained, with gaze aimed toward an offscreen partner.

## Comparison Observations

Against `ref_2p48_yes_cut.png`:

- Similarities: compact head-to-chair scale, simple facial construction, black line limbs, sparse room, visible chair/body overlap, seated legs reaching the floor.
- Differences: the original still is more front-facing and uses a new cap/hair silhouette rather than copying the brim shape. The chair perspective is simplified but intentionally opaque.
- Remaining risk: the torso is still more visibly filled than the source's almost-line-only body. For production, Moho rig setup should keep this torso slim and should avoid adding clothing bulk.

## Pipeline Roles Retained

- Moho remains the primary character-performance app.
- Adobe Animate remains for replacement drawings, accents, and smears where needed.
- Blender remains for environment/compositing/audio assembly.

