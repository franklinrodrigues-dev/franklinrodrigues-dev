#!/usr/bin/env python3
"""Gera artefatos visuais estáticos compatíveis com README do GitHub.
Uso: python scripts/gerar_perfil.py
Não publica, não faz commit e não acessa o GitHub.
"""
from __future__ import annotations
import html, json, math, pathlib, re, xml.etree.ElementTree as ET
BASE = pathlib.Path(__file__).resolve().parents[1]
DATA = json.loads((BASE/'config/perfil.json').read_text(encoding='utf8'))
ASSETS = BASE/'assets'
DARK = dict(bg='#0D1117', panel='#0D1117', line='#30322C', text='#FFFFE3', muted='#C0C0AD', dim='#929585', accent='#FF3800', icon='#858A80', green='#22C55E', soft='#151A1A')
LIGHT = dict(bg='#FBFAF3', panel='#FBFAF3', line='#D5D5C7', text='#20231F', muted='#66695E', dim='#838579', accent='#D33A12', icon='#777B73', green='#138C4A', soft='#F1EFE7')
FONT="'Inter', 'Segoe UI', Arial, sans-serif"
MONO="'JetBrains Mono', Consolas, monospace"
esc=lambda x: html.escape(str(x), quote=True)
def col(t, value): return t.get(value,value)
def txt(x,y,value,t,size=14,weight=500,color='text',anchor='',spacing=0,font=FONT):
    extra=f' text-anchor="{anchor}"' if anchor else ''
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{col(t,color)}" letter-spacing="{spacing}"{extra}>{esc(value)}</text>'
def rect(x,y,w,h,fill,stroke='',radius=0,sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>'
def line(x1,y1,x2,y2,t):return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{t["line"]}" fill="none"/>'
def base(w,h,t,label):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">',rect(0,0,w,h,t['bg'])]
def close(out):return '\n'.join(out+['</svg>'])
def frame(out,w,h,t,margin=0):
    out.append(rect(margin+.5,margin+.5,w-2*margin-1,h-2*margin-1,'none',t['line']))
def section(out,w,t,left,right,headerh=46):
    out.append(txt(23,29,left,t,11,750,spacing=1.2))
    out.append(txt(w-23,29,right,t,10,650,'dim','end',.5))
    out.append(line(0,headerh,w,headerh,t))
def words(s, limit):
    res=[];part=''
    for word in s.split():
        if part and len(part)+len(word)+1>limit:res.append(part);part=word
        else:part=f'{part} {word}'.strip()
    if part:res.append(part)
    return res

def hero(theme,mobile):
    t = DARK if theme=='dark' else LIGHT
    w,h=(430,216) if mobile else (830,230)
    out=base(w,h,t,'Franklin R. | Software Engineer & Builder')
    out.append('<defs><pattern id="dots" width="11" height="11" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.12" fill="'+ ('#384039' if theme=='dark' else '#D7D8CB') +'" opacity=".62"/></pattern></defs>')
    out.append(rect(0,47,w,h-47,'url(#dots)'))
    out.append(rect(.5,.5,w-1,h-1,'none',t['line']))
    out.append(line(0,47,w,47,t))
    out.append(txt(24 if not mobile else 15,30,DATA['topo_esquerdo'],t,10 if not mobile else 8.5,750,'muted',spacing=.75))
    if mobile:
        out.append(rect(w-112,23,6,6,t['green'],radius=3))
        out.append(txt(w-13,30,DATA['topo_direito'],t,9,700,'muted','end',.2))
    else:
        out.append(rect(w-145,23,7,7,t['green'],radius=4))
        out.append(txt(w-22,30,DATA['topo_direito'],t,10,750,'muted','end',.65))
    if mobile:
        out.append(txt(18,162,DATA['nome_curto'],t,65,900,spacing=-3.6))
        out.append(rect(289,150,17,17,t['accent'],radius=8.5))
    else:
        out.append(txt(29,187,DATA['nome_curto'],t,123,900,spacing=-7))
        out.append(rect(564,159,25,25,t['accent'],radius=12.5))
    return close(out)

def about(theme,mobile):
    t = DARK if theme=='dark' else LIGHT
    w,h=(430,293) if mobile else (830,231)
    out=base(w,h,t,'Sobre Franklin Rodrigues')
    frame(out,w,h,t); section(out,w,t,'SOBRE MIM','DESENVOLVIMENTO DE SOFTWARE')
    x=21 if mobile else 27
    if mobile:
        out.append(txt(x,79,'Tecnologia, aprendizado e',t,19,800))
        out.append(txt(x,104,'construção contínua.',t,19,800))
        y=134; n=46
    else:
        out.append(txt(x,86,'Tecnologia, aprendizado e construção contínua.',t,24,850))
        y=118;n=102
    for p in DATA['apresentacao']:
        for ln in words(p,n):
            out.append(txt(x,y,ln,t,12.5 if mobile else 13.5,450,'muted'))
            y+=21 if mobile else 24
        y+=11 if mobile else 9
    return close(out)

def icon_svg(name,x,y,size,t):
    local={'React':'react.svg','HTML5':'html5.svg','CSS3':'css3-alt.svg','JavaScript':'js.svg','Node.js':'node-js.svg','Git':'git.svg','Figma':'figma.svg','npm':'npm.svg'}
    if name in local:
        root=ET.parse(ASSETS/'logos'/local[name]).getroot()
        vb=root.attrib.get('viewBox','0 0 24 24')
        paths=[]
        for e in root.iter():
            if e.tag.rsplit('}',1)[-1]=='path' and e.attrib.get('d'):
                paths.append(f'<path d="{esc(e.attrib["d"])}" fill="{t["icon"]}"/>')
        return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{vb}">'+''.join(paths)+'</svg>'
    if name=='Vercel': return f'<path d="M{x+size/2} {y+2}L{x+size-2} {y+size-2} H{x+2}Z" fill="{t["icon"]}"/>'
    if name=='Supabase': return f'<path d="M{x+size*.46} {y+1}L{x+2} {y+size*.57}H{x+size*.46}L{x+size*.55} {y+size-1}L{x+size-2} {y+size*.38}H{x+size*.52}Z" fill="{t["icon"]}"/>'
    code={'Next.js':'N','TypeScript':'TS','FastAPI':'⚡','PostgreSQL':'PG','MySQL':'MY','SQLite':'SQ','SQL Developer':'SQL','Postman':'PM','ChatGPT':'AI'}
    val=code.get(name,'<>')
    return rect(x+1,y+1,size-2,size-2,'none',t['icon'],3)+txt(x+size/2,y+size*.68,val,t,10 if len(val)>1 else 16,850,'icon','middle',-.3)

def stack(theme,mobile):
    t = DARK if theme=='dark' else LIGHT
    w=430 if mobile else 830
    cols=2 if mobile else 4
    rowh=67 if mobile else 64
    rows=math.ceil(len(DATA['tecnologias'])/cols)
    h=46+rows*rowh
    out=base(w,h,t,'Tecnologias e ferramentas')
    frame(out,w,h,t);section(out,w,t,'TECNOLOGIAS','FERRAMENTAS E CONHECIMENTOS')
    cw=w/cols
    for i,name in enumerate(DATA['tecnologias']):
        c=i%cols;r=i//cols;x=c*cw;y=46+r*rowh
        out.append(rect(x+.5,y+.5,cw-1,rowh-1,'none',t['line']))
        out.append(icon_svg(name,x+18,y+(rowh-24)/2,24,t))
        out.append(txt(x+52,y+rowh/2+4,name,t,12.2 if mobile else 12.8,650))
    return close(out)

def mark(kind,x,y,t):
    a=t['accent']
    if kind=='web':
        return f'<path d="M{x} {y+5}H{x+44}V{y+43}H{x}Z" fill="none" stroke="{a}" stroke-width="3"/>'+f'<path d="M{x+17} {y+16}l-8 8 8 8m10-16 8 8-8 8" fill="none" stroke="{a}" stroke-width="3"/>'
    if kind=='api':
        return f'<circle cx="{x+12}" cy="{y+20}" r="10" stroke="#96D20A" stroke-width="5" fill="none"/><circle cx="{x+36}" cy="{y+25}" r="10" stroke="#96D20A" stroke-width="5" fill="none"/><path d="M{x+18} {y+24}L{x+30} {y+20}" stroke="#96D20A" stroke-width="5"/>'
    return f'<path d="M{x+5} {y+14}C{x+5} {y+1} {x+42} {y+1} {x+42} {y+14}V{y+38}C{x+42} {y+50} {x+5} {y+50} {x+5} {y+38}Z" fill="none" stroke="#1CB89D" stroke-width="4"/><path d="M{x+5} {y+23}C{x+5} {y+36} {x+42} {y+36} {x+42} {y+23}" fill="none" stroke="#1CB89D" stroke-width="4"/>'

def lab_header(theme,mobile):
    t=DARK if theme=='dark' else LIGHT;w=430 if mobile else 830;h=45
    out=base(w,h,t,'Laboratório de desenvolvimento: categorias')
    out.append(rect(.5,.5,w-1,h-1,'none',t['line']))
    out.append(txt(20,28,'LABORATÓRIO',t,11,750,spacing=1.15))
    out.append(txt(w-20,28,'EM CONSTRUÇÃO',t,10,680,'dim','end',.5))
    return close(out)

def lab_row(theme,mobile,index):
    t=DARK if theme=='dark' else LIGHT
    w,h=(430,123) if mobile else (830,98)
    job=DATA['laboratorio'][index]
    out=base(w,h,t,job['nome']+'; acessar página em desenvolvimento')
    out.append(rect(.5,.5,w-1,h-1,'none',t['line']))
    # Sem dados de projetos prontos: são áreas de criação.
    if mobile:
        out.append(line(44,0,44,h,t));out.append(line(387,0,387,h,t))
        out.append(txt(22,67,f'{index+1:02}',t,12,650,'dim','middle'))
        out.append(mark(job['icone'],58,15,t))
        out.append(txt(117,38,job['nome'],t,18.5,800))
        out.append(txt(117,58,job['descricao'],t,11,450,'muted'))
        x=116
        for tag in job['tecnologias']:
            width= min(104, max(63, len(tag)*7.1+15))
            out.append(rect(x,77,width,21,'none',t['line']))
            out.append(txt(x+6,92,tag,t,10,700,'muted'))
            x+=width+7
        out.append(txt(410,70,'↗',t,26,700,'accent','middle'))
    else:
        for boundary in (46,442,665,770):out.append(line(boundary,0,boundary,h,t))
        out.append(txt(23,56,f'{index+1:02}',t,12,650,'dim','middle'))
        out.append(mark(job['icone'],64,25,t))
        out.append(txt(123,45,job['nome'],t,23,800))
        out.append(txt(123,69,job['descricao'],t,12.5,450,'muted'))
        x=463
        for tag in job['tecnologias']:
            width=min(105,max(65,len(tag)*6.9+16))
            out.append(rect(x,37,width,24,'none',t['line']))
            out.append(txt(x+7,53,tag,t,10,750,'muted'))
            x+=width+8
        out.append(txt(718,57,'EM BREVE',t,10.5,750,'dim','middle'))
        out.append(txt(799,61,'↗',t,27,700,'accent','middle'))
    return close(out)

def contact(theme,mobile):
    t=DARK if theme=='dark' else LIGHT
    w,h=(430,420) if mobile else (830,327)
    out=base(w,h,t,'Contato profissional Franklin Rodrigues')
    frame(out,w,h,t)
    section(out,w,t,'CONTATO',DATA['contato_titulo'])
    if mobile:
        out.append(txt(22,103,'Vamos construir',t,39,900,spacing=-1.65))
        out.append(txt(22,148,'juntos.',t,53,900,'accent',spacing=-2.4))
        out.append(txt(22,175,'Trocas de ideias sobre tecnologia,',t,12.5,500,'muted'))
        out.append(txt(22,195,'produtos digitais e software.',t,12.5,500,'muted'))
        out.append(line(0,215,w,215,t))
        out.append(txt(21,238,'E-MAIL DIRETO',t,10,750,'muted',spacing=.8))
        out.append(txt(21,264,'rodrigues.tecnologia.dev',t,21,800,spacing=-.5))
        out.append(txt(21,288,'@gmail.com',t,21,800,spacing=-.5))
        out.append(line(0,304,w,304,t))
        out.append(line(215,304,215,h,t))
        out.append(txt(19,331,'LOCALIZAÇÃO',t,10,730,'muted',spacing=.6))
        out.append(txt(19,358,DATA['localizacao'],t,15,750))
        out.append(txt(230,331,'FUSO HORÁRIO',t,10,730,'muted',spacing=.6))
        out.append(txt(230,358,DATA['fuso'],t,15,750))
        out.append(line(0,380,w,380,t))
        out.append(txt(20,404,'CONECTANDO IDEIAS',t,11,720,'accent',spacing=.7))
    else:
        out.append(line(440,46,440,h,t))
        out.append(line(440,177,w,177,t))
        out.append(line(440,261,w,261,t))
        out.append(line(641,177,641,261,t))
        out.append(txt(28,132,'Vamos construir',t,50,900,spacing=-2.25))
        out.append(txt(28,199,'juntos.',t,65,900,'accent',spacing=-3.0))
        out.append(txt(28,245,'Trocas de ideias sobre tecnologia,',t,12.5,450,'muted'))
        out.append(txt(28,267,'produtos digitais e desenvolvimento.',t,12.5,450,'muted'))
        out.append(txt(466,73,'E-MAIL DIRETO',t,10,750,'muted',spacing=1))
        out.append(txt(466,114,'rodrigues.tecnologia.dev',t,22,800,spacing=-.7))
        out.append(txt(466,142,'@gmail.com',t,22,800,spacing=-.7))
        out.append(txt(466,201,'LOCALIZAÇÃO',t,10,730,'muted',spacing=.65))
        out.append(txt(466,234,DATA['localizacao'],t,16,700))
        out.append(txt(661,201,'FUSO HORÁRIO',t,10,730,'muted',spacing=.65))
        out.append(txt(661,234,DATA['fuso'],t,16,700))
        out.append(txt(466,285,'CONEXÕES',t,10,730,'muted',spacing=.75))
        out.append(rect(466,302,7,7,t['green'],radius=3.5))
        out.append(txt(485,310,'Tecnologia e colaboração',t,13.5,650))
    return close(out)

def pic(name,alt):
    align=' align="left"' if name.startswith('lab-') else ''
    return f'''<picture>
  <source media="(prefers-color-scheme: light) and (max-width: 600px)" srcset="./assets/{name}-m-light.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/{name}-light.svg" />
  <source media="(max-width: 600px)" srcset="./assets/{name}-m-dark.svg" />
  <img src="./assets/{name}-dark.svg" width="100%"{align} alt="{esc(alt)}" />
</picture>'''
def pic_footer():
    return '''<picture>
  <source media="(prefers-color-scheme: light) and (max-width: 600px)" srcset="./assets/assinatura-m-light.gif" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/assinatura-light.gif" />
  <source media="(max-width: 600px)" srcset="./assets/assinatura-m-dark.gif" />
  <img src="./assets/assinatura-dark.gif" width="100%" alt="Assinatura Franklin Rodrigues com degradê animado" />
</picture>'''

def make_readme():
    out=['<!-- Gerado por scripts/gerar_perfil.py. Para trocar textos, edite config/perfil.json. -->']
    for name,alt in [('hero','Franklin R. - Software Engineer and Builder'),('about','Sobre mim'),('stack','Tecnologias e ferramentas')]:
        out.append(f'<p align="center">\n{pic(name,alt)}\n</p>')
    out.append('<!-- Cada linha do laboratório tem seu próprio link clicável. -->')
    head=pic('lab-header','Laboratório, áreas em construção')
    rows=[f'<a href="{esc(j["link"])}" title="Abrir área em desenvolvimento: {esc(j["nome"])}">{pic(f"lab-row-{i+1}",j["nome"]+" - em desenvolvimento")}</a>' for i,j in enumerate(DATA['laboratorio'])]
    out.append('<div align="center">\n'+head+'\n'+ '\n'.join(rows)+'\n<br clear="all" />\n</div>')
    out.append(f'<p align="center">\n<a href="mailto:{esc(DATA["email"])}" title="Enviar e-mail">{pic("contact","Contato profissional")}</a>\n</p>')
    out.append(f'<p align="center">\n{pic_footer()}\n</p>')
    return '\n\n'.join(out)+'\n'

def make_preview():
    parts=['hero','about','stack','lab-header']+[f'lab-row-{i+1}' for i in range(len(DATA['laboratorio']))]+['contact','assinatura']
    def source(name):
        if name=='assinatura': return pic_footer()
        return pic(name,name.replace('-', ' '))
    out=['''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prévia do README v2 | Franklin Rodrigues</title><style>
    html,body{margin:0;background:#0d1117;color:#ffffe3;font-family:Inter,Arial,sans-serif}main{max-width:830px;margin:26px auto 44px;padding:0 12px}header{padding-bottom:18px}header h1{font-size:20px;margin:14px 0 4px}header p{color:#aaa;margin:0;font-size:12px}.tip{display:inline-block;padding:7px 12px;border:1px solid #333;color:#ff481c;font-size:11px}main img{display:block;width:100%;height:auto}main a{display:block;line-height:0}main a:hover{opacity:.88}.section{margin-bottom:14px}.lab{margin-bottom:14px}
    </style></head><body><main><header><span class="tip">PRÉVIA LOCAL V2 • NÃO PUBLICADO</span><h1>Franklin Rodrigues</h1><p>As setas abrem páginas reais de desenvolvimento. Nada foi publicado no seu GitHub.</p></header>''']
    for tag in parts:
        item=source(tag)
        if tag.startswith('lab-row-'):
            idx=int(tag.rsplit('-',1)[-1])-1
            item=f'<a href="{esc(DATA["laboratorio"][idx]["link"])}" title="Abrir página de desenvolvimento">{item}</a>'
        elif tag=='contact':
            item=f'<a href="mailto:{esc(DATA["email"])}">{item}</a>'
        if tag in ('hero','about','stack','contact','assinatura'):
            item='<div class="section">'+item+'</div>'
        if tag=='lab-header':item='<div class="lab">'+item
        if tag=='lab-row-3':item+='</div>'
        out.append(item)
    out.append('</main></body></html>')
    (BASE/'PREVIA.html').write_text('\n'.join(out),encoding='utf8')

def make_pages():
    for j in DATA['laboratorio']:
        p=BASE/j['link'];p.parent.mkdir(exist_ok=True,parents=True)
        content=f'''# {j['nome']}\n\n**Status: em preparação**\n\nEste espaço fará parte do laboratório de desenvolvimento de Franklin Rodrigues.\n\nAqui serão publicados projetos, códigos, decisões técnicas e demonstrações conforme forem desenvolvidos.\n\n**Temas de interesse:** {', '.join(j['tecnologias'])}.\n\nNenhum projeto foi anunciado como concluído nesta seção.\n\n[Voltar ao perfil](../README.md)\n'''
        p.write_text(content,encoding='utf8')

def build():
    for theme in ('dark','light'):
        for mobile in (False,True):
            suffix='-m' if mobile else ''
            for name,fn in [('hero',hero),('about',about),('stack',stack),('lab-header',lab_header),('contact',contact)]:
                (ASSETS/f'{name}{suffix}-{theme}.svg').write_text(fn(theme,mobile),encoding='utf8')
            for i in range(len(DATA['laboratorio'])):
                (ASSETS/f'lab-row-{i+1}{suffix}-{theme}.svg').write_text(lab_row(theme,mobile,i),encoding='utf8')
    (BASE/'README.md').write_text(make_readme(),encoding='utf8')
    make_preview();make_pages()
    print('README + SVGs + páginas em desenvolvimento gerados localmente, sem publicar.')

# V5 aprovada: sobreposição das seções atualizadas sobre a base V2.
# Todo conteúdo é regenerável a partir de config/perfil.json.

def hero(theme,mobile):
    t=DARK if theme=='dark' else LIGHT
    w,h=(430,216) if mobile else (830,230)
    out=base(w,h,t,'Franklin R., perfil em evolução')
    dots='#384039' if theme=='dark' else '#D7D8CB'
    out.append(f'<defs><pattern id="dots" width="11" height="11" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.12" fill="{dots}" opacity=".62"/></pattern></defs>')
    out.append(rect(0,47,w,h-47,'url(#dots)'))
    frame(out,w,h,t)
    out.append(line(0,47,w,47,t))
    # Sem cargo duplicado à esquerda, como aprovado.
    status=DATA['topo_direito']
    if mobile:
        out.append(rect(w-102,23,7,7,t['green'],radius=3.5))
        out.append(txt(w-16,30,status,t,9.7,750,'muted','end',.3))
        out.append(txt(18,162,DATA['nome_curto'],t,65,900,spacing=-3.6))
        out.append(rect(310,148,18,18,t['accent'],radius=9))
    else:
        out.append(rect(w-112,23,7,7,t['green'],radius=3.5))
        out.append(txt(w-22,30,status,t,10,750,'muted','end',.5))
        out.append(txt(29,187,DATA['nome_curto'],t,123,900,spacing=-7))
        out.append(rect(590,159,25,25,t['accent'],radius=12.5))
    return close(out)

def icon_svg(name,x,y,size,t):
    local={'React':'react.svg','HTML5':'html5.svg','CSS3':'css3-alt.svg','JavaScript':'js.svg','Node.js':'node-js.svg','Git':'git.svg','Figma':'figma.svg','npm':'npm.svg','FastAPI':'fastapi.svg','DBeaver':'dbeaver.svg'}
    if name in local:
        root=ET.parse(ASSETS/'logos'/local[name]).getroot()
        vb=root.attrib.get('viewBox','0 0 24 24')
        shapes=[]
        for e in root.iter():
            k=e.tag.rsplit('}',1)[-1]
            if k=='path' and e.attrib.get('d'):
                shapes.append(f'<path d="{esc(e.attrib["d"])}" fill="{t["icon"]}"/>')
        return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{vb}">'+''.join(shapes)+'</svg>'
    if name=='Vercel':return f'<path d="M{x+size/2} {y+2}L{x+size-2} {y+size-2} H{x+2}Z" fill="{t["icon"]}"/>'
    if name=='Supabase':return f'<path d="M{x+size*.46} {y+1}L{x+2} {y+size*.57}H{x+size*.46}L{x+size*.55} {y+size-1}L{x+size-2} {y+size*.38}H{x+size*.52}Z" fill="{t["icon"]}"/>'
    code={'Next.js':'N','TypeScript':'TS','PostgreSQL':'PG','MySQL':'MY','SQLite':'SQ','SQL Developer':'SQL','SQL':'SQL','Postman':'PM'}
    val=code.get(name,'<>')
    return rect(x+1,y+1,size-2,size-2,'none',t['icon'],3)+txt(x+size/2,y+size*.68,val,t,9 if len(val)>2 else 10 if len(val)>1 else 16,850,'icon','middle',-.3)

def stack(theme,mobile):
    t = DARK if theme=='dark' else LIGHT
    w=430 if mobile else 830
    cols=2 if mobile else 4
    rowh=67 if mobile else 64
    rows=math.ceil(len(DATA['tecnologias'])/cols)
    h=46+rows*rowh
    out=base(w,h,t,'Tecnologias')
    frame(out,w,h,t)
    # Sem o rótulo 'Ferramentas e conhecimentos' à direita.
    out.append(txt(23,29,'TECNOLOGIAS',t,11,750,spacing=1.2))
    out.append(line(0,46,w,46,t))
    cw=w/cols
    for i,name in enumerate(DATA['tecnologias']):
        c=i%cols;r=i//cols;x=c*cw;y=46+r*rowh
        out.append(rect(x+.5,y+.5,cw-1,rowh-1,'none',t['line']))
        out.append(icon_svg(name,x+18,y+(rowh-24)/2,24,t))
        out.append(txt(x+52,y+rowh/2+4,name,t,11.8 if mobile else 12.8,650))
    return close(out)

def contact(theme,mobile):
    t=DARK if theme=='dark' else LIGHT
    w,h=(430,400) if mobile else (830,327)
    out=base(w,h,t,'Contato Franklin Rodrigues')
    frame(out,w,h,t)
    section(out,w,t,'CONTATO',DATA['contato_titulo'])
    mail=DATA['email']
    if mobile:
        out.append(txt(22,98,'Vamos construir',t,39,900,spacing=-1.65))
        out.append(txt(22,143,'juntos.',t,53,900,'accent',spacing=-2.4))
        out.append(txt(22,172,'Trocas de ideias sobre tecnologia,',t,12.5,500,'muted'))
        out.append(txt(22,193,'produtos digitais e software.',t,12.5,500,'muted'))
        out.append(line(0,215,w,215,t))
        out.append(txt(21,239,'E-MAIL',t,10,750,'muted',spacing=.8))
        out.append(txt(21,274,mail,t,17,750,spacing=-.65))
        out.append(line(0,301,w,301,t))
        out.append(line(215,301,215,h,t))
        out.append(txt(19,328,'LOCALIZAÇÃO',t,10,730,'muted',spacing=.6))
        out.append(txt(19,358,DATA['localizacao'],t,15,750))
        out.append(txt(230,328,'FUSO HORÁRIO',t,10,730,'muted',spacing=.6))
        out.append(txt(230,358,DATA['fuso'],t,15,750))
    else:
        out.append(line(440,46,440,h,t))
        out.append(line(440,177,w,177,t))
        out.append(line(440,261,w,261,t))
        out.append(line(641,177,641,261,t))
        out.append(txt(28,132,'Vamos construir',t,50,900,spacing=-2.25))
        out.append(txt(28,199,'juntos.',t,65,900,'accent',spacing=-3.0))
        out.append(txt(28,245,'Trocas de ideias sobre tecnologia,',t,12.5,450,'muted'))
        out.append(txt(28,267,'produtos digitais e desenvolvimento.',t,12.5,450,'muted'))
        out.append(txt(466,73,'E-MAIL',t,10,750,'muted',spacing=1))
        out.append(txt(466,112,mail,t,16.6,780,spacing=-.7))
        out.append(txt(466,201,'LOCALIZAÇÃO',t,10,730,'muted',spacing=.65))
        out.append(txt(466,234,DATA['localizacao'],t,16,700))
        out.append(txt(661,201,'FUSO HORÁRIO',t,10,730,'muted',spacing=.65))
        out.append(txt(661,234,DATA['fuso'],t,16,700))
        out.append(txt(466,285,'CONEXÕES',t,10,730,'muted',spacing=.75))
        out.append(rect(466,302,7,7,t['green'],radius=3.5))
        out.append(txt(485,310,'Tecnologia e colaboração',t,13.5,650))
    return close(out)

SOCIAL=[('portfolio','PORTFÓLIO','portfolio',DATA['portfolio'],182),('linkedin','LINKEDIN','linkedin',DATA['linkedin'],158),('instagram','INSTAGRAM','instagram',DATA['instagram'],164),('email','E-MAIL','email','mailto:'+DATA['email'],145)]

def social_svg(theme,name,label,icon,w):
    t=DARK if theme=='dark' else LIGHT
    main=name=='portfolio'
    h=43
    bg=t['text'] if main else t['bg']
    fore=t['bg'] if main else t['text']
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">',rect(.5,.5,w-1,h-1,bg,t['line'] if not main else fore)]
    ix=18;iy=13
    if icon=='instagram':
        out.append(f'<rect x="{ix}" y="{iy}" width="16" height="16" rx="4" fill="none" stroke="{fore}" stroke-width="1.5"/><circle cx="{ix+8}" cy="{iy+8}" r="3.3" fill="none" stroke="{fore}" stroke-width="1.4"/><circle cx="{ix+12.3}" cy="{iy+3.8}" r="1" fill="{fore}"/>')
    elif icon=='email':
        out.append(f'<rect x="{ix}" y="{iy+2}" width="16" height="12" fill="none" stroke="{fore}" stroke-width="1.35"/><path d="M{ix} {iy+2}l8 7 8-7" stroke="{fore}" stroke-width="1.25" fill="none"/>')
    elif icon=='linkedin':
        out.append(f'<rect x="{ix}" y="{iy}" width="16" height="16" stroke="{fore}" stroke-width="1.2" fill="none"/><circle cx="{ix+4.9}" cy="{iy+5.15}" r="1.25" fill="{fore}"/><rect x="{ix+3.87}" y="{iy+7.24:.2f}" width="2.06" height="5.20" fill="{fore}"/><path d="M{ix+8.05} {iy+7.24:.2f}h1.98v.72c.42-.56 1.03-.84 1.84-.84 1.78 0 2.2 1.17 2.2 2.65v2.67h-1.96v-2.55c0-.65-.09-1.15-.90-1.15-.79 0-1.17.49-1.17 1.25v2.45h-1.99z" fill="{fore}"/>')
    else:
        out.append(f'<path d="M{ix} {iy+14}v-12h16v12h-16zm4-10v8m4-8v8m4-8v8" fill="none" stroke="{fore}" stroke-width="1.4"/>')
    out.append(txt(47,27,label,t,10.3,800,fore,spacing=.7))
    if name=='portfolio':out.append(txt(w-12,27,'↗',t,14,700,fore,'end'))
    return close(out)

def make_readme():
    out=['<!-- Perfil Franklin Rodrigues, versão V5 aprovada. Para trocar dados edite config/perfil.json, depois execute python scripts/gerar_perfil.py. -->']
    out.append(f'<p align="center">\n{pic("hero","Franklin R., em evolução")}\n</p>')
    out.append(f'<p align="center">\n{pic("about","Sobre mim")}\n</p>')
    social=[]
    for name,label,icon,url,w in SOCIAL:
        social.append(f'<a href="{esc(url)}" title="{esc(label)}"><picture><source media="(prefers-color-scheme: light)" srcset="./assets/btn-{name}-light.svg" /><img src="./assets/btn-{name}-dark.svg" width="{w}" height="43" alt="{esc(label)}" /></picture></a>')
    out.append('<p align="left">\n  '+'\n  '.join(social)+'\n</p>')
    out.append(f'<p align="center">\n{pic("stack","Tecnologias")}\n</p>')
    out.append('<!-- Cada linha do laboratório tem seu próprio link clicável. -->')
    head=pic('lab-header','Laboratório, áreas em construção')
    rows=[f'<a href="{esc(j["link"])}" title="Abrir área em desenvolvimento: {esc(j["nome"])}">{pic(f"lab-row-{i+1}",j["nome"]+" - em desenvolvimento")}</a>' for i,j in enumerate(DATA['laboratorio'])]
    out.append('<div align="center">\n'+head+'\n'+ '\n'.join(rows)+'\n<br clear="all" />\n</div>')
    out.append(f'<p align="center">\n<a href="mailto:{esc(DATA["email"])}" title="Enviar e-mail">{pic("contact","Contato profissional")}</a>\n</p>')
    out.append(f'<p align="center">\n{pic_footer()}\n</p>')
    return '\n\n'.join(out)+'\n'

def make_preview():
    out=['''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Franklin Rodrigues: prévia dos arquivos para GitHub</title><style>body{background:#0d1117;color:#ffffe3;font:14px Arial;margin:0} main{max-width:830px;margin:15px auto;padding:8px}main img{max-width:100%;height:auto;display:block} p{margin:0 0 12px} .social{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px}.social img{width:auto} .lab a{display:block;line-height:0}.lab{margin-bottom:12px} .lead{font-size:12px;color:#ff3800}</style></head><body><main><p class="lead">PRÉVIA LOCAL, SEM PUBLICAÇÃO NO GITHUB</p>''']
    out.append(pic('hero','Cabeçalho'))
    out.append('<p></p>'+pic('about','Sobre mim'))
    out.append('<p></p><nav class="social">')
    for name,label,icon,url,w in SOCIAL:out.append(f'<a href="{esc(url)}" title="{esc(label)}"><img src="assets/btn-{name}-dark.svg" width="{w}" height="43" alt="{esc(label)}"></a>')
    out.append('</nav>'+pic('stack','Tecnologias'))
    out.append('<div class="lab">'+pic('lab-header','Laboratório'))
    for i,j in enumerate(DATA['laboratorio']):out.append(f'<a href="{esc(j["link"])}">{pic(f"lab-row-{i+1}",j["nome"])}</a>')
    out.append('</div><a href="mailto:'+esc(DATA['email'])+'">'+pic('contact','Contato')+'</a>')
    out.append('<p></p>'+pic_footer()+'</main></body></html>')
    (BASE/'PREVIA_GITHUB.html').write_text('\n'.join(out),encoding='utf8')

def build():
    for theme in ('dark','light'):
        for mobile in (False,True):
            suffix='-m' if mobile else ''
            for name,fn in [('hero',hero),('about',about),('stack',stack),('lab-header',lab_header),('contact',contact)]:
                (ASSETS/f'{name}{suffix}-{theme}.svg').write_text(fn(theme,mobile),encoding='utf8')
            for i in range(len(DATA['laboratorio'])):
                (ASSETS/f'lab-row-{i+1}{suffix}-{theme}.svg').write_text(lab_row(theme,mobile,i),encoding='utf8')
        for name,label,ico,url,w in SOCIAL:
            (ASSETS/f'btn-{name}-{theme}.svg').write_text(social_svg(theme,name,label,ico,w),encoding='utf8')
    (BASE/'README.md').write_text(make_readme(),encoding='utf8')
    make_preview();make_pages()
    print('README V5, SVGs, botões e links gerados localmente. Nada foi enviado ao GitHub.')

if __name__=='__main__':build()
