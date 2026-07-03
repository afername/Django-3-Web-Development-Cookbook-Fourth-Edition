# 🤖 Maquetación — resultado

`PRODUCTO.md` (13 lecciones) está **maquetado** como cuaderno imprimible que acompaña a los
vídeos del mini-curso. Los vídeos los grabas tú; este PDF es el material de actividades.

## Entregables generados

| Archivo | Qué es | Páginas |
|---------|--------|--------:|
| `Tu-Primer-Robot-Cuaderno.pdf` | Cuaderno completo (acompaña a los 13 vídeos) | 13 |
| `Lead-Magnet-Tarjetas-de-Flechas.pdf` | Captación gratis: tarjetas de flechas + cuadrícula | 5 |
| `mockups/` | 3 imágenes de tienda (tablet, abanico, social) | — |

Incluye: portada, cómo funciona + materiales + seguridad, **13 lecciones** (2 por página,
codificadas por color de módulo), **tarjetas de flechas recortables** (avanzar, girar,
repetir, función) en vectorial, **plantilla de cuadrícula y laberinto**, **diploma de
programador/a** y contraportada con cross-sell.

## Identidad de marca
- Logo oficial y paleta de marca; color por módulo (Fundamentos, Programar movimientos,
  Ideas potentes, Proyecto final). Legible en blanco y negro. "Sin pantallas" en todo.

## Cómo regenerar
```bash
cd divergenios-productos-digitales/tools
python3 build_robot_pdf.py
python3 build_mockups.py
```

## Nota
El mini-curso es vídeo + cuaderno: faltaría **grabar los 13 vídeos** siguiendo el guion de
cada lección (campo "En el vídeo" de `PRODUCTO.md`). El cuaderno ya está listo para vender.
