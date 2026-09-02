/* Strings and constants the public surface shares.
 *
 * They live here rather than in each page because the same sentence appearing
 * on five pages with four wordings is how a small product starts sounding like
 * four different ones.
 */

export const SITE_NAME = 'Rumbo';

/* The tutor has a name. "Tu tutora" is a product with no identity, and these
   pages ask a stranger to hand it their work. Vera: short, unambiguous in
   Spanish, and it means true — the one thing this product sells.
   NOTE: only the public surface says it. The app still says "tu tutora" in a
   few hundred strings; renaming those is a separate, mechanical pass. */
export const TUTOR = 'Vera';

/* The default og:description. "Aprende haciendo, con tutora IA" was the
   category's generic self-description — every competitor makes that claim, so
   it positioned us as one of them in the one string that travels furthest. */
export const SITE_DESC =
  'Dinos qué quieres ser y te armamos la ruta — incluido lo que ese puesto ' +
  'pide y nosotros no enseñamos. Terminas con trabajo real que mostrar, no ' +
  'con un certificado.';

/* Real exchanges, from the real evaluator.
   Each was produced by POSTing an answer to /public/demo-explain and keeping
   EXACTLY what came back — verdict, feedback, misconception, gaps. Not one
   sentence of tutor output here was written by a copywriter, which is the only
   reason any of it can be on the page: the whole argument of this surface is
   that the evaluation is real, and an invented one would be the single most
   damaging thing on it.

   Both shown answers are WRONG on purpose. A model answer next to the textarea
   would be copied, and `demo_attempts` exists to record what strangers actually
   write when nobody is grading them — the one honest read we have on whether
   the lesson teaches. Showing the answer would destroy the measurement. */
export const EXCHANGES = {
  // Half right: the page's proof that the tutor names gaps instead of scoring.
  casi: {
    badge: 'Casi',
    said: 'Un objetivo SMART es un objetivo bien hecho, que sea claro y que se pueda cumplir. Sirve para no gastar de más en publicidad porque si tienes claro lo que quieres entonces no andas probando cosas al azar.',
    fb: 'Dices bien que un objetivo SMART es claro y que evita gastar de más porque no andas probando al azar. Eso captura el porqué. Pero cuando la pregunta te pide <b>qué significa</b>, necesitas explicar qué hay detrás de las siglas. Sin eso, la definición queda muy vaga.',
    misconception: null,
    gaps: [
      'Explica qué significa cada letra de SMART: Específico, Medible, Alcanzable, Relevante, con Plazo.',
      'Conecta cómo cada criterio ayuda a no malgastar dinero: “medible” evita no saber si funcionó, “plazo” evita campañas sin fin.',
    ],
  },
  // Confidently wrong: the only place the misconception mechanic is visible,
  // and the thing no competitor's "AI tutor" actually does.
  todavia: {
    badge: 'Todavía no',
    said: 'SMART significa que el objetivo tiene que ser específico, o sea muy detallado. Mientras más detalles le pongas mejor es el objetivo. Si escribes un párrafo largo explicando todo lo que quieres lograr, eso ya es un objetivo SMART.',
    fb: 'Captaste bien la idea de que escribir el objetivo ayuda a no ir a ciegas, y que la claridad es importante. Pero centrarte solo en “específico” y en escribir un párrafo largo deja fuera la parte más importante de SMART. De hecho, un párrafo muy detallado puede ser todo menos SMART si no cumple los otros cuatro criterios, y por ahí es justo donde se escapa el dinero.',
    misconception: 'Ojo: SMART no es sinónimo de “muy detallado” ni de escribir un texto largo. Es un acrónimo de cinco criterios que se revisan uno por uno.',
    gaps: [
      'Te faltaron las otras cuatro letras: Medible, Alcanzable, Relevante y con Plazo.',
      'No explicaste por qué evitan malgastar dinero: sin métrica no sabes si la campaña funciona, sin plazo todo se dilata.',
    ],
  },
};

/* The four steps, in the order they actually happen. */
export const STEPS = [
  ['Dinos qué quieres ser', 'Pega la oferta de trabajo que te interesa, o solo el nombre del puesto. En unos dos minutos sabes qué pide de verdad, qué parte cubrimos, qué no, y tu ruta: qué cursos y qué módulos, en qué orden.'],
  ['Elige tu proyecto real', 'Tu negocio, o una marca donde te gustaría trabajar. Todos los ejercicios se hacen sobre ese mismo proyecto, y por eso lo que produces te sirve fuera de aquí.'],
  ['Una lección al día', 'Un video corto con el porqué, una guía escrita con el cómo, lo explicas con tus palabras, y un ejercicio donde pegas el trabajo que hiciste de verdad.'],
  ['Tu tutora lo lee y te contesta', 'Recibes un puntaje, qué te falta para llegar a 100, y una pregunta que solo puede contestar quien hizo el trabajo. Reintentas sin límite y siempre se queda tu mejor intento. Usar IA está permitido: evaluamos que el trabajo sea tuyo, no quién escribió el primer borrador.'],
];

/* What a learner leaves with. Deliberately three, and the third is the gap
   report: naming what we do not teach is the reason the coverage claim is
   believable at all. */
export const GETS = [
  ['doc', 'El documento que vas a mostrar', 'Tus entregas compiladas en un entregable profesional con tu nombre: una estrategia, un plan de campaña, una auditoría. Con enlace para compartir y PDF para imprimir.'],
  ['target', 'Tu ruta, siempre a la vista', 'Cuánto llevas del puesto que quieres, curso por curso y módulo por módulo. Empiezas por lo que más pesa, no por el principio de todo.'],
  ['target', 'Lo que te falta, dicho por su nombre', 'Si el puesto pide algo que no enseñamos, te lo decimos y te lo listamos. Preferimos eso a venderte un curso que no lo cubre.'],
];

/* Re-exported so the public landing and the app cannot disagree about what a
   verdict is called. It was defined twice under two names before. */
export { VERDICT as VERDICT_WORD } from './verdicts.js';
