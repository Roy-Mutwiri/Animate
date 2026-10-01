# HonestInterview: dialogue turn and lip-sync analysis (ReviewV5)

Audio: `D:\Animate\Sounds\Bro was so honest.mp3` (70.889 s). Reference: `D:\Animate\Goal\Bro was so honest.mp4` (25 fps, offset about +0.001 s).
Note: `HONEST_INTERVIEW_PRODUCTION_DIRECTIVE.md` is still missing, so this work follows the task brief only.
**No listening was done.** Every call below comes from signal analysis, ASR and inspection of reference frames.

## Method
- **Envelope.** The MP3 was decoded to 16 kHz mono. It is sample-identical to `ProductionFull_v4/assets/full_audio_mono_16k.wav`. From it I computed a 10 ms RMS envelope, YIN F0 (numpy), librosa pyin F0 and 20 MFCCs.
- **Re-transcription.** faster-whisper large-v3 (local cache) was run with word timestamps: on the full file (greedy and beam 5), on isolated clips of the ambiguous spots, and once with a prompt that makes it spell numbers as words. Results: `_fw_large_v3.json`, `_fw_clips.json`, `_fw_clips_spelled.json`.
- **Reference video.**
  - Frame differences found the shot cuts (f62, 77, 96, 114, 180, 485, 585, 639, 694, 948, 991, 1096, 1187, 1255, 1310, 1406, 1459, 1519, 1562, 1588, 1617).
  - A Hough-circle head detector plus a lower-face "ink" measure gave mouth activity on all 1775 frames (`_mouth.json`).
  - I then inspected face-crop sheets frame by frame.
- **Phrase bounds.** The envelope threshold is max(-38 dB, local 10th percentile + 8 dB). Each bound was then checked by hand on 10 ms dumps and mouth frames.
- **Accuracy.**
  - Before 48.8 s: about ±0.02 s.
  - After 48.8 s: background music lifts the floor to about -30 dB, so bounds are about ±0.03–0.05 s.
  - Word times: large-v3 timestamps clipped into the phrase bounds, typically ±0.1 s. Some were set by hand from energy and mouth frames (billion/dollars at 17–18.5, Hey, Guess what, Five billion, What are you, entrepreneur line).

## Turn table (MP3 seconds)
| # | Spk | Start | End | Text |
|---|---|---|---|---|
| 1 | NOCAP | 0.25 | 0.47 | Okay, |
| 2 | NOCAP | 0.70 | 2.45 | for ten billion dollars, would you— |
| 3 | CAP | 2.56 | 2.87 | Yes. |
| 4 | NOCAP | 4.84 | 7.06 | Um, no, I didn't finish the question, I— |
| 5 | CAP | 7.20 | 7.47 | Listen here. |
| 6 | CAP | 8.86 | 9.41 | There is nothing, |
| 7 | CAP | 10.17 | 11.90 | and I mean nothing, |
| 8 | CAP | 12.54 | 14.42 | that could come out of that little pie hole of yours |
| 9 | CAP | 15.05 | 18.48 | to make me turn down ten billion dollars. |
| 10 | NOCAP | 20.62 | 23.35 | Even if one random person had to die? |
| 11 | CAP | 23.44 | 23.84 | Yes. |
| 12 | CAP | 24.04 | 25.66 | The answer is yes. |
| 13 | NOCAP | 25.94 | 27.56 | Okay, what if it was someone you knew? |
| 14 | CAP | 27.74 | 30.38 | Yes. Take my aunt. Take my grandma. |
| 15 | CAP | 30.64 | 31.78 | Hell, you could blow the block up. |
| 16 | CAP | 31.90 | 37.45 | Can you even fathom how much money ten billion dollars is? |
| 17 | NOCAP | 37.92 | 39.30 | Oh, it's just a hypothetical. |
| 18 | CAP | 39.42 | 40.93 | And if it was a reality, |
| 19 | CAP | 41.32 | 43.49 | I'd be first in line. |
| 20 | NOCAP | 43.92 | 47.42 | You're talking about human lives for ten billion dollars. What would— |
| 21 | CAP | 47.46 | 48.71 | Hey, hey, hey, hey. |
| 22 | CAP | 49.48 | 49.82 | Guess what? |
| 23 | NOCAP | 50.32 | 52.08 | I don't want to guess. Don't make me guess. |
| 24 | CAP | 52.33 | 55.10 | Oh, come on. You gotta be curious about what I'm going to tell you. |
| 25 | NOCAP | 56.94 | 57.12 | What? |
| 26 | CAP | 58.55 | 59.78 | I would have did it for five. |
| 27 | NOCAP | 61.10 | 62.08 | Five billion? |
| 28 | CAP | 62.51 | 63.10 | Thousand. |
| 29 | NOCAP | 63.40 | 64.00 | What are you? |
| 30 | CAP | 64.66 | 65.55 | Oh, that's a good question. |
| 31 | CAP | 66.68 | 70.46 | I guess you can call me an entrepreneur. |

## Ambiguous turns: evidence
- **"Um, no, I didn't finish the question, I— / Listen here."** (4.84–7.06 NOCAP, 7.20–7.47 CAP)
  - large-v3 hears "Um, no, … question, I-" and then, as a separate segment, "Listen here." The old transcript's "I'd listen here" merged the two.
  - There is an energy gap at 7.07–7.19 s.
  - NOCAP's last open mouth is f174–176 (6.96–7.04). The cut to CAP comes at f180 (7.20), and CAP's mouth opens at f181, f184 and f188.
  - **Verdict:** CAP interrupts with "Listen here." The v4 split gave this line to NOCAP.
- **"Okay" at 0.25.** This is a two-shot. NOCAP's mouth changes from a smile to an "O" at f7–f9 and then an open grin at f10–f14. CAP's mouth stays flat.
- **"…ten billion dollars" end (18.48).** CAP shows a B/M closure at f434 (17.36, "b" of billion), a wide "dol-" at f456–461 and O shapes until f467.
  - The CAP open-mouth hold at f474–479 (18.96–19.16) sits over weak audio (-31 dB). I treat it as a breath or hold, not a word.
- **"What would—" (NOCAP, ~47.12–47.42).**
  - Beam-5 large-v3 hears "dollars. What would-".
  - NOCAP's mouth makes O shapes at f1178–1184, then the cut to CAP comes at f1187 with CAP's mouth already open.
  - The two turns abut. There may be an overlap of 0.05 s or less.
- **"What?" (56.94–57.12, NOCAP).**
  - CAP's mouth goes still after about 55.2.
  - NOCAP's shot starts at f1406. NOCAP's mouth is still until f1420, then speaks at f1420–1432 (56.80–57.28).
  - There is a loud burst at 57.00–57.08.
  - The old 55.12–57.12 window was about 1.8 s too early at the start.
- **"I would have did it for five."** (58.55–59.78, CAP) Both the full-file and clip passes of large-v3 end the line with "five." The "$5 billion?" in the old transcript merged this line with NOCAP's reply.
- **"Five billion?"** (61.10–62.08, NOCAP)
  - It is a high-pitched outburst: YIN median 229 Hz, reaching about 400 Hz.
  - NOCAP's shot runs f1519–1561. The mouth is still until f1527, then goes teeth → open → closure ("b") → open → O until f1551.
  - The old CAP cue file has speech mouths here.
- **"Thousand."** (62.51–63.10, CAP)
  - The cut to CAP is at f1562. CAP's mouth opens at f1564–1575 and again at f1581–1584 (a hold/tail to 63.36).
  - The clip passes say "Thousand." The full-file pass wrote "$1,000".
  - "A thousand" cannot be ruled out without listening.
  - The old split gave this to NOCAP.
- **"What are you?"** (63.40–64.00, NOCAP)
  - The audio onset at 63.40–63.50 comes about 0.1 s before the cut to NOCAP at f1588.
  - NOCAP's mouth makes O / open / O shapes at f1588–1606.
- **"Oh, that's a good question."** (64.66–65.55, CAP) The cut to CAP is at f1617 (64.68) with the mouth open immediately.
- **Laughs and breaths.** No clear laugh was found. There is a breath or hold at 18.77–19.06 (CAP), and music from about 48.8 s to the end.

## Pitch and voice evidence per speaker
YIN, voiced frames with confidence > 0.85, 66–450 Hz, frames above -35 dB:

| Speaker | Frames | Median | P10–P90 | IQR |
|---|---|---|---|---|
| CAP | 507 | 100 Hz | 82–167 | 86–128 |
| NOCAP | 488 | 123 Hz | 95–226 | 104–191 |
| CAP, before 48.8 s | 372 | 102 Hz | 82–167 | — |
| NOCAP, before 48.8 s | 420 | 117 Hz | 93–208 | — |

- **Pitch:** NOCAP is usually higher. Their calm lines sit at about 105–145 Hz and the shouted ones at 184–229 Hz. CAP's calm lines sit at about 85–120 Hz.
- **Where pitch does not help:** The ranges overlap. Pitch cannot separate the raised-voice exchange at 43.9–48.7 (NOCAP 184 Hz, CAP 177 Hz), and it is unreliable under the music.
- **MFCC test:** Each turn was held out in turn and assigned to the nearer speaker average, using mean MFCCs. It agreed with the final labels on 27 of 31 turns.
  - The 4 disagreements are #8 (margin -0.21, marginal), #23, #25 and #29. The last three fall in the music section, where the MFCCs are dominated by the music.
- **Weight given:** Voice features support the split but are weak. Speaker calls rest mainly on reference mouth activity, shot structure and the ASR segmentation.
- Per-turn values are in `voice_evidence.json` and in the `voice` field of `dialogue_turns.json`.

## Rhubarb: existing v4 cue files
`ProductionFull_v4/assets/*_rhubarb_full.json`:
- **Structure:**
  - Ordered, contiguous and nonnegative: interviewer has 128 cues, respondent 197.
  - Metadata duration is 70.88. The WAVs exist, are 16 kHz mono PCM and are 70.889 s long; the difference is rounding.
  - The soundFile paths are correct.
- **Wrong-speaker cues:**
  - Interviewer file: speech mouths during CAP's "Listen here" (0.27 s), CAP's "Thousand" (0.59 s) and CAP's "And if…" (0.09 s).
  - Interviewer file: NOCAP's "Five billion?" has only 4% coverage.
  - Respondent file: speech mouths during NOCAP's "Five billion?" (0.98 s) and the end of NOCAP's line at 43.9–47.4 (0.26 s).
  - Respondent file: CAP's "Listen here" and "Thousand" have no coverage.
- **Timing and text:** The v4 `lines` carry the same errors. They also have "What?" at 55.12–57.12 and the wrong text in the 58–65 s block.

## Rhubarb: new analysis
- **Analysis WAVs:** `cap_analysis.wav` and `nocap_analysis.wav`, 16 kHz mono PCM16, 70.889 s, original timing.
  - Each keeps its own speaker's phrases from start-0.04 to end+0.08 s, trimmed so it never crosses into the other speaker's phrase, with 5 ms fades. Everything else is digital silence.
  - Transcripts: `cap_transcript.txt` and `nocap_transcript.txt`.
- **Runs:** Rhubarb 1.14.0 with `-f json --extendedShapes GHX`, once with `-r phonetic` and once with `-r pocketSphinx --dialogFile`.

| Run | Cues | Speech mouths outside own windows | Speech during other speaker | Min phrase coverage |
|---|---|---|---|---|
| cap phonetic | 226 | 34 cues (mostly B lead-in/out, 0.01–0.14 s) | 0.03 s | 0.96 |
| cap pocketSphinx+dialog | 210 | 7 cues (≤0.10 s each) | none | 0.91 |
| nocap phonetic | 144 | 18 cues | 0.02 s ×2 | 1.00 |
| nocap pocketSphinx+dialog | 129 | 4 cues | none | 0.94 |

- **Choice:** pocketSphinx with `--dialogFile` for both speakers. With the known transcript, recognition is word-constrained. It spills far less into silence, puts no speech mouths on the other speaker, and gives fewer and longer cues (mean 0.185 s for CAP) that read less like flapping.
  - Phonetic mode adds B cues at almost every phrase edge.
  - Coverage of the chosen runs is still 0.91 or better on every phrase.
- **Cleanup:** The chosen runs were post-processed so that any speech cue outside the speaker's padded phrase windows becomes X.
  - This changed 7 cue fragments for CAP and 4 for NOCAP.
  - Output: `cap_rhubarb.json` and `nocap_rhubarb.json`. The raw outputs are kept (`*_rhubarb_pocketsphinx.json`, `*_rhubarb_phonetic.json`).
- **Final validation:**
  - Both files are ordered, contiguous and nonnegative, ending at 70.88.
  - CAP has 212 cues and NOCAP 130.
  - No speech cue falls outside its own windows, and none falls during the other speaker's lines.
- **Limitation:** The mouth shapes themselves were not checked against rendered animation or by listening.

## Reference frames I inspected directly
- The overview sheet `ov_0_71.png`: 1 frame per second over 0–70 s.
- `probe.png`: 0.2, 2.7, 5.0 and 10.0 s.
- Face-crop sheets, every frame:
  - f0–19 (`crop_0000_0020.png`)
  - f58–77 (`crop_0058_0078.png`)
  - f165–199 (`crop_0165_0200.png`)
  - f428–487 (`crop_0428_0488.png`)
  - f495–519 (`crop_0495_0520.png`)
  - f1165–1194 (`crop_1165_1195.png`)
  - f1370–1439 (`crop_1370_1440.png`)
  - f1515–1624 (`crop_1515_1625.png`)
- All other frames were covered only by the automatic mouth-ink metric and the cut detector, not by eye.

## Files
- `D:\Animate\Projects\HonestInterview\ReviewV5\analysis\`:
  - Main outputs: `dialogue_turns.json`, `dialogue_report.md`, `cap_analysis.wav`, `nocap_analysis.wav`, `cap_transcript.txt`, `nocap_transcript.txt`, `cap_rhubarb.json`, `nocap_rhubarb.json`
  - Raw Rhubarb outputs: `*_rhubarb_phonetic.json`, `*_rhubarb_pocketsphinx.json`
  - Evidence: `voice_evidence.json`, `_rhubarb_validation_raw.json`, the ASR JSONs, and the crop sheets
- No originals were modified.
