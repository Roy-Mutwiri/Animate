# ProductionFull_v5 issue log

Times are seconds on the original audio; frames are global zero-based production frames (24 fps).

| # | Shot / time | Defect (evidence) | Cause | Correction | Recheck |
|---|---|---|---|---|---|
| 1 | all (stills_v5a) | Head rendered yellow, nightstand pink, wall/floor/chair fills missing (`review/cmp_stills_a1.png`) | several plain DOMShapes in one frame merged; fill-style tables collided | every shape written as a drawing object | fixed (`review/cmp_stills_b1.png`) |
| 2 | all CAP shots | cap covered the eyes; eyes too high (`review/cmp_heads_b.png`) | cap drawn as a low band; eye/brow y from an estimate | cap redrawn as a dome on the skull from a gridded zoom crop; eyes y-13, brows y-24 | fixed (`review/cmp_stills_c1.png`) |
| 3 | all GL shots | lenses too high, pupils too small | estimate | lens centres y-10, R 12; pupils r 4.6 | fixed (`review/cmp_stills_c1.png`) |
| 4 | floor | checker missing, then too weak perspective | wrong side of the wall plane kept; horizon too high | 1-point grid, horizon y 20, measured tile sizes | fixed (`review/cmp_stills_c2.png`) |
| 5 | 69.1-70.9 iris | circle filled black instead of the outside (`review/iris_test.png` earlier state) | hole path wound the same way as the outer path | single keyhole polygon, opposite winding; soft purple feather rings | fixed (`review/v5a_1s_b.png` 70 s tile) |
| 6 | 2.64 / 27.84 jut | head rotated away from the listener | tilt sign | +tilt = clockwise for the screen-right facer (ref crop `review/ref_headback.png`) | fixed in v5a |
| 7 | all | mouths ~2/3 of reference size | drawing scale | mouth instances scaled 1.45 (~0.35 head diameter) | fixed in v5a |
| 8 | 9.28-11.72 raised finger | hand at the chin read as "thinking" (`review/rep_a_cmp_7_19.png`) | pose targets | forearm vertical in front of the face, finger at eye level | fixed in v5a (to recheck in v5b sheets) |
| 9 | all | torsos too upright vs reference | head offset | HEAD_C (-15,-184) | fixed in v5a |
| 10 | speech, e.g. 9.12-9.38, 10.12-10.42, 10.75-11.0 | clenched-teeth B held 6-10 frames on vowels -> frozen mouth (`review/mouth_cap_nothing.png`) | Rhubarb labels lip shape, many vowels B | jaw pass from speaker loudness (jaw.py): CAP 350 / GL 194 frames re-opened or closed; A/E/F/G/H kept | test render `review/mouth_cap_nothing_jaw.png` shows vowels opening; full recheck in v5b |
| 11 | 64.12-64.52 GL "you?" | O mouth held 0.5 s after the word ended (64.00) | override copied from reference timing | held to 64.20 then frown | in v5b |
| 12 | F (pucker) | read as an "O in parentheses" (`review/mouth_gl_someone.png`) | drawing | black lips around a red centre, as in the reference | in v5b |
| 13 | 0.00-0.33 (f0-8) | transparent band at top of frame (independent review #1) | two-shot camera saw above the wall art | room extended to y -320 | v5c/v5d: 0 frames with any transparency (alpha scan of all 1702 PNGs) |
| 14 | 67.5-69.3 push-in | stutter: each table segment eased to zero (review #2) | 'lin' segments fell through to ease-out | true linear segments over the dense measured table | v5c/v5d per-frame zoom increments monotonic 0.002 -> 0.044 -> 0.005 |
| 15 | 70.46-70.92 | final mouth a dark open shout (review #3) | wrong drawing (C smug) | closed-eye teeth grin (B smug) | v5d frame 1695 decoded as Mouth_Cap firstFrame 20 = smug_B; `review/v5c_fixes_cmp.png` |
| 16 | 28.46-29.60 drape | arm stub hidden behind the head (review #4) | elbow inside the head circle | elbow (-58,-134), forearm along the chair-back top | `review/v5c_fixes_cmp.png` 29.0 s |
| 17 | speech, many | clenched-teeth rect held 7-23 frames (review #5) | Rhubarb lip labels, no jaw pass; long holds | jaw pass + silence rule + long-hold relaxation (quiet B >= 9f -> rest, O/pucker >= 7f -> teeth); longest non-rest hold now 13 f (hissed "s" of "yes") | verify_lipsync v5d: 0 mapping defects |
| 18 | all GL singles | CAP foot leaked at left edge (review #6) | shared stage framing | v5c hid CAP -> caused a pop at f22 during the opening move (found by producer); v5e instead widens GL single cx 239->252 so the toe is at -14 px | recheck in v5e |
| 19 | 69.25-70.88 | iris edge banded (review #7) | 8 stepped rings | 22 rings, smoothstep alpha | v5d visual |
| 20 | 59.54-60.10 | five hand small, read as fist (review #8) | drawing | larger palm, longer splayed fingers, raised higher | `review/v5d_check.png` |
| 21 | 9.42-11.71 | raised finger bent like a hook (review #9) | finger followed forearm angle | finger drawn screen-vertical above a fist | `review/v5d_check.png` |
| 22 | 11.75-11.92 | "lean snaps back" (review #10) | not reproduced: lean holds 4 deg from f284 (data + `review/check_lean_jitter_v5b.png`) | none | sent back to reviewer for recheck |
| 23 | 66.62-66.96 first smile | reads as talking (review #11) | smug open mouths dominated by tongue | smug C/D: taller teeth band, smaller tongue | v5d |
| 24 | 69.38-70.88 steeple | read as crossed X (review #12) | forearms crossed the upper arms | hands meet in front of the chest at one point | v5d |
| 25 | 60.84-62.40 tremble | "absent" (review #13) | present: 2-position (-4,-1) ref-px head jitter, ~9 px at 1080 (same as reference) | none | sent back to reviewer |
| 26 | all | window notches (review #14); v5c then erased the whole window | overlapping same-fill paths in one drawing object cancel | glass and each bar are separate drawing objects | `review/v5d_check.png` |
| 27 | 0.92-1.4 (f22+) | v5c/v5d: CAP vanished mid-move while his legs were in frame (producer check) | hide rule from fix 18 | reverted hiding; GL single cx 239 -> 252 so the toe sits at -14 px | v5e/v5f: CAP drawn in every frame; left edge clean in GL singles |
| 28 | smug grin frames (1600, 1695 ...) | teeth rendered head-grey (independent recheck residual) | mouth outline added twice (fill, then stroke) inside one drawing object; overlaps cancel | every add() written as its own drawing object (xfl.Shape) | v5f crops (`review/v5f_check.png`): white teeth; diff vs v5e shows only restored details (flower centres, chair rims, cap fringe) |
| 29 | residual | rect holds 7-9 f at 10.12-10.42, 11.25-11.62, 21.08-21.29 | recogniser labels + moderate loudness | not changed | open — disclosed in FINAL_REPORT |
| 30 | residual | push-in speed kinks; framing at ~69.4 s tighter than reference | measured scale table; fixed-point estimate | not changed | open — disclosed |
