# TikTok Ads — Documento de investigación (agosto 2026)

**Alcance.** Estado de la plataforma publicitaria de TikTok a agosto de 2026: estructura de cuenta, tipos de campaña, formatos, subasta, medición, benchmarks, capa programática (Marketing API v1.3), capa agéntica (MCP / Agentic Hub), políticas, y contexto Chile / LATAM.

**Metodología y advertencias.** Las cifras de costo y rendimiento provienen de cohortes distintas (Triple Whale, Lebesgue, DigitalApplied, TikAdSuite, Stackmatix) y no son comparables entre sí; se presentan como rangos y con la fuente indicada. Las cifras de uplift de producto (Smart+, GMV Max) son reportadas por TikTok o por anunciantes en casos de estudio, no verificadas de forma independiente. Las especificaciones creativas y los límites de la API cambian con frecuencia: la documentación oficial es la fuente de verdad y debe verificarse antes de implementar.

---

## 1. Estado de la plataforma en 2026

**Resolución de la propiedad en EE.UU.** El 22 de enero de 2026 cerró la operación que transfirió el control de las operaciones estadounidenses a `TikTok USDS Joint Venture LLC`. Estructura reportada: Oracle, Silver Lake y MGX con ~15% cada uno (~45% combinado), otros inversionistas estadounidenses ~35%, ByteDance ~19.9%; es decir, ~80% en manos no chinas. Oracle actúa como socio de seguridad designado: aloja los datos de usuarios de EE.UU., audita el cumplimiento y supervisa un algoritmo reentrenado bajo jurisdicción estadounidense. Las cifras exactas de participación varían levemente entre fuentes (Bloomberg, Reuters, eMarketer, Forrester); la estructura general es consistente.

**Efecto operacional.** Prácticamente nulo en el corto plazo: cuentas publicitarias, Ads Manager y TikTok Shop siguieron funcionando sin interrupción. El efecto real fue de confianza presupuestaria: el gasto publicitario global en TikTok alcanzó ~US$5.800 millones en Q1 2026, +32% interanual, tras la reasignación de presupuestos que habían quedado en pausa durante 2025 (DigitalApplied).

**Consecuencia de segundo orden.** Un algoritmo reentrenado sobre datos estadounidenses implica que los benchmarks históricos de EE.UU. previos a 2026 tienen valor predictivo reducido. Para mercados fuera de EE.UU. (incluido Chile) la infraestructura de entrega no cambió.

---

## 2. Arquitectura de cuenta y jerarquía de objetos

Cinco niveles, rígidos, idénticos en UI y API:

| Nivel | Contiene | Decisiones que viven aquí |
|---|---|---|
| Business Center | Múltiples cuentas publicitarias, roles, permisos | Gobernanza multi-cliente / agencia |
| Advertiser (`advertiser_id`) | Campañas | Unidad de facturación y de autorización OAuth |
| Campaign | Grupos de anuncios | Objetivo publicitario, presupuesto de campaña |
| Ad Group | Anuncios | Segmentación, puja, calendario, emplazamientos |
| Ad | — | Creatividad (video/imagen), texto, CTA |

Un anuncio pertenece a exactamente un grupo, que pertenece a una campaña, que pertenece a un anunciante. No existe una llamada atómica de "lanzar campaña completa": la jerarquía *es* el flujo de trabajo (crear campaña → obtener ID → crear grupo → obtener ID → crear anuncio).

---

## 3. Tipos de campaña y automatización

La decisión estructural de 2026 no es "qué segmentación" sino "cuánta automatización".

### Smart+
Campaña automatizada de propósito general (equivalente funcional de Meta Advantage+ y Google Performance Max). Cubre tráfico, generación de leads, instalaciones de app y conversiones web. Automatiza segmentación, puja, emplazamiento y combinación creativa, con detección de fatiga y refresco automático de creatividades.

Cambio relevante de Q2 2026: la automatización pasó a ser **modular**. El anunciante puede activar o desactivar automatización por módulo (segmentación, presupuesto, emplazamientos, catálogo) y la UI marca con etiqueta `Smart+` qué módulos están automatizados. Smart+ Automatic Placement admite ahora selección manual de emplazamientos. Disponibilidad global anunciada para Q2 2026.

Cifras reportadas por TikTok / anunciantes (tratar como marketing, no como evidencia): +52% ROAS en campañas Smart+ Web optimizadas por valor; Ray-Ban, -50% CPA; PHLUR, +28% ROAS y -14% CPA al migrar a Smart+ y Search basada en intención.

### GMV Max
Exclusivo de TikTok Shop. Optimiza sobre señales orgánicas, pagadas y de afiliados de forma combinada, contra un objetivo de ROI. Dos variantes: Product GMV Max y LIVE GMV Max. Desde fines de 2025 es obligatorio para objetivos de venta en Shop y **eliminó los controles manuales de audiencia** (edad, género, intereses). Disponibilidad limitada por mercado (EE.UU. y Sudeste Asiático principalmente; no en Chile a la fecha).

Al desaparecer las palancas de audiencia, el control se reubica en: volumen y diversidad creativa, calidad del feed de productos (títulos, precios, imágenes, categorización), la oferta misma, y el ROI objetivo.

### Search Ads
Fuera de beta. Segmentación por palabras clave sobre el buscador interno de TikTok, con destino a cualquier sitio (Shopify, Amazon, TikTok Shop). Captura intención declarada, a diferencia de GMV Max que automatiza escala. TikTok reporta que una fracción significativa de usuarios inicia búsquedas dentro de los primeros segundos de abrir la app.

### Manual
Sigue existiendo y sigue siendo la opción correcta para testing sistemático de audiencias y creatividades donde se necesita controlar variables.

---

## 4. Formatos y emplazamientos

| Formato | Compra | Uso | Nota |
|---|---|---|---|
| In-Feed estándar | Subasta | Performance, base de casi toda la inversión | Skippable; depende íntegramente del gancho |
| Top Feed | Subasta | Primer slot publicitario del feed | Premium sin takeover completo |
| Spark Ads | Subasta | Amplificar publicación orgánica propia o de creador | Requiere código de autorización de 7 o 30 días; máx. 10.000 Spark ads por cuenta |
| TopView | Reserva | Awareness masivo | Takeover al abrir la app; costo fijo; creatividades pre-aprobadas y no reemplazables una vez iniciada la carga |
| TopReach | Reserva | TopView + TopFeed en una sola compra | Novedad 2026; admite secuenciación narrativa entre ambos slots |
| TikTok Pulse (Core / Premiere) | Reserva & Frecuencia | Adyacencia a contenido trending brand-safe | Actualización de performance en 2026 (View+, por allowlist en EE.UU./Canadá) |
| Carousel / Collage Carousel | Subasta | Catálogo, múltiples productos en el primer frame | Collage Carousel inicialmente solo EE.UU. |
| Playable / Branded Effects / Branded Mission | Mixto | Engagement, gaming, activación de creadores | — |
| Search Hubs | Reserva | Página de marca en resultados de búsqueda | — |
| Streaming Ads / Growth Max: Mini Games | Nuevos | Suscripciones, juegos in-app | Lanzamientos 2026 |

**Especificaciones creativas base (In-Feed / Spark).** Vertical 9:16 recomendado, ≥540×960 px (recomendado 1080×1920). Formatos `.mp4`, `.mov`, `.mpeg`, `.3gp`, `.avi`. Duración: sin límite estricto en In-Feed de subasta; 9–15 s es el rango de mayor engagement. Imagen de perfil 98×98 px, <50 KB, con información clave dentro de 66×66 px. Texto visible hasta ~4 líneas antes de "ver más". Sin marcas de agua (incluida la propia de TikTok) y sin imitar elementos de la UI de TikTok. TopView: 9:16 obligatorio, 5–60 s (9–15 s recomendado), bitrate ≥2.500 kbps, hasta 500 MB, respetando zonas seguras de takeover y de feed.

---

## 5. Subasta, presupuestos y fase de aprendizaje

- Mínimos en Ads Manager: **US$50/día a nivel campaña, US$20/día a nivel grupo de anuncios**.
- Presupuesto práctico de arranque para campañas optimizadas a conversión: US$3.000–5.000/mes. Por debajo de ese nivel el grupo de anuncios no acumula los ~50 eventos de conversión semanales necesarios para salir de la fase de aprendizaje, y queda en aprendizaje permanente con CPM inflado.
- Modelos de compra: CPM (métrica de control: VTR a 3 y 6 segundos), CPC (métrica: CTR), oCPM/conversión (métrica: CPR — costo por resultado). Comparar CPM de una fuente contra CPV de otra produce benchmarks sin sentido.
- Frecuencia: por debajo de 3 la tasa de conversión cae; por encima de 6 el CTR se deteriora y la fatiga creativa se acelera (DigitalApplied).
- La causa más común de fracaso reportada no es la calidad creativa sino la elección incorrecta de estrategia de puja durante el setup.

---

## 6. Medición

**Pixel + Events API (CAPI).** El Events API envía eventos de conversión servidor a servidor. No es opcional en 2026: la señal de navegador se erosiona por privacidad, bloqueadores y restricciones de cookies, y la optimización de TikTok es tan buena como la señal de conversión que recibe. Un stack que instrumenta el pixel pero no CAPI entrega la mitad del ciclo de retroalimentación.

**Atribución.** La ventana por defecto reportada en 2026 es **7 días clic + 1 día view**, metodología que hace comparable el ROI de plataforma con Meta y Google por primera vez. Antes de comparar cifras entre plataformas, verificar que la ventana sea la misma; la mayoría de las discrepancias de ROAS que se atribuyen a "rendimiento" son diferencias de ventana.

**Reportería.** Dos modos en la API: síncrono (resultados acotados, respuesta inmediata) y asíncrono (rangos largos, muchas dimensiones; se crea una tarea, se hace polling, se descarga). Elegir mal el modo es la principal causa de agotamiento de cuota.

---

## 7. Benchmarks (rangos, no puntos)

| Métrica | Rango 2026 | Fuente / cohorte |
|---|---|---|
| CPM | US$4,80 (campañas amplias, Lebesgue) – US$9,16 (in-feed, DigitalApplied/WebFX) – US$13,26 (e-commerce, Triple Whale) | Tres cohortes distintas |
| CPM por vertical | US$5,20 (entretenimiento) – US$15–25 (finanzas/seguros) | Rango de ~3,5× |
| CPC | ~US$1,02 cross-industry; belleza US$0,74, retail US$0,79; finanzas US$1,71, legal US$1,92 | Stackmatix / TikAdSuite |
| CTR | 0,6% (awareness/amplio) – 1,77% (cohorte conversión). In-feed e-commerce típico 0,9–1,2%; Spark Ads ~2,4× in-feed; TopView 12–16% | Varias |
| CVR | ~2,0% mediana; Shop product ads 3,7%, Spark 2,6%, in-feed 1,8% | Triple Whale / TikAdSuite |
| CPA | Mediana US$32,74; la mayoría de categorías DTC bajo US$22 | Triple Whale |
| ROAS | Mediana 2,21; referencia práctica ≥2,5× para e-commerce | Triple Whale / AGrowth |

**Lecturas relevantes.** (1) TikTok sigue más barato que Meta en CPM y CPC, pero la brecha se cierra: el CPM subió ~16% en el último ciclo. (2) El problema resuelto en 2025 fue el clic; el no resuelto es la conversión — velocidad de landing, claridad de oferta y prueba social son el trabajo de optimización de 2026. (3) La correlación CPC alto → CPA alto sugiere que un CPA débil suele ser síntoma de gancho débil, no de audiencia cara.

---

## 8. Capa programática: Marketing API v1.3

- **Base:** `https://business-api.tiktok.com/open_api/v1.3/`. La versión va en el path, no en header.
- **Respuestas:** JSON con envoltorio consistente (`code`, `message`, `request_id`, `data`). `code: 0` = éxito. El manejo de errores debe basarse en `code`, **no** en el status HTTP, que suele ser 200 incluso en errores de aplicación.
- **Auth:** OAuth 2.0 de autorización de anunciante. Registro de app en TikTok for Developers (App ID + secret) → redirección del anunciante → `auth_code` → intercambio en `POST /oauth2/access_token/` → `access_token` + **lista de `advertiser_id` autorizados**. Cada request lleva el token en header `Access-Token` y nombra el `advertiser_id`.
- **Grupos de endpoints:** CRUD de campaña/grupo/anuncio; reportería; carga de creatividades; audiencias (custom y lookalike); Events API; Business Center.
- **SDK oficial:** JavaScript, Python, Java y Go (`tiktok/tiktok-business-api-sdk`).
- **Rate limits:** existen, son por endpoint y por ventana temporal, y la reportería es el camino más restringido. Las cifras concretas que circulan en la comunidad (~1.000 requests/día, ≤100 ítems por página) **no deben tratarse como verificadas**; consultar la página oficial de rate limits por endpoint y por tier de cuenta. Lo estable es la forma de la restricción, no el número.
- **Acceso:** es la API de paid social más gateada del mercado. Requiere onboarding a Business Center, revisión de app sandbox→producción, verificación de negocio para volumen alto y una auditoría de cumplimiento de seguridad de datos. Comparativamente, Snapchat es abierta y Pinterest tiene un gate intermedio (Trial → Standard).

---

## 9. Capa agéntica: MCP, Agentic Hub y Ads Skills

**Cronología.**
- **12–13 mayo 2026 (TikTok World '26):** anuncio del TikTok Ads MCP Server y del toolkit TikTok Ads Skills. TikTok fue la última de las cuatro grandes plataformas publicitarias en comprometerse con una capa MCP, después de Google, Meta y Amazon. Claude y ChatGPT se mencionaron explícitamente como clientes de ejemplo.
- **Junio 2026:** el anuncio aún no era producto disponible de forma general.
- **30 junio 2026:** lanzamiento de **Agentic Hub**, marketplace de AI Skills construido sobre **TikTok for Business MCP**. Documentación oficial en `business-api.tiktok.com/portal/docs/tiktok-ads-mcp-server/v1.3`.

**Qué es exactamente.** MCP permite que un agente interactúe con TikTok Ads sin credenciales de API ni código: gestión de campañas, reportería de rendimiento, gestión creativa y catálogo. Tres rutas de adopción, explícitamente soportadas:
1. Adoptar una Skill empaquetada del Hub (primera parte o terceros: HubSpot, Wix, Constant Contact, WorkMagic, Innovid, Kochava, Shoplazza, MADHOUSE, Mobvista, HuntMobi, Cyberklick, Storyverse, BELLNOVA, AI Rudder).
2. Construir Skills y flujos propios sobre MCP.
3. Conectar el agente propio directamente al servidor MCP, sin Skill intermedia.

**Estado real de madurez.** Las Skills publicadas al lanzamiento son deliberadamente estrechas: una tarea por Skill (escaneo de cumplimiento, reasignación de presupuesto, scorecard creativo, sincronización de catálogo). Ninguna reclama autoridad de gasto desatendida de extremo a extremo. El patrón operativo dominante es *aprobación humana antes de cada escritura*, no autonomía completa.

**Lo que esto implica técnicamente.** Todo MCP de TikTok Ads —el oficial y los de terceros en GitHub (`AdsMCP/tiktok-ads-mcp-server`, `ysntony/tiktok-ads-mcp`)— es, por debajo del protocolo, un wrapper sobre la Marketing API v1.3. Las capacidades del agente están acotadas por lo que v1.3 permite y su velocidad real por los rate limits de v1.3. La pregunta útil no es "qué MCP" sino "qué permite la API subyacente".

**Consideraciones de diseño para automatización agéntica:**
- **El token es el radio de impacto.** Un agente solo puede ver y modificar los `advertiser_id` que su token autorizó. Autorizar de forma estrecha (un cliente, un conjunto de cuentas) acota el daño posible antes de escribir cualquier guardrail propio.
- **Escrituras detrás de compuertas.** Lecturas continuas (estado, gasto, pacing) + escrituras acotadas y aprobadas (pausas, cambios de presupuesto) es el patrón que hoy soportan tanto el ecosistema como el nivel de confianza del mercado.
- **Higiene de datos como precondición.** Convenciones de nombres, etiquetas creativas, reglas de presupuesto y bucles de medición definidos *antes* de escalar automatización. Un agente sobre datos sucios acelera la confusión en lugar de reducirla.
- **Velocidad = problema de scheduling.** Batching de lecturas, paginación disciplinada, asíncrono para pulls pesados, backoff ante error de cuota.
- **La automatización de plataforma reduce el espacio de decisión.** Con Smart+ y GMV Max absorbiendo segmentación y puja, el valor diferencial de un sistema agéntico se desplaza hacia: suministro y diversidad creativa, calidad del feed de productos, definición de objetivos de ROI, y QA de medición. Optimizar pujas manualmente es cada vez menos donde está la ventaja.

---

## 10. Políticas publicitarias y revisión

Proceso en dos etapas:
1. **Acceso sectorial:** verificación de que el producto o servicio puede anunciarse en el mercado objetivo.
2. **Revisión creativa y de landing:** texto, visuales, coherencia con la página de destino.

Plazo típico: la mayoría de los anuncios se revisan dentro de 24 horas.

- **Prohibidos globalmente (ejemplos):** animales, partes o derivados; productos y servicios sexuales para adultos; tabaco y cigarrillos.
- **Restringidos (varían por país):** alcohol, loterías, medios de comunicación, productos y servicios para menores, farmacéutica/salud, apps de citas, productos financieros. Pueden requerir documentación adicional, avisos en el anuncio o restricción etaria.
- **Restricciones específicas por mercado:** por ejemplo, productos HFSS (altos en grasa, azúcar o sal) restringidos a 18+ en Australia, Irlanda, Noruega, Nueva Zelanda, Portugal y Reino Unido, y prohibidos en otro grupo de mercados. Existen políticas particulares para servicios legales (excluye derecho de familia, migratorio, laboral y lesiones personales).
- Rechazo: el motivo aparece en la lista de anuncios; existe "Solicitud de revisión en un clic".
- Existen programas piloto sectoriales y pruebas alfa/beta que modifican estas políticas para participantes específicos, bajo confidencialidad.

**Implicancia para automatización:** la revisión es un estado asíncrono del objeto `Ad`. Cualquier sistema que lance creatividades a escala necesita suscripción a webhooks de estado de revisión y una política de reintento/corrección, no solo lógica de creación.

---

## 11. Contexto Chile y LATAM

**Presencia local.** TikTok inició operación directa en Chile durante el último trimestre de 2025, con un equipo de ~15 personas dedicado al mercado chileno pero con base en Argentina. La gerencia general de Cono Sur y México (Astrid Mirkin) reporta más de 13 millones de usuarios en Chile y proyecta crecimiento de triple dígito para TikTok for Business durante 2026.

**Tamaño de audiencia — precaución metodológica.** Las cifras de "alcance publicitario" que publican las herramientas de TikTok y que DataReportal replica (~16,2 millones de adultos alcanzables a fines de 2025) no equivalen a usuarios activos y, contrastadas con la población adulta chilena, son claramente infladas. La propia fuente advierte la distinción. Para planificación, usar la cifra de usuarios (>13 millones) y tratar el alcance publicitario como techo teórico.

**Mercado.** La inversión digital pasó de 51,1% (2023) a 54% (2025) del gasto total en medios en Chile (IAB Chile). La Cámara de Comercio de Santiago estima ventas online cercanas a US$10.000 millones en 2025, con 12,6% de penetración del e-commerce sobre retail, y proyecta ~US$10.600 millones para 2026.

**TikTok Shop.** No está lanzado en Chile y **no hay fecha oficial**. Señales: operación directa iniciada, testing con un grupo cerrado de creadores >50.000 seguidores desde principios de 2026, y apertura de registro de vendedores en la versión global. Ya opera en México y Brasil. Escala de referencia: GMV en EE.UU. estimado en US$15.100–15.820 millones en 2025 (Momentum Works / EMARKETER, metodologías distintas), con proyección >US$23.000 millones para 2026; GMV global ~US$64.300 millones.

**Ley 21.719 (protección de datos).** Publicada el 13 de diciembre de 2024, entra en vigencia plena el **1 de diciembre de 2026**. Reemplaza la Ley 19.628 (1999) y se modela sobre GDPR. Puntos con impacto directo sobre operaciones publicitarias:
- Crea la Agencia de Protección de Datos Personales (APDP), con facultades de fiscalización y sanción.
- Derechos ARCO completos más portabilidad y **derecho a impugnar decisiones automatizadas** tomadas por algoritmos o sistemas de IA.
- Notificación obligatoria de brechas.
- Multas de hasta 20.000 UTM o hasta 4% de los ingresos anuales en reincidencia.
- Empresas de menor tamaño (Ley 20.416) reciben amonestación escrita en lugar de multa durante los primeros 12 meses (dic 2026 – dic 2027).

**Traducción operativa para stacks publicitarios:** base legal y consentimiento documentado para pixel y Events API; DPAs con procesadores; inventario de datos y logs auditables (la fiscalización es sobre evidencia operativa, no sobre políticas escritas); revisión de audiencias personalizadas construidas con datos de clientes; y — relevante para sistemas agénticos — trazabilidad de decisiones automatizadas que afecten a titulares de datos.

---

## 12. Riesgos y puntos abiertos

| Riesgo | Naturaleza |
|---|---|
| Compresión de márgenes en la subasta | CPM en alza sostenida; la ventaja de costo frente a Meta se erosiona trimestre a trimestre |
| Opacidad de la automatización | Smart+ y GMV Max reducen observabilidad; menos capacidad de diagnóstico cuando el rendimiento cae |
| Dependencia de plataforma en la capa agéntica | Construir sobre MCP oficial concentra riesgo en un roadmap que TikTok controla y puede cambiar |
| Gating de la API | Aprobación, verificación de negocio y auditoría de seguridad pueden bloquear o retrasar acceso productivo |
| Volatilidad post-JV en EE.UU. | Algoritmo reentrenado y gobernanza nueva; benchmarks históricos de EE.UU. de valor reducido |
| Cumplimiento Ley 21.719 | Deadline duro en diciembre 2026 con fiscalización basada en evidencia |
| Disponibilidad regional | GMV Max, Collage Carousel, View+ y otras funciones tienen rollout por mercado; no asumir paridad en Chile |

---

## 13. Fuentes

**Oficiales**
- TikTok Ads Manager — Centro de ayuda: https://ads.tiktok.com/help/?lang=es
- Smart+: https://ads.tiktok.com/help/article/about-smart-plus-campaign?lang=es
- GMV Max: https://ads.tiktok.com/help/article/about-gmv-max-campaigns-in-tiktok-ads-manager?lang=es
- In-Feed de subasta (specs): https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads?lang=es
- TopView (specs): https://ads.tiktok.com/help/article/tiktok-reservation-topview?lang=es
- Políticas publicitarias: https://ads.tiktok.com/help/article/tiktok-advertising-policies?lang=es
- FAQ de revisión de anuncios: https://ads.tiktok.com/help/article/ad-review-faq?lang=es
- API for Business — portal de documentación: https://business-api.tiktok.com/portal/docs
- Marketing API v1.3: https://business-api.tiktok.com/portal/docs/marketing-api/v1.3
- TikTok Ads MCP Server: https://business-api.tiktok.com/portal/docs/tiktok-ads-mcp-server/v1.3
- Agentic Hub (anuncio): https://ads.tiktok.com/business/en/blog/tiktok-agentic-hub-ai-agents-skills-mcp
- Product Preview Q2 2026: https://ads.tiktok.com/business/en-US/blog/tiktok-product-preview
- SDK oficial: https://github.com/tiktok/tiktok-business-api-sdk

**Análisis y prensa**
- Digiday — lanzamiento del MCP server: https://digiday.com/marketing/tiktok-launches-mcp-server-to-let-ai-agents-run-campaigns/
- MediaPost — marketplace agéntico: https://www.mediapost.com/publications/article/416253/tiktok-launches-agentic-marketplace-for-ad-partner.html
- Soku — Marketing API v1.3 explicada: https://soku.ai/blog/tiktok-marketing-api-v1-3-explained
- DigitalApplied — Agentic Hub / benchmarks / brand safety post-JV: https://www.digitalapplied.com/blog/tiktok-agentic-hub-ai-agents-ad-workflows-2026
- Forrester — cierre del JV en EE.UU.: https://www.forrester.com/blogs/tiktok-seals-the-deal-with-new-us-joint-venture/
- eMarketer — implicancias para anunciantes: https://www.emarketer.com/content/tiktok-s-us-overhaul-gives-advertisers-greater-certainty--though-questions-remain
- Adfirm — playbook Smart+ / GMV Max: https://www.adfirm.net/blog/tiktok-smart-plus-campaigns-2026/
- Influee — benchmarks y specs: https://influee.co/gb/blog/tiktok-ads-benchmarks

**Chile / LATAM**
- La Tercera — operación directa en Chile: https://www.latercera.com/pulso/noticia/tiktok-inicia-operacion-directa-en-chile-ya-tiene-13-millones-de-usuarios-en-el-pais/
- ANDA — TikTok Shop y e-commerce chileno: https://anda.cl/tiktok-shop-se-acerca-a-chile-desafio-para-el-e-commerce/
- Diario Financiero — TikTok Shop: https://www.df.cl/senal-df/tiktok-shop-el-e-commerce-del-gigante-chino-que-se-acerca-a-chile
- Ley 21.719 — texto y guías: https://wikiguias.digital.gob.cl/datos-personales/guia-practica-implementacion-nueva-ley-datos-personales
