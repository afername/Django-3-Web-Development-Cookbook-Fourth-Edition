# -*- coding: utf-8 -*-
"""
Identidad de marca recreada de divergenios.com para maquetar los PDF.

NOTA: la politica de red del entorno bloquea divergenios.com, asi que NO fue
posible descargar el PNG oficial del logo. Este modulo recrea un wordmark y una
mascota ("divergenio") vectoriales coherentes con la marca (STEAM, alegre,
"aprender es divertido"). Para usar el logo oficial, sustituye draw_logo() por
una imagen: c.drawImage('logo-oficial.png', x, y, width=..., preserveAspectRatio=True, mask='auto').
"""
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader
import os

# ---- Paleta OFICIAL (muestreada del logo de divergenios.com) ----
INK      = HexColor('#2A2A3C')   # texto principal
BLUE     = HexColor('#2AB3F0')   # azul bombilla (primario de marca)
BLUE_D   = HexColor('#1E8FCB')
PURPLE   = HexColor('#5512DE')   # violeta de los ojos (secundario)
PURPLE_D = HexColor('#3A0BA3')
MAGENTA  = HexColor('#C45FE0')   # magenta de pupilas/brazos (acento)
YELLOW   = HexColor('#FFC53D')   # acento cálido puntual
CREAM    = HexColor('#FFF7E6')

# Colores por area STEAM
CIENCIA  = HexColor('#0FA39A')   # teal
TECNO    = HexColor('#2AB3F0')   # azul (marca)
INGEN    = HexColor('#F6772E')   # naranja
ARTE     = HexColor('#C45FE0')   # magenta (marca)
MATES    = HexColor('#5512DE')   # violeta (marca)
FISICA   = HexColor('#F4B400')   # ambar
GREY     = HexColor('#8A8AA0')
LIGHT    = HexColor('#EEF0FB')   # fondo lila-azulado muy claro

FONT  = 'DV'
BOLD  = 'DVB'

# ---- logo oficial (imagen) ----
_LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'divergenios-logo.png')
LOGO = ImageReader(_LOGO_PATH) if os.path.exists(_LOGO_PATH) else None
LOGO_AR = 321.0 / 427.0   # ancho / alto

AREA_COLORS = {
    'ciencia': CIENCIA, 'quimica': CIENCIA, 'biologia': CIENCIA,
    'tecnologia': TECNO, 'ingenieria': INGEN, 'arte': ARTE,
    'matematicas': MATES, 'fisica': FISICA,
}


def draw_logo_image(c, cx, cy, h):
    """Dibuja el logo oficial (mascota) centrado en (cx, cy) con altura h."""
    if LOGO is None:
        draw_mascot(c, cx, cy, h / 2.4)
        return
    w = h * LOGO_AR
    c.drawImage(LOGO, cx - w / 2, cy - h / 2, width=w, height=h,
                preserveAspectRatio=True, mask='auto')


def _tint(color, t):
    """Mezcla color con blanco. t=0 -> color, t=1 -> blanco."""
    r = color.red + (1 - color.red) * t
    g = color.green + (1 - color.green) * t
    b = color.blue + (1 - color.blue) * t
    return HexColor('#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255)))


tint = _tint


def draw_bulb(c, cx, cy, R, body=YELLOW, ray=True):
    """Bombilla-idea simple (icono)."""
    c.saveState()
    if ray:
        c.setStrokeColor(_tint(body, 0.1))
        c.setLineWidth(R * 0.16)
        for ang in (90, 140, 40):
            import math
            a = math.radians(ang)
            c.line(cx + math.cos(a) * R * 1.25, cy + math.sin(a) * R * 1.25,
                   cx + math.cos(a) * R * 1.7, cy + math.sin(a) * R * 1.7)
    c.setFillColor(body)
    c.circle(cx, cy, R, fill=1, stroke=0)
    # casquillo
    c.setFillColor(HexColor('#C9C9D4'))
    c.roundRect(cx - R * 0.45, cy - R * 1.45, R * 0.9, R * 0.55, R * 0.12, fill=1, stroke=0)
    c.restoreState()


def draw_mascot(c, cx, cy, R, body=PURPLE):
    """El 'divergenio': bombilla-genio con cara curiosa."""
    c.saveState()
    # rayos de idea
    import math
    c.setStrokeColor(YELLOW)
    c.setLineWidth(R * 0.14)
    for ang in (60, 90, 120):
        a = math.radians(ang)
        c.line(cx + math.cos(a) * R * 1.12, cy + math.sin(a) * R * 1.12,
               cx + math.cos(a) * R * 1.5, cy + math.sin(a) * R * 1.5)
    # cuerpo (bombilla)
    c.setFillColor(body)
    c.circle(cx, cy, R, fill=1, stroke=0)
    # casquillo
    c.setFillColor(HexColor('#C9C9D4'))
    bw, bh = R * 0.95, R * 0.5
    c.roundRect(cx - bw / 2, cy - R - bh * 0.55, bw, bh, R * 0.1, fill=1, stroke=0)
    c.setStrokeColor(_tint(body, 0.4))
    c.setLineWidth(R * 0.06)
    for i in range(3):
        yy = cy - R - bh * 0.55 + bh * (0.25 + i * 0.28)
        c.line(cx - bw / 2, yy, cx + bw / 2, yy)
    # mejillas
    c.setFillColor(_tint(ARTE, 0.35))
    c.circle(cx - R * 0.5, cy - R * 0.12, R * 0.16, fill=1, stroke=0)
    c.circle(cx + R * 0.5, cy - R * 0.12, R * 0.16, fill=1, stroke=0)
    # ojos
    ex, ey, er = R * 0.34, cy + R * 0.18, R * 0.24
    c.setFillColor(white)
    c.circle(cx - ex, ey, er, fill=1, stroke=0)
    c.circle(cx + ex, ey, er, fill=1, stroke=0)
    c.setFillColor(INK)
    c.circle(cx - ex + er * 0.18, ey + er * 0.05, er * 0.5, fill=1, stroke=0)
    c.circle(cx + ex + er * 0.18, ey + er * 0.05, er * 0.5, fill=1, stroke=0)
    c.setFillColor(white)
    c.circle(cx - ex + er * 0.35, ey + er * 0.25, er * 0.18, fill=1, stroke=0)
    c.circle(cx + ex + er * 0.35, ey + er * 0.25, er * 0.18, fill=1, stroke=0)
    # sonrisa
    c.setStrokeColor(white)
    c.setLineWidth(R * 0.13)
    c.setLineCap(1)
    c.arc(cx - R * 0.42, cy - R * 0.55, cx + R * 0.42, cy + R * 0.05, startAng=205, extent=130)
    c.restoreState()


def draw_logo(c, x, y, size=22, dark=False, tagline=False):
    """Wordmark 'divergenios' + mascota oficial. (x,y)=base izquierda del texto."""
    c.saveState()
    base = INK if not dark else white
    accent = MAGENTA
    # mascota oficial a la izquierda
    ih = size * 1.6
    draw_logo_image(c, x + ih * LOGO_AR / 2, y + size * 0.32, ih)
    tx = x + ih * LOGO_AR + size * 0.35
    c.setFont(BOLD, size)
    c.setFillColor(base)
    c.drawString(tx, y, 'diver')
    w1 = stringWidth('diver', BOLD, size)
    c.setFillColor(accent)
    c.drawString(tx + w1, y, 'genios')
    if tagline:
        c.setFont(FONT, size * 0.42)
        c.setFillColor(BLUE if not dark else white)
        c.drawString(tx, y - size * 0.5, 'aprender es divertido')
    c.restoreState()
    return tx + w1 + stringWidth('genios', BOLD, size)


def draw_atom(c, cx, cy, R, color, lw=1.4):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.ellipse(cx - R, cy - R * 0.4, cx + R, cy + R * 0.4, stroke=1, fill=0)
    for ang in (60, 120):
        c.saveState()
        c.translate(cx, cy)
        c.rotate(ang)
        c.ellipse(-R, -R * 0.4, R, R * 0.4, stroke=1, fill=0)
        c.restoreState()
    c.setFillColor(color)
    c.circle(cx, cy, R * 0.16, fill=1, stroke=0)
    c.restoreState()


def draw_doodles(c, W, H, color=PURPLE):
    """Motivos STEAM tenues de fondo."""
    import math
    c.saveState()
    faint = _tint(color, 0.86)
    faint2 = _tint(YELLOW, 0.8)
    draw_atom(c, W * 0.12, H * 0.82, 26, faint, lw=2)
    draw_atom(c, W * 0.88, H * 0.2, 30, _tint(CIENCIA, 0.82), lw=2)
    # triangulo (ingenieria)
    c.setStrokeColor(faint2)
    c.setLineWidth(3)
    pts = [(W * 0.9, H * 0.85), (W * 0.82, H * 0.78), (W * 0.98, H * 0.78)]
    c.lines([(pts[0][0], pts[0][1], pts[1][0], pts[1][1]),
             (pts[1][0], pts[1][1], pts[2][0], pts[2][1]),
             (pts[2][0], pts[2][1], pts[0][0], pts[0][1])])
    # zig-zag (datos)
    c.setStrokeColor(_tint(ARTE, 0.82))
    c.setLineWidth(2.5)
    zx, zy = W * 0.06, H * 0.2
    seg = []
    for i in range(6):
        seg.append((zx + i * 12, zy + (8 if i % 2 == 0 else -8),
                    zx + (i + 1) * 12, zy + (8 if (i + 1) % 2 == 0 else -8)))
    c.lines(seg)
    # puntos
    for (px, py, col) in [(0.2, 0.3, MATES), (0.78, 0.7, FISICA), (0.5, 0.9, CIENCIA),
                          (0.3, 0.6, INGEN), (0.7, 0.4, ARTE)]:
        c.setFillColor(_tint(col, 0.78))
        c.circle(W * px, H * py, 5, fill=1, stroke=0)
    c.restoreState()
