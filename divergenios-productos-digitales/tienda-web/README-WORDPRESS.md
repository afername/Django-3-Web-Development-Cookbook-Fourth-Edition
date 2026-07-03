# 🛒 Tienda digital de Divergenios — guía de publicación en WordPress.com

Esta carpeta contiene la **sección de tienda lista para usar**:

- `index.html` — la página de tienda completa (catálogo, lead magnet, bundle, membresía, confianza y FAQ) con tu marca.
- `assets/` — logo y miniaturas (mockups) de los productos.

> ⚠️ **Importante (acceso):** no se ha podido publicar directamente en tu sitio porque
> eso requiere iniciar sesión en **tu** cuenta de WordPress.com y conectar **tu** pasarela
> de pago con tus datos bancarios. Por seguridad, ese último paso lo haces tú. Aquí tienes
> todo hecho y el paso a paso para dejarlo online en ~30 minutos.

---

## 1. Elige cómo vas a cobrar (lo primero)

Vendes **productos digitales descargables** a familias y colegios (muchos en la UE), así que
lo que más te conviene es una pasarela que **entregue el archivo automáticamente** y, a ser
posible, que **gestione el IVA europeo por ti**.

| Opción | Ideal si… | IVA UE | Plan WordPress.com necesario |
|--------|-----------|--------|------------------------------|
| **Lemon Squeezy** o **Paddle** (recomendado) | Quieres que ELLOS sean el "vendedor" y se encarguen del IVA/OSS automáticamente | ✅ Automático (merchant of record) | Cualquiera (incl. Free): se enlaza/embebe |
| **Payhip** | Simple y barato, con gestión de IVA UE incluida | ✅ Sí | Cualquiera |
| **Gumroad** | Lo más rápido de montar | ✅ Sí | Cualquiera |
| **WooCommerce + Stripe/PayPal** | Quieres todo "dentro" de tu WordPress y controlarlo tú | ⚠️ Lo gestionas tú (plugin de impuestos) | **Business/Commerce** |
| **Bloque "Pago con PayPal"** nativo de WordPress.com | Venta muy básica, 1 botón | ⚠️ Manual | **Premium** o superior |

**Recomendación para empezar:** crea los productos en **Lemon Squeezy** o **Payhip**, sube
cada PDF, y copia el **enlace de compra** de cada producto. Funciona con cualquier plan de
WordPress.com y te ahorra el lío del IVA. Pasas a WooCommerce más adelante si quieres.

### Cómo crear cada producto en la pasarela (vale para todas)
1. Crea una cuenta y conecta tu banco / Stripe / PayPal.
2. "Nuevo producto" → tipo **digital / descargable** → sube el PDF (p. ej. `Laboratorio-Divergenio-en-Casa.pdf`).
3. Pon nombre, precio (ver tabla de abajo) y activa la **entrega automática por email**.
4. Copia la **URL de compra** (o el botón/checkout overlay). Repite por producto.
5. Para el **Club Divergenio**, crea un producto de **suscripción** (9 €/mes).

---

## 2. Pega tus enlaces de compra en `index.html`

El archivo tiene marcadores `REEMPLAZA_...` donde van tus enlaces. Busca y sustituye:

| Marcador en index.html | Sustitúyelo por… | Precio sugerido |
|------------------------|------------------|-----------------|
| `REEMPLAZA_ENLACE_PAGO_LAB` | URL de compra de *Laboratorio Divergenio* | 14 € |
| `REEMPLAZA_ENLACE_PAGO_ING` | URL de *Retos de Ingeniería* | 11 € |
| `REEMPLAZA_ENLACE_PAGO_ADVIENTO` | URL de *Calendario de Adviento* | 9 € (estacional) |
| `REEMPLAZA_ENLACE_PAGO_ROBOT` | URL de *Tu primer robot* | 59 € |
| `REEMPLAZA_ENLACE_PAGO_AULA` | URL de *Pack Aula* | 49 € |
| `REEMPLAZA_ENLACE_SUSCRIPCION_CLUB` | URL de suscripción del *Club* | 9 €/mes |
| `REEMPLAZA_ENLACE_PAGO_BUNDLE` | URL del *Pack Divergenio* (los 3) | 27 € |
| `REEMPLAZA_CON_TU_FORMULARIO_DE_EMAIL` | `action` de tu formulario de email (ver §4) | — |

> Truco: muchas pasarelas dan un enlace que abre el checkout en una ventana superpuesta
> (overlay). Pégalo igual en el `href` del botón y listo.

---

## 3. Publica la página en WordPress.com

### Opción A — Plan Business/Commerce (recomendado para usar el diseño tal cual)
1. **Sube las imágenes:** Panel → *Medios* → sube `assets/logo.png` y `assets/thumb-*.png`.
   Copia la URL de cada una y reemplaza en `index.html` las rutas `assets/...` por esas URLs.
2. Crea una **Página** nueva llamada "Tienda".
3. Añade un bloque **HTML personalizado** y pega **todo el contenido** de `index.html`
   (o solo el `<body>`… si pegas entero, funciona dentro del bloque).
4. **Publica** y añade "Tienda" al menú principal.

### Opción B — Plan Free / Personal / Premium (HTML limitado)
WordPress.com sanea parte del CSS/JS en los planes bajos, así que tienes 2 caminos:
- **B1 (rápido):** sube el archivo `index.html` y la carpeta `assets/` a tu pasarela
  (Payhip/Lemon Squeezy permiten páginas) o a un hosting estático gratuito (Netlify,
  Cloudflare Pages, GitHub Pages) y enlaza "Tienda" del menú a esa URL.
- **B2 (nativo):** recrea la maqueta con **bloques** de WordPress (Columnas + Imagen +
  Botón) usando los textos y precios de este README. Para cada producto: una *Columna* con
  la miniatura, el título, la descripción y un **Botón** cuyo enlace es tu URL de compra.
  Para el lead magnet usa el **bloque de Formulario** (Jetpack).

> Para vender en serio y poder pegar el diseño tal cual, **merece la pena el plan Business**.

---

## 4. Conecta el lead magnet (3 experimentos gratis)

El formulario de la sección "Descarga gratis" captura el email. Para que funcione:

1. **Email marketing:** crea una lista en **MailerLite, Mailchimp, ConvertKit o Brevo**
   (todos tienen plan gratuito). Crea un formulario y copia su URL de `action` (o su embed).
2. Pega esa URL en `REEMPLAZA_CON_TU_FORMULARIO_DE_EMAIL` del `index.html`
   (o sustituye el formulario por el *embed* que te dé tu proveedor).
3. **Entrega del regalo:** configura un **email de bienvenida automático** que envíe el
   enlace de descarga del PDF de muestra. Usa los lead magnets ya generados:
   - `01-laboratorio-divergenio-en-casa/Lead-Magnet-3-Experimentos.pdf`
   - (o el del producto que quieras regalar)
4. **Alternativa nativa:** si estás en WordPress.com, usa el **bloque de Formulario de
   Jetpack**; recibirás los emails y podrás responder con el enlace, o conectarlo a tu
   proveedor de correo.

---

## 5. Detalles legales y de confianza (recomendado)

- **Páginas legales:** Aviso legal, Política de privacidad (RGPD), Términos de compra y
  Política de reembolso de productos digitales. Enlázalas en el pie.
- **Reembolsos:** al ser descargables, indica tu política (p. ej. "garantía de 14 días si
  no se ha descargado el archivo"). Está como pregunta en el FAQ: edítala con tu política.
- **IVA:** si usas Lemon Squeezy/Paddle/Payhip/Gumroad, ellos lo gestionan. Con WooCommerce
  necesitarás un plugin de impuestos UE/OSS.
- **Licencia:** los PDF ya incluyen "uso personal y de aula, prohibida la reventa". El Pack
  Aula lleva licencia de centro multi-alumno.

---

## 6. Checklist exprés (≈30 min)

- [ ] Crear cuenta en la pasarela (Lemon Squeezy / Payhip / Gumroad) y conectar cobro.
- [ ] Subir cada PDF como producto digital y copiar su enlace de compra.
- [ ] Reemplazar los marcadores `REEMPLAZA_...` en `index.html`.
- [ ] Subir `assets/` a Medios (o a tu hosting) y actualizar las rutas de imagen.
- [ ] Crear la página "Tienda" y pegar el HTML (o recrearla con bloques).
- [ ] Conectar el formulario del lead magnet y el email de bienvenida con el PDF gratis.
- [ ] Publicar, añadir al menú y hacer una **compra de prueba** de principio a fin.

---

## Precios de referencia (resumen)

| Producto | Precio | Comprador |
|----------|--------|-----------|
| Laboratorio Divergenio en Casa | 14 € | Familia + docente |
| Retos de Ingeniería Divergenio | 11 € | Familia + docente |
| Calendario de Adviento STEAM | 9 € | Familia (estacional) |
| Tu primer robot (mini-curso) | 59 € | Familia + extraescolares |
| Pack Aula (licencia de centro) | 49 € | Colegios |
| Club Divergenio (membresía) | 9 €/mes | Familia |
| **Pack Divergenio** (3 imprimibles) | **27 €** | Familia + aula |

> Cuando tengas los enlaces de compra reales y me digas tu plan de WordPress.com y tu
> pasarela elegida, puedo dejarte el `index.html` con los enlaces ya insertados y, si vas
> con bloques nativos, el desglose exacto bloque a bloque.
