"""Render the approved essay and extract ornament from the supplied plate."""
from pathlib import Path
import html
import re
import shutil
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets/patterns/egyptian'
ASSETS.mkdir(parents=True, exist_ok=True)
source = ASSETS / 'egyptian-3.jpg'
if not source.exists():
    shutil.copyfile(Path.home() / 'Downloads/egyptian-3-1600.jpg', source)
im = Image.open(source).convert('RGB')
# Loose outlines exclude adjoining figures and printed specimen numbers.
polygons = {
    '14': [(73,116),(368,116),(374,215),(316,308),(310,555),(135,557),(131,314),(72,211)],
    '16': [(390,188),(442,188),(444,141),(606,143),(610,205),(652,210),(675,260),(611,322),(611,704),(437,704),(438,324),(389,264)],
    '11': [(704,157),(739,148),(740,119),(851,117),(943,147),(947,182),(981,225),(961,280),(921,348),(921,569),(762,569),(757,349),(703,232)],
    '13': [(39,668),(73,638),(77,609),(155,582),(270,621),(276,651),(316,688),(294,757),(253,829),(252,995),(92,995),(89,832),(39,743)],
    '12': [(751,690),(788,642),(833,625),(890,587),(976,624),(979,655),(1028,696),(1033,731),(970,796),(968,995),(810,995),(809,802),(751,740)],
    '3': [(103,1052),(148,1014),(256,1034),(256,1104),(245,1140),(249,1466),(106,1469),(101,1106)],
    '2': [(800,1048),(889,1016),(949,1080),(949,1120),(941,1160),(946,1468),(801,1468),(800,1131)],
    '1': [(250,945),(276,861),(361,785),(473,750),(583,747),(695,772),(782,834),(814,910),(812,960),(758,1048),(699,1090),(680,1191),(679,1443),(653,1475),(567,1495),(451,1484),(385,1456),(386,1235),(377,1141),(337,1084),(282,1029)]
}
for name, polygon in polygons.items():
    mask = Image.new('L', im.size)
    ImageDraw.Draw(mask).polygon(polygon, fill=255)
    box = mask.getbbox()
    rgb = np.asarray(im.crop(box)).astype(float)
    inside = np.asarray(mask.crop(box)) > 0
    # Flood only the surrounding warm paper. Enclosed light areas of the
    # illustrations remain opaque; fine dark outlines preserve the silhouettes.
    paper = (rgb[:,:,0] > 170) & (rgb[:,:,1] > 155) & (rgb[:,:,2] > 140) & (rgb[:,:,2] < rgb[:,:,0]*.93) & (rgb[:,:,0]-rgb[:,:,1] < 48) & (rgb[:,:,0]-rgb[:,:,2] < 90)
    # Close tiny breaks in the printed outline before flooding the paper.
    barrier = ndimage.binary_closing(~paper & inside, iterations=2)
    paper &= ~barrier
    traversable = paper | ~inside
    seeds = ~inside
    seeds[0,:] = traversable[0,:]
    seeds[-1,:] = traversable[-1,:]
    seeds[:,0] = traversable[:,0]
    seeds[:,-1] = traversable[:,-1]
    outside = ndimage.binary_propagation(seeds, mask=traversable)
    solid = inside & ~outside
    # Remove isolated paper texture and plate-number remnants.
    labels, _ = ndimage.label(solid)
    sizes = np.bincount(labels.ravel()); sizes[0] = 0
    solid = ndimage.binary_fill_holes(labels == sizes.argmax())
    result = im.crop(box).convert('RGBA')
    result.putalpha(Image.fromarray((solid*255).astype('uint8')))
    result = result.crop(result.getbbox())
    result.save(ASSETS / f'capital-{name}.png', optimize=True)

# Distinct sequences on either side avoid a mirrored wallpaper effect.
for side, sequence in [('left',['14','13','1','3','16','11','12','2']), ('right',['11','16','2','12','14','1','13','3'])]:
    pieces=[]; y=28
    for name in sequence:
        img=Image.open(ASSETS/f'capital-{name}.png')
        width=152 if name not in ['2','3'] else 100
        height=round(img.height*width/img.width)
        pieces.append(f'<image href="capital-{name}.png" x="{(180-width)/2}" y="{y}" width="{width}" height="{height}"/>')
        y+=height+70
    # Inline raster data so browsers render reliably when SVG is a CSS image.
    import base64
    svg=''.join(pieces)
    for name in sequence:
        data=base64.b64encode((ASSETS/f'capital-{name}.png').read_bytes()).decode()
        svg=svg.replace(f'href="capital-{name}.png"', f'href="data:image/png;base64,{data}"')
    full_svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="180" height="{y}" viewBox="0 0 180 {y}">{svg}</svg>'
    (ASSETS/f'{side}.svg').write_text(full_svg,encoding='utf-8')
    def shrink(match):
        x, top, w, h = map(float, match.groups())
        nw, nh = w*.64, h*.64
        return f'x="{(180-nw)/2:g}" y="{top+(h-nh)/2:g}" width="{nw:g}" height="{nh:g}"'
    small_svg=re.sub(r'x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"',shrink,full_svg)
    (ASSETS/f'{side}-small.svg').write_text(small_svg,encoding='utf-8')

text=(HERE/'article.md').read_text(encoding='utf-8')
paragraphs=text.split('\n\n')[1:]
def paragraph(value):
    value=html.escape(value.strip())
    value=re.sub(r'\[([^]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',value)
    return '<p>'+value+'</p>'
body='\n'.join(paragraph(p) for p in paragraphs if p.strip())
template=(ROOT/'frontend-without-frontend-experience/index.html').read_text(encoding='utf-8')
old_title='Building a frontend without frontend experience'
template=template.replace(old_title,'On the avoidance of slop')
template=template.replace('frontend-without-frontend-experience/','on-the-avoidance-of-slop/')
template=template.replace('article-page--kiosk','article-page--egyptian')
template=template.replace('#F2EBD5','#F4EEE3')
template=template.replace('article.css?v=20260914','article.css?v=20260914-egyptian')
template=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="Building a personal website with AI, finding a visual identity, and making time for the details that keep generic output from creeping in.">',template)
template=template.replace('How I use AI tools to build, design and test the frontend of an application I built myself.','Found ornament, shared motifs and the details that make an AI-assisted website feel considered.')
template=re.sub(r'(<div class="col">).*?(\s*</div>\s*</article>)',lambda m:m[1]+'\n'+body+m[2],template,flags=re.S)
template=re.sub(r'<p class="pattern-credit">.*?</p>','<p class="pattern-credit">Ornament: <a href="https://www.oldbookillustrations.com/illustrations/egyptian-3/">Egyptian Capitals</a> &middot; Francis Bedford, lithographer &middot; Owen Jones, <i>The Grammar of Ornament</i>, 1868 (adapted).</p>',template)
# Theme must follow the shared article stylesheet.
template=re.sub(r'<link rel="stylesheet" href="article.css[^\n]+\n','',template)
template=template.replace('</head>','<link rel="stylesheet" href="article.css?v=20260914-small-egyptian">\n</head>')
dest=ROOT/'on-the-avoidance-of-slop'; dest.mkdir(exist_ok=True)
(dest/'index.html').write_text(template,encoding='utf-8')
print(f'Rendered {len(paragraphs)} paragraphs and {len(polygons)} extracted illustrations.')
