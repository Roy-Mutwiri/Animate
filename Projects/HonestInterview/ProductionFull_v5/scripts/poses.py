"""Pose and expression vocabulary for HonestInterview v5.

Poses are character-local (x = facing direction, y down, hip = origin), derived from the
reference gesture inventory (ReviewV5/analysis/ref_shots_*.md).  Both characters use the same
vocabulary; the glasses character is mirrored at placement time.
"""
from chars import Pose

REST = Pose()

POSES = {
    'rest': REST,
    'rest_back': Pose(lean=-4.0, legs='sit_back'),
    'lean_in': Pose(lean=7.0),
    'lean_in_more': Pose(lean=11.0, head=(3.0, 2.0)),
    'jut': Pose(lean=2.0, tilt=10.0),            # head rotates toward the listener on an emphatic word (ref 2.64s, 27.84s)
    'chin_up': Pose(lean=-3.0, tilt=-7.0),
    # far (forward) arm: forearm vertical, elbow stays near the armrest, index finger up
    'finger_up': Pose(far=('pts', (34.0, -84.0), (60.0, -140.0), 'finger_up', -70.0)),
    # far arm pointing at the other character, chest height, elbow slightly bent
    'point': Pose(lean=4.0, far=('pts', (40.0, -104.0), (92.0, -112.0), 'point', -6.0)),
    'point_push': Pose(lean=8.0, far=('pts', (52.0, -111.0), (110.0, -117.0), 'point', -4.0)),
    # both arms: palms-up shrug, upper arms down and out, forearms up
    'shrug': Pose(lean=-2.0, tilt=-4.0,
                  near=('pts', (-40.0, -82.0), (-58.0, -114.0), 'palm_up', 205.0),
                  far=('pts', (30.0, -82.0), (54.0, -114.0), 'palm_up', -25.0)),
    # far forearm lifted, open hand palm-up forward (small "come on" / presenting flick)
    'palm_up': Pose(far=('pts', (26.0, -76.0), (64.0, -98.0), 'palm_up', -20.0)),
    'palm_offer': Pose(lean=4.0, far=('pts', (34.0, -86.0), (84.0, -96.0), 'palm_up', -10.0)),
    # limp hooked hand dangling over the armrest front
    'hook': Pose(far=('pts', (20.0, -74.0), (66.0, -94.0), 'hook', 55.0)),
    # relaxed/confident: near arm draped over the chair back
    'drape': Pose(lean=-5.0, legs='sit_back', near=('pts', (-58.0, -134.0), (-108.0, -146.0), '', None)),
    # counting / listing: forearm up, two fingers
    'count': Pose(far=('pts', (24.0, -78.0), (44.0, -122.0), 'finger_up', -70.0)),
    'wave_off': Pose(far=('pts', (26.0, -80.0), (52.0, -126.0), 'open', -60.0)),
    # interrupting "hey hey hey": both forearms up, open hands forward
    'hey': Pose(lean=6.0, near=('pts', (-26.0, -86.0), (-6.0, -122.0), 'open', -70.0),
                far=('pts', (30.0, -88.0), (60.0, -124.0), 'open', -55.0)),
    # "hey hey hey": far arm straight out toward the listener, flat palm up (ref 47.56)
    'stop': Pose(lean=3.0, far=('pts', (50.0, -112.0), (108.0, -116.0), 'stop', -4.0)),
    # listener folds his arms across the chest (ref 50.52)
    'fold': Pose(lean=-3.0, near=('pts', (-22.0, -84.0), (28.0, -100.0), '', None),
                 far=('pts', (28.0, -84.0), (-22.0, -104.0), '', None)),
    # forearm pivots up from the elbow on the armrest, five splayed fingers (ref 59.56)
    'five': Pose(far=('pts', (24.0, -76.0), (58.0, -134.0), 'five', -66.0)),
    'five_b': Pose(far=('pts', (24.0, -76.0), (60.0, -133.0), 'five_b', -60.0)),
    # scheming businessman: forearms meet in a steeple in front of the chest (ref 69.40)
    'steeple': Pose(lean=3.0, near=('pts', (2.0, -74.0), (40.0, -102.0), 'fist', -40.0),
                    far=('pts', (20.0, -68.0), (42.0, -104.0), '', None)),
    'hands_lap': Pose(lean=3.0, near=('pts', (-8.0, -64.0), (30.0, -8.0), '', None),
                      far=('pts', (22.0, -64.0), (54.0, -6.0), '', None)),
}

# Expression presets: (eyes, brows, mouth emotion)
EXPR = {
    'CAP': {
        'neutral': ('open', None, 'neutral'),
        'angry': ('open', 'cap_angry', 'angry'),
        'deadpan': ('half', None, 'sad'),
        'bored': ('half_low', None, 'neutral'),
        'smug': ('half', None, 'smug'),
        'smug_closed': ('closed', None, 'smug'),
        'surprised': ('wide', 'cap_raise', 'neutral'),
        'annoyed': ('half', 'cap_angry', 'angry'),
        'pleased': ('happy', 'cap_raise', 'smug'),
    },
    'GL': {
        'neutral': ('open', 'gl_neutral', 'neutral'),
        'sly': ('open', 'gl_sly', 'smug'),
        'happy': ('happy', 'gl_raise', 'smug'),
        'angry': ('open', 'gl_angry', 'angry'),
        'annoyed': ('half', 'gl_angry', 'angry'),
        'deadpan': ('half', 'gl_neutral', 'sad'),
        'worried': ('open', 'gl_worry', 'sad'),
        'shocked': ('wide', 'gl_raise', 'neutral'),
        'disgust': ('squint', 'gl_angry', 'sad'),
        'pleading': ('half', 'gl_worry', 'sad'),
    },
}
