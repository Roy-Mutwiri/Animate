from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw


ROOT = Path(r"D:\Animate\Projects\HonestInterview\ProductionFull_v1")
FRAMES = ROOT / "frames"
REVIEW = ROOT / "review"
EXPORTS = ROOT / "exports"
ASSETS = ROOT / "assets"

W, H = 1080, 1920
FPS = 24
AUDIO_DURATION = 70.889070
FRAME_COUNT = math.ceil(AUDIO_DURATION * FPS)


@dataclass(frozen=True)
class Line:
    start: float
    end: float
    speaker: str
    text: str
    mood: str = "normal"


@dataclass(frozen=True)
class Shot:
    start: float
    end: float
    name: str
    framing: str
    note: str


LINES = [
    Line(0.00, 2.34, "interviewer", "Okay, for $10 billion, would you", "question"),
    Line(2.56, 2.82, "respondent", "Yes.", "snap"),
    Line(4.44, 7.70, "interviewer", "Um, I didn't finish the question. I'd listen here.", "object"),
    Line(8.64, 18.72, "respondent", "There was nothing. And I mean nothing that could come out of that little pie hole of yours to make me turn down $10 billion.", "confident"),
    Line(20.48, 23.44, "interviewer", "Even if one random person had to die?", "question"),
    Line(23.44, 25.12, "respondent", "Yes. The answer is yes.", "flat_yes"),
    Line(25.84, 27.60, "interviewer", "Okay, what if it was someone you knew?", "press"),
    Line(27.60, 37.36, "respondent", "Yes, take my aunt, take my grandma, hell, you could blow the block up. Can you even fathom how much money $10 billion is?", "rant"),
    Line(38.00, 39.44, "interviewer", "Oh, it's just a hypothetical.", "uneasy"),
    Line(39.44, 43.76, "respondent", "And if it was a reality, I'd be first in line.", "smug"),
    Line(43.76, 47.12, "interviewer", "You're talking about human lives for $10 billion.", "moral"),
    Line(47.12, 49.84, "respondent", "Hey, hey, hey, hey. Guess what?", "tease"),
    Line(50.40, 52.16, "interviewer", "I don't want to guess. Don't make me guess.", "annoyed"),
    Line(52.16, 55.12, "respondent", "Oh, come on. You got to be curious about what I'm going to tell you.", "tease"),
    Line(55.12, 57.12, "interviewer", "What?", "short"),
    Line(58.40, 62.08, "respondent", "I would have did it for $5 billion?", "reveal"),
    Line(62.08, 64.56, "interviewer", "$1,000. What are you?", "shocked"),
    Line(64.56, 65.60, "respondent", "Oh, that's a good question.", "consider"),
    Line(66.56, 70.32, "respondent", "I guess you can call me an entrepreneur.", "punchline"),
]


SHOTS = [
    Shot(0.00, 2.44, "S01_setup_twoshot", "two", "Interviewer sets up; respondent listens."),
    Shot(2.44, 4.44, "S02_yes_reaction", "respondent_close", "Abrupt Yes and held silence."),
    Shot(4.44, 8.05, "S03_object_close", "interviewer_close", "Interviewer objects; respondent holds offscreen confidence."),
    Shot(8.05, 18.95, "S04_respondent_rant", "respondent_close", "Respondent monologue, restrained confidence with a few accents."),
    Shot(18.95, 20.48, "S05_breath_twoshot", "two", "Pause before interviewer escalates question."),
    Shot(20.48, 23.44, "S06_random_person", "interviewer_close", "Interviewer presses the morality question."),
    Shot(23.44, 25.60, "S07_answer_yes", "respondent_close", "Respondent says yes again without hesitation."),
    Shot(25.60, 27.60, "S08_someone_known", "interviewer_close", "Interviewer tries making it personal."),
    Shot(27.60, 37.60, "S09_take_family", "respondent_close", "Respondent escalates into the darkest confidence."),
    Shot(37.60, 39.44, "S10_hypothetical", "interviewer_close", "Interviewer weakly reframes as hypothetical."),
    Shot(39.44, 43.76, "S11_first_in_line", "respondent_close", "Respondent doubles down."),
    Shot(43.76, 47.12, "S12_human_lives", "interviewer_close", "Interviewer states the moral cost."),
    Shot(47.12, 49.84, "S13_guess_what", "respondent_close", "Respondent interrupts with tease."),
    Shot(49.84, 52.16, "S14_dont_guess", "interviewer_close", "Interviewer tries to stop the bit."),
    Shot(52.16, 55.12, "S15_curiosity", "respondent_close", "Respondent keeps baiting."),
    Shot(55.12, 58.40, "S16_what_hold", "interviewer_close", "Interviewer relents, then hold."),
    Shot(58.40, 62.08, "S17_five_billion", "respondent_close", "Respondent reveals lower number."),
    Shot(62.08, 64.56, "S18_one_thousand", "interviewer_close", "Interviewer tops the confusion."),
    Shot(64.56, 70.889, "S19_entrepreneur", "respondent_close", "Final punchline and smug hold."),
]


SILENCES = [
    (2.854, 4.848),
    (7.352, 8.612),
    (18.892, 20.627),
    (37.584, 37.933),
    (43.570, 43.934),
    (55.601, 55.932),
    (57.436, 57.828),
]


def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def smoothstep(edge0, edge1, x):
    if edge0 == edge1:
        return 0.0
    t = clamp((x - edge0) / (edge1 - edge0))
    return t * t * (3 - 2 * t)


def active_line(t: float) -> Optional[Line]:
    for line in LINES:
        if line.start <= t < line.end:
            return line
    return None


def current_shot(t: float) -> Shot:
    for shot in SHOTS:
        if shot.start <= t < shot.end:
            return shot
    return SHOTS[-1]


def in_silence(t: float) -> bool:
    return any(a <= t < b for a, b in SILENCES)


def mouth_for(t: float, who: str) -> str:
    line = active_line(t)
    if not line or line.speaker != who or in_silence(t):
        return "flat" if who == "interviewer" else "closed"
    local = t - line.start
    if local < 0.06 or line.end - t < 0.08:
        return "closed"
    if line.mood in {"snap", "flat_yes"}:
        return "wide" if int(local * 18) % 3 != 0 else "closed"
    if line.mood in {"shocked", "reveal", "rant"}:
        cycle = ["open", "teeth", "round", "open", "closed"]
    elif line.mood in {"tease", "punchline", "smug"}:
        cycle = ["smile_open", "teeth", "smile_open", "closed"]
    elif line.mood in {"question", "object", "press", "moral", "annoyed"}:
        cycle = ["small", "flat_open", "round", "small", "closed"]
    else:
        cycle = ["small", "open", "closed", "round"]
    return cycle[int(local * 11) % len(cycle)]


def character_state(t: float, who: str, shot: Shot) -> dict:
    line = active_line(t)
    speaking = bool(line and line.speaker == who and not in_silence(t))
    other_speaking = bool(line and line.speaker != who and not in_silence(t))
    state = {
        "speaking": speaking,
        "mouth": mouth_for(t, who),
        "eyes": "listen",
        "brows": "neutral",
        "gesture": "rest",
        "lean": 0.0,
        "blink": False,
        "head_dx": 0.0,
        "head_dy": 0.0,
    }
    blink_phase = (t * 0.57 + (0.2 if who == "respondent" else 0.0)) % 3.8
    state["blink"] = 0.0 < blink_phase < 0.08 and not speaking

    if who == "respondent":
        state["eyes"] = "right"
        if other_speaking:
            state["brows"] = "attentive"
        if 2.54 <= t < 2.88:
            hit = smoothstep(2.54, 2.62, t) - smoothstep(2.78, 2.88, t)
            state.update({"eyes": "wide", "brows": "high", "gesture": "snap", "lean": 22 * hit, "head_dx": 10 * hit, "head_dy": -12 * hit})
            state["mouth"] = "wide"
        elif 2.88 <= t < 4.44:
            state.update({"eyes": "right", "brows": "smug", "gesture": "rest", "mouth": "smirk"})
        elif line and line.speaker == "respondent":
            state["brows"] = "smug" if line.mood in {"smug", "punchline", "tease"} else "confident"
            if line.mood in {"rant", "reveal"}:
                state["gesture"] = "point" if int((t - line.start) / 1.4) % 2 == 0 else "open_hand"
            elif line.mood in {"tease", "punchline"}:
                state["gesture"] = "small_point"
            elif line.mood == "consider":
                state["gesture"] = "chin"
            state["lean"] = 6 * math.sin((t - line.start) * 3.2)
        elif 55.12 <= t < 58.4:
            state.update({"eyes": "right", "brows": "expectant", "mouth": "smirk"})
    else:
        state["eyes"] = "left"
        if line and line.speaker == "interviewer":
            state["brows"] = "skeptical"
            if line.mood in {"object", "moral", "annoyed", "shocked"}:
                state["gesture"] = "object"
            if line.mood == "shocked":
                state["eyes"] = "wide"
                state["brows"] = "high_asym"
                state["mouth"] = "open"
            state["lean"] = -5 * math.sin((t - line.start) * 2.5)
        elif other_speaking:
            state["brows"] = "worried" if t > 27 else "skeptical"
            state["mouth"] = "flat"
        if 2.88 <= t < 4.44:
            state.update({"eyes": "left", "brows": "frozen", "mouth": "flat"})
        if 49.84 <= t < 52.16:
            state.update({"brows": "annoyed", "gesture": "stop"})
    return state


def draw_line(draw: ImageDraw.ImageDraw, pts, fill="#181310", width=8):
    draw.line(pts, fill=fill, width=width, joint="curve")


def draw_floor(draw: ImageDraw.ImageDraw):
    draw.rectangle([0, 0, W, H], fill="#d2d0cb")
    draw.rectangle([0, 1320, W, H], fill="#858e84")
    for x in range(-160, W + 220, 220):
        draw.line([(x, 1320), (x + 300, H)], fill="#727b73", width=3)
    for y in [1430, 1585, 1740]:
        draw.line([(0, y), (W, y - 45)], fill="#788179", width=3)
    draw.rectangle([700, 145, 920, 430], fill="#f9f9f2", outline="#4c4845", width=7)
    draw.line([810, 145, 810, 430], fill="#908d87", width=4)
    draw.line([700, 285, 920, 285], fill="#908d87", width=4)


def draw_table_plant(draw: ImageDraw.ImageDraw, cx=540, cy=1040, scale=1.0):
    s = scale
    draw.rectangle([cx - 100*s, cy, cx + 110*s, cy + 160*s], fill="#4a4943", outline="#181310", width=int(5*s))
    draw.rectangle([cx - 75*s, cy + 30*s, cx + 75*s, cy + 80*s], fill="#3c3d37", outline="#181310", width=int(4*s))
    draw.rectangle([cx - 75*s, cy + 98*s, cx + 75*s, cy + 145*s], fill="#3c3d37", outline="#181310", width=int(4*s))
    draw.ellipse([cx - 8*s, cy + 52*s, cx + 8*s, cy + 68*s], fill="#b99d94", outline="#181310", width=int(2*s))
    draw.ellipse([cx - 8*s, cy + 118*s, cx + 8*s, cy + 134*s], fill="#b99d94", outline="#181310", width=int(2*s))
    pot = [(cx - 42*s, cy - 12*s), (cx + 42*s, cy - 12*s), (cx + 26*s, cy + 45*s), (cx - 26*s, cy + 45*s)]
    draw.polygon(pot, fill="#a77b55")
    draw.line(pot + [pot[0]], fill="#5a4438", width=int(4*s))
    for ang in [-65, -35, -10, 25, 50]:
        x2 = cx + math.cos(math.radians(ang)) * 80 * s
        y2 = cy - 18*s + math.sin(math.radians(ang)) * 95 * s
        draw.line([(cx, cy - 5*s), (x2, y2)], fill="#2c923f", width=int(5*s))
        draw.ellipse([x2-18*s, y2-14*s, x2+18*s, y2+14*s], fill="#f38bf0", outline="#765377", width=int(2*s))


def draw_chair(draw: ImageDraw.ImageDraw, x, y, scale=1.0, flip=1, pale=False):
    s = scale
    back = "#a0918e" if not pale else "#dec9c5"
    side = "#74645f"
    seat = "#c8b1ae" if not pale else "#efd8d6"
    outline = "#181310"
    # back
    draw.polygon([(x-150*s, y-210*s), (x+155*s, y-220*s), (x+165*s, y+70*s), (x-145*s, y+75*s)], fill=back, outline=outline)
    draw.line([(x-150*s, y-210*s), (x+155*s, y-220*s), (x+165*s, y+70*s), (x-145*s, y+75*s), (x-150*s, y-210*s)], fill=outline, width=int(6*s))
    # arms
    draw.polygon([(x-250*s, y-35*s), (x-145*s, y-55*s), (x-145*s, y+210*s), (x-250*s, y+225*s)], fill=side, outline=outline)
    draw.polygon([(x+130*s, y-60*s), (x+260*s, y-30*s), (x+260*s, y+210*s), (x+135*s, y+190*s)], fill=side, outline=outline)
    # cushion and base
    draw.polygon([(x-150*s, y+100*s), (x+135*s, y+90*s), (x+205*s, y+130*s), (x-205*s, y+145*s)], fill=seat, outline=outline)
    draw.polygon([(x-190*s, y+145*s), (x+180*s, y+130*s), (x+175*s, y+265*s), (x-185*s, y+245*s)], fill="#665753", outline=outline)


def draw_mouth(draw, cx, cy, s, shape, facing=1):
    black = "#181310"
    if shape in {"closed", "flat"}:
        draw.arc([cx-40*s, cy-8*s, cx+42*s, cy+20*s], 190, 350, fill=black, width=max(2, int(5*s)))
    elif shape == "smirk":
        draw.arc([cx-35*s, cy-14*s, cx+50*s, cy+20*s], 205, 350, fill=black, width=max(2, int(5*s)))
    elif shape in {"small", "flat_open"}:
        draw.ellipse([cx-22*s, cy-12*s, cx+24*s, cy+22*s], fill="#2b1716", outline=black, width=max(2, int(4*s)))
        if shape == "flat_open":
            draw.rectangle([cx-18*s, cy-8*s, cx+20*s, cy+0*s], fill="#f4eee9")
    elif shape == "open":
        draw.ellipse([cx-28*s, cy-24*s, cx+30*s, cy+35*s], fill="#2b1716", outline=black, width=max(2, int(5*s)))
        draw.rectangle([cx-20*s, cy-18*s, cx+22*s, cy-4*s], fill="#f4eee9")
    elif shape == "round":
        draw.ellipse([cx-18*s, cy-24*s, cx+22*s, cy+26*s], fill="#2b1716", outline=black, width=max(2, int(5*s)))
    elif shape == "wide":
        draw.ellipse([cx-48*s, cy-22*s, cx+50*s, cy+32*s], fill="#2b1716", outline=black, width=max(2, int(5*s)))
        draw.rectangle([cx-38*s, cy-16*s, cx+40*s, cy-2*s], fill="#f4eee9")
    elif shape == "teeth":
        draw.rounded_rectangle([cx-42*s, cy-16*s, cx+46*s, cy+22*s], radius=int(8*s), fill="#f4eee9", outline=black, width=max(2, int(5*s)))
        draw.line([cx-35*s, cy+4*s, cx+42*s, cy+4*s], fill=black, width=max(1, int(2*s)))
    elif shape == "smile_open":
        draw.arc([cx-50*s, cy-32*s, cx+54*s, cy+36*s], 15, 165, fill=black, width=max(2, int(6*s)))
        draw.ellipse([cx-32*s, cy-10*s, cx+36*s, cy+30*s], fill="#2b1716", outline=black, width=max(2, int(3*s)))


def draw_face(draw, cx, cy, s, cap, state, facing=1):
    skin = "#d9ddd4"
    black = "#181310"
    r = 82*s
    # head
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=skin, outline=black, width=max(3, int(7*s)))
    if cap:
        draw.pieslice([cx-r*0.95, cy-r*1.02, cx+r*0.9, cy+r*0.55], 188, 350, fill=black)
        brim = [(cx-r*0.75, cy-r*0.62), (cx-r*1.45, cy-r*0.44), (cx-r*0.75, cy-r*0.30)]
        if facing < 0:
            brim = [(cx+r*0.75, cy-r*0.62), (cx+r*1.45, cy-r*0.44), (cx+r*0.75, cy-r*0.30)]
        draw.polygon(brim, fill=black)
        draw.ellipse([cx+r*0.48, cy-r*0.65, cx+r*0.62, cy-r*0.50], fill="#f3df5a")

    eye_y = cy - 10*s
    eye_dx = 34*s
    if state["eyes"] == "wide":
        ew, eh = 26*s, 42*s
    else:
        ew, eh = 23*s, 36*s
    for side in [-1, 1]:
        ex = cx + side*eye_dx
        draw.ellipse([ex-ew, eye_y-eh, ex+ew, eye_y+eh], fill="#fbfff8", outline=black, width=max(2, int(5*s)))
        p_shift = 8*s*facing
        if state["eyes"] in {"left"}:
            p_shift = -11*s
        elif state["eyes"] in {"right"}:
            p_shift = 11*s
        elif state["eyes"] == "wide":
            p_shift = 7*s*facing
        if state["blink"]:
            draw.line([ex-ew, eye_y, ex+ew, eye_y], fill=black, width=max(2, int(5*s)))
        else:
            draw.ellipse([ex+p_shift-8*s, eye_y-12*s, ex+p_shift+8*s, eye_y+12*s], fill=black)

    # eyelids and brows
    brow = state["brows"]
    if brow in {"skeptical", "annoyed", "frozen"}:
        draw.line([cx-60*s, cy-50*s, cx-20*s, cy-62*s], fill=black, width=max(2, int(5*s)))
        draw.line([cx+18*s, cy-60*s, cx+60*s, cy-48*s], fill=black, width=max(2, int(5*s)))
    elif brow in {"high", "high_asym"}:
        draw.arc([cx-70*s, cy-76*s, cx-18*s, cy-48*s], 200, 330, fill=black, width=max(2, int(5*s)))
        draw.line([cx+15*s, cy-72*s, cx+62*s, cy-70*s], fill=black, width=max(2, int(5*s)))
    elif brow in {"smug", "confident"}:
        draw.line([cx-60*s, cy-58*s, cx-20*s, cy-50*s], fill=black, width=max(2, int(5*s)))
        draw.line([cx+18*s, cy-52*s, cx+60*s, cy-58*s], fill=black, width=max(2, int(5*s)))
    elif brow == "worried":
        draw.line([cx-62*s, cy-48*s, cx-20*s, cy-62*s], fill=black, width=max(2, int(5*s)))
        draw.line([cx+20*s, cy-62*s, cx+62*s, cy-48*s], fill=black, width=max(2, int(5*s)))
    else:
        draw.arc([cx-58*s, cy-65*s, cx-18*s, cy-45*s], 200, 340, fill=black, width=max(2, int(4*s)))
        draw.arc([cx+18*s, cy-65*s, cx+58*s, cy-45*s], 200, 340, fill=black, width=max(2, int(4*s)))

    if brow in {"annoyed", "frozen", "smug"} or state["mouth"] in {"flat", "smirk"}:
        draw.line([cx-55*s, cy-18*s, cx-20*s, cy-24*s], fill=black, width=max(2, int(4*s)))
        draw.line([cx+20*s, cy-24*s, cx+55*s, cy-18*s], fill=black, width=max(2, int(4*s)))

    draw_mouth(draw, cx + 10*s*facing, cy + 70*s, s, state["mouth"], facing)


def draw_character(draw, who, x, y, scale, facing, t, shot):
    cap = who == "respondent"
    pale_chair = cap
    draw_chair(draw, x, y + 300*scale, scale, facing, pale=pale_chair)
    state = character_state(t, who, shot)
    s = scale
    lean = state["lean"] * s * facing
    hx = x + lean + state["head_dx"] * s
    hy = y + state["head_dy"] * s
    neck = (hx, hy + 84*s)
    pelvis = (x + 8*s, y + 410*s)
    shoulder_l = (hx - 52*s, hy + 110*s)
    shoulder_r = (hx + 52*s, hy + 110*s)

    # body and limbs behind head
    draw_line(draw, [neck, (x + 2*s, y + 255*s), pelvis], width=max(3, int(8*s)))
    draw_line(draw, [shoulder_l, neck, shoulder_r], width=max(3, int(8*s)))
    # arms
    if state["gesture"] in {"object", "stop"} and who == "interviewer":
        raised = shoulder_r if facing < 0 else shoulder_l
        dirx = -facing
        draw_line(draw, [raised, (raised[0] + dirx*80*s, raised[1] - 92*s), (raised[0] + dirx*125*s, raised[1] - 82*s)], width=max(3, int(8*s)))
        rest = shoulder_l if raised == shoulder_r else shoulder_r
        draw_line(draw, [rest, (rest[0] + facing*105*s, rest[1] + 165*s), (rest[0] + facing*150*s, rest[1] + 185*s)], width=max(3, int(8*s)))
    elif state["gesture"] in {"point", "small_point", "snap"} and who == "respondent":
        arm = shoulder_r if facing > 0 else shoulder_l
        reach = 190*s if state["gesture"] == "point" else 130*s
        draw_line(draw, [arm, (arm[0] + facing*110*s, arm[1] + 30*s), (arm[0] + facing*reach, arm[1] + 5*s)], width=max(3, int(8*s)))
        other = shoulder_l if arm == shoulder_r else shoulder_r
        draw_line(draw, [other, (other[0] - facing*70*s, other[1] + 140*s), (other[0] - facing*78*s, other[1] + 180*s)], width=max(3, int(8*s)))
    elif state["gesture"] == "open_hand":
        draw_line(draw, [shoulder_r, (shoulder_r[0] + facing*90*s, shoulder_r[1] + 50*s), (shoulder_r[0] + facing*165*s, shoulder_r[1] + 20*s)], width=max(3, int(8*s)))
        draw_line(draw, [shoulder_l, (shoulder_l[0] - facing*65*s, shoulder_l[1] + 145*s), (shoulder_l[0] - facing*82*s, shoulder_l[1] + 180*s)], width=max(3, int(8*s)))
    else:
        draw_line(draw, [shoulder_l, (x - 135*s, y + 280*s), (x - 185*s, y + 300*s)], width=max(3, int(8*s)))
        draw_line(draw, [shoulder_r, (x + 135*s, y + 280*s), (x + 185*s, y + 300*s)], width=max(3, int(8*s)))
    # legs
    draw_line(draw, [pelvis, (x - 110*s, y + 470*s), (x - 185*s, y + 745*s), (x - 265*s, y + 760*s)], width=max(3, int(8*s)))
    draw_line(draw, [pelvis, (x + 90*s, y + 455*s), (x + 40*s, y + 750*s), (x + 80*s, y + 785*s)], width=max(3, int(8*s)))
    draw_face(draw, hx, hy, s, cap, state, facing)


def render_frame(i: int) -> Image.Image:
    t = i / FPS
    shot = current_shot(t)
    img = Image.new("RGB", (W, H), "#d2d0cb")
    draw = ImageDraw.Draw(img)
    draw_floor(draw)

    if shot.framing == "two":
        draw_table_plant(draw, 540, 1015, 0.9)
        draw_character(draw, "interviewer", 315, 560, 0.86, 1, t, shot)
        draw_character(draw, "respondent", 775, 560, 0.86, -1, t, shot)
    elif shot.framing == "respondent_close":
        draw_table_plant(draw, 800, 970, 0.85)
        draw_character(draw, "respondent", 500, 540, 1.18, 1, t, shot)
    else:
        draw_table_plant(draw, 300, 970, 0.85)
        draw_character(draw, "interviewer", 570, 540, 1.18, -1, t, shot)

    # simple cut flash accent for the first interruption only
    if 2.44 <= t < 2.50:
        overlay = Image.new("RGB", (W, H), "#f3f0e9")
        img = Image.blend(img, overlay, 0.18)
    return img


def write_timeline():
    data = {
        "fps": FPS,
        "width": W,
        "height": H,
        "audio_duration": AUDIO_DURATION,
        "frame_count": FRAME_COUNT,
        "lines": [line.__dict__ for line in LINES],
        "shots": [shot.__dict__ for shot in SHOTS],
        "silences": SILENCES,
        "notes": [
            "Speaker-specific approximate lip sync based on available machine transcript and silence detection.",
            "No local Whisper/Rhubarb was available; no phoneme-perfect lip sync is claimed.",
            "Visual direction follows reference study: sparse seated line-body comedy, held reactions, shot changes.",
        ],
    }
    (ASSETS / "full_timeline.json").write_text(json.dumps(data, indent=2), encoding="utf-8")


def render_all():
    FRAMES.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    write_timeline()
    for i in range(FRAME_COUNT):
        out = FRAMES / f"honest_full_{i:06d}.png"
        if out.exists():
            continue
        render_frame(i).save(out)
        if i % 120 == 0:
            print(f"rendered {i}/{FRAME_COUNT}")
    print(f"rendered {FRAME_COUNT} frames")


def make_contact_sheets():
    # Compact shot contact sheet: one representative frame per shot.
    reps = []
    for shot in SHOTS:
        mid = (shot.start + shot.end) / 2
        if shot.name == "S02_yes_reaction":
            mid = 2.68
        if shot.name == "S19_entrepreneur":
            mid = 69.6
        reps.append((shot.name, min(FRAME_COUNT - 1, round(mid * FPS))))

    cols = 5
    thumb_w, thumb_h = 216, 384
    label_h = 38
    rows = math.ceil(len(reps) / cols)
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "#f2f0ea")
    d = ImageDraw.Draw(sheet)
    for idx, (name, frame) in enumerate(reps):
        im = Image.open(FRAMES / f"honest_full_{frame:06d}.png").convert("RGB")
        th = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = (idx % cols) * thumb_w
        y = (idx // cols) * (thumb_h + label_h)
        d.text((x + 4, y + 3), f"{idx+1:02d} {name} F{frame:04d}", fill="#181310")
        sheet.paste(th, (x, y + label_h))
    sheet.save(REVIEW / "honest_interview_full_shot_contact_sheet.png")

    # Key beginning/cut/ending check sheet.
    checkpoints = [0, 59, 64, 69, 107, 193, 445, 491, 563, 674, 898, 1050, 1131, 1225, 1328, 1402, 1498, 1550, 1600, FRAME_COUNT - 1]
    rows = math.ceil(len(checkpoints) / cols)
    check = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "#f2f0ea")
    d = ImageDraw.Draw(check)
    for idx, frame in enumerate(checkpoints):
        im = Image.open(FRAMES / f"honest_full_{frame:06d}.png").convert("RGB")
        th = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = (idx % cols) * thumb_w
        y = (idx // cols) * (thumb_h + label_h)
        d.text((x + 4, y + 3), f"F{frame:04d} {frame/FPS:05.2f}s", fill="#181310")
        check.paste(th, (x, y + label_h))
    check.save(REVIEW / "honest_interview_full_timing_check_sheet.png")


if __name__ == "__main__":
    render_all()
    make_contact_sheets()
