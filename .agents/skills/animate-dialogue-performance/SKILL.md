---
name: animate-dialogue-performance
description: Design or repair HonestInterview acting — beat intentions, pose choices, gesture timing, holds, facial expressions and comedy timing in the minimal seated stick-figure style. Use whenever a shot's acting, pose, gesture, reaction, blink, hold or expression is being created or criticised, even if the request is phrased as "make it less stiff" or "fix this shot".
---

# Animate Dialogue Performance

## Inputs

- Acting script (v5: `ProductionFull_v5\scripts\script_film.py` + `script_film_tail.py`), pose and
  expression vocabulary (`poses.py`), reference gesture logs, dialogue turns.

## Procedure

1. Write the intention next to every beat (asking, interrupted, insisting, lounging, steamrolling,
   refusing, outraged, smug reveal). Body changes follow thought changes, not every stressed word.
2. Match the reference's economy: hold the body for seconds; a gesture is 2-4 drawings on ones
   (hand or forearm leads, elbow stays near the armrest, no hand drawn until arrival), then a hold
   while the mouth keeps going; drop quickly. Deadpan holds (18-frame held cel) are jokes, not gaps.
3. Faces act by instant swaps of lids, brows and mouth emotion; blinks (1-3 frames) land on phrase
   ends or gesture arrivals — never on a timer, never as idle noise.
4. Construction checks on every new pose: head joins torso line at the chin, arms leave just below
   the chin, forearms rest on armrest tops, thighs over the seat to the cushion front, shins to the
   floor. Render a pose sheet (`build_posesheet.py`) for new poses before using them in a shot.
5. Comedy structure that worked: instant "Yes" with one head jut; interviewer's expectation collapses
   in stages (smile, arm, lids, brows); camera snaps on "ten / billion / dollars"; interruption cuts
   in with the arm already up; the bigger reveal ("Thousand") played smaller; first smile saved for
   "entrepreneur".
6. Head tilt sign: +tilt rotates the head toward the listener (clockwise for the screen-right facer),
   as in the reference jut at 2.64 s.

## Outputs

Updated script beats, pose/expression vocabulary, rendered previews compared with the reference.

## Failure cases

- If a pose reads wrong (e.g. raised finger at the chin reads as "thinking"), redraw the pose, don't
  tweak timing around it.
- Don't add gestures to fill time, flail, or loop idles; don't add props or gags.
