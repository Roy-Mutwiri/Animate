"""Representative section 0.00-19.40 s (frames 0-465): build XFL, render through Animate."""
import sys, time
from script_film import frames
from scene import build_document
from jsfl_render import make
N = 466
t = time.time()
st = frames()[:N]
x = build_document(st, '../xfl/rep_v5a', 'rep_v5a')
print('xfl', x, round(time.time() - t, 1), 's')
j, l = make(x, '../frames/rep_v5a', list(range(N)), fla='../editable/rep_v5a.fla')
print(j, l)
