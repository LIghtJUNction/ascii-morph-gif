#!/usr/bin/env python3
"""Render clean, looping ASCII morph GIFs. Python 3.10+, Pillow, NumPy."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageColor
import argparse, json, math, numpy as np
W,H=88,56
Y,X=np.mgrid[0:H,0:W]; x=(X-44)/30; y=(Y-28)/22
CHARS=" .,:;!+*x%#@"
PRESETS={"coffee-galaxy":("coffee","galaxy"),"bulb-jellyfish":("bulb","jellyfish"),"plane-bird":("plane","bird")}
def mask(kind,t):
 im=Image.new('L',(W*4,H*4));d=ImageDraw.Draw(im)
 def ellipse(box,fill=150,outline=None,width=1): d.ellipse(tuple(v*4 for v in box),fill=fill,outline=outline,width=width*4)
 def line(points,fill=200,width=1): d.line([(a*4,b*4) for a,b in points],fill=fill,width=width*4)
 def poly(points,fill):d.polygon([(a*4,b*4) for a,b in points],fill=fill)
 if kind=='coffee':
  ellipse((21,39,68,45),110);ellipse((23,40,65,43),0)
  ellipse((58,22,73,36),210);ellipse((60,24,70,33),0)
  poly([(25,22),(63,22),(59,38),(30,38)],140)
  ellipse((25,18,63,26),235);ellipse((28,20,60,24),45)
  for j in range(3):line([(34+j*9+2*math.sin(k*.6+t*3+j),17-k) for k in range(12)],100,1)
 elif kind=='bulb':
  ellipse((28,9,60,37),190);poly([(32,28),(56,28),(51,40),(37,40)],160)
  for a in range(3):line([(37,40+a*2),(51,40+a*2)],220,1)
  line([(40,47),(48,47)],180,2)
  line([(40,38),(38,25),(43,29),(47,25),(49,38)],245,1)
  for a in np.arange(0,2*math.pi,.65):
   line([(44+21*math.cos(a),23+19*math.sin(a)),(44+25*math.cos(a),23+23*math.sin(a))],110)
 elif kind=='jellyfish':
  z=2*math.sin(t*math.pi*2);ellipse((24,10+z,64,35+z),180)
  d.rectangle((20*4,int((25+z)*4),68*4,40*4),fill=0)
  line([(24+k,25+z+1.8*math.sin(k*.45+t*3)) for k in range(41)],230)
  for j in range(8):
   line([(28+j*4+3*math.sin(k*.25-t*5+j),26+z+k) for k in range(19+j%3*2)],120+j%3*35,1)
 elif kind=='plane':
  poly([(15,17),(73,27),(31,39),(39,29)],200);poly([(15,17),(39,29),(73,27),(41,26)],85)
  line([(15,17),(41,26),(31,39)],250)
  line([(15-k*2,37+k*.4) for k in range(5)],95)
 elif kind=='bird':
  flap=math.sin(t*math.pi*4)*9
  poly([(44,30),(31,22+flap),(9,17+flap),(24,31),(41,34)],195)
  poly([(44,30),(57,22+flap),(79,17+flap),(64,31),(47,34)],195)
  ellipse((40,23,48,38),225);ellipse((41,19,47,26),230)
  poly([(42,35),(38,42),(44,39),(50,42),(46,35)],135)
 a=np.asarray(im.resize((W,H),Image.Resampling.LANCZOS),dtype=float)/255
 if kind=='galaxy':
  r=np.sqrt(x*x+(y*1.55)**2);ang=np.arctan2(y*1.55,x)
  arms=np.exp(-((np.sin(ang*2-r*6+t*2))/.24)**2)*np.exp(-r*1.4)
  a=arms*.85+np.exp(-r*r/ .028)
  a+=((np.sin(X*71.7+Y*27.3)> .997)&(r> .4))*.5
 return np.clip(a,0,1)

def choose_font(path=None):
    if path:
        return ImageFont.truetype(path,12)
    for candidate in ["DejaVuSansMono.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "/usr/share/fonts/TTF/DejaVuSansMono.ttf", "/System/Library/Fonts/Menlo.ttc", "C:/Windows/Fonts/consola.ttf"]:
        try: return ImageFont.truetype(candidate,12)
        except OSError: pass
    raise SystemExit("No monospace font found. Pass --font /path/to/monospace.ttf")

def load_mask(path):
    with Image.open(path) as source:
        # White foreground on black; alpha cuts out transparent backgrounds.
        alpha=source.getchannel("A") if "A" in source.getbands() else None
        im=source.convert("L")
        if alpha is not None:
            im=Image.fromarray((np.asarray(im,dtype=float)*np.asarray(alpha)/255).astype("uint8"))
        im.thumbnail((W-8,H-8),Image.Resampling.LANCZOS)
        canvas=Image.new("L",(W,H));canvas.paste(im,((W-im.width)//2,(H-im.height)//2))
        return np.asarray(canvas,dtype=float)/255

def make_frames(first,second,count,seed):
    noise=np.random.default_rng(seed).random((H,W))
    for i in range(count):
        t=i/count
        if t<.22:q=0
        elif t<.46:q=(t-.22)/.24
        elif t<.76:q=1
        else:q=1-(t-.76)/.24
        q=q*q*(3-2*q);dust=math.sin(math.pi*q)**2
        a=mask(first,t) if isinstance(first,str) else first
        b=mask(second,t) if isinstance(second,str) else second
        field=(a*(1-q)+b*q)*(1-.45*dust)
        field+=dust*.32*(noise>.86)*np.exp(-(x*x+y*y)/1.2)
        field*=.80+.20*np.sin(X*2.31+Y*1.77+i*.10)**2
        yield np.clip((field*(len(CHARS)-1)).astype(int),0,len(CHARS)-1)

def render(args):
    if bool(args.from_mask)!=bool(args.to_mask):raise SystemExit("Provide both --from-mask and --to-mask")
    if args.from_mask:
        first,second=load_mask(args.from_mask),load_mask(args.to_mask)
    else:first,second=PRESETS[args.preset]
    font=choose_font(args.font)
    cw=max(1,math.ceil(font.getlength("M")));ch=14
    if font.getbbox("M")[2]>cw:raise SystemExit("Use a regular monospace font")
    atlas=[]
    for c in CHARS:
        tile=Image.new("L",(cw,ch));ImageDraw.Draw(tile).text((0,0),c,font=font,fill=255)
        atlas.append(np.asarray(tile))
    atlas=np.stack(atlas)
    foreground=np.array(ImageColor.getrgb(args.foreground));background=np.array(ImageColor.getrgb(args.background))
    palette=[]
    for i in range(256):palette.extend((background+(foreground-background)*i/255).astype("uint8").tolist())
    side=max(W*cw,H*ch)+64
    images=[];texts=[]
    for idx in make_frames(first,second,args.frames,args.seed):
        pixels=atlas[idx].transpose(0,2,1,3).reshape(H*ch,W*cw)
        canvas=Image.new("L",(side,side));canvas.paste(Image.fromarray(pixels),((side-W*cw)//2,(side-H*ch)//2))
        if args.size!=side:canvas=canvas.resize((args.size,args.size),Image.Resampling.LANCZOS)
        # Fixed grayscale-indexed palette: no labels, logos, captions or watermark.
        im=Image.frombytes("P",canvas.size,canvas.tobytes());im.putpalette(palette);images.append(im)
        texts.append("\n".join("".join(CHARS[v] for v in row) for row in idx))
    output=Path(args.output);output.parent.mkdir(parents=True,exist_ok=True)
    images[0].save(output,save_all=True,append_images=images[1:],duration=args.frame_ms,loop=0,optimize=False,disposal=1)
    images[0].convert("RGB").save(output.with_name(output.stem+"-before.png"))
    images[int(args.frames*.6)].convert("RGB").save(output.with_name(output.stem+"-after.png"))
    if args.html:
        bg=args.background;fg=args.foreground
        doc='<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>ASCII morph</title><style>body{margin:0;background:'+bg+';color:'+fg+';display:grid;place-items:center;min-height:100vh}pre{font-family:monospace;font-size:clamp(5px,1.05vw,12px);line-height:1;white-space:pre}button{position:fixed;bottom:12px;right:12px;background:transparent;color:inherit;border:1px solid;padding:8px}</style><pre aria-label="Animated ASCII art"></pre><button>Pause</button><script>const frames='+json.dumps(texts)+';let i=0,paused=matchMedia("(prefers-reduced-motion: reduce)").matches;const p=document.querySelector("pre"),b=document.querySelector("button");p.textContent=frames[0];function label(){b.textContent=paused?"Play":"Pause"}label();b.onclick=()=>{paused=!paused;label()};setInterval(()=>{if(!paused){i=(i+1)%frames.length;p.textContent=frames[i]}},'+str(args.frame_ms)+')</script>'
        output.with_suffix(".html").write_text(doc,encoding="utf-8")
    print(json.dumps({"output":str(output),"frames":args.frames,"duration_ms":args.frames*args.frame_ms,"bytes":output.stat().st_size,"size":args.size}))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--preset",choices=PRESETS,default="coffee-galaxy")
    p.add_argument("--from-mask");p.add_argument("--to-mask")
    p.add_argument("--output",required=True)
    p.add_argument("--size",type=int,default=800)
    p.add_argument("--frames",type=int,default=110)
    p.add_argument("--frame-ms",type=int,default=90)
    p.add_argument("--font");p.add_argument("--seed",type=int,default=48)
    p.add_argument("--foreground",default="#dddddd");p.add_argument("--background",default="#080808")
    p.add_argument("--html",action="store_true")
    args=p.parse_args()
    if not 128<=args.size<=1600:p.error("--size must be 128..1600")
    if not 20<=args.frames<=300:p.error("--frames must be 20..300")
    if args.frame_ms<20 or args.frame_ms>1000 or args.frame_ms%10:p.error("--frame-ms must be 20..1000, in multiples of 10 (GIF timing)")
    if Path(args.output).suffix.lower()!=".gif":p.error("--output must end in .gif")
    render(args)
if __name__=="__main__":main()
