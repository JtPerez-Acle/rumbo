# Deep-research prompts — curso de SQL

Kept beside the output it produces, so the next course can copy the shape and so
anyone can see what the document was *asked* for when judging what it delivered.

Run **Prompt 1 first**. Its answer is pasted into Prompt 2. They are split
because the environment decision is load-bearing for all thirty lessons and is
cheap to get wrong: if the tool a learner is told to use needs a credit card, a
desktop install, or an English-only signup, the whole document is built on sand.

Target file: `studio/research/sql.md` · slug `curso-sql` ·
category `Analítica y automatización` (already has two courses, so it is not a
one-course category).

---

## Prompt 1 — the environment probe (run first, ~15 minutes)

```
Necesito decidir UNA herramienta donde una persona SIN experiencia técnica en
América Latina pueda escribir y ejecutar SQL de verdad, y necesito la decisión
respaldada, no una lista de opciones.

Contexto duro, no negociable:
- La persona estudia principalmente en un TELÉFONO Android de gama media, con
  datos móviles medidos. Puede tener acceso ocasional a un computador, pero no
  se puede asumir.
- No tiene tarjeta de crédito. No puede instalar software. No puede pedirle
  permiso a un área de TI.
- Su idioma es español. Un registro sólo en inglés es fricción real, no un
  detalle.
- Va a volver a la misma herramienta ~30 veces a lo largo de semanas. Tiene que
  poder RECUPERAR su trabajo anterior, no empezar de cero cada vez.

Evalúa candidatos reales y verifica cada afirmación visitando la herramienta o
su documentación oficial en 2026. Incluye al menos: SQLite ejecutado en el
navegador (sql.js / SQLime / similares), DB Fiddle, SQLite Online, el sandbox de
Google BigQuery, el plan gratuito de Supabase, Neon, la función QUERY() de
Google Sheets, y cualquier otra que descubras y cumpla las condiciones.

Para CADA candidato responde con evidencia y fecha de consulta:
1. ¿Funciona de verdad en un navegador móvil? Dilo tras revisarlo, no por
   suposición. Si la interfaz existe pero es inusable con teclado en pantalla,
   dilo con esas palabras.
2. ¿Exige registro? ¿Exige tarjeta? ¿Está el registro disponible en español?
3. ¿El trabajo persiste entre sesiones y entre dispositivos? ¿Cómo?
4. ¿Qué dialecto de SQL es y en qué se aparta del estándar en lo que un
   principiante toca primero (tipos de fecha, concatenación, LIMIT/TOP,
   comillas)?
5. ¿Puede la persona cargar SUS PROPIOS datos — un CSV exportado de una planilla
   — y cuántos pasos toma en un teléfono?
6. Límites del plan gratuito que muerden dentro de un curso de 30 lecciones
   (pausa por inactividad, cuota, expiración del proyecto).

Termina con:
- UNA recomendación principal y por qué gana, en términos de las restricciones
  de arriba y no de features.
- UN respaldo, para cuando la principal falle.
- La respuesta honesta a esta pregunta: ¿este curso se puede hacer ENTERO desde
  un teléfono, o hay que decirle al alumno por adelantado que necesita un
  computador para algunas lecciones? Prefiero saberlo ahora y decirlo en la
  portada que descubrirlo con alumnos adentro.
- Si tu conclusión es que ninguna opción es buena en teléfono, dilo. Es un
  resultado válido y cambia el diseño del curso.
```

---

## Prompt 2 — the canonical document (paste Prompt 1's answer into it)

```
Escribe el documento canónico de investigación para un curso de SQL de 30
lecciones, en español de América Latina. Este documento es la ÚNICA fuente de
verdad desde la que se generará el curso completo: temario, guiones, guías
escritas, ejercicios y retos. Lo que no esté aquí, no existirá en el curso.

Extensión objetivo: 8.000-12.000 palabras. Los documentos buenos de este
catálogo van entre 45 y 75 KB. Markdown, UTF-8 limpio, sin bytes inválidos.

=== QUIÉN APRENDE (no lo suavices) ===
Adulto hispanohablante en LatAm que quiere emplearse o hacer crecer su negocio.
NO es programador y probablemente nunca lo será. Sabe usar una planilla. Estudia
en un teléfono, con datos móviles, en ratos robados alrededor de un trabajo.
Llega con una meta ("quiero ser analista de datos", "quiero entender mis
ventas"), no con curiosidad por las bases de datos.

Su punto de partida real es: nunca ha escrito una línea de código y cree que
esto no es para él. El curso tiene que llevarlo de ahí a escribir consultas que
respondan preguntas de negocio reales, con criterio para saber cuándo el
resultado está mal.

=== LA HERRAMIENTA (decidida, no abierta) ===
[PEGA AQUÍ LA RECOMENDACIÓN DE LA PROMPT 1]

Todo el documento asume esa herramienta y ese dialecto. Cuando algo cambie en
otro dialecto habitual (PostgreSQL, MySQL, BigQuery, SQLite), señálalo en una
tabla de divergencias en vez de escribir SQL neutro que no corre en ninguna
parte.

=== TRES RESTRICCIONES DEL FORMATO QUE CAMBIAN LO QUE DEBES ESCRIBIR ===

1. CADA LECCIÓN ES UN VIDEO DE 45-60 SEGUNDOS CON VOZ SINTÉTICA, más una guía
   escrita. La voz lee el guion en voz alta. El SQL NO SE NARRA: "SELECT
   asterisco FROM ventas WHERE fecha_compra mayor o igual" es ruido, no
   enseñanza. Los guiones se rechazan automáticamente si contienen guiones
   bajos, asteriscos, backticks, corchetes, llaves, pipes o flechas.
   Por lo tanto, para CADA lección entrega dos cosas separadas:
   - EL NÚCLEO HABLADO: la idea en palabras, sin sintaxis. Qué pregunta
     responde, con qué analogía, y cuál es el error de fondo que corrige. Debe
     poder leerse en voz alta y entenderse sin ver nada.
   - LA SINTAXIS ESCRITA: la consulta real, completa y ejecutable, que vive en
     la guía escrita y nunca en el guion.

2. EL ALUMNO ELIGE UN PROYECTO REAL EN LA LECCIÓN 1 y TODOS los ejercicios
   posteriores se hacen sobre él. La evaluación puntúa "Aplicación" con 40 de
   100 puntos y mide qué tan anclado está el trabajo en el contexto propio del
   alumno; un ejercicio genérico se topa en 15.
   Esto es un problema específico de un curso de SQL: alguien no técnico no
   tiene una base de datos. Resuélvelo explícitamente. Propón el mecanismo
   concreto por el que en la lección 1 el alumno termina con datos REALES y
   SUYOS dentro de la herramienta — sus ventas, su inventario, sus pedidos de
   WhatsApp, sus métricas exportadas, el registro de su organización — y el
   camino de respaldo para quien de verdad no tenga datos propios, sin que ese
   respaldo sea "usa esta base de datos de ejemplo de una tienda ficticia", que
   destruye la Aplicación. Incluye los pasos exactos en un teléfono.

3. CADA MÓDULO TERMINA EN UN RETO: un caso de negocio nuevo que las lecciones
   NO cubrieron, que obliga a transferir. Entrega la semilla de los 5 retos.

=== JERARQUÍA DE EVIDENCIA (márcala en todo el documento) ===
[P] Documentación oficial (el estándar SQL, docs de SQLite/PostgreSQL/BigQuery/
    MySQL), o investigación con método reproducible.
[S] Fuente secundaria respetada, identificando quién la publica.
[X] Folclore sin procedencia. Se descarta y se NOMBRA como folclore.

Este dominio está lleno de reglas repetidas que son falsas o dependen del
contexto. Dedica una sección a matarlas con evidencia, incluyendo al menos:
"SELECT * siempre es malo", "los subqueries siempre son más lentos que los
JOIN", "los índices siempre aceleran", "NULL es igual a NULL", "COUNT(*) es más
lento que COUNT(1)", "hay que usar mayúsculas para las palabras clave", y
cualquier otra que encuentres circulando en tutoriales en español.

=== ESTRUCTURA OBLIGATORIA DEL DOCUMENTO ===

A. Encabezado: fecha del documento, fecha de consulta de la documentación
   oficial, alcance, herramienta y dialecto admitidos, y lo que explícitamente
   NO se enseña.

B. Cinco bloques de seis lecciones. Para CADA bloque:
   - Prerrequisitos reales.
   - "Qué logra quien sólo hace este bloque" — un contrato de resultado, en
     segunda persona, verificable. Las rutas del sistema seleccionan módulos
     sueltos, así que un bloque tiene que valer por sí solo.
   - De qué otros dominios es prerrequisito este bloque.
   - Tabla lección por lección: propósito, el núcleo hablado, y la consulta
     escrita.

C. El diccionario canónico: cada concepto (tabla, fila, columna, clave, JOIN,
   NULL, agregación, GROUP BY, subconsulta, índice, transacción...) definido de
   forma que otro curso pueda citarlo sin reescribirlo. Qué decisión habilita,
   con qué se confunde, y el error típico.

D. Errores reales y sus mensajes. Un principiante pasa más tiempo con errores
   que con consultas correctas. Recoge los mensajes de error LITERALES más
   frecuentes de la herramienta elegida, qué los causa de verdad, y cómo se
   arreglan. Esto es material de lección, no un apéndice.

E. El laboratorio encadenado: cómo las 30 lecciones construyen UN entregable
   acumulativo sobre el proyecto del alumno, lección por lección.

F. Estructuras listas para diagramar. El compilador genera diagramas Mermaid
   desde este texto: entrega relaciones entre tablas, tipos de JOIN, orden de
   ejecución de una consulta, y el árbol de decisión "qué cláusula necesito".

G. Semillas de ejercicio: al menos una por lección, en la forma "el alumno
   produce X sobre SUS datos", no "resuelve este ejercicio de práctica".

H. Los cinco retos de módulo.

I. Qué NO cubre este curso, dicho con nombre y apellido: optimización interna
   del motor, administración de bases de datos, modelado dimensional a escala,
   procedimientos almacenados, concurrencia, y lo que decidas dejar fuera. El
   producto promete decir lo que no enseña; esta sección es la fuente de esa
   promesa.

J. Qué significa "proficiente" al terminar, en tareas concretas que la persona
   podrá hacer, y el techo honesto de 30 lecciones.

K. Bibliografía clasificada con [P]/[S]/[X] y fecha de consulta.

=== REGLAS DE ESCRITURA ===
- Español LatAm, de tú. Sin españolismos.
- Nada de "en el mundo actual", "en la era de los datos", ni introducciones que
  no informan.
- Ninguna cifra sin fuente. Si no encuentras un dato con procedencia, dilo en
  vez de inventar un promedio de la industria.
- Toda consulta de ejemplo debe ser ejecutable tal cual en la herramienta
  elegida, sobre datos que el documento describe.
```

---

## What to check when it comes back

`preflight` catches encoding and length. It cannot catch a weak document, so
read for these before generating — a bad research doc costs thirty lessons of
drift, and re-running is not a fix:

- **Is the tool decision real?** If Prompt 1 concluded a phone cannot do this,
  that belongs on the course card and in `course_brief`, not discovered later.
- **Does lesson 1 end with the learner's own data loaded?** If not, Aplicación
  scores 15 for thirty lessons and the deliverable has nothing to be about.
- **Is there a spoken core for every lesson, free of syntax?** If the document
  only has SQL, `check-narration` will fail the build and the videos will be
  unlistenable.
- **Are the error messages literal?** Paraphrased errors do not match what the
  learner sees, which is worse than omitting them.
- **Did it kill the folklore, or repeat it?** A document that says "always avoid
  SELECT *" without a source has smuggled `[X]` in as `[P]`.
