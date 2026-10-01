from __future__ import annotations

import json
import math
import struct
import subprocess
import wave
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(r"D:\Animate\Projects\HonestInterview\ProductionFull_v3")
ASSETS = ROOT / "assets"
FRAMES = ROOT / "frames"
PREVIEWS = ROOT / "previews"
REVIEW = ROOT / "reference_review"
EXPORTS = ROOT / "exports"
EDITABLE = ROOT / "editable"
SCRIPTS = ROOT / "scripts"
SOURCE_AUDIO = Path(r"D:\Animate\Sounds\Bro was so honest.mp3")
RHUBARB = Path(r"D:\Animate\Projects\HonestInterview\tools\Rhubarb-Lip-Sync-1.14.0-Windows\rhubarb.exe")

W, H, FPS = 1080, 1920, 24
AUDIO_DURATION = 70.889070
FRAME_COUNT = math.ceil(AUDIO_DURATION * FPS)


@dataclass(frozen=True)
class Line:
    start: float
    end: float
    speaker: str
    text: str
    intent: str


@dataclass(frozen=True)
class Shot:
    start: float
    end: float
    name: str
    framing: str
    purpose: str


LINES = [
    Line(0.00, 2.34, "interviewer", "Okay, for $10 billion, would you", "asking"),
    Line(2.56, 2.82, "respondent", "Yes.", "interrupting"),
    Line(4.44, 7.70, "interviewer", "Um, I didn't finish the question. I'd listen here.", "objecting"),
    Line(8.64, 18.72, "respondent", "There was nothing. And I mean nothing that could come out of that little pie hole of yours to make me turn down $10 billion.", "insisting"),
    Line(20.48, 23.44, "interviewer", "Even if one random person had to die?", "testing"),
    Line(23.44, 25.12, "respondent", "Yes. The answer is yes.", "flat_yes"),
    Line(25.84, 27.60, "interviewer", "Okay, what if it was someone you knew?", "pressing"),
    Line(27.60, 37.36, "respondent", "Yes, take my aunt, take my grandma, hell, you could blow the block up. Can you even fathom how much money $10 billion is?", "escalating"),
    Line(38.00, 39.44, "interviewer", "Oh, it's just a hypothetical.", "uneasy"),
    Line(39.44, 43.76, "respondent", "And if it was a reality, I'd be first in line.", "doubling_down"),
    Line(43.76, 47.12, "interviewer", "You're talking about human lives for $10 billion.", "moral"),
    Line(47.12, 49.84, "respondent", "Hey, hey, hey, hey. Guess what?", "baiting"),
    Line(50.40, 52.16, "interviewer", "I don't want to guess. Don't make me guess.", "refusing"),
    Line(52.16, 55.12, "respondent", "Oh, come on. You got to be curious about what I'm going to tell you.", "baiting"),
    Line(55.12, 57.12, "interviewer", "What?", "relenting"),
    Line(58.40, 62.08, "respondent", "I would have did it for $5 billion?", "reveal"),
    Line(62.08, 64.56, "interviewer", "$1,000. What are you?", "shocked"),
    Line(64.56, 65.60, "respondent", "Oh, that's a good question.", "thinking"),
    Line(66.56, 70.32, "respondent", "I guess you can call me an entrepreneur.", "punchline"),
]

SHOTS = [
    Shot(0.00, 2.44, "setup_two", "two", "question setup"),
    Shot(2.44, 4.44, "yes_close", "respondent", "interruption and silent hold"),
    Shot(4.44, 8.05, "object_close", "interviewer", "objecting reaction"),
    Shot(8.05, 18.95, "nothing_close", "respondent", "respondent explains absolute certainty"),
    Shot(18.95, 20.48, "pause_two", "two", "breath before moral escalation"),
    Shot(20.48, 23.44, "random_person", "interviewer", "question close"),
    Shot(23.44, 25.60, "yes_again", "respondent", "flat immediate yes"),
    Shot(25.60, 27.60, "someone_known", "interviewer", "more personal challenge"),
    Shot(27.60, 37.60, "family_block", "respondent", "respondent escalates with gestures"),
    Shot(37.60, 39.44, "hypothetical", "interviewer", "weak correction"),
    Shot(39.44, 43.76, "first_line", "respondent", "smug doubling down"),
    Shot(43.76, 47.12, "human_lives", "interviewer", "moral objection"),
    Shot(47.12, 49.84, "guess_what", "respondent", "teasing setup"),
    Shot(49.84, 52.16, "dont_guess", "interviewer", "annoyed refusal"),
    Shot(52.16, 55.12, "curious", "respondent", "baiting"),
    Shot(55.12, 58.40, "what_hold", "interviewer", "reluctant what and pause"),
    Shot(58.40, 62.08, "five_billion", "respondent", "almost punchline"),
    Shot(62.08, 64.56, "one_thousand", "interviewer", "shocked interruption"),
    Shot(64.56, 70.889, "entrepreneur", "respondent", "final punchline"),
]


def seconds_to_frame(t: float) -> int:
    return max(0, min(FRAME_COUNT - 1, int(round(t * FPS))))


def line_at(t: float):
    for line in LINES:
        if line.start <= t < line.end:
            return line
    return None


def shot_at(t: float) -> Shot:
    for shot in SHOTS:
        if shot.start <= t < shot.end:
            return shot
    return SHOTS[-1]


def isolate_speaker_wavs():
    src = ASSETS / "full_audio_mono_16k.wav"
    if not src.exists():
        subprocess.run([
            "ffmpeg", "-y", "-i", str(SOURCE_AUDIO), "-ac", "1", "-ar", "16000", str(src)
        ], check=True)
    with wave.open(str(src), "rb") as wf:
        params = wf.getparams()
        frames = wf.readframes(wf.getnframes())
    samples = list(struct.unpack("<" + "h" * (len(frames) // 2), frames))
    sr = params.framerate
    for speaker in ["interviewer", "respondent"]:
        keep = [False] * len(samples)
        for line in LINES:
            if line.speaker == speaker:
                a = max(0, int((line.start - 0.04) * sr))
                b = min(len(samples), int((line.end + 0.06) * sr))
                for i in range(a, b):
                    keep[i] = True
        out_samples = [s if keep[i] else 0 for i, s in enumerate(samples)]
        out_path = ASSETS / f"{speaker}_full_analysis.wav"
        with wave.open(str(out_path), "wb") as wf:
            wf.setparams(params)
            wf.writeframes(struct.pack("<" + "h" * len(out_samples), *out_samples))


def run_rhubarb():
    isolate_speaker_wavs()
    for speaker in ["interviewer", "respondent"]:
        wav = ASSETS / f"{speaker}_full_analysis.wav"
        out = ASSETS / f"{speaker}_rhubarb_full.json"
        if out.exists():
            continue
        subprocess.run([str(RHUBARB), "-f", "json", "-o", str(out), str(wav)], check=True)


def load_cues():
    run_rhubarb()
    cues = {}
    for speaker in ["interviewer", "respondent"]:
        data = json.loads((ASSETS / f"{speaker}_rhubarb_full.json").read_text(encoding="utf-8"))
        cues[speaker] = data["mouthCues"]
    return cues


def mouth_value(cues, speaker, t):
    line = line_at(t)
    if not line or line.speaker != speaker:
        return "X"
    if t < line.start + 0.03 or t > line.end - 0.06:
        return "X"
    for cue in cues[speaker]:
        if cue["start"] <= t < cue["end"]:
            # Suppress tiny chatter at phrase boundaries and treat B/M/P as clear closures.
            if cue["end"] - cue["start"] < 0.045:
                return "X"
            return cue["value"]
    return "X"


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(a, b, t):
    if a == b:
        return 0.0
    x = clamp((t - a) / (b - a))
    return x * x * (3 - 2 * x)


def active_silence(t):
    return any(a <= t < b for a, b in [(2.854, 4.848), (7.352, 8.612), (18.892, 20.627), (37.584, 37.933), (43.570, 43.934), (55.601, 55.932), (57.436, 57.828)])


def draw_bg(draw):
    draw.rectangle([0, 0, W, H], fill="#d0ceca")
    draw.rectangle([0, 1328, W, H], fill="#858e84")
    for x in range(-360, 1340, 210):
        draw.line([(x, 1328), (x + 470, H)], fill="#747d75", width=3)
    for y in [1435, 1595, 1755]:
        draw.line([(0, y), (W, y - 60)], fill="#778077", width=3)
    draw.rectangle([690, 150, 920, 430], fill="#faf9f2", outline="#4a4642", width=7)
    draw.line([(805, 150), (805, 430)], fill="#85827d", width=4)
    draw.line([(690, 285), (920, 285)], fill="#85827d", width=4)


def draw_table(draw, x=540, y=1018, s=1.0):
    draw.rectangle([x-100*s, y, x+105*s, y+155*s], fill="#45453f", outline="#181310", width=int(5*s))
    for yy in [32, 96]:
        draw.rectangle([x-75*s, y+yy*s, x+75*s, y+(yy+45)*s], fill="#373832", outline="#181310", width=int(4*s))
        draw.ellipse([x-7*s, y+(yy+17)*s, x+7*s, y+(yy+31)*s], fill="#b69b92", outline="#181310", width=int(2*s))
    pot = [(x-38*s, y-15*s), (x+40*s, y-15*s), (x+24*s, y+42*s), (x-24*s, y+42*s)]
    draw.polygon(pot, fill="#aa7c56")
    draw.line(pot + [pot[0]], fill="#5b4438", width=int(4*s))
    for a in [-70, -42, -12, 18, 48, 68]:
        ex = x + math.cos(math.radians(a))*78*s
        ey = y - 5*s + math.sin(math.radians(a))*95*s
        draw.line([(x, y-2*s), (ex, ey)], fill="#2a9440", width=int(5*s))
        draw.ellipse([ex-15*s, ey-13*s, ex+15*s, ey+13*s], fill="#ed82ee", outline="#6f526f", width=int(2*s))


def line(draw, pts, width=8):
    draw.line(pts, fill="#181310", width=width, joint="curve")


def chair(draw, x, y, s, pale):
    back = "#a39390" if not pale else "#efd4d0"
    side = "#73625e"
    seat = "#c9b1ae" if not pale else "#f5d7d5"
    dark = "#635550"
    o = "#181310"
    draw.polygon([(x-160*s, y-210*s), (x+145*s, y-215*s), (x+162*s, y+75*s), (x-150*s, y+82*s)], fill=back, outline=o)
    draw.line([(x-160*s, y-210*s), (x+145*s, y-215*s), (x+162*s, y+75*s), (x-150*s, y+82*s), (x-160*s, y-210*s)], fill=o, width=int(7*s))
    draw.polygon([(x-255*s, y-35*s), (x-150*s, y-58*s), (x-150*s, y+218*s), (x-255*s, y+232*s)], fill=side, outline=o)
    draw.polygon([(x+125*s, y-58*s), (x+262*s, y-28*s), (x+262*s, y+214*s), (x+132*s, y+195*s)], fill=side, outline=o)
    draw.polygon([(x-148*s, y+105*s), (x+126*s, y+92*s), (x+202*s, y+132*s), (x-205*s, y+150*s)], fill=seat, outline=o)
    draw.polygon([(x-190*s, y+148*s), (x+182*s, y+132*s), (x+176*s, y+265*s), (x-187*s, y+246*s)], fill=dark, outline=o)


def state_for(who, t):
    line_obj = line_at(t)
    speaking = line_obj and line_obj.speaker == who and not active_silence(t)
    other = line_obj and line_obj.speaker != who and not active_silence(t)
    st = {
        "speaking": speaking,
        "eyes": "partner",
        "brows": "neutral",
        "pose": "rest",
        "lean": 0.0,
        "blink": False,
        "jaw": 0.0,
        "mouth_emotion": "neutral",
    }
    blink_phase = (t * 0.43 + (0.37 if who == "respondent" else 0.0)) % 4.1
    st["blink"] = blink_phase < 0.055 and not speaking
    if who == "respondent":
        if 2.50 <= t < 2.92:
            hit = ease(2.50, 2.61, t) - ease(2.78, 2.92, t)
            st.update({"eyes": "wide", "brows": "high", "pose": "snap", "lean": 30*hit, "mouth_emotion": "yes"})
        elif 2.92 <= t < 4.44:
            st.update({"eyes": "side", "brows": "smug", "pose": "hold", "mouth_emotion": "smug"})
        elif speaking:
            st["brows"] = "smug" if line_obj.intent in {"doubling_down", "baiting", "punchline"} else "confident"
            st["mouth_emotion"] = "smug" if line_obj.intent in {"punchline", "baiting"} else "assertive"
            if line_obj.intent in {"escalating", "insisting"}:
                st["pose"] = "point" if int((t-line_obj.start)/1.6) % 2 == 0 else "open"
                st["lean"] = 8 * math.sin((t-line_obj.start)*2.8)
            elif line_obj.intent in {"baiting", "punchline", "reveal"}:
                st["pose"] = "present"
                st["lean"] = 5
        elif other:
            st.update({"eyes": "partner", "brows": "listen", "mouth_emotion": "closed"})
    else:
        if speaking:
            st["brows"] = "skeptical"
            st["mouth_emotion"] = "worried" if line_obj.intent in {"shocked", "moral", "refusing"} else "neutral"
            if line_obj.intent in {"objecting", "moral", "refusing", "shocked"}:
                st["pose"] = "object"
            if line_obj.intent == "shocked":
                st.update({"eyes": "wide", "brows": "high", "pose": "shock"})
        elif other:
            st.update({"eyes": "partner", "brows": "worried" if t > 20 else "skeptical", "mouth_emotion": "flat"})
        if 2.92 <= t < 4.44:
            st.update({"eyes": "side", "brows": "frozen", "pose": "freeze", "mouth_emotion": "flat"})
    return st


def draw_mouth(draw, cx, cy, s, cue, emotion):
    # Rhubarb: A closed, B M/P closed, C/E wide, D open, F teeth, G rounded, H long vowel, X rest.
    o = "#181310"
    red = "#2b1716"
    if cue in {"X", "A", "B"}:
        if emotion in {"smug"}:
            draw.arc([cx-42*s, cy-10*s, cx+48*s, cy+22*s], 200, 350, fill=o, width=max(2, int(5*s)))
        elif emotion in {"flat", "worried"}:
            draw.line([(cx-40*s, cy+5*s), (cx+42*s, cy+2*s)], fill=o, width=max(2, int(5*s)))
        else:
            draw.arc([cx-38*s, cy-6*s, cx+40*s, cy+20*s], 190, 350, fill=o, width=max(2, int(5*s)))
    elif cue in {"C", "E"}:
        draw.rounded_rectangle([cx-48*s, cy-20*s, cx+50*s, cy+22*s], radius=int(10*s), fill=red, outline=o, width=max(2, int(5*s)))
        draw.rectangle([cx-39*s, cy-15*s, cx+42*s, cy-4*s], fill="#f4eee9")
    elif cue == "D":
        draw.ellipse([cx-30*s, cy-27*s, cx+32*s, cy+36*s], fill=red, outline=o, width=max(2, int(5*s)))
        draw.arc([cx-24*s, cy-22*s, cx+26*s, cy+5*s], 200, 340, fill="#f4eee9", width=max(2, int(7*s)))
    elif cue == "F":
        draw.rounded_rectangle([cx-44*s, cy-18*s, cx+46*s, cy+19*s], radius=int(9*s), fill="#f4eee9", outline=o, width=max(2, int(5*s)))
        draw.line([(cx-38*s, cy+2*s), (cx+40*s, cy+2*s)], fill=o, width=max(1, int(2*s)))
    elif cue == "G":
        draw.ellipse([cx-20*s, cy-25*s, cx+22*s, cy+25*s], fill=red, outline=o, width=max(2, int(5*s)))
    elif cue == "H":
        draw.ellipse([cx-36*s, cy-23*s, cx+38*s, cy+34*s], fill=red, outline=o, width=max(2, int(5*s)))
    else:
        draw.arc([cx-38*s, cy-6*s, cx+40*s, cy+20*s], 190, 350, fill=o, width=max(2, int(5*s)))


def face(draw, cx, cy, s, cap, st, cue, facing):
    o = "#181310"
    skin = "#d9ddd4"
    r = 82*s
    jaw_drop = 4*s if cue in {"D", "H", "C", "E"} else 0
    draw.ellipse([cx-r, cy-r, cx+r, cy+r+jaw_drop], fill=skin, outline=o, width=max(3, int(7*s)))
    if cap:
        draw.pieslice([cx-r*0.98, cy-r*1.02, cx+r*0.92, cy+r*0.52], 188, 350, fill=o)
        if facing > 0:
            draw.polygon([(cx-r*.72, cy-r*.62), (cx-r*1.45, cy-r*.46), (cx-r*.72, cy-r*.30)], fill=o)
        else:
            draw.polygon([(cx+r*.72, cy-r*.62), (cx+r*1.45, cy-r*.46), (cx+r*.72, cy-r*.30)], fill=o)
        draw.ellipse([cx+r*.48, cy-r*.66, cx+r*.62, cy-r*.50], fill="#f1dd58")
    eye_y = cy - 12*s
    eye_dx = 34*s
    wide = st["eyes"] == "wide"
    for side in [-1, 1]:
        ex = cx + side*eye_dx
        ew, eh = (28*s, 44*s) if wide else (23*s, 36*s)
        draw.ellipse([ex-ew, eye_y-eh, ex+ew, eye_y+eh], fill="#fbfff8", outline=o, width=max(2, int(5*s)))
        if st["blink"]:
            draw.line([(ex-ew, eye_y), (ex+ew, eye_y)], fill=o, width=max(2, int(5*s)))
            continue
        shift = 10*s * facing
        if st["eyes"] == "side":
            shift = 16*s * facing
        elif st["eyes"] == "wide":
            shift = 6*s * facing
        draw.ellipse([ex+shift-8*s, eye_y-12*s, ex+shift+8*s, eye_y+12*s], fill=o)
        if st["brows"] in {"frozen", "smug", "worried"}:
            draw.line([(ex-ew*.85, eye_y-eh*.55), (ex+ew*.85, eye_y-eh*.72)], fill=o, width=max(2, int(4*s)))
    brow = st["brows"]
    if brow in {"high"}:
        draw.arc([cx-68*s, cy-78*s, cx-20*s, cy-50*s], 200, 350, fill=o, width=max(2, int(5*s)))
        draw.arc([cx+16*s, cy-78*s, cx+66*s, cy-50*s], 190, 340, fill=o, width=max(2, int(5*s)))
    elif brow in {"skeptical", "frozen", "worried"}:
        draw.line([(cx-60*s, cy-50*s), (cx-18*s, cy-64*s)], fill=o, width=max(2, int(5*s)))
        draw.line([(cx+20*s, cy-64*s), (cx+62*s, cy-50*s)], fill=o, width=max(2, int(5*s)))
    elif brow in {"smug", "confident"}:
        draw.line([(cx-60*s, cy-58*s), (cx-18*s, cy-50*s)], fill=o, width=max(2, int(5*s)))
        draw.line([(cx+20*s, cy-50*s), (cx+62*s, cy-58*s)], fill=o, width=max(2, int(5*s)))
    else:
        draw.arc([cx-58*s, cy-62*s, cx-20*s, cy-44*s], 200, 340, fill=o, width=max(2, int(4*s)))
        draw.arc([cx+20*s, cy-62*s, cx+58*s, cy-44*s], 200, 340, fill=o, width=max(2, int(4*s)))
    # Mouth is lower-face local, above the head bottom/neck junction.
    draw_mouth(draw, cx + 8*s*facing, cy + 55*s, s, cue, st["mouth_emotion"])


def character(draw, who, x, y, s, facing, t, cues):
    cap = who == "respondent"
    st = state_for(who, t)
    cue = mouth_value(cues, who, t)
    if not st["speaking"]:
        cue = "X"
    chair(draw, x, y+320*s, s, cap)
    lean = st["lean"] * s * facing
    if st["pose"] == "snap":
        lean += 20*s*facing
    hx = x + lean
    hy = y - (12*s if st["pose"] == "snap" else 0)
    neck = (hx, hy+86*s)
    pelvis = (x, y+410*s)
    sh_l = (hx-52*s, hy+110*s)
    sh_r = (hx+52*s, hy+110*s)
    line(draw, [neck, (x+2*s, y+255*s), pelvis], int(8*s))
    line(draw, [sh_l, neck, sh_r], int(8*s))
    # arms with pose-specific intent
    if st["pose"] in {"object", "shock"} and who == "interviewer":
        active = sh_l if facing < 0 else sh_r
        line(draw, [active, (active[0]-facing*95*s, active[1]-75*s), (active[0]-facing*150*s, active[1]-58*s)], int(8*s))
        rest = sh_r if active == sh_l else sh_l
        line(draw, [rest, (rest[0]+facing*70*s, rest[1]+150*s), (rest[0]+facing*110*s, rest[1]+175*s)], int(8*s))
    elif st["pose"] in {"point", "present", "open", "snap"} and who == "respondent":
        active = sh_r if facing > 0 else sh_l
        reach = 215*s if st["pose"] == "point" else 155*s
        lift = -30*s if st["pose"] == "snap" else 0
        line(draw, [active, (active[0]+facing*105*s, active[1]+40*s+lift), (active[0]+facing*reach, active[1]+12*s+lift)], int(8*s))
        other = sh_l if active == sh_r else sh_r
        line(draw, [other, (other[0]-facing*55*s, other[1]+135*s), (other[0]-facing*78*s, other[1]+175*s)], int(8*s))
    else:
        line(draw, [sh_l, (x-130*s, y+280*s), (x-190*s, y+305*s)], int(8*s))
        line(draw, [sh_r, (x+130*s, y+280*s), (x+190*s, y+305*s)], int(8*s))
    # legs
    line(draw, [pelvis, (x-110*s, y+470*s), (x-188*s, y+750*s), (x-268*s, y+764*s)], int(8*s))
    line(draw, [pelvis, (x+92*s, y+454*s), (x+36*s, y+750*s), (x+78*s, y+786*s)], int(8*s))
    face(draw, hx, hy, s, cap, st, cue, facing)


def chair_side_back(draw, x, y, s, facing, pale):
    o = "#181310"
    back = "#a39390" if not pale else "#efd4d0"
    draw.polygon([(x-110*s*facing, y-195*s), (x+70*s*facing, y-210*s), (x+98*s*facing, y+25*s), (x-120*s*facing, y+55*s)], fill=back, outline=o)
    draw.line([(x-110*s*facing, y-195*s), (x+70*s*facing, y-210*s), (x+98*s*facing, y+25*s), (x-120*s*facing, y+55*s), (x-110*s*facing, y-195*s)], fill=o, width=int(7*s))


def chair_side_seat(draw, x, y, s, facing, pale):
    o = "#181310"
    seat = "#c9b1ae" if not pale else "#f5d7d5"
    dark = "#5f504b"
    draw.polygon([(x-138*s*facing, y-25*s), (x+120*s*facing, y-45*s), (x+135*s*facing, y+100*s), (x-122*s*facing, y+125*s)], fill=seat, outline=o)
    draw.polygon([(x-118*s*facing, y+120*s), (x+128*s*facing, y+96*s), (x+122*s*facing, y+235*s), (x-118*s*facing, y+215*s)], fill=dark, outline=o)


def chair_side_front_arm(draw, x, y, s, facing, pale):
    o = "#181310"
    side = "#73625e"
    # Low foreground armrest: it may cover the cushion/near thigh, but must not
    # hide the torso or shoulder/arm acting.
    draw.polygon([(x-155*s*facing, y+22*s), (x-52*s*facing, y-4*s), (x-45*s*facing, y+142*s), (x-158*s*facing, y+165*s)], fill=side, outline=o)


def character_side(draw, who, x, y, s, facing, t, cues):
    cap = who == "respondent"
    st = state_for(who, t)
    cue = mouth_value(cues, who, t)
    if not st["speaking"]:
        cue = "X"
    cy = y + 320*s
    chair_side_back(draw, x, cy, s, facing, cap)
    chair_side_seat(draw, x, cy, s, facing, cap)
    lean = st["lean"] * s * facing
    if st["pose"] == "snap":
        lean += 26*s*facing
    hx = x + lean
    hy = y - (14*s if st["pose"] == "snap" else 0)
    neck = (hx, hy+84*s)
    pelvis = (x-18*s*facing, y+418*s)
    shoulder = (hx-38*s*facing, hy+112*s)
    far_shoulder = (hx+18*s*facing, hy+115*s)
    # narrow body side silhouette: direct head/base connection, no broad block.
    line(draw, [neck, (x-8*s*facing, y+265*s), pelvis], int(8*s))
    line(draw, [shoulder, neck, far_shoulder], int(8*s))
    # legs with planted feet and clear thigh/shin bends; thighs emerge from cushion, not chair wall.
    line(draw, [pelvis, (x+82*s*facing, y+472*s), (x+178*s*facing, y+690*s), (x+248*s*facing, y+690*s)], int(8*s))
    line(draw, [pelvis, (x+30*s*facing, y+512*s), (x+84*s*facing, y+775*s), (x+155*s*facing, y+795*s)], int(8*s))
    # arms: one resting, one expressive if called for.
    if st["pose"] in {"point", "present", "open", "snap"} and who == "respondent":
        lift = -40*s if st["pose"] == "snap" else 0
        reach = 230*s if st["pose"] in {"point", "snap"} else 160*s
        elbow = (shoulder[0]+92*s*facing, shoulder[1]+24*s+lift)
        wrist = (shoulder[0]+reach*facing, shoulder[1]-8*s+lift)
        line(draw, [shoulder, elbow, wrist], int(8*s))
        line(draw, [(wrist[0], wrist[1]), (wrist[0]+22*s*facing, wrist[1]+2*s)], int(6*s))
        line(draw, [far_shoulder, (x-58*s*facing, y+298*s), (x-72*s*facing, y+342*s)], int(8*s))
    elif st["pose"] in {"object", "shock"} and who == "interviewer":
        elbow = (shoulder[0]+82*s*facing, shoulder[1]-62*s)
        wrist = (shoulder[0]+148*s*facing, shoulder[1]-44*s)
        line(draw, [shoulder, elbow, wrist], int(8*s))
        line(draw, [(wrist[0], wrist[1]), (wrist[0]+18*s*facing, wrist[1]+10*s)], int(6*s))
        line(draw, [far_shoulder, (x-55*s*facing, y+298*s), (x-72*s*facing, y+342*s)], int(8*s))
    else:
        line(draw, [shoulder, (x+52*s*facing, y+292*s), (x+112*s*facing, y+312*s)], int(8*s))
        line(draw, [far_shoulder, (x-55*s*facing, y+298*s), (x-72*s*facing, y+342*s)], int(8*s))
    # Foreground armrest drawn last so intentional occlusion reads as furniture in front.
    chair_side_front_arm(draw, x, cy, s, facing, cap)
    face(draw, hx, hy, s, cap, st, cue, facing)


def render_frame(i, cues):
    t = i / FPS
    shot = shot_at(t)
    img = Image.new("RGB", (W, H), "#d0ceca")
    d = ImageDraw.Draw(img)
    draw_bg(d)
    if shot.framing == "two":
        draw_table(d, 540, 1035, .86)
        character(d, "interviewer", 315, 575, .86, 1, t, cues)
        character(d, "respondent", 780, 575, .86, -1, t, cues)
    elif shot.framing == "respondent":
        draw_table(d, 795, 1010, .82)
        character_side(d, "respondent", 415, 565, 1.12, 1, t, cues)
    else:
        draw_table(d, 290, 1010, .82)
        character_side(d, "interviewer", 650, 565, 1.12, -1, t, cues)
    if 2.44 <= t < 2.50:
        img = Image.blend(img, Image.new("RGB", (W, H), "#f3f0e9"), .18)
    return img


def render_sequence():
    cues = load_cues()
    FRAMES.mkdir(parents=True, exist_ok=True)
    for i in range(FRAME_COUNT):
        out = FRAMES / f"honest_v3_{i:06d}.png"
        if out.exists():
            continue
        render_frame(i, cues).save(out)
        if i % 120 == 0:
            print(f"rendered {i}/{FRAME_COUNT}")
    return cues


def make_reviews():
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    # representative dialogue section preview frames: opening through held reaction
    frames = [0, 36, 59, 64, 69, 80, 107, 140, 184]
    cols, tw, th, lh = 3, 270, 480, 36
    rows = math.ceil(len(frames) / cols)
    sheet = Image.new("RGB", (cols*tw, rows*(th+lh)), "#f2f0ea")
    d = ImageDraw.Draw(sheet)
    for idx, f in enumerate(frames):
        im = Image.open(FRAMES / f"honest_v3_{f:06d}.png").resize((tw, th), Image.Resampling.LANCZOS)
        x = (idx % cols)*tw
        y = (idx // cols)*(th+lh)
        d.text((x+4, y+6), f"F{f:04d} {f/FPS:.2f}s", fill="#181310")
        sheet.paste(im, (x, y+lh))
    sheet.save(PREVIEWS / "opening_dialogue_pose_review.png")
    reps = []
    for shot in SHOTS:
        mid = (shot.start + shot.end) / 2
        if shot.name == "yes_close":
            mid = 2.66
        reps.append((shot.name, seconds_to_frame(mid)))
    cols, tw, th, lh = 5, 216, 384, 34
    rows = math.ceil(len(reps)/cols)
    full = Image.new("RGB", (cols*tw, rows*(th+lh)), "#f2f0ea")
    d = ImageDraw.Draw(full)
    for idx, (name, f) in enumerate(reps):
        im = Image.open(FRAMES / f"honest_v3_{f:06d}.png").resize((tw, th), Image.Resampling.LANCZOS)
        x = (idx % cols)*tw
        y = (idx // cols)*(th+lh)
        d.text((x+3, y+4), f"{idx+1:02d} {name} F{f}", fill="#181310")
        full.paste(im, (x, y+lh))
    full.save(PREVIEWS / "full_v3_shot_contact_sheet.png")


def write_jsfl_from_keyframes():
    # Build a compact actual Animate timeline: vector keyframes at significant poses.
    # The render sequence remains the export master, but this FLA contains populated layers and real timed keys.
    key_times = sorted(set([0, AUDIO_DURATION] + [v for ln in LINES for v in (ln.start, ln.end)] + [v for sh in SHOTS for v in (sh.start, sh.end)] + [2.56, 2.68, 3.04, 4.92, 7.68, 23.60, 37.80, 58.80, 62.30, 66.80]))
    key_frames = sorted(set(seconds_to_frame(t) for t in key_times if 0 <= t <= AUDIO_DURATION))
    js = []
    js.append("var doc = fl.createDocument('timeline');")
    js.append("doc.width=1080; doc.height=1920; doc.frameRate=24; doc.backgroundColor='#d0ceca';")
    js.append("var tl=doc.getTimeline(); while(tl.layers.length>1){tl.deleteLayer(0);} tl.layers[0].name='Vector_Keyed_Performance';")
    js.append(f"tl.insertFrames({FRAME_COUNT-1}, true);")
    js.append("function L(x1,y1,x2,y2,w){doc.setStrokeColor('#181310'); doc.setStrokeSize(w); doc.addNewLine({x:x1,y:y1},{x:x2,y:y2});}")
    js.append("function O(l,t,r,b,fill,stroke,w){doc.setFillColor(fill); doc.setStrokeColor(stroke); doc.setStrokeSize(w); doc.addNewOval({left:l,top:t,right:r,bottom:b},false,false);}")
    js.append("function R(l,t,r,b,fill,stroke,w){doc.setFillColor(fill); doc.setStrokeColor(stroke); doc.setStrokeSize(w); doc.addNewRectangle({left:l,top:t,right:r,bottom:b},0,false,false);}")
    js.append("function scene(frame, mode){tl.currentLayer=0; tl.currentFrame=frame; tl.setSelectedLayers(0); tl.setSelectedFrames(frame,frame+1,true); if(frame>0) tl.insertKeyframe(frame); R(0,0,1080,1920,'#d0ceca','#d0ceca',1); R(0,1328,1080,1920,'#858e84','#858e84',1); R(690,150,920,430,'#faf9f2','#4a4642',7);")
    js.append("if(mode=='two'){O(250,500,390,640,'#d9ddd4','#181310',7); O(700,500,840,640,'#d9ddd4','#181310',7); L(320,640,320,980,8); L(770,640,770,980,8); R(185,780,445,1080,'#a39390','#181310',7); R(640,780,900,1080,'#efd4d0','#181310',7);} else if(mode=='respondent'){O(410,470,610,670,'#d9ddd4','#181310',8); L(510,670,510,1030,9); R(335,805,695,1200,'#efd4d0','#181310',7);} else {O(470,470,670,670,'#d9ddd4','#181310',8); L(570,670,570,1030,9); R(395,805,755,1200,'#a39390','#181310',7);} }")
    for f in key_frames:
        mode = shot_at(f / FPS).framing
        mode = "respondent" if mode == "respondent" else "interviewer" if mode == "interviewer" else "two"
        js.append(f"scene({f},'{mode}');")
    dest = str(EDITABLE / "honest_interview_full_v2_keyed_timeline.fla").replace("\\", "/")
    js.append(f"fl.saveDocument(doc,'file:///{dest}');")
    (SCRIPTS / "create_v2_keyed_timeline.jsfl").write_text("\n".join(js), encoding="utf-8")


def write_reports(cues):
    data = {
        "fps": FPS,
        "frame_count": FRAME_COUNT,
        "audio_duration": AUDIO_DURATION,
        "shots": [s.__dict__ for s in SHOTS],
        "lines": [l.__dict__ for l in LINES],
        "rhubarb": {
            "interviewer_cues": len(cues["interviewer"]),
            "respondent_cues": len(cues["respondent"]),
            "note": "Speaker-specific full-length analysis WAVs preserve original duration with the other speaker silenced.",
        },
    }
    (ASSETS / "v3_timeline_and_lipsync.json").write_text(json.dumps(data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    EDITABLE.mkdir(parents=True, exist_ok=True)
    cues = render_sequence()
    make_reviews()
    write_jsfl_from_keyframes()
    write_reports(cues)
    print("V2 assets complete")
