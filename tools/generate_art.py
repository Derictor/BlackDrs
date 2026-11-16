from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math,random,hashlib,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]
def render(size,key,transparent):
    w,h=size
    seed=int.from_bytes(hashlib.sha256(key.encode()).digest()[:8],'big')
    rng=random.Random(seed)
    im=Image.new('RGBA',size,(0,0,0,0) if transparent else (15,13,29,255))
    light=Image.new('RGBA',size)
    d=ImageDraw.Draw(light)
    cx,cy=w*.5,h*.46
    for i in range(22,0,-1):
        x=w*i/48; y=h*i/51
        d.ellipse((cx-x,cy-y,cx+x,cy+y),fill=(62+i*2,39+i,122+i,14+i*2))
    im=Image.alpha_composite(im,light.filter(ImageFilter.GaussianBlur(w*.035)))
    d=ImageDraw.Draw(im)
    amber=(215,166,96,240); violet=(158,139,208,230)
    for i in range(320):
        a=rng.uniform(0,math.tau); rr=rng.uniform(.05,.55)
        x=cx+math.cos(a)*w*rr; y=cy+math.sin(a)*h*rr
        scale=max(1,w*rng.uniform(.0008,.004))
        d.ellipse((x,y,x+scale,y+scale),fill=(210,163,100,rng.randrange(55,220)))
    if any(x in key for x in ('DRUMS','MORPHEUS','HYPNOS','PHANTOM','ONEIROS','ERES','NYX','SANDMAN','EV_','SC_','Workshop')):
        points=[(.22,.92),(.28,.68),(.40,.58),(.36,.42),(.40,.25),(.50,.16),(.59,.26),(.65,.42),(.60,.57),(.75,.69),(.82,.92),(.51,.97)]
        d.polygon([(w*x,h*y) for x,y in points],fill=(23,20,42,255),outline=violet,width=max(1,w//160))
        d.polygon([(w*.42,h*.36),(w*.50,h*.30),(w*.59,h*.37),(w*.56,h*.50),(w*.50,h*.55),(w*.44,h*.49)],fill=(50,36,56,255))
        d.line((w*.445,h*.421,w*.478,h*.427),fill=amber,width=max(2,w//100))
        d.line((w*.52,h*.427,w*.553,h*.42),fill=amber,width=max(2,w//100))
        d.arc((w*.1,h*.08,w*.90,h*.88),190,345,fill=amber,width=max(1,w//125))
    else:
        count=3+seed%6
        pts=[(cx+math.sin(a*math.tau/count)*w*.28,cy+math.cos(a*math.tau/count)*h*.28) for a in range(count)]
        d.line(pts+[pts[0]],fill=violet,width=max(2,w//37))
        for idx,(x,y) in enumerate(pts):
            d.line((cx,cy,x,y),fill=amber if idx%2 else violet,width=max(2,w//53))
    return im
def main():
    manifest=E.parse(ROOT/'info.txt').getroot()
    paths={value for e in manifest.findall('IMAGE') for field in ('Path','Path2') if (value:=e.get(field))}
    paths.add(manifest.get('Graphic'))
    for value in sorted(paths):
        p=ROOT/value
        folder=p.parent.name
        size=(512,714) if folder in {'Cards','Portraits','Events','Scenes'} else (256,256)
        if p.name=='Workshop.jpg': size=(768,768)
        im=render(size,p.stem,folder=='Roster')
        p.parent.mkdir(parents=True,exist_ok=True)
        if p.suffix.lower()=='.jpg': im=im.convert('RGB')
        im.save(p)
if __name__=='__main__': main()
