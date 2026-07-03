# -*- coding: utf-8 -*-
"""
Maqueta el 'Pack Aula' de Laboratorio Divergenio: edición docente con guía,
rúbrica, póster A3 y licencia de centro. Complementa al producto base (20
experimentos); juntos forman el Pack Aula multi-alumno.
Genera: Pack-Aula-Laboratorio-Divergenio.pdf
Uso:  python3 build_pack_aula.py
"""
import os
import sys

from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.lib.colors import white
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand as B
import build_lab_pdf as L

W, H, MARGIN = L.W, L.H, L.MARGIN
FONT, BOLD = L.FONT, L.BOLD
para, para_h = L.para, L.para_h

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, '..', '01-laboratorio-divergenio-en-casa')
LICENSE = 'Licencia de centro · uso multi-alumno · Prohibida su reventa'


def footer(c, page_no, w=W):
    c.saveState()
    c.setStrokeColor(B.tint(B.PURPLE, 0.8))
    c.setLineWidth(0.7)
    c.line(MARGIN, 40, w - MARGIN, 40)
    B.draw_logo_image(c, MARGIN + 7, 28, 17)
    c.setFont(BOLD, 8)
    c.setFillColor(B.INK)
    c.drawString(MARGIN + 20, 25, 'divergenios.com')
    c.setFont(FONT, 7.5)
    c.setFillColor(B.GREY)
    c.drawCentredString(w / 2, 25, LICENSE)
    c.setFont(BOLD, 8)
    c.setFillColor(B.PURPLE)
    c.drawRightString(w - MARGIN, 25, str(page_no))
    c.restoreState()


def header(c, title, subtitle, color=B.PURPLE):
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(color)
    c.rect(0, H - 92, W, 92, fill=1, stroke=0)
    B.draw_logo_image(c, W - MARGIN - 30, H - 46, 70)
    c.setFillColor(white)
    c.setFont(BOLD, 24)
    c.drawString(MARGIN, H - 52, title)
    if subtitle:
        c.setFont(FONT, 11)
        c.drawString(MARGIN, H - 74, subtitle)


def draw_table(c, x, y, widths, rows, header_color, font_size=9.5, header_white=True,
               fill_first_col=None):
    """Dibuja una tabla con ajuste de texto por celda. rows[0] es cabecera. Devuelve y final."""
    pad = 6
    lead = font_size + 3
    for ri, row in enumerate(rows):
        # alto de fila (mide con la MISMA fuente con la que se dibujará la celda)
        def cell_font(ci):
            return BOLD if (ri == 0 or (fill_first_col is not None and ci == 0)) else FONT
        cell_lines = []
        for ci, cell in enumerate(row):
            lines = simpleSplit(str(cell), cell_font(ci), font_size, widths[ci] - 2 * pad)
            cell_lines.append(lines)
        rh = max(1, max(len(cl) for cl in cell_lines)) * lead + 2 * pad - 3
        # fondo
        cx = x
        for ci, cell in enumerate(row):
            if ri == 0:
                c.setFillColor(header_color)
            elif fill_first_col is not None and ci == 0:
                c.setFillColor(B.tint(header_color, 0.85))
            else:
                c.setFillColor(white if ri % 2 else B.tint(header_color, 0.95))
            c.rect(cx, y - rh, widths[ci], rh, fill=1, stroke=0)
            c.setStrokeColor(B.tint(header_color, 0.6))
            c.setLineWidth(0.5)
            c.rect(cx, y - rh, widths[ci], rh, fill=0, stroke=1)
            # texto
            f = BOLD if (ri == 0 or (fill_first_col is not None and ci == 0)) else FONT
            tcol = white if (ri == 0 and header_white) else B.INK
            c.setFont(f, font_size)
            c.setFillColor(tcol)
            ty = y - pad - font_size + 2
            for ln in cell_lines[ci]:
                c.drawString(cx + pad, ty, ln)
                ty -= lead
            cx += widths[ci]
        y -= rh
    return y


# ============================================================
# PÁGINAS
# ============================================================
def page_cover(c):
    c.setFillColor(B.PURPLE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(B.PURPLE_D)
    c.rect(0, H * 0.6, W, H * 0.4, fill=1, stroke=0)
    B.draw_doodles(c, W, H, color=white)
    B.draw_logo_image(c, W / 2, H * 0.74, 140)
    # badge edición aula
    c.setFillColor(B.MAGENTA)
    c.roundRect(W / 2 - 95, H * 0.6 - 6, 190, 32, 16, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(BOLD, 15)
    c.drawCentredString(W / 2, H * 0.6 + 3, 'EDICIÓN AULA')
    c.setFillColor(white)
    c.setFont(BOLD, 40)
    c.drawCentredString(W / 2, H * 0.48, 'Laboratorio')
    c.drawCentredString(W / 2, H * 0.48 - 44, 'Divergenio')
    c.setFont(BOLD, 20)
    c.setFillColor(B.BLUE)
    c.drawCentredString(W / 2, H * 0.48 - 78, 'Guía del docente')
    para(c, 'Método, alineación curricular (LOMLOE), rúbrica de evaluación, plan de '
         'sesión, póster A3 para el aula y licencia de centro.',
         W / 2 - 210, H * 0.3, 420, FONT, 12, 17, white, align='center')
    c.setFont(FONT, 11)
    c.setFillColor(B.tint(white, 0))
    c.setFillColor(white)
    c.drawCentredString(W / 2, H * 0.14, 'Complemento de "Laboratorio Divergenio en Casa" · 20 experimentos')
    c.setFont(BOLD, 16)
    c.drawCentredString(W / 2, H * 0.1, 'divergenios.com')
    c.showPage()


def page_method(c):
    header(c, 'Tu papel no es enseñar: es preguntar', 'Cómo facilitar STEAM sin dar la respuesta')
    y = H - 118
    intro = ('El mayor error de un adulto en STEAM es dar la respuesta demasiado pronto. La '
             'ciencia se aprende equivocándose y preguntando. Resiste la tentación de explicar '
             'antes de que prueben (primero hacen, luego entienden), devuelve la pregunta '
             '("¿tú qué crees?"), valida el error ("¡qué interesante! ¿qué pudo pasar?") y '
             'nombra la ciencia al final, cuando ya la han vivido: es cuando se fija.')
    y = para(c, intro, MARGIN, y, W - 2 * MARGIN, FONT, 11.5, 16, B.INK) - 18
    c.setFont(BOLD, 16)
    c.setFillColor(B.PURPLE)
    c.drawString(MARGIN, y, 'El método de las 4 preguntas')
    c.setFont(FONT, 11)
    c.setFillColor(B.GREY)
    y -= 18
    c.drawString(MARGIN, y, 'Úsalo en CUALQUIER experimento. Estas 4 preguntas son lo que desarrolla el pensamiento científico.')
    y -= 22
    qs = [
        ('ANTES', 'Predice', '"¿Qué crees que va a pasar? ¿Por qué?"', B.INGEN),
        ('DURANTE', 'Observa', '"¿Qué estás viendo? Descríbelo con detalle."', B.BLUE),
        ('DESPUÉS', 'Explica', '"¿Por qué crees que pasó eso?"', B.CIENCIA),
        ('MÁS ALLÁ', 'Transfiere', '"¿Dónde más has visto algo parecido?"', B.MATES),
    ]
    bw = (W - 2 * MARGIN - 3 * 14) / 4
    for i, (tag, tit, q, col) in enumerate(qs):
        bx = MARGIN + i * (bw + 14)
        c.setFillColor(B.tint(col, 0.88))
        c.roundRect(bx, y - 150, bw, 150, 10, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(bx, y - 28, bw, 28, 10, fill=1, stroke=0)
        c.rect(bx, y - 28, bw, 14, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(BOLD, 11)
        c.drawCentredString(bx + bw / 2, y - 19, tag)
        c.setFillColor(col)
        c.setFont(BOLD, 14)
        c.drawCentredString(bx + bw / 2, y - 52, tit)
        para(c, q, bx + 10, y - 78, bw - 20, FONT, 10.5, 14, B.INK, align='center')
    y -= 168
    # sesión 50 min
    c.setFont(BOLD, 16)
    c.setFillColor(B.PURPLE)
    c.drawString(MARGIN, y, 'Una sesión de 50 minutos en clase')
    y -= 22
    steps = [('5 min', 'Pregunta motivadora + predicción'),
             ('10 min', 'Montaje en grupos de 3-4 (jefe de material, anotador, científico jefe, comunicador)'),
             ('15 min', 'Experimentación'),
             ('10 min', 'Rellenar el Cuaderno del Científico'),
             ('10 min', 'Puesta en común: cada grupo explica su "porqué" y su reto')]
    for t, d in steps:
        c.setFillColor(B.MATES)
        c.roundRect(MARGIN, y - 15, 52, 17, 8, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(BOLD, 9)
        c.drawCentredString(MARGIN + 26, y - 11, t)
        c.setFillColor(B.INK)
        c.setFont(FONT, 10.5)
        para(c, d, MARGIN + 62, y - 11, W - 2 * MARGIN - 62, FONT, 10.5, 13, B.INK)
        y -= 22
    footer(c, 2)
    c.showPage()


def page_curriculum(c):
    header(c, 'Alineación curricular (LOMLOE)', 'Para justificar el uso en clase y en programaciones', B.CIENCIA)
    y = H - 116
    c.setFont(FONT, 10.5)
    c.setFillColor(B.INK)
    y = para(c, 'Mapa orientativo. Etapas: Infantil (5 años) y Primaria (1.º-4.º). Adapta la cita a '
             'la normativa autonómica del centro; para LATAM, mapea contra competencias STEM/indagación.',
             MARGIN, y, W - 2 * MARGIN, FONT, 10.5, 14, B.INK) - 14
    rows = [
        ['Experimentos', 'Área / Materia', 'Saberes y competencias que trabaja'],
        ['1, 2, 3, 6, 13', 'C. del Medio Natural', 'Materia y sus cambios; reacciones; observación científica.'],
        ['4, 5, 18', 'C. del Medio Natural', 'Mezclas y separación; propiedades de la materia (densidad).'],
        ['7, 8', 'Competencia Digital (unplugged)', 'Algoritmos, secuencias, descomposición y representación de datos sin dispositivos.'],
        ['9, 10, 11, 12', 'E. Artística / Medio Natural', 'Diseño y construcción; fuerzas y estructuras; resolución de problemas.'],
        ['14, 17', 'Matemáticas / E. Artística', 'Geometría, simetría, figuras planas y composición.'],
        ['15, 16', 'Matemáticas', 'Patrones y secuencias; iniciación a la probabilidad y a los datos.'],
        ['19, 20', 'C. del Medio Natural', 'Fenómenos físicos: electricidad estática y magnetismo.'],
        ['Todos', 'Competencia STEM + Aprender a aprender', 'Método científico: pregunta, hipótesis, observación, conclusión.'],
    ]
    widths = [88, 150, W - 2 * MARGIN - 88 - 150]
    y = draw_table(c, MARGIN, y, widths, rows, B.CIENCIA, font_size=9.3, fill_first_col=True) - 18
    # combos
    c.setFont(BOLD, 14)
    c.setFillColor(B.CIENCIA)
    c.drawString(MARGIN, y, 'Combos recomendados por sesión (mismo material, sube la dificultad)')
    y -= 20
    for d in ['Reacciones: 1 → 6 (ambos producen CO₂)', 'Densidad: 13 → 18',
              'Estructuras: 10 → 9 → 11', 'Pensamiento computacional: 7 → 8']:
        c.setFillColor(B.CIENCIA)
        c.circle(MARGIN + 4, y + 3, 3, fill=1, stroke=0)
        c.setFillColor(B.INK)
        c.setFont(FONT, 10.5)
        c.drawString(MARGIN + 16, y, d)
        y -= 16
    footer(c, 3)
    c.showPage()


def page_rubric(c):
    header(c, 'Rúbrica de observación', 'Evalúa el proceso, no el resultado', B.INGEN)
    y = H - 116
    c.setFont(FONT, 10.5)
    c.setFillColor(B.INK)
    y = para(c, 'Marca una casilla por alumno o grupo en cada indicador. Mide cómo piensan y '
             'colaboran, no si el experimento "salió".', MARGIN, y, W - 2 * MARGIN, FONT, 10.5, 14, B.INK) - 12
    rows = [
        ['Indicador', 'En camino', 'Lo hace', 'Lo domina'],
        ['Formula una predicción antes de actuar', '', '', ''],
        ['Observa y describe con detalle', '', '', ''],
        ['Relaciona el resultado con un "porqué"', '', '', ''],
        ['Propone una nueva pregunta o variación', '', '', ''],
        ['Colabora y respeta el turno y el material', '', '', ''],
    ]
    cw = (W - 2 * MARGIN - 230) / 3
    widths = [230, cw, cw, cw]
    y = draw_table(c, MARGIN, y, widths, rows, B.INGEN, font_size=10, fill_first_col=True) - 24

    c.setFont(BOLD, 15)
    c.setFillColor(B.INGEN)
    c.drawString(MARGIN, y, 'Diferenciación por nivel')
    y -= 22
    diffs = [
        ('Más pequeños (5-6)', 'Céntrate en observar y describir; el adulto lee los pasos.', B.CIENCIA),
        ('Listos para más (8-10)', 'Que midan, anoten datos y repitan cambiando UNA variable.', B.BLUE),
        ('Muy motivados', 'Convierte el "reto divergenio" en un mini-proyecto de varios días.', B.MATES),
    ]
    for tit, d, col in diffs:
        c.setFillColor(B.tint(col, 0.9))
        c.roundRect(MARGIN, y - 44, W - 2 * MARGIN, 44, 8, fill=1, stroke=0)
        c.setFillColor(col)
        c.setFont(BOLD, 11.5)
        c.drawString(MARGIN + 14, y - 18, tit)
        c.setFillColor(B.INK)
        c.setFont(FONT, 10.5)
        para(c, d, MARGIN + 14, y - 34, W - 2 * MARGIN - 28, FONT, 10.5, 13, B.INK)
        y -= 54

    # seguridad por experimento
    y -= 6
    c.setFont(BOLD, 15)
    c.setFillColor(B.INGEN)
    c.drawString(MARGIN, y, 'Notas de seguridad por experimento')
    y -= 18
    srows = [
        ['Exp.', 'A vigilar'],
        ['3, 5', 'Agua caliente la manipula el adulto. Dejar enfriar antes de dar a los niños.'],
        ['6, 13', 'Nada se prueba ni se bebe. Tirar a desagüe con agua abundante.'],
        ['11', 'Lanzar solo objetos blandos (papel/pompón), nunca hacia la cara.'],
        ['18, 20', 'El alcohol y la aguja solo los maneja el adulto; cuidado con pinchazos y fuego.'],
    ]
    draw_table(c, MARGIN, y, [60, W - 2 * MARGIN - 60], srows, B.RED if hasattr(B, 'RED') else B.INGEN,
               font_size=9.3, fill_first_col=True)
    footer(c, 4)
    c.showPage()


def page_poster_a3(c):
    PW, PH = landscape(A3)        # 1191 x 842
    c.setPageSize((PW, PH))
    c.setFillColor(B.PURPLE)
    c.rect(0, 0, PW, PH, fill=1, stroke=0)
    c.setFillColor(B.PURPLE_D)
    c.rect(0, PH - 150, PW, 150, fill=1, stroke=0)
    B.draw_doodles(c, PW, PH, color=white)
    B.draw_logo_image(c, 110, PH - 75, 110)
    c.setFillColor(white)
    c.setFont(BOLD, 46)
    c.drawString(200, PH - 78, 'El método de las 4 preguntas')
    c.setFillColor(B.BLUE)
    c.setFont(FONT, 20)
    c.drawString(200, PH - 116, 'Cuélgalo en el aula · funciona con CUALQUIER experimento')
    qs = [
        ('1 · ANTES', 'Predice', '¿Qué crees que va\na pasar? ¿Por qué?', B.INGEN),
        ('2 · DURANTE', 'Observa', '¿Qué estás viendo?\nDescríbelo con detalle.', B.BLUE),
        ('3 · DESPUÉS', 'Explica', '¿Por qué crees\nque pasó eso?', B.CIENCIA),
        ('4 · MÁS ALLÁ', 'Transfiere', '¿Dónde más has visto\nalgo parecido?', B.MATES),
    ]
    m = 70
    gap = 30
    bw = (PW - 2 * m - 3 * gap) / 4
    bh = 430
    top = PH - 210
    for i, (tag, tit, q, col) in enumerate(qs):
        bx = m + i * (bw + gap)
        c.setFillColor(white)
        c.roundRect(bx, top - bh, bw, bh, 20, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(bx, top - 70, bw, 70, 20, fill=1, stroke=0)
        c.rect(bx, top - 70, bw, 35, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(BOLD, 22)
        c.drawCentredString(bx + bw / 2, top - 46, tag)
        c.setFillColor(col)
        c.circle(bx + bw / 2, top - 150, 46, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(BOLD, 40)
        c.drawCentredString(bx + bw / 2, top - 165, str(i + 1))
        c.setFillColor(col)
        c.setFont(BOLD, 30)
        c.drawCentredString(bx + bw / 2, top - 235, tit)
        c.setFillColor(B.INK)
        c.setFont(FONT, 18)
        yy = top - 290
        for ln in q.split('\n'):
            c.drawCentredString(bx + bw / 2, yy, ln)
            yy -= 26
    c.setFillColor(white)
    c.setFont(BOLD, 20)
    c.drawCentredString(PW / 2, 46, 'divergenios.com · aprender es divertido')
    c.showPage()
    c.setPageSize(A4)


def page_license(c):
    c.setFillColor(B.PURPLE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    B.draw_doodles(c, W, H, color=white)
    B.draw_logo_image(c, W / 2, H * 0.78, 120)
    c.setFillColor(white)
    c.setFont(BOLD, 30)
    c.drawCentredString(W / 2, H * 0.6, 'Licencia de centro')
    para(c, 'Esta Edición Aula autoriza el uso del material por parte del centro educativo '
         'comprador: el profesorado puede imprimir, fotocopiar y proyectar las páginas para '
         'sus grupos de alumnos tantas veces como necesite, dentro del centro.',
         W / 2 - 230, H * 0.5, 460, FONT, 13, 19, white, align='center')
    items = ['Uso multi-alumno dentro del centro comprador',
             'Imprimir, fotocopiar y proyectar para tus clases',
             'Incluye diplomas para todo el grupo',
             'Prohibida la reventa, redistribución o publicación del archivo']
    yy = H * 0.4
    for it in items:
        c.setFillColor(B.BLUE)
        c.circle(W / 2 - 150, yy + 4, 6, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(FONT, 12.5)
        c.drawString(W / 2 - 132, yy, it)
        yy -= 30
    c.setFont(FONT, 11)
    c.setFillColor(white)
    para(c, 'Para equipar a otro centro o a más profesorado externo, adquiere una licencia '
         'adicional. Gracias por apoyar el aprendizaje divergenio.',
         W / 2 - 220, H * 0.22, 440, FONT, 11, 16, white, align='center')
    c.setFont(BOLD, 18)
    c.drawCentredString(W / 2, H * 0.12, 'divergenios.com')
    c.showPage()


def main():
    out = os.path.join(OUTDIR, 'Pack-Aula-Laboratorio-Divergenio.pdf')
    c = canvas.Canvas(out, pagesize=A4)
    c.setTitle('Laboratorio Divergenio · Edición Aula (Guía del docente)')
    c.setAuthor('divergenios.com')
    c.setSubject('Guía docente, rúbrica, póster A3 y licencia de centro')
    page_cover(c)
    page_method(c)
    page_curriculum(c)
    page_rubric(c)
    page_poster_a3(c)
    page_license(c)
    c.save()
    print('OK  %-46s  %d páginas' % (os.path.basename(out), 6))


if __name__ == '__main__':
    main()
