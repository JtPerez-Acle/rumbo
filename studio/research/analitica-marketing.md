# Medición y reportería de marketing en LatAm: fuente canónica para un curso de treinta lecciones

**Fecha del documento:** 12 de agosto de 2026, America/Santiago  
**Fecha de consulta de documentación de Google, Meta, TikTok, Apple y Mailchimp:** 12 de agosto de 2026  
**Alcance:** analítica, métricas, economía unitaria, instrumentación, atribución, causalidad y reportería de marketing para marcas y agencias en América Latina.  
**Herramientas operativas admitidas:** Google Analytics 4, Google Tag Manager, Google Looker Studio, Google Sheets y analíticas nativas de las plataformas. No se enseña Tableau, Power BI, Amplitude, suites comerciales de atribución ni herramientas de pago.

Este documento adopta una regla que debe propagarse al resto del catálogo: **una métrica no está definida por su nombre, sino por su numerador, su denominador, su población, su ventana temporal y su fuente**. “CTR”, “conversion rate”, “engagement rate”, “CAC” o “ROAS” sin esos elementos son etiquetas incompletas. El problema no es semántico: TikTok, por ejemplo, publica simultáneamente una tasa de conversión sobre impresiones y otra sobre clics de destino; ambas son válidas dentro de su sistema y producen números distintos. citeturn20search0

La jerarquía de evidencia que gobierna el curso es:

| Marca | Uso en este documento |
|---|---|
| **[P]** | Documentación oficial de plataforma; norma; presentación/filing corporativo primario; o investigación con método explícito y reproducible. Es la base de las definiciones. |
| **[V]** | Investigación, guía o dato producido por un proveedor, inversionista o empresa con interés comercial. Se identifica quién lo publica/financia y no se eleva a ley universal. |
| **[X]** | Benchmark sin muestra, mercado, fecha y método verificables. Se descarta. “El CTR promedio de la industria es X”, “un buen ROAS es Y” o “todo negocio debe tener CAC de Z” entran aquí cuando circulan sin procedencia. |

Una consecuencia importante es que este material **no contiene un “buen CTR”, “buen CPC”, “buen CAC” o “buen ROAS” universal**. La propia documentación de Google Ads advierte que un CTR adecuado cambia según producto, servicio y red. citeturn19search0

## El diccionario canónico

**Bloque 1. Lecciones 1 a 6**

**Prerrequisitos reales:** ninguno. Saber usar una planilla es suficiente.

**Qué logra quien solo hace este bloque:** puede leer un reporte de publicidad, redes, email o web sin confundir exposición, respuesta, resultado y economía; puede reconstruir cualquier KPI desde datos base y rechazar una métrica cuyo denominador no esté declarado.

**Dominios que dependen de este bloque:** publicidad digital, email marketing, SEO, redes sociales, influencers/creators, ecommerce, CRO, generación de demanda, reportería ejecutiva, atribución y economía unitaria.

**Dependencias explícitas hacia adelante:** impresiones, alcance, frecuencia, clics, CTR, CPC y CPM son prerrequisito del bloque técnico y del de atribución; CPA, tasa de conversión y ROAS son prerrequisito de economía unitaria, atribución y reportería; engagement rate y métricas de email son prerrequisito de reportería multicanal. **CAC no debe aprenderse como sinónimo de CPA:** esa distinción es prerequisito del bloque de economía unitaria.

| Lección | Propósito |
|---|---|
| Lección 1 | Contrato de medición, elección de la marca real del alumno y anatomía de una métrica. |
| Lección 2 | Exposición: impresiones, alcance, frecuencia y CPM. |
| Lección 3 | Respuesta: clics, CTR y CPC. |
| Lección 4 | Resultado: conversión, tasa de conversión, CPA y ROAS. |
| Lección 5 | Email: tasa de apertura, tasa de clic y el quiebre producido por Apple Mail Privacy Protection. |
| Lección 6 | Engagement rate, denominadores incompatibles y construcción del diccionario oficial de la marca. |

**Convención para fórmulas de Google Sheets:** los ejemplos usan nombres de función en inglés y coma como separador. Según la configuración regional de la hoja puede ser necesario usar `;`. Las operaciones aritméticas son idénticas.

### Definiciones que otros cursos deben citar sin reescribir

| Métrica | Definición canónica y fórmula replicable | Unidad | Qué decisión habilita | Error típico | Se confunde con |
|---|---|---:|---|---|---|
| **Impresiones** | Número de veces que una pieza/anuncio fue servida o mostrada según la regla de conteo de la plataforma. `Impressions = COUNT(exposures)` | impresiones | Escala de entrega; base de frecuencia, CTR y CPM. | Interpretarlas como personas o asumir que implican atención. | Alcance, views. |
| **Alcance** | Número de usuarios/cuentas únicos que recibieron al menos una exposición dentro de una población y periodo. `Reach = COUNTUNIQUE(exposed_id)` cuando existe identificador deduplicable. | personas/cuentas únicas | Saber cuánta población distinta se está cubriendo. | Sumar alcance entre campañas/plataformas: una persona puede aparecer en varias. | Impresiones. |
| **Frecuencia** | Promedio de exposiciones por persona alcanzada. `=Impressions/Reach` | impresiones/persona | Diagnosticar repetición frente a expansión de cobertura. | Leer el promedio como si todos vieran el anuncio el mismo número de veces. | Impresiones por sesión, alcance. |
| **Clics de destino** | Veces que un clic lleva al destino que se quiere medir. `Clicks_destination = COUNT(destination_click)` | clics | Evaluar capacidad de una pieza para generar tráfico. | Usar “all clicks” como si fueran clics al sitio. | Link clicks, interactions, sessions. |
| **CTR** | Proporción de impresiones que producen el tipo de clic declarado. Para tráfico: `CTR_destination = DestinationClicks / Impressions * 100`. Sheets: `=IFERROR(C2/B2,0)` y formatear %. | % | Comparar respuesta de piezas o audiencias con igual definición de clic. | Diagnosticar rentabilidad solo con CTR; cambiar entre “all clicks” y “destination clicks”. | Click rate de email, conversion rate. |
| **CPC** | Gasto publicitario dividido por clics del tipo declarado. `CPC_destination = AdSpend / DestinationClicks`. Sheets: `=IFERROR(B2/C2,0)` | moneda/clic | Coste de generar una visita potencial. | CPC bajo = campaña rentable. Puede atraer tráfico barato que no convierte. | CPA, CAC. |
| **CPM** | Gasto por mil impresiones. `CPM = AdSpend / Impressions * 1000`. Sheets: `=IFERROR(B2/C2*1000,0)` | moneda/1.000 impresiones | Coste de comprar exposición. | Tratar CPM bajo como mayor efectividad; ignora calidad de la audiencia y resultado. | Coste por mil personas alcanzadas. |
| **CPA** | Gasto asignado a una campaña dividido por acciones atribuidas del tipo declarado. `CPA_purchase = AdSpend / AttributedPurchases`; `CPA_lead = AdSpend / AttributedLeads`. | moneda/acción | Eficiencia de una acción específica. | Llamar CAC al CPA de compra, registro o lead. | CAC. |
| **Tasa de conversión** | **Familia de métricas, no una cifra única. El denominador es obligatorio.** `CVR_click = Conversions/DestinationClicks*100`; `CVR_session = SessionsWithConversion/EligibleSessions*100`; `CVR_user = ConvertingUsers/EligibleUsers*100`. | % | Localizar fricción entre una oportunidad y el resultado. | Comparar CVR sobre clic con CVR sobre sesión o impresión. | CTR, key-event rate. |
| **Tasa de apertura de email** | Destinatarios entregados que registran ≥1 apertura rastreada / emails entregados. `OpenRate = UniqueTrackedOpeners / DeliveredEmails * 100`. | % | Hoy, solo señal secundaria de entregabilidad/consumo; no debería decidir por sí sola interés humano. | Suponer que una apertura rastreada equivale a una persona leyendo. | Click rate, CTOR. |
| **Tasa de clic de email** | Destinatarios entregados que registran ≥1 clic rastreado / emails entregados. `EmailClickRate = UniqueClickers / DeliveredEmails * 100`. | % | Evaluar si el mensaje genera acción. | Dividir por opens y seguir llamándolo click rate. | CTOR = clicks/openers. |
| **Engagement rate** | **Familia de métricas. No se acepta “ER” sin denominador.** Convención del curso: `ER_reach = Unique/defined engagements / Reach * 100`. Cuando la plataforma usa otro denominador debe nombrarse: `ER_views`, `ER_impressions`, etc. | % | Comparar capacidad del contenido de provocar interacción dentro de la población expuesta. | Mezclar likes, comentarios, shares, saves y clicks de forma distinta entre fuentes; comparar ER por views con ER por reach. | CTR, engagement count. |
| **ROAS** | Ingresos **atribuidos** a publicidad / gasto publicitario. `ROAS = AttributedRevenue / AdSpend`. Sheets: `=IFERROR(B2/C2,0)` y expresar como `x`. | x o % | Valorar ingreso atribuido por unidad monetaria invertida en media. | Llamarlo utilidad o causalidad; ignorar margen, costes, devoluciones y ventas que habrían ocurrido igualmente. | ROI, iROAS, MER. |

Las definiciones de impresiones, clics, CTR, CPC y coste por conversión son consistentes con la documentación operativa de Google Ads. Google define impresión como cada vez que el anuncio se muestra, clic como una interacción de clic, CTR como el porcentaje de personas que hacen clic después de verlo y CPC promedio como coste total dividido por clics. [P] citeturn19search0 TikTok define actualmente impresiones, alcance, frecuencia y clics de destino de forma equivalente a alto nivel, pero diferencia expresamente “Clicks (all)” de “Clicks (destination)”. [P] citeturn20search0

**Alcance no es aditivo.** Meta define “people reached” como cuentas únicas que vieron el contenido al menos una vez y señala que se diferencia de impresiones, que puede incluir múltiples exposiciones de las mismas cuentas. Meta también advierte que métricas únicas como Reach se deduplican y pueden basarse en estimaciones/muestreo; por eso la suma de alcance de dos ad sets puede ser superior al alcance deduplicado de la campaña. [P] citeturn21search16turn21search11

**Frecuencia es una media, no una distribución.** TikTok la define como el promedio de veces que cada usuario vio el anuncio en un periodo. [P] citeturn20search0 Una frecuencia de 3 no demuestra que todas las personas recibieron tres exposiciones: algunas pueden haber recibido una y otras muchas. Por ello sirve para diagnosticar repetición agregada, no para afirmar exposición individual.

**“Conversion rate” sin denominador queda prohibido en el catálogo.** La necesidad no es teórica: TikTok Ads Manager publica tanto `Conversions / Impressions` como `Conversions / Destination clicks` bajo variantes de CVR. [P] citeturn20search0 En cualquier reporte debe aparecer `CVR_click`, `CVR_session`, `CVR_user` o el denominador equivalente.

**Engagement rate tampoco es universal.** Por ejemplo, TikTok One documenta engagement rate como interacciones —likes, comentarios y shares— divididas por views del video, mientras que el estándar de este curso adopta `ER_reach` cuando existe alcance comparable. [P] citeturn10search1turn10search5 Por eso un curso de redes no debe copiar un “engagement rate” de otra plataforma sin llevarse también su denominador.

### Email después de Apple Mail Privacy Protection

El tracking de apertura tradicional incrusta una imagen remota diminuta. Cuando el cliente descarga esa imagen se registra una apertura. Mailchimp, por ejemplo, explica que su open rate se basa en emails entregados para los que se descargó el elemento de tracking y que el click rate usa emails entregados con al menos un clic. [V: documentación operativa publicada por Mailchimp/Intuit; no se usa como benchmark.] citeturn20search7

Apple Mail Privacy Protection rompe la equivalencia “pixel descargado = humano leyó”. Con la protección activada, Apple oculta la dirección IP y descarga contenido remoto privadamente **en segundo plano cuando el mensaje llega, en lugar de esperar a que la persona lo vea**. [P] citeturn20search2turn20search14 Mailchimp confirma el efecto práctico: para usuarios afectados, el pixel puede precargarse aunque el contacto no haya abierto humanamente el email, inflando aperturas y degradando también pruebas A/B, automatizaciones o segmentos basados en “abrió/no abrió”. [V: Mailchimp/Intuit.] citeturn20search3

Por tanto, desde este curso:

**No se afirma:** “el 48% leyó el email” porque el open rate fue 48%.

**Sí se afirma:** “el sistema registró una tasa de apertura rastreada de 48%; esta señal no equivale de forma fiable a lectura humana debido, entre otros factores, a la precarga y privacidad de clientes como Apple Mail”.

Para decisiones de comportamiento, priorizar clics, conversiones, compras, replies o acciones posteriores. Mailchimp recomienda precisamente desplazar la lectura hacia clics y compras en escenarios afectados por MPP. [V: Mailchimp/Intuit.] citeturn20search3

### Las dependencias canónicas

| Definición de este bloque | Economía unitaria | Medición técnica | Atribución y causalidad | Reportería |
|---|---:|---:|---:|---:|
| Impresiones | — | Sí | Sí | Sí |
| Alcance | — | Sí | Sí | Sí |
| Frecuencia | — | Sí | Sí | Sí |
| Clics | — | **Sí** | **Sí** | Sí |
| CTR | — | Sí | Sí | Sí |
| CPC | Indirecta | Sí | Sí | Sí |
| CPM | — | Sí | Sí | Sí |
| CPA | **Sí: distinguir de CAC** | **Sí** | **Sí** | **Sí** |
| Conversion rate | **Sí** | **Sí** | **Sí** | **Sí** |
| Open/click rate de email | — | Indirecta | Sí | Sí |
| Engagement rate | — | Sí | Sí | Sí |
| ROAS | **Sí** | Sí | **Sí: atribuido ≠ incremental** | **Sí** |

## Economía unitaria

**Bloque 2. Lecciones 7 a 12**

**Prerrequisitos reales:** del bloque anterior, CPA, tasa de conversión y ROAS. El alumno debe poder distinguir gasto publicitario, acciones y clientes.

**Qué logra quien solo hace este bloque:** puede estimar CAC, margen, LTV y payback aunque sus datos estén incompletos; puede mostrar qué parte es observada y qué parte es una hipótesis; puede decidir si escalar adquisición parece económicamente sostenible.

**Dominios dependientes:** paid media, ecommerce, generación de demanda B2B, suscripción, growth, CRM, retención, planificación financiera de marketing.

| Lección | Propósito |
|---|---|
| Lección 7 | Qué es realmente CAC y qué costes entran. |
| Lección 8 | Margen bruto, margen de contribución y por qué revenue no es utilidad. |
| Lección 9 | LTV observado por cohortes. |
| Lección 10 | LTV estimado cuando faltan meses, churn o datos perfectos. |
| Lección 11 | Payback y flujo acumulado. |
| Lección 12 | LTV:CAC, la regla 3:1 y sus trampas. |

### CAC

La definición canónica es:

\[
CAC=\frac{\text{costes económicamente vinculados a adquisición}}{\text{nuevos clientes adquiridos por esos costes}}
\]

En Sheets:

```text
=AcquisitionCosts/NewCustomers
```

El punto difícil no es dividir. Harvard Business School sintetizó precisamente este problema en 2026: tanto el numerador como el denominador requieren juicio sobre qué es un cliente adquirido, qué costes corresponden a adquisición, cómo distribuir costes compartidos y cómo alinear temporalmente gasto y clientes. Distingue además CAC blended, por canal, por cohorte y marginal. [P] citeturn17search3

Por eso este curso define tres variantes, siempre etiquetadas:

| Variante | Fórmula | Uso correcto |
|---|---|---|
| `Media CPA_purchase` | `PaidMediaSpend / AttributedPurchases` | Eficiencia de publicidad; **no llamarla CAC**. |
| `Paid CAC` | `AcquisitionMedia+AcquisitionCreative+direct acquisition costs / NewCustomers attributable to paid acquisition` | Gestión de adquisición pagada, si la separación es razonable. |
| `Blended CAC` | `All acquisition-related sales+marketing costs / All new customers` | Economía global de captación. |

Un negocio puede reportar CPA de US$20 y CAC de US$70 sin contradicción: el primero quizá solo incluya gasto de anuncios y una compra atribuida; el segundo puede incluir producción, promociones de adquisición, equipo, agencia o ventas y contar exclusivamente clientes nuevos.

**Error crítico:** usar registros, leads, primeras compras y “clientes” indistintamente. El denominador debe representar la unidad económica que genera LTV.

### Margen

Para producto:

\[
Margen\ bruto=\frac{Ingresos-COGS}{Ingresos}
\]

```text
=(Revenue-COGS)/Revenue
```

Pero para LTV y payback es más útil la **contribución** que queda para recuperar adquisición y costes fijos:

\[
Contribución = Ingresos - COGS - costes\ variables\ adicionales
\]

Ejemplos de costes variables adicionales son procesamiento de pago, subsidios de envío, comisiones variables y devoluciones cuando sean materialmente dependientes de la venta. Qué entra debe documentarse en la marca; no existe una lista universal.

```text
Contribution=Revenue-COGS-VariableFulfillment-PaymentFees-Refunds
```

**Nunca multiplicar revenue por “lifetime” y llamarlo LTV económico si la pregunta es rentabilidad.** El ingreso no paga CAC; la contribución sí.

### LTV que se pueda defender

Para una cohorte adquirida en un mes determinado:

\[
LTV_{observado,T} =
\frac{\sum_{t=0}^{T} Contribución_{cohorte,t}}
{Clientes\ adquiridos\ al\ inicio}
\]

Si en B2:M2 se registra contribución por cliente del mes 0 al 11:

```text
=SUM(B2:M2)
```

Esta forma tiene una ventaja: separa lo observado de lo proyectado.

Una definición más completa del LTV proyectado descuenta contribuciones futuras:

\[
LTV=\sum_{t=0}^{T}
\frac{E[Contribución_t]}{(1+d)^t}
\]

En una hoja, puede construirse de manera transparente:

| Columna | Campo | Fórmula ilustrativa |
|---|---|---|
| A | mes | 0, 1, 2… |
| B | clientes activos esperados | dato/hipótesis |
| C | ingreso por cliente | dato/hipótesis |
| D | contribución por cliente | `=C2*MarginRate` o cálculo explícito |
| E | contribución cohorte | `=B2*D2` |
| F | contribución descontada | `=E2/(1+$K$1)^A2` |
| Total | LTV cohorte | `=SUM(F2:F25)/InitialCustomers` |

La literatura académica de valoración de clientes modela LTV como valor presente de márgenes futuros y muestra por qué aproximaciones ingenuas de “vida media × margen” pueden distorsionar el valor. [P] citeturn7search4 En negocios contractuales, los modelos de retención pueden resultar útiles; en negocios no contractuales —retail, ecommerce ocasional, marketplaces— no observar una compra no equivale a saber que el cliente “churned”, por lo que trasladar mecánicamente fórmulas de suscripción es problemático. [P] citeturn7search1turn7search9

La fórmula popular:

\[
LTV \approx \frac{ARPA\times Margen}{Churn}
\]

es **un atajo**, no la definición canónica. Solo es razonable bajo supuestos fuertes: periodos coherentes, churn aproximadamente estable, comportamiento de retención parecido entre cohortes, contribución aproximadamente estable y sin dinámicas importantes de expansión/contracción. El propio material de operadores SaaS que popularizó este tipo de cálculo ha advertido que la fórmula simple falla con vidas largas o negative churn y ha recomendado modelos de flujos descontados en escenarios más complejos. [V: David Skok/ForEntrepreneurs, asociado a Matrix Partners.] citeturn6search2turn6search5

### Cómo calcular cuando los datos son malos

| Situación real | Cálculo honesto | Qué no hacer |
|---|---|---|
| Solo hay tres meses de historial | Reportar `LTV observado a 90 días` y, separado, un escenario proyectado. | Presentar el escenario como LTV realizado. |
| No se sabe qué cliente vino de qué canal | Usar blended CAC; canal solo como proxy con atribución claramente etiquetada. | Sumar CAC por canal como si fueran poblaciones independientes. |
| No hay COGS limpio | Construir una estimación explícita de contribución con Finanzas y presentar sensibilidad. | Usar revenue como si fuera margen. |
| Hay ventas repetidas pero no IDs confiables | LTV por cohorte no es defendible aún; usar ingreso/contribución por pedido y declarar la brecha. | Inventar repeat rate. |
| Muchos clientes existían antes de la campaña | Separar nuevos de recurrentes cuando sea posible. | Dividir spend entre todos los compradores y llamarlo CAC. |
| Los costes de equipo sirven adquisición y retención | Asignar una proporción documentada o reportar un rango de CAC. | Elegir arbitrariamente 0% para mejorar el KPI. |

### Payback

Payback responde: **¿cuándo recupera la contribución del cliente el coste de adquirirlo?**

Sea \(C_m\) la contribución acumulada hasta el mes \(m\):

\[
Payback = \min(m:C_m\ge CAC)
\]

En Sheets, cree una fila de contribución acumulada:

```text
Mes 0 acumulado = Contribution_M0
Mes 1 acumulado = PreviousCumulative + Contribution_M1
...
```

y encuentre el primer mes cuyo acumulado sea ≥ CAC. En una hoja moderna:

```text
=MATCH(TRUE,CumulativeRange>=CACCell,0)-1
```

El atajo `CAC / contribución mensual promedio` solo es válido si la contribución es suficientemente estable.

### La relación LTV:CAC y la famosa regla 3:1

\[
LTV:CAC=\frac{LTV}{CAC}
\]

```text
=LTV/CAC
```

**La regla “3:1” no es una constante económica ni un resultado científico.** No se encontró un inventor único verificable. Se observa ampliamente en guías de operadores e inversionistas SaaS: David Skok ha recomendado históricamente LTV:CAC por encima de 3 junto a payback corto, y Bessemer Venture Partners también ha publicado una orientación de CLTV/CAC del orden de 3x o más para compañías cloud. [V: Skok/ForEntrepreneurs/Matrix; Bessemer Venture Partners.] citeturn6search5turn6search7

Por tanto, en este curso:

> **3:1 = heurística de inversión/operación SaaS, no benchmark universal.**

Puede no aplicar cuando:

- el negocio tiene fuertes restricciones de caja y no puede financiar un payback largo aunque el LTV:CAC proyectado sea alto;
- el producto madura rápido y el “lifetime” histórico no representa el futuro;
- hay alto coste de capital;
- la demanda es estacional;
- el margen cambia sustancialmente por cohorte;
- la adquisición tiene capacidad limitada y una ratio extremadamente alta podría indicar, incluso, subinversión;
- se trata de retail no contractual donde la predicción de “lifetime” es mucho más incierta. La dificultad específica de inferir retención en negocios no contractuales está bien establecida en la literatura de CLV. [P] citeturn7search9

Es además extremadamente fácil inflarla:

\[
\frac{\color{gray}{LTV\ demasiado\ alto}}
{\color{gray}{CAC\ demasiado\ bajo}}
\]

Basta con excluir salarios/agencia/creatividad del CAC, incluir revenue en vez de contribución en LTV, proyectar retención optimista, mezclar cohortes antiguas de alta calidad con adquisición reciente o ignorar devoluciones. Por eso **todo LTV:CAC debe llevar versión de LTV, versión de CAC y cohorte**.

## Medición técnica sin pagar

**Bloque 3. Lecciones 13 a 18**

**Prerrequisitos reales:** clics, CTR, CPA, conversion rate y ROAS del diccionario. Para entender por qué plataforma y sitio discrepan también se necesitan impresiones/alcance.

**Qué logra quien solo hace este bloque:** puede montar una medición web básica y auditable con GA4 + GTM, probar eventos, etiquetar campañas con UTMs, documentar consentimiento y construir datos utilizables por los demás cursos.

**Dominios dependientes:** publicidad, SEO, email, social, influencers, ecommerce, CRO, atribución y tableros.

| Lección | Propósito |
|---|---|
| Lección 13 | Modelo de datos de GA4: usuario, sesión, evento, parámetro y evento clave. |
| Lección 14 | Mapa de eventos y plan de medición. |
| Lección 15 | Google Tag Manager, Preview/Debug y QA. |
| Lección 16 | Consentimiento y pérdida/modelado de señal. |
| Lección 17 | UTMs y taxonomía compartida. |
| Lección 18 | Informes, límites reales y por qué las cifras no cuadran. |

### GA4: hablar el idioma actual

GA4 es fundamentalmente event-based. En la terminología actual de Google Analytics, un **key event / evento clave** es un evento importante para el negocio; una **conversion** puede crearse a partir de un evento clave para medir/optimizar campañas de publicidad de forma alineada con Google Ads. El flujo que documenta Google es `Event → Key Event → Conversion`. [P] citeturn19search2

Esto corrige material antiguo que llama “conversion” a cualquier evento importante dentro de GA4 sin distinguir el uso actual.

**Mapa diagramable de eventos:**

```text
ADQUISICIÓN
page_view
    |
    +--> search
    |
    +--> sign_up
    |
    +--> generate_lead
            |
            +--> qualify_lead
            |       |
            |       +--> working_lead
            |               |
            |               +--> close_convert_lead
            |
            +--> disqualify_lead

ECOMMERCE
view_item
    |
    +--> add_to_cart
            |
            +--> begin_checkout
                    |
                    +--> add_payment_info
                            |
                            +--> purchase
                                    |
                                    +--> refund
```

Google recomienda, entre otros, `generate_lead`, `login`, `purchase`, `refund`, `search`, `share` y `sign_up`; para ecommerce incluye `view_item`, `add_to_cart`, `begin_checkout` y `purchase`, y ha documentado eventos adicionales para etapas de lead management. [P] citeturn11search0turn11search4

Para `purchase`, el diseño debería transportar como mínimo los identificadores y valores necesarios para que el evento sea útil al negocio —por ejemplo `transaction_id`, `value`, `currency` e items cuando correspondan— y debe evitar crear nombres nuevos si existe un evento recomendado equivalente.

### Plan de medición antes de tocar GTM

| Pregunta empresarial | KPI | Evento | Parámetros | Evento clave | Fuente de verdad |
|---|---|---|---|---|---|
| ¿Llegan al producto? | view-item rate | `view_item` | item_id, category | No | GA4 |
| ¿Inician intención? | add-to-cart rate | `add_to_cart` | item_id, value | Opcional | GA4 |
| ¿Comienzan pago? | checkout rate | `begin_checkout` | value, currency | No | GA4 |
| ¿Compran? | purchases, revenue | `purchase` | transaction_id, value, currency | **Sí** | backend para negocio; GA4 para marketing |
| ¿Generan lead? | leads | `generate_lead` | form_id, lead_type | **Sí** | CRM/operación cuando exista |
| ¿Se convierte en venta? | customers | `close_convert_lead` o reconciliación operativa | lead_id no PII | Sí si está instrumentado | sistema comercial |

La regla es diseñar desde **decisión → KPI → evento → parámetros → QA**, no desde “qué tags podemos instalar”.

### Checklist mínimo de implementación de GA4

| Estado | Verificación |
|---|---|
| ☐ | Propiedad y data stream correctos; zona horaria y moneda alineadas con el negocio. |
| ☐ | Un solo criterio documentado para entornos de producción, staging y pruebas. |
| ☐ | Google Tag Manager instalado una vez y validado. |
| ☐ | Consent Initialization configurado antes de tags que dependan del estado de consentimiento. |
| ☐ | `page_view` no se duplica por instalaciones paralelas. |
| ☐ | Eventos estándar/recomendados usados antes de inventar custom events. |
| ☐ | Eventos de negocio tienen nombre, trigger, parámetros, owner y fuente de verdad. |
| ☐ | Eventos clave definidos solo para acciones realmente importantes. |
| ☐ | `purchase` contiene identificador de transacción y valor correcto; no dispara al refresh. |
| ☐ | Moneda verificada. |
| ☐ | UTMs sobreviven redirect/landing. |
| ☐ | Tráfico interno y pruebas se identifican según política del equipo. |
| ☐ | Preview de GTM muestra tags esperados y ausencia de duplicados. |
| ☐ | DebugView confirma eventos y parámetros reales. |
| ☐ | Se prueba desktop + móvil + navegadores relevantes. |
| ☐ | Se prueba consentimiento: aceptado, rechazado y cambio de estado. |
| ☐ | Se comprueba que ningún parámetro transporte PII prohibida. |
| ☐ | Se valida al menos una transacción/lead extremo a extremo contra la fuente operativa. |
| ☐ | Se documenta fecha de release y cambio de medición. |
| ☐ | Después de publicación se hace reconciliación de 24–72 horas contra negocio y plataformas, sin exigir igualdad perfecta. |

Google Tag Manager ofrece Preview/Debug precisamente para probar el contenedor borrador y observar qué etiquetas se disparan antes de publicar; GA4 DebugView permite observar eventos y propiedades en dispositivos en modo debug. [P] citeturn11search2turn11search1

GA4 impone además límites técnicos que impiden tratarlo como un almacén infinitamente flexible: nombres de evento de hasta 40 caracteres, hasta 25 parámetros por evento y límites específicos para propiedades de usuario y valores de parámetros. [P] citeturn4search0turn4search8 Un curso básico debe enseñar **menos eventos, mejor definidos**, no telemetría indiscriminada.

### Consentimiento cambia el dato observado

Consent Mode no es una plataforma de gestión de consentimiento ni un banner. Comunica a tags de Google el estado de consentimiento decidido por el usuario y, según implementación, modifica su comportamiento. Google distingue implementaciones básica y avanzada; en modo avanzado, estados denegados pueden producir señales sin cookies que posteriormente participan en modelado cuando se cumplen las condiciones necesarias. [P] citeturn0search9

GTM tiene tipos de consentimiento como `analytics_storage`, `ad_storage`, `ad_user_data` y `ad_personalization`, además de un trigger de Consent Initialization para establecer estados antes de otros tags. [P] citeturn0search1

Consecuencia pedagógica:

```text
100 compras reales
      |
      +-- usuarios con medición permitida --> compras observables directamente
      |
      +-- usuarios sin señal equivalente --> pérdida o tratamiento distinto
      |
      +-- datos/modelado aplicable según configuración y elegibilidad
```

**Una caída en usuarios o sesiones después de cambiar consentimiento no demuestra por sí sola una caída en demanda.** Primero hay que determinar si cambió el mecanismo de observación.

Este curso no sustituye asesoría jurídica: las obligaciones de consentimiento dependen de la jurisdicción y del tratamiento de datos concreto.

### Convención canónica de UTMs

Google documenta `utm_source`, `utm_medium` y `utm_campaign` como parámetros fundamentales de etiquetado manual, y soporta además `utm_id`, `utm_term`, `utm_content`, `utm_source_platform`, `utm_creative_format` y `utm_marketing_tactic` en dimensiones asociadas. [P] citeturn19search1turn19search5

**Contrato de nomenclatura del catálogo:**

1. minúsculas;
2. caracteres ASCII siempre que sea posible;
3. guion `-` dentro de un valor; nunca espacios;
4. vocabularios controlados, no texto libre;
5. nunca PII: sin nombres, emails, teléfonos, IDs personales;
6. `source` identifica **quién entrega**;
7. `medium` identifica **cómo se distribuye**;
8. `campaign` identifica una iniciativa estable;
9. creativo, audiencia y keyword no se meten todos en campaign;
10. una campaña publicada no cambia retroactivamente de nombre.

| Parámetro | Regla | Ejemplo |
|---|---|---|
| `utm_id` | ID estable interno | `cmp-2026-042` |
| `utm_source` | plataforma/editor | `google`, `meta`, `tiktok`, `newsletter-partners` |
| `utm_medium` | canal controlado | `cpc`, `paid_social`, `email`, `organic_social`, `display`, `referral` |
| `utm_campaign` | mercado_objetivo_iniciativa_periodo | `cl_acq_backtoschool_2026q3` |
| `utm_term` | keyword o audiencia cuando tenga sentido | `running-shoes` o `prospecting-broad` |
| `utm_content` | pieza/variación | `video-ugc-15s-hook-a` |
| `utm_source_platform` | plataforma de origen si aporta desambiguación | `meta` |
| `utm_creative_format` | formato normalizado | `video`, `carousel`, `static` |
| `utm_marketing_tactic` | táctica | `prospecting`, `retargeting`, `retention` |

URL ilustrativa:

```text
https://marca.example/producto
?utm_id=cmp-2026-042
&utm_source=meta
&utm_medium=paid_social
&utm_campaign=cl_acq_backtoschool_2026q3
&utm_term=prospecting-broad
&utm_content=video-ugc-15s-hook-a
&utm_source_platform=meta
&utm_creative_format=video
&utm_marketing_tactic=prospecting
```

La planilla maestra de UTMs debe tener una fila por combinación aprobada:

| id | source | medium | campaign | term/audience | content | formato | táctica | URL final | owner |
|---|---|---|---|---|---|---|---|---|---|

Google recomienda una estrategia estandarizada de UTM precisamente porque variantes de valores fragmentan las dimensiones de adquisición y pueden perjudicar la clasificación. [P] citeturn0search3turn0search7

### Por qué GA4 nunca tiene por qué cuadrar exactamente con la plataforma

**Flujo diagramable del dato:**

```text
          PLATAFORMA PUBLICITARIA
          impresiones / alcance
          clic atribuido
                |
                | URL + UTM
                v
Navegador ---> consentimiento
                |
                v
             GTM
                |
                v
          evento GA4
      + parámetros + tiempo
                |
        sesión / usuario
                |
       reglas de atribución
                |
       informes de GA4
                |
                +--------------+
                |              |
                v              v
        Looker Studio      Google Sheets
                           gasto / margen /
                           objetivos / notas
                \              /
                 \            /
                  v          v
                 TABLERO / REPORTE
                        |
                    DECISIÓN

En paralelo:
plataforma --> su pixel/señal --> su ventana/modelo
             --> conversiones atribuidas --> Ads Manager
```

Las diferencias tienen causas estructurales:

| Causa | Plataforma | GA4 |
|---|---|---|
| Impresión sin clic | Puede atribuir según configuración de view-through | Puede no disponer del mismo touchpoint |
| Ventana | La define la plataforma/configuración | Su propia lookback/modelo |
| Clic vs sesión | Cuenta clic | La página y el tag deben llegar a cargar |
| Cross-device | Grafo/identidad propia | Identidad disponible para Analytics |
| Consentimiento/bloqueo | Señales propias y modeladas | Señal web potencialmente reducida/modelada |
| Conversion timestamp | Puede asignarse al momento de interacción o resultado según reporte | Depende de dimensión/modelo |
| Duplicación | Lógica propia | Debe deduplicarse correctamente, especialmente purchase |
| Atribución | Modelo propio | Modelo seleccionado en GA4 |

Google explica expresamente que clics publicitarios y sesiones de Analytics pueden divergir por filtrado de clics inválidos, problemas de tagging, redirects, usuarios que abandonan antes de cargar la etiqueta y otras diferencias de conteo. [P] citeturn4search7

### Límites de GA4 gratuito que sí importan

Los informes estándar, exploraciones y conectores no son exactamente la misma superficie analítica. Alta cardinalidad puede agrupar valores bajo `(other)` y consultas exploratorias grandes pueden usar muestreo; Google también aplica técnicas de estimación para métricas como usuarios/sesiones y umbrales de privacidad en determinadas dimensiones. [P] citeturn0search0turn5search2turn5search3

Para propiedades estándar, la retención de datos detallados de eventos/usuarios configurable es de 2 o 14 meses; la retención afecta especialmente exploraciones y análisis detallados, no significa que todos los agregados estándar desaparezcan a los 14 meses. [P] citeturn5search1

Estos límites son parte del curso porque cambian una decisión real: **un dashboard histórico no debe depender de una exploración que el equipo asume infinita**.

## Atribución, incrementalidad y causalidad

**Bloque 4. Lecciones 19 a 24**

**Prerrequisitos reales:** impresiones, clics, CPA, conversion rate y ROAS; entender UTMs, eventos, consentimiento y diferencia entre plataforma y GA4.

**Qué logra quien solo hace este bloque:** puede distinguir “se atribuyó a” de “fue causado por”, escoger una ventana/modelo para reporting, diseñar una prueba pequeña pero honesta y limitar explícitamente sus conclusiones.

**Dominios dependientes:** optimización de paid media, SEO/SEM, influencers, brand marketing, planificación de presupuesto y reportería ejecutiva.

| Lección | Propósito |
|---|---|
| Lección 19 | Último clic: utilidad descriptiva y mentira causal. |
| Lección 20 | Modelos y ventanas de atribución. |
| Lección 21 | Plataforma, GA4 y experimento: tres respuestas a tres preguntas. |
| Lección 22 | Incrementalidad y contrafactual. |
| Lección 23 | Experimentos honestos con presupuesto limitado. |
| Lección 24 | Límites de afirmación y cinco casos reales. |

### El último clic no pregunta qué causó la compra

Suponga esta ruta:

```text
TikTok video
   ↓
búsqueda orgánica
   ↓
email
   ↓
Google Ads marca
   ↓
compra
```

El último clic puede asignar 100% del mérito a Google Ads. Eso contesta:

> “¿Cuál fue el último touchpoint observable que satisface las reglas del modelo?”

No contesta:

> “¿La compra habría desaparecido sin Google Ads?”

Ese segundo enunciado exige un **contrafactual**.

GA4 dispone actualmente de data-driven attribution, paid and organic last click y Google paid channels last click en sus superficies de atribución; Google retiró de Analytics modelos rule-based como first click, linear, position-based y time-decay en 2023. [P] citeturn4search2turn4search6 La atribución data-driven usa datos de paths de conversión y no conversión para distribuir crédito; sigue siendo un modelo de atribución sobre las señales disponibles, no un experimento causal. [P] citeturn4search2

Las ventanas también alteran el resultado. GA4 documenta ventanas distintas según evento: `first_open/first_visit` usan por defecto 30 días y otros key events 90 días, con opciones de configuración, mientras que engaged-view tiene otra ventana. [P] citeturn5search8 Cambiar la ventana y luego comparar el ROAS como si la definición fuera idéntica es cambiar la regla del juego.

### El mismo caso da tres resultados y los tres pueden ser “correctos”

Caso didáctico **sintético, no benchmark**:

Una marca invierte **US$6.000**. El valor promedio de las órdenes relevantes es **US$100**.

| Sistema | Qué cuenta | Órdenes acreditadas | Revenue acreditado/incremental | Métrica | Resultado |
|---|---|---:|---:|---|---:|
| Plataforma publicitaria | Conversiones dentro de su ventana configurada, incluidas señales que su sistema pueda atribuir | 72 | US$7.200 | ROAS plataforma | **1,20x** |
| GA4, paid & organic last click | Compras cuyo crédito cae en el canal bajo la ventana/reglas de GA4 | 45 | US$4.500 | ROAS GA4 | **0,75x** |
| Experimento de holdout | Diferencia de revenue causada estimada entre tratamiento y contrafactual | 20 órdenes equivalentes | US$2.000 | iROAS | **0,33x** |

Cálculos:

```text
Platform_ROAS = 7200 / 6000 = 1.20
GA4_ROAS      = 4500 / 6000 = 0.75
iROAS         = 2000 / 6000 = 0.33
```

No hay que “elegir el número verdadero” sin definir la pregunta:

- 1,20x = revenue que la **plataforma reclama** bajo sus reglas;
- 0,75x = revenue que **GA4 atribuye** al canal bajo otro modelo;
- 0,33x = revenue **incremental estimado** bajo el diseño experimental.

Solo el tercero intenta contestar causalidad. Los dos primeros siguen siendo útiles para operación y diagnóstico.

### Incrementalidad

\[
Incremento=Y_{tratamiento}-Y_{contrafactual}
\]

El problema es que el contrafactual no puede observarse simultáneamente para la misma persona. Un experimento crea un grupo comparable que aproxima “qué habría pasado sin exposición”.

\[
iROAS = \frac{Ingresos\ incrementales}{Gasto\ incremental\ en\ publicidad}
\]

Google Research describe geo experiments donde regiones geográficas no superpuestas son asignadas aleatoriamente a tratamiento/control y la publicidad geolocalizada implementa esa asignación. El objetivo es estimar efectividad publicitaria con rigor experimental. [P] citeturn17search1 Investigaciones posteriores de Google han extendido estos enfoques a escenarios con menos geos y matched markets, precisamente porque países o subregiones pequeñas dificultan la replicación geográfica. [P] citeturn17search5

### Prueba honesta con presupuesto pequeño

No existe un porcentaje universal de holdout que deba imponerse a toda marca. Usar “10% siempre” sería otro benchmark sin base contextual. El diseño mínimo es:

**Decisión única.** “¿Mantengo, reduzco o aumento este canal/campaña?”

**Outcome primario único.** Compras, leads calificados, revenue o contribución; no cambiarlo después de mirar resultados.

**Unidad susceptible de aislamiento.** Cuando sea posible, geos comparables o un holdout elegible en analítica nativa de plataforma.

**Periodo pretest.** Confirmar que las unidades se comportan de forma razonablemente parecida antes de intervenir.

**Tratamiento claro.** Cambiar una cosa material; evitar rediseñar campaña, precio, promociones y web simultáneamente.

**No optimizar a mitad del test.** Cambiar tratamiento destruye la interpretación.

**Registrar interferencias.** Stockout, promoción, feriado, PR, caída del sitio, cambio de precio.

**Aceptar “no sabemos”.** Con pocas conversiones y alta variabilidad puede no haber señal suficiente para decidir. “Inconcluso” es un resultado legítimo.

No se requiere en este curso una demostración estadística formal. Sí se requiere no convertir ruido en certeza.

### Árbol de decisión de atribución

```text
¿La pregunta es "qué ocurrió" o "qué lo causó"?
                    |
          +---------+---------+
          |                   |
      QUÉ OCURRIÓ          QUÉ LO CAUSÓ
          |                   |
¿Necesito reparto          ¿Puedo crear
operativo entre canales?   un holdout?
          |                   |
         Sí              +----+----+
          |              |         |
Elegir modelo y         Sí         No
ventana estable          |         |
          |        experimento     |
Reportar como          causal      |
ATRIBUCIÓN                        |
                           ¿Puedo aislar geos/
                           periodos comparables?
                                |
                           +----+----+
                           |         |
                          Sí         No
                           |         |
                     prueba geo/     |
                     matched market  |
                                     |
                              TRIANGULAR
                         plataforma + GA4 +
                          negocio y declarar:
                          "no identificamos
                           efecto causal"
```

### Lo que se puede afirmar

| Evidencia | Afirmación permitida | Afirmación no permitida |
|---|---|---|
| Ads Manager | “La plataforma atribuyó 120 compras.” | “La publicidad creó 120 compras.” |
| GA4 last click | “45 compras fueron acreditadas al canal por este modelo.” | “El canal generó 45 ventas incrementales.” |
| DDA | “El modelo distribuyó crédito de esta forma.” | “Es la contribución causal verdadera.” |
| Antes/después | “Ventas subieron 20% tras lanzar.” | “La campaña causó el +20%.” |
| A/B/holdout bien diseñado | “El tratamiento produjo un lift estimado dentro de esta población/periodo.” | Generalizar automáticamente a otro país, audiencia o temporada. |

### Cinco casos reales de métricas mal leídas o posteriormente corregidas

| Caso | Lectura que fallaba | Evidencia/corrección | Lección para el curso |
|---|---|---|---|
| **eBay — paid search** | El ROI observado de search atribuía ventas al anuncio porque compradores y clics estaban correlacionados. | Grandes experimentos de campo mostraron que los retornos causales eran una fracción de las estimaciones no experimentales; en branded search prácticamente todo el tráfico perdido al apagar anuncios en el test referido fue capturado por búsqueda orgánica, y los anuncios de marca no mostraron beneficio de corto plazo medible. [P] citeturn17search4 | ROAS atribuido puede capturar intención que ya existía. |
| **Adidas — performance vs brand** | Dependencia de last click favorecía performance marketing; la compañía destinaba 77% del presupuesto a performance y 23% a brand. | La reconstrucción pública de la presentación de su director global de medios reportó que el modelado econométrico atribuyó 65% de ventas a actividad de marca y que un corte de paid search en LatAm no produjo la caída esperada de tráfico/revenue. Es un caso empresarial reportado, **no benchmark generalizable**. citeturn15search0turn15search9 | Medir con mucha precisión el fondo del funnel puede hacer invisible lo que crea demanda. |
| **P&G — viewability/reach** | El volumen comprado no garantizaba alcance efectivo al público objetivo. | Reuters reportó que P&G redujo US$200 millones de gasto digital en 2017 tras mayor transparencia de viewership/viewability y reinvirtió fondos en medios para aumentar alcance; no redujo simplemente “marketing total”. Caso corporativo, no benchmark. citeturn14search15 | Impresiones baratas no equivalen a exposición útil. |
| **Airbnb — dependencia de performance** | La lógica de “comprar clientes” con performance podía sobredimensionar el rol de media frente a demanda directa/brand. | Airbnb declaró en su 10-K que la fortaleza de marca y comunicaciones le permite ser menos dependiente de performance marketing y que este último se orienta a tráfico incremental de alta intención; la compañía pasó a invertir más profundamente en marca. [P: filing corporativo.] citeturn14search2 | CAC/ROAS de un canal no deben convertir toda demanda capturada en demanda creada. |
| **Anunciantes en experimentos de Facebook/Meta** | Métodos observacionales intentaban inferir efecto causal a partir de usuarios expuestos/no expuestos sin randomización. | Estudios basados en experimentos de advertising/Conversion Lift han encontrado diferencias relevantes entre estimaciones observacionales y resultados aleatorizados, incluyendo sesgo hacia arriba en muchas estimaciones. [P: estudio con método experimental.] citeturn8search2turn8search6 | Cuando el sesgo de selección es grande, “más expuestos compran más” no demuestra que exposición cause compra. |

El caso eBay es especialmente importante porque fue una prueba directa de la intuición equivocada: los usuarios que buscan la marca y compran son precisamente quienes hacen que paid search parezca extraordinario en datos observacionales. El experimento separó correlación de causalidad. citeturn17search0

## Reportería que termina en una decisión

**Bloque 5. Lecciones 25 a 30**

**Prerrequisitos reales:** ROAS y conversion rate para dashboards básicos; para un tablero económico se requieren CAC, margen/LTV/payback; para interpretar atribución es requisito el bloque anterior.

**Qué logra quien solo hace este bloque:** puede transformar GA4 + Sheets en un tablero de Looker Studio, separar métricas de dirección de métricas diagnósticas y producir un reporte ejecutivo de una página que diga qué ocurrió, qué sabemos, qué no sabemos y qué decisión se propone.

**Dominios dependientes:** todos los demás cursos del catálogo, porque esta capa estandariza cómo comunican resultados.

| Lección | Propósito |
|---|---|
| Lección 25 | Jerarquía: north star, outcome, drivers, diagnósticas y vanidad. |
| Lección 26 | Arquitectura del dashboard y grano de los datos. |
| Lección 27 | Looker Studio conectado a GA4 + Sheets. |
| Lección 28 | Reporte ejecutivo de una página. |
| Lección 29 | Diagnóstico y presentación de malos resultados. |
| Lección 30 | Ritmo de operación, calidad de datos y decisión final. |

### Jerarquía de métricas

```text
                    NORTH STAR
            valor de negocio/cliente
                      /     \
                     /       \
              OUTCOMES      ECONOMÍA
             revenue,       CAC, margen,
             clientes       LTV, payback
                 |               |
                 +-------+-------+
                         |
                      DRIVERS
            conversion rate, AOV,
              leads calificados
                         |
                   DIAGNÓSTICAS
           CTR, CPC, CPM, frecuencia,
         funnel, landing-page behavior
                         |
                    OBSERVACIÓN
         impresiones, likes, opens,
       views sin conexión demostrada
               con el objetivo
```

Una métrica no es “de vanidad” por naturaleza. Impresiones pueden ser una variable diagnóstica indispensable cuando el objetivo es cobertura; followers pueden importar a una estrategia de comunidad. Se convierte en vanidad cuando se presenta como éxito sin una relación definida con la decisión.

La **north star** debe representar valor producido, no simplemente aquello que la herramienta ofrece primero. En ecommerce puede acercarse a contribución o compradores recurrentes; en marketplace podría reflejar transacciones exitosas; en generación B2B, pipeline calificado. No se prescribe una north star universal.

### Plantilla canónica de tablero

El conector nativo de Looker Studio permite usar propiedades de GA4 a las que el usuario tenga acceso de lectura/análisis. [P] citeturn0search2 Para este curso se combinan dos familias de fuentes:

```text
GA4
- users / sessions
- traffic source
- campaign
- key events
- purchases / revenue
- funnel behavior

GOOGLE SHEETS
- ad spend por fecha/campaign
- presupuesto
- objetivos
- COGS/margen
- nuevos clientes
- notas de negocio
- cambios de tracking
```

**Grano recomendado de la hoja de marketing:**

```text
date | campaign_id | source | medium | campaign |
country | spend | impressions | clicks | platform_conversions |
platform_revenue | notes
```

No mezclar una fila “mensual por país” con GA4 “diario por campaign” esperando que el blend deduzca la relación. La granularidad debe acordarse antes.

**Plantilla de cinco páginas:**

| Página | Pregunta | Visualizaciones |
|---|---|---|
| **Executive** | ¿Estamos ganando o perdiendo contra objetivo? | north star, revenue/contribución, spend, CAC, tendencia, nota de calidad |
| **Acquisition** | ¿Dónde adquirimos tráfico/clientes? | source/medium/campaign, spend, clicks, CPC, sesiones, new customers |
| **Funnel** | ¿Dónde cae la conversión? | sesiones → producto → cart/lead → checkout → purchase; CVR por etapa |
| **Economics** | ¿El crecimiento es sostenible? | CAC, contribución, LTV observado por cohorte, LTV:CAC, payback |
| **Measurement health** | ¿Podemos confiar en lo anterior? | discrepancias plataforma/GA4, eventos faltantes, cambios GTM, consentimiento, UTMs `(not set)`/fragmentados |

**Filtros compartidos:** fecha, país/mercado, source, medium, campaign, dispositivo cuando sea accionable.

**Regla:** máximo una interpretación por gráfico. Si se necesitan cuatro párrafos para explicar qué es una tarjeta, probablemente el KPI está mal diseñado.

### Límites del conector GA4–Looker Studio

Looker Studio consulta datos de GA4 mediante el conector/API correspondiente, por lo que se encuentra sujeto a cuotas; demasiados gráficos o solicitudes concurrentes pueden generar errores. [P] citeturn12search0turn12search1 Además, cuando una solicitud ad hoc de Looker activa muestreo en Analytics, se aplica el comportamiento de muestreo de GA4 y **Looker Studio actualmente no indica visualmente que esos datos estén muestreados**. [P] citeturn19search3

Esto es una limitación real para reportería: un tablero muy recargado no es necesariamente más riguroso.

La frescura tampoco es idéntica para todas las fuentes; el conector de productos de medición Google puede tener ciclos de actualización distintos de una fuente Sheets. [P] citeturn11search3 Por eso una comparación “hasta hoy a las 11:00” puede mostrar diferencias que desaparecen cuando las fuentes terminan de procesar.

### Plantilla de reporte ejecutivo de una página

```text
MARCA / MERCADO / PERIODO
Decisión que se solicita: ______________________________

RESULTADO EN UNA FRASE
“Revenue quedó 12% bajo plan con gasto en línea; la principal caída observable
está después de begin_checkout. No tenemos evidencia aún de que media sea la causa.”

┌────────────────┬────────────────┬────────────────┬────────────────┐
│ NORTH STAR     │ GASTO          │ CAC            │ PAYBACK / ROAS │
│ Actual         │ Actual         │ Actual         │ Actual         │
│ Objetivo       │ Plan           │ Comparador     │ Comparador     │
│ Δ              │ Δ              │ Δ              │ Δ              │
└────────────────┴────────────────┴────────────────┴────────────────┘

QUÉ PASÓ
- Hecho 1, con magnitud y periodo.
- Hecho 2.
- Segmento que explica mayor parte del cambio.

QUÉ SABEMOS / QUÉ NO SABEMOS
Sabemos: ______________________________________________
No sabemos: ___________________________________________
Calidad/limitación del dato: __________________________

HIPÓTESIS, NO HECHOS
1. _________________________________________
2. _________________________________________

DECISIÓN / ACCIÓN
Owner: __________  Fecha: _________
Acción reversible: ____________________________________
Prueba que resolverá la principal incertidumbre: ______

RIESGO
Qué haría cambiar la decisión: ________________________
```

La primera línea debe expresar el **resultado**, no una excusa. “Campaña mostró aprendizajes valiosos” no sustituye “CAC fue 38% superior al plan”.

### Cómo presentar un mal resultado sin maquillarlo

**Incorrecto:**

> “Las campañas generaron 4,2 millones de impresiones y el engagement subió 20%.”

cuando la pregunta del negocio era adquirir clientes y el CAC empeoró.

**Correcto:**

> “Adquirimos 420 clientes contra 600 planificados con el mismo presupuesto; CAC quedó 43% sobre plan. CTR mejoró, por lo que la evidencia disponible apunta a que el deterioro aparece después del clic, no en generación de respuesta. La instrumentación de purchase fue validada contra pedidos; aún no podemos separar cuánto del cambio provino de landing page, mix de audiencia o demanda.”

Reglas de integridad:

- no cambiar el denominador después de ver un número malo;
- no acortar la ventana para borrar una cohorte;
- no reemplazar outcome por impresiones/engagement;
- no llamar “significativo” a un movimiento solo porque parece grande;
- separar **hecho**, **hipótesis**, **limitación de datos** y **acción**;
- mantener el histórico de definición de KPI.

### Qué nunca debe aparecer como benchmark sin evidencia

| Afirmación | Estado |
|---|---|
| “Un CTR de 2% es bueno para cualquier campaña.” | **[X] DESCARTADO** |
| “ROAS 4x es el mínimo saludable de ecommerce.” | **[X] DESCARTADO** |
| “La frecuencia ideal es 3.” | **[X] DESCARTADO** |
| “Un email debería abrir 25%.” | **[X] DESCARTADO** |
| “CAC promedio en LatAm es US$___.” | **[X] DESCARTADO** |
| “LTV:CAC siempre debe ser 3:1.” | **[X] como regla universal; se conserva solo como heurística SaaS [V] con procedencia.** |
| “CTR depende de producto, servicio y red.” | **[P] Google Ads.** citeturn19search0 |
| “Reach e impresiones son métricas distintas.” | **[P] Meta/TikTok.** citeturn21search16turn20search0 |

## Laboratorio encadenado del curso

Las quince tareas duran aproximadamente **10–20 minutos cada una** y usan **una sola marca o negocio real**, elegido por el alumno en la Lección 1. El alumno puede seleccionar su empleador, una pyme propia, una organización para la que tenga datos o una marca pública; cuando no pueda acceder a un dato debe registrar “no disponible” en vez de inventarlo.

| Tarea | Después de | Trabajo de 10–20 min | Artefacto acumulativo |
|---|---|---|---|
| **Elegir marca y decisión** | Lección 1 | Escribir negocio, mercado, producto, modelo de ingreso y una decisión real de marketing. | Brief de medición v1 |
| **Auditar exposición** | Lección 2 | Extraer de una plataforma impresiones, alcance y gasto; calcular frecuencia y CPM. | Diccionario v1 |
| **Auditar respuesta** | Lección 3 | Extraer clics del tipo correcto; calcular CTR y CPC; documentar qué significa “click”. | Diccionario v2 |
| **Definir resultado** | Lección 4 | Elegir una conversión, declarar denominador y calcular CVR, CPA y ROAS. | Diccionario v3 |
| **Auditar email/social** | Lecciones 5–6 | Registrar definición exacta de open/click/engagement; identificar cualquier denominador incompatible. | **Diccionario canónico propio** |
| **Construir CAC** | Lecciones 7–8 | Hacer lista de costes disponibles, definir cliente nuevo y calcular CAC estrecho + blended posible. | Hoja CAC |
| **Construir cohorte LTV** | Lecciones 9–10 | Usar meses realmente observados; calcular contribución acumulada y separar forecast. | **CAC + LTV realista** |
| **Calcular payback y LTV:CAC** | Lecciones 11–12 | Hallar primer mes de recuperación y ratio; listar tres supuestos que podrían inflarlo. | Economía unitaria |
| **Diseñar eventos** | Lecciones 13–14 | Dibujar funnel y mapear evento, trigger, parámetros, key event y owner. | **Plan de medición** |
| **QA en GTM/GA4** | Lección 15 | Usar Preview/DebugView en una ruta crítica o, sin acceso, auditar capturas/documentación disponible. | QA checklist |
| **Auditar consentimiento** | Lección 16 | Escribir qué tags deberían operar bajo cada estado y qué métricas perderían observabilidad. | Matriz de señal |
| **Crear UTMs** | Lección 17 | Crear cinco URLs siguiendo la taxonomía y probar consistencia de source/medium/campaign/content. | **Convención UTM propia** |
| **Reconciliar fuentes** | Lecciones 18–21 | Comparar una campaña en plataforma y GA4; explicar discrepancias sin intentar forzar igualdad. | Hoja de reconciliación |
| **Proponer prueba causal** | Lecciones 22–24 | Escribir hipótesis, outcome, tratamiento/control, riesgos y criterio para declarar “inconcluso”. | Test brief |
| **Construir y presentar** | Lecciones 25–30 | Crear versión mínima del tablero y completar el reporte ejecutivo de una página con una decisión. | **Dashboard + reporte ejecutivo final** |

Al terminar, los artefactos forman una sola cadena:

```text
Marca
  ↓
Decisión de negocio
  ↓
Diccionario
  ↓
CAC / LTV / payback
  ↓
Plan de eventos
  ↓
GTM + GA4 + consentimiento
  ↓
UTMs
  ↓
Reconciliación
  ↓
Atribución / experimento
  ↓
Looker Studio
  ↓
Reporte de una página
  ↓
Decisión documentada
```

La evaluación final no debería premiar “tener todos los datos”. Debería premiar especialmente que el alumno distinga:

```text
OBSERVADO
ESTIMADO
ATRIBUIDO
INCREMENTAL
NO DISPONIBLE
```

Esa disciplina es más transferible que memorizar cualquier benchmark.

## Bibliografía clasificada y registro de evidencia

**[P] Documentación oficial de Google — consultada el 12 de agosto de 2026.**

Google Ads Help, *Use data to optimize your Search campaigns*. Fuente para impresiones, clics, CTR, CPC, conversiones y coste por conversión, además de la advertencia de que CTR varía por producto/servicio/red. citeturn19search0

Google Analytics Help, *Traffic-source dimensions, manual tagging, and auto-tagging*. Fuente para `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content` y parámetros manuales adicionales. citeturn19search1turn19search5

Google Analytics Help, *Conversions vs. key events in Google Analytics*. Fuente para la taxonomía 2026 `Event → Key Event → Conversion`. citeturn19search2

Google Analytics Help, documentación de attribution models. Fuente para data-driven, paid & organic last click, Google paid channels last click y retiro de modelos rule-based anteriores. citeturn4search2turn4search6

Google Analytics Help, documentación de lookback windows. Fuente para las ventanas configurables y su diferencia por tipos de eventos. citeturn5search8

Google Analytics Help, documentación de data retention. Fuente para retención de datos de usuario/evento de 2 o 14 meses en propiedades estándar. citeturn5search1

Google Analytics Help, documentación de thresholds y sampling. Fuente para limitaciones de privacidad, muestreo y estimaciones. citeturn5search2turn5search3

Google Analytics Help, documentación de límites de colección. Fuente para longitud de nombres y número de parámetros/properties. citeturn4search0turn4search8

Google Analytics Help, recommended events y lead-generation events. Fuente para el mapa de eventos recomendado. citeturn11search0turn11search4

Google Analytics Help, DebugView; Google Tag Manager Help, Preview/Debug. Fuente para QA de implementación. citeturn11search1turn11search2

Google, Consent Mode y GTM consent support. Fuente para comportamiento de consentimiento, estados y Consent Initialization. citeturn0search9turn0search1

Google Analytics Help, discrepancias entre Google Ads clicks y Analytics sessions. Fuente para explicación de diferencias por tagging, invalid clicks, redirects y carga. citeturn4search7

Google Looker Studio Help, conector de Google Analytics. Fuente para permisos y conexión. citeturn0search2

Google Looker Studio Help, cuotas, muestreo y conector GA4. Fuente para limitaciones del dashboard y ausencia de indicador de sampling en Looker Studio. citeturn12search0turn12search1turn19search3

**[P] Documentación oficial de TikTok — consultada el 12 de agosto de 2026.**

TikTok for Business, *Basic metrics and definitions in TikTok Ads Manager*, última actualización indicada por TikTok: **octubre de 2025**. Fuente para clicks all/destination, frequency, impressions, reach, conversion rate sobre impresiones y sobre destination clicks, cost, cost per conversion y CPC destination. citeturn20search0turn20search4

TikTok for Business, *About TikTok reporting metrics*, última actualización indicada: **abril de 2025**. Fuente para categorías de attribution, in-app, page, video y onsite metrics. citeturn20search12

TikTok One, documentación de reporting. Fuente para engagement rate basado en likes, comentarios y shares frente a video views en ese producto. citeturn10search1turn10search5

**[P] Documentación oficial de Meta — consultada el 12 de agosto de 2026.**

Meta Business Help Center, *Creator Studio Insights glossary* —la propia página indica que las herramientas migraron a Meta Business Suite—. Fuente para `People reached` como cuentas únicas y la distinción reach/impressions. citeturn21search16

Meta Business Help Center, *Troubleshoot reasons why ad metrics may not add up*. Fuente para deduplicación, estimación/muestreo de métricas únicas y por qué reach no suma entre niveles de campaña. citeturn21search11

Meta Business Help Center, documentación de Ads Manager y reporting. Fuente para uso de métricas de Traffic, Engagement, Clicks y Reach en analítica nativa. citeturn21search8

**[P] Apple — consultada el 12 de agosto de 2026.**

Apple Support, *Use/Protect Mail Privacy Protection on Mac*. Fuente para ocultamiento de IP y descarga privada de contenido remoto en background al recibir el mensaje en lugar de al abrirlo. citeturn20search2turn20search14

**[P] Investigación académica/metodológica.**

Ascarza, Eva; McCarthy, Daniel. *Measuring Customer Acquisition Cost (CAC)*. Harvard Business School Background Note 526-077, junio de 2026. Fuente para definición managerial de CAC, alcance de costes, timing y variantes blended/channel/cohort/marginal. citeturn17search3

Gupta, Sunil; Lehmann, Donald R.; Stuart, Jennifer Ames. *Valuing Customers*. Journal of Marketing Research, 2003. Fuente para valoración de clientes mediante flujos/márgenes descontados y limitaciones de aproximaciones simplificadas. citeturn7search4

Fader, Peter S.; Hardie, Bruce G., trabajos de CLV contractual y no contractual. Fuente para heterogeneidad de cohortes y las dificultades de trasladar churn contractual a negocios donde la salida del cliente es latente. citeturn7search1turn7search9

Blake, Thomas; Nosko, Chris; Tadelis, Steven. *Consumer Heterogeneity and Paid Search Effectiveness: A Large Scale Field Experiment*. Trabajo de eBay Research Labs/academia, versión 2014 y publicación posterior en Econometrica. Fuente para sesgo de atribución en paid search y experimentos branded/non-branded. citeturn17search4

Vaver, Jon; Koehler, Jim. *Measuring Ad Effectiveness Using Geo Experiments*. Google, 2011. Fuente metodológica para experimentos geográficos con tratamiento/control. citeturn17search1

Kerman, Jouni; Wang, Peng; Vaver, Jon. *Estimating Ad Effectiveness using Geo Experiments in a Time-Based Regression Framework*. Google, 2017. Fuente para extensión a escenarios con pocos geos/matched markets. citeturn17search5

**[P] Fuentes corporativas primarias usadas como casos, no benchmarks.**

Airbnb, Form 10-K correspondiente a 2021. Fuente para estrategia de brand/communications/performance marketing y menor dependencia de performance gracias a la fortaleza de marca. citeturn14search2

**Casos empresariales documentados, usados solo como ejemplos y no como benchmarks.**

Reuters, 1 de marzo de 2018, reporte sobre P&G y la reducción de US$200 millones de inversión digital de 2017 tras revisar viewership/viewability y alcance efectivo. citeturn14search15

Cobertura pública de la presentación de Simon Peel, entonces Global Media Director de Adidas, sobre el cambio desde last-click/performance hacia medición econométrica y brand. Las cifras 77/23 y 65% pertenecen al caso Adidas y **no se generalizan a otras marcas**. citeturn15search0turn15search9

**[V] Fuentes de proveedores/inversionistas — identificadas para evitar convertirlas en leyes.**

Mailchimp/Intuit, *Apple Mail Privacy Protection FAQs* y *About Open and Click Rates*, consultadas el 12 de agosto de 2026. Financiación/publicación: Mailchimp, proveedor de email marketing propiedad de Intuit. Se usa para describir cómo su producto calcula opens/clicks y cómo MPP afecta sus mediciones; **no se usa para establecer benchmarks de open rate**. citeturn20search3turn20search7

David Skok, *ForEntrepreneurs / SaaS Metrics*. Publicación de operador/inversionista vinculada a Matrix Partners. Se utiliza exclusivamente para documentar la procedencia empresarial de la heurística LTV:CAC ≈3 y payback; no como ley económica. citeturn6search2turn6search5

Bessemer Venture Partners, guías de cloud/SaaS metrics. Financiación/publicación: Bessemer Venture Partners. Se usa como evidencia de que la orientación 3x circula en el ecosistema de venture/SaaS, no como benchmark universal. citeturn6search7

**[X] Material explícitamente excluido del curso:** promedios de CTR/CPC/CPM/CPA/ROAS por “industria” sin mercado, muestra, año y metodología; tablas SEO o social copiadas entre blogs sin dataset; “frecuencia óptima” universal; open-rate benchmarks sin separación de MPP/bots; CAC promedio global; payback universal; y cualquier uso de **3:1** que omita que es una heurística de origen operativo/inversionista SaaS y que su resultado depende por completo de cómo se hayan construido LTV y CAC.