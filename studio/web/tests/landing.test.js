/* The landing, as it actually ships.
 *
 * These assertions were written against the SPA's renderDemoLesson() and moved
 * here when the landing became a built page. They test the same promises — the
 * lesson is content and not a description of content, the question is really
 * askable, and the page claims no testimonial, no customer count and no price,
 * because PRODUCT.md records that none of those exist.
 *
 * What changed is the subject, and it changed for the better: this reads
 * dist/index.html, the bytes a visitor is served. The old suite ran the SPA's
 * render function inside a DOM shim and could pass while the served page was
 * eleven characters of "Cargando…" — which is exactly what it once was.
 *
 * The build has to have run. `npm test` runs it; a bare `vitest run` after
 * editing a page will test the previous build, so the first assertion checks
 * the file is not stale in the only way a file can prove that.
 */
import { describe, it, expect, beforeAll } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { JSDOM } from 'jsdom';
import { REPO } from './harness.js';
import { JOB_STAGES } from '../src/lib/route.js';

const DIST = path.join(REPO, 'studio/web/dist');
const demo = JSON.parse(
  fs.readFileSync(path.join(REPO, 'studio/web/src/data/demo.json'), 'utf8'),
);
const read = (name) =>
  JSON.parse(fs.readFileSync(path.join(REPO, 'studio/web/src/data', name), 'utf8'));
const catalog = read('catalog.json');
const totals = read('totals.json');

/** Markup with <script>, <style> and island props removed.
 *
 * The props strip is not cosmetic. Astro serializes an island's props into an
 * `<astro-island props="...">` attribute, so a needle can be found in a page
 * that never renders it — which is exactly what happened here: the key-points
 * assertion passed with the key points deleted, because the same words were
 * sitting unread inside that attribute. This is the RENDERED page. */
const noScripts = (html) =>
  html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/props="[^"]*"/gi, ' ');

describe('the landing', () => {
  let html, text;

  beforeAll(() => {
    const file = path.join(DIST, 'index.html');
    if (!fs.existsSync(file)) {
      throw new Error(
        'dist/index.html is missing — run `npm run build` first. ' +
        '`npm test` does it for you.',
      );
    }
    html = fs.readFileSync(file, 'utf8');
    text = noScripts(html);
  });

  it('is a real page, not a shell', () => {
    // The guard the old suite could not have: every public page used to serve
    // exactly eleven characters of body text to anything that does not run JS.
    expect(text.length).toBeGreaterThan(8000);
    expect(text).not.toContain('Cargando…');
  });

  describe('the lesson is content, not a description of content', () => {
    it('renders the real title', () => expect(text).toContain(demo.title));
    it('names the course as provenance', () => expect(text).toContain('Marketing con IA'));
    it('renders the key points', () => expect(text).toContain('metodología SMART'));
    it('renders the written guide itself', () =>
      // Not a link to it, not a promise of it: the guide's own prose.
      expect(text).toContain('Elige un proyecto que te importe'));
  });

  describe('the video costs nothing until it is asked for', () => {
    it('shows a play affordance, not a bare <video>', () => {
      expect(text).toMatch(/class="[^"]*videoplate/);
      expect(text).not.toMatch(/<video[^>]*src=/);
    });
    it('uses a real frame from the lesson as the poster', () => expect(text).toMatch(/demo-poster/));
    it('does not preload the video', () => expect(text).not.toMatch(/preload="(auto|metadata)"/));
    it('can expand the guide', () => expect(text).toMatch(/Seguir leyendo/));
  });

  describe('the question is the argument', () => {
    it('asks the real explain prompt', () => expect(text).toContain(demo.explain_prompt));
    it('gives them somewhere to answer', () => expect(text).toMatch(/<textarea[^>]*id="dq"/));
    it('labels the textarea by the question', () => expect(text).toMatch(/aria-labelledby="dqq"/));
    it('has the honeypot', () =>
      expect(text).toMatch(/aria-hidden="true"[^>]*left:-9999px|left:-9999px[^>]*aria-hidden/));
    it('promises a verdict, never a score', () => expect(text).toMatch(/No hay nota/));
    it('discloses storage honestly', () => expect(text).toMatch(/Guardamos lo que escribes/));
  });

  describe('reachability', () => {
    // The finish review caught a page that offered NOTHING until a verdict
    // rendered. What this guards is that a visitor always has a way forward.
    // The doors are one primary plus a text link on purpose: three equal
    // choices at the decision point is no hierarchy at all.
    it('leads with the goal engine', () => expect(text).toMatch(/Dinos qué quieres ser/));
    it('offers a second way out', () => expect(text).toMatch(/o pide tu acceso/));
    it('every door is a real link a crawler can follow', () => {
      expect(text).toMatch(/href="\/oferta"/);
      expect(text).toMatch(/href="\/lista"/);
      expect(text).toMatch(/href="\/cursos"/);
      expect(text).toMatch(/href="\/login"/);
    });
    it('has no anchor without a destination', () => {
      // Five of six anchors on this page once had no href: they were divs with
      // click handlers, so they were neither focusable nor crawlable.
      const anchors = text.match(/<a\b[^>]*>/g) || [];
      expect(anchors.length).toBeGreaterThan(5);
      expect(anchors.filter((a) => !/href=/.test(a))).toEqual([]);
    });
  });

  describe('the document outline is not a course catalog', () => {
    // The homepage had 1 h1, 1 h2 and SEVENTEEN h3s, fourteen of them course
    // names — so its outline literally read as a marketplace, whatever the copy
    // said. The library is one sentence and a quiet link now, after the
    // decision rather than before it.
    it('has exactly one h1', () =>
      expect((text.match(/<h1\b/g) || []).length).toBe(1));
    it('does not list the catalog in headings', () =>
      expect((text.match(/<h3\b/g) || []).length).toBeLessThan(4));
  });

  describe('honesty — PRODUCT.md records that none of these exist', () => {
    it('fabricates no learner document', () =>
      expect(text).not.toMatch(/documento real de una alumna/i));
    it('invents no testimonial or customer count', () =>
      expect(text).not.toMatch(
        /(testimonio|alumnas? satisfech|\d+\s*(alumnos|estudiantes|usuarios)\b)/i));
    it('invents no pricing', () =>
      expect(text).not.toMatch(/(\$\s?\d+\s*\/\s*mes|precio|suscripción)/i));
    it('labels the sample document as an example', () =>
      // The only existing portfolio document belongs to a seeded account.
      expect(text).not.toMatch(/documento de (una|un) (alumna|alumno) real/i));
  });

  describe('regression guards', () => {
    it('leaks no undefined', () => expect(text).not.toMatch(/\bundefined\b/));
    it('leaks no [object Object]', () => expect(text).not.toContain('[object Object]'));
    it('renders no unresolved template literal', () => expect(text).not.toMatch(/\$\{/));
  });
});

describe('the built public site', () => {
  const page = (route) => {
    const file = path.join(DIST, route, 'index.html');
    return fs.existsSync(file) ? noScripts(fs.readFileSync(file, 'utf8')) : null;
  };

  it('builds every public route', () => {
    for (const route of ['cursos', 'oferta', 'lista', 'login']) {
      expect(page(route), `${route} did not build`).toBeTruthy();
    }
  });

  it('builds one page per course in the export', () => {
    const built = fs.readdirSync(path.join(DIST, 'curso'));
    expect(built.sort()).toEqual(catalog.courses.map((c) => c.slug).sort());
  });

  it('ships the catalog as links, with no JavaScript at all', () => {
    const cursos = page('cursos');
    // Derived, not typed: this line said 14 while the catalog held 15.
    expect((cursos.match(/href="\/curso\//g) || []).length).toBe(catalog.courses.length);
    const raw = fs.readFileSync(path.join(DIST, 'cursos/index.html'), 'utf8');
    expect(raw).not.toMatch(/<script/);
  });

  it('argues the deliverable before the lesson count on a temario', () => {
    const meta = page('curso/curso-meta-ads');
    expect(meta).toContain('Plan de campaña');
    expect(meta.indexOf('Terminas con')).toBeLessThan(meta.indexOf('Módulo 1'));
  });

  it('says on /oferta what it will not teach', () => {
    // The gap report is the one claim a competitor cannot truthfully copy, and
    // it existed only in the server-rendered copy of this page before.
    expect(page('oferta')).toMatch(/no enseñamos|no lo cubre/);
  });

  it('loads no third-party script on any public page', () => {
    for (const route of ['', 'cursos', 'oferta', 'lista', 'login']) {
      const file = path.join(DIST, route, 'index.html');
      expect(fs.readFileSync(file, 'utf8'), route).not.toContain('cdn.jsdelivr.net');
    }
  });
});

describe('the wide grid places every section', () => {
  /* THE BUG THIS EXISTS FOR, and it reached production.
   *
   * `body.wide .app > *` puts each direct child of the shell in the text
   * column. Astro renders an island as `<astro-island>` with
   * `display: contents`, so the island is NOT a grid item — its CHILDREN become
   * the grid items, and they carry no column of their own. They land in the
   * implicit track past `full-end`, which rendered /oferta, /lista and /login
   * as a 32px strip against the right edge of the screen.
   *
   * Every content assertion passed the whole time. The words were all there; a
   * reader could not get at them. So this checks STRUCTURE, which is what was
   * actually wrong — and it is why the landing survived: its islands are nested
   * inside sections rather than sitting at the top level.
   *
   * Parsed with jsdom rather than a regex. The first version of this guard
   * counted tags by hand, miscounted `<path></path>` and script bodies full of
   * angle brackets, and reported a clean pass on the exact page that was broken.
   * A guard that cannot be trusted is worse than none.
   */
  /* Only pages on the WIDE GRID, which is where the invariant actually lives.
     `body.wide .app` is a named-line grid whose direct children take columns;
     the app's shell is a plain flex column with no named tracks, and there a
     `display:contents` island passing its children through to the flex parent
     is both intentional and what gives the app its inter-card gap. Encoding the
     condition beats keeping a list of exempt pages, which would go stale. */
  const parse = (html) => new JSDOM(html).window.document;
  const usesWideGrid = (doc) => doc.body.classList.contains('wide');
  const topLevelIslands = (html) => {
    const doc = parse(html);
    if (!usesWideGrid(doc)) return 0;
    return doc.querySelectorAll('main.app > astro-island').length;
  };

  it('never puts an island at the top level of the wide grid', () => {
    const offenders = [];
    let checked = 0;
    for (const route of ['', 'cursos', 'oferta', 'lista', 'login', 'curso/curso-meta-ads', 'aprende']) {
      const file = path.join(DIST, route, 'index.html');
      if (!fs.existsSync(file)) continue;
      const html = fs.readFileSync(file, 'utf8');
      if (usesWideGrid(parse(html))) checked += 1;
      if (topLevelIslands(html) > 0) offenders.push(route || '/');
    }
    // The condition must actually be matching pages, or this asserts nothing.
    expect(checked, 'no page was found on the wide grid').toBeGreaterThan(3);
    expect(offenders,
      'wrap the island in an element so the grid has something to place').toEqual([]);
  });

  it('can tell a top-level island from a nested one', () => {
    // Guards the guard: the assertion above passes trivially on a parser that
    // never finds anything, which is exactly how its first version failed.
    const wrap = (inner) => `<body class="wide"><main class="app">${inner}</main></body>`;
    expect(topLevelIslands(wrap('<astro-island></astro-island>'))).toBe(1);
    expect(topLevelIslands(wrap('<div><astro-island></astro-island></div>'))).toBe(0);
    expect(topLevelIslands(wrap('<script>if(a<b&&c>d){}</script><astro-island></astro-island>'))).toBe(1);
    expect(topLevelIslands(wrap('<svg><path d="M0 0"></path></svg><astro-island></astro-island>'))).toBe(1);
    // And a page that is not on the grid is not this rule's business.
    expect(topLevelIslands('<body><main class="app"><astro-island></astro-island></main></body>')).toBe(0);
  });
});


/* Every number the public site says about its own size.
 *
 * These were typed by hand and went stale the way typed numbers do: the landing
 * said "70 módulos en 14 cursos" and the analyser's two-minute progress copy
 * said "las 210 lecciones · 35 módulos" — a seven-course catalog's figures still
 * on screen at fifteen courses and 450 lessons. Both now read `totals.json`,
 * which `export_web.py` writes from the database, so the only way to be wrong
 * is to have a stale export — and `export_web.py --check` already fails on that.
 *
 * This block exists so nobody types one back in. */
describe('the catalog counts itself', () => {
  const page = (route) => {
    const file = path.join(DIST, route, 'index.html');
    return fs.existsSync(file) ? noScripts(fs.readFileSync(file, 'utf8')) : '';
  };

  it('agrees with the catalog it was derived from', () => {
    expect(totals.courses).toBe(catalog.courses.length);
    expect(totals.modules).toBe(
      catalog.courses.reduce((n, c) => n + c.modules, 0));
    expect(totals.lessons).toBe(
      catalog.courses.reduce((n, c) => n + c.total, 0));
  });

  it('is a catalog worth counting', () => {
    // Guards the guard: every assertion here passes on an empty export.
    expect(totals.courses).toBeGreaterThan(1);
    expect(totals.lessons).toBeGreaterThan(totals.modules);
    expect(totals.modules).toBeGreaterThan(totals.courses);
  });

  it('says the same size on the landing as in the data', () => {
    const home = page('');
    expect(home).toContain(`${totals.modules} módulos`);
    expect(home).toContain(`en ${totals.courses} cursos`);
  });

  it('tells the analyser the same size while it waits', () => {
    const stage = JOB_STAGES.find(([at]) => at === 34);
    expect(stage[1]).toBe(`Cruzando con las ${totals.lessons} lecciones`);
    expect(stage[2]).toContain(`Los ${totals.modules} módulos`);
  });

  it('leaves no seven-course-era number anywhere on the public site', () => {
    // The actual figures that were live: 14 courses, 70/35 modules, 210/420
    // lessons. A page may legitimately contain "420" one day; it may not
    // contain it as a count of our lessons or modules.
    const stale = new RegExp('\\b(?:14|15) cursos\\b|\\b(?:70|35|75) módulos\\b|\\b(?:210|420|450) lecciones\\b', 'g');
    for (const route of ['', 'cursos', 'oferta', 'lista', 'login']) {
      for (const hit of page(route).match(stale) || []) {
        const [n] = hit.split(' ');
        const ok = Number(n) === totals.courses
          || Number(n) === totals.modules
          || Number(n) === totals.lessons;
        expect(ok, `/${route} says "${hit}" and the catalog does not`).toBe(true);
      }
    }
  });
});
