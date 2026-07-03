# -*- coding: utf-8 -*-
"""
Maqueta 'Retos de Ingeniería Divergenio' a PDF profesional, con marca Divergenios.
Reutiliza la identidad (brand.py) y los helpers de build_lab_pdf.py.
Genera:
  - Retos-de-Ingenieria-Divergenio.pdf  (producto completo)
  - Lead-Magnet-3-Retos.pdf             (captación, 3 retos gratis)
Uso:  python3 build_eng_pdf.py
"""
import os
import re
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand as B
import build_lab_pdf as L           # reutiliza para/para_h/section_label/footer/_wline/clean

W, H, MARGIN = L.W, L.H, L.MARGIN
FONT, BOLD = L.FONT, L.BOLD
para, para_h, section_label, footer, clean = L.para, L.para_h, L.section_label, L.footer, L.clean
_wline = L._wline

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '02-retos-de-ingenieria', 'PRODUCTO.md')
OUTDIR = os.path.join(HERE, '..', '02-retos-de-ingenieria')

NAVY = HexColor('#10456E')      # azul profundo "ingeniería" para portadas
SECTION_CYCLE = [B.INGEN, B.BLUE, B.MATES, B.CIENCIA]


# ============================================================
# PARSER
# ============================================================
def parse_retos(path):
    with open(path, encoding='utf-8') as f:
        raw = f.read()
    retos, cur = [], None
    section, seccolor = None, B.INGEN
    si, in_retos = 0, False
    for line in raw.splitlines():
        if 'Los 16 retos' in line:
            in_retos = True
            continue
        msec = re.match(r'^##\s+(.*)$', line)
        if msec and in_retos:
            name = re.sub(r'\(.*\)', '', clean(msec.group(1))).strip()
            if name and name == name.upper() and any(ch.isalpha() for ch in name):
                section = name
                seccolor = SECTION_CYCLE[si % len(SECTION_CYCLE)]
                si += 1
            continue
        mr = re.match(r'^###\s+(\d+)\.\s+(.*)$', line)
        if mr:
            if cur:
                retos.append(cur)
            cur = {'n': int(mr.group(1)), 'title': clean(mr.group(2)),
                   'section': section, 'color': seccolor, 'flags': [], 'meta': {}}
            continue
        if cur is None:
            continue
        if line.startswith('**Tiempo:**'):
            if '🟢' in line:
                cur['meta']['dif'] = 'Fácil'
            elif '🟡' in line:
                cur['meta']['dif'] = 'Media'
            elif '🔴' in line:
                cur['meta']['dif'] = 'Con adulto'
            if '📏' in line:
                cur['flags'].append('Medible')
            if '⚡' in line:
                cur['flags'].append('Prueba varias veces')
            cur['meta']['tiempo'] = clean(line.split('·')[0].replace('**Tiempo:**', ''))
            continue
        for key, marker in (('mision', '**Misión:**'), ('necesitas', '**Necesitas:**'),
                            ('construye', '**Construye:**'), ('ingenieria', '**La ingeniería detrás:**'),
                            ('prueba', '**Prueba y mejora:**'), ('reto', '**Reto divergenio:**')):
            if marker in line:
                val = clean(line.split(marker, 1)[1])
                cur[key] = val[0].upper() + val[1:] if val else val
                break
    if cur:
        retos.append(cur)
    return retos


# ============================================================
# PÁGINAS
# ============================================================
def page_cover(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(B.BLUE_D)
    c.rect(0, H * 0.62, W, H * 0.38, fill=1, stroke=0)
    B.draw_doodles(c, W, H, color=white)
    B.draw_logo_image(c, W / 2, H * 0.75, 150)
    c.setFillColor(white)
    c.setFont(BOLD, 44)
    c.drawCentredString(W / 2, H * 0.5, 'Retos de')
    c.drawCentredString(W / 2, H * 0.5 - 48, 'Ingeniería')
    c.setFont(BOLD, 30)
    c.setFillColor(B.MAGENTA)
    c.drawCentredString(W / 2, H * 0.5 - 90, 'Divergenio')
    c.setFillColor(white)
    c.roundRect(W / 2 - 210, H * 0.32, 420, 34, 17, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont(BOLD, 13.5)
    c.drawCentredString(W / 2, H * 0.32 + 11, '16 desafíos para construir en casa · 6 a 11 años')
    para(c, 'Imagina, construye, prueba y mejora. Con materiales de reciclaje y sin ser experto.',
         W / 2 - 200, H * 0.27, 400, FONT, 12, 16, white, align='center')
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


def page_welcome(c):
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(B.LIGHT)
    c.rect(0, H - 150, W, 150, fill=1, stroke=0)
    B.draw_logo_image(c, MARGIN + 52, H - 78, 96)
    c.setFillColor(B.INK)
    c.setFont(BOLD, 26)
    c.drawString(MARGIN + 110, H - 70, 'Los ingenieros prueban,')
    c.drawString(MARGIN + 110, H - 98, 'fallan y mejoran.')
    y = H - 188
    intro = ('Los ingenieros no nacen sabiendo. En este cuaderno no hay "una solución '
             'correcta": hay misiones. Construye la torre más alta, el puente que aguante más '
             'libros, el coche que llegue más lejos. Tú decides cómo. Y cuando algo se caiga '
             '(que se caerá), no habrás fracasado: habrás encontrado la primera cosa que '
             'mejorar. Eso se llama ingeniería.')
    y = para(c, intro, MARGIN, y, W - 2 * MARGIN, FONT, 12, 17, B.INK) - 10
    c.setFont(BOLD, 13)
    c.setFillColor(B.MATES)
    c.drawString(MARGIN, y, 'Cada reto tiene cuatro partes:')
    y -= 24
    parts = [('1', 'La misión', 'Un objetivo claro que puedes medir.', B.INGEN),
             ('2', 'Construye', 'Ideas para empezar (¡el diseño es tuyo!).', B.BLUE),
             ('3', 'La ingeniería detrás', 'Por qué funciona, para peques.', B.MATES),
             ('4', 'Prueba y mejora', 'El secreto de todo ingeniero.', B.CIENCIA)]
    bw = (W - 2 * MARGIN - 30) / 4
    for i, (num, tit, desc, col) in enumerate(parts):
        bx = MARGIN + i * (bw + 10)
        c.setFillColor(B.tint(col, 0.88))
        c.roundRect(bx, y - 86, bw, 86, 10, fill=1, stroke=0)
        c.setFillColor(col)
        c.circle(bx + 16, y - 16, 10, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(BOLD, 11)
        c.drawCentredString(bx + 16, y - 19.5, num)
        c.setFillColor(col)
        c.setFont(BOLD, 9.5)
        para(c, tit, bx + 30, y - 13, bw - 34, BOLD, 9.5, 11, col)
        para(c, desc, bx + 10, y - 44, bw - 20, FONT, 8.5, 11, B.INK)
    y -= 108
    c.setFont(BOLD, 15)
    c.setFillColor(B.MATES)
    c.drawString(MARGIN, y, '¿Listo, ingeniero divergenio? Ponte el casco imaginario.')
    footer(c, 2)
    c.showPage()


def page_cycle(c):
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(B.MATES)
    c.rect(0, H - 96, W, 96, fill=1, stroke=0)
    B.draw_doodles(c, W, H, color=B.MATES)
    c.setFillColor(white)
    c.setFont(BOLD, 27)
    c.drawString(MARGIN, H - 54, 'El secreto: el ciclo de diseño')
    c.setFont(FONT, 12)
    c.drawString(MARGIN, H - 78, 'Pégalo en la pared. Lo usarás en TODOS los retos.')

    steps = [
        ('1', 'PREGUNTA', '¿Qué tengo que conseguir?', B.INGEN),
        ('2', 'IMAGINA', '¿De cuántas formas podría hacerlo?', B.BLUE),
        ('3', 'CONSTRUYE', 'Haz tu primer intento.', B.MATES),
        ('4', 'PRUEBA', '¿Funcionó? ¿Cuánto aguanta o llega?', B.CIENCIA),
        ('5', 'MEJORA', 'Cambia UNA cosa y vuelve a empezar.', B.MAGENTA),
    ]
    bx = MARGIN + 40
    bw = W - 2 * MARGIN - 130
    bh = 58
    gap = 18
    y = H - 140
    centers = []
    for num, tit, desc, col in steps:
        c.setFillColor(B.tint(col, 0.9))
        c.roundRect(bx, y - bh, bw, bh, 12, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(bx, y - bh, 8, bh, 4, fill=1, stroke=0)
        c.circle(bx + 34, y - bh / 2, 19, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(BOLD, 20)
        c.drawCentredString(bx + 34, y - bh / 2 - 7, num)
        c.setFillColor(col)
        c.setFont(BOLD, 17)
        c.drawString(bx + 66, y - 24, tit)
        c.setFillColor(B.INK)
        c.setFont(FONT, 11.5)
        c.drawString(bx + 66, y - 42, desc)
        centers.append(y - bh / 2)
        # flecha hacia abajo
        if num != '5':
            ax = bx + bw / 2
            c.setStrokeColor(B.GREY)
            c.setLineWidth(2.2)
            c.line(ax, y - bh - 2, ax, y - bh - gap + 4)
            c.setFillColor(B.GREY)
            p = c.beginPath()
            p.moveTo(ax - 5, y - bh - gap + 6)
            p.lineTo(ax + 5, y - bh - gap + 6)
            p.lineTo(ax, y - bh - gap)
            p.close()
            c.drawPath(p, fill=1, stroke=0)
        y -= bh + gap
    # flecha de retorno (MEJORA -> PREGUNTA) por la derecha
    rx = bx + bw + 30
    c.setStrokeColor(B.MAGENTA)
    c.setLineWidth(2.4)
    top, bot = centers[0], centers[-1]
    c.lines([(bx + bw, bot, rx, bot), (rx, bot, rx, top), (rx, top, bx + bw, top)])
    c.setFillColor(B.MAGENTA)
    p = c.beginPath()
    p.moveTo(bx + bw + 7, top + 5)
    p.lineTo(bx + bw + 7, top - 5)
    p.lineTo(bx + bw - 1, top)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.saveState()
    c.translate(rx + 12, (top + bot) / 2)
    c.rotate(90)
    c.setFillColor(B.MAGENTA)
    c.setFont(BOLD, 11)
    c.drawCentredString(0, 0, 'repite y mejora ↺')
    c.restoreState()
    # regla de oro (debajo de la última caja, sin solaparse)
    ry = y - 6                       # box5 acaba en y+gap; dejamos ~24px de aire
    c.setFillColor(B.INK)
    c.roundRect(MARGIN, ry - 44, W - 2 * MARGIN, 44, 10, fill=1, stroke=0)
    c.setFillColor(B.YELLOW)
    c.setFont(BOLD, 12)
    c.drawString(MARGIN + 16, ry - 18, 'Regla de oro')
    c.setFillColor(white)
    c.setFont(FONT, 11.5)
    c.drawString(MARGIN + 16, ry - 34, 'Ningún reto se hace una sola vez. Construye, prueba y MEJORA.')
    footer(c, 3)
    c.showPage()


def page_safety(c):
    c.setFillColor(B.tint(B.INGEN, 0.92))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(B.INGEN)
    c.rect(0, H - 120, W, 120, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(BOLD, 30)
    c.drawCentredString(W / 2, H - 62, 'Reglas del taller seguro')
    c.setFont(BOLD, 16)
    c.drawCentredString(W / 2, H - 92, '¡El ingeniero responsable cuida de todos!')
    rules = [
        'Siempre con un adulto cerca.',
        'Cortes y pegamento caliente: los hace el adulto.',
        'Nada que se lance va hacia las caras; solo objetos blandos.',
        'Cuidado con palillos, alambres y bordes; protégete los dedos.',
        'Recoger forma parte del reto.',
    ]
    y = H - 168
    for i, r in enumerate(rules, 1):
        c.setFillColor(white)
        c.roundRect(MARGIN, y - 56, W - 2 * MARGIN, 56, 12, fill=1, stroke=0)
        c.setFillColor(B.INGEN)
        c.circle(MARGIN + 34, y - 28, 18, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(BOLD, 20)
        c.drawCentredString(MARGIN + 34, y - 35, str(i))
        para(c, r, MARGIN + 64, y - 22, W - 2 * MARGIN - 80, BOLD, 13, 16, B.INK)
        y -= 66
    c.setFillColor(B.INK)
    c.roundRect(MARGIN, y - 54, W - 2 * MARGIN, 48, 12, fill=1, stroke=0)
    c.setFillColor(B.YELLOW)
    c.setFont(BOLD, 12)
    c.drawString(MARGIN + 16, y - 22, 'Iconos')
    leg = [('Fácil', B.CIENCIA), ('Media', B.FISICA), ('Con adulto', B.INGEN),
           ('Reto medible', B.BLUE), ('Hay que probar varias veces', B.MAGENTA)]
    lx = MARGIN + 80
    c.setFont(FONT, 9.5)
    for label, col in leg:
        c.setFillColor(col)
        c.circle(lx + 5, y - 25, 5, fill=1, stroke=0)
        c.setFillColor(white)
        c.drawString(lx + 16, y - 28, label)
        lx += pdfmetrics.stringWidth(label, FONT, 9.5) + 34
    footer(c, 4)
    c.showPage()


def page_index(c, retos, dests):
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(0, H - 96, W, 96, fill=1, stroke=0)
    B.draw_doodles(c, W, H, color=B.BLUE)
    c.setFillColor(white)
    c.setFont(BOLD, 28)
    c.drawString(MARGIN, H - 56, 'Índice de retos')
    c.setFont(FONT, 12)
    c.drawString(MARGIN, H - 80, 'Toca un reto para saltar a su página. El color indica el tipo de ingeniería.')
    col_w = (W - 2 * MARGIN - 24) / 2
    y0 = H - 128
    per_col = (len(retos) + 1) // 2
    for idx, e in enumerate(retos):
        col = 0 if idx < per_col else 1
        row = idx if col == 0 else idx - per_col
        x = MARGIN + col * (col_w + 24)
        y = y0 - row * 30
        cc = e['color']
        c.setFillColor(B.tint(cc, 0.9))
        c.roundRect(x, y - 20, col_w, 26, 6, fill=1, stroke=0)
        c.setFillColor(cc)
        c.circle(x + 16, y - 7, 11, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(BOLD, 10)
        c.drawCentredString(x + 16, y - 11, str(e['n']))
        c.setFillColor(B.INK)
        c.setFont(BOLD, 10.5)
        title = e['title']
        while pdfmetrics.stringWidth(title, BOLD, 10.5) > col_w - 44 and len(title) > 4:
            title = title[:-2]
        if title != e['title']:
            title = title.rstrip() + '…'
        c.drawString(x + 32, y - 11, title)
        c.linkAbsolute('', dests[e['n']], (x, y - 20, x + col_w, y + 6), thickness=0)
    yb = y0 - per_col * 30 - 16
    boxes = [
        ('Por concepto', ['Estructuras: 1-4', 'Fuerzas y movimiento: 5-8, 14',
                          'Máquinas simples: 9-12', 'Flotar y precisión: 13, 15',
                          'Mecanismos y robótica: 10, 16'], B.MATES),
        ('Por tiempo', ['15-20 min: 1, 6, 9, 11, 13, 14', '25-30 min: 2,3,4,5,7,8,10,12,15,16'], B.BLUE),
        ('Solo reciclaje', ['1, 2, 3, 4, 5,', '8, 11, 12, 16'], B.CIENCIA),
    ]
    bw = (W - 2 * MARGIN - 24) / 3
    for i, (tit, items, col) in enumerate(boxes):
        bx = MARGIN + i * (bw + 12)
        bh = 18 + len(items) * 13 + 14
        c.setFillColor(B.tint(col, 0.9))
        c.roundRect(bx, yb - bh, bw, bh, 8, fill=1, stroke=0)
        c.setFillColor(col)
        c.setFont(BOLD, 10)
        c.drawString(bx + 10, yb - 16, tit)
        c.setFillColor(B.INK)
        c.setFont(FONT, 8.5)
        yy = yb - 30
        for it in items:
            c.drawString(bx + 10, yy, it)
            yy -= 13
    footer(c, 5)
    c.showPage()


def page_reto(c, e, page_no, dest):
    col = e['color']
    c.bookmarkPage(dest)
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(col)
    c.rect(0, H - 92, W, 92, fill=1, stroke=0)
    c.setFillColor(B.tint(col, 0.35))
    c.rect(0, H - 96, W, 4, fill=1, stroke=0)
    c.setFillColor(white)
    c.circle(MARGIN + 26, H - 46, 22, fill=1, stroke=0)
    c.setFillColor(col)
    c.setFont(BOLD, 22)
    c.drawCentredString(MARGIN + 26, H - 54, str(e['n']))
    c.setFillColor(white)
    tt = e['title']
    size = 22
    while pdfmetrics.stringWidth(tt, BOLD, size) > W - MARGIN - 70 and size > 14:
        size -= 1
    c.setFont(BOLD, size)
    c.drawString(MARGIN + 62, H - 48, tt)
    cx, cy = MARGIN + 62, H - 76
    chips = []
    if e.get('section'):
        chips.append(e['section'])
    if e['meta'].get('tiempo'):
        chips.append(e['meta']['tiempo'])
    if e['meta'].get('dif'):
        chips.append(e['meta']['dif'])
    chips += e.get('flags', [])
    for lab in chips:
        txt = lab.upper()
        wc = pdfmetrics.stringWidth(txt, BOLD, 7.5) + 14
        c.setFillColor(white)
        c.roundRect(cx, cy, wc, 13, 6.5, fill=1, stroke=0)
        c.setFillColor(col)
        c.setFont(BOLD, 7.5)
        c.drawString(cx + 7, cy + 3.5, txt)
        cx += wc + 6

    blocks_prose = [
        ('necesitas', 'QUÉ NECESITAS', B.CIENCIA, False),
        ('construye', 'CÓMO EMPEZAR A CONSTRUIR', B.INGEN, False),
    ]

    def heights(bs):
        lead = bs + 4
        gap = 9
        used = 0
        wmax = W - 2 * MARGIN - 24
        used += para_h(e['mision'], wmax, BOLD, bs + 1, lead + 1) + 24 + gap
        for key, _, _, _ in blocks_prose:
            if e.get(key):
                used += 18 + para_h(e[key], W - 2 * MARGIN, FONT, bs, lead) + gap
        used += para_h(e['ingenieria'], wmax, FONT, bs, lead) + 26 + gap
        if e.get('prueba'):
            used += para_h(e['prueba'], wmax, FONT, bs, lead) + 24 + gap
        if e.get('reto'):
            used += para_h(e['reto'], wmax, FONT, bs, lead) + 24 + gap
        return used

    bs = 10.5
    for cand in (10.5, 10, 9.5, 9, 8.5, 8):
        if (H - 112) - heights(cand) > 52:
            bs = cand
            break
        bs = cand
    lead = bs + 4
    gap = 9
    y = H - 112
    wmax = W - 2 * MARGIN - 24

    # MISIÓN (destacada con color de sección)
    mh = para_h(e['mision'], wmax, BOLD, bs + 1, lead + 1) + 24
    c.setFillColor(B.tint(col, 0.88))
    c.roundRect(MARGIN, y - mh, W - 2 * MARGIN, mh, 10, fill=1, stroke=0)
    c.setFillColor(col)
    c.roundRect(MARGIN, y - mh, 6, mh, 3, fill=1, stroke=0)
    section_label(c, MARGIN + 12, y - 15, 'LA MISIÓN', col)
    para(c, e['mision'], MARGIN + 14, y - 32, wmax, BOLD, bs + 1, lead + 1, B.INK)
    y -= mh + gap

    for key, label, lcol, _ in blocks_prose:
        if e.get(key):
            section_label(c, MARGIN, y, label, lcol)
            y -= 18
            y = para(c, e[key], MARGIN, y, W - 2 * MARGIN, FONT, bs, lead, B.INK) - gap

    # LA INGENIERÍA DETRÁS
    ih = para_h(e['ingenieria'], wmax, FONT, bs, lead) + 26
    c.setFillColor(B.tint(col, 0.92))
    c.roundRect(MARGIN, y - ih, W - 2 * MARGIN, ih, 10, fill=1, stroke=0)
    c.setFillColor(col)
    c.setLineWidth(3)
    c.line(MARGIN + 3, y - ih + 6, MARGIN + 3, y - 6)
    section_label(c, MARGIN + 10, y - 14, 'LA INGENIERÍA DETRÁS', col)
    para(c, e['ingenieria'], MARGIN + 12, y - 32, wmax, FONT, bs, lead, B.INK)
    y -= ih + gap

    if e.get('prueba'):
        ph = para_h(e['prueba'], wmax, FONT, bs, lead) + 24
        c.setFillColor(B.tint(B.BLUE, 0.9))
        c.roundRect(MARGIN, y - ph, W - 2 * MARGIN, ph, 10, fill=1, stroke=0)
        section_label(c, MARGIN + 10, y - 14, 'PRUEBA Y MEJORA', B.BLUE)
        para(c, e['prueba'], MARGIN + 12, y - 32, wmax, FONT, bs, lead, B.INK)
        y -= ph + gap

    if e.get('reto'):
        rh = para_h(e['reto'], wmax, FONT, bs, lead) + 24
        c.setFillColor(B.tint(B.INGEN, 0.88))
        c.roundRect(MARGIN, y - rh, W - 2 * MARGIN, rh, 10, fill=1, stroke=0)
        section_label(c, MARGIN + 10, y - 14, 'RETO DIVERGENIO', B.INGEN)
        para(c, e['reto'], MARGIN + 12, y - 32, wmax, FONT, bs, lead, B.INK)
        y -= rh + gap

    footer(c, page_no)
    c.showPage()


def page_notebook(c, page_no):
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(B.MATES)
    c.rect(0, H - 86, W, 86, fill=1, stroke=0)
    B.draw_logo_image(c, W - MARGIN - 30, H - 43, 70)
    c.setFillColor(white)
    c.setFont(BOLD, 24)
    c.drawString(MARGIN, H - 50, 'Mi Cuaderno de Ingeniería')
    c.setFont(FONT, 11)
    c.drawString(MARGIN, H - 72, 'Una copia por reto. Diseña, prueba y mejora como un ingeniero de verdad.')
    x = MARGIN
    w = W - 2 * MARGIN
    y = H - 116
    c.setFillColor(B.tint(B.MATES, 0.9))
    c.roundRect(x, y - 44, w, 44, 8, fill=1, stroke=0)
    c.setFont(BOLD, 10)
    c.setFillColor(B.INK)
    c.drawString(x + 12, y - 18, 'Ingeniero/a:')
    _wline(c, x + 90, y - 20, w - 230)
    c.drawString(x + w - 120, y - 18, 'Reto n.º:')
    _wline(c, x + w - 62, y - 20, 50)
    c.drawString(x + 12, y - 36, 'Misión:')
    _wline(c, x + 60, y - 38, w - 80)
    y -= 60

    # 1) primer diseño (caja grande)
    c.setFillColor(B.INGEN)
    c.circle(x + 10, y - 6, 9, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(BOLD, 10)
    c.drawCentredString(x + 10, y - 9.5, '1')
    c.setFillColor(B.INGEN)
    c.setFont(BOLD, 11)
    c.drawString(x + 26, y - 10, 'MI PRIMER DISEÑO')
    c.setFillColor(B.GREY)
    c.setFont(FONT, 9)
    c.drawString(x + 26 + pdfmetrics.stringWidth('MI PRIMER DISEÑO', BOLD, 11) + 8, y - 10, 'Dibújalo')
    c.setStrokeColor(B.tint(B.INGEN, 0.4))
    c.setLineWidth(1.2)
    c.roundRect(x + 26, y - 26 - 120, w - 52, 120, 8, fill=0, stroke=1)
    c.setFillColor(B.tint(B.INGEN, 0.6))
    c.setFont(FONT, 9)
    c.drawCentredString(x + 26 + (w - 52) / 2, y - 26 - 60, '(tu diseño)')
    y = y - 26 - 120 - 16

    def field(num, tit, hint, col, lines=2):
        nonlocal y
        c.setFillColor(col)
        c.circle(x + 10, y - 6, 9, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(BOLD, 10)
        c.drawCentredString(x + 10, y - 9.5, num)
        c.setFillColor(col)
        c.setFont(BOLD, 11)
        c.drawString(x + 26, y - 10, tit)
        c.setFillColor(B.GREY)
        c.setFont(FONT, 9)
        c.drawString(x + 26 + pdfmetrics.stringWidth(tit, BOLD, 11) + 8, y - 10, hint)
        yy = y - 26
        for _ in range(lines):
            _wline(c, x + 26, yy, w - 26)
            yy -= 18
        y = yy - 6

    field('2', 'PRUEBA 1', '¿Qué pasó? ¿cuánto aguantó o llegó?', B.BLUE, 2)
    field('3', '¿QUÉ VOY A MEJORAR?', 'Cambio UNA sola cosa', B.MAGENTA, 2)

    # 4) prueba 2 antes/después
    c.setFillColor(B.CIENCIA)
    c.circle(x + 10, y - 6, 9, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(BOLD, 10)
    c.drawCentredString(x + 10, y - 9.5, '4')
    c.setFillColor(B.CIENCIA)
    c.setFont(BOLD, 11)
    c.drawString(x + 26, y - 10, 'PRUEBA 2')
    c.setFillColor(B.INK)
    c.setFont(BOLD, 10)
    c.drawString(x + 140, y - 10, 'Antes:')
    _wline(c, x + 185, y - 12, 90)
    c.drawString(x + 290, y - 10, 'Después:')
    _wline(c, x + 345, y - 12, 90)
    y -= 30

    field('5', 'MI MEJOR MARCA', '', B.INGEN, 1)
    c.setFillColor(B.tint(B.MATES, 0.9))
    c.roundRect(x, y - 44, w, 44, 8, fill=1, stroke=0)
    c.setFillColor(B.INK)
    c.setFont(BOLD, 10)
    c.drawString(x + 12, y - 18, 'Lo que más me costó:')
    _wline(c, x + 140, y - 20, w - 160)
    c.drawString(x + 12, y - 36, 'Lo que más me gustó:')
    _wline(c, x + 140, y - 38, w - 160)
    footer(c, page_no)
    c.showPage()


def page_diploma(c, page_no):
    c.setFillColor(B.tint(B.BLUE, 0.9))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    B.draw_doodles(c, W, H, color=B.BLUE)
    m = 60
    c.setStrokeColor(NAVY)
    c.setLineWidth(6)
    c.roundRect(m, m, W - 2 * m, H - 2 * m, 18, fill=0, stroke=1)
    c.setStrokeColor(B.YELLOW)
    c.setLineWidth(2)
    c.roundRect(m + 10, m + 10, W - 2 * m - 20, H - 2 * m - 20, 14, fill=0, stroke=1)
    B.draw_logo_image(c, W / 2, H - 150, 120)
    c.setFillColor(NAVY)
    c.setFont(BOLD, 30)
    c.drawCentredString(W / 2, H - 230, 'DIPLOMA DE')
    c.setFont(BOLD, 34)
    c.setFillColor(B.MAGENTA)
    c.drawCentredString(W / 2, H - 270, 'INGENIERO/A DIVERGENIO')
    c.setFillColor(B.INK)
    c.setFont(FONT, 14)
    c.drawCentredString(W / 2, H - 314, 'Otorgado con orgullo a:')
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.2)
    c.line(W / 2 - 180, H - 354, W / 2 + 180, H - 354)
    para(c, 'por diseñar, construir, probar y MEJORAR como un auténtico ingeniero. '
         'Por no rendirse cuando algo se cayó… ¡y volver a intentarlo mejor!',
         W / 2 - 210, H - 386, 420, FONT, 13, 18, B.INK, align='center')
    c.setFont(BOLD, 22)
    c.setFillColor(NAVY)
    c.drawCentredString(W / 2, H - 440, '¡APRENDER ES DIVERTIDO!')
    c.setFont(FONT, 13)
    c.setFillColor(B.INK)
    c.drawCentredString(W / 2, H - 478, 'Retos superados: ______ / 16')
    c.drawString(W / 2 - 180, H - 524, 'Fecha: ____ / ____ / ______')
    c.drawString(W / 2 + 10, H - 524, 'Jefe de taller:')
    c.line(W / 2 + 10, H - 544, W / 2 + 180, H - 544)
    B.draw_logo(c, W / 2 - 70, m + 24, size=18)
    footer(c, page_no)
    c.showPage()


def page_back(c, page_no):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    B.draw_doodles(c, W, H, color=white)
    B.draw_logo_image(c, W / 2, H * 0.76, 130)
    c.setFillColor(white)
    c.setFont(BOLD, 30)
    c.drawCentredString(W / 2, H * 0.58, '¿Listo para el siguiente')
    c.drawCentredString(W / 2, H * 0.58 - 38, 'desafío?')
    para(c, 'Has diseñado, construido y mejorado como un ingeniero de verdad. En '
         'divergenios.com te esperan más experimentos, robótica sin pantallas y retos '
         'nuevos cada mes para seguir creando.',
         W / 2 - 220, H * 0.44, 440, FONT, 13, 19, white, align='center')
    ctas = ['Laboratorio Divergenio · 20 experimentos', 'Club Divergenio · novedades cada mes',
            'Tu primer robot · sin pantallas']
    yy = H * 0.33
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
    c.setFillColor(B.tint(NAVY, 0.5))
    c.drawCentredString(W / 2, 40, '© divergenios.com · Uso personal y de aula. Prohibida su reventa o redistribución.')
    c.showPage()


def build(retos, outfile, subset=None, lead_magnet=False):
    c = canvas.Canvas(outfile, pagesize=A4)
    c.setTitle('Retos de Ingeniería Divergenio' + (' — Muestra gratis' if lead_magnet else ''))
    c.setAuthor('divergenios.com')
    c.setSubject('16 desafíos de ingeniería para 6-11 años')
    dests = {e['n']: 'reto%d' % e['n'] for e in retos}
    page_cover(c)
    page_welcome(c)
    page_cycle(c)
    page_safety(c)
    items = retos if subset is None else [e for e in retos if e['n'] in subset]
    if not lead_magnet:
        page_index(c, retos, dests)
        pno = 6
    else:
        pno = 5
    for e in items:
        page_reto(c, e, pno, dests[e['n']])
        pno += 1
    if not lead_magnet:
        page_notebook(c, pno)
        pno += 1
        page_diploma(c, pno)
        pno += 1
    page_back(c, pno)
    c.save()
    return pno


def main():
    retos = parse_retos(SRC)
    assert len(retos) == 16, 'Se esperaban 16 retos, hay %d' % len(retos)
    full = os.path.join(OUTDIR, 'Retos-de-Ingenieria-Divergenio.pdf')
    lead = os.path.join(OUTDIR, 'Lead-Magnet-3-Retos.pdf')
    n1 = build(retos, full)
    n2 = build(retos, lead, subset={1, 7, 16}, lead_magnet=True)
    print('OK  %-44s  %2d páginas' % (os.path.basename(full), n1))
    print('OK  %-44s  %2d páginas' % (os.path.basename(lead), n2))


if __name__ == '__main__':
    main()
