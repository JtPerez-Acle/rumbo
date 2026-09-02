/* The app's hash router, as reactive state.
 *
 * STILL A HASH ROUTER, and that is a decision rather than an omission. Real
 * paths buy two things: a crawler can read them, and a server can render them
 * per-route. Neither applies here — the app is session-gated and robots.txt
 * excludes it on purpose, because a learner's documents live on unguessable
 * tokens and a token in a search index is no longer unguessable. What real
 * paths WOULD cost is every deep link already sitting in a learner's inbox.
 * A migration is the wrong moment to spend that for nothing.
 *
 * Lesson steps stay individually addressable (#/leccion/12/ejercicio). That is
 * load-bearing: a pending conversation surfaced on Hoy has to land exactly on
 * the step where it can be answered, and before those existed a completed
 * lesson skipped the explain step and the conversation was unreachable.
 */

/** Which tab owns each route segment. Anything unknown is Hoy. */
const TAB_OF = {
  hoy: 'hoy', objetivo: 'hoy', cv: 'hoy', oferta: 'hoy',
  cursos: 'cursos', curso: 'cursos', leccion: 'cursos', reto: 'cursos',
  portafolio: 'portafolio', documento: 'portafolio', 'caso-view': 'portafolio',
  perfil: 'perfil',
};

function parse() {
  const [seg = '', arg = '', step = ''] = location.hash.replace(/^#\/?/, '').split('/');
  return { seg, arg, step, tab: TAB_OF[seg] || 'hoy' };
}

/** The current route. Reassigned on every hashchange. */
export const route = $state(parse());

function sync() {
  Object.assign(route, parse());
}

/** Start listening. Returns the teardown. */
export function startRouter() {
  window.addEventListener('hashchange', sync);
  return () => window.removeEventListener('hashchange', sync);
}

/** Go to a hash. Re-renders even when it is the one we are already on. */
export function nav(hash) {
  if (location.hash === hash) sync();
  else location.hash = hash;
}
