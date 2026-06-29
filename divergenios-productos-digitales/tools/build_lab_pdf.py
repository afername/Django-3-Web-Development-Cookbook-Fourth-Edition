# -*- coding: utf-8 -*-
"""
Maqueta 'Laboratorio Divergente en Casa' a PDF profesional, con marca Divergenios.
Genera:
  - Laboratorio-Divergente-en-Casa.pdf  (producto completo)
  - Lead-Magnet-3-Experimentos.pdf      (captacion, 3 experimentos gratis)
Uso:  python3 build_lab_pdf.py
"""
import os
import re
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand as B

W, H = A4
MARGIN = 44
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '01-laboratorio-divergente-en-casa', 'PRODUCTO.md')
OUTDIR = os.path.join(HERE, '..', '01-laboratorio-divergente-en-casa')

# ---- fuentes ----
DV = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
DVB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DV', DV))
pdfmetrics.registerFont(TTFont('DVB', DVB))
FONT, BOLD = 'DV', 'DVB'

# ---- limpieza de emojis ----
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF"
    "\U00002190-\U000021FF\U00002300-\U000023FF\U0001F1E6-\U0001F1FF"
    "\U0000FE0F\U0000200D\U000020E3\U00002700-\U000027BF]+",
    flags=re.UNICODE)


def clean(s):
    s = EMOJI_RE.sub('', s)
    s = s.replace('**', '').replace('_', '')
    return re.sub(r'\s+', ' ', s).strip()


# ============================================================
# PARSER
# ============================================================
def parse_experiments(path):
    with open(path, encoding='utf-8') as f:
        raw = f.read()
    exps = []
    cur = None
    mode = None
    for line in raw.splitlines():
        m = re.match(r'^###\s+(\d+)\.\s+(.*)$', line)
        if m:
            if cur:
                exps.append(cur)
            cur = {'n': int(m.group(1)), 'title': clean(m.group(2)),
                   'steps': [], 'meta': {}, 'flags': []}
            mode = None
            continue
        if cur is None:
            continue
        if line.startswith('**Área:**') or line.startswith('** Área'):
            # dificultad / flags por emoji crudo
            if '🟢' in line:
                cur['meta']['dif'] = 'Fácil'
            elif '🟡' in line:
                cur['meta']['dif'] = 'Media'
            elif '🔴' in line:
                cur['meta']['dif'] = 'Con adulto'
            if '🌈' in line:
                cur['flags'].append('Mancha: usa delantal')
            if '⚠️' in line or '⚠' in line:
                cur['flags'].append('Cuidado especial')
            parts = [clean(p) for p in line.split('·')]
            for p in parts:
                if p.lower().startswith('área'):
                    cur['meta']['area'] = p.split(':', 1)[1].strip()
                elif p.lower().startswith('tiempo'):
                    cur['meta']['tiempo'] = p.split(':', 1)[1].strip()
            mode = None
            continue
        if '**Pregunta divergente:**' in line:
            cur['pregunta'] = clean(line.split('**Pregunta divergente:**')[1])
            mode = None
            continue
        if '**Necesitas:**' in line:
            cur['necesitas'] = clean(line.split('**Necesitas:**')[1])
            mode = None
            continue
        if '**Paso a paso:**' in line:
            mode = 'steps'
            continue
        if '**¿Qué pasó?**' in line:
            cur['quepaso'] = clean(line.split('**¿Qué pasó?**')[1])
            mode = None
            continue
        if '**Reto divergente:**' in line:
            cur['reto'] = clean(line.split('**Reto divergente:**')[1])
            mode = None
            continue
        if '**Pregunta de oro' in line:
            cur['oro'] = clean(line.split(':**', 1)[1]) if ':**' in line else clean(line)
            mode = None
            continue
        if mode == 'steps':
            sm = re.match(r'^\s*\d+\.\s+(.*)$', line)
            if sm:
                cur['steps'].append(clean(sm.group(1)))
    if cur:
        exps.append(cur)
    return exps


def area_color(area):
    a = (area or '').lower()
    a = (a.replace('á', 'a').replace('é', 'e').replace('í', 'i')
         .replace('ó', 'o').replace('ú', 'u'))
    for key, col in B.AREA_COLORS.items():
        if key in a:
            return col
    return B.PURPLE


# ============================================================
# PRIMITIVAS DE DIBUJO
# ============================================================
def para(c, text, x, y, width, font, size, leading, color, align='left'):
    lines = simpleSplit(text, font, size, width)
    c.setFont(font, size)
    c.setFillColor(color)
    for ln in lines:
        if align == 'center':
            c.drawCentredString(x + width / 2, y, ln)
        else:
            c.drawString(x, y, ln)
        y -= leading
    return y


def para_h(text, width, font, size, leading):
    return len(simpleSplit(text, font, size, width)) * leading


def chip(c, x, y, label, color, h=15):
    w = pdfmetrics.stringWidth(label, BOLD, 8) + 16
    c.setFillColor(color)
    c.roundRect(x, y, w, h, h / 2, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(BOLD, 8)
    c.drawString(x + 8, y + 4, label)
    return w


def section_label(c, x, y, text, color):
    """Etiqueta de seccion tipo pildora + linea."""
    c.setFont(BOLD, 9.5)
    w = pdfmetrics.stringWidth(text, BOLD, 9.5) + 18
    c.setFillColor(color)
    c.roundRect(x, y - 2, w, 15, 4, fill=1, stroke=0)
    c.setFillColor(white)
    c.drawString(x + 9, y + 2, text)
    return w


def footer(c, page_no, total=None):
    c.saveState()
    c.setStrokeColor(B.tint(B.PURPLE, 0.8))
    c.setLineWidth(0.7)
    c.line(MARGIN, 40, W - MARGIN, 40)
    B.draw_logo_image(c, MARGIN + 7, 28, 17)
    c.setFont(B.BOLD, 8)
    c.setFillColor(B.INK)
    c.drawString(MARGIN + 20, 25, 'divergenios.com')
    c.setFont(B.FONT, 7.5)
    c.setFillColor(B.GREY)
    c.drawCentredString(W / 2, 25, 'Uso personal y de aula · Prohibida su reventa')
    c.setFont(B.BOLD, 8)
    c.setFillColor(B.PURPLE)
    txt = str(page_no) if not total else '%d / %d' % (page_no, total)
    c.drawRightString(W - MARGIN, 25, txt)
    c.restoreState()


# ============================================================
# PAGINAS
# ============================================================
def page_cover(c):
    c.setFillColor(B.PURPLE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # banda diagonal clara
    c.setFillColor(B.PURPLE_D)
    c.rect(0, H * 0.62, W, H * 0.38, fill=1, stroke=0)
    B.draw_doodles(c, W, H, color=white)
    # logo oficial grande
    B.draw_logo_image(c, W / 2, H * 0.75, 150)
    # titulo
    c.setFillColor(white)
    c.setFont(BOLD, 46)
    c.drawCentredString(W / 2, H * 0.5, 'Laboratorio')
    c.drawCentredString(W / 2, H * 0.5 - 50, 'Divergente')
    c.setFont(BOLD, 30)
    c.setFillColor(B.BLUE)
    c.drawCentredString(W / 2, H * 0.5 - 92, 'en casa')
    # subtitulo en banda
    c.setFillColor(white)
    c.roundRect(W / 2 - 200, H * 0.32, 400, 34, 17, fill=1, stroke=0)
    c.setFillColor(B.PURPLE)
    c.setFont(BOLD, 14)
    c.drawCentredString(W / 2, H * 0.32 + 11, '20 experimentos STEAM · 6 a 10 años')
    # promesa
    c.setFont(FONT, 12)
    c.setFillColor(B.tint(white, 0))
    c.setFillColor(white)
    para(c, 'Ciencia, ingeniería y matemáticas con cosas de casa. Sin pantallas y sin ser experto.',
         W / 2 - 200, H * 0.27, 400, FONT, 12, 16, white, align='center')
    # logo + tagline al pie
    c.setFont(BOLD, 22)
    c.setFillColor(white)
    wln = pdfmetrics.stringWidth('diver', BOLD, 22)
    c.drawString(W / 2 - (wln + pdfmetrics.stringWidth('genios', BOLD, 22)) / 2 - 4, H * 0.13, 'diver')
    c.setFillColor(B.BLUE)
    c.drawString(W / 2 - (wln + pdfmetrics.stringWidth('genios', BOLD, 22)) / 2 - 4 + wln, H * 0.13, 'genios')
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
    c.drawString(MARGIN + 110, H - 70, '¡Bienvenido al laboratorio')
    c.drawString(MARGIN + 110, H - 98, 'más divertido del mundo!')
    y = H - 190
    body = [
        ('', '¡Bienvenido al laboratorio más divertido del mundo: tu casa! Aquí no hacen '
         'falta batas blancas carísimas ni aparatos raros. Con cosas que ya tienes en la '
         'cocina y en el cajón de las manualidades vas a hacer erupcionar volcanes, '
         'descifrar mensajes secretos, construir puentes que aguantan libros y programar a '
         'un robot… que será tu papá o tu profe.'),
    ]
    for _, t in body:
        y = para(c, t, MARGIN, y, W - 2 * MARGIN, FONT, 12, 17, B.INK) - 8
    # tres partes magicas
    y -= 6
    c.setFont(BOLD, 13)
    c.setFillColor(B.PURPLE)
    c.drawString(MARGIN, y, 'Cada experimento tiene tres partes mágicas:')
    y -= 24
    parts = [
        ('1', 'Paso a paso', 'Qué hacer, fácil y claro.', B.TECNO),
        ('2', '¿Qué pasó?', 'La ciencia explicada para que de verdad la entiendas.', B.CIENCIA),
        ('3', 'Reto divergente', 'La pregunta que convierte a un curioso en científico.', B.INGEN),
    ]
    bw = (W - 2 * MARGIN - 20) / 3
    for i, (num, tit, desc, col) in enumerate(parts):
        bx = MARGIN + i * (bw + 10)
        c.setFillColor(B.tint(col, 0.88))
        c.roundRect(bx, y - 78, bw, 78, 10, fill=1, stroke=0)
        c.setFillColor(col)
        c.circle(bx + 18, y - 16, 11, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(BOLD, 12)
        c.drawCentredString(bx + 18, y - 20, num)
        c.setFillColor(col)
        c.setFont(BOLD, 11)
        c.drawString(bx + 34, y - 20, tit)
        para(c, desc, bx + 10, y - 40, bw - 20, FONT, 9, 12, B.INK)
    y -= 100
    closing = ('No hay forma de hacerlo "mal". Si algo no sale como esperabas… ¡acabas de '
               'descubrir algo! Eso también es ciencia. Imprime las páginas que quieras '
               '(¡funcionan en blanco y negro!), ten a mano el Cuaderno del Científico del '
               'final y, sobre todo, hazte preguntas. La ciencia empieza con un "¿y si…?".')
    y = para(c, closing, MARGIN, y, W - 2 * MARGIN, FONT, 12, 17, B.INK)
    # firma
    c.setFont(BOLD, 14)
    c.setFillColor(B.PURPLE)
    c.drawString(MARGIN, y - 14, '¿Listos? Ponte las gafas imaginarias. Vamos a ser divergenios.')
    footer(c, 2)
    c.showPage()


def page_safety(c):
    c.setFillColor(B.tint(B.INGEN, 0.92))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(B.INGEN)
    c.rect(0, H - 120, W, 120, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(BOLD, 30)
    c.drawCentredString(W / 2, H - 62, 'Las 6 reglas del laboratorio')
    c.setFont(BOLD, 18)
    c.drawCentredString(W / 2, H - 92, '¡Pégalas en la nevera!')
    rules = [
        'Siempre hay un adulto cerca. Tú eres el científico; el adulto es tu ayudante.',
        'Nada va a la boca. Aunque huela a limón, los experimentos no se prueban.',
        'Manos y ojos protegidos cuando lo indique el experimento.',
        'El fuego, los cuchillos y el agua caliente los maneja siempre el adulto.',
        'Recoger es parte del experimento. Un buen científico deja todo limpio.',
        'Antes de tocar, observa y predice: "¿Qué creo que va a pasar?"',
    ]
    y = H - 165
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
    # leyenda de iconos
    c.setFillColor(B.INK)
    c.roundRect(MARGIN, y - 70, W - 2 * MARGIN, 64, 12, fill=1, stroke=0)
    c.setFillColor(B.YELLOW)
    c.setFont(BOLD, 12)
    c.drawString(MARGIN + 16, y - 24, 'Leyenda de dificultad e iconos')
    leg = [('Fácil', B.CIENCIA), ('Media', B.FISICA), ('Con adulto', B.INGEN),
           ('Cuidado especial', B.ARTE), ('Mancha: usa delantal', B.TECNO)]
    lx = MARGIN + 16
    c.setFont(FONT, 9.5)
    for label, col in leg:
        c.setFillColor(col)
        c.circle(lx + 5, y - 46, 5, fill=1, stroke=0)
        c.setFillColor(white)
        c.drawString(lx + 16, y - 49, label)
        lx += pdfmetrics.stringWidth(label, FONT, 9.5) + 36
    footer(c, 3)
    c.showPage()


def page_index(c, exps, dests):
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(B.PURPLE)
    c.rect(0, H - 96, W, 96, fill=1, stroke=0)
    B.draw_doodles(c, W, H * 1.0, color=B.PURPLE)
    c.setFillColor(white)
    c.setFont(BOLD, 28)
    c.drawString(MARGIN, H - 56, 'Índice')
    c.setFont(FONT, 12)
    c.drawString(MARGIN, H - 80, 'Toca un experimento para saltar a su página. ¡Todos son independientes!')
    # lista en dos columnas con enlaces internos
    col_w = (W - 2 * MARGIN - 24) / 2
    y0 = H - 130
    per_col = (len(exps) + 1) // 2
    for idx, e in enumerate(exps):
        col = 0 if idx < per_col else 1
        row = idx if col == 0 else idx - per_col
        x = MARGIN + col * (col_w + 24)
        y = y0 - row * 30
        col_c = area_color(e['meta'].get('area'))
        c.setFillColor(B.tint(col_c, 0.9))
        c.roundRect(x, y - 20, col_w, 26, 6, fill=1, stroke=0)
        c.setFillColor(col_c)
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
    # indices rapidos al pie
    yb = y0 - per_col * 30 - 16
    boxes = [
        ('Por área STEAM', ['Ciencia: 1-6, 13, 18', 'Tecnología: 7, 8', 'Ingeniería: 9-12',
                            'Arte: 4, 8, 13, 14, 17', 'Mates: 8, 14-17', 'Física: 18-20'], B.PURPLE),
        ('Por tiempo', ['10 min o menos: 2, 6, 12, 19', '15-20 min: 1,4,5,8,11,13,14,16,18,20',
                        'Con espera (días): 5, 6, 15'], B.CIENCIA),
        ('Solo cosas de cocina', ['1, 2, 6, 7, 9, 10, 12,', '13, 15, 16, 18, 19'], B.INGEN),
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
    footer(c, 4)
    c.showPage()


def page_experiment(c, e, page_no, dest):
    col = area_color(e['meta'].get('area'))
    c.bookmarkPage(dest)
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # cabecera color
    c.setFillColor(col)
    c.rect(0, H - 92, W, 92, fill=1, stroke=0)
    c.setFillColor(B.tint(col, 0.35))
    c.rect(0, H - 96, W, 4, fill=1, stroke=0)
    # numero badge
    c.setFillColor(white)
    c.circle(MARGIN + 26, H - 46, 22, fill=1, stroke=0)
    c.setFillColor(col)
    c.setFont(BOLD, 22)
    c.drawCentredString(MARGIN + 26, H - 54, str(e['n']))
    # titulo
    c.setFillColor(white)
    tt = e['title']
    size = 22
    while pdfmetrics.stringWidth(tt, BOLD, size) > W - MARGIN - 70 and size > 14:
        size -= 1
    c.setFont(BOLD, size)
    c.drawString(MARGIN + 62, H - 50, tt)
    # chips meta
    cx = MARGIN + 62
    cy = H - 76
    c.setFillColor(B.tint(col, 0.25))
    for key, lab in (('area', e['meta'].get('area', '')), ('tiempo', e['meta'].get('tiempo', '')),
                     ('dif', e['meta'].get('dif', ''))):
        if lab:
            txt = lab.upper()
            wc = pdfmetrics.stringWidth(txt, BOLD, 7.5) + 14
            c.setFillColor(white)
            c.roundRect(cx, cy, wc, 13, 6.5, fill=1, stroke=0)
            c.setFillColor(col)
            c.setFont(BOLD, 7.5)
            c.drawString(cx + 7, cy + 3.5, txt)
            cx += wc + 6

    # cuerpo: autoajuste de tamaño
    def render(body_size):
        avail_top = H - 112
        avail_bot = 52
        y = avail_top
        lead = body_size + 4
        gap = 9
        # Pregunta divergente (destacada)
        if e.get('pregunta'):
            ph = para_h(e['pregunta'], W - 2 * MARGIN - 24, BOLD, body_size + 1, lead + 1) + 22
            c.setFillColor(B.tint(B.YELLOW, 0.7))
            c.roundRect(MARGIN, y - ph, W - 2 * MARGIN, ph, 10, fill=1, stroke=0)
            c.setFillColor(B.INK)
            c.setFont(BOLD, 9)
            c.drawString(MARGIN + 12, y - 14, 'PREGUNTA DIVERGENTE')
            para(c, e['pregunta'], MARGIN + 12, y - 30, W - 2 * MARGIN - 24,
                 BOLD, body_size + 1, lead + 1, B.INK)
            y -= ph + gap
        # Necesitas
        if e.get('necesitas'):
            section_label(c, MARGIN, y, 'QUÉ NECESITAS', B.CIENCIA)
            y -= 18
            y = para(c, e['necesitas'], MARGIN, y, W - 2 * MARGIN, FONT, body_size, lead, B.INK) - gap
        # Paso a paso
        if e.get('steps'):
            section_label(c, MARGIN, y, 'PASO A PASO', B.TECNO)
            y -= 19
            for i, st in enumerate(e['steps'], 1):
                c.setFillColor(B.TECNO)
                c.circle(MARGIN + 8, y + 3, 8, fill=1, stroke=0)
                c.setFillColor(white)
                c.setFont(BOLD, 8.5)
                c.drawCentredString(MARGIN + 8, y + 0.5, str(i))
                y = para(c, st, MARGIN + 24, y + 4, W - 2 * MARGIN - 24, FONT, body_size, lead, B.INK) - 4
            y -= gap - 2
        # Que paso
        if e.get('quepaso'):
            qh = para_h(e['quepaso'], W - 2 * MARGIN - 24, FONT, body_size, lead) + 26
            c.setFillColor(B.tint(col, 0.9))
            c.roundRect(MARGIN, y - qh, W - 2 * MARGIN, qh, 10, fill=1, stroke=0)
            c.setFillColor(col)
            c.setLineWidth(3)
            c.line(MARGIN + 3, y - qh + 6, MARGIN + 3, y - 6)
            section_label(c, MARGIN + 10, y - 14, '¿QUÉ PASÓ? LA CIENCIA', col)
            para(c, e['quepaso'], MARGIN + 12, y - 32, W - 2 * MARGIN - 24, FONT, body_size, lead, B.INK)
            y -= qh + gap
        # Reto
        if e.get('reto'):
            rh = para_h(e['reto'], W - 2 * MARGIN - 24, FONT, body_size, lead) + 24
            c.setFillColor(B.tint(B.INGEN, 0.88))
            c.roundRect(MARGIN, y - rh, W - 2 * MARGIN, rh, 10, fill=1, stroke=0)
            section_label(c, MARGIN + 10, y - 14, 'RETO DIVERGENTE', B.INGEN)
            para(c, e['reto'], MARGIN + 12, y - 32, W - 2 * MARGIN - 24, FONT, body_size, lead, B.INK)
            y -= rh + gap
        # Pregunta de oro
        if e.get('oro'):
            c.setFillColor(B.PURPLE)
            c.setFont(BOLD, body_size - 0.5)
            oro = 'Pregunta de oro (adulto): ' + e['oro']
            y = para(c, oro, MARGIN, y, W - 2 * MARGIN, BOLD, body_size - 0.5, lead - 1, B.PURPLE)
        # flags
        if e.get('flags'):
            y -= 4
            c.setFont(FONT, body_size - 1.5)
            c.setFillColor(B.ARTE)
            c.drawString(MARGIN, y, '! ' + ' · '.join(e['flags']))
            y -= lead
        return y, avail_bot

    # probar tamaños hasta que entre (medir sin dibujar: simular alturas)
    for bs in (10.5, 10, 9.5, 9, 8.5, 8):
        lead = bs + 4
        gap = 9
        total = H - 112
        used = total
        if e.get('pregunta'):
            used -= para_h(e['pregunta'], W - 2 * MARGIN - 24, BOLD, bs + 1, lead + 1) + 22 + gap
        if e.get('necesitas'):
            used -= 18 + para_h(e['necesitas'], W - 2 * MARGIN, FONT, bs, lead) + gap
        if e.get('steps'):
            used -= 19 + sum(para_h(s, W - 2 * MARGIN - 24, FONT, bs, lead) + 4 for s in e['steps']) + gap
        if e.get('quepaso'):
            used -= para_h(e['quepaso'], W - 2 * MARGIN - 24, FONT, bs, lead) + 26 + gap
        if e.get('reto'):
            used -= para_h(e['reto'], W - 2 * MARGIN - 24, FONT, bs, lead) + 24 + gap
        if e.get('oro'):
            used -= para_h('Pregunta de oro (adulto): ' + e['oro'], W - 2 * MARGIN, BOLD, bs - 0.5, lead - 1)
        if e.get('flags'):
            used -= lead + 4
        if used > 52:
            break
    render(bs)
    footer(c, page_no)
    c.showPage()


def _wline(c, x, y, w, color=None):
    c.setStrokeColor(color or B.tint(B.INK, 0.55))
    c.setLineWidth(0.8)
    c.setDash(1, 3)
    c.line(x, y, x + w, y)
    c.setDash()


def page_notebook(c, page_no):
    """Cuaderno del Cientifico: formulario vectorial imprimible."""
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(B.CIENCIA)
    c.rect(0, H - 86, W, 86, fill=1, stroke=0)
    B.draw_logo_image(c, W - MARGIN - 30, H - 43, 70)
    c.setFillColor(white)
    c.setFont(BOLD, 24)
    c.drawString(MARGIN, H - 50, 'Mi Cuaderno del Científico')
    c.setFont(FONT, 11)
    c.drawString(MARGIN, H - 72, 'Imprime una copia por experimento y piensa como un científico de verdad.')

    x = MARGIN
    w = W - 2 * MARGIN
    y = H - 116
    # cabecera de datos
    c.setFillColor(B.tint(B.CIENCIA, 0.9))
    c.roundRect(x, y - 64, w, 64, 8, fill=1, stroke=0)
    c.setFont(BOLD, 10)
    c.setFillColor(B.INK)
    c.drawString(x + 12, y - 18, 'Científico/a:')
    _wline(c, x + 90, y - 20, w - 110)
    c.drawString(x + 12, y - 40, 'Experimento n.º:')
    _wline(c, x + 110, y - 42, 70)
    c.drawString(x + 200, y - 40, 'Fecha:')
    _wline(c, x + 240, y - 42, 120)
    c.drawString(x + 12, y - 60, 'Título:')
    _wline(c, x + 60, y - 62, w - 80)
    y -= 80

    fields = [
        ('1', 'MI PREGUNTA', '¿Qué quiero descubrir?', 2, B.PURPLE),
        ('2', 'MI HIPÓTESIS', '¿Qué creo que pasará?', 2, B.INGEN),
        ('3', 'QUÉ USÉ', 'Materiales del experimento', 2, B.CIENCIA),
    ]
    for num, tit, hint, nlines, col in fields:
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
        for _ in range(nlines):
            _wline(c, x + 26, yy, w - 26)
            yy -= 18
        y = yy - 6

    # 4) Observación: caja de dibujo + lineas
    c.setFillColor(B.TECNO)
    c.circle(x + 10, y - 6, 9, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(BOLD, 10)
    c.drawCentredString(x + 10, y - 9.5, '4')
    c.setFillColor(B.TECNO)
    c.setFont(BOLD, 11)
    c.drawString(x + 26, y - 10, 'QUÉ OBSERVÉ')
    c.setFillColor(B.GREY)
    c.setFont(FONT, 9)
    c.drawString(x + 26 + pdfmetrics.stringWidth('QUÉ OBSERVÉ', BOLD, 11) + 8, y - 10, 'Dibújalo y descríbelo')
    boxw = 200
    boxh = 110
    by = y - 26 - boxh
    c.setStrokeColor(B.tint(B.TECNO, 0.4))
    c.setLineWidth(1.2)
    c.roundRect(x + 26, by, boxw, boxh, 8, fill=0, stroke=1)
    c.setFillColor(B.tint(B.TECNO, 0.6))
    c.setFont(FONT, 9)
    c.drawCentredString(x + 26 + boxw / 2, by + boxh / 2, '(tu dibujo)')
    lyy = y - 36
    for _ in range(5):
        _wline(c, x + 26 + boxw + 20, lyy, w - boxw - 46)
        lyy -= 18
    y = by - 14

    for num, tit, hint, col in [('5', 'MI CONCLUSIÓN', '¿Acerté? ¿Qué aprendí?', B.ARTE),
                                ('6', 'NUEVA PREGUNTA', '¿Qué me gustaría probar ahora?', B.FISICA)]:
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
        for _ in range(2):
            _wline(c, x + 26, yy, w - 26)
            yy -= 18
        y = yy - 6

    # valoración final
    c.setFillColor(B.tint(B.PURPLE, 0.9))
    c.roundRect(x, y - 40, w, 40, 8, fill=1, stroke=0)
    c.setFillColor(B.INK)
    c.setFont(BOLD, 10)
    c.drawString(x + 12, y - 25, 'Mi cara hoy:')
    # caritas
    fx = x + 90
    for mood in ('happy', 'neutral', 'wow'):
        c.setStrokeColor(B.PURPLE)
        c.setFillColor(white)
        c.setLineWidth(1.2)
        c.circle(fx, y - 20, 10, fill=1, stroke=1)
        c.setFillColor(B.PURPLE)
        c.circle(fx - 3.5, y - 18, 1.4, fill=1, stroke=0)
        c.circle(fx + 3.5, y - 18, 1.4, fill=1, stroke=0)
        c.setStrokeColor(B.PURPLE)
        c.setLineWidth(1.2)
        if mood == 'happy':
            c.arc(fx - 5, y - 27, fx + 5, y - 19, startAng=200, extent=140)
        elif mood == 'neutral':
            c.line(fx - 4, y - 24, fx + 4, y - 24)
        else:
            c.circle(fx, y - 24, 3, fill=0, stroke=1)
        fx += 28
    c.setFillColor(B.INK)
    c.setFont(BOLD, 10)
    c.drawString(fx + 10, y - 25, 'Estrellas:')
    sx = fx + 70
    for _ in range(5):
        _star(c, sx, y - 20, 8, B.YELLOW)
        sx += 22
    footer(c, page_no)
    c.showPage()


def _star(c, cx, cy, r, color):
    import math
    c.setFillColor(white)
    c.setStrokeColor(color)
    c.setLineWidth(1.2)
    path = c.beginPath()
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rad = r if i % 2 == 0 else r * 0.45
        px, py = cx + math.cos(ang) * rad, cy + math.sin(ang) * rad
        if i == 0:
            path.moveTo(px, py)
        else:
            path.lineTo(px, py)
    path.close()
    c.drawPath(path, fill=0, stroke=1)


def page_tangram(c, page_no):
    """Tangram vectorial geometricamente exacto, a escala real y recortable."""
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(B.MATES)
    c.rect(0, H - 86, W, 86, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(BOLD, 24)
    c.drawString(MARGIN, H - 50, 'Plantilla del Tangram')
    c.setFont(FONT, 11)
    c.drawString(MARGIN, H - 72, 'Para el experimento 17 · 7 piezas que forman un cuadrado')

    # --- geometria: cuadrado lado 4 -> 14 cm a escala 1:1 ---
    CM = 28.3464567
    side_cm = 14.0
    S = side_cm * CM                      # lado en puntos
    unit = S / 4.0
    ox = (W - S) / 2.0                    # origen x (centrado)
    oy = H - 86 - 40 - S                  # origen y

    def P(ux, uy):
        return (ox + ux * unit, oy + uy * unit)

    pieces = [
        ('1', [(0, 0), (4, 0), (2, 2)], B.tint(B.MATES, 0.55)),    # grande
        ('2', [(0, 0), (2, 2), (0, 4)], B.tint(B.MATES, 0.7)),     # grande
        ('3', [(4, 4), (4, 2), (2, 4)], B.tint(B.CIENCIA, 0.55)),  # mediano
        ('4', [(4, 2), (4, 0), (3, 1)], B.tint(B.INGEN, 0.5)),     # pequeno
        ('5', [(2, 4), (0, 4), (1, 3)], B.tint(B.INGEN, 0.5)),     # pequeno
        ('6', [(4, 2), (3, 1), (2, 2), (3, 3)], B.tint(B.FISICA, 0.45)),  # cuadrado
        ('7', [(3, 3), (2, 2), (1, 3), (2, 4)], B.tint(B.ARTE, 0.55)),    # romboide
    ]
    # relleno
    for _, pts, col in pieces:
        path = c.beginPath()
        x0, y0 = P(*pts[0])
        path.moveTo(x0, y0)
        for ux, uy in pts[1:]:
            path.lineTo(*P(ux, uy))
        path.close()
        c.setFillColor(col)
        c.drawPath(path, fill=1, stroke=0)
    # lineas de recorte (encima)
    c.setStrokeColor(B.INK)
    c.setLineWidth(1.4)
    c.setLineJoin(1)
    for _, pts, col in pieces:
        path = c.beginPath()
        x0, y0 = P(*pts[0])
        path.moveTo(x0, y0)
        for ux, uy in pts[1:]:
            path.lineTo(*P(ux, uy))
        path.close()
        c.drawPath(path, fill=0, stroke=1)
    # borde exterior mas grueso
    c.setLineWidth(2.4)
    c.rect(ox, oy, S, S, fill=0, stroke=1)
    # etiquetas (numero en el centroide)
    c.setFont(BOLD, 13)
    c.setFillColor(B.INK)
    for label, pts, _ in pieces:
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        px, py = P(cx, cy)
        c.drawCentredString(px, py - 4, label)
    # cota de escala
    c.setStrokeColor(B.MATES)
    c.setLineWidth(0.8)
    c.line(ox, oy - 12, ox + S, oy - 12)
    c.line(ox, oy - 16, ox, oy - 8)
    c.line(ox + S, oy - 16, ox + S, oy - 8)
    c.setFont(BOLD, 9)
    c.setFillColor(B.MATES)
    c.drawCentredString(ox + S / 2, oy - 24, '%.0f cm (imprime al 100%%, sin "ajustar a página")' % side_cm)

    # leyenda de piezas
    ly = oy - 48
    legend = [('1 y 2', 'triángulos grandes'), ('3', 'triángulo mediano'),
              ('4 y 5', 'triángulos pequeños'), ('6', 'cuadrado'),
              ('7', 'romboide (paralelogramo)')]
    c.setFont(FONT, 10)
    lx = MARGIN
    for num, desc in legend:
        c.setFillColor(B.MATES)
        c.setFont(BOLD, 10)
        c.drawString(lx, ly, num + ':')
        wnum = pdfmetrics.stringWidth(num + ': ', BOLD, 10)
        c.setFillColor(B.INK)
        c.setFont(FONT, 10)
        c.drawString(lx + wnum, ly, desc)
        lx += wnum + pdfmetrics.stringWidth(desc, FONT, 10) + 18
        if lx > W - 160:
            lx = MARGIN
            ly -= 16
    c.setFont(FONT, 9.5)
    c.setFillColor(B.GREY)
    c.drawString(MARGIN, ly - 18, 'Consejo: pega esta hoja sobre cartulina antes de recortar para que las piezas duren.')
    footer(c, page_no)
    c.showPage()


def page_diploma(c, page_no):
    c.setFillColor(B.tint(B.PURPLE, 0.9))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    B.draw_doodles(c, W, H, color=B.PURPLE)
    # marco doble
    m = 60
    c.setStrokeColor(B.PURPLE)
    c.setLineWidth(6)
    c.roundRect(m, m, W - 2 * m, H - 2 * m, 18, fill=0, stroke=1)
    c.setStrokeColor(B.YELLOW)
    c.setLineWidth(2)
    c.roundRect(m + 10, m + 10, W - 2 * m - 20, H - 2 * m - 20, 14, fill=0, stroke=1)
    B.draw_logo_image(c, W / 2, H - 150, 120)
    c.setFillColor(B.PURPLE)
    c.setFont(BOLD, 30)
    c.drawCentredString(W / 2, H - 230, 'DIPLOMA DE')
    c.setFont(BOLD, 36)
    c.setFillColor(B.MAGENTA)
    c.drawCentredString(W / 2, H - 272, 'CIENTÍFICO/A DIVERGENTE')
    c.setFillColor(B.INK)
    c.setFont(FONT, 14)
    c.drawCentredString(W / 2, H - 320, 'Se otorga con orgullo a:')
    c.setStrokeColor(B.PURPLE)
    c.setLineWidth(1.2)
    c.line(W / 2 - 180, H - 360, W / 2 + 180, H - 360)
    para(c, 'por su curiosidad sin límites, sus preguntas valientes y por demostrar que',
         W / 2 - 200, H - 392, 400, FONT, 13, 18, B.INK, align='center')
    c.setFont(BOLD, 22)
    c.setFillColor(B.PURPLE)
    c.drawCentredString(W / 2, H - 430, '¡APRENDER ES DIVERTIDO!')
    c.setFont(FONT, 13)
    c.setFillColor(B.INK)
    c.drawCentredString(W / 2, H - 470, 'Experimentos completados: ______ / 20')
    c.drawString(W / 2 - 180, H - 520, 'Fecha: ____ / ____ / ______')
    c.drawString(W / 2 + 10, H - 520, 'Firma jefe de laboratorio:')
    c.line(W / 2 + 10, H - 540, W / 2 + 180, H - 540)
    B.draw_logo(c, W / 2 - 70, m + 24, size=18, tagline=False)
    footer(c, page_no)
    c.showPage()


def page_back(c, page_no):
    c.setFillColor(B.PURPLE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    B.draw_doodles(c, W, H, color=white)
    B.draw_logo_image(c, W / 2, H * 0.76, 130)
    c.setFillColor(white)
    c.setFont(BOLD, 30)
    c.drawCentredString(W / 2, H * 0.58, '¿Te has quedado con ganas')
    c.drawCentredString(W / 2, H * 0.58 - 38, 'de más ciencia?')
    para(c, 'Esto es solo el principio. En divergenios.com te esperan más retos de '
         'ingeniería, robótica sin pantallas, experimentos nuevos cada mes y un montón '
         'de ideas para seguir siendo un científico divergente.',
         W / 2 - 220, H * 0.44, 440, FONT, 13, 19, white, align='center')
    # CTA pills
    ctas = ['Retos de Ingeniería Divergente', 'Club Divergente · novedades cada mes',
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
    c.setFillColor(B.tint(B.PURPLE, 0.5))
    c.drawCentredString(W / 2, 40, '© divergenios.com · Uso personal y de aula. Prohibida su reventa o redistribución.')
    c.showPage()





def build(experiments, outfile, subset=None, lead_magnet=False):
    c = canvas.Canvas(outfile, pagesize=A4)
    c.setTitle('Laboratorio Divergente en Casa' + (' — Muestra gratis' if lead_magnet else ''))
    c.setAuthor('divergenios.com')
    c.setSubject('20 experimentos STEAM para 6-10 años')

    dests = {e['n']: 'exp%d' % e['n'] for e in experiments}
    page_cover(c)
    page_welcome(c)
    page_safety(c)
    exps = experiments if subset is None else [e for e in experiments if e['n'] in subset]
    if not lead_magnet:
        page_index(c, experiments, dests)
        pno = 5
    else:
        pno = 4
    for e in exps:
        page_experiment(c, e, pno, dests[e['n']])
        pno += 1
    if not lead_magnet:
        page_notebook(c, pno)
        pno += 1
        page_tangram(c, pno)
        pno += 1
        page_diploma(c, pno)
        pno += 1
    page_back(c, pno)
    c.save()
    return pno


def main():
    exps = parse_experiments(SRC)
    assert len(exps) == 20, 'Se esperaban 20 experimentos, hay %d' % len(exps)
    full = os.path.join(OUTDIR, 'Laboratorio-Divergente-en-Casa.pdf')
    lead = os.path.join(OUTDIR, 'Lead-Magnet-3-Experimentos.pdf')
    n1 = build(exps, full)
    n2 = build(exps, lead, subset={1, 9, 19}, lead_magnet=True)
    print('OK  %-46s  %2d páginas' % (os.path.basename(full), n1))
    print('OK  %-46s  %2d páginas' % (os.path.basename(lead), n2))


if __name__ == '__main__':
    main()
