"""Crop contact sheet: python cropsheet.py VIDEO OUT COLS SCALE x0,y0,x1,y1 f0 f1 [step]
frames are source frame indices [f0,f1). Crop box may be 'auto' (uses SHOTS below for Bro video)."""
import sys, cv2
from PIL import Image, ImageDraw
v,out,cols,scale,box=sys.argv[1],sys.argv[2],int(sys.argv[3]),float(sys.argv[4]),sys.argv[5]
f0,f1=int(sys.argv[6]),int(sys.argv[7]); st=int(sys.argv[8]) if len(sys.argv)>8 else 1
x0,y0,x1,y1=map(int,box.split(','))
c=cv2.VideoCapture(v); fps=c.get(5); c.set(1,f0)
tiles=[]
for i in range(f0,f1):
    ok,fr=c.read()
    if not ok: break
    if (i-f0)%st: continue
    im=Image.fromarray(cv2.cvtColor(fr[y0:y1,x0:x1],cv2.COLOR_BGR2RGB))
    im=im.resize((int((x1-x0)*scale),int((y1-y0)*scale)),Image.LANCZOS)
    d=ImageDraw.Draw(im); lab=f"{i/fps:.2f} f{i}"
    d.rectangle([0,0,7*len(lab)+4,12],fill=(0,0,0)); d.text((2,0),lab,fill=(255,90,90))
    tiles.append(im)
w,h=tiles[0].size; rows=(len(tiles)+cols-1)//cols
S=Image.new('RGB',(cols*w+cols,rows*h+rows),'red')
for k,t in enumerate(tiles): S.paste(t,((k%cols)*(w+1),(k//cols)*(h+1)))
S.save(out); print(out,S.size,len(tiles))
