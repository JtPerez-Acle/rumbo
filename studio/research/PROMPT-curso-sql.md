# Deep-research prompts — curso de SQL

Kept beside the output it produces, so the next course can copy the shape and so
anyone judging the document can see what it was asked for.

Run **Prompt 1 first**. Its answer is pasted into Prompt 2. They are split
because the environment decision is load-bearing for all thirty lessons and is
cheap to get wrong: if the tool needs a credit card, a desktop install, or an
English-only signup, the whole document is built on sand.

Target file: `studio/research/sql.md` · slug `curso-sql` ·
category `Analítica y automatización` (already holds two courses, so it is not a
one-course category) · free stroke colour `#336791`.

---

## The decision this course is built on

**Comprehension is the spine; the audit is the proof.**

Not "understand SQL" — that is a certificate-shaped outcome and PRODUCT.md
refuses tier one. Not "type thirty queries" either: the format cannot narrate
syntax, the audience studies on a phone, and an LLM drafts a competent query in
three seconds. What is still scarce in 2026 is knowing whether the query answers
the question that was actually asked.

So the exercises are **judgement work that produces an artifact**: read a query
and say what it really returns, find the number that is wrong and name why,
specify a question precisely enough to be answerable, verify what the machine
handed you. The learner ends with an audit of their own data — questions,
verified queries, findings, and the caveats — which is a document a client pays
for.

Two consequences the prompts below enforce:

- **Only one module of five needs a keyboard.** Reading and judging work on a
  phone; writing does not. That is a far better sentence for the course card
  than "you need a laptop."
- **The deliverable must carry the queries and the verification**, not only the
  findings. `PROJECT_TEMPLATES`' default is already
  *"Documento de investigación y recomendaciones"* with Hallazgos and
  Recomendaciones; an audit that stops at findings is the default in a costume.

Recorded for honesty: the demand ledger has "SQL y bases de datos" at severity
*alta*, but from **one** analysis out of three ever run, and from a Data
Scientist posting rather than the non-technical learner this course targets.
Build threshold is 3 and nothing has reached it. The ledger neither supports nor
refutes this course; there is not enough traffic for it to mean anything yet.

---

## Prompt 1 — the environment probe (run first, ~15 minutes)

```
Necesito decidir UNA herramienta donde una persona SIN experiencia técnica en
América Latina pueda LEER, EJECUTAR y (en menor medida) ESCRIBIR SQL de verdad.
Necesito la decisión respaldada, no una lista de opciones.

Contexto duro, no negociable:
- Estudia principalmente en un TELÉFONO Android de gama media, con datos móviles
  medidos. Puede tener acceso ocasional a un computador, pero no se asume.
- No tiene tarjeta de crédito. No puede instalar software. No puede pedirle
  permiso a un área de TI.
- Su idioma es español. Un registro sólo en inglés es fricción real.
- Va a volver a la misma herramienta ~30 veces durante semanas. Tiene que poder
  RECUPERAR su trabajo anterior.

El uso NO es parejo, y esto cambia qué herramienta gana:
- En 4 de 5 módulos el alumno sobre todo ABRE una consulta ya escrita, la
  ejecuta, mira el resultado y juzga si está bien. Eso tiene que ser cómodo en
  un teléfono.
- En 1 de 5 módulos el alumno ESCRIBE sus propias consultas. Ahí un teclado
  físico es aceptable y esperable.
Prioriza en ese orden: leer y ejecutar en teléfono pesa más que escribir cómodo.

Evalúa candidatos reales y verifica cada afirmación visitando la herramienta o
su documentación oficial en 2026. Incluye al menos: SQLite en el navegador
(sql.js, SQLime y similares), DB Fiddle, SQLite Online, el sandbox de Google
BigQuery, el plan gratuito de Supabase, Neon, la función QUERY() de Google
Sheets, y cualquier otra que descubras.

Para CADA candidato, con evidencia y fecha de consulta:
1. ¿Se puede LEER y EJECUTAR una consulta cómodamente en un navegador móvil?
   Dilo tras revisarlo. Si la interfaz existe pero es inusable con teclado en
   pantalla, dilo con esas palabras.
2. ¿Se puede COMPARTIR una consulta por enlace, para que la lección le entregue
   al alumno una consulta lista para abrir y correr? Esto vale mucho: es como
   funcionan 4 de los 5 módulos.
3. ¿Se pueden ver DOS resultados y compararlos — la consulta original y la
   corregida — sin perder la primera? El módulo de verificación lo necesita.
4. ¿Exige registro? ¿Tarjeta? ¿Está el registro en español?
5. ¿El trabajo persiste entre sesiones y entre dispositivos? ¿Cómo?
6. ¿Puede cargar SUS PROPIOS datos, un CSV exportado de una planilla, con
   columnas sucias — nombres con espacios y acentos, fechas en formatos
   mezclados, celdas vacías? Cuántos pasos toma en un teléfono. Esto importa
   más que en un curso normal: el curso es una AUDITORÍA y necesita datos
   reales y desordenados para auditar.
7. ¿Qué dialecto es y en qué se aparta del estándar en lo que un principiante
   toca primero: fechas, concatenación, LIMIT, comillas, NULL?
8. Límites del plan gratuito que muerden dentro de 30 lecciones: pausa por
   inactividad, cuota, expiración del proyecto.

Termina con:
- UNA recomendación principal y por qué gana en términos de esas restricciones.
- UN respaldo para cuando la principal falle.
- La respuesta honesta: ¿qué módulos se pueden hacer enteros desde un teléfono y
  cuáles piden un teclado? Quiero poder decirlo en la portada.
- Si ninguna opción sirve en teléfono, dilo. Es un resultado válido y cambia el
  diseño del curso.
```

---

## Prompt 2 — the canonical document (paste Prompt 1's answer into it)

```
Escribe el documento canónico de investigación para un curso de SQL de 30
lecciones, en español de América Latina. Este documento es la ÚNICA fuente de
verdad desde la que se generará el curso completo: temario, guiones, guías
escritas, ejercicios y retos. Lo que no esté aquí no existirá en el curso.

Extensión objetivo: 8.000-12.000 palabras. Markdown, UTF-8 limpio.

=== LA TESIS DEL CURSO (no la negocies, constrúyela) ===
Este NO es un curso de sintaxis. La sintaxis de SQL se aprende en una tarde y
hoy una IA escribe una consulta competente en tres segundos. Lo que sigue siendo
escaso es saber si esa consulta responde la pregunta que de verdad se hizo.

La gente no fracasa en SQL por la sintaxis. Fracasa porque el modelo mental está
mal: piensa en bucles cuando SQL piensa en conjuntos, lee NULL como cero cuando
significa desconocido, y no nota que un GROUP BY cambió qué representa una fila.
El ejemplo canónico: SQL se ESCRIBE SELECT → FROM → WHERE pero se EJECUTA FROM →
WHERE → GROUP BY → HAVING → SELECT → ORDER BY. Enseñar bien ese solo hecho
disuelve la mitad de la confusión de un principiante.

Por eso el curso es de COMPRENSIÓN, y su prueba es una AUDITORÍA.

=== EL ENTREGABLE (a esto llega todo) ===
El alumno termina con una «Auditoría de datos» sobre SU propio negocio,
organización o trabajo. No es un informe de opiniones: contiene las consultas.
Sus secciones son:
  1. Resumen ejecutivo: qué se auditó y qué se encontró.
  2. Las preguntas del negocio, definidas con precisión (grano, población,
     ventana temporal, fuente).
  3. Las fuentes de datos y el estado real en que están.
  4. Hallazgos: dónde los números están mal y POR QUÉ, con la consulta que lo
     demuestra.
  5. Las consultas verificadas que sí responden cada pregunta.
  6. Salvedades: qué NO se puede afirmar con estos datos.
  7. Recomendaciones y próximos pasos.

Un hallazgo es la unidad del documento. Define en el documento qué hace que un
hallazgo esté completo: la afirmación, la consulta que la sostiene, el número,
la causa, y qué decisión cambia. Sin eso el curso produce opiniones con SQL
decorativo.

=== QUIÉN APRENDE (no lo suavices) ===
Adulto hispanohablante en LatAm que quiere emplearse o hacer crecer su negocio.
NO es programador y probablemente nunca lo será. Sabe usar una planilla. Estudia
en un teléfono, en ratos robados alrededor de un trabajo. Cree que esto no es
para él.

=== LA HERRAMIENTA (decidida, no abierta) ===
[PEGA AQUÍ LA RECOMENDACIÓN DE LA PROMPT 1]

Todo el documento asume esa herramienta y ese dialecto. Cuando algo cambie en
otro dialecto habitual (PostgreSQL, MySQL, BigQuery, SQLite), ponlo en una tabla
de divergencias en vez de escribir SQL neutro que no corre en ninguna parte.

=== TRES RESTRICCIONES DEL FORMATO QUE CAMBIAN LO QUE DEBES ESCRIBIR ===

1. CADA LECCIÓN ES UN VIDEO DE 45-60 SEGUNDOS CON VOZ SINTÉTICA, más una guía
   escrita. La voz lee el guion en voz alta y el SQL NO SE NARRA: «SELECT
   asterisco FROM ventas WHERE fecha_compra mayor o igual» es ruido. Los guiones
   se rechazan automáticamente si contienen guiones bajos, asteriscos,
   backticks, corchetes, llaves, pipes o flechas.
   Para CADA lección entrega dos cosas separadas:
   - EL NÚCLEO HABLADO: la idea en palabras, sin sintaxis. Qué pregunta
     responde, con qué analogía, y qué error de fondo corrige. Debe entenderse
     escuchándolo sin ver nada.
   - LA SINTAXIS ESCRITA: la consulta real, completa y ejecutable, que vive en
     la guía y NUNCA en el guion.
   Esta separación es más fácil en este curso que en uno de sintaxis, porque el
   núcleo hablado casi siempre es un concepto. Aprovéchalo.

2. EL ALUMNO ELIGE UN PROYECTO REAL EN LA LECCIÓN 1 y todos los ejercicios se
   hacen sobre él. La evaluación puntúa «Aplicación» con 40 de 100 y mide qué
   tan anclado está el trabajo en su contexto propio; genérico se topa en 15.
   Un curso de auditoría necesita algo que auditar. Resuelve explícitamente cómo
   en la lección 1 el alumno termina con datos REALES, SUYOS y DESORDENADOS
   dentro de la herramienta: su planilla de ventas, su inventario, sus pedidos
   de WhatsApp, la exportación de su tienda, el registro de su organización.
   Entrega los pasos exactos en un teléfono. Da también un camino de respaldo
   para quien de verdad no tenga datos, sin que sea «usa esta tienda ficticia»,
   que destruye la Aplicación — piensa en datos públicos reales de LatAm que la
   persona pueda adoptar como propios y defender.

3. CADA MÓDULO TERMINA EN UN RETO: un caso NUEVO que las lecciones no cubrieron.
   En un curso de auditoría el reto natural es «aquí hay un reporte y un número
   sospechoso; encuentra qué está mal». Entrega las 5 semillas.

=== ARQUITECTURA DE CINCO MÓDULOS (respétala) ===

Módulo 1 — Qué pregunta pueden responder los datos.
  Casi sin SQL. Grano, población, ventana temporal, fuente. Por qué una
  pregunta mal hecha no tiene respuesta correcta. El alumno carga sus datos.

Módulo 2 — Leer antes de escribir.
  Se le da una consulta y dice qué devuelve. Conjuntos y no bucles. Orden
  escrito contra orden de ejecución. Al terminar lee SQL ajeno sin escribirlo.

Módulo 3 — Escribe las tuyas.
  El módulo de producción, el único que pide teclado. Escribe las consultas que
  responden SUS preguntas. Menos conceptos nuevos, más ejecución.

Módulo 4 — Cuando el número está mal. ES EL CORAZÓN DEL CURSO.
  NULL y aritmética con desconocidos; JOIN que multiplica filas (fan-out);
  GROUP BY que cambia el grano sin avisar; duplicados; zonas horarias; filtros
  que excluyen NULL sin querer; COUNT sobre columnas con vacíos; promedios de
  promedios. Este módulo merece la sección más larga del documento y el
  catálogo más completo de fallas reales.

Módulo 5 — Verifica lo que te dio la máquina.
  El alumno usará una IA para redactar consultas: el producto lo permite
  explícitamente y evalúa que el trabajo sea suyo, no quién escribió el primer
  borrador. Enseña a verificar: contrastar contra un total conocido, probar con
  un caso extremo, revisar el grano, comparar dos formulaciones de la misma
  pregunta. Cierra la auditoría y sus salvedades.

Para CADA módulo entrega: prerrequisitos reales; «qué logra quien sólo hace este
módulo» como contrato de resultado verificable en segunda persona (las rutas del
sistema seleccionan módulos sueltos, así que cada uno debe valer solo); de qué
otros dominios es prerrequisito; y la tabla lección por lección con propósito,
núcleo hablado y consulta escrita.

=== JERARQUÍA DE EVIDENCIA (márcala en todo el documento) ===
[P] Documentación oficial (el estándar SQL, docs de SQLite/PostgreSQL/BigQuery/
    MySQL) o investigación con método reproducible.
[S] Fuente secundaria respetada, identificando quién la publica.
[X] Folclore sin procedencia. Se descarta y se NOMBRA como folclore.

Dedica una sección a matar reglas repetidas que son falsas o dependientes del
contexto, con evidencia: «SELECT * siempre es malo», «los subqueries siempre son
más lentos que los JOIN», «los índices siempre aceleran», «NULL es igual a
NULL», «COUNT(*) es más lento que COUNT(1)», «hay que escribir las palabras
clave en mayúscula», y las que encuentres circulando en tutoriales en español.

=== SECCIONES OBLIGATORIAS ADICIONALES ===

A. Encabezado: fecha del documento, fecha de consulta de la documentación
   oficial, alcance, herramienta y dialecto admitidos, y qué NO se enseña.

B. El diccionario canónico: tabla, fila, columna, clave, grano, JOIN y sus
   tipos, NULL, agregación, GROUP BY, HAVING, subconsulta, índice, transacción.
   Cada uno con qué decisión habilita, con qué se confunde y el error típico.

C. Mensajes de error LITERALES de la herramienta elegida, qué los causa de
   verdad y cómo se arreglan. Un principiante pasa más tiempo con errores que
   con consultas correctas: esto es material de lección, no un apéndice.
   Parafrasear los mensajes es peor que omitirlos.

D. Catálogo de números mal leídos: casos reales y reproducibles donde una
   consulta que corre sin error devuelve un resultado incorrecto. Es la materia
   prima del módulo 4 y de los retos.

E. El laboratorio encadenado: cómo las 30 lecciones construyen la auditoría,
   lección por lección.

F. Estructuras listas para diagramar (el compilador genera Mermaid desde este
   texto): relaciones entre tablas, tipos de JOIN, orden de ejecución de una
   consulta, y el árbol de decisión «qué cláusula necesito».

G. Semillas de ejercicio, al menos una por lección, en la forma «el alumno
   produce X sobre SUS datos». En los módulos 1, 2, 4 y 5 la forma natural es
   «juzga, encuentra, explica o verifica», no «escribe una consulta».

H. Qué NO cubre el curso, con nombre y apellido: optimización interna del motor,
   administración de bases de datos, modelado dimensional a escala,
   procedimientos almacenados, concurrencia y transacciones en profundidad,
   funciones de ventana si decides dejarlas fuera. El producto promete decir lo
   que no enseña; esta sección es la fuente de esa promesa.

I. Qué significa «proficiente» al terminar, en tareas concretas, y el techo
   honesto de 30 lecciones. Incluye la respuesta honesta a: ¿esta persona pasa
   una prueba técnica de SQL en una entrevista? Si la respuesta es «sólo
   parcialmente», dilo y di qué le faltaría.

J. Bibliografía clasificada con [P]/[S]/[X] y fecha de consulta.

=== REGLAS DE ESCRITURA ===
- Español LatAm, de tú. Sin españolismos.
- Nada de «en el mundo actual» ni introducciones que no informan.
- Ninguna cifra sin fuente. Si no encuentras un dato con procedencia, dilo en
  vez de inventar un promedio de la industria.
- Toda consulta de ejemplo debe ser ejecutable tal cual en la herramienta
  elegida, sobre datos que el documento describe.
```

---

## What to check when it comes back

`preflight` catches encoding, length and wiring. It cannot catch a weak
document, and a bad one costs thirty lessons of drift — re-running is not a fix.

- **Is module 4 the longest section?** If the failure catalogue is thin, the
  course is a syntax course wearing an audit's clothes.
- **Does lesson 1 end with the learner's own messy data loaded?** No data, no
  audit, and Aplicación scores 15 for thirty lessons.
- **Does every lesson have a spoken core free of syntax?** If not,
  `check-narration` fails the build and the videos are unlistenable.
- **Are the error messages literal?** Paraphrased ones do not match what the
  learner sees.
- **Is a "finding" defined?** Without the claim / query / number / cause /
  decision structure, the deliverable is opinions with decorative SQL — and
  indistinguishable from `PROJECT_TEMPLATES`' default.
- **Did it kill the folklore or repeat it?** "Always avoid SELECT *" with no
  source means `[X]` was smuggled in as `[P]`.

## Before generating

Add the `PROJECT_TEMPLATES` entry for `curso-sql` in `cloud/writer.py` with the
seven sections above — the skill is explicit that without one the course
silently ships the default template. Pick an unused voice; note that
`es-CO-SalomeNeural-Female` is currently shared by three courses, so preflight's
uniqueness check would flag it.
