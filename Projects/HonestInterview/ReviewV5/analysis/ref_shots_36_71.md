# Reference study: "Bro was so honest.mp4" 36.00–71.00 s, plus the other nine Goal videos

Source: `D:\Animate\Goal\Bro was so honest.mp4`. It is 480x850, 25 fps, 1775 frames. All times below are source seconds (frame = t x 25).
Method: I made every-frame contact sheets (head crop at 0.8x and body crop at 0.45x) for each shot, plus full-resolution zoom crops of key gestures. I read every sheet listed in the coverage section. I also computed a per-frame difference log (`diff_36_71.csv`), Hough head circles, ORB/affine zoom estimates for the camera push, and brightness extents for the iris.
The running notes written while viewing are in `notes_viewed.md`. The sheets are in `sheets/` and `sec/`, and the scripts are `cropsheet.py`, `framediff.py` and `headmeasure.py`.
I did **not** listen to the audio. Word timing comes from `ReferenceStudy/reports/audio_transcripts.json` (Whisper segments, which are loose) plus the visible mouth action. The directive file `HONEST_INTERVIEW_PRODUCTION_DIRECTIVE.md` is still missing, and I have not invented any of its contents.

Corrections to the brief:
- The final push-in starts at **67.52**, not 68.84.
- The iris starts at about **69.08–69.24**.
- The last two frames (70.92–70.96) are **not black**. They show an un-irised, full-brightness frame at the final zoom, probably an end-of-file or loop artefact. Do not copy it.

---

## 1. Shot table, 36–71 s

Every shot in this range is a **single**: one character alone in their armchair. The camera is locked off, apart from the ending.

Framing rules from the Hough measurements and the sheets:
- **CAP (respondent)**
  - Faces screen-right.
  - Head diameter is about 99–107 px, which is about 12% of the frame height.
  - Head centre is about (215–230, 353–365): slightly left of centre, 42% down the frame.
  - The armchair sits left and centre. Right of frame shows a pink flower pot on a dark two-drawer cabinet, a window at top right, and a grey checker floor.
- **NO-CAP (interviewer)**
  - Faces screen-left and wears round glasses with pale-blue lenses.
  - Head diameter is about 104–110 px.
  - Head centre is about (281–295, 359–365): right of centre.
  - The armchair is mirrored.
- **Both characters**
  - Knees are raised and shins drop vertically to the floor.
  - Hands rest on the armrest tops.
  - Limbs are uniform black strokes about 6–7 px thick.
  - The head outline is about 5 px thick.

| # | Start–end (s) | Frames | On screen | Framing | Camera |
|---|---|---|---|---|---|
| (prior shot, from 27.76) | –37.88 | –947 | CAP | single, as above | static |
| S2 | 37.92–39.60 | 948–990 | NO-CAP | single, head ~(280,361), d≈105–109 | static |
| S3 | 39.64–43.80 | 991–1095 | CAP | head ~(219,357), d≈99 | static |
| S4 | 43.84–47.44 | 1096–1186 | NO-CAP | head ~(281,359), d≈105 | static |
| S5 | 47.48–50.16 | 1187–1254 | CAP | head ~(211–220,358), d≈104–107 | static |
| S6 | 50.20–52.36 | 1255–1309 | NO-CAP | head ~(295,365), d≈104 | static |
| S7 | 52.40–56.20 | 1310–1405 | CAP | as S3 | static |
| S8 | 56.24–58.32 | 1406–1458 | NO-CAP | head ~(283,365), d≈110 | static |
| S9 | 58.36–60.72 | 1459–1518 | CAP | as S3 | static |
| S10 | 60.76–62.44 | 1519–1561 | NO-CAP | head ~(290,359), d≈108 | static, but the character jitters (see log) |
| S11 | 62.48–63.48 | 1562–1587 | CAP | head ~(219,359), d≈103 | static |
| S12 | 63.52–64.64 | 1588–1616 | NO-CAP | as S10 | static |
| S13 | 64.68–70.96 | 1617–1774 | CAP | head ~(220,353), d≈104, growing to ≈240 | static to 67.48, then push-in, vignette and iris-out |

Coverage alternates strictly, speaker by speaker. The only exception is S7's tail (55.24–56.20), where the cap is held on screen while the gap before the interviewer's "What?" plays.

### Ending camera: S13, measured

**Push-in**
- **Start:** 67.52 (f1688), eased in.
- **Fixed point of the zoom:** about (192, 307) in source pixels, stable within ±5 px from 67.6 to 69.24. That is just above-left of the cap's head, near the brim, so the head drifts down and right as the frame fills.
- **Scale relative to f1686:**

| Time (s) | 67.52 | 67.72 | 68.00 | 68.40 | 68.56 | 68.84 | 69.00 | 69.24 | 69.44 | 69.68 | 70.00 | 70.40 | 70.72 | 70.80 onward |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Scale | 1.001 | 1.010 | 1.039 | 1.109 | 1.156 | 1.267 | 1.355 | 1.50 | ≈1.62 | ≈1.84 | ≈2.08 | ≈2.29 | ≈2.36 | ≈2.37 (settled) |

- **Easing:** accelerating ease-in from 67.52 to about 69.9, then an ease-out to a stop by about 70.8.
- **Head diameter:** about 104 px, rising to about 155 px at 69.24 and about 240 px at 70.5.
- **Stepping:** the camera does not move on every frame. Every 3rd or 4th frame repeats the previous framing (f1701, 1704, 1708, 1711, 1715, 1718, 1722, 1726, 1729 duplicate their predecessor), so the move is effectively on ones with periodic holds, giving a slightly stepped push.

**Vignette and iris-out**
- **Centre:** the frame centre, **(240, 425) ±2 px**, throughout. The iris is not centred on the head. The zoom brings the head into the circle instead.
- **Onset:** 69.08–69.20. The corners darken first; mean frame brightness falls from 164 to 154.
- **Shrink:** by 69.28 the frame's top and bottom are black.
- **Circle radius** (outer extent of non-black pixels, threshold 25):

| Time (s) | 69.28 | 69.36 | 69.44 | 69.52 | 69.60 | 69.68 | 69.76 | 69.84 | 69.92–70.20 | 70.40 | 70.60 | 70.72 | 70.80 | 70.88 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Radius (px) | ≈390 | ≈344 | ≈304 | ≈271 | ≈245 | ≈227 | ≈214 | ≈208 | ≈205 (plateau, slow creep) | ≈198 | ≈189 | ≈180 | ≈173 | ≈164 |

  The shape is a fast close (69.28–69.84), a near-hold at about 205 px for about 0.4 s while the grin plays, then a slow final close.
- **Edge:** very soft. It ramps from full brightness to black over about 36–40 px (along the row y=425 at 70.00: value 202 at x≈64 down to 16 at x≈32). The ramp is tinted dark purple or magenta (BGR ≈ (36,11,17) to (84,59,65) in the transition). There is no hard ring and no bright glow ring, but the purple gradient reads as a faint dusky halo.
- **End:** the iris is still about 164 px when it ends at 70.88. It never closes fully to black in the picture. After that come the two artefact frames (70.92–70.96), which are bright and un-irised at 2.37x.
- **Timing against the dialogue:** "I guess you can call me an entrepreneur" runs 66.56–70.32. The push starts on "call me", the iris starts on "entre-", and the grin with closed eyes plays inside the plateau.

---

## 2. Drawing-change log, per shot

**Global drawing system (both characters)**

**Head and face**
- The head is a plain grey circle.
- Pupils are tall solid black ovals, and the mouth sits on the facing side of the head.

**Brows and lids.** These are separate overlay drawings swapped instantly, never tweened:
- Angry V brow bars.
- Worried, inner-raised arcs.
- Half-lid: a flat line across the top of the pupil. On the no-cap it is a flat bar across the lens.
- Closed-eye downward arcs.
- The cap's brows are hidden under the brim when neutral.

**Mouth family.** This is shared by both characters and swapped on ones and twos:
- **Rect:** clenched-teeth rectangle with a centre line.
- **Open:** dark interior, white top-teeth band and red tongue.
- **O:** small black oval.
- **Pucker:** black lips with a red centre.
- **F/V:** scalloped top teeth over the lip.
- **Wavy:** a squiggle line, used about once per line as an accent.
- **Closed:** a flat or slightly down-turned line.
- **Smiles**, which appear only in S13: an up-curve, a D-shaped grin with a teeth band, and a grin with teeth.

**Exposure**

These are hold lengths between drawing changes, measured in the diff log:
- S2: 14 changes held one frame, 9 held two frames.
- S4: 31 held one frame, 18 held two, 6 held three.
- S10: 19 held one frame, 11 held two.
- Speaking passages are therefore mostly on ones mixed with twos, with holds of 3–4 frames.
- Long holds are 8–18 frames (closed mouth at the end of a line, or listening).

**Bodies and blinks**
- Bodies are held for entire shots unless a gesture is scripted.
- Blinks are 2–3 frames of closed or half lids. They are placed on phrase boundaries or vowels, often mid-speech.

### S1 tail (CAP, 36.00–37.88): "…how much money $10 billion is?"
- The body is held.
- Brows are angry V throughout.
- Mouth sequence: open (36.00–36.16), rect (36.20–36.24), pucker (36.28–36.32 "much"), O (36.36–36.44), rect (36.48–36.64), wide open (36.68–36.92).
- **Blink** 36.80–36.88: 3 frames, closed arcs, mouth still open.
- 37.64–37.88: mouth closes to a slightly down-turned line and holds into the cut.
- 37.76–37.84: tiny head-and-body settle, 3 frames.

### S2 (NO-CAP, 37.92–39.60): "Oh, it's just a hypothetical."
- 37.92–38.08: **reaction held over the cut**. Worried brows and frown for 5 frames before speaking.
- 38.12: brows flatten and speech starts.
- 38.68: **thought change**. Brows snap to angry V on a wide open mouth.
- 38.76–38.80: blink, drawn as lid lines inside the lenses.
- **Shrug**
  - 38.84: the near (screen-left) forearm leaves the armrest first.
  - 38.96–39.00: both forearms are up, palms up.
  - Held 39.00–39.36.
  - 39.40–39.52: arms lower, near arm last.
- 38.96: wavy mouth on "hypo-".
- 39.56–39.60: closed frown, 2 frames.
- The head never moves. The arms lead and the face accents.

### S3 (CAP, 39.64–43.80): "And if it was a reality, I'd be first in line."
- The body is held for 4.2 s.
- 39.64: angry brows carried over the cut. By 39.68 the brows disappear under the brim, giving a matter-of-fact neutral face.
- F/V mouth at 39.80–39.88 ("if") and 41.92–42.16 ("first").
- 41.00–41.08: smug eyes-closed, 3 frames.
- **41.12 onward: half-lid deadpan pupils.** This is the respondent's signature "honest" face, held for the rest of the shot.
- Closed-mouth holds at 41.12–41.52 (10 frames) and 42.64–43.04 (11 frames), as beats between clauses.
- 42.20–42.24: eyes closed on a vowel.

### S4 (NO-CAP, 43.84–47.44): "You're talking about human lives for $10 billion."
- 43.84–43.92: worried-brow reaction for 3 frames, then 43.96 switches to angry V for the rest of the shot.
- The body is held.
- 44.92–44.96: blink with a flat mouth.
- 46.52–46.60: half-lid, 3 frames, mid-speech. This is an exasperated eye-drop.
- 47.24–47.32: half-lid on an O mouth.
- **Mouth still articulating at 47.40–47.44 when the cut lands.** The cap's interruption is staged by cutting away from the speaker mid-word, not with a listener reaction.

### S5 (CAP, 47.48–50.16): "Hey, hey, hey, hey. Guess what?"
- **Arm**
  - 47.48: the arm is already coming off the armrest on the first frame, forearm raised and elbow bent. Eyes are still half-lid with angry brows.
  - 47.52: the arm is higher and the eyes widen.
  - 47.56: the arm is fully extended, nearly horizontal toward the interviewer, with a slight elbow sag. The hand is a single up-turned stroke, a flat "hold on" palm with no fingers.
  - This is a 3-frame raise: the arm leads, the eyes follow at 47.52, and the brows drop out at 47.68.
  - The arm is held 47.56–48.92 (about 34 frames) with only tiny wrist redraws.
- **Mouth:** alternates open and rect in 3–4 frame beats, one cycle per "hey" (47.48–48.76).
- 48.80: mouth closes.
- **48.96: the arm drops back to the armrest in ONE frame**, with no ease.
- 48.80–49.48: closed-mouth pause, 18 frames. This is the timing beat before "Guess what?".
- 49.52–49.76: "Guess what" mouths.
- 49.80–49.88: eyes close smugly on "what".
- 49.92–49.96: eyes reopen and the mouth closes.
- 50.00–50.16: angry V brows return with a closed flat mouth, a 7-frame "well?" hold.

### S6 (NO-CAP, 50.20–52.36): "I don't want to guess. Don't make me guess."
- 50.20–50.44: listening hold, worried brows and frown.
- **Arm fold 50.40–50.56**
  - The near forearm swings up first, as a long diagonal stroke.
  - 50.48: the forearms cross.
  - 50.52: folded, with the forearms crossed horizontally over the stick torso.
  - Held until the end of the shot, about 45 frames.
  - Speech starts at 50.48, before the fold settles (overlap).
- **Head turn by drawing swap**
  - 50.64: profile.
  - 50.68: **front or ¾ view**, with the glasses centred on the face, both lenses visible, raised brows, and a pucker or O.
  - 50.76–51.60: eyes shut behind the lenses, facing the camera, while saying "I don't want to guess". This is refusal by looking away from the cap.
  - **51.64: snaps back to profile** with angry V brows and an open mouth: "Don't make me guess" is aimed at the cap.
  - There are no in-betweens either way.
- 51.76: 1-frame lid close.
- 51.84–52.36: angry profile, articulating.

### S7 (CAP, 52.40–56.20): "Oh come on. You got to be curious about what I'm going to tell you."
- The body is held throughout.
- 52.68–52.76: 3-frame closed pause after "Oh".
- 52.80: brows vanish, giving an open, eager, neutral face.
- 53.36: wavy mouth.
- 53.96–54.04: eyes closed on a phrase boundary.
- Line ends 55.20.
- **55.24–56.20: listening hold, 24 frames.** Closed down-turned mouth, body frozen, with a slow **double blink** at 55.64–55.72 and 55.80–55.88.

### S8 (NO-CAP, 56.24–58.32): "What?"
- **New lid drawing:** a flat horizontal bar across the top of each lens, reading as unimpressed. Held the whole shot, with a frown.
- 56.24–56.60: arms still folded (continuity from S6).
- 56.64–56.76: unfold.
- **56.80:** mouth opens as the arms rise.
- 56.92–57.00: palms-up shrug.
- 57.00–57.32: "What?" mouths (O, open, rect).
- 57.36: mouth closes.
- 57.48–57.64: arms lower, near arm last.
- **57.64–58.32: frozen listening hold, 18 frames.**
- The picture puts "What?" at about 56.80–57.32. The transcript segment of 55.12–57.12 is loose.

### S9 (CAP, 58.36–60.72): "I would have did it for $5 billion" (the first price reveal)
- 58.36–59.08: half-lid deadpan while speaking.
- 59.12–59.20: eyes closed, 3 frames.
- **Five hand, 59.48–60.20**
  - The forearm pivots up from the elbow, which stays on the armrest.
  - 59.48–59.52: plain diagonal line with no hand drawn.
  - 59.56: a full **open hand appears**. It is a solid black palm with five splayed, rounded fingers, the only articulated hand in the range.
  - 59.56–60.08: the hand makes tiny alternating angle redraws every 1–2 frames, a jitter or wag that emphasises "five".
  - 60.12: the hand is removed.
  - 60.12–60.24: lowered over 4 frames.
- **Eyes pop to full-open neutral at 59.52, the same frame the hand rises.**
- 60.24–60.32: smug eyes-closed.
- 60.36–60.72: half-lid with a closed down-turned mouth, 10 frames.

### S10 (NO-CAP, 60.76–62.44): outraged reply
I did not verify the words, because the transcript merges them into the previous line.
- 60.76–61.04: 8-frame closed-mouth reaction hold. Angry V brows and a deep frown.
- **Tremble, 60.84–62.40:** head and upper torso (diff bbox x207–347, y305–493) jump between two positions offset by (−4, −1) px, irregularly every 1–3 frames. Rage is shown with a 2-position jitter, not with redrawn poses.
- Mouth sequence includes F/V (61.08, 61.36–61.44).
- 61.80–61.88: half-lids with a pucker, a scornful blink.
- **62.00–62.44: clenched-teeth rect held 12 frames, still trembling**, into the cut.

### S11 (CAP, 62.48–63.48): the lower-price reveal ("$1,000" per the transcript)
- The first frame opens **eyes-closed with an F/V mouth**.
- 62.52: eyes open to neutral.
- 63.12–63.20: closed again.
- 63.24: half-lid with flat, angry-ish brows.
- 63.36–63.48: closed flat mouth.
- **No gesture, body frozen.** The bigger punchline is played smaller than the "five" setup.

### S12 (NO-CAP, 63.52–64.64): "What are you?"
- Angry V brows.
- 64.00–64.08: lowered lids, 3 frames.
- **64.12–64.48: small O held 10 frames** for the drawn-out "you?".
- 64.52–64.64: closed frown.
- The body is held.

### S13 (CAP, 64.68–70.96): "Oh, that's a good question. I guess you can call me an entrepreneur."
- 64.68–64.80: half-lid, then 64.84 opens to mock-sincere neutral.
- 65.84–66.08: **eyes closed while talking**, 7 frames ("good question").
- 66.28–66.60: closed-mouth thought beat, 9 frames.
- **66.64: first smile of the film.** An up-curve for 1 frame, then D-grins from 66.68.
- 66.96–67.04 and 67.68–67.76: smug closed eyes.
- **67.84: cocky V brows return on top of the grin.** This sly "entrepreneur" face is held through the push-in.
- 68.16–68.20: closed smile curve (the "m" of "me").
- 68.84–68.88: eyes closed. 68.92: half-lid.
- **Hands:** 69.36 the near forearm rises. 69.40 both forearms meet in a **tent or steeple in front of the chest**, a scheming-businessman pose, held to the end.
- 69.40–69.44: wavy lip-press.
- 69.52–69.72: grin. 69.76: pucker. 69.80–70.16: O.
- **70.20–70.72: grin with eyes closed**, inside the iris plateau.
- 70.76–70.88: eyes reopen with V brows and grin as the iris closes.
- The body is otherwise frozen. The camera carries the ending energy.

---

## 3. Example index

**Listening hold**
- **55.24–56.20, Bro (CAP):**
  - Beat: the cap is savouring the suspense.
  - Gaze and body: gaze toward the interviewer (right); body fully frozen, hands on the armrests.
  - What moves: nothing but a slow double blink (3f + 1 open + 3f).
  - Mouth: closed, slightly down-turned.
  - Cut context: the cut to the interviewer's "What?" comes 0.6 s before he speaks.
- **57.64–58.32, Bro (NO-CAP):** flat-bar lids and frown, frozen for 18 frames after the shrug settles.
- **Dirt bike 78.00–79.96, police officer:**
  - Chin on hand, bored.
  - Only the brows and lids shift every 2–4 frames, with half-lid squints.
  - The hand moves to the mouth at 79.83.

**Thought change**
- **Bro 38.68 (NO-CAP):**
  - Worried or neutral brows swap to angry V in one frame on a wide-open mouth, then a blink at 38.76.
  - Body support follows 4 frames later with the shrug.
- **Bro 66.28–66.64 (CAP):**
  - A 9-frame closed-mouth beat, then a 1-frame up-curve smile, then grin.
  - This reads as "idea arrives".
- **Wait for later 7.30–8.13:**
  - The doctor's bulging eye shrinks.
  - The lids descend through real in-betweens to closed (7.53–8.00), then open in 3 steps to a bored half-lid.
  - This is a graded version, unlike Bro's pops.

**Interruption ("hey hey hey, guess what")**
- **Bro 47.44–47.48, the cut:**
  - The interviewer is still mid-word at 47.44. The cap's arm is already off the armrest on his first frame.
  - The audience should understand that he steamrolls the moral point.
- **Staging on the cap:**
  - Gaze and body: gaze at the interviewer; body upright and unmoved.
  - Leading part: the arm (3-frame raise to a horizontal stop-palm), then the eyes widen on the next frame.
  - What holds and what changes: the arm holds 34 frames while the mouth cycles.
  - Silhouette: a clear horizontal arm, the only one in the film.
  - Exit: a 1-frame drop, then an 18-frame pause before "Guess what?", closing on smug eyes.

**Emphatic gesture**
- **Bro 59.48–60.24, the five hand:**
  - The forearm pivots from the elbow; the upper arm is still.
  - A 5-finger black hand appears on the 3rd frame and jitters as it is held.
  - The eyes pop open on the same frame the hand rises.
  - Overlap: the mouth keeps articulating the whole time; the hand drops (4 frames) as the mouth closes.
- **Bro 38.84–39.52 and 56.80–57.64, NO-CAP shrugs:** the near arm leads up and trails down.
- **Bro 69.36–69.40, CAP steeple:** a 2-frame move into a held pose.
- **Fake Studying 10.00–10.96, dad's arm flex:** a smear frame with motion arcs at 10.04, then pose swaps as the muscle grows (10.21–10.29), and a bigger re-staged pose at 10.75.

**Head turn**
- **Bro 50.64→50.68 and 51.60→51.64 (NO-CAP):**
  - A profile/front head swap with no in-betweens. The glasses relocate from the facing edge to the face centre.
  - Eyes shut while turned away. The turn itself carries the meaning (refusing to engage), and the snap back to profile aims the next line at the cap.
  - The body stays folded and still.
- **That one friend 13.80→13.83:** a profile-to-front drawing swap on the student, then 3-step escalation (14.13 puffed cheeks, 14.27 bulging eyes and squashed body).

**Mouth articulation**
- **Bro S4 43.96–47.44 (NO-CAP) and S7 52.40–55.20 (CAP):** the full shared mouth family (rect, open, O, pucker, F/V, wavy) swapped on ones and twos, one shape per phoneme group. F/V teeth appear reliably on "f/v" words ("if", "first", "for", "five").
- **Blinks:** blink or eye-close frames are laid over speech without pausing the mouth.
- **Going back home 6.50–7.47:** crowd screaming. It uses a larger family: open with tongue, gritted teeth with vertical tooth lines, wavy frown, and tiny O. Changes are on ones.

**Punchline reaction**

*Lower-price reveal*
- **CAP five-hand setup (59.5).**
- **NO-CAP outrage (60.76–62.44):**
  - An 8-frame frozen frown, then a rage tremble (2-position, 4 px jitter) and a clenched-teeth hold of 12 frames into the cut.
- **CAP "$1,000" (62.48):**
  - Deadpan, eyes closed at the start, half-lid at the end, no gesture.
- **NO-CAP "What are you?":** a held O for 10 frames.
- The escalation is carried by the interviewer's reactions while the respondent gets calmer.

*"Entrepreneur" ending*
- The first smile appears only here (66.64).
- Cocky V brows are added to the grin (67.84), then the steeple hands (69.40).
- The push-in from 67.52 is combined with the iris from 69.2 centred on the frame, with the grin and eyes-closed played inside the iris plateau.

---

## 4. Secondary videos

What transfers from each, as observed at 0.5 s overview plus the every-frame passages.

- **Dirt bike**
  - Format: 1024x576, 24 fps, 220.8 s. Cream-palette, rubber-hose-like action short, almost no dialogue.
  - Stunned hold, 21.00–22.12: the open-mouth "shock" drawing is held about 27 frames with essentially no change. This confirms that long, still reaction holds read fine.
  - Laugh, 29.50–30.33: a 2-drawing flail cycle on ones with drybrush multiple-arm smears, cut to a static wide laugh (30.42–30.96).
  - Bored cop, 78.00–79.96: good listening-hold reference. Only lids and brows change, every 2–4 frames.
  - Lesson: holds plus a few decisive drawings. Smears only for big physical action, which is not needed in our seated dialogue.

- **Fake Studying Gone Wrong**
  - Format: 576x1024, 24 fps, 13 s. bangbang.animations; seated kid in an armchair, the closest construction match to our seated shots.
  - 4.50→4.58: an instant expression swap from a manic toothy grin to innocent half-lids with a small smile on a 1-frame cut. This is the same "pop" philosophy as Bro.
  - Grin, 0.00–0.62: a nearly held drawing.
  - Flex, 10.00–11.46: one smear frame, then escalating pose swaps.
  - Lesson: expression changes as whole-face swaps. A seated body can be held for seconds.

- **Ghost House**
  - Format: 1032x576, 30 fps, 38.4 s. Rico Animations.
  - Blink, 12.60–12.87: a **graded, multi-frame blink**. Lids descend over about 3 frames, stay closed 2–3, and open over 3.
  - Worry shift, 30.50–31.97: smile to worried gritted mouth with shrinking pupils via a 1-frame swap, then held.
  - Lesson: a softer blink option, but Bro itself uses 2–3 frame pop blinks. Match Bro.

- **Going back home**
  - Format: 576x1024, 30 fps, 41.7 s. Dark, soft-focus style.
  - Face close-up, 0.50–2.23:
    - Heavy half-lids drawn as double lid lines, held on 2s–3s.
    - A head-angle drawing swap at 1.10, and a wide-eyed shocked grimace swap at 1.87.
  - Crowd scream, 6.50–7.47: an extended mouth family on ones.
  - Lesson: lid thickness and drawing swaps convey fatigue and shock. Useful vocabulary for extreme reactions only.

- **Me vs Mom Cooking**
  - Format: 576x1024, 24 fps, 8.5 s. bangbang style.
  - Mom, 1.50–3.46: an unimpressed half-lidded woman with glasses, like our no-cap's flat-bar lids. Her lids lower in steps and she blinks at 1.92–1.96 while the peeking kid's eyes widen.
  - 4.00–4.96: an arm crossing the face with overlap on the spatula.
  - Lesson: a glasses-wearing character's lids read through the lenses. Keep lid lines inside the lens.

- **POST-NuT Clarity**
  - Format: 576x1024, 30 fps, 46.2 s. Heavy blur backgrounds; seated character in an office chair.
  - 20.50–22.47: shock, then a head-drawing swap at 21.43 to an anxious lower-lid squint.
  - 44.00–45.97: a seated anxious hold where the only action is a **pupil dart** (44.10) and blinks. The body is frozen.
  - Lesson: pupil shifts are a cheap, readable addition to listening holds. Bro does not use pupil darts, so use sparingly if at all.

- **That is why!**
  - Format: 576x1024, 24 fps, 6.4 s. A stick figure walks to a bench and sits.
  - Sit-down, 2.25–2.67: a turn and drop into the sit in about 4–6 frames with no bounce.
  - Leg cross, 5.33–5.42: speed-line smear frames.
  - Lesson: stick-limb seated construction (knees apart, oval feet) and a fast sit. Relevant if any shot needs sitting motion.

- **That one friend in class**
  - Format: 576x1024, 30 fps, 20.2 s. Toonkart36.
  - Laugh cycle, 1.50–2.97: head alternates between two drawings every 2–3 frames, with hand over mouth and squint eyes.
  - Teacher, 8.00–8.60: suspicious side-eye, lowered brows and a flat mouth, with a small pupil shift.
  - Student, 13.50–14.57: profile/front head swap, then 3-step escalation of a suppressed laugh.
  - Lesson: head turns as swaps, and escalation in discrete steps.

- **wait for later one crazy**
  - Format: 576x1024, 30 fps, 21.9 s. Boos animations; glowing outline style.
  - Doctor, 7.00–8.97: bulging single eye, then in-between lid descent, closed, then a 3-step open to a bored half-lid. The mouth is hidden under a mask, so all acting is in the lids.
  - Crying, 17.00–18.27: wide-mouth cry held with tear streams.
  - Lesson: eyelid-only acting can carry a beat.

---

## 5. Coverage statement

**Bro was so honest.mp4**

*Every frame viewed*
- **Head crop plus body crop**, all frames f900–1686 (36.00–67.44). Sheets h00–h16 and b00–b16 were all read and inspected.
  - My first reads of these sheets were dropped from context before I could use them ("media removed"), so I re-read every one and wrote notes immediately. `notes_viewed.md` records only the second, visible reads.
  - h07 (f1247–1254) was viewed. Its body sheet b07 (49.88–50.16 body) was not re-viewed. The body is held there per the diff log (all changes are confined to the face).
  - h17 and b17 (f1677–1686) were not re-viewed as separate sheets. That range is covered by z_end_face.
- **Full frame at 0.3x**, f1687–1774 (67.48–70.96): end_1687.
- **Face crop at 0.45x**, f1677–1731: z_end_face.

*Full-resolution or zoom crops viewed*
- f1186–1195, f1218–1227 (hey-hey arm).
- f1258–1275 (arm fold).
- f1285–1297 (head turn).
- f1485–1507 (five hand).
- f1731–1746 (steeple and iris).
- f1768–1774 (last frames).

*Generated but never successfully viewed (stripped)*
- p00_ov (36–71 at 0.5 s).
- z_c_37_7, z_c_36mouth, z_n_shrug.
- full_900/962/1100/1735/1750/1772/1773/1774.
- Their frame ranges are covered by the every-frame sheets above.

*Numeric only (not visual claims)*
- Diff log f895–1775.
- Head Hough circles at sample times.
- Zoom scale f1686–1774.
- Iris extents f1726–1774.
- Tremble offsets f1519–1561.

*Not covered by me:* 0–36 s.

*Audio:* not listened to. Word timings are from the Whisper transcript and the mouth drawings.

**Other nine videos**

Overview at 0.5 s, viewed:
- Dirt bike: 0–220.5 s.
- Fake Studying: 0–12.5.
- Ghost House: 0–38.0.
- Going back home: 0–41.5.
- Me vs Mom: 0–8.5.
- POST-NuT: 0–46.0.
- That is why: 0–6.0.
- That one friend: 0–20.0.
- wait for later: 0–21.5.

Every frame viewed (crop sheets in `sec/ef_*.png`):

| Video | Passages (s) | Frames |
|---|---|---|
| Dirt bike | 21.00–22.46; 29.50–30.96; 78.00–79.96 | f504–539, 708–743, 1872–1919 |
| Fake Studying | 0.00–0.96; 4.00–4.96; 10.00–11.46 | f0–23, 96–119, 240–275 |
| Ghost House | 12.00–13.17; 30.50–31.97 | f360–395, 915–959 |
| Going back home | 0.50–2.47; 6.50–7.47 | f15–74, 195–224 |
| Me vs Mom | 1.50–3.46; 4.00–4.96 | f36–83, 96–119 |
| POST-NuT | 20.50–22.47; 44.00–45.97 | f615–674, 1320–1379 |
| That is why | 2.00–3.96; 5.00–6.33 | f48–95, 120–152 |
| That one friend | 1.50–2.97; 8.00–8.77; 13.50–14.57 | f45–89, 240–263, 405–437 |
| wait for later | 7.00–8.97; 17.00–18.27 | f210–269, 510–548 |

All other time in these videos was seen only at 0.5 s sampling. No audio was reviewed for any secondary video. Their transcripts are mostly noise.

**Not performed:** normal-speed playback, direct listening, lip-sync verification, artistic approval.
