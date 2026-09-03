# Documento canónico de investigación — Curso de SQL en 30 lecciones (LatAm, 2026)

> Fuente única de verdad. Lo que no está aquí no existe en el curso.

## A. Encabezado y alcance

- **Fecha del documento:** 3 de septiembre de 2026.
- **Fecha de consulta de la documentación oficial:** 3 de septiembre de 2026 (SQLite en sqlite.org; portales de datos abiertos con fecha propia en cada ficha).
- **Herramienta admitida:** sqliteonline.com (SQL Online IDE). Planes B: Sqlime (sqlime.org) y Datasette Lite (lite.datasette.io). Decisión heredada de la investigación previa; no se re-litiga.
- **Dialecto admitido:** SQLite 3.50.x (el motor que corre sqliteonline.com). La versión estable más reciente de SQLite es 3.53.4, publicada el 24 de julio de 2026, según sqlite.org [P]. Nota de contexto: la versión 3.52.0 fue retirada por el proyecto y reemplazada por el parche 3.51.3, de modo que la línea 3.53.x es la vigente; el curso, en todo caso, fija su suelo de compatibilidad en 3.50.x, la versión que corre la herramienta. Toda consulta del curso debe correr tal cual en 3.50.x.
- **Idioma:** español de América Latina, de tú, sin españolismos.
- **Qué es este curso:** un curso de COMPRENSIÓN cuya prueba es una AUDITORÍA de datos reales del propio alumno.
- **Qué NO es:** un curso de sintaxis, de administración de bases de datos, de optimización de motores, ni de programación. Ver sección H para el detalle con nombre y apellido.

### La tesis, en una frase
La sintaxis de SQL se aprende en una tarde y una IA escribe una consulta competente en segundos. Lo escaso es saber si esa consulta responde la pregunta que de verdad se hizo. La gente no fracasa por la sintaxis: fracasa porque el modelo mental está mal. Piensa en bucles cuando SQL piensa en conjuntos; lee NULL como cero cuando significa desconocido; no nota que un GROUP BY cambió qué representa una fila. El hecho canónico que disuelve la mitad de la confusión: SQL se ESCRIBE SELECT → FROM → WHERE pero se EJECUTA FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY.

### El entregable final: la Auditoría de datos
El alumno termina con una «Auditoría de datos» sobre su propio negocio, organización o trabajo, que contiene las consultas. Sus siete secciones:
1. Resumen ejecutivo: qué se auditó y qué se encontró.
2. Las preguntas del negocio, definidas con precisión (grano, población, ventana temporal, fuente).
3. Las fuentes de datos y su estado real.
4. Hallazgos: dónde los números están mal y por qué, con la consulta que lo demuestra.
5. Las consultas verificadas que responden cada pregunta.
6. Salvedades: qué NO se puede afirmar con estos datos.
7. Recomendaciones y próximos pasos.

**Qué hace que un hallazgo esté completo (la unidad del documento).** Un hallazgo tiene cinco partes obligatorias: (1) la afirmación en una frase; (2) la consulta que la sostiene, ejecutable; (3) el número que arroja; (4) la causa —por qué el dato estaba mal o por qué la respuesta ingenua engañaba—; (5) qué decisión cambia. Sin las cinco partes es una opinión con SQL decorativo, no un hallazgo.

## B. El diccionario canónico

Cada término trae: qué decisión habilita, con qué se confunde y el error típico.

- **Tabla.** Una colección de filas con las mismas columnas. *Habilita:* nombrar dónde viven los datos. *Se confunde con:* una planilla (una planilla mezcla varias tablas y notas en una hoja). *Error típico:* meter dos cosas distintas —ventas y clientes— en una sola tabla ancha.
- **Fila.** Una observación: un pedido, una persona, un día. *Habilita:* definir el grano. *Se confunde con:* «un registro visual» en la planilla. *Error típico:* creer que una fila siempre es «una venta» cuando tras un JOIN puede ser «una línea de venta».
- **Columna.** Un atributo con un tipo (o afinidad, en SQLite). *Habilita:* elegir qué medir. *Se confunde con:* una celda. *Error típico:* asumir que una columna «monto» es numérica cuando entró como texto.
- **Clave.** Columna(s) que identifican una fila (clave primaria) o que apuntan a otra tabla (clave foránea). *Habilita:* unir tablas sin duplicar. *Se confunde con:* un simple número de orden. *Error típico:* unir por una clave no única y multiplicar filas.
- **Grano.** Qué representa exactamente una fila del resultado. *Habilita:* saber si SUM y COUNT significan lo que crees. *Se confunde con:* el número de filas. *Error típico:* sumar sobre un grano que un JOIN o un GROUP BY ya cambió.
- **JOIN y sus tipos.** Combinar filas de dos tablas por una condición. `INNER JOIN` conserva solo las coincidencias; `LEFT JOIN` conserva todas las filas de la izquierda y rellena con NULL lo que no casa; `CROSS JOIN` combina todo con todo. *Habilita:* traer atributos de otra tabla. *Se confunde con:* pegar columnas lado a lado. *Error típico:* el fan-out (una fila de la izquierda casa con varias de la derecha y los totales se inflan).
- **NULL.** Marcador de valor desconocido o ausente, no un cero ni un texto vacío. *Habilita:* representar «no sabemos». *Se confunde con:* cero o cadena vacía. *Error típico:* filtrar con `= NULL` (nunca es verdadero) en vez de `IS NULL`.
- **Agregación.** Colapsar muchas filas en un resumen: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. *Habilita:* pasar de detalle a total. *Se confunde con:* un cálculo fila por fila. *Error típico:* creer que `AVG` ignora los ceros (ignora los NULL, no los ceros).
- **GROUP BY.** Parte las filas en grupos y calcula una agregación por grupo. *Habilita:* «por cliente», «por mes». *Se confunde con:* ordenar. *Error típico:* cambiar el grano sin darse cuenta y luego leer mal el resultado.
- **HAVING.** Filtra grupos después de agregar. *Habilita:* «solo los meses con más de 100 ventas». *Se confunde con:* WHERE. *Error típico:* poner una condición de agregado en WHERE (error de «misuse of aggregate»).
- **Subconsulta.** Una consulta dentro de otra. *Habilita:* calcular por pasos, agregar antes de unir. *Se confunde con:* que siempre es más lenta que un JOIN (folclore [X], ver sección de mitos). *Error típico:* subconsultas correlacionadas innecesarias.
- **Índice.** Estructura que acelera la búsqueda por ciertas columnas. *Habilita:* que una búsqueda no recorra toda la tabla. *Se confunde con:* «siempre acelera todo». *Error típico:* creer que un índice arregla cualquier lentitud (irrelevante en un curso de auditoría con datos pequeños; se menciona, no se practica).
- **Transacción.** Un grupo de cambios que ocurren todos o ninguno. *Habilita:* no dejar los datos a medias. *Se confunde con:* una consulta cualquiera. *Error típico:* no aplica a este curso (solo lectura); se nombra y se deja fuera (sección H).

## C. Mensajes de error literales de SQLite

Un principiante pasa más tiempo con errores que con consultas correctas. Estos son los textos exactos que produce SQLite; parafrasearlos sería peor que omitirlos. Verificados contra la documentación y el foro oficial de sqlite.org [P]. Advertencia de los propios desarrolladores de SQLite: no escribas programas que dependan del texto exacto, porque puede cambiar entre versiones; para aprender a leerlos, en cambio, el texto exacto es justo lo que necesitas.

- **`no such column: X`** — SQLite no encontró ninguna columna con ese nombre. Causa real frecuente: un texto escrito con comillas dobles que SQLite interpretó como identificador. *Arreglo:* revisa el nombre; usa comillas simples para texto.
- **`no such table: X`** — la tabla o vista no existe en la base conectada. *Arreglo:* revisa que importaste el CSV y que el nombre coincide (mayúsculas incluidas).
- **`near "X": syntax error`** — el analizador chocó con el token X y no pudo seguir. Un token vacío aparece como `near "": syntax error`. *Arreglo:* mira justo antes de X (coma de más, paréntesis sin cerrar, palabra mal escrita).
- **`misuse of aggregate: COUNT()`** (forma moderna, con dos puntos; versiones muy viejas decían `misuse of aggregate function COUNT()`) — usaste un agregado donde no se permite, típicamente en WHERE. *Arreglo:* mueve la condición de agregado a HAVING. Nota: el texto exacto depende de la versión; en 3.50.x se usa la forma con dos puntos.
- **`UNIQUE constraint failed: tabla.columna`** — intentaste crear un valor duplicado en una columna única. *Arreglo:* en auditoría suele señalar que tus datos ya traen duplicados; investígalos.
- **`NOT NULL constraint failed: tabla.columna`** — intentaste dejar en NULL una columna declarada obligatoria. *Arreglo:* provee el valor o revisa la definición.
- **`datatype mismatch`** — caso estricto de SQLite; el más común es meter algo que no es entero en la columna rowid o INTEGER PRIMARY KEY. *Arreglo:* revisa el tipo de la clave.
- **`unrecognized token: "X"`** — el tokenizador halló un carácter que no es SQL válido (una comilla «inteligente» copiada del teléfono, un símbolo suelto). *Arreglo:* reescribe la comilla o el símbolo a mano.
- **`incomplete input`** — la sentencia quedó incompleta (falta un paréntesis, una comilla de cierre o el punto y coma final). *Arreglo:* cierra lo que abriste.

Estos ocho son el catálogo mínimo. Cada uno merece un momento de lección en el módulo correspondiente, no un apéndice.

## D. Catálogo de números mal leídos

Casos donde una consulta corre sin error y devuelve un número incorrecto. Es la materia prima del módulo 4 y de los retos. Cada caso: el síntoma, la causa y la verificación.

1. **NULL tratado como cero en una suma condicional.** Si sumas una columna con NULL creyendo que aporta cero, el total puede ser correcto (SUM ignora NULL) pero el promedio no: `AVG` divide por la cantidad de valores no nulos, no por el total de filas. Verificado contra la documentación de SQLite: los agregados salvo `count(*)` ignoran los NULL [P]. *Verificación:* compara `COUNT(*)` con `COUNT(columna)`; si difieren, hay NULL.
2. **Filtro que excluye NULL sin querer.** `WHERE estado <> 'cerrado'` NO devuelve las filas con estado NULL, porque `NULL <> 'cerrado'` es desconocido, no verdadero [P]. *Verificación:* suma las filas de `<> 'cerrado'` más las de `IS NULL` y compáralas con el total.
3. **`= NULL` no encuentra nada.** `WHERE columna = NULL` siempre devuelve cero filas aunque haya NULL. Hay que usar `IS NULL` [P]. *Verificación:* corre las dos y observa la diferencia.
4. **Fan-out por JOIN.** Un cliente con tres pedidos aparece tres veces tras el JOIN; sumar su saldo lo triplica. *Verificación:* `COUNT(*)` antes y después del JOIN; si crece, hubo multiplicación. Solución: agregar antes de unir con una subconsulta.
5. **GROUP BY que cambió el grano.** Tras agrupar, cada fila ya no es «una venta» sino «un mes»; sumar «cantidad de filas» ahora cuenta meses, no ventas. *Verificación:* pregúntate en voz alta «¿qué es una fila aquí?».
6. **COUNT sobre columna con vacíos.** `COUNT(telefono)` cuenta solo los teléfonos presentes; si el 20% está vacío, tu conteo es el 80% de las filas [P]. *Verificación:* contrástalo con `COUNT(*)`.
7. **División entera.** En SQLite `5 / 2` da `2`, no `2.5`, porque ambos son enteros; un porcentaje calculado así sale siempre con `.0`. Confirmado en el foro oficial de SQLite [P]. *Verificación:* fuerza real con `5 * 1.0 / 2`.
8. **Números que entraron como texto.** Tras importar un CSV, `'10'` como texto ordena antes que `'2'` y `SUM` puede tratar textos no numéricos como 0. `AVG` interpreta texto y BLOB no numéricos como cero [S, w3resource / SQLite Tutorial]. *Verificación:* `SELECT typeof(monto)`; si dice `text`, hay que convertir con `CAST`.
9. **Promedio de promedios.** Promediar los promedios diarios NO da el promedio del período si los días tienen distinto número de casos; el correcto es la suma total dividida por el total de casos. *Verificación:* compara `AVG` del detalle contra el promedio de los promedios; si difieren, tenías ponderaciones desiguales.
10. **Zonas horarias y fechas mezcladas.** SQLite guarda `'now'` en UTC por defecto; una venta de las 23:00 hora local puede caer «al día siguiente» en UTC, corriendo el conteo diario. Además, fechas en formatos mezclados (`31/01/2026` vs `2026-01-31`) rompen el orden. *Verificación:* revisa el formato con `SELECT DISTINCT` sobre la columna de fecha.
11. **Duplicados exactos.** Dos filas idénticas por una exportación repetida inflan todo. *Verificación:* `SELECT columnas, COUNT(*) ... GROUP BY columnas HAVING COUNT(*) > 1`.

## E. El laboratorio encadenado

Las 30 lecciones construyen la auditoría paso a paso. Cada lección aporta un ladrillo al documento final.

- **Lecciones 1–6 (Módulo 1):** el alumno carga sus datos reales y escribe las secciones 2 y 3 de la auditoría (preguntas con grano/población/ventana/fuente, y estado real de las fuentes).
- **Lecciones 7–13 (Módulo 2):** aprende a leer SQL ajeno; produce borradores de la sección 5 (consultas candidatas) sin escribirlas todavía, juzgando cuáles responden de verdad cada pregunta.
- **Lecciones 14–19 (Módulo 3):** escribe sus propias consultas; completa la sección 5 con consultas ejecutables.
- **Lecciones 20–26 (Módulo 4):** encuentra dónde los números están mal; llena la sección 4 (hallazgos) con las cinco partes obligatorias cada uno.
- **Lecciones 27–30 (Módulo 5):** verifica lo que le dio la IA, escribe la sección 6 (salvedades), la 1 (resumen ejecutivo) y la 7 (recomendaciones); entrega la auditoría.

## F. Estructuras listas para diagramar

Texto plano del que el compilador genera diagramas.

**Relaciones entre tablas (ejemplo del caso de ventas):**
- clientes (uno) se relaciona con pedidos (muchos) por id de cliente.
- pedidos (uno) se relaciona con lineas de pedido (muchos) por id de pedido.
- productos (uno) se relaciona con lineas de pedido (muchos) por id de producto.

**Tipos de JOIN:**
- INNER JOIN: solo filas que casan en ambas tablas.
- LEFT JOIN: todas las de la izquierda, más las que casan de la derecha, NULL donde no casa.
- CROSS JOIN: todas las combinaciones posibles.

**Orden de ejecución de una consulta:**
- Paso 1 FROM y JOIN: arma las filas.
- Paso 2 WHERE: filtra filas.
- Paso 3 GROUP BY: forma grupos.
- Paso 4 HAVING: filtra grupos.
- Paso 5 SELECT: calcula columnas y alias.
- Paso 6 ORDER BY: ordena.
- Paso 7 LIMIT: recorta.

**Árbol de decisión «qué cláusula necesito»:**
- ¿Quiero filtrar filas individuales? WHERE.
- ¿Quiero un resumen por categoría? GROUP BY con una agregación.
- ¿Quiero filtrar esos resúmenes? HAVING.
- ¿Quiero traer datos de otra tabla? JOIN.
- ¿Quiero ordenar el resultado? ORDER BY.
- ¿Quiero ver solo las primeras filas? LIMIT.

## G y arquitectura de los cinco módulos

Regla de guion para todo el curso: **el núcleo hablado no narra sintaxis**. Nada de guiones bajos, asteriscos, backticks, corchetes, llaves, pipes ni flechas en el audio. La consulta vive en la guía escrita. El núcleo hablado es un concepto; aprovéchalo. Cada video dura 45 a 60 segundos con voz sintética; la guía escrita acompaña con la sintaxis real y ejecutable.

### Módulo 1 — Qué pregunta pueden responder los datos
**Prerrequisitos reales:** saber usar una planilla; tener un teléfono Android; tener (o poder conseguir) datos propios.
**Qué logras si solo haces este módulo:** al terminar, sabes convertir una pregunta vaga («¿cómo va el negocio?») en una pregunta respondible (grano, población, ventana temporal, fuente), y tienes tus propios datos cargados en la herramienta, listos para consultar.
**Es prerrequisito de:** todos los demás módulos.

| Lección | Propósito | Núcleo hablado (sin sintaxis) | Consulta escrita (en la guía) |
|---|---|---|---|
| 1 | Elegir el proyecto y cargar datos reales | Todo el curso se hará sobre tus datos. Hoy los metes a la herramienta. | (Sin consulta: pasos de importación, ver más abajo.) |
| 2 | Qué es una tabla, fila, columna | Una tabla es una lista de cosas del mismo tipo; una fila es una de esas cosas. | `SELECT * FROM ventas LIMIT 10;` |
| 3 | El grano: qué es una fila | Antes de contar, pregúntate qué representa una fila. Si no lo sabes, cualquier número miente. | `SELECT COUNT(*) FROM ventas;` |
| 4 | Población y ventana temporal | Una pregunta sin «quiénes» y «cuándo» no tiene respuesta correcta. | `SELECT MIN(fecha_compra), MAX(fecha_compra) FROM ventas;` |
| 5 | La fuente y su estado real | De dónde salió el dato importa tanto como el dato. | `SELECT typeof(monto), COUNT(*) FROM ventas GROUP BY typeof(monto);` |
| 6 | Escribir las preguntas del negocio | Una buena pregunta ya trae adentro su grano, su población, su ventana y su fuente. | (Sin consulta: redacción de la sección 2.) |

**Semillas de ejercicio (juzga/define):** L1 «carga tus datos y describe en dos frases qué contiene cada tabla». L3 «define el grano de tu tabla principal y defiéndelo». L4 «escribe la ventana temporal exacta de tu auditoría». L6 «redacta tres preguntas de negocio respondibles sobre TUS datos».

### Módulo 2 — Leer antes de escribir
**Prerrequisitos reales:** módulo 1 (datos cargados).
**Qué logras si solo haces este módulo:** al terminar, tomas una consulta que te pasan y dices qué devuelve y sobre qué grano, sin escribirla tú; entiendes que SQL piensa en conjuntos y no en bucles, y por qué el orden en que se ejecuta no es el orden en que se escribe.
**Es prerrequisito de:** módulos 3, 4 y 5.

| Lección | Propósito | Núcleo hablado | Consulta escrita |
|---|---|---|---|
| 7 | Conjuntos, no bucles | SQL no recorre fila por fila como tú leerías; opera sobre el conjunto entero de una vez. | `SELECT ciudad, COUNT(*) FROM clientes GROUP BY ciudad;` |
| 8 | Orden escrito vs orden de ejecución | Lo escribes empezando por lo que quieres ver, pero la máquina empieza por dónde están los datos. | `SELECT ciudad, COUNT(*) FROM clientes WHERE activo = 1 GROUP BY ciudad;` |
| 9 | Leer un WHERE | Un WHERE decide qué filas entran; imagínalo como un portero. | `SELECT * FROM ventas WHERE monto > 1000;` |
| 10 | Leer un GROUP BY | Cuando ves agrupar, cada fila del resultado ya no es una venta: es un grupo. | `SELECT vendedor, SUM(monto) FROM ventas GROUP BY vendedor;` |
| 11 | Leer un JOIN | Un JOIN pega datos de otra tabla usando una clave en común. | `SELECT p.id, c.nombre FROM pedidos p JOIN clientes c ON p.id_cliente = c.id;` |
| 12 | Leer NULL en resultados | Una celda vacía puede ser un desconocido, no un cero. | `SELECT * FROM clientes WHERE telefono IS NULL;` |
| 13 | Decir qué devuelve una consulta | Antes de correr algo, di en voz alta qué esperas ver y con qué grano. | `SELECT strftime('%Y-%m', fecha_compra) AS mes, COUNT(*) FROM ventas GROUP BY mes;` |

**Semillas de ejercicio (juzga/encuentra):** L8 «te doy una consulta y dime qué paso ocurre primero». L10 «di cuál es el grano del resultado de esta consulta sobre TUS datos». L11 «predice cuántas filas devolverá este JOIN y verifica». L13 «lee esta consulta y escribe en una frase qué pregunta responde».

### Módulo 3 — Escribe las tuyas
**Prerrequisitos reales:** módulo 2 (leer SQL). **Recomendado teclado físico.**
**Qué logras si solo haces este módulo:** al terminar, escribes desde cero las consultas que responden tus propias preguntas de negocio: filtras, agrupas, unes dos tablas y ordenas.
**Es prerrequisito de:** módulos 4 y 5.

| Lección | Propósito | Núcleo hablado | Consulta escrita |
|---|---|---|---|
| 14 | Tu primer SELECT con filtro | Escribir es elegir qué columnas y qué filas. | `SELECT fecha_compra, monto FROM ventas WHERE monto >= 500;` |
| 15 | Tu primer GROUP BY | Agrupar es responder «por cada…». | `SELECT vendedor, SUM(monto) AS total FROM ventas GROUP BY vendedor ORDER BY total DESC;` |
| 16 | Filtrar grupos con HAVING | Cuando la condición es sobre el resumen, va después de agrupar. | `SELECT vendedor, COUNT(*) AS n FROM ventas GROUP BY vendedor HAVING n > 10;` |
| 17 | Tu primer JOIN | Unir es traer el nombre que vive en otra tabla. | `SELECT c.nombre, SUM(p.monto) AS total FROM clientes c JOIN pedidos p ON c.id = p.id_cliente GROUP BY c.nombre;` |
| 18 | Fechas como texto | En esta herramienta la fecha es texto; se corta y se agrupa como texto. | `SELECT strftime('%Y-%m', fecha_compra) AS mes, SUM(monto) FROM ventas GROUP BY mes ORDER BY mes;` |
| 19 | Convertir texto a número | Si el monto entró como texto, hay que forzarlo a número para sumarlo bien. | `SELECT SUM(CAST(monto AS REAL)) FROM ventas;` |

**Semillas de ejercicio (escribe):** L14 «escribe la consulta que responde tu pregunta 1». L15 «agrupa tus ventas por la categoría que más te importe». L17 «une tus dos tablas principales y explica el grano». L19 «convierte tu columna sospechosa y compara el total antes y después».

### Módulo 4 — Cuando el número está mal (el corazón del curso)
**Prerrequisitos reales:** módulos 2 y 3.
**Qué logras si solo haces este módulo:** al terminar, detectas y explicas las fallas silenciosas más comunes —consultas que corren sin error pero mienten— y las corriges: NULL en aritmética, fan-out de JOIN, cambios de grano, duplicados, COUNT sobre vacíos, división entera, promedios de promedios y fechas/zonas horarias.
**Es prerrequisito de:** módulo 5.

| Lección | Propósito | Núcleo hablado | Consulta escrita |
|---|---|---|---|
| 20 | NULL no es cero | Un desconocido contamina las cuentas; contar y promediar no lo tratan igual. | `SELECT COUNT(*), COUNT(telefono) FROM clientes;` |
| 21 | Filtros que botan los NULL | Cuando excluyes un valor, sin querer también excluyes los desconocidos. | `SELECT COUNT(*) FROM ventas WHERE estado <> 'cerrado'; SELECT COUNT(*) FROM ventas WHERE estado <> 'cerrado' OR estado IS NULL;` |
| 22 | El JOIN que multiplica | Si una fila casa con varias, tus totales se inflan sin avisar. | `SELECT COUNT(*) FROM pedidos; SELECT COUNT(*) FROM pedidos p JOIN lineas l ON p.id = l.id_pedido;` |
| 23 | Agregar antes de unir | Para no inflar, resume primero y une después. | `SELECT c.nombre, t.total FROM clientes c JOIN (SELECT id_cliente, SUM(monto) AS total FROM pedidos GROUP BY id_cliente) t ON c.id = t.id_cliente;` |
| 24 | Duplicados escondidos | A veces la misma fila entró dos veces por una exportación repetida. | `SELECT id_pedido, COUNT(*) AS n FROM pedidos GROUP BY id_pedido HAVING n > 1;` |
| 25 | División entera y promedios de promedios | Dividir enteros trunca; promediar promedios no da el promedio real. | `SELECT 100 * COUNT(*) / (SELECT COUNT(*) FROM ventas) AS mal, 100.0 * COUNT(*) / (SELECT COUNT(*) FROM ventas) AS bien FROM ventas WHERE monto > 1000;` |
| 26 | Fechas y zonas horarias | Una venta de la noche puede saltar de día si la hora está en otro huso. | `SELECT DISTINCT substr(fecha_compra, 1, 10) FROM ventas ORDER BY 1 LIMIT 20;` |

**Semillas de ejercicio (encuentra/explica):** L20 «encuentra una columna de TUS datos donde contar filas y contar valores difiera, y explica por qué». L22 «demuestra con una consulta si tu JOIN infla algún total». L24 «encuentra duplicados en tus datos y estima cuánto distorsionan». L25 «reconstruye un porcentaje tuyo mal calculado y arréglalo».

### Módulo 5 — Verifica lo que te dio la máquina
**Prerrequisitos reales:** módulos 3 y 4.
**Qué logras si solo haces este módulo:** al terminar, tomas una consulta escrita por una IA y la verificas —contra un total conocido, con un caso extremo, revisando el grano y comparando dos formulaciones— y cierras tu auditoría con salvedades honestas. El producto permite usar IA explícitamente; lo que se evalúa es que el trabajo y el juicio sean tuyos.
**Es prerrequisito de:** ninguno (cierra el curso).

| Lección | Propósito | Núcleo hablado | Consulta escrita |
|---|---|---|---|
| 27 | Contrastar contra un total conocido | Si conoces el total por otra vía, tu consulta debe reproducirlo. | `SELECT SUM(CAST(monto AS REAL)) FROM ventas;` |
| 28 | Probar con un caso extremo | Prueba con un cliente que sabes de memoria; si ahí falla, falla en todo. | `SELECT * FROM ventas WHERE id_cliente = 1 ORDER BY fecha_compra;` |
| 29 | Comparar dos formulaciones | Dos caminos a la misma pregunta deben dar el mismo número; si no, uno miente. | `SELECT COUNT(DISTINCT id_cliente) FROM pedidos; SELECT COUNT(*) FROM (SELECT DISTINCT id_cliente FROM pedidos);` |
| 30 | Salvedades y cierre de la auditoría | Decir qué NO puedes afirmar es parte del trabajo, no una debilidad. | (Sin consulta: redacción de las secciones 1, 6 y 7.) |

**Semillas de ejercicio (verifica):** L27 «pide a una IA una consulta para tu pregunta 2 y verifícala contra un total que ya conoces». L28 «rompe una consulta con un caso extremo de TUS datos». L29 «formula la misma pregunta de dos maneras y concilia los números». L30 «escribe tres salvedades reales de tu auditoría».

## Cómo la lección 1 termina con datos reales, suyos y desordenados

Pasos exactos en un teléfono Android, en sqliteonline.com:
1. Exporta tu planilla como CSV. En la app de Google Sheets: menú de tres puntos → Compartir y exportar → Guardar como → CSV. En Excel móvil: Archivo → Guardar como → tipo CSV. Si tus pedidos están en WhatsApp, pásalos primero a una planilla (una fila por pedido) y expórtala.
2. Abre sqliteonline.com en Chrome. No pide cuenta ni tarjeta. Su propia página lo declara textualmente en su meta-descripción: «No registration for start, No DownLoad, No Install» [P].
3. Toca el botón «Import» y elige tu archivo CSV desde el almacenamiento del teléfono.
4. Confirma el nombre de la tabla y ejecuta `SELECT * FROM tu_tabla LIMIT 10;` para ver que cargó.
5. Corre `SELECT typeof(columna) FROM tu_tabla LIMIT 5;` sobre tus columnas de monto y fecha. Si dice `text`, ya descubriste tu primer hallazgo: los números entraron como texto.

**Advertencia técnica verificada:** el `.import` de SQLite crea columnas de tipo TEXT cuando la tabla no existe todavía y no infiere tipos; hay que crear la tabla con tipos antes, o convertir después con CAST [P, foro y docs de SQLite]. En sqliteonline el botón «Import»/«Intelligent-Import» puede comportarse distinto; por eso la lección 1 incluye la comprobación con `typeof()` en vez de asumir. Si el import falla o confunde tipos en el teléfono, el plan de respaldo es entregar el dataset ya como base `.db` para abrir en Sqlime, o cargar el CSV por URL en Datasette Lite.

### Camino de respaldo con datos públicos reales de LatAm
Para quien de verdad no tenga datos propios, que adopte un conjunto público real como propio y lo defienda (nunca una «tienda ficticia», que destruye la Aplicación). Fuentes verificadas el 3 de septiembre de 2026, todas con descarga en CSV:
- **Chile — datos.gob.cl** (Portal de Datos Abiertos, Ministerio de Hacienda). El catálogo permite filtrar directamente por formato CSV. [P/S]
- **Colombia — datos.gov.co** (Datos Abiertos Colombia, MinTIC). [P/S]
- **México — datos.gob.mx** e **INEGI (inegi.org.mx/datosabiertos)**. [P/S]
- **Argentina — datos.gob.ar** (plataforma nacional CKAN). [P/S]
- **Perú — datosabiertos.gob.pe** y el portal del MEF (datosabiertos.mef.gob.pe). [P/S]

Cómo se descarga en el teléfono: abre el portal en Chrome, busca un conjunto (por ejemplo presupuesto municipal o vacunación), toca el recurso en formato CSV y descárgalo; luego súbelo con «Import» en sqliteonline. Estos datasets vienen desordenados de verdad (encabezados con acentos, fechas mezcladas, celdas vacías), que es justo lo que necesita una auditoría.

## Los cinco retos de fin de módulo

Cada módulo cierra con un caso NUEVO no cubierto en las lecciones. La forma canónica de la auditoría: «aquí hay un reporte y un número sospechoso; encuentra qué está mal».

1. **Reto módulo 1:** te doy un reporte de ventas con un total anual y su definición de «cliente activo». La definición no dice ventana temporal. Reescribe la pregunta para que tenga respuesta y di qué datos harían falta.
2. **Reto módulo 2:** te doy tres consultas que dicen responder «ventas del mes». Sin ejecutarlas, di cuál cambia el grano y por qué las tres pueden dar números distintos.
3. **Reto módulo 3:** te doy dos tablas y una pregunta de negocio. Escribe la consulta que la responde y justifica el grano del resultado.
4. **Reto módulo 4:** un tablero muestra «ingreso promedio por cliente = 1.240». Con los datos crudos, demuestra que el número está inflado por un JOIN y calcula el correcto.
5. **Reto módulo 5:** una IA entregó una consulta que «cuadra» con el total anual pero reparte mal por mes. Encuentra el error con un caso extremo y corrígelo.

## Matando reglas falsas (folclore [X] con evidencia)

- **«SELECT asterisco siempre es malo.»** [X] como regla absoluta. En producción conviene pedir solo las columnas necesarias por claridad y para que el motor use mejores índices [S, SQLShack]. Pero en una auditoría exploratoria en el teléfono, ver todo primero es correcto y útil. La regla real: pide todo para explorar, nombra columnas para entregar.
- **«Los subqueries siempre son más lentos que los JOIN.»** [X]. Los optimizadores suelen reescribir subconsultas no correlacionadas como JOIN. En una prueba publicada por Slava Rozhnev en DEV Community, ambas formas midieron alrededor de 1 ms en SQLite 3.45 —«SQLite 3.45: A Tie! Execution Times: Both ~1 ms… choose based on readability»— con planes de ejecución casi idénticos [S]. La regla real: elige por claridad; en datos pequeños da igual.
- **«Los índices siempre aceleran.»** [X]. Un índice acelera lecturas selectivas pero puede no usarse y añade costo a las escrituras; irrelevante en un curso de auditoría con datos chicos. La regla real: en este curso no vas a necesitar índices.
- **«NULL es igual a NULL.»** [X], y peligrosísimo. `NULL = NULL` da desconocido, no verdadero; hay que usar `IS NULL`. Confirmado en la documentación de SQLite y en el foro oficial [P].
- **«COUNT(asterisco) es más lento que COUNT(1).»** [X]. Es un mito viejo; los motores modernos tratan ambas formas igual y producen el mismo plan. Lukas Eder (jOOQ) lo resume: «One of the biggest and undead myths in SQL is that COUNT(*) is faster than COUNT(1)… there's really no reason at all why one should be faster than the other» [S]. La regla real: usa `COUNT(*)`, es lo más claro.
- **«Hay que escribir las palabras clave en mayúscula.»** [X] como obligación. SQL no distingue mayúsculas en las palabras clave; la mayúscula es estilo, no requisito [S]. La regla real: sé consistente; el curso las escribe en mayúscula por legibilidad.
- **«En SQLite las comillas dobles sirven para texto.»** [X] peligroso que circula en tutoriales. SQLite acepta comillas dobles como texto solo por compatibilidad histórica cuando no coinciden con un identificador, lo que esconde errores de tipeo [P, docs de SQLite]. La regla estricta del curso: texto = comilla simple.

## Tabla de divergencias entre dialectos

Cuando algo cambia respecto de otro motor habitual, va aquí en vez de escribir SQL neutro que no corre en ninguna parte. Curso: SQLite.

| Tema | SQLite (el curso) | PostgreSQL | MySQL | BigQuery |
|---|---|---|---|---|
| Concatenar texto | `a || b` | `a || b` | `CONCAT(a,b)` | `CONCAT(a,b)` |
| Limitar filas | `LIMIT n` | `LIMIT n` | `LIMIT n` | `LIMIT n` |
| Comillas de identificador | `"col"` | `"col"` | `` `col` `` | `` `col` `` |
| División de enteros | `5/2` = 2 (trunca) | `5/2` = 2 | `5/2` = 2.5 | `5/2` = 2.5 |
| Tipo fecha nativo | No; TEXT/REAL/INTEGER | Sí (DATE, TIMESTAMP) | Sí (DATE, DATETIME) | Sí (DATE, TIMESTAMP) |
| Extraer parte de fecha | `strftime('%Y', f)` | `EXTRACT(YEAR FROM f)` | `YEAR(f)` | `EXTRACT(YEAR FROM f)` |
| Orden de NULL | NULL primero al ordenar ascendente | configurable con `NULLS FIRST/LAST` | NULL primero | `NULLS FIRST/LAST` |
| Tipado | Afinidad laxa (dinámico) | Estricto | Estricto (con modos) | Estricto |

Sobre el orden de NULL: en SQLite, al ordenar de menor a mayor, los NULL vienen primero, luego enteros y reales, luego texto, luego BLOB, según la documentación oficial [P]. PostgreSQL y BigQuery permiten `NULLS FIRST/LAST`; SQLite también acepta esa cláusula en versiones recientes, pero el comportamiento por defecto es el descrito.

## Particularidades de SQLite que el principiante toca primero [P]

- **Concatenación con `||`;** si un operando es NULL, el resultado es NULL.
- **`LIMIT n`** para recortar filas (no `TOP`, no `FETCH FIRST`).
- **Comillas:** simples para texto, dobles para identificadores; regla estricta del curso: texto = comilla simple.
- **Fechas:** no hay tipo fecha nativo; se guardan como TEXT (ISO 8601 `'2026-01-31'`), REAL (día juliano) o INTEGER (unix), y se manipulan con `date()`, `datetime()`, `strftime()`. `'now'` es UTC por defecto.
- **NULL y tres valores:** `NULL` no es igual ni distinto a nada; usa `IS NULL`.
- **Afinidad de tipos (type affinity):** una columna admite cualquier tipo; el `.import` de CSV tiende a crear TEXT sin inferir, así que números y fechas pueden entrar como texto. Para auditar hay que forzar con `CAST(x AS REAL)` o `CAST(x AS INTEGER)`.
- **`COUNT(*)`** cuenta todas las filas; **`COUNT(columna)`** cuenta solo los valores no NULL; los demás agregados (SUM, AVG, MIN, MAX) ignoran NULL [P].

## H. Qué NO cubre el curso (con nombre y apellido)

- Optimización interna del motor (planes de ejecución, `EXPLAIN`, estadísticas).
- Administración de bases de datos (respaldos, usuarios, permisos, réplicas).
- Modelado dimensional a escala (esquemas estrella, tablas de hechos y dimensiones).
- Procedimientos almacenados, triggers y funciones definidas por el usuario.
- Concurrencia y transacciones en profundidad (se nombra la transacción en el diccionario; no se practica).
- Escritura de datos en profundidad: INSERT, UPDATE y DELETE se mencionan al importar, pero la auditoría es de solo lectura.
- **Funciones de ventana (window functions): quedan fuera de estas 30 lecciones.** Son la primera cosa que el alumno debería aprender después, y el curso lo dice explícitamente (ver sección I).
- DDL avanzado (constraints complejas, vistas materializadas), y cualquier dialecto que no sea SQLite salvo en la tabla de divergencias.

## I. Qué significa «proficiente» al terminar

**Tareas concretas que el egresado puede hacer solo:** cargar un CSV propio; definir el grano, la población y la ventana de una pregunta; leer una consulta ajena y decir qué devuelve; escribir SELECT con WHERE, GROUP BY, HAVING, un JOIN de dos tablas y ORDER BY; detectar y explicar las fallas del catálogo de la sección D; verificar una consulta contra un total conocido; y entregar una auditoría con hallazgos completos y salvedades.

**El techo honesto de 30 lecciones.** El egresado NO domina funciones de ventana, subconsultas complejas anidadas, CTEs recursivas, optimización, ni varios JOIN encadenados con lógica fina. Su fuerza no es la sintaxis avanzada: es el juicio sobre si un número responde la pregunta.

**¿Pasa una prueba técnica de SQL en una entrevista de analista junior en LatAm?** Solo parcialmente. La evidencia disponible indica que las pruebas técnicas de analista de datos combinan preguntas conceptuales y ejercicios prácticos, y que SQL es el lenguaje más evaluado, casi siempre con JOINs, GROUP BY y frecuentemente funciones de ventana [S, Datademia]. TestGorilla comercializa una prueba de SQLite descrita como de nivel intermedio —«evaluates candidates' skills in creating a query on a database with medium complexity… solving it requires intermediate SQLite querying skills»— que cubre justamente JOIN, GROUP BY y HAVING [S]. El egresado de este curso llega bien preparado en la mitad conceptual (grano, NULL, orden de ejecución, por qué un número está mal —justo lo que muchos candidatos no saben explicar) y en JOINs y GROUP BY básicos, pero le faltarían funciones de ventana y subconsultas intermedias para aprobar una prueba práctica completa. Qué le falta, explícito: window functions (`ROW_NUMBER`, `RANK`, `SUM OVER`), CTEs, y práctica de velocidad escribiendo sin ayuda. Recomendación honesta para la portada: este curso te vuelve capaz de auditar datos y de razonar con ellos; para una entrevista técnica de analista, súmale un módulo posterior de funciones de ventana y subconsultas.

## J. Bibliografía clasificada

**[P] Documentación oficial y fuentes con método reproducible** (consultadas el 3 de septiembre de 2026):
- SQLite, «Datatypes In SQLite Version 3» (type affinity, orden de NULL, sin tipo fecha nativo). sqlite.org/datatype3.html
- SQLite, «Date And Time Functions». sqlite.org/lang_datefunc.html
- SQLite, «Built-in Aggregate Functions» (COUNT(*) vs COUNT(X), agregados ignoran NULL). sqlite.org/lang_aggfunc.html
- SQLite, «SQL Language Expressions» (lógica de tres valores, operadores con NULL, división entera). sqlite.org (lang_expr.html) y system.data.sqlite.org.
- SQLite, foro oficial: división entera `5/2`; `.import` y afinidad; textos de error (`near "…": syntax error`, `UNIQUE constraint failed`, `NOT NULL constraint failed`, `unrecognized token`, `incomplete input`, `misuse of aggregate: COUNT()`). sqlite.org/forum
- SQLite, «Result and Error Codes» (SQLITE_MISMATCH / datatype mismatch). sqlite.org/rescode.html
- SQLite, «Release History» y portada (versión 3.53.4, 2026-07-24; retiro de 3.52.0 y parche 3.51.3; notas de 3.50.0). sqlite.org/changes.html, sqlite.org/news.html y sqlite.org
- sqliteonline.com (meta-descripción «No registration for start, No DownLoad, No Install»; motor SQLite en el navegador).
- Portales de datos abiertos: datos.gob.cl, datos.gov.co, datos.gob.mx, inegi.org.mx/datosabiertos, datos.gob.ar, datosabiertos.gob.pe.

**[S] Fuentes secundarias respetadas (con editor identificado):**
- Lukas Eder, jOOQ, «What's Faster? COUNT(*) or COUNT(1)?» — mito de COUNT desmentido.
- Slava Rozhnev, DEV Community, «Debunking the Myth: Is JOIN Always Faster Than Correlated Subqueries?» — empate en SQLite 3.45.
- DataCamp, «SQL Order of Execution» — orden lógico de ejecución.
- SQLShack (Red Gate), sobre SELECT * y planes de ejecución.
- w3resource y SQLite Tutorial — comportamiento de AVG con texto/BLOB y de COUNT.
- DZone, Medium y blog de Vesko Vujović — fan-out de JOIN y agregados.
- Datademia («Entrevista técnica data analyst») y TestGorilla («SQLite Intermediate-Level Querying Test») — cómo son las pruebas técnicas de analista de datos.

**[X] Folclore identificado y descartado** (ver sección de mitos): «SELECT * siempre es malo», «subqueries siempre más lentos que JOIN», «índices siempre aceleran», «NULL = NULL», «COUNT(*) más lento que COUNT(1)», «hay que escribir en mayúscula», «comillas dobles para texto en SQLite».

### Nota de reproducibilidad
Toda consulta de ejemplo de este documento corre tal cual en SQLite 3.50.x sobre las tablas descritas (`ventas`, `clientes`, `pedidos`, `lineas`, `productos`) con las columnas nombradas. Los guiones hablados no contienen sintaxis; la sintaxis vive solo en las guías escritas.

### Salvedades del propio documento
- No se verificó en vivo el comportamiento exacto del selector de archivos de Android en sqliteonline ni si su «Intelligent-Import» infiere tipos o crea columnas TEXT; por eso la lección 1 comprueba con `typeof()`.
- La interfaz de sqliteonline está en inglés; el alumno depende de «Traducir página» de Chrome. Los planes B (Sqlime, Datasette Lite) también están en inglés.
- Los límites de planes gratuitos y las versiones de herramientas cambian; verificados en septiembre de 2026.
- El texto exacto de algunos mensajes de error de SQLite depende de la versión; los aquí listados corresponden a SQLite 3.x moderno (3.50.x en adelante).