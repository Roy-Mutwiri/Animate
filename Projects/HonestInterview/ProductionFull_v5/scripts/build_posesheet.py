"""Pose-vocabulary check: every pose on both characters in their single set-ups."""
from scene import *
from poses import POSES, EXPR
names = list(POSES)
states = []
exprs = ['neutral', 'angry', 'deadpan', 'smug', 'surprised', 'annoyed', 'pleased', 'bored']
for i, n in enumerate(names):
    e, b, emo = EXPR['CAP'][exprs[i % len(exprs)]]
    states.append(FrameState(Cam(*CAM_CAP), CharState(POSES[n], e, b, ('C', emo)), CharState(POSES['rest'])))
gl_ex = ['neutral', 'sly', 'happy', 'angry', 'annoyed', 'deadpan', 'worried', 'shocked', 'disgust', 'pleading']
for i, n in enumerate(names):
    e, b, emo = EXPR['GL'][gl_ex[i % len(gl_ex)]]
    states.append(FrameState(Cam(*CAM_GL), CharState(POSES['rest']), CharState(POSES[n], e, b, ('D' if i % 2 else 'B', emo))))
states.append(FrameState(Cam(-100, 360, 1.6), CharState(POSES['rest']), CharState(POSES['rest']), iris=(540, 700, 420)))
print(build_document(states, '../xfl/posesheet', 'posesheet'), len(states), names)
