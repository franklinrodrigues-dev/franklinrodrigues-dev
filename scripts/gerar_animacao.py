#!/usr/bin/env python3
"""Cria GIF do nome com brilho suave. Dependência: Pillow. Sem rede/GitHub."""
import json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE=Path(__file__).resolve().parents[1]
CFG=json.loads((BASE/'config/perfil.json').read_text(encoding='utf-8'))
NOME=CFG['nome'].upper()
OUTPUT=BASE/'assets'

def font(size):
    candidates=[
       '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf',
       '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
       'C:/Windows/Fonts/arialbd.ttf','arialbd.ttf','DejaVuSans-Bold.ttf'
    ]
    for candidate in candidates:
        try: return ImageFont.truetype(candidate,size)
        except OSError: pass
    return ImageFont.load_default()

def rgba(h):
    h=h.lstrip('#');return tuple(int(h[i:i+2],16) for i in (0,2,4))

def blend(a,b,f):
    return tuple(int(a[k]*(1-f)+b[k]*f) for k in range(3))

def make(theme,mobile):
    w,h=(430,162) if mobile else (830,146)
    bg=rgba('#0D1117' if theme=='dark' else '#FBFAF3')
    faint=rgba('#22241F' if theme=='dark' else '#D7D5C8')
    burnt=rgba('#743020' if theme=='dark' else '#AA482A')
    orange=rgba('#FF3800' if theme=='dark' else '#DC3D16')
    text_lines=NOME.split(' ',1) if mobile else [NOME]
    fit_font=[]
    mask=Image.new('L',(w,h),0)
    d=ImageDraw.Draw(mask)
    for idx,line in enumerate(text_lines):
        sz=72 if not mobile else 58
        while sz>20:
            ff=font(sz)
            b=d.textbbox((0,0),line,font=ff,stroke_width=0)
            if b[2]-b[0] <= w-70:break
            sz-=1
        fit_font.append((ff,line,b))
    if mobile:
        for idx,(ff,line,b) in enumerate(fit_font):
            width=b[2]-b[0];height=b[3]-b[1]
            cy=(59 if idx==0 else 119)
            x=(w-width)/2-b[0];y=cy-height/2-b[1]
            d.text((x,y),line,font=ff,fill=255)
    else:
        ff,line,b=fit_font[0]; width=b[2]-b[0];height=b[3]-b[1]
        d.text(((w-width)/2-b[0],h/2-height/2-b[1]),line,font=ff,fill=255)
    frames=[]
    for frame in range(24):
        im=Image.new('RGB',(w,h),bg)
        canvas=ImageDraw.Draw(im)
        for x in range(w):
            pos=x/max(w-1,1)
            # Orange is strongest at center, fading toward the edges.
            base=.06 + .92*math.exp(-((pos-.56)/.27)**2)
            basecolor=blend(faint,burnt,min(1,base*.48))
            basecolor=blend(basecolor,orange,min(.94,base*.82))
            # One moving vertical band produces the animated reflection.
            center=(-.15 + frame/23*1.3)
            glint=.40*math.exp(-((pos-center)/.095)**2)
            color=blend(basecolor,orange,glint)
            canvas.line((x,0,x,h),fill=color)
        out=Image.composite(im,Image.new('RGB',(w,h),bg),mask)
        border=ImageDraw.Draw(out)
        outline=rgba('#30322C' if theme=='dark' else '#D5D5C7')
        border.rectangle((0,0,w-1,h-1),outline=outline,width=1)
        inset=12 if mobile else 18
        border.rectangle((inset,13,w-inset-1,h-14),outline=outline,width=1)
        frames.append(out.quantize(colors=72))
    dest=OUTPUT/('assinatura' + ('-m' if mobile else '') + '-' + theme + '.gif')
    frames[0].save(dest,save_all=True,append_images=frames[1:],duration=115,loop=0,optimize=True,disposal=2)
    print(dest.name,round(dest.stat().st_size/1024),'KB')

if __name__=='__main__':
    for theme in ('dark','light'):
        for mobile in (False,True):make(theme,mobile)
