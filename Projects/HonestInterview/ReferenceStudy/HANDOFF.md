# HonestInterview Reference Study Handoff

## Status

Do not extend or polish `honest_interview_v2.fla`. V2 failed the visual target.

The reference study folder is:
`D:\Animate\Projects\HonestInterview\ReferenceStudy`

## Key Artifacts

- Inventory: `reports/reference_inventory.csv`
- Review coverage manifest: `reports/review_manifest.csv`
- Audio transcript pass: `reports/audio_transcripts.json`
- Visual style guide: `reports/visual_style_guide.md`
- V2 gap analysis: `reports/v2_gap_analysis.md`
- Side-by-side V2/reference image: `reports/v2_gap_side_by_side.jpg`
- Pipeline/interchange findings: `reports/pipeline_and_interchange.md`
- Redesign brief and shot plan: `reports/redesign_brief_and_shot_plan.md`
- Extraction script: `reference_study.py`
- Primary consecutive frame sheets:
  `contact_sheets/Bro_was_so_honest__frames_00000_00199_step1`
- DesignV3 proof folder:
  `D:\Animate\Projects\HonestInterview\DesignV3`
- DesignV3 proof review:
  `DesignV3\reports\design_proof_review.md`
- DesignV3 pipeline repair report:
  `DesignV3\reports\pipeline_repair_report.md`
- DesignV3 coverage update:
  `DesignV3\reports\coverage_update.md`
- DesignV3 next redesign brief:
  `DesignV3\reports\next_redesign_brief.md`
- DesignV5 focused correction:
  `D:\Animate\Projects\HonestInterview\DesignV5`
- DesignV5 reference correction and review:
  `DesignV5\reports\reference_correction_and_review.md`

## Strongest Findings

1. The primary reference opening is not a static two-shot. Around 2.48s it cuts to the interviewer reaction and holds the pause.
2. The joke depends on held reaction timing, gaze, eyelids, and custom facial drawings more than constant motion.
3. V2 fails structurally: floating heads, rectangular torsos, weak hands/arms, rigid eyebrows, hollow-looking eyes, doubled outlines, and no seated body integration.
4. The next design must be rebuilt from seated characters with necks, shoulders, chairs, and readable eyes before lip sync or animation polish.
5. Moho should be the target character-performance app, but its export template is not production-ready yet. A real Lua-created Moho pass rendered, but it came out 1280x720 with Demo Mode watermark lines.
6. DesignV3 and DesignV4 are preserved but not approved for rigging. Do not reuse their broad torso, detached neck-block, bulky leg, microphone, or circular finger-bump construction.
7. The newly inspected reference frames override conflicting earlier briefs. Use compact rounded heads, narrow tapered torsos meeting the head directly, thin black line limbs, simple hand endpoints unless action requires detail, and opaque armchairs with clear seated contact.
8. Corrected neutral identifiers: `ref_2p48_yes_cut.png` and `ref_3p04_freeze.png` show the cap-wearing character; `ref_4p92_object.png` shows the no-cap character; `ref_7p68_point_hold.png` shows the cap-wearing character extending an arm.
9. Source video timing and production soundtrack timing must stay separate. The source is 25 fps; production is 24 fps. Opening audio offset check measured MP3-minus-source-video at about +0.001s, effectively zero for dialogue placement, but source frame numbers still need conversion.

## Actual Coverage

Completed:
- Full metadata inventory for every MP4 in `D:\Animate\Goal`.
- One-second overview sheets for every reference video.
- Consecutive source-frame visual inspection of `Bro was so honest.mp4` from 0.00-8.00s, frames 0-199.
- Consecutive source-frame contact-sheet inspection of `That is why!.mp4` from 0.00-6.33s, frames 0-152.
- Visual overview review of every reference video.
- Selected style-frame review across secondary references.
- Machine transcription pass for all videos.
- V2 rendered-frame audit using actual exported frames and comparison image.
- Disposable interchange test for Animate transparent PNG plus Moho-generated PNG into Blender composite.
- DesignV3 character design proof with scene still, two model sheets, three storyboard panels, editable SVG sources, and internal reference comparison.
- Pipeline repair retest using known RGBA patches and a Moho/Animate/Blender composite.
- DesignV5 focused correction with one clean seated-character still, editable SVG source, and separate reference comparison.
- Reference study corrected to use neutral cap-wearing/no-cap identifiers and source-video timestamps before production frame conversion.

Not completed:
- Full consecutive frame-by-frame visual inspection of every long reference video.
- Production-ready Moho transparent render/export validation. Command-line Lua did render after a delayed output check, but size/license/watermark issues remain; MCP screenshot timed out once and was not retried.
- Moho portrait 1080 x 1920 project/template automation. The currently preserved Moho test render is 1280 x 720 and has visible Demo Mode watermark lines.
- Human real-time audio playback review inside the environment.

## Next Concrete Task

Do not create a new animated pilot yet.

Next, review the DesignV5 still before rigging:
- Use `DesignV5\exports\seated_character_scene.png` and `DesignV5\reference_comparison\reference_comparison.png`.
- If approved, build Moho-ready character structure from the DesignV5 simplified construction, not V1-V4.
- Define Animate replacement drawings only where a pose needs custom face/hand/accent art.
- Use Blender as the environment/composite/audio owner.
- Resolve Moho license/export watermark and portrait template dimensions before relying on Moho renders for production.

Production animation should resume only after the simplified DesignV5 construction is approved and visually checked against the corrected reference frame interpretation.

## BlenderConstructionV4 Handoff Update

Current connected-asset handoff folder:
`D:\Animate\Projects\HonestInterview\BlenderConstructionV4`

Blender work completed and preserved:
- `honest_interview_construction_v4.blend`
- `camera_construction_v4.png`
- `side_pose_diagnostic_v4.png`
- `side_pose_diagnostic_near_arm_hidden_v4.png`
- `camera_landmarks_v4.json`
- `chair_projected_faces_v4.json`

Generated-art work completed:
- `generate_projected_2d_art.py` was corrected to read projected chair faces from `chair_projected_faces_v4.json` instead of inventing armrest/base depth using fixed pixel offsets.
- `Chair_Base` is now drawn before `Character_Legs`, so it no longer obscures the leg construction.
- The torso silhouette now reaches the underside of the head instead of starting below the shoulders.
- SVG output uses real newline separators rather than literal backslash-n strings.
- Corrected outputs:
  - `projected_2d_artwork_v4.svg`
  - `projected_2d_artwork_v4.png`
  - `projection_alignment_comparison_v4.svg`
  - `projection_alignment_comparison_v4.png`

Animate status:
- Animate is running and Windows reports the process as responsive.
- The Animate CEP panel process is running and connected to the Node proxy.
- Node proxy is running on port 3099 and has established localhost connections.
- Python MCP client, proxy, and CEP panel all agree on port 3099.
- Direct Socket.IO probe reaches the proxy and the CEP panel receives `getDocuments`, but no packet response returns.
- CEP debugger test with `CSInterface.evalScript("1+1")` stays pending, confirming the current failure is between the CEP panel and Animate JSFL execution.
- Visible modal dialog found in Animate: `Import honest_interview_clean_2d_still.svg to Stage`.
- Active Animate document title: `Untitled-14*`, so there may be unsaved work.
- Do not retry Animate import/mutation until the modal dialog is cleared. The user should either complete or cancel that import dialog in Animate, then reconnect/verify the MCP panel before continuing the small editable-head import test.

Follow-up correction completed:
- The pending Animate import dialog `Import honest_interview_clean_2d_still.svg to Stage` was cancelled with Escape after confirming it was the active modal.
- `get_documents` succeeded afterward, confirming Animate/MCP communication recovered.
- `honest_interview_construction_v4.blend` was corrected in place after saving a backup at `BlenderConstructionV4\honest_interview_construction_v4_pre_base_fix.blend`.
- Chair base was raised in Blender so its top is `z=0.765`, directly under the seat cushion bottom at `z=0.77`; this fixes the visible disconnected-base gap from the projected artwork source rather than hiding it in SVG.
- Regenerated from corrected Blender camera:
  - `BlenderConstructionV4\camera_construction_v4.png`
  - `BlenderConstructionV4\camera_landmarks_v4.json`
  - `BlenderConstructionV4\chair_projected_faces_v4.json`
  - `BlenderConstructionV4\projected_2d_artwork_v4.png`
  - `BlenderConstructionV4\projection_alignment_comparison_v4.png`
- Added unobstructed side diagnostic:
  - `BlenderConstructionV4\side_pose_diagnostic_unobstructed_wire_v4.png`
  - Both armrests and opaque chair solids were hidden only temporarily; chair wire outlines were temporary and removed; normal scene visibility was restored.
- Corrected `generate_projected_2d_art.py` so shoulder attachment points match the torso silhouette and near/far wrist/hand overlap is handled separately instead of drawing every hand above the chair.
- Small Animate editable-import proof completed:
  - Source SVG: `BlenderConstructionV4\animate_head_eyes_import_test.svg`
  - Saved FLA: `BlenderConstructionV4\animate_import_test\head_eyes_editable_import_test.fla`
  - Moved-eye proof PNG: `BlenderConstructionV4\animate_import_test\head_eyes_editable_import_test_eye_moved.png`
  - Import produced three separate Animate `shape` elements: head, left eye, right eye.
  - One eye was moved independently by +42 px and exported. JSFL `doc.undo()` is not available, so the exact move was manually reversed before saving. Reopening the FLA verified the original three editable vector shapes persisted.

## Animate Character Asset / Acting Test Update

One usable V4 character asset was completed inside Animate from the current projected artwork parts. This was not a new independent SVG redesign; the layers were imported from the current V4 projected art split into manageable SVG parts.

Deliverables:
- Split part SVGs: `BlenderConstructionV4\animate_character_parts\00_background.svg` through `08_mouth.svg`
- Initial editable asset FLA: `BlenderConstructionV4\animate_asset_v1\honest_interview_v4_character_asset.fla`
- Initial Animate-exported still: `BlenderConstructionV4\animate_asset_v1\honest_interview_v4_character_asset_clean_still.png`
- Acting FLA: `BlenderConstructionV4\animate_acting_test\honest_interview_v4_acting_test.fla`
- Reopened Animate-exported still: `BlenderConstructionV4\animate_acting_test\honest_interview_v4_acting_clean_still.png`
- Corrected Animate PNG sequence: `BlenderConstructionV4\animate_acting_test\frames_png_selected_v2\acting_0000.png` through `acting_0047.png`
- Corrected two-second MP4: `BlenderConstructionV4\animate_acting_test\honest_interview_v4_acting_test_v2.mp4`
- Corrected pose contact sheet: `BlenderConstructionV4\animate_acting_test\honest_interview_v4_acting_contact_sheet_v2.png`

Animate file verification:
- `honest_interview_v4_acting_test.fla` was saved, closed, reopened, and inspected.
- Stage is 1080 x 1920 at 24 fps with 48 frames.
- Populated layers after reopen: `Mouth`, `Brows`, `Eyes`, `Head`, `Chair_Foreground`, `Arms`, `Body`, `Chair_Back_Base`, `Background`.
- Editable shapes were verified on all character/chair layers. Background contains four shapes and one imported instance.

Acting test content:
- 0-15: initial listening hold.
- 16-23: eye-only shift toward the offscreen speaker.
- 24-35: compact asymmetric brow/head/mouth accent.
- 36-47: restrained skeptical settle/final hold.
- Static chair/body/feet layers were held throughout.

Export note:
- The earlier `animate_acting_test\frames_png` sequence and `honest_interview_v4_acting_test.mp4` were superseded because they exported as a frozen frame sequence.
- The corrected sequence used selected-frame export into `frames_png_selected_v2`. RGB-composited frame diffs confirm frame 16 changes only the eye area, frame 24 changes the head/face accent area, and frame 36 settles into a distinct held pose.

Remaining visual shortcomings:
- The asset is editable and usable for a short acting proof, but still visually simple compared with the references.
- The chair remains boxy/heavy.
- The right wrist/armrest contact is improved enough for the test but still reads awkwardly.
- Facial acting is readable in the contact sheet, but eyelid/brow construction is still basic and not production-polished.

## Animate Bodyfix Update

The original acting FLA was preserved:
- `BlenderConstructionV4\animate_acting_test\honest_interview_v4_acting_test.fla`

Corrected copy:
- `BlenderConstructionV4\animate_acting_test\honest_interview_v4_acting_test_bodyfix.fla`

Visible corrections made in Animate:
- Replaced the disconnected narrow filled torso with a minimal line-body drawn on the existing `Body` layer.
- Added Body and Arms keys at frames 0, 16, 24, and 36 so the body follows the head adjustment without reopening the neck/shoulder gap.
- Body now has a continuous spine from head base to seated pelvis, and both visible thigh lines start from that seated center.
- Arms now start from connected shoulder points; the screen-right shoulder is no longer detached.
- Removed the old visible arm hand dot/stray limb construction by replacing the `Arms` layer with connected line strokes.
- Strengthened the final skeptical face with a compressed mouth, asymmetric brows, and lowered upper eyelid strokes while preserving the rightward/offscreen pupil direction.

Corrected exports:
- `BlenderConstructionV4\animate_acting_test\frames_png_bodyfix\bodyfix_0000.png` through `bodyfix_0047.png`
- `BlenderConstructionV4\animate_acting_test\honest_interview_v4_acting_test_bodyfix.mp4`
- `BlenderConstructionV4\animate_acting_test\honest_interview_v4_bodyfix_contact_sheet.png`
- `BlenderConstructionV4\animate_acting_test\honest_interview_v4_bodyfix_allframes_review.png`

Verification:
- The corrected FLA was saved, closed, reopened, and inspected.
- Exported MP4 is 1080 x 1920, 24 fps, 2 seconds, 48 frames.
- All 48 exported frames were reviewed via the all-frame contact sheet. No new detached head/body, shoulder, or facial-part gaps were visible in that review.

## ProductionFull_v4 Update

Newest production revision:
`D:\Animate\Projects\HonestInterview\ProductionFull_v4`

Primary deliverables:
- Full MP4: `ProductionFull_v4\exports\honest_interview_full_v4.mp4`
- PNG sequence: `ProductionFull_v4\frames\honest_v4_000000.png` through `honest_v4_001701.png`
- Main editable Animate source: `ProductionFull_v4\editable\honest_interview_full_v4_layered_keyed_timeline.fla`
- Production script: `ProductionFull_v4\scripts\build_v4_assets.py`
- Reports: `ProductionFull_v4\ISSUE_LOG.md` and `ProductionFull_v4\FINAL_REPORT.md`

V4 corrections actually completed:
- Created project skills under `D:\Animate\.agents\skills` and added `D:\Animate\AGENTS.md`.
- Regenerated V4 Rhubarb cues against V4-local analysis WAV paths.
- Changed frame conversion to `floor(seconds * 24 + 0.5)`.
- Extended several speech tails based on cue/waveform evidence.
- Rebuilt smaller mouth drawings and lowered respondent gesture arms away from the face.
- Rendered and inspected V4 review sheets.
- Created a layered Animate FLA with seven populated layers.

Known limitations:
- `D:\Animate\HONEST_INTERVIEW_PRODUCTION_DIRECTIVE.md` was requested but was not found on disk; the pasted directive was used as authority.
- The V4 rendered MP4/PNG sequence has 1702 frames; the layered Animate FLA reports 1703 frames after creation and could not be trimmed by the two JSFL calls attempted.
- Direct real-time audio listening/playback was not available to the agent; lip sync review used Rhubarb cues, waveform evidence, and rendered frame inspection.
