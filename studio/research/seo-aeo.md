# SEO y AEO/GEO en 2026 — Investigación base y diseño de curso práctico para LatAm

Documento de trabajo. Fecha de corte: 5 de agosto de 2026.
Objetivo: material fuente para un curso en español, orientado a contenidos y e-commerce, ejecutable por una persona sola.

---

## 0. Advertencia sobre la calidad de la evidencia

El nicho "AEO/GEO" está saturado de contenido generado con IA que cita estadísticas inventadas. Ejemplos que circulan y **no tienen fuente verificable**: "similitud coseno > 0.88 → 7.3× más citaciones", "contenido multimodal → 317% más selección", "pasajes de 134-167 palabras". Ninguno proviene de un estudio publicado.

Este documento clasifica cada dato en tres niveles y el curso debe enseñar esa misma disciplina:

| Nivel | Qué es | Ejemplos usados aquí |
|---|---|---|
| **P — Primario** | Documentación oficial del propio motor, o paper con revisión de pares | Google Search Central, OpenAI Help Center / ACP docs, Bing Webmaster Tools, KDD 2024, NeurIPS 2025 |
| **V — Vendor** | Estudio de una empresa que vende herramientas SEO. Metodología parcialmente pública, incentivo comercial | Ahrefs, Semrush, Seer Interactive, BrightEdge, Moz, SE Ranking |
| **X — No verificable** | Cifra que circula en blogs sin estudio detrás | (se descarta) |

Regla del curso: **ningún alumno repite un número sin saber de qué nivel es.**

---

## 1. Estado del terreno (números con fuente)

### Presencia de AI Overviews

- **[V]** BrightEdge: los AI Overviews aparecen en ~48% de las consultas rastreadas a febrero de 2026, contra ~31% un año antes.
- **[V]** Semrush (10M+ keywords, 2025): 6,49% en enero 2025 → pico de 24,61% en julio 2025 → 15,69% en noviembre 2025.
- La diferencia entre ambos no es un error: **dependen del set de keywords**. Semrush incluye una mayoría de términos de bajo volumen. Enseñar esto: *la métrica de "cuánto AIO hay" no existe en abstracto, existe para tu set de consultas.*

### Impacto en clics

- **[V]** Seer Interactive: el CTR orgánico cayó 61% en consultas con AIO presente (1,76% → 0,61%), datos de junio 2024 a septiembre 2025. En su actualización 2026 (≈53 marcas, 5,47M consultas), el CTR se recuperó desde un piso de 1,3% en diciembre 2025 hasta 2,4% en febrero 2026.
- **[V]** Ahrefs: los AI Overviews redujeron 58% los clics al contenido mejor posicionado, comparando CTR de diciembre 2023 vs diciembre 2025 sobre 300.000 keywords con datos agregados de Search Console.

Lectura honesta para el curso: la caída es real y grande, pero **no es monotónica ni uniforme**. Varía por vertical, por tipo de consulta y por trimestre. Un curso que prometa "recuperar el tráfico perdido" miente; uno que enseñe a medir la propia exposición, no.

### Concentración de citaciones

- **[V]** Semrush, *2026 AI Visibility Index* (126 millones de prompts en EE. UU., enero–abril 2026):
  - ChatGPT cita en promedio **15 fuentes** por respuesta; Gemini, **3**.
  - En Gemini, el solapamiento entre marcas *mencionadas* y dominios *citados* baja hasta **30%**. Ser mencionado y ser citado son dos cosas distintas.
  - Solo **36 marcas** mantuvieron visibilidad top-100 en las cuatro plataformas (ChatGPT, Gemini, AI Mode, AI Overviews): YouTube, Google, Reddit, Amazon, Facebook, Apple, Walmart, Disney, Nintendo, entre otras.
  - Tráfico de IA hacia retail en EE. UU.: **+1.324%** entre octubre 2024 y mayo 2026. Viajes: **+2.215%**.
- **[V]** Ahrefs Brand Radar (consultas amplias EE. UU., julio 2026): Reddit concentra **16,7%** de las citaciones de ChatGPT. Le siguen Wikipedia, Amazon, Forbes, Business Insider.
- **[V]** Moz: sobre 40.000 consultas en Google AI Mode, **88%** de las citaciones vinieron de páginas fuera del top 10 orgánico.
- **[V]** BrightEdge: solo ~17% de las fuentes citadas en AIO también rankean en el top 10 orgánico para esa misma consulta; el solapamiento con el top 100 va de 48,7% a 53,1%.

Consecuencia operativa: **estar en el top 10 no garantiza ser citado, y no estar en el top 10 no te excluye.** Esto es lo que hace viable que un sitio pequeño de LatAm compita.

### Mercado LatAm

- **[V]** El e-commerce latinoamericano supera los **USD 215.000 millones en 2026**; la región tiene el mayor crecimiento mundial en compradores nuevos. México y Brasil lideran volumen; Colombia, Chile y Argentina crecen sostenido.
- **[P]** Google AI Mode se expandió a más de 180 países en agosto de 2025 (solo inglés al inicio) y se habilitó en español para LatAm en septiembre de 2025. En Google I/O 2026 dejó de ser experimento y pasó a ser pestaña permanente.
- Implicación estratégica: la adopción de AI Mode en español todavía va por detrás de los mercados anglosajones. **Hay una ventana de entrada más barata en español que en inglés.** Ese es el argumento comercial central del curso.

---

## 2. Cómo funciona Google hoy

### 2.1 La documentación oficial (lo más importante de 2026)

El 15 de mayo de 2026 Google publicó **"Optimizing your website for generative AI features on Google Search"** (`developers.google.com/search/docs/fundamentals/ai-optimization-guide`, última actualización 10 de julio de 2026). Es el ancla del curso: por primera vez Google documenta formalmente qué hacer y qué ignorar.

Puntos textuales de esa guía **[P]**:

1. **AEO y GEO "siguen siendo SEO"** desde la perspectiva de Google. No hay una disciplina separada para sus features generativos.
2. Las features generativas se apoyan en **RAG (grounding)** sobre el índice de búsqueda existente y en **query fan-out**: el modelo genera consultas relacionadas concurrentes. Ejemplo de la propia doc: para "cómo arreglar un césped lleno de malezas", el fan-out genera "mejores herbicidas para césped", "eliminar malezas sin químicos", "cómo prevenir malezas".
3. **Requisito de elegibilidad**: la página debe estar indexada y ser elegible para mostrarse con snippet, y el sitio debe estar **incluido en las features generativas desde Search Console**. Google añadió un control de opt-out: se puede excluir el contenido de AI Overviews / AI Mode / Discover AI sin salir de la búsqueda tradicional.
4. **Contenido no-commodity**: el ejemplo de Google es explícito. Commodity = "7 consejos para compradores primerizos". No-commodity = "Por qué renunciamos a la inspección y ahorramos dinero: por dentro de la línea de alcantarillado".
5. Merchant Center y Google Business Profile alimentan las respuestas generativas para productos y negocios locales.

### 2.2 Lo que Google dice explícitamente que se puede ignorar **[P]**

| Táctica | Postura de Google |
|---|---|
| `llms.txt` y "markup especial" | No se usan. Crearlos "ni perjudica ni ayuda" |
| "Chunking" del contenido | Innecesario. Los sistemas entienden páginas multi-tema. No hay largo ideal |
| Reescribir para IA | Innecesario. Los sistemas entienden sinónimos; no hace falta cubrir cada variante long-tail |
| Buscar menciones inauténticas | Contraproducente; los sistemas antispam las bloquean |
| Sobre-enfocarse en datos estructurados | **No son requeridos** para búsqueda generativa. Siguen siendo útiles para rich results |

Este cuadro es, probablemente, la diapositiva más valiosa del curso: **desactiva de un golpe la mitad de lo que venden las agencias "GEO" en la región.**

### 2.3 Los core updates de 2025-2026

- 2025: tres core updates (marzo, junio, diciembre).
- Febrero 2026: **primer core update exclusivo de Discover** de la historia.
- Marzo 2026: spam update (24–25 de marzo) seguido de core update (27 de marzo – 8 de abril, 12 días y 4 horas). Ventanas superpuestas → atribución difícil.
- Mayo 2026: core update (21 de mayo – 2 de junio, 11 días y 21 horas), con volatilidad reportada aún mayor.
- **[V]** Análisis de Aleyda Solis con datos de Sistrix (26 marzo – 11 abril): la visibilidad se movió desde sitios intermediarios hacia fuentes destino — oficiales/institucionales, especialistas de nicho, marcas establecidas.
- Contexto de fondo: desde marzo de 2024 el Helpful Content System dejó de ser un sistema aparte y se integró al núcleo. Ya no se puede "esperar a que pase".

### 2.4 Señales que siguen vigentes

No cambiaron. Indexación, relevancia, calidad del contenido, enlaces, experiencia de página, señales de E-E-A-T. Lo que cambió es **el uso** que se hace de ellas: primero deciden si entras al conjunto de candidatos que recupera el RAG, y recién ahí se decide qué pasaje se cita.

---

## 3. Cómo citan los motores de respuesta

### 3.1 El patrón común

Los cuatro grandes comparten arquitectura: recuperar candidatos de un índice → leerlos → sintetizar → citar un subconjunto. Las diferencias están en **de qué índice recuperan**.

| Motor | Índice de recuperación | Consecuencia práctica |
|---|---|---|
| **Google AI Overviews / AI Mode** | Índice de Google | SEO clásico + estar habilitado en Search Console |
| **ChatGPT (búsqueda)** | Índice de Bing | **Verificar el sitio en Bing Webmaster Tools es obligatorio, no opcional** |
| **Microsoft Copilot** | Índice de Bing, nativo | Igual que arriba. Superficie mucho menos disputada |
| **Perplexity** | Índice propio con crawling continuo | Favorece frescura y fuentes de noticias/académicas |
| **Gemini** | Grounding con Google Search | Cita muy pocas fuentes (~3); alto riesgo de mención sin citación |

### 3.2 Datos por motor

- **[V]** ChatGPT cita en promedio 15 fuentes; Gemini, 3 (Semrush 2026).
- **[V]** ChatGPT prefiere contenido fresco: edad media de sus citaciones en contexto ≈958 días vs 1.432 días de los resultados orgánicos (Ahrefs, 17M de citaciones). En agregado, las citaciones de IA son ~25,7% más recientes que el orgánico.
- **[V]** Perplexity es el más "search-like": cerca de 1 de cada 3 enlaces citados ya rankea en el top 10 de Google.
- **[V]** SE Ranking: **88% de las citaciones de Copilot son exclusivas de Copilot** — es decir, puedes dominar AIO, Perplexity y ChatGPT y estar ausente en Copilot.
- **[V]** Growth Memo (2026): 44,2% de las citaciones LLM provienen del **primer 30% del texto**; 31,1% del medio; 24,7% del cierre.

### 3.3 Bing como cuello de botella olvidado

Punto operativo de alto ROI para LatAm y que casi nadie hace:

1. Verificar el sitio en **Bing Webmaster Tools** (gratis).
2. Enviar sitemap.
3. Activar **IndexNow** (protocolo que también consumen Yandex, Seznam, Naver y Yep) — indexa en minutos en vez de esperar el ciclo de crawl.
4. Confirmar que el firewall/CDN no bloquee Bingbot.
5. Dar de alta **Bing Places** si hay negocio local.

Sin esto, dos de los mayores motores de respuesta no ven el sitio, sin importar qué tan bien esté en Google.

---

## 4. AEO/GEO: qué dice la evidencia real

Aquí es donde el curso se diferencia. Hay dos papers que se contradicen y hay que enseñar los dos.

### 4.1 El paper fundacional: GEO (Princeton et al., KDD 2024) **[P]**

Aggarwal, Murahari, Rajpurohit, Kalyan, Narasimhan, Deshpande — Princeton, Georgia Tech, Allen Institute for AI, IIT Delhi. Benchmark GEO-bench: 10.000 consultas en 9 dominios.

Hallazgos:
- Agregar **estadísticas**, **citas textuales** y **fuentes citadas** eleva la visibilidad hasta **+40%**.
- Efecto nivelador: páginas en posición 5 con citaciones añadidas ganaron **+115,1%** de visibilidad.
- La optimización de fluidez (escritura más clara, sin agregar contenido) rindió ~28%.
- **Keyword stuffing rindió 10% peor que la línea base** en Perplexity.

### 4.2 El correctivo: C-SEO Bench (Puerto et al., NeurIPS 2025 D&B) **[P]**

Puerto, Gubri, Green, Oh, Yun (Parameter Lab / Naver AI Lab). 9 métodos C-SEO, 6 dominios, 2 tareas (QA y recomendación de producto), 1.921 consultas, y — clave — **tasas variables de adopción por múltiples actores**.

Hallazgos:
- La mayoría de los métodos C-SEO son **en gran medida inefectivos**, y varios **empeoran** el ranking del documento.
- El baseline de SEO tradicional (mejorar el ranking de recuperación, mover el documento a la posición 1 del contexto) fue **~7,6× más efectivo** que el mejor método C-SEO en el dominio retail.
- C-SEO es un **juego congestionado y de suma cero**: a mayor adopción, menor ganancia marginal.
- El estudio original de Princeton sobreestima porque usa un escenario de actor único con solo 5 fuentes compitiendo.

### 4.3 Síntesis defendible para el curso

> Las técnicas de GEO tienen efecto real pero **de segundo orden**. El efecto de primer orden sigue siendo la recuperación: ser indexado, ser relevante, ser confiable. Estimación de reparto de esfuerzo: **~80% SEO fundamental, ~20% formato citable.**

Coherente con la propia postura de Google ("sigue siendo SEO") y con la del sector — la cita de Jeremy Moser (uSERP) "el 80% del GEO es SEO fundamental bien hecho" circula ampliamente y describe bien el consenso.

### 4.4 Autoridad: lo que sí correlaciona **[V]**

Ahrefs, *Q1 2026 AI Search Benchmark Report* (13 estudios; 146M de SERPs, 730.000 respuestas de IA). Sobre 75.000 marcas con DR > 40 y keywords de 800+ búsquedas/mes, correlaciones de Spearman con visibilidad en IA:

| Señal | Correlación |
|---|---|
| Menciones en YouTube | **0,737** |
| Menciones de marca en la web | **0,664** |
| Anchor text de marca | 0,527 |
| Volumen de búsqueda de marca | 0,334–0,392 |
| **Backlinks** | **0,218** |
| Número de páginas del sitio | débil |

Dos lecturas obligatorias en clase:

1. **Correlación no es causalidad.** Los propios investigadores de Ahrefs lo advierten. Las marcas conocidas tienen más menciones *y* más visibilidad en IA porque son conocidas.
2. **Publicar volumen no construye visibilidad en IA.** El conteo de páginas casi no correlaciona. Esto contradice de frente la estrategia de "300 artículos con IA" que se vende en la región.

Y la advertencia de Google **[P]**: buscar menciones inauténticas no funciona. La lectura correcta de 0,664 no es "compra menciones", es "el trabajo que genera menciones genuinas — producto, prensa, comunidad, video — es lo que mueve la aguja".

### 4.5 `llms.txt`: caso cerrado

- **[P]** Google: "No necesitas crear archivos legibles por máquina, archivos de texto para IA, markup ni Markdown para aparecer en Google Search (incluidas sus capacidades generativas), ya que Google Search no los usa."
- **[P]** John Mueller lo comparó con la meta tag `keywords` — una señal autodeclarada que se abandonó por manipulable.
- **[V]** Ahrefs (137.000 sitios): **97% de los archivos `llms.txt` recibieron cero solicitudes** en mayo de 2026.
- **[V]** SE Ranking (~300.000 dominios): sin correlación estadísticamente significativa con la frecuencia de citación. Quitar la variable del modelo **mejoró** su precisión — era ruido.
- Uso legítimo restante: documentación técnica que consumen agentes de código (Cursor, Windsurf). Si tu audiencia son desarrolladores, media jornada de trabajo. Si vendes zapatillas, no.

---

## 5. SEO on-page 2026

### 5.1 Intención de búsqueda: el mapeo que evita canibalización

Una consulta → un tipo de página. Regla dura:

| Intención | Señales léxicas (español LatAm) | Página |
|---|---|---|
| Informacional | "qué es", "cómo", "para qué sirve", "diferencia entre" | Artículo/guía |
| Comercial | "mejor", "mejores", "cuál conviene", "vs", "opiniones", "reseña" | Comparativa o categoría |
| Transaccional | "comprar", "precio", "oferta", "envío", "cotizar", "tienda" | Categoría o ficha |
| Navegacional | marca + producto | Home / ficha |
| Local | "cerca de mí", "en Santiago", "a domicilio" | Landing local + GBP |

**Método sin herramientas de pago**: buscar la consulta en incógnito, con el país correcto, y clasificar por lo que Google ya está mostrando. Si el top 10 son categorías, no ganarás con un blog post. La SERP es la respuesta a "qué quiere Google aquí".

### 5.2 Títulos

- Título HTML ≈ **50–60 caracteres** (el límite real es en píxeles, no en caracteres; en español, con más tildes y palabras largas, conviene apuntar a 55).
- Estructura para blog: `[Consulta exacta] + [modificador de valor] + [año si aplica] | Marca`
- Estructura para ficha: `[Producto] [Marca] [Modelo] [Atributo diferenciador] — [Tienda]`
- H1 ≠ título HTML necesariamente; el H1 puede ser más natural.
- Meta description no es factor de ranking, pero sí de CTR. ~150-160 caracteres.

### 5.3 Formato citable (la parte de AEO que sí sostiene evidencia)

Aplicar en cada sección, no en toda la página:

1. **Respuesta primero.** La afirmación central en las primeras 2-3 oraciones bajo cada H2. Consistente con el dato de que ~44% de las citaciones salen del primer 30% del texto.
2. **Una afirmación por encabezado.** H2/H3 formulados como la pregunta real del usuario.
3. **Cifras específicas con fuente y fecha.** "El 48% de las consultas rastreadas por BrightEdge en febrero de 2026" > "la mayoría de las consultas".
4. **Enlazar la fuente primaria.** Es la técnica "cite sources" del paper de Princeton y además reduce el riesgo de que el modelo prefiera al que sí la enlaza.
5. **Autor real, con bio y credenciales verificables.** Fecha de publicación y de actualización visibles.
6. **Experiencia de primera mano.** Es lo que Google llama contenido no-commodity y lo que los core updates de 2026 premiaron.
7. **Tablas y listas para datos comparables.** Extraíbles sin ambigüedad.

Lo que **no** hay que hacer: partir el artículo en 40 micro-secciones "para el LLM" (Google dice que no hace falta), ni escribir en un dialecto artificial "para IA".

### 5.4 Keyword research con IA en 2026

El cambio de fondo: **el prompt promedio de ChatGPT ronda las 60 palabras; la búsqueda promedio en Google, 3,4** (Similarweb, *Generative AI Landscape*). Son dos listas distintas y hacen falta las dos.

**Flujo práctico, herramientas gratis:**

1. **Base real, no inventada.** Exportar Search Console (16 meses, filtro por país). Esas son las consultas que ya te asocian.
2. **Expansión con LLM sobre datos propios.** Pegar el export en ChatGPT/Claude/Gemini y pedir: agrupar por intención, detectar consultas en posición 8-20 (cercanas a página 1), detectar clusters sin página dedicada. *Nunca* pedirle volúmenes al LLM: los inventa.
3. **Validación de volumen** con Keyword Planner (gratis con cuenta de Google Ads activa), Google Trends (comparación relativa por país), y autocompletado de Google / "Otras preguntas" / búsquedas relacionadas.
4. **Lenguaje real de compra**: autocompletado de **Mercado Libre** y de **Amazon**. Es la fuente más directa de cómo la gente nombra los productos en la región, y es gratis.
5. **Prompt research** (lo nuevo): armar un set fijo de 20-40 prompts que un comprador realmente escribiría, en español, largos y con contexto. Fuentes: tickets de soporte, transcripciones de ventas, WhatsApp, hilos de Reddit y foros locales. Correrlos periódicamente y registrar si aparece la marca y quién aparece en su lugar.
6. **Localización léxica.** Obligatorio en LatAm: *palta/aguacate*, *auto/carro/coche*, *celular/móvil*, *computador/computadora/ordenador*, *polera/playera/remera/franela*, *departamento/apartamento*. El keyword research en "español" genérico falla. Se hace **por país**.

---

## 6. SEO técnico mínimo viable

El objetivo no es un sitio perfecto, es **no quedar fuera del conjunto de candidatos**.

### 6.1 Indexación (prioridad 1)

- Search Console verificado + sitemap XML enviado.
- Revisar el informe **Páginas** → "No indexadas". Los tres motivos frecuentes: `noindex` accidental, canonical apuntando a otra URL, "Rastreada, actualmente sin indexar" (= problema de calidad/valor, no técnico).
- `robots.txt` auditado **bot por bot**. Error común y caro: bloquear el bot que entrena (`GPTBot`) creyendo que se protege el contenido, y bloquear de paso el que recupera para las respuestas (`OAI-SearchBot`, `PerplexityBot`), lo que borra el sitio de esos motores.
- Bing Webmaster Tools + IndexNow (ver 3.3).
- Contenido principal en el HTML. Si depende de JavaScript para renderizarse, seguir las prácticas de JavaScript SEO de Google. Los agentes de navegación además leen DOM y árbol de accesibilidad.

### 6.2 Core Web Vitals — estado real 2026 **[P]**

Umbrales **sin cambios**, medidos en **campo (CrUX), percentil 75, ventana móvil de 28 días**:

| Métrica | Bueno | Necesita mejora | Malo |
|---|---|---|---|
| LCP (carga) | ≤ 2,5 s | 2,5–4,0 s | > 4,0 s |
| INP (respuesta) | ≤ 200 ms | 200–500 ms | > 500 ms |
| CLS (estabilidad) | ≤ 0,1 | 0,1–0,25 | > 0,25 |

Notas para el curso:
- **Mito a desmontar**: "el umbral de LCP bajó a 2,0 s en 2026". Es falso. web.dev sigue documentando 2,5 s. Circula en blogs generados con IA.
- INP reemplazó a FID en **marzo de 2024**. Cualquier guía que hable de FID está desactualizada.
- Se aprueban **las tres o ninguna**. Dos en verde y una en amarillo = reprobado.
- **Lighthouse es laboratorio, CrUX es campo.** 100/100 en Lighthouse no significa nada si el 25% de los usuarios reales entran con un gama media y 4G.
- Se optimiza **por plantilla**, no por URL. Un fix en la plantilla de ficha de producto arregla miles de URLs.
- Es un factor de desempate, no un sustituto de relevancia. Su mayor valor real es conversión.

Diagnóstico gratis: Search Console → Core Web Vitals (campo), PageSpeed Insights (campo + laboratorio), CrUX.

---

## 7. E-commerce específico

### 7.1 Nombrar con las palabras exactas de compra

Principio: **el nombre de la categoría y del producto se toma del comprador, no del catálogo interno ni del proveedor.**

Método, 45 minutos por categoría, sin costo:

1. Escribir 5 formas en que un cliente pediría el producto por WhatsApp.
2. Autocompletar en Mercado Libre del país objetivo. Anotar los sufijos que aparecen (`para`, `de`, `con`, marcas, medidas).
3. Autocompletar en Google con el país correcto. Revisar "Otras preguntas" y "Búsquedas relacionadas".
4. Validar volumen relativo en Keyword Planner / Trends **por país**.
5. Contrastar con Search Console: ¿ya llegan impresiones con otro término?

Ejemplos de la brecha típica:

| Nombre interno (mal) | Nombre de compra (bien) |
|---|---|
| "Soluciones de almacenamiento" | "Cajas organizadoras plásticas con tapa" |
| "Línea Premium Hogar" | "Sábanas 100% algodón 2 plazas" |
| "Calzado deportivo unisex" | "Zapatillas para correr mujer" |
| "Dispositivos de audio portátil" | "Parlante bluetooth resistente al agua" |

Reglas:
- La categoría es **más importante que la ficha** para consultas no-marca: rankea para términos más amplios y con más volumen.
- Una categoría no es una grilla vacía: 150–300 palabras útiles arriba o abajo (criterios de elección reales, no relleno), enlaces a subcategorías y a los productos top, breadcrumbs.
- **Nunca** copiar la descripción del fabricante. Es la misma en 50 sitios: contenido commodity por definición.
- Navegación facetada: decidir explícitamente qué combinaciones se indexan. Sin reglas de canonical/`noindex`/robots, los filtros generan miles de URLs duplicadas y consumen presupuesto de rastreo.

### 7.2 Datos estructurados de producto

Aunque Google diga que schema **no es requerido** para búsqueda generativa **[P]**, sigue siendo la vía para rich results y la forma más barata de que cualquier máquina lea el producto sin ambigüedad. Mínimo por ficha:

`Product` con: `name`, `image`, `brand`, `sku`, `gtin`/`mpn`, `description`, `offers` (`price`, `priceCurrency`, `availability`, `url`), `aggregateRating` + `review` cuando sean reseñas reales.
Complementos: `BreadcrumbList`, `Organization` en el sitio, políticas de envío y devolución.

Regla de oro: **el precio y el stock del schema deben coincidir con lo que muestra la página.** Un desajuste no es un detalle de UX; te cuesta posición.

### 7.3 AI Overviews en consultas de compra

**[V]** Search Engine Land, sobre 20,9 millones de SERPs de shopping: los AI Overviews pasaron de ~2,1% de las consultas de compra en noviembre 2025 a **~14% en marzo de 2026** (≈5,6×). Aparecen mucho más en consultas informacionales tipo "mejor [producto]" que en las puramente transaccionales tipo "comprar X".

Implicación: **las páginas de comparación y guías de compra son la palanca de AEO en e-commerce**, no las fichas.

### 7.4 ChatGPT Shopping — el cambio de marzo de 2026 **[P]**

El 24 de marzo de 2026 OpenAI publicó *"Powering product discovery in ChatGPT"*. Contenido relevante:

- OpenAI reconoció por escrito que la primera versión de **Instant Checkout no daba la flexibilidad buscada**, habilitó a los comercios a usar su propio checkout y **redirigió el esfuerzo hacia el descubrimiento de producto**. El Agentic Commerce Protocol (ACP) se extendió a descubrimiento.
- **Tres puertas de entrada**, que no compiten entre sí:
  1. **Shopify Catalog** — automática. Si la tienda corre en Shopify, los productos ya están integrados; OpenAI lo dice explícitamente: no se requiere trabajo adicional del comercio. *(Si alguien cobra por "listarte en ChatGPT" y vendes en Shopify, te está cobrando por algo que ya tienes.)*
  2. **Feed directo** — el schema de ACP tiene **79 campos, 19 obligatorios** para un feed no-Ads: `item_id`, `title`, `description`, `url`, `brand`, `image_url`, `price` con código ISO 4217, `availability`, más los flags `is_eligible_search` e `is_eligible_checkout`. Es un proyecto de ingeniería vivo, no un archivo que se sube una vez.
  3. **La web abierta** — la puerta que aplica a todos. ChatGPT considera metadatos estructurados de proveedores propios y de terceros, más otro contenido de terceros. Es decir: tus fichas *y* lo que otros publican sobre tus productos.
- **Factores de ordenamiento declarados por OpenAI** cuando lista los comercios que venden un producto: **disponibilidad, precio, calidad, y si eres el fabricante o vendedor principal del artículo.** Si revendes algo que el fabricante también vende, partes en desventaja estructural.
- **ChatGPT puede reescribir títulos y descripciones** porque los comercios nombran el mismo producto de formas distintas. Etiquetas como "económico" o "más popular" las genera el modelo y **no son afirmaciones verificadas**. Consecuencia directa: **rellenar el título de keywords es trabajo para que un modelo lo reescriba.** Lo que sobrevive es dato duro y correcto.
- El carrusel de productos hoy es orgánico: OpenAI afirma que los resultados se seleccionan de forma independiente, no son anuncios y no están influidos por partnerships. Pero el mismo schema del feed incluye un flag `is_ads_eligible`. Ambos futuros conviven en el archivo.
- **ChatGPT no lee tu feed de Google Merchant Center.** Nada en la documentación de OpenAI lo indica. La higiene de datos que exige Merchant Center sí paga en todos los canales, pero el feed no viaja solo.

### 7.5 Orden de trabajo recomendado para una tienda

1. ¿ChatGPT/Gemini/Perplexity mencionan mi tienda cuando alguien describe lo que vendo? (baseline)
2. ¿Mis fichas son rastreables y el contenido está en el HTML?
3. ¿`robots.txt` deja pasar a los bots de recuperación correctos?
4. ¿Product schema completo, con precio y stock sincronizados?
5. ¿Tengo reseñas reales en sitios públicos? (los resúmenes de reseñas que muestra ChatGPT salen de ahí; sin reseñas no hay nada que resumir)
6. ¿Soy el vendedor principal de mi propia marca, o mi producto está mejor documentado y más barato en un marketplace?
7. Recién aquí: ¿necesito un feed directo?

---

## 8. Medición y monitoreo

### 8.1 Herramientas gratuitas (base obligatoria)

| Herramienta | Qué da | Costo |
|---|---|---|
| **Google Search Console** | Consultas, impresiones, clics, indexación, CWV de campo. **Nuevo:** informe *Generative AI performance* | Gratis |
| **Bing Webmaster Tools** | Indexación, IndexNow y **AI Performance report** | Gratis |
| **Google Analytics 4** | Tráfico referido desde chatgpt.com, perplexity.ai, gemini.google.com | Gratis |
| **PageSpeed Insights / CrUX** | Core Web Vitals campo + laboratorio | Gratis |
| **Rich Results Test / Schema validator** | Validación de datos estructurados | Gratis |
| **Google Trends** | Demanda relativa por país y estacionalidad | Gratis |
| **Keyword Planner** | Volúmenes (rangos amplios sin campaña activa) | Gratis con cuenta Ads |
| **Google Merchant Center** | Feed de producto, fichas gratuitas | Gratis |
| **Google Business Profile** | Negocio local en Search/Maps y respuestas de IA | Gratis |
| **Screaming Frog** | Crawl técnico | Gratis hasta 500 URLs |
| **Autocompletado de Mercado Libre / Amazon** | Lenguaje real de compra | Gratis |

### 8.2 Los dos informes nuevos de 2026 (lo más importante para el curso)

**Bing Webmaster Tools — AI Performance** **[P]**
- Vista previa pública desde el **10 de febrero de 2026**; ampliado el **16 de junio de 2026** con Intents, Topics, Citation Share y Compare.
- Métricas: **citaciones** (cuántas veces tu contenido se mostró visiblemente como fuente en respuestas de IA) y **grounding queries** (las frases de recuperación que el sistema genera internamente al construir una respuesta). Ventana de 90 días.
- Cubre Copilot, resúmenes de IA de Bing e integraciones de partners. **No** cubre ChatGPT, Perplexity, AI Overviews, Claude ni Gemini directamente — pero como ChatGPT recupera del índice de Bing, funciona como **proxy razonable**.
- Sin API por ahora.
- **Es el único dato de citación de primera parte y gratuito que existe.** Verificar el sitio en Bing es la acción de mejor relación costo/beneficio de todo el curso.

**Google Search Console — Generative AI performance** **[P]**
- Lanzado el **3 de junio de 2026**. Datos desde el **18 de mayo de 2026**; sin histórico previo.
- Dos informes: features generativas en Search (AI Overviews + AI Mode) y features generativas en Discover.
- Dimensiones: **impresiones**, páginas, países, dispositivos, fechas.
- **No incluye clics, CTR, posición ni consultas.** Es visibilidad, no valor de tráfico.
- Los datos ya estaban contabilizados en el informe de rendimiento general: **lo nuevo es la vista separada, no el dato**. Los totales agregados no cambian.
- Despliegue por fases (Reino Unido primero). Sin API.
- En el mismo anuncio, Google añadió el **control de inclusión/exclusión** de las features generativas.

### 8.3 Herramientas pagas: cuándo tienen sentido

Rangos observados en 2026: desde ~USD 39–69/mes (AIclicks, Qwairy) y ~USD 99/mes (Semrush AI Visibility Toolkit, Profound Starter) hasta USD 300–1.000+/mes (Scrunch AI) y planes enterprise de USD 1.500–2.000+.

Criterio para LatAm: **no se paga hasta tener un baseline manual**. El baseline manual cuesta 0 y consiste en correr 20-40 prompts fijos a mano una vez al mes y anotar los resultados en una planilla. Solo cuando ese proceso duele por volumen se justifica automatizarlo.

Consideración regional: casi todas cobran en USD con tarjeta internacional. Con IVA/impuestos digitales, una suscripción de USD 99 puede acercarse a USD 120-140 efectivos en varios países. Vale la pena mencionarlo explícitamente en clase.

Advertencia de Google **[P]**: desconfiar de herramientas de terceros que prometan éxito de ranking o afirmen usar métricas "internas" de Google. Ninguna herramienta externa tiene acceso a sus sistemas de ranking o de IA.

### 8.4 Métricas que sí sirven

| Métrica | Dónde | Frecuencia |
|---|---|---|
| Impresiones en features generativas | GSC | Semanal |
| Citaciones y grounding queries | Bing WMT | Semanal |
| Tasa de mención en set de prompts fijos | Manual / herramienta | Mensual |
| Share of citations vs 3 competidores | Manual / herramienta | Mensual |
| Clics y CTR orgánicos por cluster | GSC | Semanal |
| Páginas indexadas vs publicadas | GSC | Mensual |
| CWV por plantilla | GSC / CrUX | Mensual |
| Tráfico referido de LLMs | GA4 | Semanal |
| Conversiones asistidas por IA | GA4 + "¿cómo nos encontraste?" | Mensual |

Nota: cuando comercial diga "el cliente dijo que ChatGPT nos recomendó", **eso es un dato**. Registrarlo. En muchos negocios de la región va a ser la evidencia más fuerte disponible durante todo 2026.

---

## 9. Errores comunes

**De estrategia**
1. Tratar AEO/GEO como un canal separado del SEO. Google dice explícitamente que no lo es.
2. Publicar volumen con IA. El conteo de páginas casi no correlaciona con visibilidad en IA y los core updates de 2026 castigaron el contenido escalado sin expertise humano.
3. Perseguir menciones inauténticas tras leer el 0,664 de Ahrefs. Confundir correlación con receta.
4. Optimizar solo para ChatGPT. 88% de las citaciones de Copilot son exclusivas de esa plataforma.
5. Medir solo tráfico. Con respuestas de cero clic, la mención sin clic ya influyó en la decisión.

**Técnicos**
6. Implementar `llms.txt` en lugar de arreglar indexación.
7. No verificar el sitio en Bing Webmaster Tools — cierra ChatGPT y Copilot de un plumazo.
8. Bloquear el bot equivocado en `robots.txt`.
9. Perseguir 100/100 en Lighthouse mientras CrUX está en rojo.
10. Navegación facetada sin reglas: miles de URLs duplicadas.
11. Contenido principal solo en JavaScript.

**De contenido**
12. Enterrar la respuesta bajo tres párrafos de introducción.
13. Escribir contenido commodity ("7 tips para...") y esperar diferenciación.
14. Cifras sin fuente ni fecha. Es lo primero que un modelo no puede corroborar.
15. Sin autor real, sin bio, sin fecha visible.
16. Actualizar solo la fecha sin tocar el contenido. Google detecta modificación real.
17. Traducir del inglés sin localizar el léxico por país.

**De e-commerce**
18. Nombrar categorías con jerga interna o de marketing.
19. Copiar la descripción del fabricante.
20. Rellenar títulos de producto con keywords — ChatGPT los reescribe igual.
21. Precio o stock desincronizados entre página, schema y feed.
22. Pagar por "listarse en ChatGPT" teniendo Shopify.
23. Asumir que el feed de Merchant Center llega a ChatGPT. No llega.
24. Cero reseñas públicas y luego preguntarse por qué la IA no recomienda la tienda.

**De medición**
25. Leer el informe de IA en GSC como si midiera tráfico. Solo mide impresiones.
26. Reaccionar a un core update en pleno rollout. Esperar a que cierre y comparar ventanas limpias.
27. Borrar páginas de bajo rendimiento tras una caída. Suele empeorar la autoridad temática; conviene mejorarlas o consolidarlas.
28. Comprar una herramienta de USD 300/mes antes de tener un baseline manual.

---

## 10. Flujo de trabajo semanal para una persona

Presupuesto: **6 horas por semana.** Diseñado para ser sostenible, no heroico.

### Lunes — Lectura de datos (45 min)
- GSC: informe de rendimiento, últimos 7 días vs 7 anteriores. Anotar consultas en posición 8-20.
- GSC: informe *Generative AI performance* (si el sitio ya lo tiene habilitado).
- Bing WMT: AI Performance. Nuevas grounding queries. Páginas que ganan o pierden citaciones.
- GA4: tráfico referido de chatgpt.com, perplexity.ai, gemini.google.com.
- Salida: **una lista de 3 acciones**, no un informe.

### Martes — Producción (2 h)
- Un artículo nuevo o una reescritura profunda. No dos.
- Checklist antes de publicar: respuesta primero bajo cada H2; al menos 2 cifras con fuente y fecha; fuentes primarias enlazadas; autor con bio; una tabla o lista comparativa; un dato o experiencia que no exista en otro lado.
- Enlazado interno desde y hacia el cluster.

### Miércoles — E-commerce / fichas (1 h)
- 5 fichas o 1 categoría por semana.
- Título con palabras de compra, descripción propia, schema validado, precio y stock verificados, imágenes con alt real.
- Cada 4 semanas: revisión de navegación facetada y de URLs indexadas de más.

### Jueves — Autoridad fuera del sitio (1 h)
Rotar una actividad por semana:
- Semana 1: un video corto en YouTube sobre el tema del artículo del martes (mayor correlación medida con visibilidad en IA).
- Semana 2: responder 3 preguntas reales en Reddit/foros/grupos del rubro, sin spam, con la experiencia propia.
- Semana 3: perfiles y directorios — actualizar GBP, Bing Places, marketplaces, sitios de reseñas del sector.
- Semana 4: outreach de prensa o colaboración con un medio/newsletter local.

### Viernes — Técnico y control (45 min)
- Cobertura de indexación en GSC: revisar nuevos "no indexados".
- IndexNow para las URLs nuevas o modificadas de la semana.
- PageSpeed Insights sobre **una plantilla** (home / categoría / ficha / artículo), en rotación mensual.
- Validar schema de lo publicado.

### Mensual (30 min extra, primer viernes)
- Correr el set fijo de 20-40 prompts en ChatGPT, Gemini y Perplexity. Registrar: ¿aparece la marca? ¿quién aparece en su lugar? ¿qué fuentes se citan?
- Actualizar la planilla de share of citations vs 3 competidores.
- Revisar el Search Status Dashboard de Google por updates confirmados.

### Trimestral (medio día)
- Auditar y actualizar el 20% de contenido más antiguo con tráfico.
- Revisar `robots.txt` bot por bot.
- Revisar cifras citadas en artículos: si envejecieron, actualizarlas (la frescura es una señal medida en las citaciones de IA).

---

## 11. Diseño del curso

**Formato sugerido:** 8 módulos, 16–20 horas totales, en vivo o grabado con entregables por módulo.
**Perfil de alumno:** dueño de e-commerce, marketer generalista, freelance de contenidos en LatAm. No se asume conocimiento técnico previo.
**Principio pedagógico:** cada módulo termina con algo hecho sobre el sitio real del alumno, no con un ejercicio hipotético.

| # | Módulo | Horas | Entregable |
|---|---|---|---|
| 1 | **Cómo funciona la búsqueda en 2026** — RAG, query fan-out, AI Overviews vs AI Mode, la guía oficial de Google, qué se puede ignorar | 2 | Documento de una página: qué de lo que hago hoy Google dice que es inútil |
| 2 | **Los motores de respuesta y sus índices** — ChatGPT/Bing, Copilot, Perplexity, Gemini. Verificación en Bing WMT, IndexNow, `robots.txt` bot por bot | 2 | Sitio verificado en Bing WMT + IndexNow activo + `robots.txt` auditado |
| 3 | **Evidencia: qué funciona y qué no** — Princeton GEO vs C-SEO Bench, correlaciones de Ahrefs, el caso `llms.txt`. Cómo leer un estudio de vendor | 2 | Clasificación P/V/X de 10 afirmaciones tomadas de blogs SEO reales |
| 4 | **Intención de búsqueda y keyword research con IA** — mapeo intención→página, GSC como base, expansión con LLM, prompt research, localización por país | 3 | Mapa de 30 consultas clasificadas + set de 20 prompts propio |
| 5 | **On-page y contenido citable** — títulos, estructura respuesta-primero, cifras con fuente, autoría, contenido no-commodity | 3 | Un artículo publicado con el checklist completo |
| 6 | **SEO técnico mínimo viable** — indexación, Core Web Vitals reales, schema, JavaScript, facetas | 2 | Auditoría de indexación + CWV por plantilla, con 3 fixes priorizados |
| 7 | **E-commerce** — nombrar con palabras de compra, categorías, Product schema, Merchant Center, ChatGPT Shopping y ACP, marketplaces vs tienda propia | 3 | Una categoría y 5 fichas renombradas y con schema válido |
| 8 | **Medición, monitoreo y rutina** — GSC Generative AI, Bing AI Performance, GA4, baseline manual de prompts, cuándo pagar una herramienta, el flujo semanal | 2 | Planilla de baseline + calendario semanal personalizado |

**Proyecto final:** baseline documentado (mes 0) + 4 semanas de ejecución del flujo + informe de cambio en impresiones generativas, citaciones en Bing y tasa de mención en el set de prompts. Con la advertencia explícita de que **4 semanas no bastan para concluir causalidad** — parte del aprendizaje es saber qué no se puede afirmar.

**Materiales a producir:**
- Planilla de baseline de prompts (Google Sheets).
- Checklist de publicación (una página).
- Checklist técnico mínimo viable (una página).
- Plantillas de Product / Article / Organization / BreadcrumBList schema listas para pegar.
- Glosario español/inglés: los términos llegan en inglés y los alumnos necesitan poder leer la documentación original.

---

## 12. Qué cambió en 2025–2026 vs antes

| Área | Antes (≤2024) | 2025–2026 |
|---|---|---|
| **Postura oficial de Google** | Sin documentación sobre IA generativa | Guía formal (15 may 2026, act. 10 jul 2026): "AEO y GEO siguen siendo SEO", con lista explícita de tácticas a ignorar |
| **Medición de IA en Google** | Ninguna | *Generative AI performance report* en GSC (3 jun 2026), solo impresiones, datos desde 18 may 2026, sin API |
| **Medición de IA en Microsoft** | Ninguna | *AI Performance report* en Bing WMT (10 feb 2026, ampliado 16 jun 2026): citaciones + grounding queries, gratis |
| **Control sobre inclusión** | Todo o nada (`noindex`) | Toggle en Search Console para excluirse de AI Overviews / AI Mode / Discover AI sin salir del orgánico |
| **Objetivo del trabajo** | Posición en el top 10 | Ser una de 3–15 fuentes citadas. Solo ~17% de las fuentes de AIO están en el top 10 orgánico; 88% de las citaciones de AI Mode vienen de fuera del top 10 (Moz) |
| **Señales de autoridad** | Backlinks | Menciones de marca y presencia en YouTube correlacionan 2–3× más que backlinks (Ahrefs, 75k marcas) |
| **`llms.txt`** | No existía | Propuesto, hypeado, y descartado por evidencia: 97% sin una sola solicitud (Ahrefs, 137k sitios); Google declara que lo ignora |
| **Estado de GEO como técnica** | Solo el paper de Princeton (+40%) | C-SEO Bench (NeurIPS 2025) muestra que la mayoría de los métodos son inefectivos en condiciones multi-actor; SEO tradicional ~7,6× más efectivo |
| **Helpful Content System** | Sistema independiente | Integrado al núcleo desde marzo 2024. No se puede "esperar a que pase" |
| **Cadencia de core updates** | Meses de separación | Marzo y mayo 2026 con ~6 semanas de diferencia. Primer core update solo de Discover (feb 2026) |
| **Core Web Vitals** | FID | INP desde marzo 2024. Umbrales sin cambios en 2026: 2,5 s / 200 ms / 0,1 |
| **Compra dentro de ChatGPT** | No existía | Instant Checkout (2025) → OpenAI reconoce sus límites y **pivota a descubrimiento de producto** (24 mar 2026). ACP extendido a discovery |
| **Feeds para IA** | Solo Merchant Center | Schema propio de OpenAI: 79 campos, 19 obligatorios. Shopify integrado automáticamente. Merchant Center **no** alimenta ChatGPT |
| **AIO en consultas de compra** | Marginal | ~2,1% (nov 2025) → ~14% (mar 2026), sobre 20,9M de SERPs de shopping |
| **AI Mode en español** | No existía | Global desde ago 2025 (inglés), español LatAm desde sep 2025, pestaña permanente desde I/O 2026 |
| **Keyword research** | Volumen y dificultad | Volumen + **prompt research**: prompts de ~60 palabras vs búsquedas de 3,4 |

---

## 13. Fuentes principales

**Primarias**
- Google Search Central — *Optimizing your website for generative AI features on Google Search*: `developers.google.com/search/docs/fundamentals/ai-optimization-guide`
- Google Search Central Blog — *Introducing Search Generative AI performance reports in Search Console* (3 jun 2026)
- Google Search Central — *Guidance on using third-party SEO tools, services, and advice* (5 jun 2026)
- Google Search Status Dashboard — historial de ranking updates
- web.dev — *Web Vitals*, *Largest Contentful Paint*
- Bing Webmaster Tools — *AI Performance* (feb 2026, ampliado jun 2026)
- OpenAI — *Powering product discovery in ChatGPT* (24 mar 2026)
- OpenAI Help Center — *Shopping with ChatGPT Search*
- OpenAI Developers — Agentic Commerce Protocol: especificación de feed y guía de buenas prácticas
- Aggarwal et al., *GEO: Generative Engine Optimization*, KDD 2024
- Puerto, Gubri, Green, Oh, Yun, *C-SEO Bench: Does Conversational SEO Work?*, NeurIPS 2025 Datasets & Benchmarks (arXiv:2506.11097)

**Vendor (útiles, con incentivo comercial declarado)**
- Ahrefs — *Q1 2026 AI Search Benchmark Report* (13 estudios; 146M SERPs; 730k respuestas de IA); estudio de 75.000 marcas; estudio de `llms.txt` sobre 137.000 sitios; *Most-cited domains in ChatGPT* (Brand Radar)
- Semrush — *2026 AI Visibility Index* (126M prompts, ene–abr 2026); *AI Overviews Study* (10M+ keywords, 2025)
- Seer Interactive — estudios de CTR con AIO (sep 2025 y actualización 2026)
- BrightEdge — prevalencia y solapamiento de AIO
- Moz — 40.000 consultas en AI Mode
- SE Ranking — estudio de `llms.txt` (~300k dominios); comparativa Copilot/Perplexity
- Search Engine Land — análisis de 20,9M de SERPs de shopping
- Similarweb — *Generative AI Landscape*, *Generative AI Brand Visibility Index*

---

## 14. Tres cosas que el curso no debe prometer

1. **Recuperar el tráfico perdido por los AI Overviews.** La caída de CTR es estructural. Lo que se puede enseñar es a medir la exposición real, capturar la demanda que sí queda, y construir presencia donde la decisión se toma.
2. **Un método que garantice citaciones.** C-SEO Bench muestra que las ganancias se diluyen con la adopción. Es un juego de suma cero congestionado.
3. **Que las herramientas de terceros ven lo que ve Google.** Google lo dice textualmente: ninguna herramienta externa tiene acceso a sus sistemas internos de ranking o de IA.

Vender lo contrario es lo que está haciendo la mayoría de la oferta en la región. La honestidad metodológica es el diferenciador comercial del curso, no un costo.
