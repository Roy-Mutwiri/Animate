# ProductionFull_v3 Issue Log

| Shot/timecode | Visible defect | Correction | Recheck result |
|---|---|---|---|
| all close-ups | V2 side chair/body overlap was rough; foreground armrest hid torso/arms in first V3 patch | Split chair into back/seat/front-arm passes; lowered foreground armrest so it occludes cushion/thigh instead of torso; adjusted pelvis/thigh start points | Rechecked `previews\opening_dialogue_pose_review.png`; torso and shoulder acting are visible again, overlap is more readable though still simplified |
| all close-ups | gesture arms too straight and isolated from shoulder/torso | Added elbow/wrist/hand endpoints for pointing/objecting poses; tied active arm to shoulder and gave resting arm a separate bend | Rechecked opening preview and full contact sheet; gesture silhouettes are clearer |
| spoken phrases | Rhubarb cues used but not refined for closures/silences | Added boundary cleanup in `mouth_value`: force closed/rest at phrase starts/ends and suppress tiny cue chatter | Rebuilt all frames; mouth shapes no longer sit open at line boundaries |
| production source | V2 FLA was one flattened vector layer | Created `editable\honest_interview_full_v3_layered_keyed_timeline.fla` with 7 populated layers and 26 timed keys per layer | Reopened/inspected via Animate MCP; layer/key counts verified |
