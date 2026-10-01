"""Acting script 19.40 s to the end (continues script_film.build)."""
from scene import Cam, CAM_CAP, CAM_GL


def build_tail(cam, cap, gl):
    # ------------------------------------------------------------ 7. 19.40-23.40  GL, face only
    # "Even if one random person had to die?"  Appalled; testing whether CAP means it.
    cam.cut(19.40, Cam(*CAM_GL))
    gl.expr(19.40, 'angry').mouth(19.40, 20.02, 'D', 'angry')       # aghast hold over the cut
    gl.eyes(20.00, 'half').eyes(20.12, 'open').eyes(20.24, 'half').eyes(20.40, 'open')
    gl.eyes(20.96, 'half').eyes(21.40, 'open')                       # "come on" deadpan lids
    gl.eyes(22.48, 'half').eyes(22.62, 'open').eyes(23.20, 'half')

    # ------------------------------------------------------------ 8. 23.40-25.56  CAP "Yes. The answer is yes."
    cam.cut(23.40, Cam(*CAM_CAP))
    cap.expr(23.40, 'neutral')
    cap.eyes(23.68, 'half').expr(23.80, 'deadpan')                   # bored, honest
    cap.eyes(24.48, 'open').eyes(24.92, 'half')
    cap.expr(25.00, 'angry')

    # ------------------------------------------------------------ 9. 25.56-27.76  GL presses
    # "Okay, what if it was someone you knew?"  Personal now; offers the question with an open palm.
    cam.cut(25.56, Cam(*CAM_GL))
    gl.expr(25.56, 'angry').eyes(25.76, 'half').eyes(26.00, 'open')
    gl.eyes(27.00, 'half').eyes(27.06, 'open')
    gl.pose(27.12, 'palm_offer', frames=1)
    gl.eyes(27.64, 'half')
    gl.pose(28.30, 'rest', frames=2)

    # ------------------------------------------------------------ 10. 27.76-37.92  CAP escalates
    # "Yes. Take my aunt. Take my grandma. Hell, you could blow the block up.
    #  Can you even fathom how much money ten billion dollars is?"  Casual certainty -> lecturing.
    cam.cut(27.76, Cam(*CAM_CAP))
    cap.pose(27.84, 'jut', frames=1).pose(27.96, 'rest', frames=1)
    cap.blink(28.08, 2)
    cap.pose(28.52, 'drape', frames=3)                               # lounges: family is expendable
    cap.expr(28.56, 'bored').blink(28.84, 3)
    cap.pose(29.84, 'shrug', frames=3)
    cap.expr(29.84, 'angry')
    cap.pose(30.52, 'rest', frames=3)
    cap.blink(31.20, 2)
    cap.pose(31.96, 'palm_up', frames=2)                             # "can you even fathom"
    cap.pose(32.68, 'rest', frames=2)
    cap.blink(32.92, 1)
    cap.blink(34.12, 3).blink(34.64, 2).blink(35.56, 1).blink(36.80, 3)
    cap.pose(37.80, 'rest_back', frames=2)                           # settles back, done

    # ------------------------------------------------------------ 11. 37.92-39.64  GL "Oh, it's just a hypothetical."
    cam.cut(37.92, Cam(*CAM_GL))
    gl.expr(37.92, 'worried')                                        # uneasy: backing off
    gl.expr(38.12, 'neutral')
    gl.expr(38.68, 'angry').blink(38.76, 2)
    gl.pose(39.00, 'shrug', frames=3)
    gl.pose(39.52, 'rest', frames=3)
    gl.mouth(39.56, 39.64, 'X', 'sad')

    # ------------------------------------------------------------ 12. 39.64-43.84  CAP "And if it was a reality, I'd be first in line."
    cam.cut(39.64, Cam(*CAM_CAP))
    cap.pose(39.64, 'rest', frames=0)
    cap.expr(39.64, 'angry').expr(39.68, 'neutral')
    cap.eyes(41.00, 'closed').eyes(41.12, 'half')                    # the honest half-lid, held
    cap.blink(42.20, 2)

    # ------------------------------------------------------------ 13. 43.84-47.48  GL moral objection
    # "You're talking about human lives for ten billion dollars. What would-"  (cut off mid-word)
    cam.cut(43.84, Cam(*CAM_GL))
    gl.expr(43.84, 'worried').expr(43.96, 'angry')
    gl.blink(44.92, 2)
    gl.eyes(46.52, 'half').eyes(46.64, 'open')
    gl.eyes(47.24, 'half')

    # ------------------------------------------------------------ 14. 47.48-50.20  CAP "Hey, hey, hey, hey. Guess what?"
    # Steamrolls him: the arm is already coming up on the first frame, held, dropped in one frame.
    cam.cut(47.48, Cam(*CAM_CAP))
    cap.pose(47.56, 'stop', frames=2)
    cap.expr(47.48, 'annoyed').eyes(47.52, 'open').brows(47.68, None).emo(47.68, 'neutral')
    cap.pose(48.96, 'rest', frames=0)
    cap.eyes(49.80, 'closed').eyes(49.92, 'open')                    # smug on "what"
    cap.expr(50.00, 'angry')

    # ------------------------------------------------------------ 15. 50.20-52.40  GL "I don't want to guess. Don't make me guess."
    cam.cut(50.20, Cam(*CAM_GL))
    gl.expr(50.20, 'worried')
    gl.pose(50.52, 'fold', frames=3)                                 # closes himself off
    gl.look(50.68, -27.0).expr(50.68, 'shocked')                     # turns away to camera...
    gl.eyes(50.76, 'closed')                                         # ...refusing to engage
    gl.look(51.64, 0.0).expr(51.64, 'angry')                         # snaps back: aimed at CAP
    gl.blink(51.76, 1)

    # ------------------------------------------------------------ 16. 52.40-56.24  CAP coaxes
    # "Oh, come on. You gotta be curious about what I'm going to tell you."
    cam.cut(52.40, Cam(*CAM_CAP))
    cap.expr(52.40, 'neutral').mouth(52.68, 52.80, 'X', 'neutral')
    cap.pose(52.92, 'lean_in', frames=3)                             # leans in, teasing
    cap.blink(53.96, 2)
    cap.pose(55.30, 'rest', frames=3)
    cap.mouth(55.24, 56.24, 'X', 'sad')
    cap.blink(55.64, 2).blink(55.80, 2)                              # savouring the suspense

    # ------------------------------------------------------------ 17. 56.24-58.36  GL "What?"
    cam.cut(56.24, Cam(*CAM_GL))
    gl.eyes(56.24, 'half').brows(56.24, 'gl_neutral').emo(56.24, 'sad')   # flat, unimpressed
    gl.pose(57.00, 'shrug', frames=5)                                # unfolds straight into the shrug
    gl.pose(57.64, 'rest', frames=3)

    # ------------------------------------------------------------ 18. 58.36-60.76  CAP "I would have did it for five."
    cam.cut(58.36, Cam(*CAM_CAP))
    cap.expr(58.36, 'neutral').eyes(58.36, 'half')
    cap.blink(59.12, 3)
    cap.eyes(59.52, 'open')                                          # eyes pop as the hand rises
    cap.pose(59.56, 'five', frames=2)
    for k, t in enumerate([59.64, 59.68, 59.76, 59.84, 59.88, 59.96, 60.04]):
        cap.pose(t, 'five_b' if k % 2 == 0 else 'five', frames=0)   # the "five" wag
    cap.pose(60.24, 'rest', frames=3)
    cap.eyes(60.24, 'closed').eyes(60.36, 'half').mouth(60.36, 60.76, 'X', 'sad')

    # ------------------------------------------------------------ 19. 60.76-62.48  GL "Five billion?!"
    cam.cut(60.76, Cam(*CAM_GL))
    gl.expr(60.76, 'angry').mouth(60.76, 61.08, 'X', 'angry')
    gl.jitter(60.84, 62.40)                                          # rage tremble
    gl.eyes(61.80, 'half').eyes(61.90, 'open')
    gl.mouth(62.08, 62.48, 'B', 'angry')                             # gritted teeth into the cut

    # ------------------------------------------------------------ 20. 62.48-63.52  CAP "Thousand."
    # The bigger reveal is played smaller: deadpan, no gesture.
    cam.cut(62.48, Cam(*CAM_CAP))
    cap.expr(62.48, 'neutral').eyes(62.48, 'closed').eyes(62.56, 'open')
    cap.eyes(63.12, 'closed').expr(63.24, 'annoyed')

    # ------------------------------------------------------------ 21. 63.52-64.68  GL "What are you?"
    cam.cut(63.52, Cam(*CAM_GL))
    gl.expr(63.52, 'angry')
    gl.eyes(64.00, 'half').eyes(64.12, 'open')
    gl.mouth(64.00, 64.20, 'E', 'angry')                             # "you?" held 5 frames past the word
    gl.mouth(64.20, 64.68, 'X', 'sad')

    # ------------------------------------------------------------ 22. 64.68-end  CAP
    # "Oh, that's a good question.  I guess you can call me an entrepreneur."
    cam.cut(64.68, Cam(*CAM_CAP))
    cap.expr(64.68, 'neutral').eyes(64.68, 'half').eyes(64.84, 'open')   # mock-sincere
    cap.eyes(65.14, 'closed').eyes(65.42, 'open')
    cap.mouth(66.28, 66.64, 'X', 'neutral')                          # the idea arrives...
    cap.emo(66.64, 'smug').mouth(66.64, 66.68, 'X', 'smug')          # ...first smile of the film
    cap.blink(66.96, 2).blink(67.68, 2)
    cap.brows(67.84, 'cap_angry')                                    # cocky V brows on the grin
    cap.blink(68.84, 2).eyes(68.92, 'half').eyes(69.30, 'open')
    cap.pose(69.40, 'steeple', frames=1)                             # the businessman
    cap.eyes(70.20, 'closed').mouth(70.46, 70.92, 'B', 'smug')          # closed-eye teeth grin
    cap.eyes(70.76, 'open')

    # ending push-in about a fixed screen point just above the brim (ref 67.52-70.80)
    fx, fy = 192.0, 307.0
    wx, wy = CAM_CAP[0] + (fx - 240), CAM_CAP[1] + (fy - 425)
    table = [(67.52, 1.001), (67.72, 1.010), (68.00, 1.039), (68.40, 1.109), (68.56, 1.156), (68.84, 1.267),
             (69.00, 1.355), (69.24, 1.50), (69.44, 1.62), (69.68, 1.84), (70.00, 2.08), (70.40, 2.29),
             (70.72, 2.36), (70.80, 2.37)]
    for (t0, z0), (t1, z1) in zip(table, table[1:]):
        cam.move(t0, t1, Cam(wx - (fx - 240) / z1, wy - (fy - 425) / z1, z1), 'lin')


# iris-out centred on the frame (ref 69.08-70.88); radius in reference px
IRIS = [(69.08, 520), (69.20, 440), (69.28, 390), (69.36, 344), (69.44, 304), (69.52, 271), (69.60, 245),
        (69.68, 227), (69.76, 214), (69.84, 208), (70.20, 205), (70.40, 198), (70.60, 189), (70.72, 180),
        (70.80, 173), (70.88, 164), (70.92, 158)]


def iris(f):
    t = f / 24.0
    if t < IRIS[0][0]:
        return None
    for (t0, r0), (t1, r1) in zip(IRIS, IRIS[1:]):
        if t0 <= t <= t1:
            r = r0 + (r1 - r0) * (t - t0) / (t1 - t0)
            return (540.0, 960.0, r * 2.25)
    return (540.0, 960.0, IRIS[-1][1] * 2.25)
