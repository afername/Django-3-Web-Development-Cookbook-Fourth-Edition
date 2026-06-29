# 🎨 Maquetación — resultado

`PRODUCTO.md` ya está **maquetado en PDF** con la identidad de Divergenios y el
logo oficial. Se genera con un script, así que es regenerable en segundos.

## Entregables generados

| Archivo | Qué es | Páginas |
|---------|--------|--------:|
| `Retos-de-Ingenieria-Divergente.pdf` | Producto completo, listo para vender | 24 |
| `Lead-Magnet-3-Retos.pdf` | Muestra gratis (retos 1, 7 y 16) para captación | 8 |

Incluye: portada, carta de bienvenida, **póster del ciclo de diseño** (pregunta →
imagina → construye → prueba → mejora ↺), reglas del taller, **índice clicable**,
los 16 retos (uno por página, codificados por color según el tipo de ingeniería),
**Cuaderno de Ingeniería** (formulario imprimible) y **Diploma**.

## Identidad de marca

- **Logo oficial** integrado en portada, bienvenida, cuaderno, diploma, contraportada y pies.
- **Paleta oficial** (azul `#2AB3F0`, violeta `#5512DE`, magenta `#C45FE0`) sobre blanco.
- Portada en **azul profundo "ingeniería"** para diferenciarla del Producto 1
  (violeta) manteniendo la coherencia de la línea.
- Color por sección: Estructuras (naranja), Movimiento (azul), Máquinas (violeta),
  Flotar/precisión (teal).
- Diseñado para leerse bien en **blanco y negro**.

## Cómo regenerar

```bash
cd divergenios-productos-digitales/tools
pip install reportlab
python3 build_eng_pdf.py     # escribe los 2 PDF en esta carpeta
```

- `tools/brand.py` — marca compartida (logo, paleta, motivos).
- `tools/build_eng_pdf.py` — parsea `PRODUCTO.md` y maqueta; reutiliza helpers de `build_lab_pdf.py`.

## Estrategia de bundle

Pensado para venderse **junto al Producto 1** (Laboratorio Divergente). Las
contraportadas de ambos se enlazan entre sí (cross-sell). Bundle sugerido de los dos.

## Pendiente (opcional, antes de publicar)

- [ ] Generar 3-4 **mockups** para la tienda.
- [ ] Crear la página/checkout del **bundle** (Producto 1 + 2).
