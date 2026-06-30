# 🎨 Maquetación — resultado

El contenido de `PRODUCTO.md` ya está **maquetado en PDF** con la identidad visual
de Divergenios. Los archivos se generan con un script (no a mano), así que si
editas el texto fuente puedes regenerarlos en segundos.

## Entregables generados

| Archivo | Qué es | Páginas |
|---------|--------|--------:|
| `Laboratorio-Divergenio-en-Casa.pdf` | Producto completo, listo para vender | 28 |
| `Lead-Magnet-3-Experimentos.pdf` | Muestra gratis (exp. 1, 9 y 19) para captación | 7 |

Incluye: portada, carta de bienvenida, póster de seguridad, **índice clicable**,
los 20 experimentos (uno por página, codificados por color según el área STEAM),
**Cuaderno del Científico** (formulario imprimible), **Tangram vectorial a escala
real (14 cm) y recortable**, **Diploma** y contraportada con CTA.

## Identidad de marca

- **Logo oficial** de Divergenios (`tools/assets/divergenios-logo.png`) integrado en
  portada, bienvenida, cuaderno, tangram, diploma, contraportada y en cada pie de página.
- **Paleta oficial** muestreada del logo: azul `#2AB3F0`, violeta `#5512DE` y
  magenta `#C45FE0`, sobre mucho blanco. Acentos por área STEAM para codificar color.
- **Wordmark** "diver**genios**" + leyenda de iconos y nota de licencia en cada página.
- Diseñado para leerse bien también en **blanco y negro** (tintas suaves).

> Para cambiar el logo o la paleta en el futuro: reemplaza la imagen en
> `tools/assets/divergenios-logo.png` o ajusta los colores en la cabecera de
> `tools/brand.py`, y regenera.

## Cómo regenerar

```bash
cd divergenios-productos-digitales/tools
pip install reportlab          # única dependencia
python3 build_lab_pdf.py       # escribe los 2 PDF en esta carpeta
```

- `tools/brand.py` — paleta, wordmark, mascota y motivos (un solo sitio para retocar la marca).
- `tools/build_lab_pdf.py` — parsea `PRODUCTO.md` y maqueta las páginas.

## Pendiente (opcional, antes de publicar)

- [ ] Generar 3-4 **mockups** para la tienda (PDF en tablet / impreso con materiales).
- [ ] Versión **Pack Aula** (rúbricas + póster A3 + licencia de centro).
