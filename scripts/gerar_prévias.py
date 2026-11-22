from PIL import Image,ImageDraw,ImageFont
import cairosvg,io,pathlib
P=pathlib.Path(__file__).resolve().parents[1]
parts=['hero','about','stack','lab-header','lab-row-1','lab-row-2','lab-row-3','contact','assinatura']
for mobile in [False,True]:
 w=430 if mobile else 830; margin=20 if mobile else 52
 for theme in ['dark','light']:
  gap=12
  images=[]
  for i,name in enumerate(parts):
   ext='gif' if name=='assinatura' else 'svg'
   file=P/'assets'/f'{name}{"-m" if mobile else ""}-{theme}.{ext}'
   if ext=='svg':img=Image.open(io.BytesIO(cairosvg.svg2png(url=str(file),output_width=w))).convert('RGBA')
   else:img=Image.open(file).convert('RGBA')
   images.append(img)
  # lab no spaces; all other sections spacing
  canvas_h=sum(im.height for im in images)+4*gap+90
  bg='#0d1117' if theme=='dark' else '#fbfaf3'
  canvas=Image.new('RGB',(w+margin*2,canvas_h),bg)
  draw=ImageDraw.Draw(canvas)
  f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
  draw.text((margin,15),'PRÉVIA LOCAL V2 - NÃO PUBLICADO',fill='#f55c30' if theme=='dark' else '#ad3918',font=f)
  y=50
  for i,im in enumerate(images):
   canvas.paste(im,(margin,y),im)
   y+=im.height
   if i in (0,1,2,7):y+=gap
  canvas=canvas.crop((0,0,w+margin*2,y+margin))
  name=f'PREVIA-{("CELULAR" if mobile else "DESKTOP")}-{theme.upper()}.png'
  canvas.save(P/name,optimize=True)
  print(name,canvas.size)
