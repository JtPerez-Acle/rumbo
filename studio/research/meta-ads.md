# Meta Ads — Documento de investigación

**Fecha de compilación:** 3 de agosto de 2026
**Ámbito:** plataforma publicitaria de Meta (Facebook, Instagram, Messenger, WhatsApp, Audience Network) — arquitectura de entrega, estructura de campaña, señales, medición, superficie de API, costos y marco regulatorio.

---

## 0. Método y advertencias sobre las fuentes

Este documento combina tres tipos de fuente, con distinto grado de confiabilidad:

| Tipo | Ejemplos | Confiabilidad |
|---|---|---|
| Primaria (Meta) | blog de ingeniería, changelog de Graph/Marketing API, Business Help Center, blog de desarrolladores | Alta |
| Prensa especializada | Search Engine Land, PPC Land, Social Media Today, CNBC, Reuters | Media-alta |
| Blogs de vendors y agencias | proveedores de herramientas de ads, agencias de performance | Baja a media — con conflicto de interés estructural |

Los **benchmarks de costo** (sección 10) provienen casi enteramente del tercer grupo. Se incluyen como orden de magnitud, no como referencia auditada. Cualquier cifra de "lift" publicada por Meta sobre sus propios productos debe tratarse como marketing hasta contrastarla con un experimento propio.

Cuando una afirmación no pudo verificarse en fuente primaria, está marcada como **[no verificado]**.

---

## 1. Cambio estructural: de plataforma configurable a sistema de recomendación

El cambio más relevante de los últimos 24 meses no es un producto nuevo, sino la sustitución del motor de entrega. Meta reemplazó una arquitectura de cientos de modelos pequeños —cada uno optimizado para un objetivo y una superficie— por una jerarquía de modelos grandes que generalizan entre objetivos.

La consecuencia operativa: **la mayoría de los controles que un anunciante manipula hoy son entradas al modelo, no restricciones sobre él.** Segmentación por intereses, públicos similares y ubicaciones manuales pasaron de ser reglas duras a ser señales.

### Capas del sistema

**Lattice** — arquitectura de ranking unificada. Sustituye modelos verticales separados por una sola arquitectura que aprende de forma cruzada entre objetivos y superficies. El rendimiento en Reels informa el ranking en Feed.

**Andromeda** — motor de recuperación (*retrieval*). Selecciona el conjunto de anuncios candidatos —del orden de miles, desde millones— antes de que entren a la subasta. Su despliegue global se completó en octubre de 2025. Opera en sentido inverso al modelo clásico: en vez de partir del público definido por el anunciante, evalúa primero el creativo, el formato y el historial de interacción, y desde ahí predice qué usuarios calzan.

**GEM (Generative Ads Recommendation Model)** — modelo fundacional entrenado a escala de LLM sobre miles de GPUs. Meta publicó el detalle técnico el 10 de noviembre de 2025. No sirve anuncios directamente: es demasiado costoso en inferencia. Funciona como *maestro* en un esquema de destilación de conocimiento, transfiriendo aprendizaje a Lattice, Andromeda y los modelos verticales. Meta reporta que es 4× más eficiente en generar mejoras de rendimiento por unidad de datos y cómputo que sus modelos de ranking originales, con incrementos de conversión reportados de hasta 5% en Instagram y 3% en Facebook Feed durante el despliegue inicial.

**Adaptive Ranking Model** — capa de infraestructura publicada por Meta Engineering el 31 de marzo de 2026. Resuelve el problema de latencia: ejecutar modelos de escala billonaria (10¹²) en menos de 100 ms por impresión, miles de millones de veces al día. Incluye cuantización selectiva FP8 y asignación dinámica de cómputo.

### Implicancias directas

1. **El creativo hace el trabajo de segmentación.** Un anuncio que expresa un problema específico le da al sistema una señal precisa contra la cual hacer matching. Un anuncio genérico no.
2. **La similitud entre creativos importa.** Cambiar el color del CTA o el titular no registra como creativo nuevo. Para que el sistema lo trate como una variante distinta hay que cambiar elementos estructurales: talento, narrativa, y sobre todo los primeros segundos del video, que el sistema pondera con fuerza. **[parcialmente verificado — la lógica es consistente con la arquitectura publicada, pero el detalle de ponderación proviene de análisis de terceros]**
3. **Los períodos de aprendizaje son reales, no una convención.** El sistema necesita observar secuencias de usuario para calibrar.

---

## 2. Estructura de campaña en 2026

### Advantage+ como camino por defecto

Meta unificó los flujos de creación manual y Advantage+ en una sola interfaz. Los objetivos Sales, App y Leads llegan por defecto a la configuración automatizada. Esto no es un cambio de UI: es la eliminación progresiva del camino manual.

La estructura evolucionó respecto de la versión original de 2022:

- **Volvieron los conjuntos de anuncios.** La estructura plana original (hasta 150 anuncios sin ad sets) fue reemplazada por campañas con ad sets, cada uno con un tope del orden de 50 anuncios. Esto devuelve flexibilidad para segmentar por oferta, línea de producto o tipo de creativo.
- **Presupuesto a nivel de campaña.** Es lo que habilita la reasignación dinámica. Cambiar a presupuesto por ad set solo tiene sentido cuando se requiere aislamiento estricto de gasto.
- **Reels priorizado por defecto** en la distribución de ubicaciones, salvo que el creativo no renderice correctamente en ese formato. **[fuente secundaria]**

### Fase de aprendizaje

El umbral operativo reportado para 2026 es de aproximadamente **50 eventos de optimización por semana** por ad set o campaña, con duración típica de 7 a 14 días y hasta 21 en mercados de bajo volumen. Durante la fase de aprendizaje el CPA suele correr 20–50% por sobre el promedio posterior.

Regla práctica derivada: el presupuesto diario × 7 debe ser capaz de generar 50 conversiones. Si no lo es, la campaña no saldrá de aprendizaje y el gasto se consume en exploración.

Para *Value Optimization* y puja por pLTV dentro de Advantage+ Sales, el umbral reportado bajó a 30–50 eventos de compra de alto valor por semana. **[fuente secundaria]**

Toda modificación significativa —presupuesto, público, creativo— reinicia la fase. El error operativo más común y más caro es apagar campañas a los 2–3 días por CPA alto.

### Estructura recomendada

El patrón que reportan operadores con volumen: Advantage+ para prospecting escalado y retargeting; campañas manuales reservadas como banco de pruebas para conceptos creativos nuevos, productos nuevos y nichos específicos, cuyos ganadores luego se inyectan al sistema automatizado.

Para campañas manuales, la regla de 2026 es 3–5 ángulos creativos únicos por ad set como máximo. Más de 5 diluye presupuesto y confunde la señal de optimización.

---

## 3. Segmentación

Advantage+ Audience es el comportamiento por defecto. La segmentación detallada funciona como **sugerencia**, no como restricción: el sistema expandirá más allá de la definición del público si las señales del creativo indican mejor calce en otra parte.

Consecuencia contraintuitiva pero consistente con la arquitectura: **la segmentación estrecha tiende a subir el CPM sin mejorar el resultado**, porque restringe el espacio de recuperación de Andromeda sin aportar información que el sistema no pueda inferir del creativo y de las señales de conversión.

Lo que sí sigue teniendo peso como entrada:
- **Datos propios (first-party).** Listas de email, eventos de píxel, CAPI. Su valor relativo subió a medida que bajó el de los intereses de terceros.
- **Exclusiones.** Siguen operando como restricción dura en la mayoría de los casos.
- **Categorías especiales de anuncios** (crédito, empleo, vivienda, temas sociales/electorales/políticos), que imponen restricciones regulatorias sobre segmentación.

En Marketing API v26.0 el flag de Advantage+ Audience debe fijarse explícitamente; las llamadas que lo omitan fallan.

---

## 4. Señales: Pixel, Conversions API y calidad de match

Toda decisión de entrega se apoya en la calidad y completitud de los datos que llegan a Events Manager. Es la capa donde una implementación mediocre destruye rendimiento sin dejar rastro visible en Ads Manager.

### Pérdida de señal del lado del navegador

Fuentes acumulativas de pérdida: ATT en iOS, ITP de Safari, bloqueo de cookies de terceros, extensiones de bloqueo, y marcos de consentimiento que impiden que el JavaScript se ejecute. Las estimaciones de terceros ubican la pérdida de eventos client-side en el rango de 25–40% para el anunciante promedio. **[fuente secundaria — la cifra varía mucho por vertical y mezcla de dispositivos]**

### Conversions API (CAPI)

Envío servidor-a-servidor que evita el navegador. En 2026 Meta lo recomienda para todo anunciante con inversión activa. Meta reporta un 17,8% menor costo por resultado para anunciantes que usan CAPI en eventos web (cifra del propio Meta; tratar como tal).

Cambios de 2026 relevantes:
- **Setup de CAPI en un clic**, liberado en abril de 2026, para eventos web estándar. No cubre eventos personalizados, conversiones offline ni ruteo multiplataforma.
- **Pixel asistido por IA**, que enriquece automáticamente los eventos con detalles de producto y página. Se activó por defecto tras una ventana de revisión de 30 días; en la mayoría de las cuentas elegibles ya está operando. Conviene verificar su estado en Events Manager y establecer una línea base de calidad de evento antes/después.

### Event Match Quality (EMQ)

Puntaje de 0 a 10 que mide con qué confianza Meta puede asociar un evento a una persona. Depende enteramente de los parámetros de identificación enviados, todos hasheados con SHA-256: email (`em`), teléfono (`ph`), `fbc` (Facebook Click ID, capturado desde el parámetro `fbclid` y guardado en la cookie `_fbc`), `fbp`, IP, user agent, nombre, dirección.

Rangos reportados por operadores:

| Configuración | EMQ típico |
|---|---|
| Solo email | 5,5 – 6,5 |
| Email + teléfono | 7,5 – 8,0 |
| Email + teléfono + `fbp` + `fbc` | 8,5 – 9,0 |
| Lo anterior + nombre y dirección | 9+ |

Piso práctico: 7,0. Bajo eso, el match no aporta lo suficiente para mejorar la optimización.

### El error de deduplicación

Es el fallo más frecuente y el más silencioso. Si el `event_id` no es idéntico entre el evento del navegador y el del servidor, las conversiones se cuentan dos veces. El resultado: ROAS inflado, y un modelo de puja entrenado sobre datos corruptos.

Corrección: generar un único UUID al inicio del checkout, guardarlo en sesión, y pasarlo tanto al parámetro `eventID` de `fbq()` como al campo `event_id` del payload de CAPI. Si Events Manager muestra el doble de las compras reales, el pareo está roto.

---

## 5. Atribución: qué cambió y qué significa

2026 trajo dos cambios que rompieron la mayoría de los dashboards. **El rendimiento no cambió; cambió la medición.** Distinguir una cosa de otra es la primera obligación analítica de cualquier operación sobre Meta este año.

### Enero de 2026

El 12 de enero Meta **eliminó de forma permanente las ventanas de atribución de 7 días vista y 28 días vista** de la Ads Insights API. No se pueden solicitar ni siquiera vía API. Las conversiones que antes caían en esas ventanas simplemente dejaron de atribuirse. El impacto se concentra en campañas de awareness y video, donde el usuario ve el anuncio y convierte después sin hacer clic.

En la misma fecha se añadieron límites de retención: 13 meses para desgloses únicos y horarios, 6 meses para frecuencia, y los desgloses de marketing mix modeling pasaron a jobs asíncronos exclusivamente.

### Marzo de 2026

- El **click-through se redefinió como solo clic en enlace**. Las interacciones sociales dejaron de contar como clic.
- Se introdujo **engage-through attribution** (1 día), que captura interacciones sociales y visualizaciones de video. El umbral de visualización bajó de 10 a 5 segundos, calibrado para Reels en lugar de video largo de Feed.

Caídas reportadas en conversiones registradas tras ambos cambios: 15–40%. **[fuente secundaria; la dispersión es amplia según mezcla de campañas]**

**Configuración por defecto en 2026:** 7 días clic, 1 día engage-through, 1 día vista, modelo estándar.

### Atribución incremental

Opción avanzada que usa modelado causal entrenado sobre la biblioteca de estudios de Conversion Lift de Meta, para estimar qué conversiones fueron efectivamente *causadas* por el anuncio. Al seleccionarla se pierde la capacidad de editar ventanas de atribución, porque no opera con ventanas temporales.

Requiere objetivos elegibles con ubicación de conversión en sitio web y meta de rendimiento *maximize conversions* o *maximize value*.

Cifras publicadas por Meta: lift promedio de 46% en conversiones incrementales (Q1 2025), y +24% en conversiones incrementales tras la actualización del modelo de enero de 2026.

**Contraste independiente:** Seer Interactive testeó atribución incremental sobre USD 1,05M de inversión en 6+ cuentas. Meta reportó que 87% de las conversiones eran incrementales; el cruce contra GA4 dio 67%. Brecha de 20 puntos porcentuales. El mejor desempeño incremental se dio en públicos de mid-funnel refinados; el peor, en targeting amplio y retargeting hiperestrecho.

Recomendación operativa observable en la práctica: usarla como *una* lente, no como verdad. Es mejor default para anunciantes de presupuesto alto con volumen sobrado de conversión; contraproducente para cuentas que aún luchan por salir de la fase de aprendizaje, donde el holdout retira datos que no sobran.

### Marco de tres números

| Número | Uso |
|---|---|
| ROAS de plataforma | Comparar campañas *dentro* de Meta |
| ROAS blended / MER | Decisiones de presupuesto y escalamiento |
| Lift incremental (experimento propio) | Determinar si la campaña causa conversiones |

El ROAS de Meta nunca va a coincidir con GA4 ni con Shopify. Es estructural: solapamiento de atribución, definiciones distintas de conversión y modelado distinto de los datos perdidos en iOS. La reconciliación es imposible por diseño; intentarla consume tiempo sin producir información.

---

## 6. Creativo

### Volumen y diversidad

Los operadores con datos agregados reportan que el sistema requiere del orden de **15–50 creativos activos** para optimizar correctamente, y ritmos de prueba de 15–25 creativos nuevos por semana en cuentas de alto rendimiento. **[fuente secundaria]**

La razón es arquitectónica, no arbitraria: si se entrega un solo concepto creativo, el sistema solo puede calzarlo con un tipo de usuario en un punto de su recorrido. Más conceptos distintos amplían el espacio de secuenciación.

**Frecuencia:** mantener bajo ~3,4. El CTR cae fuerte pasadas 4+ exposiciones. **[fuente secundaria]**

### Herramientas generativas de Meta

Meta reporta más de 8 millones de anunciantes usando al menos una de sus herramientas de creativo generativo.

**Muse Image** (Meta Superintelligence Labs, julio de 2026) llegó primero a Meta AI, Instagram Stories y WhatsApp, con acceso para anunciantes y agencias vía Advantage+ Creative. Capacidades relevantes para producción publicitaria: generación de fondos alrededor de imágenes de producto, variantes de imagen lifestyle inspiradas en anuncios existentes, y generación de estáticos a partir de creativo en video. Meta lo describe con razonamiento visual agéntico y auto-refinamiento, orientado a interpretar briefs en lugar de keywords sueltas.

**Muse Video** está anunciado pero no es de producción. **[no verificado como disponible]**

Toda salida generativa debe pasar por los mismos dos filtros que cualquier otro asset: las especificaciones de formato de Meta y la política de etiquetado de contenido generado por IA.

### Riesgos de gobernanza creativa

Automatizar la generación de variantes multiplica los modos de falla, no solo el volumen:
- Representaciones engañosas: características implicadas visualmente que el producto no entrega.
- Inconsistencia de packaging o color, que erosiona confianza y sube devoluciones.
- Likeness humano sintético sin divulgación (ver sección 9).

Cualquier pipeline que genere creativo a escala necesita una compuerta de revisión antes del upload, no después de la denuncia.

---

## 7. Superficie técnica: Marketing API

### Estado de versiones

- **v26.0** — Graph API y Marketing API, liberadas el **29 de julio de 2026**. Es el batch de deprecaciones más agresivo del año en el lado de ads.
- **v25.0** — liberada el 18 de febrero de 2026.
- **v23.0** — expiró el 9 de junio de 2026.

Cadencia: nueva versión cada ~6 meses; cada versión corre un reloj de aproximadamente 2 años. Las llamadas sin versión explícita se rutean a la versión "default", que no siempre es la última. **Especificar la versión en cada llamada.**

### Deprecaciones que afectan a la cuenta, no solo al código

Con v26.0:
- **Instagram Explore Feed eliminado como ubicación publicitaria.** Toda campaña que lo tuviera hardcodeado redistribuye a otras ubicaciones.
- **El flag de Advantage+ Audience debe fijarse explícitamente**, o la llamada falla.
- **Shop Ads** por defecto a destino web-y-shop, salvo opt-out explícito.
- Deprecados: creación de anuncios tipo poll, ubicación Messenger Stories.
- Prohibidos los destinos solo-web en campañas Web-plus-App.
- **Campos de Delivery Estimate eliminados**: `daily_outcomes_curve`, `budget_guardrail`, `estimate_dau`. Sin reemplazo — el servicio que los alimentaba fue retirado.
- **Commerce Order Management API descontinuada**: 47 endpoints, bloqueados en v26.0 desde ya y en todas las versiones el **27 de octubre de 2026**. Sin ruta de reemplazo.

### Cambios anteriores de 2026 aún relevantes

- **19 de mayo de 2026** — el bloqueo a creación, duplicación y actualización de campañas legacy Advantage+ Shopping (ASC) y Advantage+ App (AAC) se extendió a **todas** las versiones de Marketing API. Volver a una versión anterior ya no evade la restricción. Es parte de la iniciativa "Automation Unification".
- **31 de marzo de 2026** — Meta cambió la autoridad certificadora de los certificados mTLS de webhooks a una CA propia. Se requiere el certificado raíz nuevo (`meta-outbound-api-ca-2025-12.pem`) en el trust store. Una cadena de confianza rota se manifiesta como silencio en el pipeline de reporting, no como un error obvio.
- **Junio de 2026** — retiro de métricas legacy en Graph API: reach de post y página, impresiones de video, impresiones de stories. Reemplazadas por Media Views, Media Viewers y Page Viewer. Los dashboards que leen los nombres antiguos devuelven vacío, no error.
- **Webhooks a nivel de cuenta publicitaria** documentados en julio de 2026, para reemplazar polling.

---

## 8. Automatización agéntica: el servidor MCP oficial de Meta

Esta es la novedad más relevante desde el punto de vista de construir sistemas autónomos sobre la plataforma.

### Cronología

- **29 de abril de 2026** — Meta liberó los Ads AI Connectors en beta abierta: un servidor MCP en `mcp.facebook.com/ads` y una CLI que comparte la misma API. Acceso inicialmente restringido a asistentes de terceros seleccionados.
- **16 de julio de 2026** — Meta **abrió el servidor MCP de ads a cualquier desarrollador con su propia app de Meta**.

### Configuración

1. En el dashboard de desarrolladores, seleccionar la app.
2. **Use cases** → **Add use cases**.
3. **Ads and monetization** → **Create & manage ads with ads MCP server** → Save.
4. Si se administran datos por cuenta de otros negocios (agencia o partner), se requiere App Review con Advanced Access sobre el permiso `ads_mcp_management`.
5. Autenticación: OAuth vía Facebook Login for Business (manejo automático de tokens), o token de acceso pre-obtenido si se administra el ciclo de vida del token internamente.

### Capacidades expuestas

| Área | Operaciones |
|---|---|
| Creación y edición | Crear, editar y eliminar campañas, ad sets y anuncios |
| Públicos | Crear, actualizar y eliminar públicos personalizados |
| Catálogo | Crear catálogo, agregar productos, definir product sets, resolver problemas que impiden que productos aparezcan en anuncios |
| Reporting | Gasto, impresiones, CTR, ROAS, con rangos de fecha flexibles, desgloses por edad/género/plataforma y múltiples niveles de agregación |
| Diagnóstico de señales | Salud y calidad de señal, para priorizar inversión en la capa de datos |
| Soporte | Búsqueda en artículos del Business Help Center desde el flujo del agente |
| Experimentación | Crear y administrar A/B tests y estudios de Conversion Lift, y recuperar detalles de tests existentes |

Meta indica que agrega herramientas de forma continua y que el rollout de acceso a herramientas por cuenta publicitaria es gradual. La forma recomendada de descubrir el estado actual es preguntarle al propio agente qué herramientas tiene disponibles.

### Consideraciones de arquitectura

**A favor del servidor oficial frente a MCPs de terceros:**
- La autenticación corre directamente entre usuario y Meta. No hay que compartir un token de Marketing API con un tercero — un vector real, dado los reportes de servidores MCP expuestos y suspensiones de cuentas por mal uso de tokens de desarrollador.
- Sin costo durante la beta. Los vendors de terceros parten en el rango de USD 25–99 mensuales por cuenta.
- Sin código de integración que mantener contra los cambios de versión.

**Limitaciones a considerar en un diseño autónomo:**
- El servidor expone operaciones de escritura sobre presupuesto real. Cualquier sistema que las invoque necesita guardarraíles fuera del modelo: límites duros de gasto, reversibilidad de cada acción, y registro de la señal que disparó cada cambio.
- La capacidad de leer diagnósticos de señal y crear estudios de lift permite cerrar un ciclo completo —observar, hipotetizar, testear, medir— sin intervención humana. Esa es exactamente la razón por la que la capa de aprobación humana importa más, no menos.
- El diseño defendible es el que separa *proponer* de *ejecutar*: el agente propone con evidencia y puntaje de confianza; un humano o una política aprueba; toda acción queda revertible.

---

## 9. Costos, tasas y regulación

### Location fees (tasas por ubicación de entrega)

Desde el **1 de julio de 2026**, Meta traspasa a los anunciantes los Digital Services Taxes en seis jurisdicciones:

| Jurisdicción | Tasa |
|---|---|
| Reino Unido | 2% |
| Francia | 3% |
| Italia | 3% |
| España | 3% |
| Austria | 5% |
| Turquía | 5% |

Mecánica que importa para cualquier sistema de reconciliación:

- Se aplica según **dónde se entregan las impresiones**, no dónde está el anunciante.
- Se suma **por encima** del presupuesto, no se descuenta de él. Un presupuesto de USD 100 entregado en Italia produce una factura de USD 103.
- **No aparece en Ads Manager.** Solo en la factura y en el billing hub, desglosada por jurisdicción.
- La optimización de presupuesto de campaña **no** la considera, por lo que el cargo facturado puede exceder los topes de presupuesto configurados. Las reglas automatizadas basadas en topes de gasto no la detectan.
- Aplica también a campañas de click-to-message de WhatsApp y a algunos mensajes de marketing facturados junto con anuncios.

Riesgo específico para operaciones de agencia: reconciliar gasto desde datos de Ads Manager subfactura sistemáticamente la porción de location fee, y la agencia la absorbe.

Meta indica que la lista de países y las tasas cambiarán con el panorama regulatorio. **Brasil** implementó su propio impuesto a la publicidad superior al 12% desde el 1 de enero de 2026 — el dato más relevante para operaciones en LATAM. **[fuente secundaria; verificar la mecánica exacta de traspaso antes de modelar presupuestos]**

Chile no está en la lista de las seis jurisdicciones iniciales.

### Divulgación de intérpretes sintéticos

La ley de Nueva York sobre *synthetic performer disclosure* entró en vigencia el **9 de junio de 2026**. Exige divulgación conspicua cuando un anuncio usa un intérprete humano generado por IA. **Aplica según dónde se ve el anuncio, no dónde está el negocio.** Se espera que otros estados sigan el mismo modelo.

Colisión directa con la ola de creativo generativo: cualquier pipeline que genere likeness humano necesita un flujo de etiquetado antes de escalar entrega hacia Nueva York.

### Chile — Ley 21.719

Contexto regulatorio local para cualquier operación que trate datos personales de titulares en Chile, incluidos los que alimentan CAPI, públicos personalizados y listas de clientes.

- **Publicada:** 13 de diciembre de 2024. **Entrada en vigencia plena: 1 de diciembre de 2026.**
- Reemplaza el marco de la Ley 19.628 (1999). Referencia de diseño: GDPR.
- Crea la **Agencia de Protección de Datos Personales (APDP)** con facultades autónomas de fiscalización, sanción y orden de suspensión de tratamiento.
- Derechos ARCO completos más portabilidad.
- **Notificación de brechas a la Agencia dentro de 72 horas** desde el conocimiento del incidente, y a los titulares afectados sin dilación indebida cuando el riesgo sea alto.
- Multas de hasta 20.000 UTM, o hasta 4% de los ingresos anuales en reincidencia.
- Empresas de menor tamaño (Ley 20.416): durante los primeros 12 meses (dic 2026 – dic 2027) reciben amonestación escrita en lugar de multa por primeras infracciones.

Implicancias concretas para una operación publicitaria:

1. **Base de licitud para publicidad.** El titular puede negarse a recibir publicidad si entregó sus datos para otro fin. Esto afecta directamente la construcción de listas de clientes para públicos personalizados.
2. **Registro de actividades de tratamiento.** Hay que poder demostrar qué dato se envía a Meta, con qué finalidad y bajo qué base legal.
3. **Encargados de tratamiento.** Meta actúa como tercero en el flujo. Requiere contrato de encargo (DPA) y trazabilidad de transferencia internacional.
4. **Hashing no equivale a anonimización.** Enviar email o teléfono hasheado a CAPI sigue siendo tratamiento de datos personales bajo el marco.
5. **La ley fiscaliza evidencia operativa**, no políticas: logs, inventarios y registros fechados.

---

## 10. Benchmarks — con reservas

Las cifras siguientes provienen de agregadores comerciales y proveedores de herramientas. **Difieren entre sí de forma material** —el CPM mediano global oscila entre USD 6,59 y USD 14,19 según la fuente— lo que refleja diferencias de muestra, no del mercado. Úsense como orden de magnitud.

### Referencias globales cruzadas (2026)

| Métrica | Rango reportado |
|---|---|
| CPM mediano, todas las industrias | USD 13,48 – 14,19 |
| CPC promedio, todas las industrias | USD 0,78 – 1,11 |
| CTR mediano | 1,55% – 2,19% |
| CVR mediano | ~1,57% |
| ROAS mediano | 1,86× – 1,93× |
| CPA mediano | ~USD 38 |

### Por vertical (CPC)

Extremos reportados: apparel USD 0,45 y alimentos/bebidas USD 0,52 en el rango bajo; legal USD 3,45 y finanzas USD 3,77 en el alto.

CPA por vertical, extremos: educación USD 7,85; ecommerce ~USD 30; servicios para el hogar USD 89; salud USD 157; legal USD 188; seguros USD 198.

### Por nivel de mercado

Mercados Tier 1 (EE.UU., Australia, Canadá, Europa Occidental) reportan CPM entre USD 10 y 23, con EE.UU. en el extremo superior. Los mercados de menor costo reportan CPM bajo USD 2. **No encontré datos de LATAM desagregados por país en fuentes con metodología publicada** — el vacío es real, no una omisión de este documento. Para Chile, la única referencia confiable es la data propia de la cuenta.

### Estacionalidad

CPM de Q4 promedia ~26% por sobre Q1. La semana de Black Friday reporta CPM de 2–3× el nivel normal. Implicancia operativa: construir la biblioteca creativa en Q1–Q2, cuando el costo de testear es bajo, para desplegar en Q4.

### Cálculo de ROAS de equilibrio

```
ROAS de equilibrio = 1 / margen de contribución
```

Margen de 20% → se requieren USD 5 de ingreso por cada USD 1 invertido para empatar. Este número, y no el ROAS de la plataforma, es el que define si una campaña es viable.

---

## 11. Calendario de fechas críticas

| Fecha | Evento | Estado |
|---|---|---|
| 12 ene 2026 | Eliminación de ventanas 7d-view y 28d-view; límites de retención | Ejecutado |
| 18 feb 2026 | Graph API / Marketing API v25.0 | Ejecutado |
| Mar 2026 | Redefinición de click-through; engage-through attribution | Ejecutado |
| 31 mar 2026 | Cambio de CA para certificados mTLS de webhooks | Ejecutado |
| Abr 2026 | CAPI de un clic; Pixel asistido por IA | Ejecutado |
| 29 abr 2026 | Ads AI Connectors (MCP + CLI) en beta abierta | Ejecutado |
| 19 may 2026 | Bloqueo de ASC/AAC legacy en todas las versiones de MAPI | Ejecutado |
| 9 jun 2026 | Expiración de Marketing API v23.0 | Ejecutado |
| 9 jun 2026 | Ley de divulgación de intérpretes sintéticos (Nueva York) | Vigente |
| Jun 2026 | Retiro de métricas legacy de reach/impresiones en Graph API | Ejecutado |
| 1 jul 2026 | Location fees en 6 jurisdicciones | Vigente |
| 16 jul 2026 | Servidor MCP de ads abierto a todo desarrollador | Vigente |
| 29 jul 2026 | Graph API / Marketing API v26.0 | Vigente |
| **27 oct 2026** | Commerce Order Management API bloqueada en todas las versiones | **Pendiente** |
| **1 dic 2026** | Entrada en vigencia Ley 21.719 (Chile) | **Pendiente** |
| dic 2027 | Fin del período de amonestación para empresas menores (Chile) | Pendiente |

---

## 12. Lista de verificación operativa

**Señales**
- [ ] CAPI implementado además del Pixel
- [ ] `event_id` idéntico entre navegador y servidor; conteo verificado contra el backend
- [ ] EMQ ≥ 7,0 en eventos de conversión principales
- [ ] `fbc` y `fbp` capturados y enviados
- [ ] Estado del Pixel asistido por IA verificado en Events Manager

**Medición**
- [ ] Línea base de atribución establecida antes/después de enero y marzo de 2026
- [ ] Tres números separados: ROAS de plataforma, MER, lift incremental
- [ ] Al menos un estudio de Conversion Lift ejecutado por trimestre
- [ ] Sin intentos de reconciliar Meta contra GA4

**Estructura**
- [ ] Presupuesto diario × 7 ≥ 50 conversiones por ad set
- [ ] Sin cambios estructurales antes de 7–14 días
- [ ] 3–5 ángulos creativos por ad set en campañas manuales
- [ ] Frecuencia bajo 3,4

**Técnico**
- [ ] Versión de API especificada explícitamente en cada llamada
- [ ] Flag de Advantage+ Audience fijado explícitamente
- [ ] Certificado raíz `meta-outbound-api-ca-2025-12.pem` en trust store
- [ ] Dashboards migrados de métricas legacy a Media Views / Viewers
- [ ] Dependencias de Commerce Order Management eliminadas antes del 27 oct

**Financiero y legal**
- [ ] Reconciliación de facturas contra Ads Manager, con location fees como línea separada
- [ ] Inventario de campañas por geografía de entrega
- [ ] Flujo de etiquetado para creativo con likeness humano generado por IA
- [ ] Registro de actividades de tratamiento y DPA con Meta (Chile, antes de dic 2026)

---

## 13. Preguntas abiertas

1. **Umbrales exactos de la fase de aprendizaje.** Meta no publica el número. Las cifras de 50 (y 30–50 para value optimization) provienen de observación agregada de terceros. Verificar contra data propia.
2. **Ponderación real de los primeros segundos de video en Andromeda.** La dirección es clara; la magnitud no está documentada públicamente.
3. **Costo del servidor MCP tras la beta.** Meta no ha anunciado precio.
4. **Expansión de la lista de location fees.** Meta señaló explícitamente que cambiará. Vale monitorear si LATAM entra.
5. **Benchmarks de LATAM con metodología auditable.** No los encontré. Cualquier planificación de costos para Chile debería apoyarse en datos propios de cuenta.
6. **Disponibilidad de Muse Video.** Anunciado, no confirmado como productivo.

---

## 14. Fuentes

**Primarias (Meta)**
- Engineering at Meta — GEM: modelo generativo de recomendación de ads (10 nov 2025): `https://engineering.fb.com/2025/11/10/ml-applications/metas-generative-ads-model-gem-the-central-brain-accelerating-ads-recommendation-ai-innovation/`
- Meta for Business — innovación de IA en ads ranking: `https://www.facebook.com/business/news/ai-innovation-in-metas-ads-ranking-driving-advertiser-performance`
- Meta for Developers — servidor MCP de ads abierto a desarrolladores (16 jul 2026): `https://developers.facebook.com/blog/post/2026/07/16/meta-ads-mcp-server/`
- Documentación del servidor MCP de ads: `https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-overview`
- Changelog de Marketing API / versiones: `https://developers.facebook.com/docs/marketing-api/marketing-api-changelog/versions/`
- Introducción de Graph API y Marketing API v25.0 (18 feb 2026): `https://developers.facebook.com/blog/post/2026/02/18/introducing-graph-api-v25-and-marketing-api-v25/`

**Prensa especializada**
- Search Engine Land — Andromeda y GEM: `https://searchengineland.com/meta-ai-driven-advertising-system-andromeda-gem-468020`
- PPC Land — v26.0 y bloqueo de 47 endpoints de commerce: `https://ppc.land/meta-blocks-47-commerce-endpoints-as-graph-api-v26-0-lands-today/`
- Social Media Today — cambios de Marketing API: `https://www.socialmediatoday.com/news/meta-updates-marketing-api-to-align-with-latest-ad-shifts/812648/`
- Social Media Today — Muse Image para anunciantes: `https://www.socialmediatoday.com/news/meta-improves-ai-image-generation-tools-for-advertisers/824650/`
- CNBC — Muse Image: `https://www.cnbc.com/2026/07/07/meta-ai-muse-image.html`
- Jon Loomer — atribución en 2026: `https://www.jonloomer.com/meta-ads-attribution-2026/`

**Análisis de terceros (usar con criterio)**
- Kitchn — actualización de Marketing API Q2 2026: `https://www.kitchn.io/blog/meta-marketing-api-q2-2026-update`
- Triple Whale — benchmarks por industria: `https://www.triplewhale.com/blog/facebook-ads-benchmarks`
- Zentric Digital — configuración de atribución y test de Seer Interactive: `https://www.zentric.digital/insights/meta-ads-attribution-settings-guide`
- Digital Applied — location fees en Europa: `https://www.digitalapplied.com/blog/meta-europe-location-fees-july-2026-advertiser-guide`

**Regulación (Chile)**
- Biblioteca del Congreso Nacional — texto oficial Ley 21.719
- Secretaría de Gobierno Digital — guía de implementación: `https://wikiguias.digital.gob.cl/datos-personales/guia-practica-implementacion-nueva-ley-datos-personales`
