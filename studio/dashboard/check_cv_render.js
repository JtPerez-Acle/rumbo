/* Render check for the CV screen — the paste box and renderCvResult (docs/10).
 *
 *   node studio/dashboard/check_cv_render.js studio/dashboard/static/learn.html
 *
 * Same fallback as check_job_render.js: no bundler, no test runner, and the
 * browser pane wedges (docs/07), so the render functions are exercised under a
 * tiny DOM shim and we assert what a learner actually sees.
 *
 * What this file really guards is a PROMISE, not a layout. The whole feature
 * rests on the CV being a proposal rather than a permission — so the screen has
 * to keep saying that a skip is the learner's choice, that it can be undone,
 * that the reto is what makes it count, and that the CV never reaches their
 * document. Those sentences ageing silently is the failure docs/07 names as
 * "copy that ages silently", and it is exactly what check_how_section.js exists
 * to prevent on the landing.
 */
const fs = require('fs'), vm = require('vm');

const html = fs.readFileSync(process.argv[2] || 'studio/dashboard/static/learn.html', 'utf8');
const blocks = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
let src = blocks[blocks.length - 1].replace(/\bboot\(\);\s*$/, '');

// Richer than check_job_render's stub: these cards build their buttons into a
// child container (`.cvacts`), so a querySelector result has to be a real
// capturing node or half the screen is invisible to the assertions.
src = src.replace(/const \$=\(h\)=>\{[^\n]*\};/, 'const $=(h)=>__mk(h);');
src = src.replace(
  /const app=document\.getElementById\('app'\), tabbar=document\.getElementById\('tabbar'\);/,
  'const app={innerHTML:"",append(x){if(x&&x.__html)__cap.push(x.__html)},querySelector:()=>({onclick:null}),' +
  'querySelectorAll:()=>[]}; const tabbar={classList:{add(){},remove(){},toggle(){}}};');
if (!/__cap\.push/.test(src)) { console.error('FATAL: shim substitution failed'); process.exit(2); }

const captured = [];
const el = () => new Proxy(function () {}, {
  get: (t, k) => k === 'querySelector' || k === 'querySelectorAll' ? () => el()
    : k === 'append' || k === 'appendChild' ? (x) => { if (x && x.__html) captured.push(x.__html); }
    : k === 'classList' ? { add(){}, remove(){}, toggle(){}, contains(){return false} }
    : k === 'dataset' ? {} : k === 'style' ? {} : k === 'value' ? '' : el(),
  set: () => true, apply: () => el(),
});
const sandbox = {
  console,
  document: { getElementById: () => el(), createElement: () => el(),
              querySelector: () => el(), querySelectorAll: () => [],
              addEventListener(){}, body: el() },
  window: { addEventListener(){}, open(){}, matchMedia: () => ({matches:false}) },
  location: { hash: '', search: '', href: '' },
  localStorage: { getItem: () => null, setItem(){}, removeItem(){} },
  sessionStorage: { getItem: () => null, setItem(){}, removeItem(){} },
  fetch: async () => ({ ok: true, status: 200, json: async () => ({}) }),
  setTimeout: (fn) => { try { fn(); } catch (e) {} return 0 },
  setInterval: () => 0, clearInterval(){}, Date, Math, JSON, String, Number, Array, Object,
};
// One node factory for both `$` and any querySelector inside a built card.
sandbox.__mk = function __mk(h) {
  return {
    __html: h || '', onclick: null, style: {}, dataset: {}, textContent: '',
    value: '', disabled: false,
    classList: { add(){}, remove(){}, toggle(){}, contains(){ return false } },
    addEventListener(){}, replaceWith(){}, remove(){},
    append(x){ if (x && x.__html) captured.push(x.__html); },
    querySelector(){ return __mk(''); },
    querySelectorAll(){ return []; },
  };
};
sandbox.__cap = captured;
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
vm.runInContext(src, sandbox);

// ---- the paste box -------------------------------------------------------
vm.runInContext('renderCvBox()', sandbox);
const box = captured.join('\n');
captured.length = 0;

// ---- the result, with one of each state ----------------------------------
const claim = (over) => Object.assign({
  course_slug: 'curso-meta-ads', course_title: 'Meta Ads', module_no: 1,
  module_title: 'Cuenta y pixel', outcome: 'Sabrás dejar la cuenta midiendo de verdad.',
  capability: 'instaló el pixel', evidence: 'Instalé el pixel en 12 tiendas Shopify',
  confidence: 'alta', lessons: 6, proposed: true, state: 'pendiente', exempt_score: null,
}, over);

const data = {
  exists: true, pass_score: 70, created_at: '2026-08-26',
  headline: 'Media buyer senior', years_experience: 5,
  proposed_modules: 3, proposed_lessons: 18,
  claims: [
    claim({}),
    claim({ module_no: 2, state: 'declarado' }),
    claim({ module_no: 4, state: 'acreditado', exempt_score: 85 }),
    claim({ module_no: 3, confidence: 'baja', proposed: false, capability: 'mencionó creatividades' }),
  ],
  fuera_del_catalogo: [{ name: 'Inglés C1', evidence: 'certificado C1' }],
};
vm.runInContext('renderCvResult(' + JSON.stringify(data) + ')', sandbox);
const out = captured.join('\n');
captured.length = 0;

// ---- a credited claim ALONE ---------------------------------------------
// Rendered on its own because the shim captures a flat stream: with several
// cards in it, "is there an undo button" cannot be attributed to a card. On its
// own the question is exact, and it is the invariant that matters most — a
// credited module was earned by passing a reto, so nothing may take it back.
vm.runInContext('renderCvResult(' + JSON.stringify({
  exists: true, pass_score: 70, created_at: '2026-08-26', headline: 'X',
  years_experience: 5, proposed_modules: 1, proposed_lessons: 6,
  claims: [claim({ state: 'acreditado', exempt_score: 85 })], fuera_del_catalogo: [],
}) + ')', sandbox);
const credited = captured.join('\n');
captured.length = 0;

// ---- the empty reading: a CV that proves nothing must not read as a verdict
const empty = { exists: true, pass_score: 70, created_at: '2026-08-26',
                headline: 'Asistente administrativa', years_experience: 1,
                proposed_modules: 0, proposed_lessons: 0, claims: [], fuera_del_catalogo: [] };
vm.runInContext('renderCvResult(' + JSON.stringify(empty) + ')', sandbox);
const none = captured.join('\n');

// ---- the temario, with one module skipped ---------------------------------
// "No me hagas ver de nuevo lo que ya sé" is the ask this feature answers, so
// the course outline has to honour it too — while never locking anything.
const outline = {
  slug: 'curso-meta-ads', title: 'Meta Ads', description: '', total: 12, done: 0,
  modules: [
    { module_no: 1, module_title: 'Cuenta y pixel', module_description: 'Sabrás medir.',
      exempt: 'declarado', exempt_score: null,
      lessons: [{ id: 1, position: 1, title: 'Qué es el pixel', objectives: 'o', status: 'current' },
                { id: 2, position: 2, title: 'Instalarlo', objectives: 'o', status: 'locked' }],
      capstone: { id: 91, title: 'Reto: monta la medición', status: 'available', score: null, test_out: true } },
    { module_no: 2, module_title: 'Públicos', module_description: 'Sabrás segmentar.',
      exempt: null, exempt_score: null,
      lessons: [{ id: 7, position: 7, title: 'Públicos guardados', objectives: 'o', status: 'locked' }],
      capstone: { id: 92, title: 'Reto: arma tus públicos', status: 'locked', score: null, test_out: false } },
  ],
};
vm.runInContext(
  'api = async (p) => p.indexOf("/course/") === 0 ? __outline : ({exists:false, eligible:false});',
  sandbox);
sandbox.__outline = outline;
// viewOutline is async (it awaits the outline), unlike every other render
// function here — so the whole report waits on it. Reading `captured` straight
// after the call returns an empty screen and four assertions that fail for the
// wrong reason.
Promise.resolve()
  .then(() => vm.runInContext('viewOutline("curso-meta-ads")', sandbox))
  .then(() => captured.join('\n'), (e) => 'THREW: ' + e.message)
  .then((temario) => { captured.length = 0; report(temario); });

function report(temario) {
const checks = [
  // the temario
  ['skipped module is flagged in the temario', /Ya lo sabes/.test(temario)],
  ['skipped module can still be opened', /Ver igual/.test(temario)],
  ['skipped module is not called locked', !/Te saltaste este m[óo]dulo[\s\S]{0,120}Bloquead/.test(temario)],
  ['its reto is offered as the way to credit it', /Acredita este m[óo]dulo/.test(temario)],
  ['a normal module is untouched', /P[úu]blicos guardados/.test(temario) && /Reto: arma tus p[úu]blicos/.test(temario)],
  ['temario did not throw', !temario.startsWith('THREW')],

  // the box
  ['paste box has a textarea', /<textarea[^>]*id="cvtext"/.test(box)],
  ['honeypot present', /id="cvcompany"/.test(box)],
  ['wait declared up front', /cerca de un minuto/.test(box)],
  ['tells them not to close the tab', /No cierres esta pesta/.test(box)],
  ['box promises contact stripping', /correo y tu tel/.test(box)],
  ['box promises the CV stays out of the document', /solo va trabajo tuyo evaluado/.test(box)],
  ['box says the learner decides', /T[úu] decides/.test(box)],
  ['asks for what they DID, not titles', /qu[ée] hiciste/.test(box)],

  // the result: the promise, stated on screen
  ['headline rendered', out.includes('Media buyer senior')],
  ['module outcome shown, not the lesson list', out.includes('Sabrás dejar la cuenta midiendo')],
  ['every claim quotes the CV', out.includes('Instalé el pixel en 12 tiendas Shopify')],
  ['pending claim offers the skip', /Ya lo s[ée], s[áa]ltalo/.test(out)],
  ['pending claim offers to keep the lessons', /Prefiero verlo igual/.test(out)],
  ['declared claim offers the reto', /Pru[ée]balo con el reto/.test(out)],
  ['declared claim is undoable', /Mejor ens[ée][ñn]amelo/.test(out)],
  ['the reto is described as an uncovered case', /caso nuevo que las lecciones no cubren/.test(out)],
  ['the pass bar is stated', out.includes('70+')],
  ['credited claim shows its score', /Acreditado 85/.test(out)],
  ['credited claim is NOT undoable', !/Mejor ens[ée][ñn]amelo/.test(credited)],
  ['credited claim offers no skip button either', !/s[áa]ltalo/i.test(credited)],
  ['credited module stays open', /sigue abierto/.test(credited)],
  ['low-confidence claims are separated, not proposed', /no alcanza para salt/.test(out)],
  ['low-confidence claims can still be earned via the reto', /se acredita solo/.test(out)],
  ['outside-catalog strengths shown', out.includes('Inglés C1')],
  ['CV is deletable', /Borrar mi CV/.test(out)],
  ['result repeats the document boundary', /solo va trabajo tuyo evaluado/.test(out)],

  // the empty reading
  ['empty reading does not read as a verdict on the person',
   /no dice nada malo de tu experiencia/.test(none)],
  ['empty reading explains the evidence rule', /sin cita no damos nada por sabido/.test(none)],

  // regressions
  ['no undefined leaked', !/\bundefined\b/.test(out + box + none)],
  ['no [object Object]', !(out + box + none + credited).includes('[object Object]')],
  // The word that must never appear: a skip is not a lock, and the moment the
  // copy says it is, the feature has become the thing docs/10 refuses to build.
  ['never calls a skipped module blocked', !/bloquead/i.test(out)],
];

let bad = 0;
for (const [name, ok] of checks) { if (!ok) bad++; console.log((ok ? 'PASS  ' : 'FAIL  ') + name); }
console.log('\n' + (checks.length - bad) + '/' + checks.length + ' CV render checks passed');
if (bad) {
  console.log('\n--- result ---\n' + out.slice(0, 1500));
  console.log('\n--- temario ---\n' + temario.slice(0, 1500));
  process.exit(1);
}
}
