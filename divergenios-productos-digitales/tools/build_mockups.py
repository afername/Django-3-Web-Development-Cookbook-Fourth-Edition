# -*- coding: utf-8 -*-
"""
Genera mockups de tienda (imágenes promocionales) para los productos digitales.
Para cada producto crea, en su carpeta `mockups/`:
  - <slug>-tablet.png    : la portada en una tablet, fondo de marca
  - <slug>-fan.png       : varias páginas en abanico con sombra
  - <slug>-social.png    : pieza cuadrada 1080x1080 para redes/tienda
Uso:  python3 build_mockups.py
Requiere: pymupdf (render del PDF) y Pillow.
"""
import os

import fitz
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
LOGO = os.path.join(HERE, 'assets', 'divergenios-logo.png')
DV = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
DVB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

INK = (42, 42, 60)
WHITE = (255, 255, 255)


def font(bold, size):
    return ImageFont.truetype(DVB if bold else DV, size)


def render_page(pdf_path, index, dpi=170):
    doc = fitz.open(pdf_path)
    pix = doc[index].get_pixmap(dpi=dpi)
    img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    doc.close()
    return img


def round_mask(size, radius):
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return m


def round_corners(img, radius):
    img = img.convert('RGBA')
    img.putalpha(round_mask(img.size, radius))
    return img


def drop_shadow(card, blur=28, alpha=120, grow=10):
    """Devuelve una capa RGBA del tamaño de card+margen con la sombra de su silueta."""
    w, h = card.size
    pad = blur * 2 + grow
    layer = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    sil = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    a = card.split()[-1] if card.mode == 'RGBA' else Image.new('L', card.size, 255)
    blk = Image.new('RGBA', card.size, (0, 0, 0, alpha))
    sil.paste(blk, (pad, pad), a)
    return sil.filter(ImageFilter.GaussianBlur(blur)), pad


def paste_with_shadow(bg, card, cx, cy, blur=28, alpha=120, dy=18):
    sh, pad = drop_shadow(card, blur=blur, alpha=alpha)
    bg.alpha_composite(sh, (cx - card.size[0] // 2 - pad, cy - card.size[1] // 2 - pad + dy))
    bg.alpha_composite(card.convert('RGBA'), (cx - card.size[0] // 2, cy - card.size[1] // 2))


def lin_gradient(size, top, bottom):
    w, h = size
    base = Image.new('RGB', (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        base.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return base.resize((w, h)).convert('RGBA')


def scatter_doodles(draw, w, h, color, points=None):
    # círculos tenues deterministas (sin random)
    pts = points if points is not None else [
        (0.08, 0.2), (0.9, 0.15), (0.15, 0.8), (0.85, 0.78), (0.5, 0.07),
        (0.3, 0.5), (0.7, 0.4), (0.05, 0.55), (0.95, 0.5), (0.45, 0.9),
        (0.6, 0.85), (0.22, 0.3), (0.78, 0.62), (0.4, 0.25), (0.65, 0.18)]
    for i, (px, py) in enumerate(pts):
        r = 6 + (i * 7) % 16
        x, y = px * w, py * h
        a = 26 if i % 2 else 18
        draw.ellipse([x - r, y - r, x + r, y + r], outline=color + (a + 20,), width=3)


def fit_logo(h):
    lg = Image.open(LOGO).convert('RGBA')
    w = int(h * lg.width / lg.height)
    return lg.resize((w, h), Image.LANCZOS)


# ---------------- mockups ----------------
def mockup_tablet(cover, bg_color, accent, out):
    W, Hh = 1500, 1100
    bg = lin_gradient((W, Hh), bg_color, tuple(max(0, c - 30) for c in bg_color))
    d = ImageDraw.Draw(bg)
    scatter_doodles(d, W, Hh, WHITE)
    # marco de tablet
    cov = cover.copy()
    target_h = 820
    cw = int(cov.width * target_h / cov.height)
    cov = cov.resize((cw, target_h), Image.LANCZOS)
    bezel = 26
    body = Image.new('RGBA', (cw + 2 * bezel, target_h + 2 * bezel), (24, 24, 34, 255))
    body = round_corners(body, 46)
    screen = round_corners(cov, 14)
    body.alpha_composite(screen, (bezel, bezel))
    paste_with_shadow(bg, body, W // 2, Hh // 2 - 10, blur=34, alpha=130, dy=26)
    # logo + claim
    lg = fit_logo(120)
    bg.alpha_composite(lg, (60, 60))
    d.text((190, 78), 'divergenios.com', font=font(True, 38), fill=WHITE)
    d.text((190, 124), 'aprender es divertido', font=font(False, 26), fill=accent + (255,))
    badge = 'DESCARGABLE · IMPRIMIBLE PDF'
    bw = d.textlength(badge, font=font(True, 26))
    d.rounded_rectangle([W - bw - 110, 70, W - 50, 124], radius=27, fill=accent + (255,))
    d.text((W - bw - 80, 84), badge, font=font(True, 26), fill=INK + (255,))
    bg.convert('RGB').save(out)


def mockup_fan(pages, bg_color, out):
    W, Hh = 1500, 1100
    bg = lin_gradient((W, Hh), tuple(min(255, c + 235) // 1 for c in (240, 240, 245)),
                      (228, 230, 240))
    d = ImageDraw.Draw(bg)
    scatter_doodles(d, W, Hh, (120, 120, 160))
    target_h = 740
    angles = [12, -2, -14]
    offsets = [330, 0, -330]
    order = [2, 0, 1]  # pintar laterales primero, centro encima
    cards = []
    for p in pages[:3]:
        cw = int(p.width * target_h / p.height)
        card = round_corners(p.resize((cw, target_h), Image.LANCZOS), 12)
        # borde blanco
        bordered = Image.new('RGBA', (card.width + 12, card.height + 12), (255, 255, 255, 255))
        bordered = round_corners(bordered, 16)
        bordered.alpha_composite(card, (6, 6))
        cards.append(bordered)
    for i in order:
        rot = cards[i].rotate(angles[i], expand=True, resample=Image.BICUBIC)
        paste_with_shadow(bg, rot, W // 2 + offsets[i], Hh // 2, blur=26, alpha=95, dy=16)
    bg.convert('RGB').save(out)


def mockup_social(cover, title_lines, bullets, bg_color, accent, out):
    S = 1080
    bg = lin_gradient((S, S), bg_color, tuple(max(0, c - 28) for c in bg_color))
    d = ImageDraw.Draw(bg)
    # solo en zonas seguras (lejos del texto izquierdo y del CTA inferior)
    scatter_doodles(d, S, S, WHITE, points=[(0.52, 0.04), (0.62, 0.12), (0.95, 0.06),
                                            (0.04, 0.06), (0.97, 0.66), (0.9, 0.92)])
    # portada a la derecha, inclinada
    cov = cover.copy()
    th = 720
    cw = int(cov.width * th / cov.height)
    card = round_corners(cov.resize((cw, th), Image.LANCZOS), 14)
    rot = card.rotate(-6, expand=True, resample=Image.BICUBIC)
    paste_with_shadow(bg, rot, S - 250, S // 2 + 40, blur=30, alpha=130, dy=20)
    # logo arriba izq
    lg = fit_logo(96)
    bg.alpha_composite(lg, (60, 56))
    d.text((168, 74), 'divergenios', font=font(True, 40), fill=WHITE)
    # titulo
    y = 230
    for ln in title_lines:
        d.text((70, y), ln, font=font(True, 62), fill=WHITE)
        y += 70
    y += 18
    for b in bullets:
        d.ellipse([74, y + 8, 100, y + 34], fill=accent + (255,))
        d.line([80, y + 21, 86, y + 28], fill=WHITE, width=4)
        d.line([86, y + 28, 95, y + 14], fill=WHITE, width=4)
        d.text((120, y), b, font=font(False, 34), fill=WHITE)
        y += 58
    # CTA (píldora ajustada al ancho del texto)
    cta = 'Descárgalo en divergenios.com'
    cf = font(True, 30)
    cw2 = d.textlength(cta, font=cf)
    d.rounded_rectangle([70, S - 150, 70 + cw2 + 64, S - 86], radius=32, fill=accent + (255,))
    d.text((102, S - 138), cta, font=cf, fill=INK + (255,))
    bg.convert('RGB').save(out)


# ---------------- config por producto ----------------
PRODUCTS = [
    dict(slug='laboratorio-divergente', folder='01-laboratorio-divergente-en-casa',
         pdf='Laboratorio-Divergente-en-Casa.pdf',
         bg=(85, 18, 222), accent=(42, 179, 240),
         title=['Laboratorio', 'Divergente', 'en casa'],
         bullets=['20 experimentos STEAM', 'Materiales de casa · sin pantallas', '6-10 años · imprimible PDF'],
         fan_pages=[0, 4, 24]),
    dict(slug='retos-ingenieria', folder='02-retos-de-ingenieria',
         pdf='Retos-de-Ingenieria-Divergente.pdf',
         bg=(16, 69, 110), accent=(196, 95, 224),
         title=['Retos de', 'Ingeniería', 'Divergente'],
         bullets=['16 desafíos de construcción', 'Aprende el ciclo de diseño', '6-11 años · imprimible PDF'],
         fan_pages=[0, 2, 5]),
    dict(slug='calendario-adviento', folder='03-calendario-adviento-steam',
         pdf='Calendario-Adviento-STEAM.pdf',
         bg=(21, 84, 59), accent=(244, 180, 0),
         title=['Calendario de', 'Adviento', 'STEAM'],
         bullets=['24 mini-retos · 1 por día', 'Ciencia de Navidad sin pantallas', '6-10 años · imprimible PDF'],
         fan_pages=[0, 2, 3]),
    dict(slug='tu-primer-robot', folder='04-tu-primer-robot',
         pdf='Tu-Primer-Robot-Cuaderno.pdf',
         bg=(85, 18, 222), accent=(42, 179, 240),
         title=['Tu primer', 'robot'],
         bullets=['Robótica SIN pantallas', '13 lecciones + cuaderno', 'Vídeos + tarjetas recortables'],
         fan_pages=[0, 2, 9]),
]


def build_for(cfg):
    folder = os.path.join(ROOT, cfg['folder'])
    pdf = os.path.join(folder, cfg['pdf'])
    if not os.path.exists(pdf):
        print('!! falta', pdf)
        return
    outdir = os.path.join(folder, 'mockups')
    os.makedirs(outdir, exist_ok=True)
    cover = render_page(pdf, 0)
    pages = [render_page(pdf, i) for i in cfg['fan_pages']]
    mockup_tablet(cover, cfg['bg'], cfg['accent'], os.path.join(outdir, cfg['slug'] + '-tablet.png'))
    mockup_fan(pages, cfg['bg'], os.path.join(outdir, cfg['slug'] + '-fan.png'))
    mockup_social(cover, cfg['title'], cfg['bullets'], cfg['bg'], cfg['accent'],
                  os.path.join(outdir, cfg['slug'] + '-social.png'))
    print('OK mockups ->', os.path.relpath(outdir, ROOT))


def main():
    for cfg in PRODUCTS:
        build_for(cfg)


if __name__ == '__main__':
    main()
