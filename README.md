# Reparabrisas

Sitio estático sin framework ni instalación de dependencias: landing, páginas de reparación y grabado, diseño adaptable, contacto por WhatsApp y SEO local.

## Vista local

Ejecutar `python -m http.server 8765 --bind 127.0.0.1` desde esta carpeta y abrir `http://127.0.0.1:8765`. Detener con Ctrl+C. También se puede abrir `index.html` directamente.

## Datos del negocio

- Contacto mediante botones de WhatsApp, sin número visible ni enlaces de llamada. El número se conserva únicamente en el destino de WhatsApp.
- Atención principalmente a domicilio en la zona norte de la Región Metropolitana. Las demás zonas de la región quedan sujetas a evaluación.
- Horario conservado de la versión anterior: lunes a sábado, 08:00–19:00. Confirmar antes de publicar.
- Instagram conservado: `https://www.instagram.com/reparabrisas_colina/`.
- No se inventaron dirección de taller, precios, certificaciones, años de experiencia, garantías, reseñas ni resultados fotográficos.

## Dominio y SEO antes de publicar

El dominio definitivo todavía no fue proporcionado. No hay URLs canónicas falsas ni sitemap apuntando a una URL inventada. Una vez definido, ejecutar:

```powershell
python scripts/configure-seo.py --base-url https://TU-DOMINIO-REAL
python scripts/check-site.py
```

Sustituir `https://TU-DOMINIO-REAL` por la URL pública real, incluyendo subcarpeta si se aloja en un proyecto de GitHub Pages. El script actualiza las tres páginas con canonical, Open Graph, tarjeta social PNG y URLs de datos estructurados; genera `sitemap.xml` y actualiza `robots.txt`. Es idempotente. No realiza llamadas de red ni publica nada.

Las rutas relativas admiten alojamiento bajo subcarpeta. En ese caso, los buscadores sólo leen `robots.txt` en la raíz del dominio; enviar el sitemap directamente a Search Console. Configurar HTTPS y una sola versión pública del dominio en el alojamiento. Estas redirecciones no pueden configurarse sólo desde HTML.

Datos estructurados: `AutoRepair` en portada y `Service` en las páginas de servicios. Se declara información conocida. Sin una dirección comercial pública real, el marcado no reúne todos los requisitos del resultado enriquecido LocalBusiness de Google. Esto no impide la indexación normal. No se agregan estrellas ficticias.

## Videos y fotos

El bloque `#videos` usa `data-video-id="ysz5S6PUM-U"` como **prueba**, claramente identificada. El reproductor no conecta con YouTube hasta pulsar reproducir. Para poner un video real:

1. Cambiar el ID de 11 caracteres en `index.html`, el enlace dentro de `noscript` y el enlace visible para abrir el video directamente en YouTube.
2. Cambiar los textos de demostración en esa sección y el título del iframe en `assets/js/main.js`.
3. Añadir una descripción real del trabajo, con autorización para mostrar imágenes de clientes.

La portada incluye una ilustración SVG propia, identificada como referencial. Para reemplazarla por una foto propia, guardar una imagen WebP/AVIF optimizada y actualizar `src`, dimensiones y texto alternativo en `.hero-visual`. Conservar dimensiones explícitas para evitar saltos. Para antes/después, usar fotos del mismo caso, ángulo y luz. Las reseñas y biografía del técnico se agregarán cuando existan datos verificables y el enlace del Perfil de Empresa.

## Contacto y medición

El formulario prepara un mensaje con servicio, comuna y vehículo, y abre WhatsApp. El usuario adjunta las fotos y decide enviar. No hay backend, cookies de analítica, localStorage ni almacenamiento del formulario. El reproductor carga contenido externo de YouTube al usarlo.

Los clics emiten un evento local `reparabrisas:contact` con `detail.source`, sin datos del formulario. Es un punto de integración, **no una instalación activa de Analytics**. Conectar el proveedor y su política correspondiente cuando se disponga de la cuenta. Un clic no equivale a una cotización recibida o una venta.

Acciones externas pendientes del propietario:

- Verificar dominio en Google Search Console, enviar sitemap e inspeccionar las tres URLs.
- Completar el Perfil de Empresa de Google como negocio de área de servicio, con cobertura real y domicilio oculto si no se reciben clientes allí.
- Confirmar horario, categoría, servicios y teléfono; subir fotos propias y solicitar reseñas auténticas.
- Medir consultas, clics y contactos; evaluar rendimiento móvil con PageSpeed Insights una vez publicado. Una prueba local no demuestra Core Web Vitals de usuarios reales.
- Confirmar precios, tiempos, garantía, medios de pago y presentación del técnico para reemplazar las respuestas generales actuales.

## Comprobaciones y Git

```powershell
python scripts/check-site.py
node --check assets/js/main.js
node scripts/check-contact.cjs
git diff --check
git status --short
```

La comprobación revisa enlaces locales, anchors, IDs duplicados, metadatos, JSON-LD, teléfono y conflictos residuales; prueba también el generador SEO en una carpeta temporal sin cambiar el dominio de este sitio.

Los conflictos incrustados en HTML y CSS se resolvieron conservando servicios e Instagram. No se hizo commit, push, pull, cambio de rama ni modificación del remoto. Revisar y subir manualmente los archivos cuando se desee. Ninguna implementación puede garantizar una posición específica en Google.
