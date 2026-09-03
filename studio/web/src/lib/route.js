/* The route matcher's client-side vocabulary. */

/* Written by `export_web.py` from the live catalog. Imported here rather than
   read off catalog.json because this module ships to the browser and the full
   catalog would be every course title and description for the sake of two
   integers. */
import totals from '../data/totals.json';

/* What the analyser is actually doing, and roughly when.
   The seconds are observed, not invented — a progress display that lies is
   worse than none, and this product's whole pitch is that it does not.

   Which is exactly why the counts are interpolated and not typed. They read
   "210 lecciones" and "35 módulos" until 2026-09-03 — a seven-course catalog's
   numbers, shown to every visitor for two minutes while the thing they were
   describing crossed 450 lessons. The stage copy was lying in the one component
   whose comment says not to. */
export const JOB_STAGES = [
  [0, 'Leyendo la oferta completa', 'Cada requisito, incluso los que vienen escondidos en la descripción.'],
  [12, 'Separando lo que de verdad se estudia', 'Las competencias que puedes aprender, no los años de experiencia ni "ortografía impecable".'],
  [34, `Cruzando con las ${totals.lessons} lecciones`, `Los ${totals.modules} módulos del catálogo, uno por uno, para ver cuál cubre cada competencia.`],
  [72, 'Decidiendo hasta dónde tienes que llegar', 'Casi nunca necesitas el curso completo: depende de lo que pida el puesto.'],
  [104, 'Escribiendo tu ruta y tu documento', 'Qué estudiar, en qué orden, y qué vas a poder llevar a la entrevista.'],
];

/** Seconds past which we say it is slow instead of pretending otherwise. */
export const JOB_SLOW_AT = 170;

/* Route entries: v2 carries a module set, v1 only a depth. One formatter for
   both, so a skipped module reads honestly ("Módulos 1 y 3") instead of as a
   prefix that claims work the route never selected. */
export function modLabel(r) {
  const m = r.modules && r.modules.length ? r.modules : null;
  if (!m) return 'Hasta módulo ' + r.through_module;
  const sequential = m.length === m[m.length - 1] - m[0] + 1;
  if (sequential && m[0] === 1) {
    return m.length === 1 ? 'Módulo 1' : 'Hasta módulo ' + m[m.length - 1];
  }
  if (m.length === 1) return 'Módulo ' + m[0];
  return 'Módulos ' + m.slice(0, -1).join(', ') + ' y ' + m[m.length - 1];
}
