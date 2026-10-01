"""Full film: build the XFL master timeline and render every frame through Animate."""
import sys, time
from script_film import frames, NFRAMES
from scene import build_document
from jsfl_render import make
tag = sys.argv[1] if len(sys.argv) > 1 else 'v5a'
lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0
hi = int(sys.argv[3]) if len(sys.argv) > 3 else NFRAMES
t = time.time()
st = frames()
x = build_document(st, '../xfl/honest_%s' % tag, 'honest_interview_%s' % tag)
print('xfl', x, round(time.time() - t, 1), 's')
j, l = make(x, '../frames/full_%s' % tag, list(range(lo, hi)), fla='../editable/honest_interview_%s_render.fla' % tag)
print(j); print(l)
