/* CV intake: the paste box, the proposals, and the temario that honours them.
 *
 * docs/10's whole contract is that a CV PROPOSES and a reto DISPOSES. A claim
 * is not evidence, a skip is not a lock, and a credited module was earned by
 * passing a reto so nothing may take it back. Those are one-word-away from
 * being violated by a copy edit, which is why they are asserted here.
 *
 * Ported from studio/dashboard/check_cv_render.js — assertions unchanged.
 */
import { describe, it, expect, beforeAll } from 'vitest';
import { loadSpa } from './harness.js';

const claim = (over = {}) => ({
  course_slug: 'curso-meta-ads', course_title: 'Meta Ads', module_no: 1,
  module_title: 'Cuenta y pixel', outcome: 'Sabrás dejar la cuenta midiendo de verdad.',
  capability: 'instaló el pixel', evidence: 'Instalé el pixel en 12 tiendas Shopify',
  confidence: 'alta', lessons: 6, proposed: true, state: 'pendiente', exempt_score: null,
  ...over,
});

const BASE = { exists: true, pass_score: 70, created_at: '2026-08-26' };

describe('CV intake', () => {
  let spa, box, out, credited, none, temario;

  beforeAll(async () => {
    spa = loadSpa();
    box = spa.run('renderCvBox()');

    out = spa.run(`renderCvResult(${JSON.stringify({
      ...BASE, headline: 'Media buyer senior', years_experience: 5,
      proposed_modules: 3, proposed_lessons: 18,
      claims: [
        claim(),
        claim({ module_no: 2, state: 'declarado' }),
        claim({ module_no: 4, state: 'acreditado', exempt_score: 85 }),
        claim({ module_no: 3, confidence: 'baja', proposed: false, capability: 'mencionó creatividades' }),
      ],
      fuera_del_catalogo: [{ name: 'Inglés C1', evidence: 'certificado C1' }],
    })})`);

    // Rendered ALONE on purpose: the harness captures a flat stream, so with
    // several cards in it "is there an undo button" cannot be attributed to one.
    credited = spa.run(`renderCvResult(${JSON.stringify({
      ...BASE, headline: 'X', years_experience: 5, proposed_modules: 1, proposed_lessons: 6,
      claims: [claim({ state: 'acreditado', exempt_score: 85 })], fuera_del_catalogo: [],
    })})`);

    none = spa.run(`renderCvResult(${JSON.stringify({
      ...BASE, headline: 'Asistente administrativa', years_experience: 1,
      proposed_modules: 0, proposed_lessons: 0, claims: [], fuera_del_catalogo: [],
    })})`);

    spa.sandbox.__outline = {
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
    spa.setApi('async (p) => p.indexOf("/course/") === 0 ? __outline : ({exists:false, eligible:false})');
    // viewOutline awaits its payload, unlike every other render here.
    temario = await spa.runAsync('viewOutline("curso-meta-ads")');
  });

  describe('the paste box', () => {
    it('has a textarea', () => expect(box).toMatch(/<textarea[^>]*id="cvtext"/));
    it('has the honeypot', () => expect(box).toMatch(/id="cvcompany"/));
    it('declares the wait up front', () => expect(box).toMatch(/cerca de un minuto/));
    it('tells them not to close the tab', () => expect(box).toMatch(/No cierres esta pesta/));
    it('promises contact stripping', () => expect(box).toMatch(/correo y tu tel/));
    it('promises the CV stays out of the document', () =>
      expect(box).toMatch(/solo va trabajo tuyo evaluado/));
    it('says the learner decides', () => expect(box).toMatch(/T[úu] decides/));
    it('asks what they DID, not their titles', () => expect(box).toMatch(/qu[ée] hiciste/));
  });

  describe('the proposals', () => {
    it('renders the headline', () => expect(out).toContain('Media buyer senior'));
    it('shows the module outcome, not a lesson list', () =>
      expect(out).toContain('Sabrás dejar la cuenta midiendo'));
    // The matcher was caught paraphrasing instead of quoting; quotes are now
    // dropped server-side unless they appear literally in the CV.
    it('quotes the CV verbatim', () => expect(out).toContain('Instalé el pixel en 12 tiendas Shopify'));
    it('offers the skip on a pending claim', () => expect(out).toMatch(/Ya lo s[ée], s[áa]ltalo/));
    it('offers to keep the lessons instead', () => expect(out).toMatch(/Prefiero verlo igual/));
    it('offers the reto on a declared claim', () => expect(out).toMatch(/Pru[ée]balo con el reto/));
    it('lets a declared claim be undone', () => expect(out).toMatch(/Mejor ens[ée][ñn]amelo/));
    it('describes the reto as an uncovered case', () =>
      expect(out).toMatch(/caso nuevo que las lecciones no cubren/));
    it('states the pass bar', () => expect(out).toContain('70+'));
    it('shows outside-catalog strengths', () => expect(out).toContain('Inglés C1'));
    it('lets the CV be deleted', () => expect(out).toMatch(/Borrar mi CV/));
    it('repeats the document boundary', () => expect(out).toMatch(/solo va trabajo tuyo evaluado/));
  });

  describe('a credited module was earned, so nothing takes it back', () => {
    it('shows its score', () => expect(credited).toMatch(/Acreditado 85/));
    it('is NOT undoable', () => expect(credited).not.toMatch(/Mejor ens[ée][ñn]amelo/));
    it('offers no skip button either', () => expect(credited).not.toMatch(/s[áa]ltalo/i));
    it('stays open', () => expect(credited).toMatch(/sigue abierto/));
  });

  describe('low confidence is not a proposal', () => {
    it('is separated out', () => expect(out).toMatch(/no alcanza para salt/));
    it('can still be earned via the reto', () => expect(out).toMatch(/se acredita solo/));
  });

  describe('an empty reading is not a verdict on the person', () => {
    it('says so plainly', () => expect(none).toMatch(/no dice nada malo de tu experiencia/));
    it('explains the evidence rule', () => expect(none).toMatch(/sin cita no damos nada por sabido/));
  });

  describe('the temario honours a skip without locking anything', () => {
    it('did not throw', () => expect(temario.startsWith('THREW')).toBe(false));
    it('flags the skipped module', () => expect(temario).toMatch(/Ya lo sabes/));
    it('still lets it be opened', () => expect(temario).toMatch(/Ver igual/));
    /* This guard is NARROW ON PURPOSE and must stay narrow.
     *
     * I broadened it during the port to `not.toMatch(/bloquead/i)` over the
     * whole temario, on the reasoning that broader is safer. It is not: module 2
     * in the fixture has genuinely locked lessons and a locked reto, and a
     * module you have not reached IS locked. The broad version failed on
     * correct output.
     *
     * The word is only wrong when it lands on a SKIPPED module, so the
     * assertion is scoped by adjacency to that card. The flat capture stream
     * the harness produces is why it is adjacency rather than a DOM query —
     * when this screen becomes a component, scope it to the card properly and
     * this comment can go.
     */
    it('never calls a skipped module locked', () =>
      expect(temario).not.toMatch(/Te saltaste este m[óo]dulo[\s\S]{0,120}Bloquead/));
    it('offers its reto as the way to credit it', () => expect(temario).toMatch(/Acredita este m[óo]dulo/));
    it('leaves a normal module untouched', () => {
      expect(temario).toMatch(/P[úu]blicos guardados/);
      expect(temario).toMatch(/Reto: arma tus p[úu]blicos/);
    });
  });

  describe('regression guards', () => {
    it('leaks no undefined', () => expect(out + box + none).not.toMatch(/\bundefined\b/));
    it('leaks no [object Object]', () =>
      expect(out + box + none + credited).not.toContain('[object Object]'));
    // The word that must never appear. A skip is not a lock, and the moment the
    // copy says it is, the feature has become the thing docs/10 refuses to build.
    it('never calls a skipped module blocked', () => expect(out).not.toMatch(/bloquead/i));
  });
});
