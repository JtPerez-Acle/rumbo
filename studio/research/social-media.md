# Gestión de redes sociales y comunidad en agencia: documento fuente autoritativo para LatAm

**Fecha de cierre editorial:** 12 de agosto de 2026  
**Fecha de consulta de especificaciones de plataforma:** 12 de agosto de 2026  
**Ámbito:** gestión orgánica de Instagram, Facebook, TikTok, YouTube y LinkedIn con herramientas nativas y gratuitas, más una planilla de cálculo.  
**Herramientas operativas permitidas:** Meta Business Suite, Instagram/Facebook Insights, TikTok Creator Center/TikTok Analytics, YouTube Studio, LinkedIn Analytics y una planilla. Meta define Business Suite como una herramienta gratuita que reúne administración, programación, mensajería e insights para Facebook e Instagram. citeturn21search1turn21search6

## Marco editorial, evidencia y arquitectura del curso

Este documento parte de una distinción que debe atravesar las treinta lecciones: **una plataforma de redes sociales no tiene “un algoritmo” único ni una fórmula secreta que el social media manager deba descifrar**. Tiene múltiples sistemas de selección, elegibilidad, recuperación, ranking y recomendación, distintos según superficie, formato, usuario y contexto. Meta documenta sistemas diferentes para Feed, Stories, Reels y recomendaciones de cuentas que una persona no sigue; YouTube diferencia Home, Up Next, Search, Shorts y otras superficies; TikTok personaliza individualmente For You; y LinkedIn describió en 2026 un sistema de recuperación y ranking de Feed basado en modelos generativos y señales profesionales y de interacción. citeturn25search1turn24search0turn23search11turn9view0

Por eso, el trabajo profesional no consiste en “hackear” plataformas. Consiste en alinear **objetivo de negocio → objetivo de canal → audiencia → propuesta editorial → formato → distribución → comunidad → métrica → aprendizaje**.

**Código de evidencia obligatorio del curso.**

| Código | Qué significa | Cómo se utiliza |
|---|---|---|
| **[P]** | Documentación oficial de plataforma, changelog o declaración pública de producto/empresa; también investigación con método publicado y replicable. | Base para explicar funcionalidades, sistemas de recomendación y principios que sí pueden enseñarse como conocimiento respaldado. |
| **[V]** | Estudio, benchmark o verificación producida por una herramienta, agencia o proveedor. | Puede orientar hipótesis o especificaciones cuando la fuente primaria no sea accesible, pero debe declararse quién lo publica/financia y nunca convertirse en una “ley del algoritmo”. |
| **[X]** | Afirmación del tipo “el algoritmo premia X” sin respaldo suficiente. | Se descarta. Puede aparecer únicamente como mito para enseñar a detectarlo. |

Para estudios de casos históricos se utiliza además la etiqueta **HC — hemeroteca de caso**. No eleva una noticia o análisis periodístico a categoría [P]: solo verifica qué ocurrió. Ningún caso de marca se utiliza para inferir una regla algorítmica universal.

El principio editorial es especialmente importante porque las propias plataformas cambian. Por ejemplo, desde el 16 de diciembre de 2025 Meta incorporó las interacciones con sus funciones de IA como una señal adicional para personalizar contenido y anuncios en las regiones donde la actualización se desplegó. En marzo de 2026 Meta explicitó además que en Facebook prioriza contenido original y reduce distribución de duplicaciones o transformaciones de bajo valor. LinkedIn, por su parte, describió en marzo de 2026 una nueva generación de ranking de Feed basada en modelos generativos y LLM. citeturn25search3turn25search4turn9view0

**Stack operativo del curso.** No se enseña ninguna interfaz de Sprout Social, Hootsuite, Later, Metricool de pago ni plataforma equivalente. Una suite pagada puede resolver, a escala, permisos multiusuario, flujos de aprobación, calendario multicuenta, versionado, inbox unificado, asignación de casos, SLA, etiquetado y exportaciones centralizadas. Sin ella, la arquitectura equivalente es:

**Planilla maestra + carpeta de activos + RACI + herramientas nativas de publicación + herramientas nativas de analítica + registro de comunidad/crisis.**

TikTok ofrece desde su entorno Creator Center/Creator Studio funciones de publicación o programación, gestión de contenido y comentarios y analítica nativa; YouTube concentra analítica y publicación en Studio; y Meta Business Suite ofrece programación, inbox e insights para Facebook e Instagram. citeturn23search0turn21search1

**Mapa completo de las treinta lecciones.**

| Bloque | Lecciones | Producto final del bloque |
|---|---|---|
| Estrategia de canal | Auditoría; función de plataformas; selección; objetivos; arquetipo y tono; documento de estrategia | Estrategia de canales defendible |
| Parrilla y producción | Pilares; matriz; cadencia; formatos; adaptación; aprobación | Parrilla mensual aprobable y sistema de producción |
| Algoritmos y distribución | Modelo mental; Meta; TikTok; YouTube; LinkedIn; analítica y mitos | Diagnóstico de distribución basado en evidencia |
| Comunidad y crisis | Política; taxonomía; escalamiento; comunidad; detección; war room/postmortem | Política de moderación y protocolo de crisis |
| Medición y reportería | Framework; higiene métrica; reporte; tendencias; defensa ante cliente; mejora continua | Reporte mensual completo y plan de optimización |

Un alumno puede entrar directamente a cualquier bloque porque cada módulo declara sus prerrequisitos reales y produce un artefacto independiente. Las tareas, sin embargo, están diseñadas para encadenarse sobre **una misma marca real**, escogida por el alumno al comenzar.

## Bloque: estrategia de canal

**Modularidad.**

| Elemento | Definición |
|---|---|
| **Prerrequisitos reales** | Poder identificar qué vende o qué propósito cumple una marca, a quién necesita influir y qué recursos tiene para producir contenido. No requiere haber cursado otro bloque. |
| **Resultado si solo se cursa este bloque** | El alumno puede decidir racionalmente dónde debe estar una marca, qué papel cumple cada canal, qué no debe pedirle y qué objetivos y tono asignarle. |
| **Conexión con influencer marketing** | Define en qué contexto una colaboración tiene sentido y qué rol debe cumplir el creador. |
| **Conexión con analítica** | Convierte objetivos abstractos en señales observables. |
| **Conexión con paid media** | Distingue el trabajo que debe resolver contenido orgánico del que requiere distribución comprada. |
| **Conexión con contenidos** | Entrega el brief estratégico que alimentará pilares, formatos, guiones y parrilla. |

**Lección 1 — Auditoría antes de estrategia.** El alumno elige su marca real. La primera regla de agencia es **no confundir presencia con estrategia**: encontrar una cuenta activa no prueba que el canal sea necesario.

La auditoría comienza con una planilla de una fila por canal:

| Campo | Pregunta |
|---|---|
| Objetivo aparente | ¿Para qué parece existir esta cuenta? |
| Audiencia observable | ¿Con quién conversa? |
| Propuesta editorial | ¿Qué recibiría alguien por seguirla? |
| Formatos dominantes | ¿Qué produce de verdad? |
| Frecuencia real | ¿Cuál es la mediana de publicaciones de los últimos meses? |
| Señales de distribución | ¿Qué piezas llegan más allá de la base habitual? |
| Señales de comunidad | ¿Hay respuestas, preguntas repetidas, defensores, críticas? |
| Acción deseada | ¿Qué debería hacer una persona después del contenido? |
| Recursos requeridos | ¿Video, diseño, vocería, expertos, atención al cliente? |
| Decisión preliminar | Mantener, redefinir, reducir o abandonar |

No se evalúa una cuenta por sus seguidores aislados. Se pregunta si existe correspondencia entre el trabajo invertido y el resultado que el canal debe producir.

**Lección 2 — Qué hace bien y mal cada plataforma.** La siguiente tabla es una **interpretación operativa**, no una clasificación algorítmica.

| Canal | Tratarlo principalmente como | Funciona bien cuando… | Funciona mal cuando… |
|---|---|---|---|
| **Instagram** | Marca visual + descubrimiento + relación recurrente | Hay capacidad para imagen/video, narrativa de marca, piezas cortas, Stories y conversación | La marca solo publica gráficas corporativas sin utilidad ni personalidad |
| **Facebook** | Comunidad, distribución social, servicio y contenidos amplios | Ya existe audiencia, hay conversación local/comunitaria, eventos, servicio o contenidos compartibles | Se replica automáticamente Instagram sin entender el contexto de Facebook |
| **TikTok** | Descubrimiento cultural, entretenimiento/información breve y búsqueda | La marca puede producir ideas nativas de video y responder rápido a intereses reales | Cada pieza requiere semanas de aprobación y termina pareciendo un comercial |
| **YouTube** | Biblioteca audiovisual, búsqueda, recomendación y profundidad | Existe conocimiento, entretenimiento o historias que justifican atención sostenida | Se usa como repositorio de videos hechos para otros medios sin propuesta para el espectador |
| **LinkedIn** | Autoridad profesional, reputación corporativa, talento y B2B | La organización posee personas, datos, experiencia o puntos de vista que aportan valor profesional | El feed se llena de comunicados, efemérides internas y autopromoción sin contexto |

El carácter de descubrimiento de TikTok no es una suposición basada en “virales”: la empresa documenta que For You recomienda contenido en función de interacciones, información del video y otras señales, y que el número de seguidores no es un factor directo de recomendación en su explicación pública del sistema. TikTok también ha desarrollado Creator Search Insights porque la búsqueda es una vía explícita de descubrimiento. citeturn24search0turn24search1turn24search10

YouTube, de forma similar, explica que su sistema busca encontrar videos apropiados para cada espectador, no “promover canales” de manera uniforme. El rendimiento depende del espectador y del contexto de la superficie. citeturn23search11

**Lección 3 — Decidir en qué canales estar.** En agencia conviene puntuar cada canal de 0 a 3 en seis variables: presencia de la audiencia objetivo, adecuación al objetivo de negocio, ventaja editorial, capacidad de producción, capacidad de respuesta y posibilidad de medición. Un canal con audiencia pero sin capacidad operativa puede ser peor decisión que un canal más pequeño que la organización sí puede sostener.

La fórmula de decisión puede expresarse como:

`Prioridad de canal = Ajuste estratégico × Viabilidad operativa`

No es una fórmula estadística; obliga al equipo a evitar el error habitual de discutir solo audiencia potencial.

La decisión final debe dejar cada plataforma en una de cuatro categorías: **primaria, secundaria, mantenimiento o no operar**. “Estar en todas” no constituye estrategia.

**Lección 4 — Objetivos que no sean “ganar seguidores”.** Un objetivo de canal debería especificar **qué cambio busca producir en la audiencia**, no qué contador quiere elevar.

| Objetivo | Métricas de resultado razonables |
|---|---|
| Aumentar conocimiento | Alcance único, viewers nuevos, búsquedas o visitas de perfil cuando estén disponibles |
| Ganar atención | Watch time, duración media, retención, finalización |
| Desarrollar consideración | Clics, visitas a páginas relevantes, guardados, consultas calificadas |
| Construir autoridad | Consumo de contenido experto, comentarios cualitativos, tráfico hacia recursos, invitaciones o menciones relevantes |
| Mejorar relación | Respuesta, recurrencia de participantes, preguntas resueltas, participación de miembros |
| Generar demanda | Clics o leads atribuibles dentro de las limitaciones del tracking |
| Servicio | Tiempo de respuesta, tasa de resolución, reincidencia y motivos de contacto |

Seguidores pueden aparecer como **métrica contextual de stock de audiencia**, pero no como resultado universal. TikTok, por ejemplo, declara explícitamente que follower count no es un factor directo de For You en su documentación pública de recomendaciones; una cuenta grande puede obtener más reproducciones mecánicamente por poseer una base mayor, pero eso no convierte “seguidores” en objetivo de negocio. citeturn24search0

**Lección 5 — Arquetipo y tono por canal.** Los arquetipos son una herramienta creativa, no una verdad psicológica. Su utilidad está en producir consistencia.

La marca define primero cinco elementos estables: **qué cree, qué sabe, qué promete, qué jamás diría y cómo quiere hacer sentir**. Después adapta la expresión al contexto.

Ejemplo de matriz:

| Dimensión | Instagram | TikTok | LinkedIn | YouTube | Facebook |
|---|---|---|---|---|---|
| Rol | Curador | Compañero experto | Colega experto | Profesor/anfitrión | Vecino útil |
| Formalidad | Media | Baja-media | Media-alta | Según formato | Media |
| Humor | Visual/cultural | Alto si es auténtico | Selectivo | Según serie | Conversacional |
| Profundidad | Media | Baja-media por pieza | Media | Alta posible | Media |
| CTA | Guardar, responder, descubrir | Ver, comentar, buscar | Debatir, leer, visitar | Ver siguiente, suscribirse | Conversar, visitar |

Cambiar de tono no significa cambiar de personalidad. La frase central de la marca debe sobrevivir a todos los canales.

**Lección 6 — Documento de estrategia de canal.** El entregable final cabe en una página por plataforma: audiencia prioritaria, trabajo que el canal debe realizar, tres objetivos, KPI, propuesta editorial, formatos, cadencia de partida, tono, CTA y criterio para abandonar o aumentar inversión.

Una estrategia completa debe poder responder: **“¿Qué perdería el negocio si cerráramos esta cuenta mañana?”** Si la respuesta es “seguidores”, la estrategia todavía está incompleta.

## Bloque: parrilla editorial y producción

**Modularidad.**

| Elemento | Definición |
|---|---|
| **Prerrequisitos reales** | Una marca, una audiencia y un objetivo general. Puede cursarse sin el bloque estratégico si esos tres elementos ya existen. |
| **Resultado autónomo** | El alumno puede transformar estrategia en un mes de contenido producible, adaptable y aprobable. |
| **Influencer marketing** | Los pilares y briefs permiten incorporar creators sin convertir cada colaboración en una campaña aislada. |
| **Analítica** | Cada pieza queda etiquetada por pilar, formato, objetivo e hipótesis. |
| **Paid media** | Las piezas de alto potencial pueden entregarse a paid sin diseñar la parrilla orgánica alrededor del media plan. |
| **Contenidos** | Es el bloque central de arquitectura editorial y producción. |

**Lección 7 — Los pilares existen para tomar decisiones.** Un pilar no es un tema amplio como “producto”. Debe explicar **qué valor recibe la audiencia y qué trabajo hace para la marca**.

**Plantilla de matriz de pilares.**

| Pilar | Necesidad de audiencia | Trabajo para la marca | Territorios | Formatos | CTA | KPI primario | Qué queda fuera |
|---|---|---|---|---|---|---|---|
| Aprender | Resolver preguntas | Autoridad | Tutoriales, explicación, mitos | Video, carrusel, YouTube | Guardar/ver más | Retención/guardados | Promoción pura |
| Descubrir | Inspiración | Awareness | Historias, tendencias relevantes | Reel/TikTok/Short | Compartir | Alcance/viewers nuevos | Trend sin relación |
| Elegir | Reducir incertidumbre | Consideración | Comparaciones, casos, demos | Video/documento | Visitar/consultar | Clic/consulta | Claim no demostrable |
| Participar | Pertenencia | Comunidad | Preguntas, UGC, miembros | Post, Stories, comentarios | Responder | Participantes recurrentes | Engagement bait |
| Confiar | Evidencia | Reputación | Personas, procesos, datos | LinkedIn/YouTube/carrusel | Leer/ver | Atención cualificada | Corporate speak |

**Lección 8 — Convertir pilares en sistema.** Cada publicación recibe cuatro etiquetas en la planilla: `pilar`, `objetivo`, `formato` y `hipótesis`. Esto permite descubrir si “video funciona mejor” o si en realidad un determinado **tema + promesa + formato** está funcionando.

Una matriz equilibrada no necesita porcentajes universales como “80/20”. El mix se define por problema de negocio. Una marca recién lanzada puede necesitar más descubrimiento; una marca estable con producto complejo, más explicación y consideración.

**Lección 9 — Calendario mensual realista y ritmo de publicación.** Ninguna frecuencia universal se presenta aquí como ventaja algorítmica. YouTube afirma expresamente que no encontró correlación entre crecer en views y el intervalo entre publicaciones, que no es necesario publicar diariamente o semanalmente y que los descansos no muestran correlación con caídas de views de largo plazo. También indica que la hora de publicación no es conocida por afectar el rendimiento de largo plazo de un video, aunque sí importa operativamente para Lives y Premieres. citeturn23search11

Por eso la frecuencia se calcula desde capacidad.

Una referencia de **planificación, no de algoritmo**, para un equipo pequeño podría ser asignar más slots al canal primario, menos al secundario y dejar capacidad del 15–20 % para coyuntura, comunidad o imprevistos. En YouTube, donde una pieza profunda puede requerir mucho más trabajo, dos videos de calidad pueden representar más producción que veinte posts de texto.

**Plantilla de parrilla editorial mensual.**

| Fecha | Canal | Pilar | Objetivo | Idea/promesa | Formato | Hook/título | CTA | Responsable | Estado | Aprobación | Asset | KPI | Resultado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 03/09 | IG | Aprender | Consideración | “Tres errores al…” | Carrusel | Error más común | Guardar | CM A | Aprobado | Cliente | ID-014 | Guardados/reach | |
| 05/09 | TikTok | Descubrir | Awareness | Demostración | Video | “Esto ocurre cuando…” | Comentar | Video B | Edición | | ID-015 | Views cualificadas | |
| 08/09 | LinkedIn | Confiar | Autoridad | Dato propio | Documento | Hallazgo principal | Debatir | Copy C | Brief | | ID-016 | Clics/engagement | |

La planilla debe tener validaciones de estado: `brief → producción → revisión interna → cliente → cambios → aprobado → programado → publicado → medido`.

**Lección 10 — Formatos y especificaciones.** Las especificaciones siguientes están **consultadas o verificadas al 12 de agosto de 2026**. Las plataformas pueden cambiar límites sin que una estrategia haya cambiado; por eso conviene separar **master de producción** de **límite de upload**.

| Plataforma/formato | Especificación operativa | Tipo de evidencia y vigencia |
|---|---|---|
| Instagram Reels / Stories | Master vertical recomendado por el curso: **9:16, 1080×1920**. Mantener texto crítico dentro de zona segura. | Meta especifica 9:16 para Reels en sus guías creativas; la duración máxima puede diferir según producto/superficie. **[P]**, consulta 12-08-2026. citeturn21search5 |
| Instagram Feed | Master **4:5, 1080×1350** para vertical o **1:1, 1080×1080** cuando la composición lo requiera. | Meta documentó 4:5 y 1:1 como buenas prácticas de feed en su documentación de Smart Crop, hoy una referencia legacy porque Creator Studio migró a Business Suite. **[P]**, consulta 12-08-2026. citeturn21search7 |
| Facebook Reels | Para publicación vía API de Pages Meta documenta **9:16**, recomienda **1080×1920**, mínimo 540×960, 24–60 fps y 3–90 s. El compositor nativo puede evolucionar con reglas diferentes. | Documentación oficial Meta Developers. **[P]**, consulta 12-08-2026. citeturn21search0 |
| Facebook Feed | Master operativo 4:5 o 1:1 para piezas visuales orientadas a feed. | Base creativa Meta legacy; no se presenta como factor de ranking. **[P]**, consulta 12-08-2026. citeturn21search7 |
| TikTok video web | MP4 o WebM; resolución **720×1280 o superior**; en Creator Center consultado, upload de hasta **10 minutos** y menos de **10 GB**. | TikTok Support/Creator Center. **[P]**, consulta 12-08-2026. citeturn23search0 |
| YouTube Shorts | Video **cuadrado o vertical**, hasta **3 minutos** en los uploads que califican bajo las reglas vigentes. | YouTube Help; para canales estándar aplica a videos cargados desde 15-10-2024. **[P]**, consulta 12-08-2026. citeturn23search1 |
| YouTube largo | Master recomendado por el curso: horizontal **16:9, 1080p** salvo necesidad creativa distinta. No se enseña como límite ni ventaja de ranking. | Estándar operativo del curso; verificar requisitos de upload en Studio. |
| LinkedIn imagen | Master de trabajo: 1:1 o 4:5. La verificación secundaria consultada admite un rango más amplio. | ContentIn, proveedor de software que publica su propia guía y declara haber contrastado LinkedIn Help: **[V]**, financiación/publicación propia, consulta 12-08-2026. citeturn4search5 |
| LinkedIn video | La guía secundaria verificada reporta **3 s–15 min en desktop**; conviene trabajar masters 1:1, 4:5, 9:16 o 16:9 según intención. | ContentIn: **[V]**, publicación propia. Los límites deben revalidarse en el compositor nativo antes de una producción crítica. citeturn4search5 |
| LinkedIn documento | Guía secundaria: hasta 100 MB y 300 páginas; diseñar principalmente para lectura móvil. | **[V]**, ContentIn, publicación propia; revalidar trimestralmente. citeturn4search5 |

**Importante:** 9:16, 4:5 o 1080×1920 son decisiones de compatibilidad y producción. Decir que “1080×1920 recibe más alcance porque el algoritmo lo premia” sería **[X]** salvo evidencia específica.

**Lección 11 — Adaptar no es copiar.** Una idea puede viajar; una ejecución no necesariamente.

Ejemplo: investigación propia sobre “cinco errores al elegir X”.

`Dato original → YouTube explicativo → TikTok/Reel con un hallazgo → carrusel IG → documento LinkedIn → post Facebook → respuestas en comentarios → nuevo contenido desde preguntas`

Ese es el **embudo de contenido**:

```text
TEMA / INSIGHT
      ↓
PIEZA FUENTE
      ↓
DESCUBRIMIENTO ──→ Reel / TikTok / Short
      ↓
ATENCIÓN ────────→ carrusel / video / post
      ↓
PROFUNDIDAD ─────→ YouTube / documento / artículo
      ↓
ACCIÓN ──────────→ clic / consulta / demo / registro
      ↓
COMUNIDAD ───────→ comentario / caso / UGC / pregunta
      ↓
NUEVO INSIGHT ───→ siguiente ciclo editorial
```

Un Reel no debe ser simplemente un corte vertical de un video largo si pierde contexto. La adaptación comienza por identificar la **promesa mínima autosuficiente** de cada pieza.

**Lección 12 — Flujo de aprobación de agencia.** El mayor costo de producción de muchas cuentas no es diseñar: es esperar, reabrir versiones y recibir feedback contradictorio.

```text
BRIEF ESTRATÉGICO
       ↓
CONCEPTO + COPY
       ↓
REVISIÓN INTERNA DE AGENCIA
       ↓
QA: MARCA / DATOS / ORTOGRAFÍA / DERECHOS
       ↓
ENVÍO ÚNICO A CLIENTE
       ↓
¿APROBADO?
   ↙       ↘
 NO         SÍ
 ↓           ↓
CAMBIOS    VERSIÓN BLOQUEADA
 ↓           ↓
QA FINAL → PROGRAMACIÓN NATIVA
             ↓
          PUBLICACIÓN
             ↓
       MONITOREO + APRENDIZAJE
```

El RACI mínimo distingue: responsable operativo, aprobador final, expertos consultados e informados. Se establece **una única voz consolidada del cliente**. Un programador pagado resolvería parte del versionado, permisos y aprobación a escala; sin él, la planilla debe registrar versión, fecha de envío, fecha límite, aprobador y estado, y la carpeta debe contener solamente un master marcado `FINAL_APROBADO`.

**Ciclo mensual de planificación:**

```text
CIERRE DE DATOS
   ↓
REPORTE Y DIAGNÓSTICO
   ↓
HIPÓTESIS DEL MES
   ↓
BACKLOG DE IDEAS
   ↓
PARRILLA
   ↓
PRODUCCIÓN
   ↓
APROBACIÓN
   ↓
PROGRAMACIÓN NATIVA
   ↓
PUBLICACIÓN + COMUNIDAD
   ↓
OPTIMIZACIÓN INTRAMES
   ↺
```

## Bloque: algoritmos y distribución con evidencia

**Modularidad.**

| Elemento | Definición |
|---|---|
| **Prerrequisitos reales** | Entender qué es una publicación, un feed, una recomendación y una métrica básica. |
| **Resultado autónomo** | Poder explicar qué se conoce y qué no sobre la distribución de Meta, TikTok, YouTube y LinkedIn, y diagnosticar caídas sin recurrir a supersticiones. |
| **Influencer marketing** | Permite evaluar el contenido de creators por señales reales y no por seguidores solamente. |
| **Analítica** | Es su conexión principal: las señales documentadas se convierten en hipótesis medibles. |
| **Paid media** | Evita atribuir a orgánico resultados comprados y viceversa. |
| **Contenidos** | Explica por qué la satisfacción de una audiencia importa más que obedecer “hacks”. |

**Lección 13 — El modelo mental correcto.** Una versión simplificada del proceso es:

```text
CONTENIDO ELEGIBLE
      ↓
RECUPERACIÓN DE CANDIDATOS
      ↓
PREDICCIONES POR USUARIO Y CONTEXTO
      ↓
RANKING
      ↓
DISTRIBUCIÓN
      ↓
RESPUESTA REAL DEL USUARIO
      ↓
NUEVAS SEÑALES
```

Esto significa que una misma pieza puede ser muy pertinente para un usuario y poco pertinente para otro. Meta explica que sus sistemas predicen cuánto valor podría tener un contenido para una persona utilizando numerosas señales y predicciones; compartir un post, por ejemplo, puede servir como una señal de que resultó valioso, pero no constituye una regla única. citeturn25search1

La pregunta profesional deja de ser “¿qué quiere el algoritmo?” y pasa a ser: **“¿Qué comportamiento demuestra que esta pieza produjo la experiencia que el sistema y nuestra estrategia intentan identificar?”**

**Lección 14 — Meta: lo documentado.** Meta publicó tarjetas de sistema para Feed, Stories, Reels y recomendaciones de contenido conectado y no conectado. La empresa explica que sus sistemas utilizan señales de comportamiento y predicen acciones o valor probable para cada persona; también ofrece controles como Interested/Not Interested, Favorites y feeds cronológicos que modifican la experiencia. citeturn25search1turn25search5

En diciembre de 2025 se incorporaron, donde corresponde, interacciones con Meta AI como señal adicional de personalización. En enero de 2026 Meta afirmó que mejoras de ranking de Q4 2025 aumentaron las views de contenido orgánico de Feed y video y que Instagram incrementó la prevalencia de contenido original entre sus recomendaciones en Estados Unidos; en marzo explicó de manera explícita que contenido duplicado o con cambios de poco valor puede ser depriorizado en Facebook Feed y Reels. Son **datos y políticas declaradas por la propia compañía**, no auditorías independientes. citeturn25search0turn25search3turn25search4

Lo útil para un SMM no es convertir “original” en el nuevo hack. Es evitar construir una operación basada en reuploads o agregación pobre y medir si las piezas originales satisfacen a la audiencia.

Instagram también ofrece Trial Reels: originalmente fueron diseñados para mostrar un Reel primero a no seguidores y entregar datos iniciales de desempeño. Meta indicó en 2025, en un análisis interno de creators que probaron la función, que muchos publicaron más y parte de ellos observó mayor alcance a no seguidores; la propia naturaleza observacional de ese dato obliga a no presentarlo como garantía causal. citeturn25search2turn25search9

**Lección 15 — TikTok: lo documentado.** La explicación pública fundamental de TikTok identifica tres grupos de factores para For You: interacciones del usuario —likes, shares, follows, comments y contenido creado—; información del video —como captions, sonidos y hashtags—; y configuración de dispositivo/cuenta. TikTok señala que las señales de configuración reciben menos peso que indicios activos de interés, y ofrece como ejemplo que completar un video largo constituye una señal más fuerte que la coincidencia de país entre creador y espectador. También aclara que el número de seguidores y haber tenido videos virales anteriormente no son factores directos de recomendación. citeturn24search0

La documentación es de 2020 y **no debe fingirse que describe todo el modelo de 2026**. Sin embargo, TikTok ha ratificado después el principio de personalización conductual: en 2025 explicó que likes, favoritos, búsquedas, tiempo de visualización, controles de temas y “Not Interested” ayudan a moldear For You. citeturn24search2turn24search5

La búsqueda también es una superficie estratégica. Creator Search Insights muestra temas buscados y, en algunas regiones, “content gaps”; TikTok lanzó la función en mercados latinoamericanos como México y Colombia. Eso permite formular contenidos alrededor de preguntas existentes, pero no justifica afirmar “poner la keyword en pantalla garantiza alcance”. citeturn24search1turn24search10

**Lección 16 — YouTube: lo documentado.** YouTube describe recomendaciones que utilizan señales como historial de visualización y búsqueda, suscripciones, likes, dislikes y “Not interested”, además de señales de satisfacción y comportamiento contextual. La empresa insiste en que el sistema intenta encontrar contenido para el espectador, no simplemente empujar canales a una audiencia. citeturn23search11

Tres correcciones importantes para un curso de SMM:

Primero, **no existe una duración universal ideal**: YouTube recomienda usar la longitud que el contenido necesita y estudiar la retención propia. citeturn23search3

Segundo, **publicar más no equivale a crecer más**. YouTube afirma que no observa una correlación entre intervalo de uploads y crecimiento de views, y que tomar pausas no genera por sí mismo una penalización de canal. citeturn23search11

Tercero, **CTR debe leerse junto a impresiones, fuente de tráfico y audiencia**. Una caída de CTR puede acompañar un resultado positivo cuando el video está llegando a una audiencia mucho más amplia. Incluso CTR y duración media altas no garantizan crecimiento infinito de impresiones: el tamaño del mercado interesado y la competencia también importan. citeturn23search2turn23search10

Esto es exactamente el tipo de matiz que un reporte de agencia debe preservar.

**Lección 17 — LinkedIn: lo documentado en 2026.** La ingeniería de LinkedIn describió en marzo de 2026 una nueva arquitectura de Feed que utiliza recuperación y ranking con LLM y modelos generativos sobre una plataforma que declara servir a más de 1.300 millones de profesionales. Entre los inputs descritos figuran información profesional del miembro —industria, experiencia, habilidades, ubicación—, texto y formato del post, autor, metadata y engagement, así como historial de acciones del miembro: leer, hacer like, comentar, volver, pasar de largo y otras interacciones. El sistema busca equilibrar relevancia y frescura. citeturn9view0

La compañía describió también el uso de señales como dwell, likes, comments, shares y skips y actualizaciones nearline de comportamiento. En una explicación pública complementaria, LinkedIn señaló que está tomando medidas contra engagement pods, automatización de comentarios, engagement bait del tipo “Comment YES” y contenido genérico o reciclado diseñado para manipular distribución. citeturn9view0turn8view0

Eso permite afirmar que **relevancia profesional, semántica, comportamiento y calidad de interacción entran en el sistema**. No permite afirmar que “tres comentarios en los primeros quince minutos multiplican alcance” o que “publicar texto sin enlace obtiene un bonus”: ambas serían [X].

**Lección 18 — Analíticas nativas y folclore.**

| Plataforma | Señales operativas a observar | Fuente |
|---|---|---|
| Meta | Reach/views, interacciones, watch metrics disponibles, audiencia, visitas/acciones de perfil | Meta Business Suite e Instagram Insights ofrecen métricas de performance y audiencia; las métricas exactas cambian por producto. **[P]** citeturn21search11turn21search14 |
| TikTok | Views, likes, seguidores netos, métricas por pieza, variables de audiencia disponibles | Creator Center documenta analytics de cuenta, contenido y followers. **[P]** citeturn23search0 |
| YouTube | Impresiones, CTR, views, unique viewers, watch time, average view duration, retención y fuentes | YouTube Studio/Help. **[P]** citeturn23search2turn23search10 |
| LinkedIn | Impresiones/views, clicks/interacciones, seguidores y estadísticas de Page disponibles | LinkedIn/Microsoft documenta estadísticas de organización y contenido; disponibilidad depende del activo. **[P]** citeturn4search1 |

**Tabla de mitos que deben descartarse.**

| Afirmación | Veredicto | Razón |
|---|---|---|
| “Existe una hora mágica universal para publicar.” | **[X]** | YouTube niega un efecto conocido de la hora sobre desempeño de largo plazo; ninguna evidencia primaria habilita universalizar una hora para todas las plataformas. citeturn23search11 |
| “Hay que publicar todos los días o el algoritmo castiga.” | **[X]** | YouTube lo contradice explícitamente; no existe base para convertir frecuencia diaria en ley multiplataforma. citeturn23search11 |
| “TikTok solo entrega alcance a cuentas con muchos seguidores.” | **[X]** | TikTok declara que follower count no es factor directo de For You. citeturn24search0 |
| “Exactamente N hashtags desbloquean alcance.” | **[X]** | TikTok menciona hashtags como parte de la información de video, no una cuota mágica. citeturn24search0 |
| “Todo depende de los primeros 30/60 minutos.” | **[X]** | Las plataformas describen frescura y respuesta del usuario, pero no una ventana universal fija con esa regla. |
| “Si el alcance cae, es shadowban.” | **[X]** | Una caída aislada no identifica causalidad: audiencia, formato, competencia, elegibilidad y tamaño de tema pueden producir resultados distintos. YouTube documenta precisamente varios de estos efectos contextuales. citeturn23search2 |
| “CTR más alto siempre significa mejor video.” | **[X]** | Puede subir porque la pieza solo alcanzó una audiencia pequeña y leal. citeturn23search2turn23search10 |
| “Todos los engagements valen igual.” | **[X]** | TikTok y LinkedIn documentan tipos y pesos/contextos diferentes de interacción. citeturn24search0turn9view0 |
| “Formato nuevo = boost automático.” | **[X]** | Que una plataforma lance una función no prueba una bonificación universal de ranking. |
| “Borrar y republicar resetea el algoritmo.” | **[X]** | No hay base primaria suficiente para enseñarlo como táctica. |

La prueba de madurez del alumno es poder decir **“no sabemos”** cuando la plataforma no lo ha documentado.

## Bloque: comunidad y crisis

**Modularidad.**

| Elemento | Definición |
|---|---|
| **Prerrequisitos reales** | Conocer la voz básica de la marca y tener acceso a los comentarios o mensajes que debe gestionar. |
| **Resultado autónomo** | Diseñar una política de moderación, clasificar conversaciones, escalar riesgos y operar una crisis con roles y tiempos. |
| **Influencer marketing** | Define cómo responder cuando una colaboración produce críticas, desinformación o incidentes. |
| **Analítica** | Convierte conversaciones en datos: motivos, volumen, reincidencia, resolución, participación. |
| **Paid media** | Aclara quién modera comentarios en contenidos promocionados y cómo un issue pagado puede escalar al equipo orgánico. |
| **Contenidos** | La comunidad alimenta briefs: preguntas, objeciones y vocabulario real se convierten en contenido. |

**Lección 19 — Moderación no es “contestar todo”.** Su objetivo es proteger tres bienes: **personas, conversación y marca**.

La política debe especificar qué se mantiene, qué se responde, qué se oculta/elimina según herramientas disponibles y qué se escala. El criterio profesional es no borrar crítica legítima solo porque es incómoda. Spam, exposición de datos personales, amenazas, discurso de odio, contenido ilícito o violaciones claras de las normas pueden requerir moderación; una queja dura sobre el servicio requiere respuesta y registro.

**Plantilla de política:**

| Clase | Acción pública | Acción interna |
|---|---|---|
| Pregunta simple | Responder | Etiquetar motivo |
| Reclamo operativo | Reconocer + orientar | Abrir/derivar caso |
| Crítica/opinión | Reconocer cuando aporte | Registrar insight |
| Error de la marca | Corregir | Notificar owner |
| Desinformación verificable | Corregir con fuente | Vigilar recurrencia |
| Provocación repetida | Una respuesta factual o no enganchar | Registrar |
| Datos personales | Mover conversación a privado/moderar | Proteger datos |
| Spam | Ocultar/eliminar según política | Registrar |
| Amenaza o riesgo de daño | No improvisar | Escalamiento inmediato |
| Alegación legal/regulatoria | Acusar recibo sin adjudicar | Legal/compliance |
| Odio/acoso | Aplicar normas | Reportar/escalar |

**Lección 20 — Tono cuando existe conflicto.** El orden recomendado es:

`Escuchar → reconocer → verificar → responder lo que se sabe → decir qué ocurrirá después → cumplir la actualización`

La respuesta no debe comenzar defendiéndose. “Lamentamos que te sientas así” suele ser peor que identificar el hecho: “Entendemos que recibiste X cuando esperabas Y; estamos revisando el caso.”

Transparencia, rapidez y consistencia cuentan con respaldo empírico, aunque la evidencia no convierte ningún wording específico en universal. Un estudio de 2026 con 174 participantes y modelamiento estructural encontró asociaciones significativas entre transparencia y confianza, rapidez y efectividad percibida, y consistencia y confianza. Su tamaño y contexto obligan a usarlo como apoyo, no como ley universal. **[P-estudio replicable]** citeturn29search2

**Lección 21 — Árbol de moderación y escalamiento.**

```text
NUEVO COMENTARIO / MENSAJE
          ↓
¿VIOLA NORMAS O EXPONE A ALGUIEN?
      ↙             ↘
    SÍ               NO
    ↓                 ↓
MODERAR + LOG     ¿HAY RIESGO DE
+ REPORTAR        SEGURIDAD, LEGAL,
SI APLICA         REGULATORIO O PRENSA?
                      ↙        ↘
                    SÍ          NO
                    ↓            ↓
                   P0/P1     ¿RECLAMO?
                               ↙   ↘
                             SÍ     NO
                             ↓       ↓
                      RESPONDER +    ¿CRÍTICA?
                       DERIVAR       ↙      ↘
                                  SÍ          NO
                                  ↓            ↓
                            RECONOCER/      PARTICIPAR,
                            EXPLICAR        AGRADECER,
                                           AMPLIFICAR
```

La planilla de comunidad utiliza: fecha/hora, canal, enlace, usuario anonimizado si corresponde, categoría, severidad, responsable, primera respuesta, derivación, resolución y observaciones.

**Lección 22 — Comunidad como activo y no buzón.** Una comunidad útil produce cuatro cosas: **feedback, conocimiento entre miembros, prueba social y participación en el producto o cultura de marca**.

Nubank constituye un caso latinoamericano claro. En abril de 2024 la compañía informó que NuCommunity superaba los 386.000 miembros, promediaba unas 150.000 pageviews diarias y 4,5 millones mensuales, y se utilizaba para interacción, feedback, pruebas de productos y contacto con ejecutivos. La compañía relata que miembros participaron en pruebas de productos como Ultravioleta, tarjeta virtual y NuCoin. Son cifras declaradas por Nubank, no auditadas aquí, pero el diseño del caso demuestra que una comunidad puede ser utilizada como **infraestructura de escucha y cocreación**, no solamente soporte. **[P-declaración de empresa]** citeturn27search1turn27search5

El SMM debería extraer cada mes: preguntas recurrentes, lenguaje utilizado por usuarios, objeciones, casos positivos, miembros activos, ideas de contenido y feedback que debe llegar a producto.

**Lección 23 — Detectar una crisis antes de que sea “trending”.** Una crisis no se define por “muchos comentarios”. Se define por una combinación de **severidad + velocidad + legitimidad + exposición + impacto operativo/reputacional**.

Escala propuesta:

| Nivel | Ejemplo | Owner |
|---|---|---|
| P3 | Queja individual sin riesgo | Community manager |
| P2 | Tema repetido o post adverso con tracción moderada | SMM + cliente |
| P1 | Volumen acelerado, prensa/creators, falla amplia o acusación seria | Líder de cuenta + comunicaciones |
| P0 | Seguridad, salud, fallecimiento, regulación, litigio relevante, datos, crisis nacional/multimercado | Comité ejecutivo de crisis |

Un estudio de 2025 analizó **3.135.675 registros de difusión de 94 crisis corporativas ocurridas entre 2016 y 2019** en el ecosistema social chino. Encontró que intervenir durante la fase ascendente estaba asociado con ciclos de propagación más cortos y que combinar respuestas formales e informales podía resultar más efectivo que limitarse a un comunicado. Por contexto y periodo no debe extrapolarse mecánicamente a LatAm, pero sí respalda abandonar la lógica de “esperemos a mañana para ver si desaparece”. **[P-estudio replicable]** citeturn29search0turn29search10

**Lección 24 — Protocolo de crisis en tiempo real.** Los tiempos siguientes son **SLA internos propuestos para una agencia**, no reglas científicas ni legales.

| Desde detección | Acción |
|---|---|
| **0–15 min** | Capturar evidencia, enlaces y métricas; verificar que el incidente existe; clasificar P0–P3. |
| **15–30 min** | Alertar owner; reunir hechos conocidos/desconocidos; definir vocería y canales. |
| **30–60 min** | Si la conversación crece y los hechos aún no están completos, preparar un holding statement factual. |
| **60–120 min** | Emitir la primera actualización sustantiva cuando haya hechos suficientemente verificados; nunca inventar certeza para cumplir un reloj. |
| **Cada 1–2 h en fase activa** | Reevaluar velocidad, nuevos hechos, misinformation, prensa y respuesta de comunidad. Actualizar si materialmente necesario. |
| **Al estabilizarse** | Explicar qué ocurrió, qué se hizo y qué sigue. |
| **24–72 h posteriores** | Postmortem operativo; cambios a FAQ, producto, proceso y playbook. |

Para riesgos de seguridad, salud, privacidad o materias legales, **la precisión y la intervención de responsables especializados prevalecen sobre un SLA de redes**.

**Árbol de crisis:**

```text
INCIDENTE
   ↓
¿RIESGO DE SEGURIDAD / SALUD / LEGAL / DATOS?
       ↙                         ↘
     SÍ                           NO
     ↓                             ↓
     P0                    ¿SE ACELERA ENTRE
COMITÉ + VOCERO            PLATAFORMAS/PRENSA?
                               ↙       ↘
                             SÍ         NO
                             ↓           ↓
                            P1       ¿AFECTA A MUCHOS
                                     CLIENTES/OPERACIÓN?
                                       ↙       ↘
                                     SÍ         NO
                                     ↓           ↓
                                    P1/P2       P2/P3
```

En crisis de desinformación, una corrección única no garantiza aprendizaje duradero. Dos experimentos de panel preregistrados publicados en *Journal of Communication*, con N=6.983 en conjunto, encontraron que el efecto de fact-checks disminuía sustancialmente con el tiempo y que recordatorios posteriores podían prolongarlo. Por eso, una marca no debería asumir que “ya aclaramos esto ayer” resuelve necesariamente una falsedad persistente. **[P-estudio replicable]** citeturn29search3turn29search5

## Bloque: medición y reportería de agencia

**Modularidad.**

| Elemento | Definición |
|---|---|
| **Prerrequisitos reales** | Acceso a datos nativos y comprensión básica de porcentajes. |
| **Resultado autónomo** | Construir un reporte mensual que conecte resultados, hipótesis y decisiones sin sobreinterpretar variaciones. |
| **Influencer marketing** | Permite integrar creator results usando objetivos comparables, no follower counts aislados. |
| **Analítica** | Es el módulo de traducción de métricas a decisiones. |
| **Paid media** | Obliga a separar distribución orgánica, pagada y mixta. |
| **Contenidos** | Determina qué pilares, formatos y promesas deben repetirse, cambiar o retirarse. |

**Lección 25 — La métrica depende de la pregunta.** El SMM no “reporta métricas”; reporta evidencia respecto a objetivos.

| Pregunta | Métrica principal | Métrica diagnóstica |
|---|---|---|
| ¿Llegamos a gente? | Reach/viewers | Impresiones, fuente |
| ¿Capturamos atención? | Watch time/retención | View duration, completion |
| ¿El packaging convenció? | CTR donde existe | Impresiones/fuente |
| ¿La gente consideró volver? | Guardados, recurrencia, returning viewers cuando exista | Comentarios cualitativos |
| ¿Generamos conversación? | Participación pertinente | Tipo de comentarios |
| ¿Generamos acción? | Clic/conversión atribuible | CTR, landing performance |
| ¿Atendimos bien? | Resolución/SLA | Motivo y reincidencia |
| ¿Construimos comunidad? | Participantes recurrentes | Contribuciones, UGC, respuestas entre miembros |

YouTube ilustra por qué hay que usar pares de métricas: la propia plataforma advierte que un CTR menor puede acompañar una expansión saludable de impresiones a una audiencia más amplia. citeturn23search2

**Lección 26 — Higiene métrica.** Nunca sumar indiscriminadamente “views” de distintas plataformas como si significaran lo mismo. Las definiciones, superficies y reglas de conteo pueden variar. Para un reporte multicanal, es más defendible mostrar resultados dentro de cada ecosistema y luego construir indicadores estratégicos comunes —por ejemplo, porcentaje de contenidos por encima de su baseline— que fingir equivalencias.

Fórmulas útiles en la planilla:

`Engagement por alcance = interacciones relevantes / reach × 100`

`Click rate = clics / impresiones u oportunidades de clic × 100`

`Crecimiento neto = altas - bajas`

`Mediana de reach por pieza = mediana(reach de posts comparables)`

`Eficiencia de contenido = resultado objetivo / unidades producidas`

El denominador debe aparecer siempre. “Subimos 40 % el engagement” no significa nada sin saber si se habla de interacciones totales, tasa por reach, tasa por impresión o posts publicados.

**Lección 27 — Construcción del reporte mensual.**

**Plantilla de reporte de agencia:**

| Objetivo | KPI | Target/expectativa | Mes | Mes anterior | Baseline 3M | Diagnóstico | Decisión |
|---|---|---:|---:|---:|---:|---|---|
| Awareness | Mediana reach/post | 25k | 27k | 23k | 22k | Mejora concentrada en pilar educativo | Producir dos variaciones |
| Atención | Watch time/view | — | 8,4 s | 8,1 s | 7,9 s | Cambio pequeño | No concluir aún |
| Consideración | Click rate | 1,8 % | 2,1 % | 1,7 % | 1,6 % | Tres piezas explican crecimiento | Repetir promesa |
| Comunidad | Tiempo mediano primera respuesta | <2 h | 1h20 | 2h10 | 1h55 | Mejora operativa | Mantener turnos |

El reporte completo tiene siete capas: **resumen ejecutivo, objetivos, resultados, diagnóstico, contenidos, comunidad/riesgos y plan de acción**.

El resumen ejecutivo no debe comenzar con followers. Un buen ejemplo sería: “El canal aumentó su capacidad de descubrimiento debido a tres piezas educativas; la interacción por alcance permaneció estable; el tráfico cualificado mejoró; no existe todavía evidencia suficiente para atribuir el cambio a mayor frecuencia.”

**Lección 28 — Tendencia contra ruido.** Una variación mes a mes no es automáticamente una tendencia.

Reglas prácticas del curso, presentadas como **heurística de análisis, no significancia estadística**:

Comparar piezas semejantes por objetivo y formato. Usar medianas además de totales cuando cambia el número de posts. Mantener una línea base móvil de aproximadamente tres meses. Antes de declarar ganador un formato, buscar varios activos comparables. Y si la dirección cambia cada mes, describir el resultado como volatilidad hasta tener más evidencia.

La planilla puede incluir una distribución por pilar:

| Pilar | N piezas | Mediana reach | Mediana ER/reach | Mediana watch | Clicks | Observación |
|---|---:|---:|---:|---:|---:|---|
| Aprender | 8 | | | | | |
| Descubrir | 6 | | | | | |
| Elegir | 4 | | | | | |
| Comunidad | 5 | | | | | |

Con un solo video exitoso no debe decirse “el público quiere tutoriales”. Se dice: **“una pieza tutorial mostró una señal positiva; produciremos réplicas controladas para verificarla.”**

**Lección 29 — Defender resultados ante un cliente obsesionado con seguidores.** El SMM no debe ridiculizar la preocupación del cliente. Debe traducirla.

“Queremos seguidores” suele esconder una de tres necesidades: demostrar notoriedad, construir una base propia o exhibir crecimiento visible. Se responde con una jerarquía:

`Resultado de negocio → comportamiento de audiencia → KPI del canal → followers como contexto`

Ejemplo: “La base creció menos que el mes anterior, pero las piezas llegaron a más no seguidores, sostuvieron mayor watch time y aumentaron clics al producto. Para el objetivo de consideración, esos indicadores son más directos.”

TikTok constituye una evidencia particularmente útil para separar follower count y distribución: la propia plataforma dice que cantidad de followers no es un factor directo de For You, aunque una cuenta grande pueda beneficiarse mecánicamente de tener mayor audiencia existente. citeturn24search0

**Lección 30 — Operación mensual de mejora continua.** El equipo cierra cada reporte con máximo tres decisiones:

`Seguir` — qué patrón tiene suficiente señal para mantenerse.  
`Probar` — qué hipótesis necesita más evidencia.  
`Detener` — qué consume recursos sin contribuir al objetivo.

La planilla maestra recomendada tiene seis pestañas:

| Pestaña | Función |
|---|---|
| **Config** | Objetivos, KPI, canales, owners, convenciones |
| **Calendario** | Parrilla y aprobación |
| **Posts** | Datos por pieza |
| **Comunidad** | Casos, motivos, SLA, insights |
| **Reporte** | Agregaciones mensuales |
| **Experimentos** | Hipótesis, cambio aplicado, resultado, decisión |

Un software pagado puede automatizar ingestión de datos, aprobaciones, permisos, inbox, tagging y dashboards. **La alternativa gratuita no es hacer menos gobernanza:** es trasladar explícitamente esa gobernanza a la planilla y las herramientas nativas.

## Plantillas operativas, casos latinoamericanos y ejercicios encadenados

**Protocolo de gobernanza de archivos.** Cada asset utiliza un ID único, por ejemplo `MARCA_2026-09_IG_014`. La planilla y la carpeta utilizan el mismo ID. No se programan piezas sin estado `APROBADO`. Los cambios posteriores a aprobación generan versión nueva; no se sobreescribe silenciosamente un master.

**Plantilla mínima de brief de pieza:**

| Campo | Contenido |
|---|---|
| ID | |
| Objetivo | |
| Audiencia/contexto | |
| Pilar | |
| Una sola promesa | |
| Hook/título | |
| Prueba/dato | |
| Estructura | |
| CTA | |
| Adaptaciones | |
| Riesgos/claims | |
| KPI | |

**Guion breve de video:**

```text
HOOK: ¿por qué debería detenerme?
↓
CONTEXTO: ¿qué necesito saber?
↓
VALOR / DEMOSTRACIÓN: ¿qué obtiene el espectador?
↓
PRUEBA: ejemplo, dato o evidencia
↓
CIERRE: conclusión
↓
CTA: siguiente acción coherente
```

### Cinco casos latinoamericanos para discusión docente

**Caso Domino’s Pizza Perú — cuando la defensa agrava el incidente.** El 27 de enero de 2015 un cliente denunció en Facebook haber encontrado una cucaracha en una pizza y cuestionó la respuesta inicial de la operación. ESAN documentó que la comunicación posterior llegó a cuestionar la interpretación del cliente y que la gerente utilizó la frase “no somos comunicadores, somos pizzeros”. En los días siguientes hubo inspecciones, nuevas denuncias, respuesta desde la matriz y cierre temporal de la operación peruana. Domino’s volvió posteriormente con otro operador. **HC.** citeturn28search0turn28search1turn28search2turn28search5

El aprendizaje no es “responder en menos de X minutos hubiera salvado la franquicia”, porque eso no puede probarse. El aprendizaje operacional es que **cuestionar al denunciante antes de controlar los hechos, responder defensivamente, carecer de vocería preparada y permitir inconsistencia entre operación local y marca global aumenta el riesgo comunicacional**. El caso sirve para simular P0/P1, holding statement, vocería y coordinación con operaciones.

**Caso Nubank — comunidad como infraestructura de producto.** NuCommunity se originó, según Nubank, a partir de comunidades que ya surgían orgánicamente alrededor de la marca. Para 2024 la empresa reportaba más de 386.000 miembros y utilización del espacio para feedback, pruebas y conversación directa con ejecutivos. **[P-declaración de empresa].** citeturn27search1turn27search5

Aprendizaje: el CM no debería entregar solo un informe de “sentimiento”. Puede convertir preguntas y aportes en backlog para contenidos, producto, CX y reputación.

**Caso LATAM Brasil — abrir un canal con un trabajo definido.** En junio de 2024 LATAM Brasil anunció su entrada a TikTok como parte de su estrategia de comunicación. La compañía declaró que el perfil se dedicaría a destinos, experiencias, eventos y tendencias de viaje, con la intención de acercarse a comunidades y generar un nuevo canal de interacción. El lanzamiento acompañó la campaña “Férias das Férias”, desarrollada con una estrategia 360 y agencias del ecosistema que atendía a LATAM en Brasil. **[P-declaración de empresa].** citeturn27search0

Aprendizaje: abrir un canal debe venir acompañado de **territorios editoriales y función**, no del argumento “todos están en TikTok”.

**Caso Mercado Livre/Mercado Libre — una idea fuente que genera distribución entre medios.** En Cannes Lions 2026, “Field Barcode/Cupom em Campo”, creado por GUT São Paulo para Mercado Livre, convirtió el patrón del césped del Pacaembu en un enorme código de barras y ganó el Grand Prix de Outdoor. La pieza física circuló después a través de imágenes, plataformas digitales y redes sociales. **HC; fuente sectorial independiente.** citeturn27search2turn27search6

El valor para este curso no es premiación ni paid media, sino arquitectura de contenido: **una idea fuerte puede ser fuente de múltiples activos**, mientras que publicar veinte ejecuciones sin idea no crea necesariamente una narrativa.

**Caso Lu do Magalu — personalidad de marca sostenida.** Magazine Luiza ha desarrollado a “Lu” durante años como personaje de marca y presencia digital. En una publicación corporativa de 2023 la propia compañía enumeraba presencia del personaje en Instagram, TikTok, Facebook y YouTube y reconocimientos recibidos por proyectos de influencer y contenido social; esos premios y afirmaciones proceden de la marca y se tratan como tales. **[P-declaración de empresa].** citeturn20search1

El aprendizaje no es “crear un avatar”. Es que un tono se vuelve activo cuando posee reglas suficientes para mantenerse reconocible entre plataformas, formatos y años. La personalidad no puede depender del copywriter de turno.

### Semillas de ejercicio encadenadas

Las siguientes **quince tareas duran aproximadamente 10–20 minutos cada una** y se realizan sobre la misma marca real. Juntas producen los artefactos finales del curso.

| Tarea | Trabajo | Artefacto acumulado |
|---|---|---|
| **1** | Elegir marca y escribir en tres líneas negocio, audiencia y principal resultado buscado. | Ficha de marca |
| **2** | Auditar todos sus canales activos con cinco publicaciones recientes por canal. | Auditoría de canales |
| **3** | Puntuar cada plataforma por ajuste estratégico y capacidad operativa. | Scorecard |
| **4** | Elegir máximo tres objetivos de canal que no sean seguidores. | Mapa objetivo/KPI |
| **5** | Escribir voz estable y adaptación de tono para cada canal. | Matriz de tono |
| **6** | Diseñar entre tres y cinco pilares utilizando necesidad de audiencia + trabajo de marca. | **Matriz de pilares** |
| **7** | Colocar cada pilar dentro del embudo descubrimiento-atención-consideración-acción-comunidad. | Embudo de contenido |
| **8** | Calcular una cadencia mensual sostenible con la capacidad real del equipo. | Presupuesto de contenidos |
| **9** | Completar cuatro semanas de publicaciones con pilar, objetivo, formato y CTA. | **Parrilla de un mes** |
| **10** | Escoger una idea y adaptarla a tres plataformas sin copiar exactamente el asset. | Sistema de adaptación |
| **11** | Escribir hook, desarrollo, prueba, cierre y CTA de un video. | **Guion de una pieza** |
| **12** | Asignar responsable, aprobador, consultados, fecha límite y estados del flujo. | RACI + flujo de aprobación |
| **13** | Elegir cinco publicaciones reales y explicar su performance sin utilizar explicaciones algorítmicas no demostrables. | Diagnóstico basado en evidencia |
| **14** | Clasificar diez comentarios imaginarios/reales y definir P0–P3, respuesta, derivación y SLA. | **Política de moderación + protocolo de crisis** |
| **15** | Construir un mes simulado/real de métricas, baseline, diagnóstico, tres aprendizajes y tres decisiones. | **Reporte mensual completo** |

La tarea 13 tiene una condición: cada frase que comience con “la plataforma mostró esta pieza porque…” debe ser marcada [P], [V] o [X]. Si el alumno no puede respaldarla, se reescribe como hipótesis: “observamos que…” o “probaremos si…”.

## Bibliografía clasificada y reglas de actualización

Este documento debe tener **control de versiones trimestral** para especificaciones y, como mínimo, semestral para las explicaciones de producto. Una publicación oficial antigua puede seguir siendo útil —por ejemplo, la explicación de TikTok de 2020—, pero debe presentarse con fecha y contrastarse con comunicaciones más recientes, como los controles de personalización que TikTok publicó en 2025. citeturn24search0turn24search5

| Clase | Fuente y fecha | Uso permitido en el curso |
|---|---|---|
| **[P]** | Meta, *How AI Influences What You See on Facebook and Instagram*, 29-06-2023. citeturn25search1 | Modelo general de ranking, señales, predicciones y múltiples superficies. |
| **[P]** | Meta, actualización de personalización con Meta AI, 01-10-2025; efectiva desde 16-12-2025. citeturn25search3turn25search7 | Mostrar que las señales cambian y requieren fecha. |
| **[P]** | Meta, *2026: AI Drives Performance*, 28-01-2026. citeturn25search0 | Cambios recientes de ranking/originalidad; datos internos de Meta, no evidencia independiente. |
| **[P]** | Meta, *Rewarding Original Creators on Facebook*, 13-03-2026. citeturn25search4 | Política actual declarada sobre contenido original/duplicado en Facebook. |
| **[P]** | Meta, *Trial Reels*, 10-12-2024, y actualización de Adam Mosseri, 12-06-2025. citeturn25search9turn25search2 | Cómo opera Trial Reels y resultados internos con cautela causal. |
| **[P]** | Meta Business Suite / Business Help. citeturn21search1turn21search11 | Stack gratuito, programación e insights. |
| **[P]** | Meta Developers, Facebook Reels Publishing API, consulta 12-08-2026. citeturn21search0 | Especificaciones técnicas de Reels de Pages vía API. |
| **[P]** | TikTok Newsroom, *How TikTok recommends videos #ForYou*, 18-06-2020. citeturn24search0 | Factores públicamente descritos y descarte del mito de follower count directo. |
| **[P]** | TikTok, Creator Search Insights, 13-03-2024; despliegue LatAm comunicado 30-08-2024. citeturn24search1turn24search10 | Búsqueda como superficie de descubrimiento. |
| **[P]** | TikTok, actualización de personalización de For You, 03-06-2025. citeturn24search2turn24search5 | Controles y señales de preferencia recientes. |
| **[P]** | TikTok Creator Center Support, consulta 12-08-2026. citeturn23search0 | Analytics, gestión, scheduling y especificaciones web actuales consultadas. |
| **[P]** | YouTube Help, *Performance FAQ and troubleshooting*, consulta 12-08-2026. citeturn23search11 | Frecuencia, pausas, publicación y lógica de recomendación. |
| **[P]** | YouTube Help, *Decoding CTR & impressions*, consulta 12-08-2026. citeturn23search2 | Interpretación correcta de CTR, impresiones y expansión de audiencia. |
| **[P]** | YouTube Help, *Understand three-minute YouTube Shorts*, consulta 12-08-2026. citeturn23search1 | Clasificación y duración actual de Shorts. |
| **[P]** | YouTube Help, recomendaciones, consulta 12-08-2026. citeturn23search3 | Ausencia de duración universal y personalización contextual. |
| **[P]** | LinkedIn Engineering, nueva generación del Feed, 12-03-2026. citeturn9view0 | Arquitectura, información profesional, historial de interacción, relevancia/frescura y señales de Feed. |
| **[P]** | Tim Jurka/LinkedIn, comunicaciones públicas de producto, 2025–2026. citeturn9view1turn8view0 | Personalización, calidad, medidas contra manipulación y engagement bait. |
| **[P]** | Microsoft Learn / LinkedIn organization statistics, actualizado 24-06-2026. citeturn4search1 | Tipos de métricas de Page/organización. |
| **[P-estudio]** | Yu, Ye & Zhang, *Mathematics*, 2025; 94 crisis y 3.135.675 registros. citeturn29search0turn29search10 | Timing de respuesta y dinámica de propagación. Investigación replicable; contexto chino, no universalizar magnitudes. |
| **[P-estudio]** | Salem et al., *Frontiers in Communication*, 2026; N=174, SEM. citeturn29search2 | Transparencia, rapidez, consistencia y percepción de crisis; tamaño/contexto limitan generalización. |
| **[P-estudio]** | Chae, Groeling & Song, *Journal of Communication*, 2026; dos panel experiments preregistrados, N total=6.983. citeturn29search3turn29search5 | Duración de correcciones y utilidad de recordatorios. |
| **[V]** | ContentIn, guía LinkedIn 2026. Publicada/financiada por el propio proveedor de software. citeturn4search5 | Solo verificación operativa secundaria de límites/especificaciones cuando LinkedIn Help no resulta indexable; nunca evidencia algorítmica. |
| **HC** | ESAN y Gestión sobre Domino’s Perú, 2015–2025. citeturn28search0turn28search1turn28search2 | Reconstrucción histórica del caso; no algoritmo. |
| **[P-empresa]** | Nubank Newsroom, NuCommunity, 11-04-2024. citeturn27search1turn27search5 | Diseño de comunidad y cifras declaradas por la empresa. |
| **[P-empresa]** | LATAM Airlines, lanzamiento de TikTok Brasil, 20-06-2024. citeturn27search0 | Estrategia declarada de entrada a un canal. |
| **HC** | AdNews/B9, Mercado Livre “Field Barcode”, junio de 2026. citeturn27search2turn27search6 | Caso de idea fuente y expansión entre medios. |
| **[P-empresa]** | Magazine Luiza, comunicación corporativa sobre Lu do Magalu, 2023. citeturn20search1 | Caso de personalidad consistente de marca. |

El criterio de actualización debe ser estricto. Cuando una plataforma cambia una métrica, formato o sistema de recomendación, **se cambia la lección, no se racionaliza el dato anterior**. Cuando una agencia publica un benchmark, se pregunta quién lo financió, cuál fue la muestra, qué cuentas incluyó, qué periodo abarcó y si correlación fue confundida con causalidad. Cuando alguien afirma “el algoritmo premia…”, la primera pregunta del curso debe ser siempre: **“¿Cuál es la evidencia, de qué fecha y para qué superficie?”**

Esa disciplina constituye la diferencia entre gestión profesional de redes y folclore de marketing.