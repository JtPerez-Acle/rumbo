# Investigación: Google Ads 2026 — curso "Google Ads en 30 días"

Material de referencia compilado en agosto de 2026 a partir de la documentación
oficial de Google Ads y guías actualizadas de la industria. Enfoque del curso:
dominar los tipos de campaña y sus FORMATOS creativos (lo que piden los empleos
de marketing hoy: saber diseñar y pensar contenidos que encajen en cada formato),
más la base técnica de medición sin la cual ninguna campaña optimiza bien.

---

## 1. El panorama Google Ads en 2026

### Tipos de campaña activos (agosto 2026)

Ocho tipos: **Search (Búsqueda), Performance Max, Shopping, Demand Gen, Display,
Video (YouTube), App y AI Max for Search**. Dos cambios grandes del año:

- **Display independiente se retira en julio de 2026**: todo el inventario de
  display pasa a servirse vía **Demand Gen**. Las campañas de Display antiguas
  deben migrarse.
- **AI Max for Search** es el tipo de campaña nuevo más importante: genera el
  copy del anuncio y elige páginas de destino automáticamente a partir del sitio.
  Google comenzó a convertir automáticamente las Dynamic Search Ads (DSA) a
  AI Max desde septiembre de 2026. Exige un sitio bien estructurado y señales de
  conversión sólidas; si el sitio es débil, AI Max amplifica el problema.

### La estructura recomendada 2026 ("Power Pack")

Google recomienda operar tres tipos de campaña en conjunto:

| Campaña | Rol | Presupuesto orientativo |
|---|---|---|
| Performance Max | Alcance full-funnel en todos los canales (incl. Search y Shopping) | 50-60% e-commerce / 30-40% B2B y servicios |
| AI Max for Search | Capturar búsquedas de alta intención | 30-40% |
| Demand Gen | Awareness y consideración (YouTube, Discover, Gmail) | 10-20% inicial, escalar al probar ROI |

Regla práctica para presupuestos chicos (LatAm, $150-500/mes): empezar con UNA
campaña (Search o PMax según el negocio), medir bien, y solo después sumar capas.
El Power Pack es la meta, no el punto de partida.

### Cómo decide Google quién ve cada anuncio

- **Ad Rank** = puja × calidad del anuncio × contexto (dispositivo, hora,
  ubicación) × impacto esperado de extensiones/recursos.
- **Calidad** (nivel de calidad 1-10 en Search): CTR esperado, relevancia del
  anuncio respecto a la búsqueda, y experiencia de página de destino (velocidad,
  claridad, coherencia con el anuncio). Mejor calidad = pagar menos por clic que
  un competidor con peor anuncio.
- Con Smart Bidding, la puja la pone la máquina subasta por subasta; el trabajo
  humano se corre a señales (conversiones bien medidas), creatividades y
  estructura.

---

## 2. Search: la base que todo lo demás asume

### Anuncios de búsqueda responsivos (RSA) — el único formato de texto

- Hasta **15 títulos de 30 caracteres** y **4 descripciones de 90 caracteres**.
  Google combina y prueba; se muestran hasta 3 títulos + 2 descripciones.
- Buenas prácticas: llenar los 15 títulos; incluir la palabra clave en 2-3
  títulos; variar ángulos (beneficio, precio/oferta, prueba social, urgencia,
  CTA directo); usar el "anclado" (pinning) con moderación porque reduce las
  combinaciones que la máquina puede probar.
- **Fortaleza del anuncio** (Ad Strength: pobre → excelente) mide variedad, no
  rendimiento; sirve de checklist, no de KPI.

### Palabras clave y concordancias en la era del Smart Bidding

- **Concordancia amplia (broad)**: hoy es la recomendada por Google SOLO
  combinada con Smart Bidding y buena medición; la IA usa la señal de conversión
  para filtrar. Sin conversiones bien medidas, broad quema dinero.
- **Concordancia de frase** ("comprar zapatillas running") y **exacta**
  ([zapatillas running mujer]): control creciente, alcance decreciente.
- **Negativas**: la herramienta de control número 1. Revisar el informe de
  términos de búsqueda cada semana las primeras 4-6 semanas y alimentar listas
  negativas (marca propia vs genéricas, "gratis", empleos, DIY, etc.).

### Recursos (antes "extensiones")

Enlaces de sitio, textos destacados, extractos estructurados, llamada,
ubicación, promoción, precios, imágenes. Suben el Ad Rank y el CTR; llenar
todos los que apliquen es de lo más rentable que existe en Search.

---

## 3. Performance Max (PMax)

Una sola campaña que sirve en Search, Shopping, YouTube, Discover, Gmail, Maps
y Display. Se le entregan activos + objetivos + señales; Google arma los
anuncios y decide dónde servirlos. En 2026 dejó de ser una caja negra total:
hay **reporte por canal** y más controles (exclusiones de marca, exclusión de
URLs, control de edad).

### Grupos de activos (asset groups) — el corazón creativo

Cada campaña: mínimo 1, máximo 100 grupos (no se comparten entre campañas).
Estructura recomendada: **un grupo de activos por tema/línea de producto**, con
señales de audiencia propias.

Requisitos mínimos por grupo (2026):

- **Texto**: 3 títulos (30 car.), 1 título largo (90 car.), 3 descripciones
  (90 car., la primera de 60), nombre del negocio, CTA, 2 rutas de URL.
- **Imágenes**: mínimo 1 horizontal 1.91:1 (1200×628), 1 cuadrada 1:1
  (1200×1200), 1 logo cuadrado; recomendado sumar vertical 4:5 (960×1200).
  JPG/PNG, máx. 5 MB, hasta 20 imágenes por grupo.
- **Video**: hasta 5 videos de 10+ segundos. Si no subes video, Google lo
  auto-genera con tus imágenes (casi siempre peor: subir siempre al menos un
  video vertical 9:16 y uno horizontal 16:9).

### Señales de audiencia y temas de búsqueda

- **Audience signals**: punto de partida, no límite — Google expande desde ahí.
  Alimentar con: datos propios (listas de clientes, visitantes web), segmentos
  personalizados (búsquedas de la competencia), intereses.
- **Search themes** (hasta 25 por grupo): dicen a PMax qué búsquedas te
  interesan; cubren huecos que el feed/página no expresa.

### Cuándo PMax sí y cuándo no

- Sí: e-commerce con feed (PMax + Merchant Center reemplazó a Smart Shopping),
  negocios con varias líneas y suficiente presupuesto/conversiones (≥30
  conversiones/mes para que el algoritmo aprenda).
- No (todavía): cuentas nuevas sin historial de conversiones, presupuestos muy
  chicos, lead gen sin validación de calidad de leads (PMax puede llenar de
  leads basura si el "conversion" es un formulario fácil).

---

## 4. Demand Gen: el formato visual (reemplazo de Discovery y Display)

Corre en **YouTube (in-stream, in-feed, Shorts, Home), Discover, Gmail
(pestañas Social/Promociones), Maps (pines promocionados, 2026) y la red de
Display**. Es la respuesta de Google a Meta/TikTok Ads: audiencias visuales que
no están buscando activamente.

### Formatos y especificaciones (2026)

- **Video**: 9:16 vertical obligatorio para Shorts (1080×1920), 16:9
  secundario, 1:1 cuadrado (1080×1080). Duración ideal 15-30 s; para Shorts
  6-15 s. El gancho en los primeros 2-3 segundos decide todo (igual que en
  orgánico).
- **Imagen**: horizontal 1.91:1 (1200×628), cuadrada 1:1 (1200×1200), vertical
  4:5 donde se soporta. JPG/PNG/GIF no animado, máx. 5 MB.
- **Carrusel**: 2 a 10 tarjetas, cuadradas o horizontales; cada tarjeta con su
  título de 40 caracteres, URL propia y CTA opcional. Ideal para catálogo,
  pasos de un proceso, antes/después.
- Textos: títulos 40 car., descripciones 90 car., nombre de negocio + logo.

### Audiencias en Demand Gen

- **Lookalike segments** (volvieron a Google vía Demand Gen): a partir de
  listas propias de 100+ usuarios; tamaños estrecho/equilibrado/amplio.
- Segmentos personalizados, datos propios, intereses y datos demográficos.
- Optimización: puja por conversiones, por clics o **maximizar conversiones
  con tCPA**; para awareness, CPM objetivo.

### Demand Gen vs Performance Max (pregunta de examen clásica)

- PMax optimiza a conversión en TODOS los canales con control creativo bajo;
  Demand Gen da control total de audiencia y creatividad en canales visuales.
- Usar Demand Gen para: llenar el funnel, remarketing visual, lanzar marca,
  productos que se "descubren" (moda, comida, viajes). PMax para: exprimir
  conversión con feed o multi-canal.

---

## 5. Shopping y Merchant Center (e-commerce)

- **Merchant Center (Next)**: la fuente del catálogo. Feed con atributos:
  id, título, descripción, link, image_link, precio, disponibilidad, GTIN/MPN,
  marca, categoría de producto, talla/color para moda.
- **El título del producto es el nuevo keyword research**: estructura
  recomendada Marca + Producto + Atributos clave (talla, color, material,
  cantidad). Lo que la gente escribe para COMPRAR debe estar en el título;
  primeros 70 caracteres visibles.
- **Listados gratuitos** (free listings): exposición orgánica en la pestaña
  Shopping solo por tener el feed sano — configurarlo aunque no haya presupuesto
  de pauta aún.
- Shopping estándar vs PMax con feed: Shopping estándar da control por producto
  y términos de búsqueda visibles; PMax da alcance total. Común: empezar con
  Shopping estándar para aprender, migrar a PMax al tener 30+ conv./mes.
- Higiene del feed: precios/stock sincronizados (desaprobaciones por
  discrepancia), imágenes sin marcas de agua, GTIN correcto, política de
  devoluciones y datos de envío completos.

---

## 6. Medición: la parte técnica que decide todo lo demás

Sin conversiones bien medidas, Smart Bidding optimiza a ruido. Orden de montaje:

1. **Google Tag / Google Tag Manager (GTM)**: instalar vía GTM es lo estándar
   en 2026 (versionado, debug y consentimiento en un solo lugar).
2. **Acción de conversión** en Google Ads (Objetivos → Conversiones → Nueva):
   compra, lead, llamada. Definir la conversión PRIMARIA (la que optimiza) y
   secundarias (solo observación). Alternativa: enlazar GA4 e importar Key
   Events — pero la etiqueta propia de Ads da mejor señal para pujar.
3. **Enhanced Conversions (conversiones mejoradas)**: envían datos propios
   hasheados (email, teléfono) junto a la conversión; Google los cruza con
   usuarios logueados y recupera conversiones perdidas por cookies/multi-
   dispositivo. Meta de salud: 50%+ de conversiones "mejoradas"; bajo 30%,
   la implementación está mal.
4. **Consent Mode v2**: obligatorio para EEA/UK; sin las señales de
   consentimiento correctas (ad_user_data, ad_personalization) el tracking se
   rompe EN SILENCIO. En LatAm aplica si vendes a Europa; buena práctica
   configurarlo igual.
5. **GA4 enlazado**: audiencias, comportamiento post-clic, embudos. Activar
   Enhanced Measurement (scrolls, clics de salida, búsquedas, video).

### Valores de conversión

Asignar valor aunque sea aproximado (lead = ticket promedio × tasa de cierre)
habilita **tROAS** y hace comparables campañas distintas.

---

## 7. Pujas (bidding) en 2026

| Estrategia | Cuándo |
|---|---|
| Maximizar clics | Solo arranque, 1-2 semanas, para juntar datos |
| Maximizar conversiones | Al tener la medición sana, sin objetivo de costo aún |
| tCPA (costo por acción objetivo) | Lead gen con costo por lead conocido |
| tROAS (retorno objetivo) | E-commerce con valores de conversión |
| CPM/CPV | Awareness (Demand Gen / Video) |

Reglas de operación: no tocar una campaña en aprendizaje (5-7 días tras cambios
grandes); cambios de presupuesto/objetivo de a ±20-30% máximo; juzgar con
ventanas que respeten el lag de conversión del negocio.

---

## 8. Creatividad y copy que convierten en Google (transversal)

- Search: el anuncio responde la búsqueda — repetir la intención en el título,
  beneficio concreto + diferenciador + CTA. Nada de "somos líderes".
- PMax/Demand Gen: pensar como catálogo de variaciones — cada imagen/video/
  título es una pieza que la máquina combina. Entregar variedad REAL (ángulos
  distintos, no la misma frase reordenada).
- Video: gancho ≤3 s, producto/beneficio visible temprano, funciona sin sonido
  (subtítulos), CTA hablado y en pantalla. Vertical primero.
- IA generativa dentro de Ads (2026): generación de imágenes y variaciones de
  texto integrada en PMax/Demand Gen — útil para volumen, pero la dirección
  creativa (ángulo, oferta, prueba social) sigue siendo humana.
- Página de destino: coherencia mensaje-anuncio-página, velocidad móvil, un
  solo objetivo por página. Los mejores anuncios mueren en páginas lentas.

---

## 9. Operación semanal de una cuenta chica (LatAm)

1. Lunes: informe de términos de búsqueda → negativas nuevas.
2. Revisar conversiones vs semana anterior (no CTR/impresiones sueltas).
3. Fortaleza de anuncio: reemplazar activos "bajos" en RSA/PMax (la máquina
   reporta qué activo rinde bajo/bueno/mejor).
4. Presupuesto: mover hacia lo que convierte con costo aceptable, de a poco.
5. Mensual: revisar ubicaciones de PMax/Demand Gen, excluir apps/sitios basura,
   refrescar 1-2 creatividades (fatiga creativa ≈ 4-6 semanas).

### Errores típicos de principiante (material para quizzes)

- Optimizar a clics/CTR en lugar de conversiones.
- Broad match sin medición de conversiones ni negativas.
- Tocar la campaña todos los días y reiniciar el aprendizaje.
- Un solo anuncio/creatividad por grupo ("la máquina no tiene con qué probar").
- Feed de Merchant Center con títulos pobres ("Zapatilla modelo X123").
- No definir conversión primaria (todas optimizando a la vez).
- Ignorar el informe por canal de PMax y no excluir tráfico basura.
- Medir el éxito de Demand Gen con métricas de Search (es otra etapa del funnel).

---

## 10. Glosario mínimo (ES/EN que el alumno verá en la plataforma)

CPC (costo por clic) · CPM (costo por mil) · CPA (costo por adquisición) ·
ROAS (retorno de la inversión publicitaria) · CTR (tasa de clics) · RSA
(anuncio de búsqueda responsivo) · PMax (Performance Max) · DSA (anuncios
dinámicos de búsqueda, migrando a AI Max) · GTM (Google Tag Manager) · GA4
(Google Analytics 4) · tCPA/tROAS (objetivos de costo/retorno) · Merchant
Center (catálogo de productos) · Ad Rank (posición en subasta) · Quality
Score (nivel de calidad) · Learning phase (período de aprendizaje).
