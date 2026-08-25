# Curso: Email Marketing para E-commerce — LatAm 2026

Diseño de curso práctico. Datos verificados a agosto de 2026.

---

## Ficha del curso

| Campo | Valor |
|---|---|
| Público | Dueños de tiendas online, encargados de marketing en PyME, freelancers de e-commerce en LatAm |
| Nivel de entrada | Sin conocimientos previos de email marketing. Requiere tener (o estar armando) una tienda online |
| Duración | 10 módulos / 8 semanas / ~22 h de contenido + ~15 h de trabajo práctico |
| Formato | Video + workbook + plantillas + revisión de proyecto |
| Herramienta obligatoria | Una cuenta gratuita en Brevo o Klaviyo (ambas permiten completar el curso sin pagar) |
| Entregable final | Programa de email operativo: 5 flujos activos, autenticación configurada, tablero de métricas |
| Idioma / moneda | Español neutro LatAm. Precios en USD con nota de conversión; ejemplos con ticket en USD y equivalencia local |

**Promesa concreta del curso:** al terminar, el alumno tiene cinco flujos automatizados corriendo, dominio autenticado (SPF/DKIM/DMARC) y un tablero de cuatro métricas. No "aprende sobre" email marketing: lo deja funcionando.

---

## Nota metodológica (leer antes de dictar el curso)

1. **Los precios de plataformas cambian varias veces al año.** Mailchimp modificó su plan gratuito en enero de 2026 (efectivo el 17 de febrero) y subió precios de planes pagos alrededor de abril de 2026. Klaviyo cambió su modelo de cobro a "perfiles activos" en febrero de 2025. Todo precio en este curso debe re-verificarse en la página oficial del proveedor antes de cada cohorte. El módulo 1 incluye un ejercicio donde el alumno verifica los precios él mismo, lo que resuelve la obsolescencia estructuralmente.

2. **Los benchmarks provienen mayoritariamente de datasets de EE.UU./Europa.** Klaviyo publica sobre 183.000 marcas; Omnisend sobre ~150.000. No existe un dataset público equivalente de LatAm con rigor comparable. El curso debe enseñar los benchmarks globales como *orden de magnitud* y enseñar al alumno a construir su propio baseline en 60-90 días. Esto se dice explícitamente en el módulo 8, no se esconde.

3. **Las tasas de apertura están rotas desde iOS 15.** Apple Mail Privacy Protection precarga los píxeles de seguimiento, generando "aperturas" que nunca ocurrieron. La inflación estimada va de 40% a 68% en usuarios de Apple Mail. Todo el curso trata la apertura como métrica direccional de entregabilidad, nunca como KPI.

---

## Mapa de módulos

| # | Módulo | Horas | Entregable del alumno |
|---|---|---|---|
| 0 | Contexto: por qué email en un continente de WhatsApp | 1,0 | Decisión de mix de canales documentada |
| 1 | Plataformas: comparativa honesta y decisión | 2,0 | Plataforma elegida y cuenta creada |
| 2 | Captura de lista, consentimiento y ley | 2,0 | Formulario de captura + texto de consentimiento |
| 3 | Entregabilidad: SPF, DKIM, DMARC y no caer en spam | 3,0 | Dominio autenticado + Postmaster Tools activo |
| 4 | Los cinco flujos (núcleo del curso) | 6,0 | 5 flujos construidos y activos |
| 5 | Copywriting: asuntos y cuerpos | 3,0 | 30 asuntos + 5 cuerpos escritos |
| 6 | Segmentación y RFM | 2,5 | Hoja de RFM con 6 segmentos accionables |
| 7 | Diseño móvil que convierte | 2,0 | Plantilla base propia, testeada |
| 8 | Métricas: cuáles importan y cuáles ignorar | 2,0 | Tablero de 4 métricas + baseline propio |
| 9 | IA aplicada: dónde sirve y dónde estorba | 1,5 | Biblioteca de prompts + política de revisión |
| 10 | Errores comunes y auditoría final | 1,0 | Auditoría de su propio programa |

---

# Módulo 0 — Contexto: por qué email en un continente de WhatsApp

**Objetivo:** que el alumno entienda dónde encaja el email en LatAm y no lo abandone por el canal de moda.

## Contenido

**El argumento honesto.** WhatsApp domina la mensajería en LatAm de forma que no tiene paralelo en EE.UU. o Europa. México supera los 90 millones de usuarios de WhatsApp (~70% de la población). Entre 62% y 80% de los usuarios de WhatsApp en la región ya se comunican con empresas por ese canal. Las proyecciones de transacciones comerciales vía WhatsApp en LatAm superan los USD 15.000 millones anuales hacia 2027. Un instructor que finja que el email es el canal principal en LatAm pierde credibilidad en el minuto tres.

**Por qué el email sigue siendo la base:**

| Dimensión | Email | WhatsApp Business API |
|---|---|---|
| Costo marginal por mensaje | Cercano a cero dentro del plan | Se paga por conversación/plantilla |
| Propiedad del canal | La lista es tuya, exportable | Depende de políticas de Meta |
| Tolerancia a frecuencia | Alta (2-4/semana aceptable) | Muy baja; satura y genera bloqueos |
| Aptitud para contenido largo | Alta | Baja |
| Aptitud para catálogo/imágenes | Alta | Media |
| Riesgo regulatorio de opt-in | Medio | Alto (opt-in explícito estricto) |
| Costo de recuperar un carrito | Marginal | Real por mensaje |

**Regla de asignación que enseña el curso:**
- **Email** = capa base. Todos los flujos, todo el contenido, todas las campañas.
- **WhatsApp** = capa de urgencia y alto valor. Solo tres usos: (a) segundo toque de carrito abandonado en tickets sobre el promedio, (b) avisos de despacho/entrega, (c) back-in-stock. Nada más al principio.
- **SMS** = prácticamente irrelevante en la mayoría de LatAm; WhatsApp lo desplazó. No lo enseñamos.

**Realidad de tamaño.** El e-commerce LatAm crece pero las listas son pequeñas. La mayoría de los alumnos tendrá entre 500 y 15.000 contactos. Todo el curso está calibrado para ese rango, no para marcas de USD 20M.

## Ejercicio 0
Documentar en una hoja: tamaño actual de la lista, ticket promedio (AOV), pedidos/mes, ciclo de recompra estimado en días. Estos cuatro números se usan en todos los módulos siguientes.

---

# Módulo 1 — Plataformas: comparativa honesta

**Objetivo:** que el alumno elija plataforma con criterio y sepa cuánto le va a costar en 18 meses, no hoy.

## 1.1 Los cuatro modelos de cobro (esto es lo que realmente importa)

Antes de comparar precios hay que entender que **cobran cosas distintas**:

| Plataforma | Unidad de cobro | Consecuencia práctica |
|---|---|---|
| Klaviyo | Perfiles **activos** (todo contacto contactable, haya comprado o no) | La factura sube sola con el crecimiento de la tienda. Un checkout con email capturado ya cuenta |
| Mailchimp | Contactos totales de la audiencia | Cobra por desuscritos e inactivos salvo que los archives manualmente |
| Brevo | **Emails enviados**, contactos ilimitados | Lista grande + baja frecuencia = muy barato. Alta frecuencia = se encarece |
| ActiveCampaign | Contactos × nivel de plan | Precio sube por dos ejes a la vez |

**Este es el concepto más rentable del módulo.** Una tienda con 40.000 contactos que envía dos campañas al mes paga órdenes de magnitud distintas según el modelo. Comparar "precio de entrada" es un error de principiante.

## 1.2 Planes gratuitos (verificado a mediados de 2026)

| Plataforma | Plan gratuito | ¿Sirve para aprender? |
|---|---|---|
| **Brevo** | 300 emails/día, contactos ilimitados, automatización básica | **Sí.** Es el mejor plan gratuito real del grupo |
| **Klaviyo** | 250 perfiles, 500 emails/mes | Sí, para practicar flujos con lista muy chica. Funcionalidad completa |
| **Mailchimp** | 250 contactos, 500 emails/mes, 250/día. Sin automatización multi-paso, sin programación de envíos, con marca Mailchimp | **No.** Se recortó en enero de 2026 (efectivo 17 de febrero): antes eran 500 contactos y 1.000 envíos. Antes de 2022 eran 2.000 contactos |
| **ActiveCampaign** | No tiene. Prueba de 14 días | No |

**Punto de honestidad para el curso:** el plan gratuito de Mailchimp dejó de ser útil. Mailchimp ha recortado su capa gratuita tres veces desde 2022 y subió precios de planes pagos en abril de 2026 (~11-13%). Si un alumno llega con la idea de "empiezo con Mailchimp gratis", hay que corregirla con datos.

## 1.3 Costo real por tamaño de lista

Cifras aproximadas en USD/mes, plan de email solamente, sin SMS ni add-ons. **Verificar antes de cada cohorte.**

| Contactos | Klaviyo (Email) | Mailchimp (Standard) | Brevo (por envíos) | ActiveCampaign (Starter) |
|---|---|---|---|---|
| 250-500 | $0 (250) → $20 (500) | $0 (250) → ~$20+ | $0 hasta 9.000 envíos/mes | ~$15 (1.000) |
| 1.000 | ~$30 | ~$25-30 | $0-9 | ~$15 |
| 5.000 | ~$100 | ~$60-75 | ~$9-19 (según frecuencia) | ~$70-90 |
| 10.000 | ~$150 | ~$110 | ~$19-29 | ~$149 |
| 50.000 | ~$720 | ~$400+ | ~$29-69 | Cotización |
| 250.000 | ~$2.300 | Cotización | ~$69+ | Cotización |

Referencia de Brevo por volumen de envío: ~$9/mes por 5.000 emails, ~$19 por 20.000, ~$29 por 40.000, ~$69 por 100.000.

**Notas que hay que decir en clase:**
- Klaviyo aplica un tope de 25% al salto de precio entre escalones, pero ese descuento se erosiona con cada downgrade.
- Klaviyo pasa a su nivel enterprise (Klaviyo One, +20% sobre el gasto total) cuando el gasto mensual supera los ~$10.000.
- ActiveCampaign no tiene plan gratuito y la mayoría de las funciones de CRM/lead scoring están en Plus (~$49/mes a 1.000 contactos), no en Starter.
- El caso extremo que ilustra el modelo de cobro: una tienda con ~80.000 contactos que envía un newsletter semanal paga del orden de $49/mes en Brevo contra varios cientos en Mailchimp.

## 1.4 Qué hace bien cada una (opinión fundamentada, no ranking)

**Klaviyo** — La integración más profunda con Shopify/WooCommerce, atribución de ingresos por flujo lista para usar, analítica predictiva y RFM incluidos en niveles superiores. Es el estándar de facto en e-commerce DTC. *Contra:* el modelo de perfiles activos hace que la factura crezca sin que crezcan las ventas; la sorpresa suele llegar en el segundo año, no el primero.

**Brevo** — Mejor relación precio/función del grupo. Email + SMS + WhatsApp + CRM en una interfaz, infraestructura transaccional incluida. Cobrar por envío y no por contacto la vuelve ideal para listas grandes con baja frecuencia. *Contra:* biblioteca de plantillas más chica, automatización con menos ramificación condicional, reportes menos ergonómicos y analítica avanzada restringida a planes superiores.

**Mailchimp** — La interfaz más amable para quien nunca hizo esto y el ecosistema de integraciones más amplio. *Contra:* cobra por contactos desuscritos e inactivos si no los archivas; el constructor de automatización clásico fue deprecado en junio de 2025, empujando la automatización multi-paso al plan Standard; historial sostenido de recortes y alzas. Su ventaja competitiva se erosionó.

**ActiveCampaign** — La automatización más profunda del grupo: scoring, ramificación condicional compleja, CRM integrado. Fuerte para B2B, servicios y ciclos de venta largos. *Contra:* sin plan gratuito, curva de aprendizaje real, y la mayoría de los equipos usa una fracción de lo que paga.

**Sobre entregabilidad:** las pruebas independientes anuales (EmailToolTester, GlockApps) ubican a las cuatro en rangos comparables, del orden de 95-99% de colocación para remitentes autenticados. **La entregabilidad la determinan tus prácticas, no tu proveedor.** Este punto hay que repetirlo: es el error de atribución más común del principiante.

## 1.5 Árbol de decisión (contenido central del módulo)

```
¿Tu tienda está en Shopify/WooCommerce y facturas > USD 20k/mes?
├── SÍ → Klaviyo. La atribución por flujo y las integraciones
│         justifican el sobreprecio. Presupuesta el crecimiento
│         de la factura con anticipación.
└── NO
    ├── ¿Lista > 20.000 con frecuencia baja (1-4 envíos/mes)?
    │   └── SÍ → Brevo. El modelo por envío te ahorra mucho.
    ├── ¿Necesitas email + WhatsApp + SMS en una sola herramienta?
    │   └── SÍ → Brevo.
    ├── ¿Vendes servicios / B2B / ciclo largo con seguimiento comercial?
    │   └── SÍ → ActiveCampaign (plan Plus, no Starter).
    └── ¿Estás empezando, < 2.000 contactos, sin equipo técnico?
        └── Brevo (gratis y escalable) o Klaviyo (gratis hasta 250,
            con funcionalidad completa para aprender flujos).
```

**Recomendación por defecto del curso para LatAm:** Brevo para la mayoría de los alumnos; Klaviyo si ya facturan bien en Shopify. Mailchimp no se recomienda como punto de partida en 2026.

## Ejercicio 1
1. Abrir la página de precios oficial de las cuatro plataformas y llenar la tabla con los precios **de hoy** para el tamaño de lista propio y el proyectado a 24 meses (asumiendo el crecimiento real de los últimos 6 meses).
2. Calcular el costo total a 24 meses de las dos finalistas.
3. Crear la cuenta y conectar la tienda.

**Entregable:** tabla de costos comparados + cuenta creada y conectada.

---

# Módulo 2 — Captura de lista, consentimiento y ley

**Objetivo:** construir una lista que sea legal, entregable y que crezca sin comprar contactos.

## 2.1 La regla que ordena todo

**Nunca compres, alquiles ni importes una lista que no te dio consentimiento.** No es solo un asunto legal. Una lista comprada destruye la reputación del dominio en semanas y arrastra a la basura los envíos a la parte legítima de la lista. El daño es difícil de revertir.

## 2.2 Marco legal LatAm (estado a agosto de 2026)

**Chile — Ley 21.719.** Publicada el 13 de diciembre de 2024, **entra en plena vigencia el 1 de diciembre de 2026**. Reemplaza a la Ley 19.628 de 1999. Crea la Agencia de Protección de Datos Personales con facultades reales de fiscalización y sanción. Multas de hasta 20.000 UTM (del orden de USD 1,5 millones) o hasta 4% de los ingresos anuales en reincidencia. Exige consentimiento libre, informado, específico e inequívoco; derecho a revocarlo con la misma facilidad con que se otorgó; derechos de acceso, rectificación, supresión, oposición, portabilidad y bloqueo; notificación de brechas sin dilación indebida (estándar internacional: 72 horas). Reconoce seis bases legales, entre ellas el interés legítimo. La ley fiscaliza **evidencia operativa** —registros, logs, inventarios— no políticas escritas.

*Implicancia directa para el curso:* si el alumno es chileno, este módulo tiene fecha de vencimiento inmediata. Hay que enseñarle a guardar, para cada contacto: fecha y hora del opt-in, origen (formulario, checkout, popup), texto exacto que aceptó, e IP si la plataforma la registra. Las cuatro plataformas guardan esto; hay que saber dónde encontrarlo y exportarlo.

**Brasil — LGPD.** En vigor desde 2020, con ANPD activa. Modelo más cercano al GDPR.

**México — LFPDPPP.** Exige aviso de privacidad accesible en el punto de captura.

**Colombia, Argentina, Perú:** regímenes de habeas data con registro de bases de datos en algunos casos. Verificar por país.

**Regla operativa transversal que enseña el curso:** aplicar el estándar más alto (opt-in explícito, doble registro de consentimiento, baja en un clic) a todos los mercados. Es más simple que mantener reglas por país y te deja cubierto ante cualquier endurecimiento.

## 2.3 Mecánicas de captura ordenadas por rendimiento

| Mecánica | Volumen | Calidad de intención | Nota |
|---|---|---|---|
| Popup con incentivo (10-15% primera compra) | Alto | Media | El caballo de batalla. Disparar a los 15-30 s o al 50% de scroll, no al instante |
| Checkout (casilla de marketing) | Medio | **Muy alta** | Debe ser opt-in explícito, nunca precargado |
| Back-in-stock ("avísame") | Bajo | **Máxima** | Genera el flujo de mayor conversión que existe |
| Popup de salida (exit intent) | Medio | Baja | Segundo intento, con oferta distinta |
| Landing de sorteo/concurso | Muy alto | **Muy baja** | Enseñar el riesgo: infla la lista con cazadores de premios y hunde el engagement |
| Wi-Fi / tienda física / QR | Bajo | Alta | Subutilizado en LatAm |

**Segmentación desde el origen.** Etiquetar cada contacto con su fuente de alta. Un suscriptor de popup con 10% de descuento tiene intención distinta a uno que se registró en el checkout. Esto habilita bienvenidas diferenciadas en el módulo 4 y es una de las palancas con mejor retorno del curso.

## 2.4 Texto de consentimiento (plantilla)

> Quiero recibir novedades, ofertas y lanzamientos de [Marca] por correo electrónico. Puedo darme de baja en cualquier momento desde el enlace al final de cada email. Ver [Política de Privacidad].

Casilla **sin** marcar por defecto. Enlace a política funcional. Confirmación visible tras el envío.

## Ejercicio 2
Instalar el popup con temporizador correcto, configurar el opt-in de checkout, redactar el texto de consentimiento y verificar dónde guarda la plataforma la evidencia del consentimiento (y cómo exportarla).

---

# Módulo 3 — Entregabilidad: SPF, DKIM, DMARC y no caer en spam

**Objetivo:** que el email llegue. Este módulo es el de mayor retorno del curso y el que más se salta la gente.

## 3.1 Por qué esto es primero y no último

Con autenticación completa, la colocación en bandeja de entrada ronda el 89%; sin ella, cae al orden del 44%. Aproximadamente uno de cada seis emails falla antes de que la calidad del contenido pueda importar. Optimizar asuntos sin resolver entregabilidad es pintar una casa sin techo.

## 3.2 Los tres protocolos, explicados sin jerga

Analogía única del curso (se usa esta y ninguna otra):

- **SPF** = la lista de quiénes tienen permiso de enviar cartas a nombre de tu empresa. Es un registro DNS que dice: "estos servidores están autorizados". Si llega un correo de un servidor fuera de la lista, sospecha.
- **DKIM** = la firma con sello. Cada email sale firmado criptográficamente. El receptor verifica que la firma corresponde a tu dominio y que el contenido no fue alterado en tránsito.
- **DMARC** = la instrucción de qué hacer si algo falla. Un registro DNS que dice: si un correo dice venir de tu dominio pero no pasa SPF ni DKIM, hacé **X**. Donde X es:
  - `p=none` → no hagas nada, solo avisame (monitoreo)
  - `p=quarantine` → mandalo a spam
  - `p=reject` → rechazalo directamente

Adicionalmente, **alineación (alignment)**: no basta con que SPF o DKIM pasen; el dominio que validan debe coincidir con el dominio del campo "De:". Este es el punto donde falla la mayoría de las auditorías, junto con el enlace de baja de un clic mal implementado.

## 3.3 Requisitos vigentes de Google, Yahoo y Microsoft (2026)

**Umbral de "remitente masivo": 5.000 o más mensajes por día a casillas personales** (@gmail.com, dominios de Yahoo, y Outlook.com/Hotmail/Live). El conteo suma todos los subdominios bajo el dominio principal. Una vez que cruzás el umbral, la clasificación no expira aunque tu volumen baje después. No aplica a correo interno entre cuentas de Google Workspace.

| Requisito | Google | Yahoo | Microsoft |
|---|---|---|---|
| SPF + DKIM | Sí | Sí | Sí |
| DMARC (mínimo `p=none`) para masivos | Sí | Sí | Sí (desde mayo 2025) |
| Alineación de dominio | Sí | Sí | Sí |
| TLS en tránsito | Sí | Sí | Sí |
| Registro PTR válido | Sí | Sí | Sí |
| Baja en un clic (RFC 8058) | Sí | Sí | Recomendado, no exigido |
| Procesar bajas en ≤ 48 h | Sí | Sí | — |
| Tasa de spam | < 0,30% (objetivo < 0,10%) | < 0,30% | Sin umbral numérico público |

**Fechas relevantes:** Google y Yahoo anunciaron en octubre de 2023 con aplicación desde febrero de 2024. El plazo para la baja en un clic (RFC 8058) fue el 1 de junio de 2024. Microsoft anunció en abril de 2025 y aplica desde mayo de 2025. Google escaló la aplicación en noviembre de 2025, pasando de demoras temporales a **rechazos permanentes**.

**Qué pasa si fallás hoy:** no vas a spam, te **rechazan**. Google devuelve errores 550 permanentes a nivel SMTP; Microsoft devuelve `550 5.7.515 Access denied`. El mensaje nunca llega a ninguna carpeta.

**Detalle importante sobre la tasa de spam:** aunque el umbral es 0,30% en los tres proveedores, el cálculo de Yahoo es más estricto porque usa como denominador solo los emails entregados a bandeja de entrada, excluyendo los que fueron a spam. Con la misma cantidad de quejas, tu tasa en Yahoo sale más alta. Además, en Google, si superás 0,30%, tu dominio queda inelegible para mitigación de entrega hasta que la tasa se mantenga bajo el umbral durante siete días consecutivos.

**Excepción:** los emails transaccionales (confirmación de pedido, aviso de despacho, reseteo de contraseña) están exentos del requisito de baja en un clic, pero **no** de la autenticación.

## 3.4 Procedimiento paso a paso

1. **Usar un subdominio para marketing.** Enviar desde `envios.tumarca.com` o `news.tumarca.com`, no desde el dominio raíz. Aísla la reputación: si el marketing tiene un mal mes, tus correos transaccionales y corporativos no se contagian.
2. **Configurar SPF y DKIM** con las instrucciones del proveedor. Las cuatro plataformas dan los registros DNS listos para copiar. Toma 10 minutos y hasta 48 horas de propagación.
3. **Publicar DMARC en `p=none`** con dirección `rua=` para recibir reportes. Ejemplo de registro:
   `v=DMARC1; p=none; rua=mailto:dmarc@tumarca.com; fo=1`
4. **Leer reportes 30 días.** Confirmar que el 100% del tráfico legítimo pasa con alineación.
5. **Escalar a `p=quarantine`,** luego a `p=reject`. No saltarse el monitoreo: pasar directo a `reject` con SPF mal configurado bloquea tu propio correo.
6. **Verificar la baja en un clic.** Enviarse un correo de prueba y confirmar que Gmail muestra el botón "Cancelar suscripción" junto al remitente. Si solo hay un enlace en el pie, **no cumple**. El requisito es la cabecera (`List-Unsubscribe` + `List-Unsubscribe-Post`), no el enlace visual.
7. **Activar Google Postmaster Tools.** Es gratis y es el único lugar donde ves tu tasa de spam real según Gmail.

## 3.5 Calentamiento (warm-up) de dominio

Un dominio nuevo que envía 30.000 correos el día uno se marca como spam sin excepción. Programa de 4 semanas:

| Semana | Volumen diario | A quién |
|---|---|---|
| 1 | 200-500 | Solo compradores de los últimos 30 días |
| 2 | 500-2.000 | Compradores últimos 90 días + suscriptores últimos 30 días |
| 3 | 2.000-5.000 | Todos los que abrieron o clickearon en 90 días |
| 4 | 5.000-15.000 | Todos los activos de 180 días |

Los flujos automatizados son el mejor calentador: van a gente con intención alta y generan aperturas y clics reales.

## 3.6 Higiene de lista

- **Suprimir** (no borrar) a quien no abre ni clickea en 180 días, tras un intento de winback. Esto además baja la factura en Klaviyo y Mailchimp, que cobran por contacto.
- **Nunca reactivar** listas viejas sin re-permiso.
- **Rebotes duros:** eliminación automática. Verificar que la plataforma lo haga.
- **Tasa de rebote objetivo:** < 2%. Sobre 5% es una emergencia.

## Ejercicio 3
Configurar subdominio, SPF, DKIM y DMARC en `p=none`. Activar Postmaster Tools. Enviar correo de prueba a Gmail, Outlook y Yahoo, verificar el botón nativo de baja y revisar las cabeceras de autenticación (en Gmail: "Mostrar original").

**Entregable:** captura de pantalla de los tres registros DNS validados + Postmaster Tools activo.

---

# Módulo 4 — Los cinco flujos (núcleo del curso)

**Objetivo:** dejar cinco flujos funcionando. Este módulo es el 40% del valor del curso.

## 4.0 Por qué los flujos primero y las campañas después

Los datos son inequívocos. Sobre un análisis de más de 183.000 marcas:

| Métrica | Campañas programadas | Flujos automatizados | Top 10% de flujos |
|---|---|---|---|
| Apertura | 31,0% | 32,2% | 45,8% |
| Clic | 1,69% | **5,58%** | 10,48% |
| Tasa de pedido | 0,16% | **2,11%** | 4,30% |
| Ingreso por destinatario (RPR) | $0,32 | **$2,54** | $5,26 |

Los flujos representan **5,3% de los envíos y generan cerca del 41% de los ingresos por email**. El ingreso por destinatario es del orden de 18 veces el de una campaña. Además, casi el 48% de los ingresos generados por flujos viene de compradores nuevos, contra 16% en campañas: los flujos no solo retienen, adquieren.

**Consecuencia pedagógica:** un alumno que solo construye estos cinco flujos y nunca envía una campaña ya tiene un programa de email rentable. Las campañas vienen después.

---

## 4.1 FLUJO 1 — Bienvenida

**Disparador:** alta en la lista.
**Condición de salida:** compra realizada (sale del flujo y entra a post-compra).
**Benchmarks:** apertura ~41,9%, clic 5,5-6,1%, tasa de pedido 2,32%. Dato clave: **la tasa de clic-a-conversión es 58,26%** — más de la mitad de quienes clickean, compran. El primer email genera 40-50% del ingreso total del flujo.

**Estructura: 5 emails en 10 días**

| # | Timing | Objetivo | Contenido |
|---|---|---|---|
| 1 | 0-5 min | Entregar lo prometido | Código de descuento en grande. Confirmación de que está adentro. Un solo CTA: "Usar mi código". Nada de historia de marca todavía |
| 2 | +48 h | Por qué existimos | La historia real: qué problema resolvés, qué hacés distinto. Una foto de personas, no de producto. CTA suave a "conocer la marca" |
| 3 | +día 4 | Qué comprar | Los 3-5 más vendidos con reseñas visibles. Si etiquetaste el origen del alta, filtrar por categoría de interés |
| 4 | +día 6 | Derribar objeciones | Envíos (costo, plazo, cobertura), cambios y devoluciones, medios de pago y cuotas, garantía. En LatAm: aclarar si hay envío a regiones y cuánto demora realmente |
| 5 | +día 9 | Vencimiento | "Tu código vence en 24 h". Urgencia **real**: el código debe vencer de verdad |

**Ejemplos de asunto (email 1):**
- `Acá está tu 15% —` [30 caracteres, el valor entra completo en pantalla]
- `Listo. Tu código: BIENVENIDA15`
- `Tu descuento, sin vueltas`

**Copy del email 1 (esqueleto):**
```
Gracias por sumarte.

Tu código: BIENVENIDA15
15% en tu primera compra. Vence en 10 días.

[ VER PRODUCTOS ]   ← botón, ancho completo

Envío gratis sobre $XX.XXX. Cambios sin costo en 30 días.
```
Bajo 60 palabras. Un CTA. El descuento visible sin hacer scroll.

**Variante por origen (diferenciador de nivel intermedio):**
- Alta por popup con descuento → secuencia estándar de arriba.
- Alta en checkout sin comprar → saltar el email 1 (ya no hay descuento que entregar), empezar por el 4 (objeciones), porque la fricción fue del sitio, no del interés.
- Alta por "avisame cuando vuelva" → la bienvenida queda supeditada al aviso de stock.

---

## 4.2 FLUJO 2 — Carrito abandonado

El flujo de mayor retorno que existe.

**Contexto:** globalmente se abandona el 70,22% de los carritos (meta-análisis de 50 estudios de Baymard). Varía por dispositivo (78,74% en móvil contra 66,74% en escritorio), por rubro (84,61% en moda contra 50,03% en alimentos) y por región (73,25% en las Américas). Planificá asumiendo que 7 de cada 10 carritos no se convierten.

**Benchmarks:** apertura 50,5%, clic 6,25%, tasa de pedido 3,33%, RPR **$3,65** — el más alto de todos los flujos. El decil superior alcanza 65,34% de apertura, 13,33% de clic, 7,69% de pedidos y **$28,89 de RPR**.

**Distribución del ingreso dentro de la secuencia:** el primer email captura 45-55% del ingreso total del flujo; el segundo 25-30%; el tercero 15-20%. **Por eso el timing del primero es lo más importante del flujo entero.**

**Disparador:** producto agregado al carrito, sin compra.
**Condiciones de salida:** compra realizada; también se debe excluir a quien ya está en el flujo de checkout abandonado.

**Estructura: 3 emails en 72 horas**

| # | Timing | Ángulo | Contenido | Descuento |
|---|---|---|---|---|
| 1 | **1 hora** | Recordatorio | Bloque dinámico con el producto exacto: imagen, nombre, precio. "Te lo guardamos". Botón directo al carrito recuperado | **No** |
| 2 | **+24 h** | Objeciones + prueba social | Reseñas del producto abandonado, política de cambios, medios de pago y cuotas, costo de envío explícito. Responder al motivo real del abandono | **No** |
| 3 | **+72 h** | Incentivo | El mínimo viable: envío gratis o 10%. Escasez **real** de stock si existe. Fecha límite | **Sí** |

**Email 4 opcional (día 7):** solo para tickets altos (hardware, electrónica, muebles, joyería), donde el ciclo de decisión es más largo.

**Regla crítica que separa un programa amateur de uno profesional:** **no pongas descuento en el email 1.** Si el primer correo trae 15% off, entrenás a tu base a abandonar el carrito a propósito. Es un impuesto permanente sobre tu margen. Los datos lo sostienen: el email 1 ya captura casi la mitad del ingreso del flujo **sin** descuento.

**Asuntos por email:**
- E1: `¿Te quedó algo pendiente?` / `Tu carrito sigue acá` / `[Producto], todavía disponible`
- E2: `Lo que dicen quienes lo compraron` / `3 cosas antes de decidir`
- E3: `Envío gratis, hasta mañana` / `Última llamada por tu carrito`

**Motivos reales de abandono que hay que atacar en el email 2:** costos extra inesperados (envío, impuestos, cargos) es la causa principal a nivel global. En LatAm sumar: falta de claridad sobre cuotas sin interés, plazos de entrega a regiones, y desconfianza en el medio de pago. El email 2 debe responder a los tres.

**Distinción importante para el instructor:** *abandono de carrito* (agregó al carrito) y *abandono de checkout* (inició el proceso de pago) son flujos distintos. El de checkout tiene intención mucho más alta y convierte mejor. Si la plataforma lo permite, separalos: checkout a 30 minutos, carrito a 1 hora.

---

## 4.3 FLUJO 3 — Post-compra

El flujo más subutilizado. **Su métrica no es la conversión inmediata** (tasa de pedido promedio: 0,54%), es la tasa de recompra a 12 meses. RPR de referencia por banda de AOV: $0,24-$0,72 con ticket de $83-112; $0,29-$1,30 con ticket de $112-163.

**Disparador:** pedido confirmado.

**Estructura: 5 mensajes escalonados según el ciclo del producto**

| # | Timing | Tipo | Contenido |
|---|---|---|---|
| 0 | Inmediato | **Transaccional** | Confirmación de pedido. Datos, monto, plazo estimado. No es marketing: no lleva promoción ni requiere baja |
| 1 | +12-24 h | Reducir ansiedad | "Qué pasa ahora": el pedido está en preparación, se despacha el día X, llega entre X e Y. Cómo contactarnos. **Este correo baja tickets de soporte de forma medible** |
| 2 | Al despachar | Transaccional | Número de seguimiento, transportista, link de rastreo |
| 3 | +3-5 días post-entrega | Uso del producto | Cómo sacarle provecho: cuidados, combinaciones, tutorial. **Cero venta.** Genera afinidad y reduce devoluciones |
| 4 | +10-14 días post-entrega | Reseña | Pedido de reseña. Un clic para calificar. Incentivo opcional pequeño |
| 5 | Según ciclo de consumo | Cross-sell o reposición | Producto complementario, o recordatorio de reposición si es consumible |

**Cómo calcular el timing del email 5:** para consumibles, tomar la duración real del producto y disparar al 80% de ese plazo. Para durables, esperar 30-45 días y ofrecer complementarios. **No hagas cross-sell antes de que el producto llegue.** Vender de nuevo antes de cumplir la primera promesa es la forma más rápida de perder confianza.

**Segmentación mínima:** primera compra contra recompra. Al primer comprador se le explica la marca; al recurrente se le habla de novedades o de un programa de fidelidad.

---

## 4.4 FLUJO 4 — Winback / Recuperación

**Benchmarks:** apertura 30-35%, clic ~4,0%, tasa de pedido 0,9-1,4%. Tasa de baja esperada: 0,25-0,50%, muy por encima del resto — **y está bien**. Un winback es en parte una operación de higiene de lista: sirve para reactivar a unos y para identificar y retirar a los demás.

**Advertencia honesta que hay que dar en clase:** el winback es donde más programas fracasan. La mayoría lo deja corriendo de fondo sin oferta que realmente compense el motivo del abandono. O se construye en serio, o no se construye.

**Cómo definir el disparador (no es "6 meses" arbitrario):**

```
Ciclo de recompra mediano de tu tienda × 1,5 = umbral de inactividad
```

Si tus clientes recompran en promedio cada 60 días, el winback dispara a los 90. Si recompran cada 8 meses (rubro de muebles), disparar a los 12. Un umbral genérico de 6 meses es incorrecto para casi todos.

**Estructura: 4 emails en 30 días**

| # | Timing | Ángulo | Contenido | Incentivo |
|---|---|---|---|---|
| 1 | Día 0 | Sin oferta | "Volvimos con novedades": qué cambió, qué productos nuevos hay desde su última compra | Ninguno |
| 2 | +7 días | Oferta moderada | 10-15% o envío gratis. Recomendaciones basadas en lo que compró antes | Bajo |
| 3 | +14 días | Oferta fuerte + plazo | 20-25% con fecha de vencimiento. El mejor incentivo que tu margen tolere | Alto |
| 4 | +25 días | Preferencias / despedida | "¿Seguimos en contacto?" Opciones: recibir menos, cambiar de temas, o darse de baja. Botón de baja visible | Ninguno |

**Después del email 4:** si no hubo apertura ni clic, **suprimir**. No borrar (perdés el historial y podés reimportarlo por error), suprimir. Bajás la factura y protegés la reputación del dominio.

**Particularidad:** en winback, el email 3 o 4 suele superar a los anteriores, porque los más motivados ya reaccionaron y queda el segmento sensible a precio. Es el único flujo donde la degradación por posición no aplica.

---

## 4.5 FLUJO 5 — Browse abandonment (abandono de navegación)

**Benchmarks:** tasa de pedido 0,95%, clic-a-conversión ~15,9%. Es un flujo de **volumen**, no de RPR: la intención es más baja que en carrito, pero la población elegible es mucho mayor.

**Disparador (importa el detalle):** vio una ficha de producto **dos o más veces**, o permaneció más de 30-60 segundos, **y** no lo agregó al carrito, **y** no está en el flujo de carrito abandonado.

Un disparador mal calibrado (una sola vista, 5 segundos) genera correos irrelevantes que queman reputación. Este es el flujo donde más se equivoca el principiante.

**Estructura: 2 emails**

| # | Timing | Contenido |
|---|---|---|
| 1 | +2-4 h | El producto visto + **3 alternativas** de la misma categoría. Reseñas visibles. Tono informativo, no de venta |
| 2 | +24-48 h | Contenido de categoría: guía de compra, comparativa, "cómo elegir". Valor primero |

**Sin descuento, nunca.** Alguien que solo miró no ganó el derecho a un descuento, y ofrecérselo enseña a la base a esperar promociones por navegar.

**Frecuencia:** limitar a un ingreso al flujo cada 7 días por persona, o saturás.

---

## 4.6 Flujos adicionales (mencionar, construir después)

| Flujo | Cuándo agregarlo | Dato |
|---|---|---|
| **Back-in-stock** | Apenas tengas quiebres de stock | Apertura 59,19%, conversión 5,34%, clic-a-conversión 27,45%. **Es el flujo con mejor conversión que existe.** Solo requiere un botón "Avisame" en las fichas agotadas |
| Baja de precio | Con catálogo amplio | Alta intención, cero fricción |
| Reposición | Solo consumibles | Se solapa con post-compra E5 |
| Sunset | Cuando la lista supere ~10.000 | Suprime automáticamente al inactivo crónico |
| Aniversario / cumpleaños | Cuando captures la fecha | Bajo volumen, buena conversión |

**Referencia de madurez:** los programas en el percentil 90 corren entre 16 y 22 flujos activos. El curso deja 5 y explica cuáles son los siguientes 5.

## 4.7 Reglas de gobierno de flujos (evita el error más caro)

1. **Toda persona sale de un flujo al comprar.** Sin excepción. Recibir "¿te quedó algo pendiente?" después de haber pagado destruye la confianza.
2. **Prioridad entre flujos solapados:** Back-in-stock > Checkout abandonado > Carrito abandonado > Browse abandonment > Bienvenida > Campañas.
3. **Tope de frecuencia global:** máximo 1 email automatizado por día por persona, 5 por semana contando campañas.
4. **Suprimir de campañas a quien esté dentro de un flujo activo** de carrito o checkout durante esas 72 horas.

## Ejercicio 4
Construir los cinco flujos completos en la plataforma elegida. Activarlos con la lista real. Documentar disparadores, tiempos y condiciones de salida en una hoja.

**Entregable:** los cinco flujos activos + captura de pantalla del diagrama de cada uno.

---

# Módulo 5 — Copywriting: asuntos y cuerpos

**Objetivo:** escribir asuntos que se lean completos en móvil y cuerpos que lleven a un solo clic.

## 5.1 Benchmarks 2026 para calibrar expectativas

**Advertencia obligatoria antes de mostrar cualquier número de apertura:** Apple Mail Privacy Protection precarga los píxeles de seguimiento, generando aperturas que nunca ocurrieron. La inflación estimada va de 40% a 68% en usuarios de Apple Mail; hasta 75% de las aperturas registradas pueden ser automáticas. Las fuentes discrepan según metodología: Klaviyo reporta ~31% de apertura promedio en campañas de e-commerce, MailerLite ~32,7% (mediana), ActiveCampaign ~35,7%, y Brevo reporta 20,73% sin MPP contra 33,87% incluyéndola. **Las cuatro son "correctas": miden cosas distintas.** Esto se enseña como lección de alfabetización de datos, no se esconde.

**Campañas de e-commerce por categoría** (Klaviyo, 183.000+ marcas):

| Categoría | Apertura | Clic | Tasa de pedido |
|---|---|---|---|
| Ropa y accesorios | 33,1% | 1,83% | 0,12% |
| Salud y belleza | 30,5% | 1,24% | 0,19% |
| Joyería | 32,5% | 1,60% | 0,08% |
| Hogar y jardín | 32,5% | 1,78% | 0,13% |
| Alimentos y bebidas | 31,2% | 1,70% | **0,26%** |
| Deportes | 31,9% | 1,88% | 0,11% |
| Electrónica | 29,3% | 1,85% | 0,09% |
| Juguetes y hobbies | 31,7% | 2,03% | 0,19% |
| **Promedio** | **31,0%** | **1,69%** | **0,16%** |
| **Top 10%** | 45,1% | 3,38% | 0,36% |

Lectura: alimentos y bebidas lidera en pedidos (producto consumible, ciclo corto). Electrónica y joyería van último (ticket alto, decisión larga) — no significa que su email funcione peor, significa que el email cumple un rol de investigación y no de compra impulsiva. **Comparate contra tu categoría, nunca contra el promedio general.**

**Tasas de baja** — la señal de alerta temprana más confiable:

| Tipo | Promedio | Umbral de alarma |
|---|---|---|
| Campañas | 0,10-0,20% | > 0,30% |
| Flujos | 0,05-0,10% | > 0,20% |
| Bienvenida | 0,08% | > 0,15% |
| Carrito abandonado | 0,04% | > 0,10% |
| Winback | 0,25-0,50% | Esperado y aceptable |

## 5.2 Reglas de asunto

1. **30-50 caracteres, con el valor cargado en los primeros 30.** Es lo que entra en la vista vertical de iPhone Mail, que concentra más de la mitad de las aperturas de consumo. Un asunto largo no descalifica si el comienzo funciona truncado.
2. **Escribí "De:", asunto y preheader como una sola unidad.** Los tres se leen juntos en la bandeja. El preheader no es relleno: si lo ignorás, el cliente muestra "Ver este email en tu navegador". 40-130 caracteres.
3. **Personalización específica, no token de nombre.** "Hola {nombre}" ya no mueve nada. Lo que mueve es el detalle concreto: el producto que miró, la categoría que compra, la ciudad de envío.
4. **Bajá la urgencia artificial.** "ÚLTIMA OPORTUNIDAD" en mayúsculas activa filtros y erosiona confianza. Las mayúsculas sostenidas se asocian con caídas fuertes de apertura y con activación de filtros de spam.
5. **Emoji: uno o ninguno, nunca dos.** Los datos son mixtos: en B2C de mercado medio la adopción ronda el 42% con efecto variable; hay datasets donde el emoji baja apertura pero sube clic. Es un candidato a test, no una regla.
6. **Los números ya no son magia.** Datos de 2021 mostraban +45% de apertura con números; datasets de 2024-2026 muestran efecto neutro o levemente negativo. Las tácticas se degradan cuando se masifican. Enseñá el principio, no el truco.
7. **Probá siempre.** Es la única regla no negociable. Testeá largo vs. corto, con emoji vs. sin, título vs. minúscula, específico vs. amplio. Una variable por vez.

**Ejercicio de calibración en clase:** que cada alumno escriba 10 asuntos y los mida con un contador de caracteres. La mayoría descubre que sus asuntos habituales tienen 70-90 caracteres y se cortan a la mitad en móvil.

## 5.3 Estructura de cuerpo que convierte

```
[Preheader: 40-130 caracteres, complementa el asunto, no lo repite]

[Logo pequeño]

TITULAR: 6-9 palabras, la promesa completa

Una o dos líneas de contexto. Máximo 25 palabras.

[ BOTÓN — ancho completo, verbo en primera persona ]

[Imagen de producto o prueba social]

Segundo bloque: objeción o beneficio. 30 palabras.

[ MISMO BOTÓN, mismo texto ]

[Pie: dirección física, motivo del envío, baja]
```

**Reglas de cuerpo:**
- **Un objetivo por email.** Si el email hace tres cosas, no hace ninguna.
- **El mismo CTA repetido**, no tres CTAs distintos.
- **Texto del botón en primera persona:** "Ver mi carrito" rinde mejor que "Ver carrito".
- **La promesa del asunto debe cumplirse en las primeras dos líneas.** El desajuste entre asunto y contenido es la causa más común de clic bajo con apertura alta.
- **Nada crítico dentro de una imagen.** Muchos clientes bloquean imágenes por defecto; si tu descuento está dentro del JPG, no existe.

## 5.4 Adaptación a LatAm (sección propia, no un apéndice)

- **No traduzcas plantillas del inglés.** "Shop now" traducido a "Compra ahora" suena a importación. "Ver productos", "Quiero el mío", "Ir al carrito" suenan locales.
- **Voseo vs. tuteo:** decidilo por mercado principal y mantenelo. Argentina/Uruguay: voseo. México/Colombia/Chile/Perú: tuteo. Mezclarlos delata plantilla.
- **Moneda y formato numérico:** mostrar la moneda local con separadores correctos. `$45.990` en Chile no es `$45,990`. Un error de formato cuesta credibilidad instantánea.
- **Cuotas.** En buena parte de LatAm, "3 cuotas sin interés" es un argumento de conversión más fuerte que un 10% de descuento. Debe estar en el email 2 del carrito abandonado.
- **Envío a regiones.** Explicitar plazo y costo fuera de la capital. Es un motivo de abandono enorme y poco atendido.
- **Fechas comerciales locales:** Hot Sale (México, mayo; Argentina, mayo), CyberMonday Chile (octubre), Buen Fin (México, noviembre), Black Friday (adopción creciente en toda la región), Día de la Madre (fechas distintas por país). El calendario comercial de EE.UU. no aplica.

## Ejercicio 5
Escribir 30 asuntos (6 por cada uno de los 5 flujos), medirlos en caracteres, y redactar los 5 cuerpos del flujo de bienvenida.

---

# Módulo 6 — Segmentación y RFM

**Objetivo:** dejar de enviar lo mismo a todos.

## 6.1 Los tres niveles de segmentación

**Nivel 1 — Por engagement (obligatorio, tarda 10 minutos, protege la entregabilidad):**

| Segmento | Definición | Uso |
|---|---|---|
| Activos | Abrió o clickeó en 90 días | Envío normal |
| Semi-activos | Abrió o clickeó entre 90-180 días | Frecuencia reducida |
| Inactivos | Sin actividad en 180+ días | Solo winback, luego supresión |

Si el alumno solo implementa esto, ya protegió su reputación de dominio. Es la palanca de mayor relación resultado/esfuerzo del módulo.

**Nivel 2 — Por comportamiento:** compradores primerizos vs. recurrentes; categoría comprada; rango de ticket; origen del alta.

**Nivel 3 — RFM.**

## 6.2 RFM explicado desde cero

RFM puntúa a cada cliente en tres ejes:

- **R (Recencia)** — días desde la última compra. Menos es mejor.
- **F (Frecuencia)** — cantidad de compras en el período analizado. Más es mejor.
- **M (Monto)** — valor total gastado. Más es mejor.

**Método práctico para una tienda chica (planilla, sin herramientas):**

1. Exportar de la tienda: `email, fecha_última_compra, cantidad_compras, monto_total` para los últimos 24 meses.
2. Ordenar por cada columna y dividir en 5 grupos iguales (quintiles). Asignar puntaje 1-5.
   - Recencia: el quintil más reciente recibe 5.
   - Frecuencia y Monto: el quintil más alto recibe 5.
3. Cada cliente queda con tres dígitos, por ejemplo `5-4-5`.

**Versión simplificada para listas bajo 1.000 clientes:** usar 3 niveles en vez de 5 (alto/medio/bajo). Con pocos datos, los quintiles producen grupos sin significado estadístico. Este ajuste importa para el público del curso.

## 6.3 Los seis segmentos accionables

| Segmento | Puntaje R-F-M | % típico de la base | Qué hacer |
|---|---|---|---|
| **Campeones** | 5-5-5, 5-4-5 | 5-10% | Acceso anticipado, no descuentos. Ya compran. Pedirles reseñas y referidos |
| **Leales** | 4-4-4 a 5-3-4 | 10-15% | Cross-sell, programa de fidelidad, contenido |
| **Potenciales** | 5-1-x, 4-2-x | 15-20% | Compraron hace poco pero poco. Empujar a la 2ª compra: es el punto de mayor apalancamiento del LTV |
| **En riesgo** | 2-4-4, 2-5-5 | 10-15% | Compraban mucho y pararon. **Máxima prioridad de winback.** Oferta agresiva justificada |
| **Hibernando** | 1-2-2 a 2-2-3 | 20-30% | Winback estándar, luego supresión |
| **Perdidos** | 1-1-1 | 20-30% | Un intento y suprimir. No gastes reputación |

**La observación que más cambia el negocio:** el segmento "Potenciales" (compró una vez, hace poco) es donde está el mayor retorno. Llevar a alguien de 1 a 2 compras es sustancialmente más barato que adquirir un cliente nuevo, y cambia la curva de LTV de toda la cohorte. La mayoría de las tiendas no tiene ninguna comunicación dedicada a ese grupo.

## 6.4 Consulta SQL de referencia (para alumnos técnicos, opcional)

```sql
WITH base AS (
  SELECT
    email,
    DATE_DIFF(CURRENT_DATE(), MAX(fecha_pedido), DAY) AS recencia,
    COUNT(DISTINCT id_pedido)                          AS frecuencia,
    SUM(total_pedido)                                  AS monto
  FROM pedidos
  WHERE fecha_pedido >= DATE_SUB(CURRENT_DATE(), INTERVAL 24 MONTH)
  GROUP BY email
)
SELECT
  email, recencia, frecuencia, monto,
  6 - NTILE(5) OVER (ORDER BY recencia ASC)  AS r,  -- menor recencia = 5
  NTILE(5) OVER (ORDER BY frecuencia ASC)    AS f,
  NTILE(5) OVER (ORDER BY monto ASC)         AS m
FROM base;
```

**Nota para el instructor:** presentarlo como opcional. La versión en planilla cubre al 90% del público del curso y no debe quedar en segundo plano.

## Ejercicio 6
Exportar los pedidos, construir la tabla RFM, definir los seis segmentos y crearlos en la plataforma. Escribir una frase por segmento describiendo qué mensaje recibe.

---

# Módulo 7 — Diseño móvil que convierte

**Objetivo:** que el email funcione en la pantalla donde se lee.

## 7.1 Especificaciones técnicas

Más del 60% de los emails se abren en móvil. El diseño es móvil primero, no "responsive como agregado".

| Elemento | Especificación |
|---|---|
| Ancho | 600 px (máximo 640) |
| Estructura | **Una sola columna**, siempre |
| Cuerpo de texto | Mínimo 16 px |
| Titulares | 24-32 px |
| Botón CTA | Mínimo 44 × 44 px de área táctil; ancho completo en móvil |
| Peso del HTML | Bajo 100 KB (sobre 102 KB Gmail recorta el email) |
| Imágenes | Bajo 200 KB cada una |
| Texto alternativo | En todas las imágenes |
| Preheader | 40-130 caracteres |

**Por qué una sola columna:** los diseños de dos columnas colapsan de forma impredecible. Las barras laterales quedan abajo donde nadie llega; las grillas de dos productos se achican a tamaño ilegible. Una columna hace el orden de lectura obvio y evita alineaciones rotas en Gmail y Outlook.

## 7.2 Modo oscuro

No es un caso borde. Y son tres problemas distintos: Apple Mail invierte agresivamente, Outlook de escritorio casi no cambia nada, Gmail invierte parcialmente y solo algunas paletas.

- Logos en PNG con fondo transparente y contorno visible en ambos contextos, con 20-30 px de relleno.
- Texto vivo con alto contraste. Nada de gris claro sobre blanco.
- No depender de un solo color de marca para que el CTA se distinga.
- Probar en modo claro y oscuro antes de cada envío.

## 7.3 Checklist previo a cada envío (imprimible, 2 minutos)

```
[ ] ¿El botón se ve sin hacer scroll en móvil?
[ ] ¿El email es de una sola columna?
[ ] ¿El texto del cuerpo está en 16 px o más?
[ ] ¿Todas las imágenes pesan menos de 200 KB?
[ ] ¿Todas las imágenes tienen texto alternativo?
[ ] ¿El HTML total está bajo 100 KB?
[ ] ¿El preheader está escrito (no vacío, no "Ver en navegador")?
[ ] ¿Probé en un teléfono real, no solo en la previsualización?
[ ] ¿Revisé el renderizado en modo oscuro?
[ ] ¿El descuento/oferta está en texto, no dentro de una imagen?
[ ] ¿El enlace de baja funciona?
[ ] ¿Los enlaces tienen etiquetas UTM?
```

## Ejercicio 7
Construir la plantilla base propia con estas especificaciones. Enviarla a tres teléfonos distintos (iPhone, Android, y una cuenta de Outlook) y corregir lo que se rompa.

---

# Módulo 8 — Métricas: cuáles importan y cuáles ignorar

**Objetivo:** que el alumno mida el negocio, no el email.

## 8.1 Las cuatro métricas del tablero

| Métrica | Fórmula | Por qué importa |
|---|---|---|
| **RPR — Ingreso por destinatario** | Ingreso atribuido ÷ emails entregados | Le pone precio a cada envío. Es la métrica que correlaciona con resultados de negocio |
| **Tasa de pedido** | Pedidos ÷ emails entregados | Mide conversión real, no interés |
| **Tasa de clic** | Clics únicos ÷ entregados | La mejor señal de engagement disponible, no afectada por MPP |
| **% de ingresos totales que viene del email** | Ingreso email ÷ ingreso total | El número que le importa al dueño del negocio |

**Referencias:** para el % de ingresos, si el programa de email no aporta al menos 20-30% del ingreso total, hay margen de mejora. Los programas en el percentil 90 llegan a 38-45% contando email + SMS/WhatsApp, con 58-65% de ese ingreso proveniente de flujos.

## 8.2 Métricas de salud (revisar mensual, no optimizar)

| Métrica | Objetivo | Alarma |
|---|---|---|
| Tasa de spam (Postmaster Tools) | < 0,10% | > 0,30% |
| Rebote duro | < 1% | > 2% |
| Baja en campañas | < 0,20% | > 0,30% |
| Crecimiento neto de lista | Positivo | Negativo 2 meses seguidos |

## 8.3 Qué ignorar (sección explícita del curso)

**1. La tasa de apertura como KPI.** Rota por MPP. Sirve para una sola cosa: detectar caídas bruscas, que indican problema de entregabilidad, no de asunto. Una apertura sostenidamente bajo 20% señala problema de bandeja, no de copywriting.

**2. "El email tiene ROI de 42:1".** Es una cifra promocional que circula desde hace años, calculada sobre cohortes no comparables. Enseñá al alumno a calcular **su** ROI: `(ingreso atribuido − costo de plataforma − horas × tarifa) ÷ costo total`.

**3. La tasa de entrega.** Siempre da ~99% porque solo mide que el servidor aceptó el correo. No dice nada sobre si llegó a bandeja de entrada o a spam. Es el número más engañoso del panel.

**4. El tamaño de la lista.** 50.000 contactos con 8% de actividad valen menos que 6.000 con 45%, y cuestan más en Klaviyo y Mailchimp.

**5. Comparar tu apertura con el promedio general de la industria.** Compará contra tu categoría y, sobre todo, contra tu propio mes anterior.

## 8.4 Diagnóstico por síntoma

| Síntoma | Causa probable | Acción |
|---|---|---|
| Apertura < 20% sostenida | Entregabilidad, no asunto | Revisar autenticación, limpiar lista, revisar tasa de spam |
| Apertura normal, clic < 1% (campañas) o < 3% (flujos) | Desajuste entre asunto y contenido | Testear asuntos, revisar jerarquía visual, segmentar mejor |
| Clic bueno, pedidos bajos | El problema está en el sitio, no en el email | Revisar ficha de producto, checkout, costos de envío, medios de pago |
| Bajas en aumento | Frecuencia o relevancia | Reducir cadencia, segmentar por engagement |
| Tasa de spam subiendo | Origen de lista o falta de baja visible | Auditar fuentes de alta, revisar botón nativo de baja |

## 8.5 Modelo económico de ejemplo (ejercicio con números)

**Tienda de referencia:** 8.000 contactos activos, AOV USD 60, 1.000 carritos creados por mes, 400 altas nuevas por mes, 4 campañas mensuales.

*Carrito abandonado:*
```
1.000 carritos × 70% abandono            = 700 abandonados
700 × ~60% con email capturado           = 420 destinatarios/mes
420 × RPR $3,65 (promedio)               = ~$1.533/mes
420 × RPR $28,89 (decil superior)        = ~$12.134/mes  ← el rango es la lección
```

*Bienvenida:*
```
400 altas/mes × RPR $0,35 (p25)          = $140/mes
400 altas/mes × RPR $2,53 (p75)          = $1.012/mes
```

*Campañas:*
```
8.000 × 4 envíos = 32.000 entregas
32.000 × RPR $0,32 (promedio)            = ~$10.240/mes
```

*Costo de plataforma a 8.000 contactos:* Brevo ~$29 (32.000 envíos) · Mailchimp ~$95 · Klaviyo ~$130 · ActiveCampaign ~$135.

**Conclusión del ejercicio:** el flujo de carrito abandonado solo, en su versión promedio, paga la plataforma 10 a 50 veces. **Y la diferencia entre el promedio y el decil superior es de casi 8×** con la misma lista y el mismo tráfico. Esa diferencia es arquitectura y ejecución, no volumen.

**Advertencia metodológica obligatoria:** estos RPR vienen de datasets mayoritariamente estadounidenses con AOV en dólares. Un alumno con AOV de USD 25 debe escalar proporcionalmente. El ejercicio real es que cada uno calcule su propio RPR después de 60 días de datos. Los benchmarks sirven para saber si estás en el orden de magnitud correcto, no para fijar metas.

## Ejercicio 8
Construir el tablero de 4 métricas. Registrar el baseline propio. Repetir la medición a los 30 y 60 días.

---

# Módulo 9 — IA aplicada: dónde sirve y dónde estorba

**Objetivo:** usar IA donde da retorno y no donde produce ruido genérico.

## 9.1 Dónde la IA rinde de verdad (ordenado por retorno)

**1. Optimización de horario de envío (send-time optimization).** La función más segura de activar: en el peor caso envía a una hora normal. Los rangos reportados van de 5-15% a 20-30% de mejora en apertura según fuente y baseline. Requiere ~90 días de historial de interacción por suscriptor.

**Advertencia técnica importante:** MPP rompió los modelos de horario basados en aperturas, porque genera aperturas automáticas en el momento de la entrega. Verificá que tu plataforma optimice sobre **clics y conversiones**, no sobre aperturas. Klaviyo hizo ese cambio; no todas lo hicieron. Si tu plataforma sigue optimizando sobre aperturas, estás optimizando ruido.

**2. Segmentación predictiva.** Agrupa por lo que la persona *va a hacer*, no por lo que hizo. Mejoras reportadas de 10-25% en conversión, hasta 30-50% frente a segmentos demográficos planos. **Requiere 3 a 6 meses de datos de comportamiento y al menos ~5.000 suscriptores.** Por debajo de eso las predicciones no son confiables — dato relevante para el público del curso, donde muchos no alcanzan el umbral.

**3. Generación de variantes de asunto para testear.** La IA puede producir 40 variantes y puntuarlas antes de enviar. Es fuerza bruta que ningún equipo humano replica. Las pruebas multivariadas (5-10 variantes evaluando tono, largo, tokens y emoji) identifican al ganador con más precisión que un A/B simple.

**4. Recomendaciones de producto.** Las recomendaciones generadas por IA elevan el clic promedio a ~3,75% (y ~8,79% en el decil superior), con RPR materialmente mayor.

## 9.2 Dónde la IA no sirve

**Escribir el email final.** El borrador sale limpio y genérico. Sirve para primeras pasadas, variantes de asunto o descripciones de catálogo de bajo riesgo. Falla en los emails que pesan: un lanzamiento, una disculpa, cualquier cosa que deba sonar a tu marca y no a las otras mil marcas que usan el mismo modelo. **Tratala como un borrador rápido que reescribís, no como un email terminado.**

**Estrategia.** Qué flujos construir, qué margen sacrificar, qué frecuencia tolerar. Eso lo decide una persona con el negocio en la cabeza.

**Arrancar de cero.** Ningún modelo predictivo funciona sin datos. En cold start, la IA es un adorno.

## 9.3 El punto que casi nadie enseña

**La calidad de tus datos de primera parte es el techo del rendimiento de la IA.** Toda función —personalización, segmentación, horario, predicción de abandono— corre sobre tus datos. Los programas con datos ricos, precisos y actualizados ven varias veces más beneficio que los programas con datos escasos o viejos. Antes de activar funciones de IA, invertí en captura de datos limpia.

**Riesgo operativo:** no le des a un agente de IA autoridad de envío sin restricción. Un agente sobre-permisionado que envía a toda la lista sin aprobación es el patrón de falla principal de esta categoría. Aprobación humana antes de cada envío masivo, sin excepción.

## 9.4 Biblioteca de prompts (entregable del módulo)

```
ASUNTOS
"Sos copywriter de e-commerce. Marca: [descripción, 2 líneas].
Producto: [X]. Público: [Y]. Escribí 15 asuntos para el email
[N] del flujo de [carrito abandonado / bienvenida / ...].
Restricciones: máximo 45 caracteres; el valor debe entrar en los
primeros 30; español de [país]; sin mayúsculas sostenidas; sin
urgencia falsa. Marcá cuáles usan emoji."

OBJECIONES (email 2 de carrito)
"Estas son las 5 preguntas más frecuentes de nuestros clientes:
[pegar]. Escribí un email que las responda en menos de 120
palabras, con un solo CTA, tono [X]."

DIAGNÓSTICO
"Estos son mis datos del último mes: [pegar apertura, clic, tasa
de pedido, baja, spam, por flujo]. Comparalos con los benchmarks
de e-commerce 2026 e identificá los 3 problemas más graves en
orden de impacto en ingresos. No propongas más de 3."
```

**Política de revisión que el alumno debe escribir y firmar:** ningún email generado por IA se envía sin (a) verificación de datos concretos —precios, plazos, stock—, (b) lectura en voz alta para detectar tono genérico, (c) revisión del CTA.

## Ejercicio 9
Activar optimización de horario de envío. Generar 15 variantes de asunto con IA, elegir 3, testearlas. Escribir la política de revisión.

---

# Módulo 10 — Errores comunes y auditoría final

## 10.1 Los 16 errores, ordenados por costo

**Costo catastrófico (destruyen el programa):**

1. **Comprar o importar listas sin consentimiento.** Quema el dominio en semanas y arrastra a la parte legítima de la lista. En Chile, desde el 1 de diciembre de 2026, además es sancionable.
2. **No configurar SPF, DKIM y DMARC.** La colocación cae de ~89% a ~44%. Con la aplicación actual de Google, Yahoo y Microsoft, no es que vayas a spam: te rechazan.
3. **Enviar desde el dominio raíz sin subdominio.** Un mal mes de marketing contamina tu correo transaccional y corporativo.
4. **Enviar 30.000 correos el primer día.** Sin calentamiento, marcado como spam sin apelación.

**Costo alto (dejan dinero grande sobre la mesa):**

5. **Empezar por campañas antes que por flujos.** Los flujos son 5,3% de los envíos y ~41% del ingreso.
6. **Un solo email de carrito abandonado.** Perdés el 45-55% del ingreso del flujo que aportan los emails 2 y 3.
7. **Descuento en el email 1 del carrito.** Entrena a la base a abandonar a propósito. Impuesto permanente sobre el margen.
8. **No excluir a quien compró.** Recibir "¿te quedó algo pendiente?" después de pagar destruye confianza.
9. **Nunca segmentar por engagement.** Enviar a inactivos hunde la reputación y perjudica a los activos.
10. **No pedir reseñas en post-compra.** La prueba social es insumo de todos los demás emails.

**Costo medio (erosionan resultados):**

11. **Medir por tasa de apertura.** Optimizás una métrica rota por MPP.
12. **Email de una sola imagen grande.** Si se bloquean imágenes, el correo queda en blanco; además dispara filtros.
13. **Traducir plantillas del inglés literalmente.** Suena importado, y el formato de moneda mal puesto delata amateurismo.
14. **No limpiar la lista.** Pagás por contactos muertos en Klaviyo y Mailchimp, y perjudicás la entregabilidad.
15. **Frecuencia sin criterio** (todo o nada). Ni 1 email cada dos meses ni 5 por semana a toda la base.
16. **Flujos solapados sin reglas de prioridad.** La persona recibe tres correos automáticos el mismo día y se da de baja.

## 10.2 Auditoría final (rúbrica de evaluación del curso)

| Área | Criterio | Puntos |
|---|---|---|
| Autenticación | SPF, DKIM y DMARC publicados y validados; subdominio en uso; Postmaster Tools activo | 20 |
| Flujos | Los 5 flujos activos, con timing correcto y condiciones de salida configuradas | 30 |
| Consentimiento | Formulario con opt-in explícito, evidencia guardada, baja en un clic verificada en Gmail | 15 |
| Segmentación | Segmentos de engagement + tabla RFM con 6 segmentos accionables | 10 |
| Diseño | Plantilla propia que pasa el checklist de 12 puntos en 3 dispositivos | 10 |
| Métricas | Tablero de 4 métricas con baseline propio registrado | 15 |

**Aprobación:** 70/100. **Con distinción:** 90/100 y evidencia de al menos un test A/B completado con resultado documentado.

---

# Anexos

## A1 — Calendario sugerido de dictado (8 semanas)

| Semana | Módulos | Foco |
|---|---|---|
| 1 | 0 + 1 | Contexto y elección de plataforma |
| 2 | 2 + 3 | Captura, ley y autenticación (semana técnica) |
| 3 | 4 (parte 1) | Bienvenida y carrito abandonado |
| 4 | 4 (parte 2) | Post-compra, winback, browse |
| 5 | 5 | Copywriting + taller de asuntos en vivo |
| 6 | 6 + 7 | RFM y diseño móvil |
| 7 | 8 + 9 | Métricas e IA |
| 8 | 10 | Auditoría cruzada entre alumnos + revisión |

**Versión intensiva (2 días, 16 h):** día 1 = módulos 0-4; día 2 = módulos 5-10. Se sacrifica la práctica; los flujos quedan construidos pero sin datos para medir.

## A2 — Stack de herramientas gratuitas del curso

| Herramienta | Uso |
|---|---|
| Google Postmaster Tools | Tasa de spam real según Gmail. Imprescindible |
| MXToolbox / dmarcian | Verificar registros SPF, DKIM, DMARC |
| Mail-tester.com | Puntaje de spam previo al envío |
| Litmus / Email on Acid | Previsualización multi-cliente (versión de prueba) |
| Constructor de UTM de Google | Etiquetado de enlaces |
| GA4 | Atribución del tráfico de email |

## A3 — Biblioteca de asuntos por flujo (arranque para el alumno)

**Bienvenida**
```
Acá está tu 15%
Listo, ya estás adentro
Tu código: BIENVENIDA15
Lo prometido: 15% off
Bienvenido. Empezá por acá
```

**Carrito abandonado — email 1**
```
¿Te quedó algo pendiente?
Tu carrito sigue acá
[Producto], todavía disponible
Te lo guardamos
Volvé a tu carrito
```

**Carrito abandonado — email 3**
```
Envío gratis, hasta mañana
Última llamada por tu carrito
Tu carrito vence hoy
```

**Post-compra**
```
Tu pedido está en camino
Cómo cuidar tu [producto]
¿Cómo te fue con tu compra?
Una pregunta rápida
```

**Winback**
```
Pasaron cosas desde tu última visita
¿Volvemos a vernos?
Esto es nuevo desde que no venís
Última oferta antes de despedirnos
```

**Browse abandonment**
```
¿Seguís pensando en [producto]?
Tres opciones parecidas a la que viste
Lo que otros eligieron en [categoría]
```

## A4 — Fuentes

Verificadas entre enero y agosto de 2026. Re-verificar precios y requisitos antes de cada cohorte.

**Benchmarks**
- Klaviyo, 2026 Email Marketing Benchmarks (183.000+ marcas) — klaviyo.com/products/email-marketing/benchmarks
- Klaviyo, Abandoned Cart Benchmark Report — klaviyo.com/blog/abandoned-cart-benchmarks
- Brevo, 2026 Marketing Orchestration Benchmark — brevo.com/blog/email-marketing-benchmarks
- MailerLite, Email marketing benchmarks by industry and region (3,6 M campañas)
- Omnisend, Ecommerce Marketing Report
- Baymard Institute, meta-análisis de abandono de carrito (50 estudios)

**Entregabilidad**
- Google Email Sender Guidelines (requisitos para remitentes masivos)
- Microsoft, requisitos para Outlook.com/Hotmail/Live (abril 2025, vigencia mayo 2025)
- PowerDMARC, Bulk Email Sender Requirements — powerdmarc.com/bulk-email-sender-requirements

**Precios de plataformas**
- Páginas oficiales de precios de Klaviyo, Mailchimp, Brevo y ActiveCampaign
- PriceTimeline, historial de cambios de precio de Mailchimp
- EmailToolTester, registro de cambios de planes

**Legal**
- Ley 21.719 (Chile), publicada 13/12/2024, vigencia plena 01/12/2026
- LGPD (Brasil), LFPDPPP (México)

**LatAm**
- We Are Social / Meltwater / DataReportal, Digital Report 2026
- Blip, Infobip: estadísticas de WhatsApp Business en LatAm

---

*Documento de diseño de curso. Los precios de plataformas y los umbrales de proveedores de correo cambian con frecuencia; el módulo 1 está diseñado para que el propio alumno los verifique, de modo que el curso no dependa de datos que caducan.*
