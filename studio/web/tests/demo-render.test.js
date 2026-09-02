/* The public demo: the free lesson, the verdict, and the doors out.
 *
 * This surface's whole argument is that a stranger gets a REAL verdict from the
 * REAL evaluator on their own words before meeting any wall. So these assert
 * that the lesson is content rather than a description of content, that the
 * verdict is a word and never a number, and — the group that matters most —
 * that the page claims no testimonial, no customer count and no price, because
 * PRODUCT.md records that none of those exist.
 *
 * Ported from studio/dashboard/check_demo_render.js — assertions unchanged.
 */
import { describe, it, expect, beforeAll } from 'vitest';
import { loadSpa, DEMO_PAYLOAD as demo } from './harness.js';

describe('public demo surface', () => {
  let spa, lesson, failed, verdict, doorsLit, doorsGhost;

  beforeAll(async () => {
    spa = loadSpa();
    spa.sandbox.__demo = demo;

    spa.setApi('async () => __demo');
    lesson = await spa.runAsync('renderDemoLesson(app)');

    spa.setApi('async () => ({detail:"nope"})');
    failed = await spa.runAsync('renderDemoLesson(app)');
    spa.setApi('async () => __demo');

    verdict = spa.run(`renderDemoVerdict(app, ${JSON.stringify({
      verdict: 'casi', feedback: 'Vas bien, pero te falta el plazo.',
      misconception: 'SMART no es solo "ser específico".',
      missing: ['un número', 'una fecha'],
    })}, ${JSON.stringify(demo)})`);

    doorsLit = spa.returned('landingDoors("lit")');
    doorsGhost = spa.returned('landingDoors("ghost")');
  });

  describe('the lesson is content, not a description of content', () => {
    it('renders the real title', () => expect(lesson).toContain(demo.title));
    it('names the course as provenance', () => expect(lesson).toContain('Marketing con IA'));
    it('renders the key points', () => expect(lesson).toContain('metodología SMART'));

    // A <video> with preload buffers 5.4MB on a marketing page aimed at people
    // on metered mobile data. The plate is a real frame plus our own affordance.
    it('shows a play affordance, not a bare <video>', () => {
      expect(lesson).toMatch(/videoplate/);
      expect(lesson).not.toMatch(/<video/);
    });
    it('uses a real frame from the lesson as the poster', () => expect(lesson).toMatch(/demo-poster/));
    it('does not preload the video', () => expect(lesson).not.toMatch(/preload="(auto|metadata)"/));

    it('can expand the guide', () => expect(lesson).toMatch(/Seguir leyendo/));
  });

  describe('the question is the argument', () => {
    it('asks the real explain prompt', () => expect(lesson).toContain(demo.explain_prompt));
    it('gives them somewhere to answer', () => expect(lesson).toMatch(/<textarea[^>]*id="dq"/));
    it('labels the textarea by the question', () => expect(lesson).toMatch(/aria-labelledby="dqq"/));
    it('has the honeypot', () => expect(lesson).toMatch(/id="dqc"/));
    // Putting a number on a comprehension check is a category error this
    // product already made once (docs/02).
    it('promises a verdict, never a score', () => expect(lesson).toMatch(/No hay nota/));
    it('discloses storage honestly', () => expect(lesson).toMatch(/Guardamos lo que escribes/));
  });

  describe('the verdict', () => {
    it('is a word, not a number', () => {
      expect(verdict).toMatch(/Casi/);
      expect(verdict).not.toMatch(/\/100/);
    });
    it('renders the tutor feedback', () => expect(verdict).toContain('te falta el plazo'));
    it('surfaces a misconception', () => expect(verdict).toContain('SMART no es solo'));
    it('names what is missing', () => {
      expect(verdict).toContain('un número');
      expect(verdict).toContain('una fecha');
    });
    it('announces the region to a screen reader', () => expect(lesson).toMatch(/aria-live/));
  });

  describe('what follows the verdict is real content, not claims', () => {
    it('numbers the rows it actually shows', () => expect(verdict).toMatch(/dos de los cinco pasos/));
    it("shows this lesson's real exercise", () =>
      expect(verdict).toContain('Elige tu proyecto real y redacta'));
    it("shows this module's real reto", () => expect(verdict).toContain('pastelería en Bogotá'));
    it('names the real document type', () => expect(verdict).toContain('Estrategia de marketing digital'));
    it('promises no certificate', () => expect(verdict).toMatch(/No damos certificados/));
  });

  describe('reachability', () => {
    // The finish review caught a page that offered NOTHING until a verdict
    // rendered. What this guards is that a visitor always has a way forward —
    // not a button count. The doors went from three equal buttons to one
    // primary plus a text link on purpose: three equal choices at the decision
    // point is no hierarchy at all.
    it('leads with the goal engine', () => expect(doorsLit).toMatch(/Dinos qué quieres ser/));
    it('offers a second way out', () => expect(doorsLit).toMatch(/o pide tu acceso/));
    it('has a door set for the page tail', () => expect(doorsGhost).toMatch(/Dinos qué quieres ser/));
    it('does not stack equal buttons at the close', () =>
      expect((doorsLit.match(/<button/g) || []).length).toBe(1));
    it('gives the primary treatment only to the lit set', () => {
      expect(doorsLit).toMatch(/btn-primary/);
      expect(doorsGhost).not.toMatch(/btn-primary/);
    });
    it('still offers somewhere to go when the demo fails', () =>
      expect(failed).toMatch(/Dinos qué quieres ser/));
    it('says plainly that it failed', () => expect(failed).toMatch(/no está disponible/));
  });

  describe('honesty — PRODUCT.md records that none of these exist', () => {
    it('fabricates no learner document', () =>
      expect(lesson + verdict).not.toMatch(/documento real de una alumna/i));
    it('invents no testimonial or customer count', () =>
      expect(lesson + verdict).not.toMatch(
        /(testimonio|alumnas? satisfech|\d+\s*(alumnos|estudiantes|usuarios)\b)/i));
    it('invents no pricing', () =>
      expect(lesson + verdict).not.toMatch(/(\$\s?\d+\s*\/\s*mes|precio|suscripción)/i));
  });

  describe('regression guards', () => {
    it('leaks no undefined', () =>
      expect(lesson + verdict + doorsLit + failed).not.toMatch(/\bundefined\b/));
    it('leaks no [object Object]', () =>
      expect(lesson + verdict + doorsLit + failed).not.toContain('[object Object]'));
  });
});

/* Routing is asserted in its own sandbox because it needs a different `window`.
 *
 * A server URL (/login, /oferta, /curso/<slug>) tells the SPA which view to open
 * first. That hint used to be re-read on every route(), which made it sticky:
 * "#/" normalises to an empty segment, empty is falsy, so on /login every
 * attempt to go home fell back to the hint and re-rendered login. "‹ Conocer
 * Rumbo" and the waitlist's "‹ Volver" were both dead ends. The invariant: the
 * hint applies to the FIRST render only, after which the hash is the authority —
 * empty included, and empty means the landing.
 */
describe('the server-named view is consumed exactly once', () => {
  it('reads the hint, then clears it', () => {
    const spa = loadSpa();
    // renderLogin reads the query string; without this the view throws, and
    // because route() is async it surfaces as an unhandled rejection.
    spa.sandbox.URLSearchParams = URLSearchParams;
    // __serverView is captured when the script evaluates, so set it directly to
    // model "the server named a view for this request".
    spa.evaluate('__serverView = "login"');
    expect(spa.evaluate('__serverView')).toBe('login');

    const p = spa.evaluate('route()');
    if (p && typeof p.catch === 'function') p.catch(() => {});   // assert routing, not render

    // Cleared synchronously at the top of route(), before any await.
    expect(spa.evaluate('__serverView')).toBe('');
  });
});
