# 🎨 Maquetación — resultado

El contenido de `PRODUCTO.md` ya está **maquetado en PDF** con la identidad visual
de Divergenios. Los archivos se generan con un script (no a mano), así que si
editas el texto fuente puedes regenerarlos en segundos.

## Entregables generados

| Archivo | Qué es | Páginas |
|---------|--------|--------:|
| `Laboratorio-Divergente-en-Casa.pdf` | Producto completo, listo para vender | 28 |
| `Lead-Magnet-3-Experimentos.pdf` | Muestra gratis (exp. 1, 9 y 19) para captación | 7 |

Incluye: portada, carta de bienvenida, póster de seguridad, **índice clicable**,
los 20 experimentos (uno por página, codificados por color según el área STEAM),
**Cuaderno del Científico** (formulario imprimible), **Tangram vectorial a escala
real (14 cm) y recortable**, **Diploma** y contraportada con CTA.

## Identidad de marca

- **Paleta STEAM** alegre (violeta primario + acentos por área) sobre mucho blanco.
- **Wordmark** "diver**genios**" y **mascota "divergenio"** (bombilla-genio) vectoriales.
- Pie de marca, leyenda de iconos y nota de licencia en cada página.
- Diseñado para leerse bien también en **blanco y negro** (tintas suaves).

> ⚠️ **Sobre el logo oficial:** la política de red del entorno bloquea el acceso a
> `divergenios.com`, así que **no se pudo descargar el PNG oficial del logo**. Se
> recreó un wordmark + mascota coherentes con la marca. Para usar el logo oficial,
> sustitúyelo en `tools/brand.py` → `draw_logo()` por una imagen:
> `c.drawImage('logo-oficial.png', x, y, width=..., preserveAspectRatio=True, mask='auto')`.
> Lo mismo aplica a la paleta exacta (ajustable en la cabecera de `tools/brand.py`).

## Cómo regenerar

```bash
cd divergenios-productos-digitales/tools
pip install reportlab          # única dependencia
python3 build_lab_pdf.py       # escribe los 2 PDF en esta carpeta
```

- `tools/brand.py` — paleta, wordmark, mascota y motivos (un solo sitio para retocar la marca).
- `tools/build_lab_pdf.py` — parsea `PRODUCTO.md` y maqueta las páginas.

## Pendiente (opcional, antes de publicar)

- [ ] Sustituir el logo recreado por el **PNG/SVG oficial** de divergenios.com.
- [ ] Generar 3-4 **mockups** para la tienda (PDF en tablet / impreso con materiales).
- [ ] Versión **Pack Aula** (rúbricas + póster A3 + licencia de centro).
