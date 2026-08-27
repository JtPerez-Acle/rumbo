/* Render check for the public landing — the free lesson and its verdict (docs/11).
 *
 *   node studio/dashboard/check_demo_render.js studio/dashboard/static/learn.html
 *
 * Same fallback as the other two render checks: no bundler, no test runner, the
 * browser pane wedges (docs/07), so the render functions run under a DOM shim.
 *
 * What this guards is the surface's argument, not its layout. The landing exists
 * because a stranger cannot tell this product from any other by reading, so the
 * page has to keep DOING rather than claiming: a real lesson, a real question, a
 * real verdict, and honest copy about what does not exist yet. It also guards the
 * two things a finish review found missing on the first build — a call to action
 * that exists before anyone writes an answer, and a failure path that still
 * offers somewhere to go.
 */
const fs = require('fs'), vm = require('vm');

const html = fs.readFileSync(process.argv[2] || 'studio/dashboard/static/learn.html', 'utf8');
const blocks = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
let src = blocks[blocks.length - 1].replace(/\bboot\(\);\s*$/, '');

src = src.replace(/const \$=\(h\)=>\{[^\n]*\};/, 'const $=(h)=>__mk(h);');
src = src.replace(
  /const app=document\.getElementById\('app'\), tabbar=document\.getElementById\('tabbar'\);/,
  'const app=__mk(""); const tabbar={classList:{add(){},remove(){},toggle(){}}};');
if (!/__mk/.test(src)) { console.error('FATAL: shim substitution failed'); process.exit(2); }

const captured = [];
const sandbox = {
  console,
  document: { getElementById: () => __mk(''), createElement: () => __mk(''),
              querySelector: () => __mk(''), querySelectorAll: () => [],
              addEventListener(){}, body: { classList: { add(){}, remove(){}, toggle(){}, contains(){return false} } } },
  window: { addEventListener(){}, open(){}, matchMedia: () => ({ matches: false }) },
  location: { hash: '', search: '', href: '' },
  localStorage: { getItem: () => null, setItem(){}, removeItem(){} },
  sessionStorage: { getItem: () => null, setItem(){}, removeItem(){} },
  fetch: async () => ({ ok: true, status: 200, json: async () => ({}) }),
  setTimeout: (fn) => { try { fn(); } catch (e) {} return 0 },
  setInterval: () => 0, clearInterval(){}, Date, Math, JSON, String, Number, Array, Object, Promise,
};
function __mk(h) {
  const node = {
    __html: h || '', onclick: null, style: {}, dataset: {}, textContent: '',
    value: '', disabled: false,
    classList: { add(){}, remove(){}, toggle(){ return false }, contains(){ return false } },
    addEventListener(){}, replaceWith(){}, remove(){}, focus(){}, scrollIntoView(){},
    setAttribute(){}, getAttribute(){ return null },
    append(x){ if (x && x.__html) captured.push(x.__html); },
    querySelector(){ return __mk(''); },
    querySelectorAll(){ return []; },
  };
  // renderDemoVerdict builds its "así sigue" rows with innerHTML, and renderMD
  // writes the guide the same way; a plain property would swallow both.
  let _inner = '';
  Object.defineProperty(node, 'innerHTML', {
    get: () => _inner,
    set: (v) => { _inner = v; if (v) captured.push(String(v)); },
  });
  return node;
}
sandbox.__mk = __mk;
sandbox.__cap = captured;
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
vm.runInContext(src, sandbox);

// The payload GET /api/learn/public/demo really returns.
const demo = {
  course_slug: 'curso-marketing-ia', course_title: 'Marketing con IA', module_no: 1,
  module_title: 'Fundamentos', title: 'Elige tu proyecto real y define el objetivo',
  objectives: 'Seleccionar un negocio propio como caso transversal.',
  key_points: ['Determina el resultado que quieres', 'Usa la metodología SMART'],
  written: '## Pasos para definir tu objetivo SMART\n\nElige un proyecto que te importe.',
  transcript: 'transcripción',
  explain_prompt: '¿Qué significa que un objetivo sea SMART y por qué es clave?',
  has_video: true,
  exercise: { instruction: 'Elige tu proyecto real y redacta su meta.', deliverable: 'Una meta SMART' },
  reto: { title: 'Reto: San Valentín con $200', scenario: 'Una pastelería en Bogotá con 200 dólares.' },
  doc_type: 'Estrategia de marketing digital',
};

function run(fn) { captured.length = 0; vm.runInContext(fn, sandbox); return captured.join('\n'); }
// renderDemoLesson is async — it fetches its own payload. Stub api, run it, and
// let the microtask queue drain before reading what it appended.
async function runAsync(fn) {
  captured.length = 0;
  await vm.runInContext(fn, sandbox);
  await new Promise(r => setImmediate(r));
  return captured.join('\n');
}
// landingDoors RETURNS an element rather than appending one.
function returned(fn) { return String(vm.runInContext(fn, sandbox).__html || ''); }

(async () => {
sandbox.__demo = demo;
vm.runInContext('api = async () => __demo;', sandbox);
const lesson = await runAsync('renderDemoLesson(app)');

vm.runInContext('api = async () => ({detail:"nope"});', sandbox);
const failed = await runAsync('renderDemoLesson(app)');
vm.runInContext('api = async () => __demo;', sandbox);

const verdict = run('renderDemoVerdict(app, ' + JSON.stringify({
  verdict: 'casi', feedback: 'Vas bien, pero te falta el plazo.',
  misconception: 'SMART no es solo "ser específico".',
  missing: ['un número', 'una fecha'],
}) + ', ' + JSON.stringify(demo) + ')');
const doorsLit = returned('landingDoors("lit")');
const doorsGhost = returned('landingDoors("ghost")');

// ---- routing: the server-named view is consumed once ----------------------
// A server URL (/login, /oferta, /curso/<slug>) tells the SPA which view to open
// first. That hint used to be re-read on every route(), which made it sticky:
// "#/" normalises to an empty segment, empty is falsy, so on /login every attempt
// to go home fell back to the hint and re-rendered login. "‹ Conocer Rumbo" and
// the waitlist's "‹ Volver" were both dead ends. The invariant is that the hint
// applies to the FIRST render only; after that the hash is the authority, empty
// included — and empty means the landing.
const routing = (() => {
  try {
    const sb = Object.assign({}, sandbox, {
      window: { addEventListener(){}, open(){}, __VIEW__: 'login', __ARG__: '',
                matchMedia: () => ({ matches: false }) },
      // renderLogin reads the query string; without this the view throws and,
      // because route() is async, it surfaces as an unhandled rejection that
      // kills the process AFTER the results print — an exit 1 on a clean file.
      URLSearchParams,
    });
    sb.__mk = __mk; sb.__cap = captured; sb.globalThis = sb;
    vm.createContext(sb);
    vm.runInContext(src, sb);
    const before = vm.runInContext('__serverView', sb);
    // __serverView is cleared synchronously at the top of route(), before any
    // await, so it can be read straight after the call. The returned promise is
    // swallowed: this asserts the routing decision, not the render.
    const p = vm.runInContext('route()', sb);
    if (p && typeof p.catch === 'function') p.catch(() => {});
    const after = vm.runInContext('__serverView', sb);
    return { before, after };
  } catch (e) { return { before: 'THREW: ' + e.message, after: 'THREW' }; }
})();

const checks = [
  ['the server names the first view', routing.before === 'login'],
  ['...and the hint is consumed, so "home" works afterwards', routing.after === ''],

  // The lesson is real content, not a description of content.
  ['the real lesson title renders', lesson.includes(demo.title)],
  ['the course is named as provenance', lesson.includes('Marketing con IA')],
  ['a play affordance exists, not a bare <video>', /videoplate/.test(lesson) && !/<video/.test(lesson)],
  ['the poster is a real frame from the lesson', /demo-poster/.test(lesson)],
  ['the video is NOT preloaded', !/preload="(auto|metadata)"/.test(lesson)],
  ['key points render', lesson.includes('metodología SMART')],
  ['the guide is a masked preview, not a scroll region',
   /guidewrap/.test(lesson) && !/overflow:auto/.test(lesson)],
  ['the guide can be expanded', /Seguir leyendo/.test(lesson)],

  // The question is the argument.
  ['the real explain prompt is asked', lesson.includes(demo.explain_prompt)],
  ['there is a textarea to answer in', /<textarea[^>]*id="dq"/.test(lesson)],
  ['the textarea is labelled by the question', /aria-labelledby="dqq"/.test(lesson)],
  ['honeypot present', /id="dqc"/.test(lesson)],
  ['it promises a verdict, never a score', /No hay nota/.test(lesson)],
  ['storage is disclosed honestly', /Guardamos lo que escribes/.test(lesson)],

  // The verdict.
  ['the verdict is a word, not a number', /Casi/.test(verdict) && !/\/100/.test(verdict)],
  ['the tutor feedback renders', verdict.includes('te falta el plazo')],
  ['a misconception is surfaced', verdict.includes('SMART no es solo')],
  ['what is missing is named', verdict.includes('un número') && verdict.includes('una fecha')],
  ['the verdict region is announced', /aria-live/.test(lesson)],

  // What follows is real content, not claims.
  ['the numbering matches the rows shown', /dos de los cinco pasos/.test(verdict)],
  ["this lesson's real exercise is shown", verdict.includes('Elige tu proyecto real y redacta')],
  ["this module's real reto is shown", verdict.includes('pastelería en Bogotá')],
  ['the real document type is named', verdict.includes('Estrategia de marketing digital')],
  ['no certificate is promised', /No damos certificados/.test(verdict)],

  // Reachability — both found missing by the finish review.
  ['the verdict offers all three doors',
   /Dinos qué quieres ser/.test(doorsLit) && /Quiero entrar/.test(doorsLit) && /Tengo una invitación/.test(doorsLit)],
  ['a quiet door set exists for the page tail', /Tengo una invitación/.test(doorsGhost)],
  ['only the lit set uses the primary treatment',
   /btn-primary/.test(doorsLit) && !/btn-primary/.test(doorsGhost)],
  ['a failed demo still offers somewhere to go', /Dinos qué quieres ser/.test(failed)],
  ['a failed demo says so plainly', /no está disponible/.test(failed)],

  // Honesty: PRODUCT.md records these do not exist.
  ['no fabricated learner document', !/documento real de una alumna/i.test(lesson + verdict)],
  ['no invented testimonial or customer count',
   !/(testimonio|alumnas? satisfech|\d+\s*(alumnos|estudiantes|usuarios)\b)/i.test(lesson + verdict)],
  ['no invented pricing', !/(\$\s?\d+\s*\/\s*mes|precio|suscripción)/i.test(lesson + verdict)],

  // Regressions.
  ['no undefined leaked', !/\bundefined\b/.test(lesson + verdict + doorsLit + failed)],
  ['no [object Object]', !(lesson + verdict + doorsLit + failed).includes('[object Object]')],
];

let bad = 0;
for (const [name, ok] of checks) { if (!ok) bad++; console.log((ok ? 'PASS  ' : 'FAIL  ') + name); }
console.log('\n' + (checks.length - bad) + '/' + checks.length + ' demo render checks passed');
if (bad) {
  console.log('\n--- lesson ---\n' + lesson.slice(0, 1400));
  console.log('\n--- verdict ---\n' + verdict.slice(0, 1200));
  process.exit(1);
}
})();
