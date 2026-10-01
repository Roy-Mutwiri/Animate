from xfl import *
d = Document(1080, 1920, 24, '#FFFFFF')
m = d.symbol('Test/Mouth')
L = m.timeline.layer('art')
shapes = []
for i, (rx, ry, col) in enumerate([(40, 5, '#000000'), (40, 25, '#8B1A1A'), (20, 30, '#1A4B8B')]):
    s = Shape(); s.add(Path().ellipse(0, 0, rx, ry), fill=col, stroke='#000000', weight=4)
    L.key(i, 1, [s])
sc = d.scene('Scene 1')
bg = sc.layer('shapes')
s = Shape()
s.add(Path().poly([(100,100),(400,100),(400,400),(100,400)], close=True), fill='#FF0000')            # CW on screen
s.add(Path().poly([(600,100),(600,400),(900,400),(900,100)], close=True), fill='#00AA00')            # CCW on screen
s.add(Path().ellipse(540, 800, 200, 150), fill='#DDDDDD', stroke='#000000', weight=6)
s.add(Path().smooth([(100,1200),(300,1000),(500,1300),(800,1100)]), stroke='#000000', weight=8)
bg.key(0, 24, [s])
inst = sc.layer('mouth')
inst.key(0, 12, [Instance('Test/Mouth', 300, 1500, first=1)], tween=True)
inst.key(12, 12, [Instance('Test/Mouth', 800, 1600, rot=30, first=2)])
print(d.write('../tests/xfl_test', 'xfl_test'))
