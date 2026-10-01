# Reference study — "Bro was so honest.mp4", source 0.00–36.00 s

Analyst: read-only reference pass (no Animate/Blender/Moho contact). Source: `D:\Animate\Goal\Bro was so honest.mp4`, 480x850, 25 fps. All times are **source seconds** (frame = t x 25). No audio was listened to in this pass; speaker attribution below comes from **visible mouth motion only**. `HONEST_INTERVIEW_PRODUCTION_DIRECTIVE.md` is still missing (not consulted, not invented).

Method: every frame f0–f899 was decoded sequentially (OpenCV) to PNG. Consecutive frames were pixel-diffed (a pixel counts as changed if the gray difference is >40; a frame counts as a new drawing if >50 pixels changed). That gave **480 distinct drawings in 900 frames**. Every distinct drawing was then viewed in labeled contact sheets that show the start frame and hold length (`xN` = number of frames on screen). Faces, hands and chair were checked in 2.5x/2x zoomed crops. Measurements come from grid overlays (25 px grid), Hough circle fits, and pixel scans.

Naming: **CAP** = the respondent (black cap, sits screen-left, faces screen-right). **GLASSES** = the interviewer (no cap). He wears round wire glasses, which the brief did not mention; this is his defining feature. He sits screen-right and faces screen-left.

---

## 1. Shot table

Framing figures are in 480x850 pixel space. Head diameter is measured outside the outline. "Seat top" is the red seat-top/cushion line under the thighs. "Horizon" is the wall/floor line.

| # | Start–end (s) | Frames | On screen | Framing | Camera |
|---|---|---|---|---|---|
| 1 | 0.00–2.48 | 0–61 | Two-shot → GLASSES single | f0: CAP head centre (66,380), Ø≈84; cap top y≈322. GLASSES head centre (398,370), Ø≈90. Nightstand x175–298, y503–600, centred between them. Seat tops ≈ y535 (CAP) and 525 (GLASSES). Horizon ≈ y515. Window x135–355, y75–310. **End (f40): GLASSES head centre (282,360), Ø≈106; seat top ≈ 553; horizon ≈ 540; window top-left x0–230, y10–295; nightstand + plant screen-left.** | Eased pan-right plus zoom-in, **f2–f37 = 0.08–1.48 s** (the brief said 0.36–1.24). Per-frame diff ramps up to a peak around 0.76 s, then down: slow-in/slow-out. About 1 duplicate frame in every 3–4 during the move. The subject keeps lip-syncing during the move. |
| 2 | 2.48–3.08 | 62–76 | CAP single | Head centre (222,358), Ø≈106–108; cap top y≈287; eyes y327–349; seat top y≈545; horizon ≈ y520 (behind the chair) / 540; chair x105–315; nightstand x350–480, y505–625; window x315–480, y0–275. | Static |
| 3 | 3.08–3.84 | 77–95 | GLASSES single | Head centre (274,364), Ø≈108; seat top ≈ 555–560; horizon ≈ 540; chair x185–400; nightstand x10–160 (screen-left); window x0–215. Mirror of the CAP single. | Static |
| 4 | 3.84–4.56 | 96–113 | CAP single | Same set-up as shot 2. | Static |
| 5 | 4.56–7.20 | 114–179 | GLASSES single | Same set-up as shot 3 (head centre (278,364), Ø≈108). | Static |
| 6 | 7.20–19.40 | 180–484 | CAP single → push-in | Starts as the shot-2 set-up (head (228,358), Ø≈106). After step 1 (f416): head Ø≈110, centre y≈352, seat top ≈ 575. After step 2 (f438): head Ø≈145–155, centre (222,334), seat top ≈ 610. After step 3 (f459): head Ø≈165–176, centre (230,≈314–330), cap top y≈205, seat top ≈ 620, feet off the bottom edge. Horizon falls out of frame after step 2. | **Stepped push-in in 3 snaps**: 16.52–16.64 (f413–416), 17.40–17.52 (f435–438), 18.24–18.36 (f456–459). Each snap is 3–4 frames, then a static hold. Animation continues across the snaps. |
| 7 | 19.40–23.40 | 485–584 | GLASSES single | Shot-3 set-up (head (292,368), Ø≈108). | Static |
| 8 | 23.40–25.56 | 585–638 | CAP single | Shot-2 set-up (head (220,358), Ø≈106). | Static |
| 9 | 25.56–27.76 | 639–693 | GLASSES single | Head (280,362), Ø≈112. Nightstand x10–160, y525–645; window x0–215, y10–295. | Static |
| 10 | 27.76–(37.92) | 694–899 viewed | CAP single | Head (220,356), Ø≈100–106; seat top ≈ 545. | Static (continues past 36.00) |

Cut list confirmed from full-frame diffs: f62, 77, 96, 114, 180, 485, 585, 639, 694. These match the brief's 2.48, 3.08, 3.84, 4.56, 7.20, 19.40, 23.40, 25.56, 27.76. The GLASSES singles and CAP singles are the same two locked set-ups reused every time. They are mirror compositions:
- Each head sits at x≈220 (CAP) or x≈275–290 (GLASSES).
- Each head centre is at y≈358–364, which is 42–43% of frame height.
- The chair fills the lower-middle of the frame.
- The nightstand and plant are on the side the character faces.
- The window is behind, on the side the character faces.

---

## 2. Drawing-change logs

**Global timing facts (measured):**
- Drawing holds across 0–36 s: 245 drawings held 1 frame, 169 held 2, 30 held 3, 18 held 4, and a few longer holds (5–18 frames).
- During dialogue the mouth changes roughly every 1–2 frames (≈16–18 changes/s). Ones and twos are mixed irregularly, not on strict twos. This is consistent with an original ≈15 fps-on-twos/30 fps source resampled to 25; that is a hypothesis, not verified.
- **Most changes are mouth-only.** The diff bounding box is about 40x25 px around the mouth. Eyes/brows change separately (bounding box ≈ 55x35 px at the eyes).
- Body and arms hold for seconds between gestures.
- Arm gestures take **3–4 drawings**, mostly single-frame (1–1–1–2), and then hold.
- Blinks are 1–3 frames of closed-arc lids, often timed on a phrase end or with a gesture.

### Shot 1 (0.00–2.48): two-shot → GLASSES single, GLASSES speaking
- 0.00–0.24: GLASSES has a smug closed smile (upward curve) with angled brows. CAP is neutral: black oval eyes, short slightly-down flat mouth. Both are held; only GLASSES' mouth varies.
- 0.28: GLASSES starts talking (small O). Lip sync then runs on 1s/2s: O → open smile with top teeth → teeth → ...
- 0.68–0.76 (f17–19): CAP, drifting off screen-left, shows **half-lidded/closed eyes** (a flat lid line over the eyes). This is a blink/skeptical squint while exiting frame. CAP's body is held.
- 0.92–1.00: GLASSES closes his eyes behind the glasses (lid arcs) with an open grin. This is a pleased blink on a phrase.
- 1.08 (f27): puckered "ooh" mouth.
- 1.12 and 1.48 (f28, f37): **big open smile, white top-teeth band, red tongue**.
- 1.64 (f41): eyes closed (lids at mid-lens) plus **pursed/puckered lips** drawn as a black shape with lip bumps.
- 1.68–1.76: small O mouth with eyes open.
- 1.80 (x5): clenched-teeth grin.
- 2.00–2.20: **point gesture on the screen-left (near) arm.** Timeline:
  - 2.00 (x2): arm still on the armrest, mouth O.
  - 2.08 (f52): forearm lifts off the armrest. The hand leads, swinging out low and nearly straight.
  - 2.12 (x2): arm at about 30° up-forward, slightly bowed, no hand drawn yet.
  - 2.20 (f55): arm fully extended horizontally toward CAP at head-to-chest height. The **pointing hand** is a black mitten with an extended index finger and a thumb stub.
  - The point is held 2.20–3.28, across the cut into shot 3.
  - Upper arm and forearm are a single, slightly curved line; no elbow break once extended.
  - Body, legs and the other arm are held throughout.
- Brows through 1.48–2.48: thick curved arcs angled down toward the nose (sly/confident), plus a small hair curl at the top-left of the head.

### Shot 2 (2.48–3.08): CAP single, CAP speaking (1 short word, e.g. "Yes", by picture only)
- 2.48 (x2): neutral. No brows. Black oval eyes looking screen-right. Short flat mouth angled slightly down.
- 2.56: mouth opens to the clenched-teeth band.
- **2.64 (f66): head tilts back.** The cap brim rotates up about 10° while the whole head/cap rotates, with an open mouth (black interior, white top teeth, maroon tongue). This is the only head-attitude change in this shot.
- 2.68–2.76: mouth closes back through the teeth shape. Head settles.
- **2.92 (f73, x2): blink.** Both eyes are drawn as closed down-curving arcs with the mouth flat. It lands on the end of the word.
- 3.00 (x2): eyes open, neutral frown held.
- Arms rest on the armrests the whole shot. Body is held.

### Shot 3 (3.08–3.84): GLASSES single, GLASSES speaking
- 3.08: still pointing (continuity from shot 1), smug smile.
- 3.12–3.28: talks. Mouth is an open black rectangle with teeth.
- The pointing arm drops in 3 drawings:
  - 3.20: arm lowered to ~15° below horizontal, hand now open/mitten.
  - 3.24: forearm near the armrest.
  - 3.28: arm rests on the armrest.
- The brows lower into a frown during the talk.
- **3.56 (x3): half-lid/closed eyes** behind the lenses.
- 3.68 (x4): eyes reopen, brows angled.

### Shot 4 (3.84–4.56): CAP single — listening hold
- **One identical drawing held 18 frames** (3.84–4.52): neutral frown, eyes open looking screen-right, arms on the armrests, no brows.
- Pure held cel, not even a blink.

### Shot 5 (4.56–7.20): GLASSES single, GLASSES speaking (annoyed)
- **4.56 (x9): frown hold before speaking.** Brows are lowered hard into an angry V over the lenses. The mouth is a downturned arc. This is a thought-change beat that reads as "that's not good enough".
- 4.92–5.00 (x7): open angry mouth (black, top teeth band, maroon tongue), held about ¼ s.
- 5.28–5.48: **eyes half-closed** (lids across the lens middles, disdain) while talking. Clenched teeth, then open.
- 5.52–6.40: talking on 1s/2s. Brows stay angry. Arms held on the armrests.
- 6.48 (f162): **F/V mouth** (upper teeth over the lower lip, drawn as a row of white bumps).
- **Shrug gesture, 6.52–6.68:**
  - 6.52: both forearms lift.
  - 6.56 (x2): elbows bend and hands come up.
  - 6.64–6.68: **palms-up shrug**. Upper arms go down and out, forearms up, making a "V/W". Hands are small hooked cups, with no fingers articulated beyond 1–2 stubs.
  - The shrug is held 6.68–7.20 while talking. Blinks at 6.84–6.92; O mouth at 6.80 and 6.96.
- The legs never move.

### Shot 6 (7.20–19.40): CAP single → stepped push-in, CAP speaking
- **7.20: cut in with CAP's screen-right (far) arm already extended** forward at shoulder height, open-ended with no hand drawn. The line is slightly curved.
- Mouth neutral at 7.20. 7.24: mouth opens. **7.28: angry brows appear.** They are thin black strokes slanting down toward the centre and overlapping the top of each eye oval, cutting the ovals into wedges.
- The angry brows then persist for most of the shot.
- 7.52–7.64: O mouth.
- **Arm lowers in 4 drawings:**
  - 7.76 (x4): forearm dropping.
  - 7.92: forearm near horizontal.
  - 7.96: bowed.
  - 8.00: forearm lying on the armrest.
- **8.08 (x10): angry-brow listening/thinking hold** with the mouth closed flat, about 0.4 s.
- 8.48–8.52: talking.
- **8.56 (x3): eyes closed** (arc lids) with the mouth open.
- 8.68–9.24: talking. Clenched-teeth and O shapes.
- **Raised index finger ("one thing…"), 9.28–9.40:**
  - 9.28 (x2): screen-right forearm lifts, bent at the elbow.
  - 9.36: forearm vertical.
  - 9.40: **index finger up**, black finger shape with a fist stub.
  - The elbow stays near the armrest; the forearm leads.
  - The finger is held 9.40–11.72 (≈2.3 s) while the mouth and eyes keep animating.
- 9.52: F/V mouth (teeth on lip). 10.12–10.20 (x5): open. 11.36–11.48: blink.
- **Point at the interviewer, 11.76–11.84:**
  - 11.76: the arm swings forward/down from the raised finger.
  - 11.80: F/V mouth.
  - 11.84 (x6): **pointing hand** extended screen-right at chest height, elbow slightly bent.
  - 11.84 also has eyes closed and an F/V mouth. The emphatic beat lands with a blink.
- 12.08 (x10): point held, mouth open. The point stays held until 14.24.
- 13.56 (x3): pressed wavy lips (M/B/P).
- **14.28–14.48: F/V mouth, then the point pushes further.** The arm straightens to full length (14.40, x2) for emphasis, held to 15.36.
- **Arm drops, 15.40–15.56:**
  - 15.40: arm lowering.
  - 15.48: bent, with no hand.
  - 15.52: arm on the armrest.
  - 15.56: O mouth.
- 15.64 (x1) mouth closed. 15.68–15.76: eyes closed (half-lid arcs).
- 15.84–16.48: talking, with angry brows.
- **16.80–16.84: screen-right forearm lifts, with a limp hand hooked downward.** The hand is drawn as a small black mitten with the fingers dangling over the front of the armrest. It is held about 0.3 s, lowered, then repeated around 17.0–17.6 in the push-in frames. It is a small "come on" emphasis.
- 17.08–17.12: eyes closed and the mouth open.
- **17.36 (x2): wavy pressed mouth.**
- After push step 2 (17.52 on): the face is large, so the eyes and mouth read clearly:
  - 17.76–17.92: eyes closed.
  - 18.08 (x4): open.
  - 18.24–18.48: talking.
  - 18.56: O.
- **18.80 (x3): half-lidded disdain.** Two flat-topped half-ovals under a horizontal lid with a lower curve. Mouth: clenched teeth.
- 18.92–19.00 (x5): flat half-lids plus an open mouth.
- **19.24 (x4): final unimpressed hold.** Half-lidded eyes with flat lids and a short downturned mouth, before the cut.
- Throughout: the torso line, legs and screen-left arm (on the armrest) are held.

### Shot 7 (19.40–23.40): GLASSES single, GLASSES speaking
- **19.40 (x15): hold with the mouth open**, angry brows. This is the first 0.6 s held (a reaction/start beat), and there is no body change.
- 20.00 (x3): half-lids. 20.12: angry. 20.24: half-lids plus clenched teeth.
- 20.36 (x7): open.
- 20.64: teeth. 20.76: F/V. 20.80: pursed lips.
- 20.96: half-lid.
- 21.00–21.12: F/V (teeth on lip) with the eyes half-lidded.
- **21.20 (x1) and 21.24 (x4): half-lids plus a straight flat mouth** (a "come on" deadpan).
- 21.40–22.48: angry brows, talking. Shapes: O, open, teeth, frown arc (21.52), pursed lips.
- **22.48–22.56 (x6): half-lids plus a downturned wavy mouth.**
- 22.80 on: talking with pursed/O shapes. 23.20: half-lids.
- Arms rest on the armrests for the whole shot, and there is no gesture. The acting is face-only, carried by the brow/lid alternation.

### Shot 8 (23.40–25.56): CAP single, CAP speaking
- 23.40: **no brows**, neutral eyes, short frown mouth.
- 23.52–23.64: talking.
- **23.68–23.76: half-lids.**
- **23.80 (x4) → 23.96 (x13): half-lidded "bored/honest" eyes plus a downturned mouth, held about 0.5 s.**
- 24.48 (x2): eyes open, talking.
- 24.64 (x1): open mouth. 24.76–24.80: O.
- 24.92–24.96: half-lids plus open mouth.
- 25.00–25.12: angry brows return, clenched teeth.
- **25.24 (x8): angry-brow frown hold** to the cut.
- The arms and body never move.

### Shot 9 (25.56–27.76): GLASSES single, GLASSES speaking
- 25.56: angry, frown arc.
- 25.64: F/V. 25.68: pursed lips. 25.76–25.80: half-lids plus a frown arc.
- 26.00–26.80: talking, angry brows.
- 26.84–26.96: F/V with the eyes open. 27.00: half-lids.
- **Open-palm gesture, 27.08–27.12:**
  - 27.08 (x1): screen-left (near) forearm lifts off the armrest and extends forward and low toward CAP.
  - 27.12 (x2): extended to an **open palm up/forward**, drawn as a short hooked hand.
  - Held 27.12–27.76 while talking.
- 27.24: frown arc. 27.64–27.68: half-lids plus a frown.

### Shot 10 (27.76–36.00 of this range): CAP single, CAP speaking
- 27.76: clenched teeth. 27.80: open.
- **27.84 (x2): head tilt back.** The cap brim tilts up, the same drawing type as 2.64.
- 27.92–28.24: talking. 28.08–28.12: eyes closed.
- **Arm drape, 28.40–28.56:**
  - 28.40 (x2): screen-left (upstage/back) arm lifts. The elbow rises first and the hand trails.
  - 28.48: the arm bends up over the chair back.
  - 28.52: forearm lying across the top of the chair back.
  - **28.56 on: arm draped across the chair back** (a relaxed, confident posture), held to 29.64.
  - Mouth and eyes keep animating. Blink at 28.84 (x3).
- **Shrug, 29.64–29.84:**
  - 29.64: draped arm comes forward.
  - 29.68 (x2): both arms rising.
  - 29.76: forearms up.
  - 29.80: V arms.
  - **29.84 (x3): full palms-up shrug**, with the angry brows returning.
  - Held 29.84–30.32 while talking.
- **30.36–30.52: arms lower.**
  - 30.36: bending.
  - 30.40 (x2): far forearm crosses down.
  - 30.48: near horizontal.
  - 30.52 (x3): both arms on the armrests.
- 30.64–31.76: talking, angry brows. 31.20–31.24: eyes closed, wavy mouth.
- **Small palm-up flick, 31.80–31.96:**
  - 31.80: screen-right forearm lifts.
  - 31.84 (x3): hand turning up.
  - 31.96: open hand palm-up, forward-right.
  - Held to 32.56.
  - 32.64: forearm down. 32.68: on the armrest.
- 32.52: wavy lips. 32.76: F/V.
- 32.92: eyes closed plus teeth on lip.
- 33.00: F/V. 33.08 onward: talking.
- **33.56 (x14): closed-mouth angry-brow hold** (0.56 s). This is a pause.
- 34.12 (x3): eyes closed plus a frown.
- 34.24 (x3): angry frown.
- 34.36–34.56: talking.
- 34.64–34.68: eyes closed, twice (x1, x2).
- 34.80 (x4): angry.
- 35.00–35.24: talking.
- **35.28 (x7): angry frown hold.**
- 35.56: eyes closed. 35.68–35.96: talking. 35.96: wavy lips.

---

## 3. Style spec (from full-res and zoomed crops, CAP/GLASSES singles unless noted)

**Proportions (single set-up):**
- Head Ø ≈ 106 px, which is **12.5% of frame height**.
- Head centre y ≈ 358–364.
- Seat top y ≈ 545–560: the head centre is about 1.75 head-diameters above the seat.
- Neck/torso line is ≈ 1.1–1.3 head-diameters long from the chin to the seat.
- Feet at y ≈ 650–690 (1 head below the seat).
- Two-shot head Ø ≈ 84–90.

**Line work:**
- Pure black #000000 with anti-aliasing.
- **Head outline ≈ 4–5 px ≈ 4% of head Ø.**
- **Limbs and torso ≈ 6–7 px ≈ 6% of head Ø.** Limbs are thicker than the head outline, with round caps.
- Each limb is **one single uniform line**, with gentle bends at the elbow/knee and no tapering.
- Chair and furniture outlines are thin, 1–2 px, dark grey (#3x3x3x), about 1/4 of the character line weight.

**Head:**
- Perfect circle, flat fill **#CECECE** (light grey, slightly lighter than the wall #CBCBCB–#CDCBCC), no shading.

**CAP (respondent) face:**
- **Eyes are solid black vertical ovals, ≈12x22 px**, with no sclera and no highlight.
  - Gap between the eyes ≈ 16 px.
  - The eye pair is centred ≈ +26 px (≈0.25 Ø) toward the facing direction.
  - Eye centre is ≈ 20 px above the head centre.
- Mouth sits ≈ 20 px below the head centre, also offset toward the facing side.
- Brows are absent when neutral. Angry brows are thin black strokes slanting down toward the centre, overlapping the tops of the eye ovals so each eye reads as a wedge.
- Closed eyes: down-curving arcs ("◡" lids) about the eye width.
- Half-lid: horizontal lid line with a black half-oval below it, flat-topped.
- A few thin hair strokes poke out under the cap at the back.

**Cap:**
- Solid black dome covering the top ≈ 35% of the head.
- **Flat bill projecting toward the BACK of the head** (screen-left while CAP faces right), i.e. the cap is worn backwards. The bill is ≈ 0.55 Ø long.
- **Button:** small yellow ellipse **#F8EB63**, ≈ 6x9 px, at the crown top, toward the front.
- The cap tilts with the head on head-back beats (2.64, 27.84).

**GLASSES (interviewer) face:**
- Round wire glasses. Two lens circles ≈ 21–22 px Ø with thin black rims, a small bridge, and a temple line running back toward the ear.
- Lens fill is tinted pale blue-grey: gradient from **#D1E3E6** (light) to **#687B7E** (dark), median #798B8E.
- The eye shows as a dark pupil disc inside the lens. The upper lid line is drawn across the lens, lowered for half-lids.
- Brows are **thick curved arcs** tilted toward the centre (angry), plus 1–2 hair-curl strokes at the top of the head. Neutral brows are gentle raised arcs.

**Mouth set (both characters):**
- Outlined in black. Interior is black, with a **white top-teeth band (#F0–#FF)** and a **maroon/rose tongue #7F3E55–#9D3A50**. The tongue is brighter red in the smile mouths.
- Catalogue:
  1. Neutral: short line, slightly down.
  2. Smug closed smile curve (GLASSES).
  3. Wide open rectangle: black, teeth top, tongue bottom.
  4. **Clenched "H" teeth**: white band with a black centre line and a black outline.
  5. Small O: black oval, tiny tongue.
  6. Pursed/puckered lips: black with lip bumps.
  7. **F/V**: upper teeth drawn as white bumps over the lower lip.
  8. Wavy pressed line (M/B/P, disgust).
  9. Frown arc (GLASSES).
  10. Big open grin with teeth and red tongue (GLASSES, happy).
- Mouth width is ≈ 0.3–0.45 Ø.

**Body, arms, hands and legs:**
- The body is **one line from the chin to the seat**, slightly diagonal.
- Arms leave from just below the chin as two lines.
- Rest pose: upper arms angle down and outward to the elbows, forearms lie flat along the armrest tops. The near forearm is on the near arm; the far forearm is over the far arm.
- **Hands are only drawn when gesturing**, as small black filled shapes: pointing mitten (index finger plus thumb stub), raised index finger, hooked/limp mitten, cupped palm-up hook. At rest the arm just ends.
- Legs: thigh lines run forward horizontally over the seat top to the knee at the cushion front edge. Shins drop near-vertically (slightly forward). Feet are short forward strokes (≈0.3 Ø), with no shoes.
- The character sits *in* the chair: the chair back is behind the torso, the near arm block is beside the torso, and the thighs lie on the red seat top.

**Armchair (3/4 view, boxy, rounded corners):**
- **Mauve-grey #6F6363** on the outer faces: outer back, near arm front and outer faces.
- **Pale pink #ECD7D7** on the inner faces: inner back, inner arm faces, far arm top.
- **Seat top #8C595A** (dusty red), a thin strip.
- **Cushion front** is pale pink with a darker **#685758** band under it.
- **Base skirt #504542** on the front face, #6F6363 on the side.
- The back is taller than the arms by ≈ 0.6 Ø.
- **Floor shadow:** a flat dark ellipse **#3C3A38**, low opacity, under the chair and the nightstand.

**Nightstand:**
- Body and drawer faces **#444441**, drawer outlines darker.
- Two drawers, each with a round knob **#9D918A**.
- It sits beside the chair and faces camera straight-on, with a slight 3/4 top.

**Plant:**
- Terracotta cone pot, gradient **#A38F82** (lit side) to **#9B7458** (shade side).
- Grey-green stems, bright green leaves with a dark outline, magenta/pink flowers with a yellow centre, and tulip-like buds.

**Wall and window:**
- **Wall #CBCBCB–#CDCBCC**, with a faint vertical darker gradient near the corners (#C7C2C1 in the two-shot).
- **Window:** white glass #FCFCFC, dark grey frame **#534E50** with a thick top lintel, and a mullion cross dividing it into 4 panes.

**Floor:**
- Checkerboard of **#828282 (light) and #5A5E60 (dark)** tiles in strong 1-point perspective. Tile rows get taller toward the bottom of the frame (≈40 px near the horizon, ≈70 px at the bottom).
- The vanishing point is roughly centred behind the characters.
- The horizon is at y≈515–540 in singles.

**Shading:** none on the characters. Furniture has flat 2-tone faces only; the only shadows are the flat contact shadows under the furniture.

---

## 4. Example index (0–36 s only)

| Type | Time | Audience should understand | Gaze | Body support | Leading part | Changes | Holds | Silhouette | Mouth/eyelids | Overlap | Cut context |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Seated construction | 2.48 (f62), also 3.84 (f96) | Relaxed respondent at rest | Screen-right, to the interviewer | Thighs on the seat top, forearms flat on both armrests, torso line upright | — | nothing | everything | Round head plus 2 arms making a "Λ" to the armrests; legs make an "L" | Neutral short line, open oval eyes | — | Opening CAP single |
| Listening hold | 3.84–4.52 (f96, x18) | CAP just takes it, no reaction | Screen-right | Seated rest | — | none: a single held cel | all 18 frames | Same as rest | Flat frown, eyes open, no brows | none | Short insert between GLASSES lines |
| Thought change | 4.56 (x9) GLASSES; 8.08 (x10) CAP | Annoyance forming before speaking | At the other character | Rest | Brows (drop into V) | brows plus mouth set to frown | body/arms | Unchanged | Frown arc / closed flat mouth with angry brows | none | First drawing after a cut, held before the first mouth open |
| Interruption / cut-in on action | 7.20 (f180) | CAP jumps in mid-gesture | Screen-right | Seated, far arm already extended | Arm (already out when the cut happens) | brows appear 2 frames later (7.28), arm drops 7.76–8.00 | legs, torso | Long horizontal arm line breaks the silhouette | Opens 7.24; angry brows from 7.28 | Brows lag the cut by 2 frames | Cut into a pose already mid-gesture. No audio check done |
| Emphatic gesture | 9.28–9.40 raised finger; 11.76–11.84 point; 14.28–14.40 point extension | "One thing…" → "you!" | Screen-right | Seated; elbow stays low near the armrest for the finger | Forearm/hand (the elbow stays put) | arm in 2–3 single-frame drawings, then held for seconds | legs, torso, other arm | Vertical finger beside the head; then a horizontal arm with a black pointing hand | F/V and eyes closed on the landing frame (11.84) | Mouth keeps animating through the hold | Within a long CAP shot |
| Head turn/tilt | 2.64 (f66); 27.84 (f696) | Head tilts back on the emphatic word | Up-right | Seated | Head/cap as one unit (brim rotates up about 10°) | head angle for 1–2 drawings, then back | body | Bill angle changes | Open mouth | none | Mid-line |
| Mouth articulation | 5.00–6.40; 8.68–9.24; 18.08–18.60 (large, after push-in) | Lip sync | — | — | Mouth only | Mouth on 1s/2s from the 10-shape set; F/V and pursed shapes are used as accents | Everything else | — | See §3 | Blinks overlap speech | — |
| Punchline / deadpan reaction | 18.80–19.36 (half-lids, x3 → x5 → x4); 23.80–24.44 (x4 + x13 half-lid frown); 21.24 GLASSES (x4) | "Unimpressed / honest" deadpan | Screen-right, level | Seated rest, nothing moves | Eyelids (drop to flat half-lids) | lids then mouth to frown, then hold | body | Unchanged | Flat-topped half-lids plus downturned short mouth | none | Held into the cut (19.40) or after the line |

Other useful poses in range:
- Palms-up shrug (6.64–7.20 GLASSES; 29.84–30.32 CAP).
- Arm draped over the chair back (28.56–29.64 CAP, confident).
- Open-palm offer (27.12–27.76 GLASSES).
- Hooked limp-hand flick (16.80–17.6 CAP).

---

## 5. Coverage statement
- **Every-frame (distinct-drawing) density, 0.00–35.96 s (f0–f899): 100% of frames accounted for.** All 480 distinct drawings were opened and viewed in labeled contact sheets. The remaining 420 frames were verified as held duplicates by pixel diff (≤50 px changed, gray threshold 40); they were not individually viewed.
- Sheet scales:
  - f0–61: full frame at 0.4x (192 px wide).
  - f0–36: head band at 0.8x.
  - f36–61: 1.1x crop.
  - f62–329: 340x260 crop at 0.8x.
  - f330–484: 360x360 crop at 0.62x.
  - f485–899: 340x260 crop at 0.72x.
  - f705–765: re-viewed at 0.6x to confirm the arm-drape/shrug order.
- Face/hand details are only reliable in the zoomed crops below. In the other tiles, mouth identification (teeth vs O vs F/V) is from tiles where the face is ≈60–80 px wide. Small-mouth calls have moderate confidence.
- **Zoomed / full-res crops viewed:**
  - CAP faces, 2.5x: f62, 66, 73, 188, 228, 239, 312, 470, 480, 839.
  - GLASSES faces, 2.5x: f37, 41, 114, 124, 132, 162, 506, 556, 564, 677.
  - Body/hands, 1.3x: f55, 166, 180, 236, 302, 421, 712, 762, 799, 677.
  - Chair/nightstand, 2x: f62.
  - Full-frame grid overlays: f0, 40, 62, 77, 96, 114, 180, 420, 445, 470, 485, 585, 639, 694.
- **Not done:** no audio listening; no normal-speed playback; speaker identity comes from mouth motion only. Push-in head sizes after steps 2–3 are ±10 px estimates (Hough fits and grid disagree slightly). Colours are 3x3 medians from compressed video (±3 per channel).
