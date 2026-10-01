"""Checkpoint 1: three stills (two-shot, CAP single, GLASSES single) rendered by Animate."""
import sys
from scene import *
from chars import Pose
rest = Pose()
cap_talk = CharState(rest, 'open', None, ('C', 'neutral'))
gl_talk = CharState(rest, 'open', 'gl_sly', ('D', 'smug'))
cap_angry = CharState(Pose(far=('pts', (30.0, -110.0), (34.0, -150.0), 'finger_up', -80.0)), 'open', 'cap_angry', ('B', 'angry'))
gl_half = CharState(Pose(near=('pts', (-20.0, -90.0), (40.0, -110.0), 'point', -5.0)), 'half', 'gl_angry', ('X', 'sad'))
states = [
    FrameState(Cam(*CAM_TWO), CharState(rest), gl_talk),
    FrameState(Cam(*CAM_CAP), cap_talk, gl_talk),
    FrameState(Cam(*CAM_GL), cap_talk, gl_talk),
    FrameState(Cam(*CAM_CAP), cap_angry, gl_talk),
    FrameState(Cam(*CAM_GL), cap_talk, gl_half),
    FrameState(Cam(-100, 360, 1.6), cap_angry, gl_talk, iris=(540, 700, 520)),
]
print(build_document(states, '../xfl/stills_v5a', 'stills_v5a'))
