# -*- coding: utf-8 -*-
"""
Maqueta el cuaderno imprimible de 'Tu primer robot' (acompaña a los vídeos).
Reutiliza brand.py y helpers de build_lab_pdf.py.
Genera:
  - Tu-Primer-Robot-Cuaderno.pdf        (cuaderno completo)
  - Lead-Magnet-Tarjetas-de-Flechas.pdf (captación: tarjetas + mini-cuadrícula)
Uso:  python3 build_robot_pdf.py
"""
import math
import os
import re
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand as B
import build_lab_pdf as L

W, H, MARGIN = L.W, L.H, L.MARGIN
FONT, BOLD = L.FONT, L.BOLD
para, para_h, section_label, footer, clean = L.para, L.para_h, L.section_label, L.footer, L.clean

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '04-tu-primer-robot', 'PRODUCTO.md')
OUTDIR = os.path.join(HERE, '..', '04-tu-primer-robot')

MOD_COLORS = {
    'Fundamentos': B.BLUE,
    'Programar movimientos': B.MATES,
    'Ideas potentes': B.INGEN,
    'Proyecto final': B.CIENCIA,
}


def parse_lessons(path):
    raw = open(path, encoding='utf-8').read()
    lessons, cur, module = [], None, None
    for line in raw.splitlines():
        ms = re.match(r'^##\s+Módulo\s*\d*:?\s*(.*)$', line)
        if ms:
            module = clean(ms.group(1))
            continue
        mr = re.match(r'^###\s+Lección\s+(\d+)\.\s+(.*)$', line)
        if mr:
            if cur:
                lessons.append(cur)
            cur = {'n': int(mr.group(1)), 'title': clean(mr.group(2)), 'module': module, 'meta': {}}
            continue
        if cur is None:
            continue
        if line.startswith('**Módulo:**'):
            if '🟢' in line:
                cur['meta']['dif'] = 'Fácil'
            elif '🟡' in line:
                cur['meta']['dif'] = 'Reto'
            elif '🔴' in line:
                cur['meta']['dif'] = 'Superdesafío'
            mt = re.search(r'\*\*Tiempo:\*\*\s*([^·]+)', line)
            if mt:
                cur['meta']['tiempo'] = clean(mt.group(1))
            continue
        for key, marker in (('video', '**En el vídeo:**'), ('necesitas', '**Necesitas:**'),
                            ('actividad', '**Actividad sin pantallas:**'), ('idea', '**La idea:**'),
                            ('reto', '**Reto divergenio:**')):
            if marker in line:
                cur[key] = clean(line.split(marker, 1)[1])
                break
    if cur:
        lessons.append(cur)
    return lessons


def modcolor(m):
    return MOD_COLORS.get(m or '', B.BLUE)


# ---------- iconos de flecha ----------
def arrow_forward(c, cx, cy, s, col):
    c.setFillColor(col)
    c.setStrokeColor(col)
    c.setLineWidth(s * 0.22)
    c.setLineCap(1)
    c.line(cx, cy - s, cx, cy + s * 0.5)
    p = c.beginPath()
    p.moveTo(cx - s * 0.5, cy + s * 0.3)
    p.lineTo(cx + s * 0.5, cy + s * 0.3)
    p.lineTo(cx, cy + s)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def arrow_turn(c, cx, cy, s, col, left=True):
    c.saveState()
    c.setStrokeColor(col)
    c.setLineWidth(s * 0.22)
    c.setLineCap(1)
    sgn = -1 if left else 1
    # tramo vertical + giro
    c.line(cx - sgn * s * 0.45, cy - s * 0.6, cx - sgn * s * 0.45, cy + s * 0.1)
    c.bezier(cx - sgn * s * 0.45, cy + s * 0.1, cx - sgn * s * 0.45, cy + s * 0.55,
             cx, cy + s * 0.55, cx + sgn * s * 0.15, cy + s * 0.55)
    c.setFillColor(col)
    p = c.beginPath()
    p.moveTo(cx + sgn * s * 0.15, cy + s * 0.85)
    p.lineTo(cx + sgn * s * 0.15, cy + s * 0.25)
    p.lineTo(cx + sgn * s * 0.6, cy + s * 0.55)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


# ============================================================
# PÁGINAS
# ============================================================
def page_cover(c):
    c.setFillColor(B.PURPLE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(B.PURPLE_D)
    c.rect(0, H * 0.62, W, H * 0.38, fill=1, stroke=0)
    B.draw_doodles(c, W, H, color=white)
    B.draw_logo_image(c, W / 2, H * 0.75, 150)
    c.setFillColor(white)
    c.setFont(BOLD, 50)
    c.drawCentredString(W / 2, H * 0.5, 'Tu primer robot')
    c.setFont(BOLD, 20)
    c.setFillColor(B.BLUE)
    c.drawCentredString(W / 2, H * 0.5 - 36, 'Cuaderno de actividades')
    c.setFillColor(white)
    c.roundRect(W / 2 - 220, H * 0.33, 440, 34, 17, fill=1, stroke=0)
    c.setFillColor(B.PURPLE)
    c.setFont(BOLD, 13)
    c.drawCentredString(W / 2, H * 0.33 + 11, 'Robótica y programación SIN pantallas · 6 a 10 años')
    para(c, 'Acompaña a los 13 vídeos del mini-curso. Recorta las tarjetas, dibuja tu cuadrícula y… ¡a programar!',
         W / 2 - 210, H * 0.28, 420, FONT, 12, 16, white, align='center')
    c.setFont(BOLD, 22)
    c.setFillColor(white)
    wln = pdfmetrics.stringWidth('diver', BOLD, 22)
    tot = wln + pdfmetrics.stringWidth('genios', BOLD, 22)
    c.drawString(W / 2 - tot / 2, H * 0.13, 'diver')
    c.setFillColor(B.BLUE)
    c.drawString(W / 2 - tot / 2 + wln, H * 0.13, 'genios')
    c.setFont(FONT, 11)
    c.setFillColor(white)
    c.drawCentredString(W / 2, H * 0.11, 'aprender es divertido · divergenios.com')
    c.showPage()


def page_howto(c):
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(B.PURPLE)
    c.rect(0, H - 150, W, 150, fill=1, stroke=0)
    B.draw_logo_image(c, MARGIN + 52, H - 78, 92)
    c.setFillColor(white)
    c.setFont(BOLD, 26)
    c.drawString(MARGIN + 110, H - 66, 'Programar es pensar')
    c.drawString(MARGIN + 110, H - 96, 'con orden (¡sin pantallas!)')
    y = H - 184
    intro = ('Para crear un robot no necesitas cables ni pantallas: necesitas pensar con orden '
             'y dar instrucciones clarísimas. En este cuaderno vas a "programar" robots con '
             'juegos, tarjetas de flechas y tu propio cuerpo. Cada lección tiene un vídeo corto '
             'y una actividad para hacer con las manos.')
    y = para(c, intro, MARGIN, y, W - 2 * MARGIN, FONT, 12, 17, B.INK) - 16
    c.setFont(BOLD, 15)
    c.setFillColor(B.PURPLE)
    c.drawString(MARGIN, y, 'Materiales para todo el curso')
    y -= 22
    mats = [('Tarjetas de flechas', 'Recórtalas de la página de tarjetas.', B.BLUE),
            ('Cuadrícula en el suelo', 'Con tiza, cinta de pintor o cuerda.', B.MATES),
            ('Fichas y tapones', 'Para el robot, las metas y los obstáculos.', B.INGEN),
            ('Un adulto ayudante', 'Para jugar, recortar y hacer de robot.', B.CIENCIA)]
    bw = (W - 2 * MARGIN - 30) / 2
    for i, (tit, desc, col) in enumerate(mats):
        bx = MARGIN + (i % 2) * (bw + 30)
        by = y - (i // 2) * 74
        c.setFillColor(B.tint(col, 0.9))
        c.roundRect(bx, by - 60, bw, 60, 10, fill=1, stroke=0)
        c.setFillColor(col)
        c.circle(bx + 22, by - 22, 11, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(BOLD, 12)
        c.drawCentredString(bx + 22, by - 26, str(i + 1))
        c.setFillColor(col)
        c.setFont(BOLD, 12)
        c.drawString(bx + 42, by - 20, tit)
        para(c, desc, bx + 42, by - 36, bw - 54, FONT, 9.5, 12, B.INK)
    y -= 168
    c.setFillColor(B.INK)
    c.roundRect(MARGIN, y - 40, W - 2 * MARGIN, 40, 10, fill=1, stroke=0)
    c.setFillColor(B.BLUE)
    c.setFont(BOLD, 11)
    c.drawString(MARGIN + 16, y - 24, 'Seguridad:')
    c.setFillColor(white)
    c.setFont(FONT, 10.5)
    c.drawString(MARGIN + 92, y - 24, 'Despeja el suelo, camina (no corras) y recorta con tijeras de punta redonda y un adulto cerca.')
    footer(c, 2)
    c.showPage()


def draw_lesson_card(c, e, x, y, w, h):
    col = modcolor(e['module'])
    pad = 14
    c.setFillColor(B.tint(col, 0.95))
    c.roundRect(x, y - h, w, h, 12, fill=1, stroke=0)
    c.setStrokeColor(B.tint(col, 0.55))
    c.setLineWidth(1)
    c.roundRect(x, y - h, w, h, 12, fill=0, stroke=1)
    hd = 40
    c.setFillColor(col)
    c.roundRect(x, y - hd, w, hd, 12, fill=1, stroke=0)
    c.rect(x, y - hd, w, hd / 2, fill=1, stroke=0)
    c.setFillColor(white)
    c.circle(x + 26, y - 20, 15, fill=1, stroke=0)
    c.setFillColor(col)
    c.setFont(BOLD, 15)
    c.drawCentredString(x + 26, y - 25, str(e['n']))
    c.setFillColor(white)
    c.setFont(BOLD, 8)
    c.drawString(x + 46, y - 15, ('LECCIÓN %d · %s' % (e['n'], (e['module'] or '').upper()))[:46])
    tt = e['title']
    ts = 13
    while pdfmetrics.stringWidth(tt, BOLD, ts) > w - 56 and ts > 9:
        ts -= 0.5
    c.setFont(BOLD, ts)
    c.drawString(x + 46, y - 30, tt)

    inner = w - 2 * pad
    cy = y - hd - 12
    cx = x + pad
    for lab in (e['meta'].get('tiempo'), e['meta'].get('dif')):
        if lab:
            t = lab.upper()
            wc = pdfmetrics.stringWidth(t, BOLD, 7) + 12
            c.setFillColor(B.tint(col, 0.75))
            c.roundRect(cx, cy - 11, wc, 13, 6.5, fill=1, stroke=0)
            c.setFillColor(col)
            c.setFont(BOLD, 7)
            c.drawString(cx + 6, cy - 7.5, t)
            cx += wc + 5
    cy -= 18

    labels = [('video', 'EN EL VÍDEO', B.MATES), ('necesitas', 'NECESITAS', B.CIENCIA),
              ('actividad', 'ACTIVIDAD SIN PANTALLAS', col), ('idea', 'LA IDEA', B.INGEN),
              ('reto', 'RETO DIVERGENIO', B.ARTE)]

    def total(bs):
        lead = bs + 3
        hh = 0
        for key, _, _ in labels:
            if e.get(key):
                hh += 11 + para_h(e[key], inner, FONT, bs, lead) + 4
        return hh

    avail = cy - (y - h) - pad
    bs = 9.5
    for cand in (9.5, 9, 8.5, 8, 7.5, 7):
        if total(cand) <= avail:
            bs = cand
            break
        bs = cand
    lead = bs + 3
    for key, lab, lcol in labels:
        if not e.get(key):
            continue
        c.setFillColor(lcol)
        c.setFont(BOLD, 7.5)
        c.drawString(x + pad, cy, lab)
        cy -= 11
        cy = para(c, e[key], x + pad, cy, inner, FONT, bs, lead, B.INK) - 4


def page_lessons(c, batch, page_no, dests, done):
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    top = H - 40
    bottom = 52
    gapmid = 16
    ch = (top - bottom - gapmid) / 2
    w = W - 2 * MARGIN
    for i, e in enumerate(batch):
        if e['n'] not in done:
            c.bookmarkPage(dests[e['n']])
            done.add(e['n'])
        draw_lesson_card(c, e, MARGIN, top - i * (ch + gapmid), w, ch)
    if len(batch) == 2:
        midy = top - ch - gapmid / 2
        c.setStrokeColor(B.GREY)
        c.setLineWidth(0.7)
        c.setDash(4, 4)
        c.line(MARGIN, midy, W - MARGIN, midy)
        c.setDash()
    footer(c, page_no)
    c.showPage()


def page_arrow_cards(c, page_no):
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(B.MATES)
    c.rect(0, H - 86, W, 86, fill=1, stroke=0)
    B.draw_logo_image(c, W - MARGIN - 30, H - 43, 70)
    c.setFillColor(white)
    c.setFont(BOLD, 24)
    c.drawString(MARGIN, H - 50, 'Tarjetas de flechas')
    c.setFont(FONT, 11)
    c.drawString(MARGIN, H - 72, 'Recórtalas y úsalas para programar a tu robot. Pégalas sobre cartulina para que duren.')
    # cuadrícula de tarjetas
    cols, rows = 3, 4
    gx, gy = 16, 16
    cw = (W - 2 * MARGIN - (cols - 1) * gx) / cols
    chh = 150
    top = H - 110
    cards = [('AVANZAR', 'forward', B.BLUE), ('GIRA IZQUIERDA', 'left', B.MATES),
             ('GIRA DERECHA', 'right', B.INGEN), ('AVANZAR', 'forward', B.BLUE),
             ('GIRA IZQUIERDA', 'left', B.MATES), ('GIRA DERECHA', 'right', B.INGEN),
             ('REPETIR x ___', 'loop', B.ARTE), ('FUNCIÓN: ______', 'func', B.CIENCIA),
             ('AVANZAR', 'forward', B.BLUE), ('GIRA IZQUIERDA', 'left', B.MATES),
             ('GIRA DERECHA', 'right', B.INGEN), ('AVANZAR', 'forward', B.BLUE)]
    for idx, (lab, kind, col) in enumerate(cards):
        r, cc = idx // cols, idx % cols
        x = MARGIN + cc * (cw + gx)
        y = top - r * (chh + gy)
        c.setStrokeColor(B.tint(col, 0.4))
        c.setLineWidth(1)
        c.setDash(3, 3)
        c.roundRect(x, y - chh, cw, chh, 10, fill=0, stroke=1)
        c.setDash()
        c.setFillColor(B.tint(col, 0.95))
        c.roundRect(x + 3, y - chh + 3, cw - 6, chh - 6, 8, fill=1, stroke=0)
        midx, midy = x + cw / 2, y - chh / 2 + 8
        if kind == 'forward':
            arrow_forward(c, midx, midy, 30, col)
        elif kind == 'left':
            arrow_turn(c, midx, midy, 30, col, left=True)
        elif kind == 'right':
            arrow_turn(c, midx, midy, 30, col, left=False)
        elif kind == 'loop':
            c.setStrokeColor(col)
            c.setLineWidth(5)
            c.arc(midx - 22, midy - 22, midx + 22, midy + 22, startAng=70, extent=300)
            arrow_forward(c, midx + 16, midy + 14, 12, col)
        elif kind == 'func':
            c.setFillColor(col)
            c.setFont(BOLD, 30)
            c.drawCentredString(midx, midy - 8, 'f( )')
        c.setFillColor(col)
        c.setFont(BOLD, 11)
        c.drawCentredString(x + cw / 2, y - chh + 12, lab)
    footer(c, page_no)
    c.showPage()


def page_grid(c, page_no):
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(B.CIENCIA)
    c.rect(0, H - 86, W, 86, fill=1, stroke=0)
    B.draw_logo_image(c, W - MARGIN - 30, H - 43, 70)
    c.setFillColor(white)
    c.setFont(BOLD, 24)
    c.drawString(MARGIN, H - 50, 'Cuadrícula y laberinto')
    c.setFont(FONT, 11)
    c.drawString(MARGIN, H - 72, 'Úsala en la mesa, o cópiala en grande en el suelo con tiza o cinta.')
    # cuadrícula 6x6
    n = 6
    gs = (W - 2 * MARGIN)
    cell = gs / n
    topy = H - 120
    c.setStrokeColor(B.tint(B.CIENCIA, 0.3))
    c.setLineWidth(1.2)
    for i in range(n + 1):
        c.line(MARGIN, topy - i * cell, MARGIN + gs, topy - i * cell)
        c.line(MARGIN + i * cell, topy, MARGIN + i * cell, topy - n * cell)
    # marcas inicio/meta
    c.setFillColor(B.tint(B.BLUE, 0.6))
    c.rect(MARGIN + 2, topy - cell + 2, cell - 4, cell - 4, fill=1, stroke=0)
    c.setFillColor(B.BLUE)
    c.setFont(BOLD, 12)
    c.drawCentredString(MARGIN + cell / 2, topy - cell / 2 - 4, 'INICIO')
    c.setFillColor(B.tint(B.INGEN, 0.6))
    c.rect(MARGIN + gs - cell + 2, topy - n * cell + 2, cell - 4, cell - 4, fill=1, stroke=0)
    c.setFillColor(B.INGEN)
    c.drawCentredString(MARGIN + gs - cell / 2, topy - n * cell + cell / 2 - 4, 'META')
    # zona para escribir el programa
    py = topy - n * cell - 26
    c.setFillColor(B.tint(B.MATES, 0.9))
    c.roundRect(MARGIN, py - 150, W - 2 * MARGIN, 150, 10, fill=1, stroke=0)
    c.setFillColor(B.MATES)
    c.setFont(BOLD, 12)
    c.drawString(MARGIN + 14, py - 22, 'Mi programa (pega o dibuja tus flechas en orden):')
    c.setStrokeColor(B.tint(B.MATES, 0.5))
    c.setLineWidth(0.8)
    for i in range(4):
        yy = py - 44 - i * 30
        c.setDash(2, 3)
        c.line(MARGIN + 14, yy, W - MARGIN - 14, yy)
        c.setDash()
    footer(c, page_no)
    c.showPage()


def page_diploma(c, page_no):
    c.setFillColor(B.tint(B.BLUE, 0.9))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    B.draw_doodles(c, W, H, color=B.BLUE)
    m = 60
    c.setStrokeColor(B.PURPLE)
    c.setLineWidth(6)
    c.roundRect(m, m, W - 2 * m, H - 2 * m, 18, fill=0, stroke=1)
    c.setStrokeColor(B.BLUE)
    c.setLineWidth(2)
    c.roundRect(m + 10, m + 10, W - 2 * m - 20, H - 2 * m - 20, 14, fill=0, stroke=1)
    B.draw_logo_image(c, W / 2, H - 150, 120)
    c.setFillColor(B.PURPLE)
    c.setFont(BOLD, 30)
    c.drawCentredString(W / 2, H - 232, 'DIPLOMA DE')
    c.setFont(BOLD, 32)
    c.setFillColor(B.MAGENTA)
    c.drawCentredString(W / 2, H - 272, 'PROGRAMADOR/A DIVERGENIO')
    c.setFillColor(B.INK)
    c.setFont(FONT, 14)
    c.drawCentredString(W / 2, H - 318, 'Otorgado con orgullo a:')
    c.setStrokeColor(B.PURPLE)
    c.setLineWidth(1.2)
    c.line(W / 2 - 180, H - 356, W / 2 + 180, H - 356)
    para(c, 'por aprender a pensar con orden, cazar bugs sin rendirse y programar su primer '
         'robot… ¡sin una sola pantalla!',
         W / 2 - 200, H - 388, 400, FONT, 13, 18, B.INK, align='center')
    c.setFont(BOLD, 22)
    c.setFillColor(B.PURPLE)
    c.drawCentredString(W / 2, H - 436, '¡APRENDER ES DIVERTIDO!')
    c.setFont(FONT, 13)
    c.setFillColor(B.INK)
    c.drawCentredString(W / 2, H - 476, 'Lecciones completadas: ______ / 13')
    c.drawString(W / 2 - 175, H - 520, 'Fecha: ____ / ____ / ______')
    c.drawString(W / 2 + 15, H - 520, 'Jefe de robots:')
    c.line(W / 2 + 15, H - 540, W / 2 + 180, H - 540)
    B.draw_logo(c, W / 2 - 70, m + 24, size=18)
    footer(c, page_no)
    c.showPage()


def page_back(c, page_no):
    c.setFillColor(B.PURPLE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    B.draw_doodles(c, W, H, color=white)
    B.draw_logo_image(c, W / 2, H * 0.76, 128)
    c.setFillColor(white)
    c.setFont(BOLD, 30)
    c.drawCentredString(W / 2, H * 0.57, 'Sigue programando el mundo')
    para(c, 'Ya piensas como un programador. En divergenios.com te esperan experimentos, retos '
         'de ingeniería y más aventuras STEAM para seguir creando.',
         W / 2 - 220, H * 0.45, 440, FONT, 13, 19, white, align='center')
    ctas = ['Laboratorio Divergenio · 20 experimentos', 'Retos de Ingeniería · 16 desafíos',
            'Club Divergenio · novedades cada mes']
    yy = H * 0.34
    for t in ctas:
        wc = pdfmetrics.stringWidth(t, BOLD, 13) + 40
        c.setFillColor(B.BLUE)
        c.roundRect(W / 2 - wc / 2, yy, wc, 30, 15, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(BOLD, 13)
        c.drawCentredString(W / 2, yy + 9, t)
        yy -= 42
    c.setFont(BOLD, 20)
    c.setFillColor(white)
    c.drawCentredString(W / 2, H * 0.16, 'divergenios.com')
    c.setFont(FONT, 12)
    c.drawCentredString(W / 2, H * 0.13, 'aprender es divertido')
    c.setFont(FONT, 8)
    c.setFillColor(B.tint(B.PURPLE, 0.5))
    c.drawCentredString(W / 2, 40, '© divergenios.com · Uso personal y de aula. Prohibida su reventa o redistribución.')
    c.showPage()


def build(lessons, outfile, lead_magnet=False):
    c = canvas.Canvas(outfile, pagesize=A4)
    c.setTitle('Tu primer robot · Cuaderno' + (' — Muestra gratis' if lead_magnet else ''))
    c.setAuthor('divergenios.com')
    c.setSubject('Robótica y programación sin pantallas · 6-10 años')
    dests = {e['n']: 'lec%d' % e['n'] for e in lessons}
    page_cover(c)
    page_howto(c)
    if lead_magnet:
        page_arrow_cards(c, 3)
        page_grid(c, 4)
        page_back(c, 5)
        c.save()
        return 5
    pno = 3
    done = set()
    for i in range(0, len(lessons), 2):
        page_lessons(c, lessons[i:i + 2], pno, dests, done)
        pno += 1
    page_arrow_cards(c, pno); pno += 1
    page_grid(c, pno); pno += 1
    page_diploma(c, pno); pno += 1
    page_back(c, pno)
    c.save()
    return pno


def main():
    lessons = parse_lessons(SRC)
    assert len(lessons) == 13, 'Se esperaban 13 lecciones, hay %d' % len(lessons)
    full = os.path.join(OUTDIR, 'Tu-Primer-Robot-Cuaderno.pdf')
    lead = os.path.join(OUTDIR, 'Lead-Magnet-Tarjetas-de-Flechas.pdf')
    n1 = build(lessons, full)
    n2 = build(lessons, lead, lead_magnet=True)
    print('OK  %-40s  %2d páginas' % (os.path.basename(full), n1))
    print('OK  %-40s  %2d páginas' % (os.path.basename(lead), n2))


if __name__ == '__main__':
    main()
