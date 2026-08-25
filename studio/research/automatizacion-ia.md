# Automatización de marketing con IA sin herramientas enterprise

**Guía práctica 2026 para negocios chicos y marketers solos**

Datos verificados en agosto de 2026. Precios en dólares. Las fuentes están al final.

---

## Cómo usar este documento

Este documento asume que sabés de marketing y no de programación. Cada término técnico se explica la primera vez que aparece.

Está ordenado así:

1. **Glosario** — los diez términos que necesitás para entender el resto.
2. **La decisión que define tu costo** — por qué el mismo flujo cuesta $0 en una herramienta y $73 en otra.
3. **Las tres plataformas** — Zapier, Make, n8n: qué son, qué cuestan, cuál te conviene.
4. **Cuánto cuesta la IA de verdad** — con números, no con estimaciones vagas.
5. **Cuatro flujos concretos** — paso a paso, con un negocio de ejemplo cada uno.
6. **Qué rinde y qué no** — ordenado por retorno real.
7. **Presupuestos** — tres escenarios completos.
8. **Errores caros** — los que se repiten.
9. **Plan de 30 días** — por dónde empezar.

---

## 1. Glosario mínimo

No necesitás más que esto.

**Flujo (o *workflow*, o *escenario*, o *Zap*)**
Una receta automática. "Cuando pase X, hacé Y, después Z." Cada plataforma le pone un nombre distinto a lo mismo: Zapier los llama *Zaps*, Make los llama *escenarios*, n8n los llama *workflows*.

**Disparador (o *trigger*)**
Lo que arranca el flujo. Puede ser un horario ("todos los lunes a las 8 AM"), un evento ("llegó un formulario nuevo") o una condición ("las ventas bajaron 20%").

**Paso (o *acción*, o *módulo*, o *nodo*)**
Cada cosa individual que el flujo hace. "Leer la planilla" es un paso. "Escribir el resumen con IA" es otro. "Mandar el mail" es otro. **Esto importa mucho para el costo: leelo de nuevo.**

**API**
La puerta de entrada que una herramienta le abre a otras herramientas. Google Analytics tiene una API: eso significa que otro programa puede pedirle datos sin que vos entres a la interfaz y hagas clic. Cuando alguien dice "no hay API para eso", quiere decir que solo se puede hacer a mano.

**Token**
La unidad con la que se mide y se cobra el texto que procesa una IA. Aproximadamente, **1 token ≈ 0,75 palabras en español**. Un párrafo de 100 palabras son unos 135 tokens. Los precios de IA se publican "por millón de tokens", que suena enorme y lo es: un millón de tokens son unas 750.000 palabras, más o menos diez libros.

**Webhook vs. polling**
Dos formas de que una herramienta se entere de que pasó algo.
- *Polling* es preguntar cada tanto: "¿hay algo nuevo? ¿y ahora? ¿y ahora?". Gasta recursos preguntando aunque no haya nada.
- *Webhook* es al revés: la otra herramienta te avisa cuando pasa algo. Más barato y más rápido. Siempre que puedas elegir, elegí webhook.

**Self-hosted vs. cloud**
- *Cloud* significa que la empresa corre el software en sus servidores y vos pagás una suscripción.
- *Self-hosted* significa que vos corrés el software en un servidor propio. El software puede ser gratis, pero pagás el servidor y te hacés cargo del mantenimiento.

**VPS**
Un servidor alquilado. Cuesta entre $4 y $20 al mes. Es lo que necesitás si vas por el camino *self-hosted*.

**Rate limit (límite de llamadas)**
El tope de veces por hora o por día que una plataforma te deja usar su API. Instagram, Meta Ads y Google Analytics tienen límites distintos. Este es el motivo número uno por el que una automatización "funciona en la prueba" y se rompe en producción.

**Human in the loop**
Un paso donde una persona aprueba antes de que el flujo siga. Es la diferencia entre "la IA me propone 40 anuncios y yo elijo 6" y "la IA publicó 40 anuncios anoche".

---

## 2. La decisión que define tu costo

Esto es lo más importante del documento y casi nadie lo explica bien.

Las tres plataformas cobran por cosas distintas:

| Plataforma | ¿Qué te cobra? |
|---|---|
| **Zapier** | Cada **acción** ejecutada |
| **Make** | Cada **paso** ejecutado |
| **n8n** | Cada **flujo completo** ejecutado |

Parece un detalle contable. Es la diferencia entre gratis y $73 al mes.

### Ejemplo real

Tenés una tienda de ropa online. Querés un flujo que, cada vez que entra un pedido:

1. Lee los datos del pedido
2. Busca si el cliente ya compró antes
3. Le asigna un segmento (nuevo / recurrente / VIP)
4. Lo escribe en tu planilla de clientes
5. Le manda un mail de bienvenida distinto según el segmento

Son 5 pasos. Recibís 30 pedidos por día, o sea 900 al mes.

| Plataforma | Cálculo | Consumo mensual |
|---|---|---|
| **n8n** | 900 ejecuciones de flujo | **900 ejecuciones** |
| **Make** | 5 pasos × 900 | **4.500 créditos** |
| **Zapier** | 4 acciones × 900 | **3.600 tasks** |

Ahora los planes:

- **n8n**: 900 entra cómodo en el plan Starter ($24/mes) y es gratis e ilimitado si lo tenés en servidor propio.
- **Make**: 4.500 créditos entran en el plan Core, que cuesta unos $10,59/mes con 10.000 créditos.
- **Zapier**: 3.600 tasks te obliga al tramo de 5.000 tasks, que sale alrededor de **$73/mes** con pago anual.

El flujo es idéntico. El resultado de negocio es idéntico. La factura no.

### La regla que sale de acá

> **Cuantos más pasos tiene tu flujo, más te conviene n8n. Cuantos menos pasos, menos importa la diferencia.**

Y los flujos con IA tienden a tener muchos pasos: leer datos, limpiarlos, mandarlos al modelo, validar la respuesta, guardarla, notificar. Seis u ocho pasos es lo normal. Por eso la automatización con IA es exactamente el caso donde el modelo de cobro de Zapier duele más.

---

## 3. Las tres plataformas

### Zapier

**Qué es:** la más vieja y la más fácil. Conecta más de 9.000 aplicaciones. Si existe una herramienta rara que usás, es probable que Zapier sea el único que la soporte.

**Tier gratuito:** 100 tasks al mes, y —esto es lo que lo mata— **los flujos gratuitos solo pueden tener dos pasos**: un disparador y una acción. No podés poner condiciones, ni ramificaciones, ni encadenar. Además revisa si hay novedades solo cada 15 minutos.

Traducido: el plan gratuito de Zapier sirve para aprender la interfaz, no para operar.

**Primer plan pago:** Professional, desde $19.99/mes con pago anual (750 tasks). Ahí sí tenés flujos de varios pasos, condiciones y revisión cada 2 minutos.

**Cuándo elegirlo:** cuando la integración que necesitás no existe en los otros dos, o cuando no tenés a nadie con perfil técnico y el volumen es bajo.

### Make

**Qué es:** el punto medio. Interfaz visual de arrastrar y conectar, más potente que Zapier, más fácil que n8n.

**Tier gratuito:** 1.000 créditos al mes, **2 escenarios activos**, y un intervalo mínimo de 15 minutos entre corridas programadas. Esto sí sirve para algo real: alcanza para un flujo diario de 8 pasos (240 créditos al mes) con margen de sobra.

**Primer plan pago:** Core, alrededor de $10,59/mes con 10.000 créditos.

**Cuándo elegirlo:** es el mejor valor si no querés administrar un servidor. Para la mayoría de los negocios chicos, esta es la respuesta correcta.

**Ojo con un detalle:** en agosto de 2025 Make renombró las "operaciones" a "créditos", y las funciones de IA consumen créditos a un ritmo distinto que un paso normal. Revisá el consumo real en el panel durante el primer mes antes de asumir que tu estimación era correcta.

### n8n

**Qué es:** de código abierto. Podés usar su servicio en la nube, o instalarlo en un servidor propio y usarlo gratis sin límite de ejecuciones.

**Tier gratuito en la nube:** no existe uno permanente. Hay 14 días de prueba sin tarjeta.

**Versión gratuita real:** la *Community Edition*, que instalás en tu propio servidor. Incluye casi todas las funciones; lo que falta son cosas de empresa grande (inicio de sesión corporativo, auditoría, permisos por equipo).

**Planes en la nube:** Starter $24/mes (2.500 ejecuciones), Pro $60/mes (10.000 ejecuciones). En 2026 se eliminaron los topes de usuarios y de flujos activos: lo único que mueve la factura es el volumen de ejecuciones.

**Un detalle importante:** en Starter y Pro, cuando llegás al tope de ejecuciones **los flujos se pausan hasta que empieza el ciclo siguiente**. No hay cobro por exceso, pero tampoco hay servicio. Si tenés un flujo crítico, dimensioná con holgura.

**Cuándo elegirlo:** cuando alguien del equipo puede manejar un servidor, o cuando el volumen hace que el modelo por-paso sea insostenible.

**El costo real del self-hosting** no es el servidor de $5. Son unas 4 a 8 horas de instalación inicial, unas 2 horas por mes de mantenimiento (actualizaciones, respaldos, monitoreo), y el hecho de que si algo se rompe un domingo a la madrugada, no hay a quién llamar.

---

## 4. Cuánto cuesta la IA de verdad

Esta es la parte que la gente sobreestima por un factor de diez.

Precios por millón de tokens (recordá: un millón de tokens ≈ 750.000 palabras):

| Modelo | Entrada | Salida |
|---|---|---|
| Claude Haiku 4.5 | $1 | $5 |
| Claude Sonnet 5 | $2 | $10 (precio introductorio hasta el 31 de agosto de 2026; después $3 / $15) |
| Claude Opus 5 | $5 | $25 |
| Gemini 2.5 Flash | $0,30 | $2,50 |

La salida siempre cuesta más que la entrada, en general unas cinco veces más. O sea: **mandarle mucho texto a la IA es barato; pedirle que escriba mucho texto es lo caro.** Un prompt de 3.000 palabras que devuelve un resumen de 200 cuesta menos que uno de 200 palabras que devuelve un artículo de 2.000.

Dos descuentos que casi nadie usa y deberían:

- **Caché**: si le mandás el mismo contexto una y otra vez (por ejemplo, la guía de marca de tu cliente en cada generación de copy), ese contexto repetido cuesta un 10% del precio normal.
- **Batch (por lotes)**: si no necesitás la respuesta en el momento, mandás el trabajo en lote y pagás la mitad. Reportes nocturnos y generación masiva de variaciones son casos perfectos: nadie está esperando frente a la pantalla.

### Números concretos

**Resumen semanal de Google Analytics.** Le mandás los datos crudos (unas 2.200 palabras) y te devuelve un resumen ejecutivo (unas 600 palabras), con el modelo más barato.
→ **Menos de un centavo por corrida. Tres centavos al mes.**

**200 variaciones de copy publicitario al mes.** Cada una con contexto de marca e instrucciones, devolviendo título, texto principal, descripción y llamado a la acción.
→ **Alrededor de $2,60 al mes.** Con procesamiento por lotes, $1,30.

Comparalo con lo que estás pagando de plataforma de automatización. **La IA es la línea barata de tu presupuesto.** Lo caro es el sistema de plomería que la rodea.

### Sobre los planes gratuitos de IA

Gemini tiene el plan gratuito más usable de la industria, pero hay que decir tres cosas:

1. Google recortó las cuotas gratuitas entre 50% y 80% en diciembre de 2025, y los números publicados varían entre fuentes y entre regiones. Verificá los tuyos en la consola de Google AI Studio antes de diseñar nada encima.
2. Los términos del plan gratuito **permiten que Google use tus prompts para entrenar modelos**. El plan pago y Vertex AI, no. Si vas a procesar datos de clientes, esto solo te descalifica del plan gratuito.
3. Construir un sistema de producción entero sobre cuotas gratuitas es frágil por definición. Un modelo pequeño pago a $2 o $3 al mes te compra estabilidad y previsibilidad. Vale la pena.

---

## 5. Cuatro flujos concretos

### Flujo 1 — Reporte automático de Google Analytics

**Para quién:** cualquiera que hoy entre a GA4, saque capturas de pantalla y las pegue en un documento una vez por semana o por mes.

**Negocio de ejemplo:** una agencia de dos personas con cinco clientes. Hoy dedican una tarde completa por mes a armar reportes.

**Por qué este primero:** es el único flujo de la lista donde el ahorro es medible, el riesgo es cero, los datos ya son tuyos y no dependés de que ninguna plataforma te apruebe nada. Referencias del sector estiman que reemplaza entre 3 y 4 horas de trabajo manual por cliente al mes. Con cinco clientes, son 15 a 20 horas mensuales.

**Cómo funciona:**

```
Todos los lunes 8 AM
    ↓
Pedir datos a Google Analytics
    ↓
Guardarlos en una planilla de Google
    ↓
Mandarle los datos a la IA para que escriba el resumen
    ↓
Enviar el resumen por mail o Slack
```

**Pasos de armado:**

1. **Habilitar el acceso a los datos.** En la Consola de Google Cloud (es gratis crear una cuenta), creás un proyecto y activás la "Google Analytics Data API". Después creás lo que se llama una *cuenta de servicio*: es un usuario robot que va a leer tus datos. Google te da un archivo de credenciales para descargar.

2. **Darle permiso a ese robot.** En Google Analytics, agregás la cuenta de servicio como usuario con permiso de solo lectura (*Viewer*).

3. **Armar el disparador.** En Make o n8n, un paso de horario: lunes a las 8 AM.

4. **Pedir los datos.** Configurás el paso de Google Analytics y **pedís tres métricas, no quince**: sesiones, usuarios y conversiones, separadas por canal de origen. Es tentador pedir todo. No lo hagas: cuantos más datos le mandás a la IA, más ruido tiene el resumen.

5. **Guardar en la planilla.** Acá hay un detalle que rompe muchos flujos: guardá **actualizando la fila de esa fecha si ya existe**, en vez de agregar siempre una fila nueva. Si no, cada vez que el flujo se reintenta por un error, te duplica los datos y los promedios quedan mal.

6. **El paso de IA.** Le mandás los datos y un prompt con formato fijo. Algo así:

   > Sos analista de marketing. Con estos datos, escribí exactamente tres párrafos: (1) qué cambió respecto de la semana anterior, con números; (2) la causa más probable del cambio; (3) una sola acción recomendada para esta semana. No uses adjetivos entusiastas. Si los datos no permiten sacar una conclusión, decilo.

   Esa última frase importa más de lo que parece: sin ella, la IA inventa explicaciones cuando no hay señal.

7. **Enviar.** Mail o Slack.

**Alternativa sin plataforma de automatización.** Si no querés montar nada: instalá un complemento de Google Sheets que traiga datos de GA4 (hay varios en el Marketplace de Google Workspace, con refresco automático de hasta una vez por hora, sujeto solo a las cuotas de Google). Después usás Apps Script —el sistema de automatización que ya viene incluido en Google Sheets, gratis— para llamar a la IA. Cero suscripciones.

**Costo mensual:** $0 en infraestructura si vas por Apps Script, unos 5 centavos en IA.

---

### Flujo 2 — Monitoreo de competencia

**Para quién:** cualquiera que hoy revise a mano los sitios y los rankings de sus competidores.

**Negocio de ejemplo:** una tienda de suplementos deportivos que compite con cinco marcas y quiere enterarse cuando alguna baja precios, publica contenido nuevo o le gana posiciones en Google.

**Cómo funciona:**

```
Todos los días, dos veces
    ↓
Consultar posiciones en buscadores (vía un servicio de datos de búsqueda)
    ↓
Revisar si publicaron páginas nuevas (comparando el mapa del sitio contra el de ayer)
    ↓
Mandarle los cambios a la IA para que separe lo importante de lo irrelevante
    ↓
Avisar solo lo que amerita
```

**Números de una implementación documentada:** cinco dominios monitoreados en cincuenta palabras clave, corriendo dos veces por día. **Costo total: $21,60 al mes**, de los cuales solo $1,10 son las consultas de búsqueda (el servicio DataForSEO cobra $0,0006 por palabra clave). El resto es el servidor.

**La cifra honesta sobre el rendimiento:** ese mismo caso genera unas **14 alertas por semana, de las cuales solo 2 o 3 son accionables**. No es un problema del sistema; es la naturaleza del monitoreo competitivo. Lo importante no es generar más alertas sino filtrarlas bien. Ese es exactamente el trabajo que le das a la IA en el paso 3: no que detecte cambios, sino que decida cuáles merecen tu atención.

**Un detalle técnico que vale su peso:** las URLs del mismo contenido pueden verse distintas (con o sin barra final, con o sin parámetros de campaña). Si no las normalizás antes de comparar, el sistema te avisa "contenido nuevo" cuando no lo hay. En el caso documentado, arreglar esto bajó los falsos positivos del 35% a menos del 8%.

**No lo construyas desde cero.** El repositorio público de plantillas de n8n tiene varias listas para importar: buscá *"Competitor Intelligence Agent"*, *"SERP competitor research"*, *"Price monitoring dashboard"*. Importás la plantilla, reemplazás las credenciales por las tuyas y ajustás el prompt.

**Costo mensual:** $1 a $3 en servicios de datos, más IA. El servidor ya lo estás pagando por el flujo 1.

---

### Flujo 3 — Generación de variaciones de anuncios

Acá hay que separar dos cosas que se mezclan todo el tiempo:

- **Generar** variaciones es fácil, barato y funciona muy bien.
- **Publicarlas automáticamente** en Meta es donde todo se complica.

**Negocio de ejemplo:** una escuela de idiomas que corre anuncios en Instagram y necesita probar ángulos distintos cada semana.

#### La parte que funciona: generación

1. **Armá una planilla de entrada** con estas columnas: ángulo (miedo a quedarse atrás / aspiracional / precio / prueba social), público objetivo, oferta, prueba social disponible, límite de caracteres.

2. **El flujo lee las filas pendientes** y por cada una le pide a la IA que devuelva un conjunto estructurado: título, texto principal, descripción, llamado a la acción. Pedile explícitamente que devuelva los campos separados, no un párrafo suelto — así se pueden escribir en columnas distintas.

3. **Escribe las variaciones de vuelta en la planilla**, en filas nuevas, con una columna de estado que diga `borrador`.

4. **Vos revisás en la planilla.** Cambiás el estado a `aprobado` en las que sirven.

5. **Solo lo aprobado sigue** al paso siguiente.

Ese paso 4 es el *human in the loop*, y es lo que hace que este flujo sea seguro.

#### La parte que se complica: publicación

Meta clasifica el acceso a su API de publicidad en niveles, y el nivel por defecto es de juguete: da 60 "puntos" que se regeneran cada 5 minutos, y una carga de creativos consume 30 o 40 puntos. **O sea: entre 10 y 13 anuncios y te quedaste sin cuota.**

En mayo de 2026 Meta reestructuró estos niveles y los renombró (ahora son *Limited Access* y *Full Access*). La buena noticia para un negocio chico: **si solo vas a crear anuncios en tus propias cuentas publicitarias, el acceso estándar alcanza.** El nivel avanzado, que requiere una revisión formal de Meta que tarda semanas, solo hace falta si vas a operar cuentas de terceros — es decir, si sos una agencia construyendo una herramienta para clientes.

**Dos recomendaciones firmes:**

1. Mantené el humano en el loop. La ganancia de tiempo está en generar y versionar, no en publicar sin mirar.
2. Si igual automatizás la publicación, **dejá las campañas en estado PAUSADO por defecto.** Revisás y activás a mano. Un error de configuración que se publica solo puede quemar presupuesto durante horas antes de que te enteres.

**Costo mensual:** $1 a $3 en IA.

---

### Flujo 4 — Publicación en redes sociales

Este es el que todo el mundo quiere primero y el que peor relación esfuerzo/beneficio tiene. Vale la pena explicar por qué.

**Generar el contenido funciona bien.** Tenés una cola en una planilla, la IA adapta cada pieza al formato de cada red, listo.

**Publicarlo automáticamente es un campo minado.** El panorama en 2026:

- **X (Twitter)**: es de pago por uso. Alrededor de $0,20 por publicación que incluya un enlace.
- **Meta (Instagram, Facebook, Threads)**: gratis, pero detrás de un proceso de revisión de aplicación.
- **LinkedIn**: la API de gestión de comunidad exige aprobación como partner oficial. Para la mayoría, inaccesible.
- **TikTok**: obliga a pasar una auditoría en entorno de pruebas.

Y en el detalle de Instagram, que es la que más pide la gente:

- Solo cuentas Business o Creator, nunca personales.
- Solo a través de la API de Facebook, no directo.
- **Solo imágenes JPEG.** No PNG, no HEIC.
- Tope duro de **50 publicaciones cada 24 horas**.
- **Stories, etiquetas de compra y filtros no son accesibles por API en ninguna herramienta.** No es una limitación de tu automatización; no existe la puerta.

Y el riesgo estructural: en diciembre de 2024 Meta discontinuó una de sus APIs de Instagram y **todos los flujos construidos sobre ella dejaron de funcionar de un día para el otro**. Los cambios de plataforma no se arreglan solos. Los arreglás vos, y te enterás cuando algo dejó de publicarse.

**La recomendación práctica:** no integres cada red por separado. Usá un servicio unificado de publicación (Blotato, Upload-Post, Postiz, Zernio y varios más) que te da una sola puerta para todas las redes. Absorben las colas de revisión, los cambios de API y los formatos, a cambio de unos $10 a $30 mensuales. Es dinero bien gastado.

O, directamente: programá los posts a mano en Meta Business Suite, que es gratis, y usá tu automatización solo para *generar* el contenido.

---

## 6. Qué rinde y qué no

**Ordenado por retorno real para un negocio chico:**

| # | Flujo | Por qué |
|---|---|---|
| 1 | **Reportes automáticos** | Máximo ahorro de horas, cero dependencias externas, datos propios. Empezá siempre acá. |
| 2 | **Enrutamiento y respuesta de leads** | Impacto directo en ingresos. Cuidado: es el que más rápido quema cuota en Zapier. |
| 3 | **Monitoreo de competencia** | Barato, señal moderada. Calibrá expectativas: 2 o 3 alertas útiles por semana. |
| 4 | **Generación de variaciones creativas** | Alto valor como asistente. Bajo valor como sistema autónomo. |
| 5 | **Publicación social automática** | La fricción de las plataformas se come el beneficio. Delegá o hacelo a mano. |

**Lo que no rinde a esta escala:** los sistemas de "agentes autónomos" que deciden estrategia solos. Cuando hay una sola persona supervisando, el costo de revisar lo que hizo el sistema supera el ahorro de que lo haya hecho. La arquitectura que funciona para un negocio chico es la aburrida: un flujo predecible, de pasos fijos, con llamadas a la IA en momentos específicos y acotados. La IA escribe, clasifica y resume. No decide.

---

## 7. Tres presupuestos completos

### Escenario A — $0 al mes

- Google Sheets + Apps Script (el automatizador que ya viene incluido, gratis)
- API de datos de Google Analytics (gratis dentro de cuota)
- Plan gratuito de un modelo de IA

**Cubre:** reportes y generación de textos.
**Techo:** cuotas de Apps Script, cuotas variables del modelo gratuito, y la prohibición práctica de meter datos de clientes en un plan gratuito que puede usarlos para entrenamiento.

### Escenario B — $8 a $12 al mes

- Servidor propio con n8n Community: $3,70/mes en un hosting administrado tipo PikaPods, o $5 a $6 en un VPS que administrás vos. Ejecuciones ilimitadas.
- Modelo de IA económico, pago: $2 a $5/mes.

**Cubre:** los cuatro flujos, sin techo práctico de volumen.
**Requiere:** alguien que pueda instalar y mantener. Unas 4 a 8 horas iniciales y 2 horas mensuales.

### Escenario C — $35 a $45 al mes

- Make Core ($10,59) o n8n Cloud Starter ($24)
- Servicio de datos de búsqueda: $1 a $3
- IA: $3 a $8
- Margen para un servicio unificado de publicación si lo necesitás

**Cubre:** lo mismo que B, sin administrar servidores.
**Es el escenario correcto** para un marketer sin perfil técnico o para un negocio que prefiere pagar por no tener que pensar en infraestructura.

---

## 8. Errores caros que se repiten

**Poner los filtros al final.** Si tu flujo hace dos acciones y recién después descarta el registro porque no cumplía una condición, pagaste esas dos acciones para nada. En un caso documentado, mover el filtro al primer paso bajó el consumo mensual un 30% sin cambiar el resultado.

**Usar polling donde podés usar webhook.** Preguntar cada 5 minutos si hay algo nuevo significa 8.640 verificaciones al mes desde un solo flujo. Si la herramienta soporta webhooks, la otra parte te avisa y no gastás nada esperando.

**Subestimar el consumo por un factor de 3 a 5.** Es el error más común y siempre pasa por lo mismo: la gente cuenta flujos, no ejecuciones. "Tengo tres automatizaciones" no dice nada. "Tengo tres automatizaciones de seis pasos que corren 900 veces al mes" son 16.200 pasos. Hacé la multiplicación antes de elegir plan.

**Agregar filas en vez de actualizarlas.** Cualquier flujo que escriba en una planilla y no maneje el caso de "esta fecha ya existe" te va a duplicar datos en el primer reintento por error de red.

**Construir todo el sistema sobre cuotas gratuitas.** Los planes gratuitos cambian. El de Gemini se recortó entre 50% y 80% de un mes para otro. Si tu operación depende de eso, tu operación es frágil.

**Automatizar la publicación antes que el reporte.** Publicar es lo más visible y lo que peor funciona. Reportar es lo menos glamoroso y lo que más horas ahorra.

---

## 9. Plan de 30 días

**Semana 1 — Medir antes de automatizar.**
Anotá durante una semana cuánto tiempo real dedicás a tareas repetitivas y cuáles son. No automatices por intuición: la tarea que más te molesta no suele ser la que más tiempo consume.

**Semana 2 — Armar el flujo de reportes.**
Solo ese. Con un solo cliente o una sola propiedad. Que funcione tres semanas seguidas antes de agregar nada.

**Semana 3 — Medir el consumo real.**
Mirá el panel de tu plataforma y anotá cuántas ejecuciones o créditos consumió el flujo. Ahora sí podés proyectar qué plan vas a necesitar cuando lo repliques.

**Semana 4 — Elegir el segundo flujo según lo que midiste en la semana 1.**
Si tu cuello de botella son los leads, hacé el de leads. Si es la producción de contenido, hacé el de generación de variaciones. No copies el orden de esta guía si tus números dicen otra cosa.

**Lo que no hagas en los primeros 30 días:** automatizar la publicación en redes, montar sistemas multi-agente, o pagar un plan anual antes de haber medido tu consumo real durante un mes completo.

---

## Fuentes

Precios y límites verificados en agosto de 2026. Todos cambian; revisá antes de comprometerte.

**Plataformas de automatización**
- Zapier — planes y precios oficiales: https://zapier.com/pricing
- Zapier — qué incluye el plan gratuito: https://help.zapier.com/hc/en-us/articles/32337438839565-What-s-included-in-Zapier-s-Free-plan
- Make — análisis de precios y créditos 2026: https://workflowpick.com/pricing-guides/make-com-pricing-2026-review/
- Make — cambio de operaciones a créditos: https://alltomate.com/blogs/make-com-pricing-plans-explained/
- n8n — documentación de ediciones y Community Edition: https://docs.n8n.io/deploy/host-n8n/community-edition-features
- n8n — precios oficiales: https://n8n.io/pricing/
- n8n — análisis de costos cloud vs. self-hosted: https://instapods.com/blog/n8n-pricing/ y https://www.nocode.mba/articles/n8n-pricing

**Modelos de IA**
- Precios oficiales de la plataforma Claude: https://platform.claude.com/docs/en/about-claude/pricing
- Claude Haiku 4.5: https://www.anthropic.com/news/claude-haiku-4-5
- Límites del plan gratuito de Gemini: https://tokenmix.ai/blog/gemini-api-free-tier-limits y https://www.aifreeapi.com/en/posts/gemini-api-free-tier-complete-guide

**Google Analytics**
- Conectar GA4 a un automatizador, paso a paso: https://www.graphed.com/blog/how-to-connect-google-analytics-to-n8n
- Pipeline completo GA4 → Sheets → IA → Slack: https://whoisalfaz.me/blog/n8n-google-analytics-4-pipeline/
- Complemento de GA4 para Google Sheets: https://workspace.google.com/marketplace/app/ga4_reporting_for_google_analytics_4/126881055683

**Monitoreo de competencia**
- Implementación con costos desglosados: https://nextgrowth.ai/seo-competitive-intelligence-guide/
- Costos de operación de una agencia chica: https://nextgrowth.ai/n8n-google-search-console-automation/
- Plantillas listas para importar: https://n8n.io/workflows/10252-competitor-intelligence-agent-serp-monitoring-summary-with-thordata-openai/ y https://n8n.io/workflows/6428-price-monitoring-dashboard-with-ai-component-and-alerts/

**APIs de redes sociales y publicidad**
- Panorama comparado de todas las APIs sociales en 2026: https://www.blotato.com/blog/social-media-api
- Limitaciones reales de la automatización social: https://autoadify.com/blog/n8n-social-media-automation-limitations
- Niveles de acceso de la API de publicidad de Meta: https://www.adamigo.ai/blog/meta-ads-api-key-creation-workflow-explained
- Cuotas del nivel gratuito de la API de Meta: https://www.get-ryze.ai/blog/meta-marketing-api-free-tier-limitations-and-quotas
