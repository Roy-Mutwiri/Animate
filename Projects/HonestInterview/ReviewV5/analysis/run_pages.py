import subprocess
V='D:/Animate/Goal/Bro was so honest.mp4'
cuts=[900,948,991,1096,1187,1255,1310,1406,1459,1519,1562,1588,1617,1687]
who=['C','N','C','N','C','N','C','N','C','N','C','N','C']
HEAD={'C':'140,280,310,420','N':'205,290,360,430'}
BODY={'C':'90,280,360,700','N':'150,290,420,700'}
k=0
for s,(a,b) in enumerate(zip(cuts[:-1],cuts[1:])):
    w=who[s]
    for f0 in range(a,b,60):
        f1=min(b,f0+60)
        subprocess.run(['python','cropsheet.py',V,f'sheets/h{k:02d}_{w}_{f0}.png','12','0.8',HEAD[w],str(f0),str(f1)])
        subprocess.run(['python','cropsheet.py',V,f'sheets/b{k:02d}_{w}_{f0}.png','12','0.45',BODY[w],str(f0),str(f1)])
        k+=1
subprocess.run(['python','cropsheet.py',V,'sheets/end_1687.png','10','0.3','0,0,480,850','1687','1775'])
