# -*- coding: utf-8 -*-
"""
Maqueta 'Calendario de Adviento STEAM' a PDF profesional con marca Divergenios.
Formato: portada festiva, cómo funciona, póster de 24 puertitas (clicable) y
24 tarjetas recortables (2 por página). Reutiliza brand.py y helpers de build_lab_pdf.py.
Genera:
  - Calendario-Adviento-STEAM.pdf   (producto completo)
  - Lead-Magnet-3-Retos-Adviento.pdf (captación: días 1, 13 y 24)
Uso:  python3 build_advent_pdf.py
"""
import math
import os
import re
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand as B
import build_lab_pdf as L

W, H, MARGIN = L.W, L.H, L.MARGIN
FONT, BOLD = L.FONT, L.BOLD
para, para_h, section_label, footer, clean = L.para, L.para_h, L.section_label, L.footer, L.clean

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '03-calendario-adviento-steam', 'PRODUCTO.md')
OUTDIR = os.path.join(HERE, '..', '03-calendario-adviento-steam')

GREEN = HexColor('#15543B')
GREEN_D = HexColor('#0E3B29')
RED = HexColor('#D1495B')
GOLD = HexColor('#F4B400')

# día -> área (del índice del producto) -> color
AREA = {}
for col, days in [
    (B.CIENCIA, [2, 4, 5, 7, 9, 14, 24]),
    (B.FISICA, [11, 15, 18, 20, 22, 23]),
    (B.INGEN, [6, 12]),
    (B.BLUE, [3, 8, 19]),
    (B.MATES, [1, 10, 16, 21]),
    (B.ARTE, [13, 17]),
]:
    for dd in days:
        AREA[dd] = col


def star(c, cx, cy, r, color, fill=True):
    c.saveState()
    if fill:
        c.setFillColor(color)
    c.setStrokeColor(color)
    p = c.beginPath()
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rad = r if i % 2 == 0 else r * 0.45
        x, y = cx + math.cos(ang) * rad, cy + math.sin(ang) * rad
        p.moveTo(x, y) if i == 0 else p.lineTo(x, y)
    p.close()
    c.drawPath(p, fill=1 if fill else 0, stroke=0 if fill else 1)
    c.restoreState()


def snow(c, color=white, n=22):
    pts = [(0.06, 0.9), (0.9, 0.85), (0.2, 0.7), (0.8, 0.6), (0.5, 0.95),
           (0.12, 0.5), (0.95, 0.45), (0.35, 0.83), (0.7, 0.92), (0.04, 0.3),
           (0.96, 0.7), (0.45, 0.6), (0.6, 0.78), (0.28, 0.45), (0.85, 0.3)]
    c.saveState()
    for i, (px, py) in enumerate(pts):
        r = 2 + (i * 3) % 5
        c.setFillColor(color)
        c.setFillAlpha(0.5 if i % 2 else 0.8)
        c.circle(W * px, H * py, r, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.restoreState()


# ============================================================
# PARSER
# ============================================================
def parse_days(path):
    raw = open(path, encoding='utf-8').read()
    days, cur = [], None
    for line in raw.splitlines():
        if line.startswith('# 🗂️') or 'Índice por área' in line:
            break
        mr = re.match(r'^###\s+(\d+)\.\s+(.*)$', line)
        if mr:
            if cur:
                days.append(cur)
            cur = {'n': int(mr.group(1)), 'title': clean(mr.group(2)), 'meta': {}}
            continue
        if cur is None:
            continue
        if line.startswith('**Día:**'):
            if '🟢' in line:
                cur['meta']['dif'] = 'Fácil'
            elif '🟡' in line:
                cur['meta']['dif'] = 'Media'
            elif '🔴' in line:
                cur['meta']['dif'] = 'Con adulto'
            mt = re.search(r'\*\*Tiempo:\*\*\s*([^·]+)', line)
            if mt:
                cur['meta']['tiempo'] = clean(mt.group(1))
            continue
        for key, marker in (('necesitas', '**Necesitas:**'), ('hazlo', '**Hazlo:**'),
                            ('chispa', '**La chispa:**'), ('toque', '**Toque divergenio:**')):
            if marker in line:
                cur[key] = clean(line.split(marker, 1)[1])
                break
    if cur:
        days.append(cur)
    return days


# ============================================================
# PÁGINAS
# ============================================================
def page_cover(c):
    c.setFillColor(GREEN)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GREEN_D)
    c.rect(0, H * 0.62, W, H * 0.38, fill=1, stroke=0)
    snow(c)
    for (px, py, r) in [(0.12, 0.84, 12), (0.88, 0.8, 16), (0.85, 0.2, 10), (0.15, 0.25, 9)]:
        star(c, W * px, H * py, r, GOLD)
    B.draw_logo_image(c, W / 2, H * 0.75, 148)
    c.setFillColor(white)
    c.setFont(BOLD, 44)
    c.drawCentredString(W / 2, H * 0.5, 'Calendario de')
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, H * 0.5 - 48, 'Adviento STEAM')
    c.setFillColor(white)
    c.roundRect(W / 2 - 215, H * 0.33, 430, 34, 17, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont(BOLD, 13.5)
    c.drawCentredString(W / 2, H * 0.33 + 11, '24 mini-retos de ciencia, día a día · 6 a 10 años')
    para(c, 'Cada día, una puertita con un experimento de 5-15 minutos. Con cosas de casa y sin pantallas.',
         W / 2 - 210, H * 0.28, 420, FONT, 12, 16, white, align='center')
    c.setFont(BOLD, 22)
    c.setFillColor(white)
    wln = pdfmetrics.stringWidth('diver', BOLD, 22)
    tot = wln + pdfmetrics.stringWidth('genios', BOLD, 22)
    c.drawString(W / 2 - tot / 2, H * 0.13, 'diver')
    c.setFillColor(GOLD)
    c.drawString(W / 2 - tot / 2 + wln, H * 0.13, 'genios')
    c.setFont(FONT, 11)
    c.setFillColor(white)
    c.drawCentredString(W / 2, H * 0.11, 'aprender es divertido · divergenios.com')
    c.showPage()


def page_howto(c):
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.rect(0, H - 150, W, 150, fill=1, stroke=0)
    snow(c, color=white)
    B.draw_logo_image(c, MARGIN + 52, H - 78, 92)
    c.setFillColor(white)
    c.setFont(BOLD, 26)
    c.drawString(MARGIN + 110, H - 66, 'Cómo funciona tu')
    c.drawString(MARGIN + 110, H - 96, 'calendario')
    y = H - 184
    intro = ('Llega diciembre y, además de chocolatinas, te proponemos algo más dulce: abrir '
             'cada día una "puertita" con un mini-reto STEAM de 5 a 15 minutos. Cada reto es '
             'independiente; da igual si empiezas el día 1 o te enganchas el 9. Lo importante '
             'no es que "salga perfecto", sino observar, probar y entender por qué pasa lo que pasa.')
    y = para(c, intro, MARGIN, y, W - 2 * MARGIN, FONT, 12, 17, B.INK) - 14
    items = [
        ('Un reto por día', 'Del 1 al 24 de diciembre. Abre la puertita y… ¡a explorar!', B.CIENCIA),
        ('En casa o en clase', 'En la mesa de la cocina, o como rutina de aula por parejas.', B.BLUE),
        ('Materiales de casa', 'Papel, sal, hielo, vasos, un imán de nevera, un globo…', B.MATES),
        ('Seguridad primero', 'Un adulto cerca. Tijeras, velas y agua caliente las maneja el adulto.', RED),
    ]
    bw = (W - 2 * MARGIN - 30) / 2
    for i, (tit, desc, col) in enumerate(items):
        bx = MARGIN + (i % 2) * (bw + 30)
        by = y - (i // 2) * 78
        c.setFillColor(B.tint(col, 0.9))
        c.roundRect(bx, by - 64, bw, 64, 10, fill=1, stroke=0)
        c.setFillColor(col)
        c.circle(bx + 22, by - 22, 12, fill=1, stroke=0)
        c.setFillColor(white)
        star(c, bx + 22, by - 22, 7, white)
        c.setFillColor(col)
        c.setFont(BOLD, 12)
        c.drawString(bx + 44, by - 20, tit)
        para(c, desc, bx + 44, by - 36, bw - 56, FONT, 9.5, 12, B.INK)
    y -= 174
    # leyenda
    c.setFillColor(B.INK)
    c.roundRect(MARGIN, y - 40, W - 2 * MARGIN, 40, 10, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont(BOLD, 11)
    c.drawString(MARGIN + 16, y - 24, 'Dificultad:')
    leg = [('Fácil', B.CIENCIA), ('Media', B.FISICA), ('Necesita más ayuda del adulto', RED)]
    lx = MARGIN + 110
    c.setFont(FONT, 10)
    for label, col in leg:
        c.setFillColor(col)
        c.circle(lx + 5, y - 21, 5, fill=1, stroke=0)
        c.setFillColor(white)
        c.drawString(lx + 16, y - 24, label)
        lx += pdfmetrics.stringWidth(label, FONT, 10) + 40
    footer(c, 2)
    c.showPage()


def page_poster(c, days, dests):
    c.setFillColor(GREEN)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    snow(c, color=white)
    c.setFillColor(white)
    c.setFont(BOLD, 30)
    c.drawCentredString(W / 2, H - 70, 'Tu calendario de adviento')
    c.setFillColor(GOLD)
    c.setFont(FONT, 13)
    c.drawCentredString(W / 2, H - 92, 'Toca una puertita para ir a su reto · táchala al completarla')
    cols, rows = 4, 6
    gx, gy = 18, 16
    gridw = W - 2 * MARGIN
    cw = (gridw - (cols - 1) * gx) / cols
    ch = 92
    top = H - 120
    by_day = {e['n']: e for e in days}
    for idx in range(24):
        n = idx + 1
        r, cc = idx // cols, idx % cols
        x = MARGIN + cc * (cw + gx)
        y = top - r * (ch + gy)
        col = AREA.get(n, B.MATES)
        c.setFillColor(white)
        c.roundRect(x, y - ch, cw, ch, 12, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(x, y - 26, cw, 26, 12, fill=1, stroke=0)
        c.rect(x, y - 26, cw, 13, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(BOLD, 13)
        c.drawString(x + 8, y - 19, 'DÍA %d' % n)
        star(c, x + cw - 14, y - 13, 6, white)
        c.setFillColor(col)
        c.setFont(BOLD, 30)
        c.drawCentredString(x + cw / 2, y - 64, str(n))
        e = by_day.get(n)
        if e:
            t = e['title']
            c.setFillColor(B.INK)
            c.setFont(FONT, 7.2)
            while pdfmetrics.stringWidth(t, FONT, 7.2) > cw - 12 and len(t) > 3:
                t = t[:-2]
            if t != e['title']:
                t = t.rstrip() + '…'
            c.drawCentredString(x + cw / 2, y - ch + 8, t)
        c.linkAbsolute('', dests[n], (x, y - ch, x + cw, y), thickness=0)
    footer(c, 3)
    c.showPage()


def draw_card(c, e, x, y, w, h):
    """Dibuja una tarjeta de reto en el rectángulo (x, y-h, w, h)."""
    col = AREA.get(e['n'], B.MATES)
    pad = 14
    # fondo
    c.setFillColor(B.tint(col, 0.95))
    c.roundRect(x, y - h, w, h, 12, fill=1, stroke=0)
    c.setStrokeColor(B.tint(col, 0.5))
    c.setLineWidth(1)
    c.roundRect(x, y - h, w, h, 12, fill=0, stroke=1)
    # cabecera
    hd = 40
    c.setFillColor(col)
    p = c.beginPath()
    rr = 12
    c.roundRect(x, y - hd, w, hd, 12, fill=1, stroke=0)
    c.rect(x, y - hd, w, hd / 2, fill=1, stroke=0)
    # badge día
    c.setFillColor(white)
    c.circle(x + 26, y - 20, 15, fill=1, stroke=0)
    c.setFillColor(col)
    c.setFont(BOLD, 16)
    c.drawCentredString(x + 26, y - 25, str(e['n']))
    c.setFillColor(white)
    c.setFont(BOLD, 8)
    c.drawString(x + 46, y - 15, 'DÍA %d' % e['n'])
    tt = e['title']
    ts = 13
    while pdfmetrics.stringWidth(tt, BOLD, ts) > w - 56 and ts > 9:
        ts -= 0.5
    c.setFont(BOLD, ts)
    c.drawString(x + 46, y - 30, tt)

    inner_w = w - 2 * pad
    cy = y - hd - 12
    # chips
    cx = x + pad
    for lab in (e['meta'].get('tiempo'), e['meta'].get('dif')):
        if lab:
            txt = lab.upper()
            wc = pdfmetrics.stringWidth(txt, BOLD, 7) + 12
            c.setFillColor(B.tint(col, 0.75))
            c.roundRect(cx, cy - 11, wc, 13, 6.5, fill=1, stroke=0)
            c.setFillColor(B.tint(col, -0.2) if False else col)
            c.setFont(BOLD, 7)
            c.drawString(cx + 6, cy - 7.5, txt)
            cx += wc + 5
    cy -= 18

    # auto-fit
    def total_h(bs):
        lead = bs + 3.2
        hh = 0
        for key in ('necesitas', 'hazlo', 'chispa', 'toque'):
            if e.get(key):
                hh += 11 + para_h(e[key], inner_w, FONT, bs, lead) + 5
        return hh

    avail = (cy) - (y - h) - pad
    bs = 10
    for cand in (10, 9.5, 9, 8.5, 8, 7.5):
        if total_h(cand) <= avail:
            bs = cand
            break
        bs = cand
    lead = bs + 3.2
    labels = [('necesitas', 'NECESITAS', B.CIENCIA), ('hazlo', 'HAZLO', col),
              ('chispa', 'LA CHISPA', B.FISICA), ('toque', 'TOQUE DIVERGENIO', B.ARTE)]
    for key, lab, lcol in labels:
        if not e.get(key):
            continue
        c.setFillColor(lcol)
        c.setFont(BOLD, 7.5)
        c.drawString(x + pad, cy, lab)
        cy -= 11
        cy = para(c, e[key], x + pad, cy, inner_w, FONT, bs, lead, B.INK) - 5


def page_cards(c, batch, page_no, dests, dest_done):
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    top = H - 40
    bottom = 52
    gapmid = 16
    card_h = (top - bottom - gapmid) / 2
    w = W - 2 * MARGIN
    for i, e in enumerate(batch):
        if e['n'] not in dest_done:
            c.bookmarkPage(dests[e['n']])
            dest_done.add(e['n'])
        cy = top - i * (card_h + gapmid)
        draw_card(c, e, MARGIN, cy, w, card_h)
    # línea de recorte entre tarjetas
    if len(batch) == 2:
        midy = top - card_h - gapmid / 2
        c.setStrokeColor(B.GREY)
        c.setLineWidth(0.7)
        c.setDash(4, 4)
        c.line(MARGIN, midy, W - MARGIN, midy)
        c.setDash()
        c.setFillColor(B.GREY)
        c.setFont(FONT, 7)
        c.drawCentredString(W / 2, midy - 3, '✂  recorta por aquí')
    footer(c, page_no)
    c.showPage()


def page_diploma(c, page_no):
    c.setFillColor(B.tint(GREEN, 0.9))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    snow(c, color=GREEN)
    m = 60
    c.setStrokeColor(GREEN)
    c.setLineWidth(6)
    c.roundRect(m, m, W - 2 * m, H - 2 * m, 18, fill=0, stroke=1)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.roundRect(m + 10, m + 10, W - 2 * m - 20, H - 2 * m - 20, 14, fill=0, stroke=1)
    B.draw_logo_image(c, W / 2, H - 150, 118)
    for (px, py) in [(0.2, 0.6), (0.8, 0.6), (0.5, 0.78)]:
        star(c, W * px, H * py, 9, GOLD)
    c.setFillColor(GREEN)
    c.setFont(BOLD, 30)
    c.drawCentredString(W / 2, H - 232, '¡CALENDARIO COMPLETADO!')
    c.setFont(BOLD, 22)
    c.setFillColor(RED)
    c.drawCentredString(W / 2, H - 268, 'Diploma de Científico/a Divergenio')
    c.setFillColor(B.INK)
    c.setFont(FONT, 14)
    c.drawCentredString(W / 2, H - 318, 'Otorgado con orgullo a:')
    c.setStrokeColor(GREEN)
    c.setLineWidth(1.2)
    c.line(W / 2 - 180, H - 356, W / 2 + 180, H - 356)
    para(c, 'por abrir las 24 puertitas, preguntarse "¿y si…?" y descubrir que la Navidad '
         'también se vive jugando con la ciencia.',
         W / 2 - 200, H - 388, 400, FONT, 13, 18, B.INK, align='center')
    c.setFont(BOLD, 22)
    c.setFillColor(GREEN)
    c.drawCentredString(W / 2, H - 436, '¡APRENDER ES DIVERTIDO!')
    c.setFont(FONT, 13)
    c.setFillColor(B.INK)
    c.drawCentredString(W / 2, H - 476, 'Retos completados: ______ / 24')
    c.drawString(W / 2 - 175, H - 520, 'Mi reto favorito: ')
    c.line(W / 2 - 80, H - 522, W / 2 + 175, H - 522)
    B.draw_logo(c, W / 2 - 70, m + 24, size=18)
    footer(c, page_no)
    c.showPage()


def page_back(c, page_no):
    c.setFillColor(GREEN)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    snow(c, color=white)
    B.draw_logo_image(c, W / 2, H * 0.76, 128)
    c.setFillColor(white)
    c.setFont(BOLD, 30)
    c.drawCentredString(W / 2, H * 0.58, 'La ciencia no se acaba')
    c.drawCentredString(W / 2, H * 0.58 - 38, 'en diciembre')
    para(c, 'Si te ha gustado esta cuenta atrás, en divergenios.com te esperan experimentos, '
         'retos de ingeniería y robótica sin pantallas para seguir explorando todo el año.',
         W / 2 - 220, H * 0.44, 440, FONT, 13, 19, white, align='center')
    ctas = ['Laboratorio Divergenio · 20 experimentos', 'Retos de Ingeniería · 16 desafíos',
            'Club Divergenio · novedades cada mes']
    yy = H * 0.33
    for t in ctas:
        wc = pdfmetrics.stringWidth(t, BOLD, 13) + 40
        c.setFillColor(GOLD)
        c.roundRect(W / 2 - wc / 2, yy, wc, 30, 15, fill=1, stroke=0)
        c.setFillColor(GREEN)
        c.setFont(BOLD, 13)
        c.drawCentredString(W / 2, yy + 9, t)
        yy -= 42
    c.setFont(BOLD, 20)
    c.setFillColor(white)
    c.drawCentredString(W / 2, H * 0.16, 'divergenios.com')
    c.setFont(FONT, 12)
    c.drawCentredString(W / 2, H * 0.13, 'aprender es divertido')
    c.setFont(FONT, 8)
    c.setFillColor(B.tint(GREEN, 0.5))
    c.drawCentredString(W / 2, 40, '© divergenios.com · Uso personal y de aula. Prohibida su reventa o redistribución.')
    c.showPage()


def build(days, outfile, subset=None, lead_magnet=False):
    c = canvas.Canvas(outfile, pagesize=A4)
    c.setTitle('Calendario de Adviento STEAM' + (' — Muestra gratis' if lead_magnet else ''))
    c.setAuthor('divergenios.com')
    c.setSubject('24 mini-retos STEAM para diciembre · 6-10 años')
    dests = {e['n']: 'dia%d' % e['n'] for e in days}
    items = days if subset is None else [e for e in days if e['n'] in subset]
    page_cover(c)
    page_howto(c)
    if not lead_magnet:
        page_poster(c, days, dests)
        pno = 4
    else:
        pno = 3
    dest_done = set()
    for i in range(0, len(items), 2):
        page_cards(c, items[i:i + 2], pno, dests, dest_done)
        pno += 1
    if not lead_magnet:
        page_diploma(c, pno)
        pno += 1
    page_back(c, pno)
    c.save()
    return pno


def main():
    days = parse_days(SRC)
    assert len(days) == 24, 'Se esperaban 24 días, hay %d' % len(days)
    full = os.path.join(OUTDIR, 'Calendario-Adviento-STEAM.pdf')
    lead = os.path.join(OUTDIR, 'Lead-Magnet-3-Retos-Adviento.pdf')
    n1 = build(days, full)
    n2 = build(days, lead, subset={1, 13, 24}, lead_magnet=True)
    print('OK  %-42s  %2d páginas' % (os.path.basename(full), n1))
    print('OK  %-42s  %2d páginas' % (os.path.basename(lead), n2))


if __name__ == '__main__':
    main()
