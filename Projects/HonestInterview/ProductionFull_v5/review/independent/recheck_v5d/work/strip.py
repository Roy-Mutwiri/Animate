"""strip.py OUT f0 f1 x0 y0 x1 y1 [cols] [tilew] -- prod every frame crop, speech marker bar (red=CAP speaking, blue=NOCAP)"""
import sys,json
from PIL import Image,ImageDraw
F='D:/Animate/Projects/HonestInterview/ProductionFull_v5/frames/full_v5d/f%06d.png'
T=json.load(open('D:/Animate/Projects/HonestInterview/ProductionFull_v5/assets/dialogue_turns.json'))['turns']
out=sys.argv[1]; f0,f1,x0,y0,x1,y1=map(int,sys.argv[2:8]); cols=int(sys.argv[8]) if len(sys.argv)>8 else 12; W=int(sys.argv[9]) if len(sys.argv)>9 else 150
tiles=[]
for f in range(f0,f1+1):
    t=f/24; im=Image.open(F%f).convert('RGB').crop((x0,y0,x1,y1)); im=im.resize((W,int(im.height*W/im.width)),Image.LANCZOS)
    d=ImageDraw.Draw(im); lab=f'{t:.2f} f{f}'; d.rectangle([0,0,7*len(lab)+4,12],fill=(0,0,0)); d.text((2,0),lab,fill=(255,255,0))
    sp=[u for u in T if u['start']<=t<u['end']]
    for u in sp:
        col=(220,0,0) if u['speaker']=='CAP' else (0,80,255)
        d.rectangle([0,im.height-8,W,im.height],fill=col)
        w=[x['w'] for x in u['words'] if x['start']<=t<x['end']]
        if w: d.text((3,im.height-22),w[0],fill=col)
    tiles.append(im)
w,h=tiles[0].size; rows=(len(tiles)+cols-1)//cols
S=Image.new('RGB',(cols*(w+2),rows*(h+2)),(30,30,30))
for k,t in enumerate(tiles): S.paste(t,((k%cols)*(w+2),(k//cols)*(h+2)))
S.save(out); print(out,S.size)
