# 🎄 Maquetación — resultado

`PRODUCTO.md` está **maquetado en PDF** con la identidad de Divergenios y el logo oficial.

## Entregables generados

| Archivo | Qué es | Páginas |
|---------|--------|--------:|
| `Calendario-Adviento-STEAM.pdf` | Producto completo, listo para vender | 17 |
| `Lead-Magnet-3-Retos-Adviento.pdf` | Muestra gratis (días 1, 13 y 24) | 5 |
| `mockups/` | 3 imágenes de tienda (tablet, abanico, social 1080×1080) | — |

Incluye: portada festiva, cómo funciona + seguridad, **póster de 24 puertitas clicable**
(centro del producto y a la vez índice), **24 tarjetas recortables** (2 por página,
codificadas por color según el área STEAM, con línea de recorte), **diploma** y
contraportada con cross-sell.

## Identidad de marca

- **Logo oficial** y wordmark integrados; paleta de marca + acentos festivos
  (verde abeto, oro y rojo) y motivos de nieve/estrellas.
- Color por área STEAM en cada puertita y tarjeta.
- Diseñado para leerse e imprimirse bien en **blanco y negro**.

## Cómo regenerar

```bash
cd divergenios-productos-digitales/tools
python3 build_advent_pdf.py     # los 2 PDF
python3 build_mockups.py        # mockups de los 3 productos
```

## Estacionalidad

Producto de temporada: lanzar en octubre (early bird), empujar en noviembre, pico de
ventas del 1 al 10 de diciembre. Ver `KIT-DE-VENTA.md`.
