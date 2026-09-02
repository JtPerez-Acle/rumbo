/* The DOM shim that lets the vanilla frontend be tested without a browser.
 *
 * WHY THIS FILE EXISTS
 * --------------------
 * There is no bundler and no test runner (PRODUCT.md), so four `check_*.js`
 * scripts each carried their own copy of this shim: read learn.html, pull out
 * the last <script>, swap the two DOM entry points for fakes, run it in a VM,
 * and collect whatever the render functions append. Roughly sixty near-identical
 * lines, four times, drifting apart — one of them had async support, one had a
 * matchMedia stub, one had neither.
 *
 * It is one module now, and it is the seam the Astro migration turns on. The
 * ASSERTIONS in the test files are about user-facing promises — "unlimited
 * retries is stated", "a skipped module is never called blocked" — and those
 * survive a rewrite untouched. Only this harness knows how the markup was
 * produced. When a screen becomes a Svelte component, its test swaps
 * `loadSpa()` for a component render and every expectation stays exactly as it
 * is. That is the whole reason phase 0 comes before phase 1: these assertions
 * are the only net under a 3,900-line rewrite.
 */
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const REPO = path.resolve(HERE, '../../..');
export const LEARN_HTML = path.join(REPO, 'studio/dashboard/static/learn.html');

/** A DOM node stand-in that records the HTML written through it. */
function makeNode(captured, html) {
  const node = {
    __html: html || '', onclick: null, style: {}, dataset: {}, textContent: '',
    value: '', disabled: false, rows: 2,
    classList: { add() {}, remove() {}, toggle() { return false }, contains() { return false } },
    addEventListener() {}, replaceWith() {}, remove() {}, focus() {}, scrollIntoView() {},
    setAttribute() {}, getAttribute() { return null },
    append(x) { if (x && x.__html) captured.push(x.__html); },
    prepend(x) { if (x && x.__html) captured.push(x.__html); },
    querySelector() { return makeNode(captured, '') },
    querySelectorAll() { return [] },
  };
  // renderDemoVerdict builds its rows with innerHTML and renderMD writes the
  // guide the same way; a plain property would swallow both silently.
  let inner = '';
  Object.defineProperty(node, 'innerHTML', {
    get: () => inner,
    set: (v) => { inner = v; if (v) captured.push(String(v)); },
  });
  return node;
}

/**
 * Load the SPA's script into a sandbox and return handles for exercising it.
 *
 * @param {string} [htmlPath] page to read; defaults to learn.html
 * @returns {{run,runAsync,returned,evaluate,setApi,sandbox}}
 */
export function loadSpa(htmlPath = LEARN_HTML) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  const blocks = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  let src = blocks[blocks.length - 1].replace(/\bboot\(\);\s*$/, '');

  // Two substitutions turn the real DOM entry points into recording fakes.
  src = src.replace(/const \$=\(h\)=>\{[^\n]*\};/, 'const $=(h)=>__mk(h);');
  src = src.replace(
    /const app=document\.getElementById\('app'\), tabbar=document\.getElementById\('tabbar'\);/,
    'const app=__mk(""); const tabbar={classList:{add(){},remove(){},toggle(){}}};');
  if (!/__mk/.test(src)) {
    // Loud on purpose. A silently failed substitution means every assertion
    // below runs against an empty string and the suite reports a clean pass —
    // exactly the failure mode docs/07 records for the allowlist audit.
    throw new Error('harness: shim substitution failed — learn.html changed shape');
  }

  const captured = [];
  const mk = (h) => makeNode(captured, h);
  const sandbox = {
    console,
    document: {
      getElementById: () => mk(''), createElement: () => mk(''),
      querySelector: () => mk(''), querySelectorAll: () => [],
      addEventListener() {},
      body: { classList: { add() {}, remove() {}, toggle() {}, contains() { return false } },
              prepend() {} },
      head: { appendChild() {} },
    },
    window: { addEventListener() {}, open() {}, matchMedia: () => ({ matches: false }) },
    location: { hash: '', search: '', href: '' },
    localStorage: { getItem: () => null, setItem() {}, removeItem() {} },
    sessionStorage: { getItem: () => null, setItem() {}, removeItem() {} },
    fetch: async () => ({ ok: true, status: 200, json: async () => ({}) }),
    setTimeout: (fn) => { try { fn(); } catch { /* fire immediately in tests */ } return 0 },
    clearTimeout() {}, setInterval: () => 0, clearInterval() {},
    requestAnimationFrame: (fn) => { try { fn(); } catch { /* ignore */ } return 0 },
    Date, Math, JSON, String, Number, Array, Object, Promise, RegExp, Error,
    __mk: mk, __cap: captured,
  };
  sandbox.globalThis = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(src, sandbox);

  return {
    sandbox,
    /** Run an expression and return everything it appended. */
    run(expr) { captured.length = 0; vm.runInContext(expr, sandbox); return captured.join('\n'); },
    /** Same, for an async render: drains microtasks before reading. */
    async runAsync(expr) {
      captured.length = 0;
      await vm.runInContext(expr, sandbox);
      await new Promise(r => setImmediate(r));
      return captured.join('\n');
    },
    /** For builders that RETURN an element instead of appending one. */
    returned(expr) { return String(vm.runInContext(expr, sandbox).__html || '') },
    /** Read a value out of the sandbox (constants, config). */
    evaluate(expr) { return vm.runInContext(expr, sandbox) },
    /** Replace the api() the views call, so a render can be driven with a payload. */
    setApi(jsExpr) { vm.runInContext(`api = ${jsExpr};`, sandbox) },
  };
}

/** The payload GET /api/learn/public/demo really returns. */
export const DEMO_PAYLOAD = {
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
