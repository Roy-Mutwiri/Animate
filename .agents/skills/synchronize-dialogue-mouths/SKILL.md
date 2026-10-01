---
name: synchronize-dialogue-mouths
description: Build, map, verify and correct HonestInterview mouth drawings and dialogue timing against the original audio (Rhubarb cues, speaker turns, jaw opening, frame conversion). Use whenever lip sync, mouth shapes, speaker assignment, cue files, "mouth frozen/flapping", or dialogue timing is involved, even if only one phrase is mentioned.
---

# Synchronize Dialogue Mouths

## Inputs

- Final audio: `D:\Animate\Sounds\Bro was so honest.mp3` (never edited or stretched).
- Validated turns and cues (v5): `ProductionFull_v5\assets\dialogue_turns.json`, `cap_rhubarb.json`,
  `nocap_rhubarb.json`, speaker analysis WAVs (full length, other speaker silenced, original timing).

## Procedure

1. **Trust turns only after picture + voice agree.** v4's split was wrong in several places
   ("Listen here." 7.20 s is CAP; 58-64 s is four turns: CAP "…for five", NOCAP "Five billion?",
   CAP "Thousand.", NOCAP "What are you?"). The reference video's animated mouths are strong speaker
   evidence because it animates this exact audio.
2. **One frame policy**: global zero-based frame = `floor(t*24 + 0.5)`; a cue covers
   `[F(start), F(end))`; a cue collapsing to zero frames is dropped unless it is A (closure) or F
   (pucker), which keep their start frame. Never round durations and accumulate.
3. **Rhubarb labels lip shape, not jaw.** pocketSphinx+transcript labels many vowels `B`; held 6-10
   frames it reads as a frozen mouth. Run the jaw pass (`scripts/jaw.py`): per-frame speaker loudness
   relative to the phrase-local peak opens B/C/D; closures, rounds, F/V and tongue shapes keep their
   labels so contacts survive. Record how many frames it changed.
4. **Drawings** (shared family, emotion variants change corners not articulation): X rest line,
   A pressed/wavy lips, B clenched-teeth rectangle, C open (black inside, white top-teeth band,
   maroon tongue), D wide open, E small O, F black lips around a red centre, G F/V teeth over lip,
   H tongue up. Reference mouths are ~0.35 head diameter wide.
5. **Verify inside the source document**: `scripts/verify_lipsync.py <xfl_dir>` decodes every
   mouth-layer pick and reports mismatches vs the planned track, speech shapes outside the speaker's
   windows, and deliberate overrides. Target: 0 unexplained mismatches, 0 stray speech shapes.
6. **Look at phrases frame by frame**: `scripts/mouth_sheet.py WHO t0 t1 out.png` labels each frame
   with cue and word; check beginning/middle/end of the film, closures, rounds, holds after lines.
7. Overrides (held smiles, gritted teeth, drawn-out "you?") must not keep a mouth open in silence
   longer than the performance justifies — e.g. trim to ~5 frames past the word.

## Outputs

Cue/jaw tracks, verification report (`review/lipsync_verify_*.md`), phrase sheets, correction log.

## Failure cases

- No tool here presents audio to the model: say so. Waveform, cue and frame checks are evidence of
  alignment, not proof of natural-looking speech.
- Diagnose the failing layer (recognition, speaker isolation, offset, frame conversion, drawing
  mapping, export) instead of rerunning the recogniser.
