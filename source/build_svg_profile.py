from pathlib import Path
import base64, io, json, os, socket, struct, time, urllib.request, subprocess, zipfile, shutil
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT=Path(__file__).parent
OUT=ROOT/'Raunak_Flow_Studio_Updated'; A=OUT/'flow-assets'; A.mkdir(parents=True,exist_ok=True)
PAPER='#f8f6f1'; INK='#1c1b19'; ORANGE='#f64200'
fonts={k:TTFont('C:/Windows/Fonts/'+v) for k,v in {'regular':'arial.ttf','bold':'arialbd.ttf','italic':'georgiai.ttf','symbol':'seguisym.ttf'}.items()}
def text(s,x,y,size=18,font='regular',color=INK):
 f=fonts[font]; gs=f.getGlyphSet(); cmap=f.getBestCmap(); scale=size/f['head'].unitsPerEm; result=[]
 for c in s:
  cf=f if ord(c) in cmap else fonts['symbol']; cg=cf.getGlyphSet(); name=cf.getBestCmap().get(ord(c),'space'); pen=SVGPathPen(cg); cg[name].draw(pen); scale=size/cf['head'].unitsPerEm
  result.append(f'<path fill="{color}" transform="translate({x:.3f} {y}) scale({scale} {-scale})" d="{pen.getCommands()}"/>'); x+=cf['hmtx'][name][0]*scale
 return ''.join(result)
def lines(items,x,y,size=18,leading=23,**kw):return ''.join(text(s,x,y+i*leading,size,**kw) for i,s in enumerate(items))
def line(y):return f'<path d="M40 {y}H984" stroke="#a09b93" stroke-width="1"/>'
def svg(parts,h,title):return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1024" height="{h}" viewBox="0 0 1024 {h}" role="img"><title>{title}</title><rect width="1024" height="{h}" fill="{PAPER}"/>'+''.join(parts)+'</svg>'
h=[text('01 / FLOW STUDIO',42,30,15,'bold'),'<path d="M224 25H984" stroke="#a09b93"/>',text('Make work',40,128,76,'bold'),text('flow.',434,128,84,'italic',ORANGE),'<path d="M440 158Q525 132 615 149" stroke="#f64200" fill="none" stroke-width="3"/>',text('Raunak Vaja',42,206,53,'bold'),text('R&D & IT Manager at Windbridge Concepts',44,240,19),text('Ahmedabad, India',44,268,18),lines(['I turn everyday business processes into connected, dependable','workflows. With a background in operations, product development','and IT, I build practical automation and internal systems that bring','clarity, accuracy and consistency to day-to-day work.'],44,306,17,22),'<rect x="44" y="390" width="145" height="37" rx="7" fill="#f64200"/>',text('Portfolio ↗',62,415,18,'bold','#ffffff'),text('raunakvaja.pages.dev',207,415,18)]
(A/'hero-static.svg').write_text(svg(h,450,'Make work flow — Raunak Vaja'),encoding='utf-8')
b=[line(0),text('04',42,62,59,'bold'),lines(['INTERNAL','SYSTEMS'],139,37,15,19,font='bold'),text('/',266,58,44,'italic'),text('04',322,62,59,'bold'),lines(['DJANGO','PROJECTS'],418,37,15,19,font='bold'),text('Design → R&D → IT → Automation',648,47,19),line(86),text('Behind the scenes. Ahead of the repetition.',40,143,43,'bold')]
systems=[('01','Production SOT',['Centralizes order intake, tracking and','shipment reconciliation in one place.'],62,189),('02','Invoice Creation System',['Creates shipment-based invoices with validation,','review and PDF/Excel generation.'],520,229),('03','Checklist Automation',['Automates checklist validation using','defined business rules to reduce manual work.'],116,309),('04','Bill of Entry Checking',['Checks import documents, flags exceptions','and helps resolve issues early.'],632,349)]
for n,title,ls,x,y in systems:b += [text(n,x,y,20,'bold',ORANGE),text(title,x+40,y,23,'bold'),lines(ls,x+40,y+25,16,21)]
b += ['<path d="M390 210C450 199 428 248 496 236m-8-6 9 6-8 8 M508 327C570 312 547 365 612 350m-8-6 9 6-8 8" stroke="#f64200" fill="none" stroke-width="1.4"/>',text('Internal source and company data are not public.',44,414,13,color='#736f67'),line(436),text('DJANGO PROJECTS',40,466,15,'bold'),text('PREVIEWS · NOT LIVE DEMOS',731,466,13,color='#736f67')]
projects=[('Velvet Ember','velvet-home.webp',['Restaurant demo with','menu filters and a','session-based bag.']),('Recipe Explorer','recipe-discover.webp',['TheMealDB recipes','and a detailed','cooking view.']),('StreetX Store','street-home.webp',['Fake Store API catalog','with categories','and caching.']),('Quest Travel','quest-home.webp',['City search and place','details using the','Geoapify API.'])]
for i,(name,file,ls) in enumerate(projects):
 x=34+(i%2)*483;y=483+(i//2)*177
 im=Image.open(ROOT/'portfolio_source/site/assets/gallery'/file).convert('RGB'); w,hh=im.size; im=im.crop((0,0,w,min(hh,int(w/1.78)))) ;im.thumbnail((560,320)); bio=io.BytesIO(); im.save(bio,format='JPEG',quality=88)
 data=base64.b64encode(bio.getvalue()).decode()
 b += [f'<rect x="{x}" y="{y}" width="472" height="165" rx="16" fill="#eeeae3"/>',f'<clipPath id="p{i}"><rect x="{x+12}" y="{y+10}" width="276" height="145" rx="10"/></clipPath><image x="{x+12}" y="{y+10}" width="276" height="145" preserveAspectRatio="xMidYMin slice" clip-path="url(#p{i})" xlink:href="data:image/jpeg;base64,{data}"/>',text(name,x+303,y+34,21,'bold'),lines(ls,x+303,y+61,14,19),text('Source + previews ↗',x+303,y+143,13,'bold')]
b += [line(850),text('SKILLS',40,875,15,'bold')]
for x,title,ls,icon in [(46,'Connect & automate',['n8n, REST APIs, Webhooks,','JSON, Google Sheets, Telegram'],'↗'),(380,'Deploy & maintain',['Docker, Ubuntu, monitoring,','troubleshooting, backup & recovery'],'◇'),(722,'Build & analyse',['Python, Django, NumPy, pandas,','Matplotlib, Seaborn'],'</>')]:
 b += [text(icon,x,911,28,'bold',ORANGE),text(title,x+40,909,21,'bold'),lines(ls,x+40,934,15,21)]
b += ['<path d="M352 885V970M695 885V970" stroke="#a09b93"/>',line(987),text('LEARNING & COURSES',44,1020,14,'bold'),lines(['Completed foundation coursework: Python, Django, NumPy, pandas, Matplotlib and Seaborn.','Advanced Full Stack AI at Felix ITs — expected March 2027.'],303,1015,14,22),'<rect x="0" y="1061" width="1024" height="143" fill="#f64200"/>',lines(['Your next workflow.','My next chapter.'],39,1113,35,37,font='bold',color='#ffffff'),'<path d="M430 1080V1185M868 1080V1185" stroke="white"/>',lines(["I’m open to automation opportunities.",'Remote or relocation, with a one-month notice.'],465,1099,16,22,color='#ffffff'),text('Portfolio ↗    LinkedIn ↗    Email ↗',465,1164,19,'bold','#ffffff'),text('rv*',902,1149,52,'bold','#ffffff')]
(A/'profile-body.svg').write_text(svg(b,1204,'Automation systems, Django projects, skills and opportunities'),encoding='utf-8')

# Capture the portfolio's HTML/CSS animation with the browser's own renderer.
class CDP:
 def __init__(self,url):
  from urllib.parse import urlparse
  u=urlparse(url); self.s=socket.create_connection((u.hostname,u.port)); self.s.settimeout(30); key=base64.b64encode(os.urandom(16)).decode(); self.s.sendall(f'GET {u.path} HTTP/1.1\r\nHost: {u.netloc}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'.encode()); buf=b''
  while b'\r\n\r\n' not in buf:buf+=self.s.recv(1)
  assert b'101' in buf,buf;self.n=0
 def read(self,n):
  a=b''
  while len(a)<n:a+=self.s.recv(n-len(a))
  return a
 def call(self,m,p={}):
  self.n+=1; data=json.dumps({'id':self.n,'method':m,'params':p}).encode(); mask=os.urandom(4); n=len(data); head=bytes([129,128|n]) if n<126 else bytes([129,254])+struct.pack('!H',n);self.s.sendall(head+mask+bytes(c^mask[i%4] for i,c in enumerate(data)))
  while True:
   a,b=self.read(2);n=b&127
   if n==126:n=struct.unpack('!H',self.read(2))[0]
   elif n==127:n=struct.unpack('!Q',self.read(8))[0]
   data=self.read(n)
   if a&15==1:
    r=json.loads(data)
    if r.get('id')==self.n:
     if 'error'in r:raise RuntimeError(r['error'])
     return r.get('result',{})
work=ROOT/'orbit_capture';work.mkdir(exist_ok=True)
source=(ROOT/'portfolio_source/site/index.html').read_text(encoding='utf-8-sig'); start=source.index('<div class="hero-art"');end=source.index('<a class="scroll-note"',start);fragment=source[start:end]
css=(ROOT/'portfolio_source/site/styles.css').read_text(encoding='utf-8-sig')
html='<html><head><meta charset="utf-8"><style>'+css+'body{margin:0;width:1024px;height:560px;background:#f8f6f1;overflow:hidden}.hero-art{position:absolute!important;width:480px!important;height:480px!important;right:auto!important;left:40px!important;top:40px!important;opacity:1!important;z-index:1!important}</style></head><body>'+fragment+'</body></html>'
(work/'orbit.html').write_text(html,encoding='utf-8'); (OUT/'source').mkdir(exist_ok=True);(OUT/'source/orbit.html').write_text(html,encoding='utf-8')
args=['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','--headless=new','--no-sandbox','--disable-gpu','--disable-extensions','--no-first-run','--remote-debugging-port=9337','--remote-allow-origins=*','--allow-file-access-from-files','--hide-scrollbars','--user-data-dir='+str(work/'edge-profile'),'about:blank']
proc=subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=0x08000000)
try:
 for _ in range(100):
  try:pages=json.load(urllib.request.urlopen('http://127.0.0.1:9337/json'));break
  except Exception:time.sleep(.1)
 c=CDP(next(p['webSocketDebuggerUrl'] for p in pages if p['type']=='page'))
 c.call('Page.enable'); c.call('Emulation.setDeviceMetricsOverride',{'width':1024,'height':560,'deviceScaleFactor':1,'mobile':False})
 c.call('Page.navigate',{'url':(A/'hero-static.svg').as_uri()});time.sleep(.6)
 def shot(w,h):return Image.open(io.BytesIO(base64.b64decode(c.call('Page.captureScreenshot',{'format':'png','clip':{'x':0,'y':0,'width':w,'height':h,'scale':1}})['data']))).convert('RGB')
 header=shot(1024,450)
 c.call('Page.navigate',{'url':(work/'orbit.html').as_uri()});time.sleep(.5)
 c.call('Runtime.evaluate',{'expression':'window.animations=document.getAnimations();animations.forEach(a=>a.pause());animations.length','returnByValue':True})
 frames=[];orbits=[]
 for i in range(144):
  c.call('Runtime.evaluate',{'expression':f'animations.forEach(a=>a.currentTime={i*1000/12})'})
  orbit=shot(560,560);orbits.append(orbit.resize((400,400),Image.Resampling.LANCZOS))
  frame=header.copy();frame.paste(orbit.resize((390,390),Image.Resampling.LANCZOS),(632,47));frames.append(frame)
  if i%36==0: print('Captured',i,'of 144 frames',flush=True)
 palette=frames[0].quantize(colors=256,dither=Image.Dither.NONE)
 frames=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
 frames[0].save(A/'hero.gif',save_all=True,append_images=frames[1:],duration=[80,80,90]*48,loop=0,optimize=True,disposal=1)
 orbits[0].save(A/'orbit.gif',save_all=True,append_images=orbits[1:],duration=[80,80,90]*48,loop=0,optimize=True,disposal=1)
 frames[0].save(OUT/'header-preview.png')
 # Actual SVG browser rendering for visual QA and combined reference.
 c.call('Emulation.setDeviceMetricsOverride',{'width':1024,'height':1204,'deviceScaleFactor':1,'mobile':False});c.call('Page.navigate',{'url':(A/'profile-body.svg').as_uri()});time.sleep(.5);body=shot(1024,1204)
 combined=Image.new('RGB',(1024,1654),PAPER);combined.paste(frames[0]);combined.paste(body,(0,450));combined.save(OUT/'FULL_PREVIEW.png')
finally:proc.terminate()

readme='''<!-- Upload README.md and the complete flow-assets folder to raunakvaja/raunakvaja. -->
<p align="center"><a href="https://raunakvaja.pages.dev/"><img src="flow-assets/hero.gif" width="100%" alt="Raunak Vaja — Make work flow. R&D and IT Manager in Ahmedabad. Animated orbit captured from my portfolio." /></a><a href="https://raunakvaja.pages.dev/#projects"><img src="flow-assets/profile-body.svg" width="100%" alt="Four internal automation systems, four Django learning projects, toolkit and learning. Full text and repository links below." /></a></p>

**Explore:** [Portfolio](https://raunakvaja.pages.dev/) · [LinkedIn](https://www.linkedin.com/in/raunakvaja/) · [Email](mailto:raunakvaja@gmail.com)

**Project source & screenshots:** [Velvet Ember](https://github.com/raunakvaja/Velvet-Ember-Django) · [Recipe Explorer](https://github.com/raunakvaja/Recipe-Explorer-Django) · [StreetX Store](https://github.com/raunakvaja/StreetX-Store-Django) · [Quest Travel](https://github.com/raunakvaja/Quest-Travel-Django)

<details>
<summary>Read the profile as text · accessibility & searchable version</summary>

# Raunak Vaja — Make work flow.

R&D & IT Manager at Windbridge Concepts · Ahmedabad, India.

I turn everyday business processes into connected, dependable workflows. With a background in operations, product development and IT, I build practical automation and internal systems that bring clarity, accuracy and consistency to day-to-day work.

**Design → R&D → IT → Automation**

## Behind the scenes. Ahead of the repetition.

| Internal system | What it does |
|---|---|
| Production SOT | Centralizes order intake, production tracking, shipment reconciliation and reporting. |
| Invoice Creation System | Validates shipment and parcel data, supports review, and generates PDF/Excel outputs. |
| Checklist Automation | Applies defined Accounts & Finance checklist rules and validation. |
| Bill of Entry Checking | Checks import documents, flags exceptions and sends correction notifications. |

Internal source and company data are not public. I also work on workflow backups, recovery checks and Telegram notifications. [Automation case studies](https://raunakvaja.pages.dev/#work).

## Four completed Django learning projects

- **Velvet Ember:** Restaurant demo with menu filters, session-based bag and contact form validation.
- **Recipe Explorer:** TheMealDB recipes, ingredients, instructions and a dedicated cooking view.
- **StreetX Store:** Fake Store API product catalog with categories and caching.
- **Quest Travel:** Geoapify city search, nearby attractions and detailed place information.

These are learning demonstrations. Screenshots are previews, not live demos; no commercial payments, orders or bookings.

## Toolkit

- **Connect & automate:** n8n, REST APIs, Webhooks, JSON, Google Sheets, Telegram.
- **Deploy & maintain:** Docker, Ubuntu, monitoring, troubleshooting, workflow backups and recovery.
- **Build & analyse:** Python, Django, NumPy, pandas, Matplotlib, Seaborn.

Completed foundation coursework in Python, Django, NumPy, pandas, Matplotlib and Seaborn. Advanced Full Stack AI at Felix ITs — expected March 2027. Continuing JavaScript for n8n, resilient API integrations, Git and practical data projects.

## Your next workflow. My next chapter.

Open to automation opportunities · Remote or relocation · One-month notice.

[Portfolio](https://raunakvaja.pages.dev/) · [LinkedIn](https://www.linkedin.com/in/raunakvaja/) · [Email](mailto:raunakvaja@gmail.com) · [WhatsApp](https://wa.me/918447389219)

</details>
'''
(OUT/'README.md').write_text(readme,encoding='utf-8')
(OUT/'START_HERE.txt').write_text('''UPDATE YOUR GITHUB PROFILE

1. Extract this ZIP.
2. Open https://github.com/raunakvaja/raunakvaja
3. Choose Add file > Upload files.
4. Drag ONLY README.md and the complete flow-assets folder onto GitHub.
   Upload the folder contents from this package, not the ZIP or outer folder.
5. Commit message: Apply cream Flow Studio profile with portfolio orbit
6. Click Commit changes, then open your profile and refresh.

Do not upload source, FULL_PREVIEW.png, header-preview.png or this instruction file.
The updated README does not reference the earlier assets; those can remain safely.

WHAT IS INCLUDED
- hero.gif: custom typography stays still; only the actual portfolio orbit animates.
- orbit.gif: standalone recording from your saved portfolio HTML/CSS.
- hero-static.svg: outlined custom lettering on cream paper, provided as editable source.
- profile-body.svg: cream layout, actual project screenshots, skills and orange footer.
- Native links and an expandable text transcript in README.md.
- FULL_PREVIEW.png: rendered reference, not a file to upload.
- source/orbit.html: self-contained HTML/CSS source of the captured orbit.

GitHub controls the outer page background. The cream background belongs to the image panels.
SVG image text cannot be selected; use the expandable text transcript to copy it.
Links drawn inside an image are visual labels. The real clickable links are below the panels.
The header and body image each also link to your portfolio.
The GIF is a 12-second capture of the original CSS animation; it restarts when it loops.
The orbit was captured from your saved Portfolio_Cloudflare_Ready source package.
If the live portfolio has newer orbit code, replace source/orbit.html and re-render.
''',encoding='utf-8')
shutil.copy2(__file__,OUT/'source/build_svg_profile.py')
z=ROOT/'Raunak_Flow_Studio_Updated.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as archive:
 for p in OUT.rglob('*'):
  if p.is_file():archive.write(p,p.relative_to(OUT))
with zipfile.ZipFile(z) as archive:assert archive.testzip() is None
gif=Image.open(A/'hero.gif');assert gif.n_frames==144
print('ZIP READY',z,z.stat().st_size,'bytes; GIF frames',gif.n_frames,flush=True)
