/* Render check for renderJobResult — the public job-analysis result page.
 *
 *   node studio/dashboard/check_job_render.js \
 *        studio/dashboard/static/learn.html \
 *        studio/fixtures/job-postings/sample-analysis.json
 *
 * There is no bundler and no test runner for the single-file frontends, and the
 * browser pane wedges often enough that docs/07 names the fallback: extract the
 * render function and exercise it under a tiny DOM shim in Node. `$` is stubbed
 * to capture the HTML it is handed rather than build nodes, which is enough to
 * assert what a learner actually sees.
 *
 * Run it after touching renderJobResult. It has already caught the gap block
 * rendering empty — the block that carries the honesty promise.
 */
const fs = require('fs'), path = require('path'), vm = require('vm');

const html = fs.readFileSync(process.argv[2], 'utf8');
const blocks = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
let src = blocks[blocks.length - 1].replace(/\bboot\(\);\s*$/, '');   // don't bootstrap

// `$` and `app` are const in the source, so swap them at the text level: `$`
// captures the HTML it is handed instead of building nodes, `app` collects it.
src = src.replace(
  /const \$=\(h\)=>\{[^\n]*\};/,
  'const $=(h)=>({__html:h,querySelector:()=>({onclick:null,style:{},value:"",classList:{add(){},remove(){},toggle(){}}}),' +
  // children appended to a created element must be captured too, or blocks
  // built as card > rows (the gap list) silently read as empty
  'querySelectorAll:()=>[],classList:{add(){},remove(){},toggle(){}},' +
  'append(x){if(x&&x.__html)__cap.push(x.__html)},onclick:null,style:{},dataset:{},textContent:""});');
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
sandbox.__cap = captured;
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
vm.runInContext(src, sandbox);

// --- the paste box: the wait must be declared BEFORE anyone commits to it ---
vm.runInContext('renderJobBox()', sandbox);
const box = captured.join('\n');
const stages = vm.runInContext('JOB_STAGES', sandbox);
const slowAt = vm.runInContext('JOB_SLOW_AT', sandbox);
const boxChecks = [
  ['paste box has a textarea', /<textarea[^>]*id="jtext"/.test(box)],
  ['goal-mode toggle present', /Solo sé el puesto/.test(box)],
  ['goal input present', /id="jgoal"/.test(box)],
  ['honeypot present', /id="jcompany"/.test(box)],
  ['wait declared up front', /dos minutos/.test(box)],
  ['tells them not to close the tab', /No cierres esta pesta/.test(box)],
  ['stages defined', Array.isArray(stages) && stages.length >= 4],
  ['stages start at 0s', stages[0][0] === 0],
  ['stage times ascend', stages.every((s, i) => i === 0 || s[0] > stages[i - 1][0])],
  ['every stage explains itself', stages.every(s => s[2] && s[2].length > 20)],
  ['slow threshold past the last stage', slowAt > stages[stages.length - 1][0]],
];
captured.length = 0;

const analysis = JSON.parse(fs.readFileSync(process.argv[3], 'utf8')).analysis;
// With a token: the share affordance must appear. Without one (an analysis
// re-rendered from storage) it must not offer a link that does not exist.
vm.runInContext('renderJobResult(' + JSON.stringify(analysis) + ')', sandbox);
const noToken = captured.join('\n');
captured.length = 0;
vm.runInContext('renderJobResult(' + JSON.stringify(analysis) + ', "TESTTOKEN123")', sandbox);

const out = captured.join('\n');
boxChecks.push(
  ['share card shown when a token exists', /Comparte esta ruta/.test(out)],
  ['share card hidden without a token', !/Comparte esta ruta/.test(noToken)],
);
const nucleo = analysis.ruta.filter(r => r.phase === 'nucleo');
const later = analysis.ruta.filter(r => r.phase !== 'nucleo');
const checks = [
  ...boxChecks,
  ['role title rendered', out.includes(analysis.role_title)],
  ['coverage % rendered', out.includes('Cubrimos ' + analysis.coverage + '%')],
  ['núcleo header', !nucleo.length || out.includes('Empieza por aquí')],
  ['later header', !later.length || out.includes('Después, para completar')],
  ['every route course shown', analysis.ruta.every(r => out.includes(r.course_title))],
  // Mirrors modLabel in learn.html/ruta.html: v2 module sets read "Módulos 1 y 3",
  // v1 rows (no modules list) and full prefixes read "Hasta módulo N".
  ['every module selection shown', analysis.ruta.every(r => {
    const m = r.modules && r.modules.length ? r.modules : null;
    if (!m) return out.includes('Hasta módulo ' + r.through_module);
    const seq = m.length === m[m.length - 1] - m[0] + 1;
    if (seq && m[0] === 1) return out.includes(m.length === 1 ? 'Módulo 1'
      : 'Hasta módulo ' + m[m.length - 1]);
    if (m.length === 1) return out.includes('Módulo ' + m[0]);
    return out.includes('Módulos ' + m.slice(0, -1).join(', ') + ' y ' + m[m.length - 1]);
  })],
  ['gaps header', !analysis.gaps.length || out.includes('no lo cubrimos')],
  ['every gap shown', analysis.gaps.every(g => out.includes(g.name))],
  ['document shown', !analysis.doc_type || out.includes(analysis.doc_type)],
  ['honesty line', !analysis.gaps.length || out.includes('Preferimos decírtelo')],
  ['no undefined leaked', !/\bundefined\b/.test(out)],
  ['no [object Object]', !out.includes('[object Object]')],
];
let bad = 0;
for (const [name, ok] of checks) { if (!ok) bad++; console.log((ok ? 'PASS  ' : 'FAIL  ') + name); }
console.log('\n' + (checks.length - bad) + '/' + checks.length + ' render checks passed');
if (bad) { console.log('\n--- rendered ---\n' + out.slice(0, 1500)); process.exit(1); }
