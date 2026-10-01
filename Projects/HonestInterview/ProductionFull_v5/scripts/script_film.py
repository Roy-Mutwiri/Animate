"""HonestInterview v5 acting script (times = seconds on the original audio).

Sources: reference shot/gesture log (ReviewV5/analysis/ref_shots_00_36.md, ref_shots_36_71.md),
dialogue turns + validated Rhubarb cues (assets/dialogue_turns.json, *_rhubarb.json).
CAP = respondent (cap, screen-left).  GL = interviewer (glasses, screen-right).
Intentions are written next to each beat; body changes follow thought changes, not every word.
"""
import os
from perf import Track, CamTrack, load_cues, assemble, F
from scene import Cam, CAM_TWO, CAM_CAP, CAM_GL
from script_film_tail import build_tail, iris

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')
NFRAMES = 1702          # ceil(70.889 s * 24)

# CAP head centre in world units = hip(-120,543) + chars.HEAD_C
CAP_HEAD = (-135.0, 359.0)


def cam_on_cap(z, sx, sy):
    """Camera that puts the CAP head centre at reference-screen (sx, sy) with zoom z."""
    return Cam(CAP_HEAD[0] - (sx - 240) / z, CAP_HEAD[1] - (sy - 425) / z, z)


def build():
    from jaw import frame_db
    cap = Track('CAP', load_cues(os.path.join(ASSETS, 'cap_rhubarb.json')),
                frame_db(os.path.join(ASSETS, 'cap_analysis.wav'), NFRAMES))
    gl = Track('GL', load_cues(os.path.join(ASSETS, 'nocap_rhubarb.json')),
               frame_db(os.path.join(ASSETS, 'nocap_analysis.wav'), NFRAMES))
    cam = CamTrack()

    # ------------------------------------------------------------ 1. 0.00-2.48  two-shot -> GL
    # GL: "Okay, for ten billion dollars, would you-"  Pleased with his big hypothetical; sells it.
    cam.cut(0.0, Cam(*CAM_TWO)).move(0.08, 1.48, Cam(*CAM_GL))
    gl.expr(0.0, 'sly').mouth(0.0, 0.25, 'X', 'smug')
    gl.blink(0.92, 2, 'happy')                       # pleased blink on "billion"
    gl.pose(2.20, 'point', frames=3)                 # hand leads out toward CAP, lands on "would you"
    # CAP in the two-shot: flat, already decided.
    cap.expr(0.0, 'neutral').blink(0.68, 2, 'half')

    # ------------------------------------------------------------ 2. 2.48-3.08  CAP "Yes."
    # Instant answer: no anticipation, one head jut on the word, a blink closes it.
    cam.cut(2.48, Cam(*CAM_CAP))
    cap.pose(2.64, 'jut', frames=1).pose(2.80, 'rest', frames=1)
    cap.blink(2.92, 2)

    # ------------------------------------------------------------ 3. 3.08-3.84  GL: interrupted
    # Expectation collapses: smile drops first, the pointing arm falls, lids lower, brows set.
    cam.cut(3.08, Cam(*CAM_GL))
    gl.mouth(3.08, 3.20, 'X', 'smug')
    gl.pose(3.28, 'rest', frames=2)
    gl.expr(3.20, 'neutral')
    gl.eyes(3.56, 'half').eyes(3.68, 'open').expr(3.68, 'angry').mouth(3.68, 4.84, 'X', 'sad')

    # ------------------------------------------------------------ 4. 3.84-4.56  CAP held cel
    cam.cut(3.84, Cam(*CAM_CAP))                     # 18 frames, nothing moves: the deadpan is the joke

    # ------------------------------------------------------------ 5. 4.56-7.20  GL objects
    # "Um, no, I didn't finish the question, I-"  Annoyed, trying to regain control; shrug of disbelief.
    cam.cut(4.56, Cam(*CAM_GL))
    gl.eyes(5.28, 'half').eyes(5.52, 'open')
    gl.pose(6.64, 'shrug', frames=3)
    gl.blink(6.84, 2)
    gl.pose(7.90, 'rest', frames=3)                  # off screen by now

    # ------------------------------------------------------------ 6. 7.20-19.40  CAP takes over
    cam.cut(7.20, Cam(*CAM_CAP))
    # "Listen here." cuts in mid-gesture: arm already out at the cut, brows arrive 2 frames later.
    cap.pose(7.20, 'point', frames=3)
    cap.brows(7.28, 'cap_angry').emo(7.28, 'angry')
    cap.pose(8.00, 'rest', frames=3)
    cap.mouth(8.00, 8.86, 'X', 'angry')              # set jaw, gathering the thought
    cap.blink(8.56, 3)
    # "There is nothing, and I mean nothing," - one finger, held while he talks
    cap.pose(9.40, 'finger_up', frames=3)
    cap.blink(11.36, 2)
    # "...that could come out of that little pie hole of yours" - aims it at him, lands with a blink
    cap.pose(11.84, 'point', frames=2)
    cap.blink(11.84, 2)
    cap.pose(14.40, 'point_push', frames=2, overshoot=1.08)
    cap.pose(15.52, 'rest', frames=2)
    cap.blink(15.68, 3)
    # "to make me turn down ... ten ... billion ... dollars." - each word gets a camera snap
    cam.move(16.52, 16.64, cam_on_cap(1.04, 228, 352), 'out')
    cam.move(17.40, 17.52, cam_on_cap(1.42, 222, 334), 'out')
    cam.move(18.24, 18.36, cam_on_cap(1.60, 230, 318), 'out')
    cap.pose(16.84, 'hook', frames=1).pose(17.12, 'rest', frames=2)
    cap.pose(17.60, 'hook', frames=1).pose(17.96, 'rest', frames=2)
    cap.eyes(17.76, 'closed').eyes(17.96, 'open')      # savouring "billion"
    cap.pose(18.24, 'jut', frames=1).pose(18.60, 'rest', frames=2)
    # the disdainful after-look, held into the cut
    cap.eyes(18.80, 'half').mouth(18.56, 19.40, 'X', 'sad')
    cap.expr(19.24, 'deadpan')

    build_tail(cam, cap, gl)
    return cam, cap, gl


def frames(n=NFRAMES):
    cam, cap, gl = build()
    return assemble(cam, cap, gl, n, iris)
