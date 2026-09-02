// @vitest-environment jsdom
/* CV intake: the paste box, the proposals, and the temario that honours them.
 *
 * docs/10's whole contract is that a CV PROPOSES and a reto DISPOSES. A claim
 * is not evidence, a skip is not a lock, and a credited module was earned by
 * passing a reto so nothing may take it back. Those are one word away from
 * being violated by a copy edit, which is why they are asserted here.
 *
 * Assertions unchanged from the DOM-shim version; the subject is now the
 * components that replaced renderCvBox / renderCvResult / viewOutline.
 */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, waitFor, cleanup } from '@testing-library/svelte';
import Cv from '../src/components/app/views/Cv.svelte';
import CvClaim from '../src/components/app/views/CvClaim.svelte';
import Outline from '../src/components/app/views/Outline.svelte';

const claim = (over = {}) => ({
  course_slug: 'curso-meta-ads', course_title: 'Meta Ads', module_no: 1,
  module_title: 'Cuenta y pixel', outcome: 'Sabrás dejar la cuenta midiendo de verdad.',
  capability: 'instaló el pixel', evidence: 'Instalé el pixel en 12 tiendas Shopify',
  confidence: 'alta', lessons: 6, proposed: true, state: 'pendiente', exempt_score: null,
  ...over,
});

const BASE = { exists: true, pass_score: 70, created_at: '2026-08-26' };

/* A component's textContent carries the template's own line breaks and
   indentation, so a sentence that wraps in the source arrives with newlines
   inside it. Normalising is not cosmetic: without it an assertion fails on how
   the markup is formatted rather than on what the page says. */
const flat = (el) => (typeof el === 'string' ? el : el.textContent).replace(/\s+/g, ' ').trim();


/** Stub the endpoints a view calls, keyed by path suffix. */
function stubApi(routes) {
  vi.stubGlobal('fetch', vi.fn(async (url) => {
    const key = Object.keys(routes).find((k) => String(url).includes(k));
    return { ok: true, status: 200, json: async () => (key ? routes[key] : {}) };
  }));
}

async function cvScreen(payload) {
  stubApi({ '/cv': payload });
  const { container } = render(Cv);
  await waitFor(() => expect(container.textContent.length).toBeGreaterThan(80));
  return flat(container);
}

beforeEach(() => { window.matchMedia ??= () => ({ matches: false }); });
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe('the paste box', () => {
  let box;
  beforeEach(async () => { box = await cvScreen({ exists: false }); });

  it('has a textarea', () => expect(screen.getByLabelText('Tu CV')).toBeTruthy());
  it('has the honeypot', () =>
    expect(document.querySelector('input[aria-hidden="true"]')).toBeTruthy());
  it('declares the wait up front', () => expect(box).toMatch(/cerca de un minuto/));
  it('tells them not to close the tab', () => expect(box).toMatch(/No cierres esta pesta/));
  it('promises contact stripping', () => expect(box).toMatch(/correo y tu tel/));
  it('promises the CV stays out of the document', () =>
    expect(box).toMatch(/solo va trabajo tuyo evaluado/));
  it('says the learner decides', () => expect(box).toMatch(/T[úu] decides/));
  it('asks what they DID, not their titles', () => expect(box).toMatch(/qu[ée] hiciste/));
});

describe('the proposals', () => {
  let out;
  beforeEach(async () => {
    out = await cvScreen({
      ...BASE, headline: 'Media buyer senior', years_experience: 5,
      proposed_modules: 3, proposed_lessons: 18,
      claims: [
        claim(),
        claim({ module_no: 2, state: 'declarado' }),
        claim({ module_no: 4, state: 'acreditado', exempt_score: 85 }),
        claim({ module_no: 3, confidence: 'baja', proposed: false, capability: 'mencionó creatividades' }),
      ],
      fuera_del_catalogo: [{ name: 'Inglés C1', evidence: 'certificado C1' }],
    });
  });

  it('renders the headline', () => expect(out).toContain('Media buyer senior'));
  it('shows the module outcome, not a lesson list', () =>
    expect(out).toContain('Sabrás dejar la cuenta midiendo de verdad.'));
  it('quotes the CV verbatim', () =>
    expect(out).toContain('Instalé el pixel en 12 tiendas Shopify'));
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

  describe('a weak claim', () => {
    it('is separated out', () => expect(out).toMatch(/no alcanza para salt/));
    it('can still be earned via the reto', () => expect(out).toMatch(/se acredita solo/));
  });

  describe('regression guards', () => {
    it('leaks no undefined', () => expect(out).not.toMatch(/\bundefined\b/));
    it('leaks no [object Object]', () => expect(out).not.toContain('[object Object]'));
    // A skipped module is COLLAPSED, never locked. "Bloqueado" here would be a
    // lie about what the learner chose.
    it('never calls a skipped module blocked', () => expect(out).not.toMatch(/bloquead/i));
  });
});

describe('a credited module', () => {
  // Rendered ALONE on purpose: with several cards in one string, "is there an
  // undo button" cannot be attributed to a particular one.
  let credited;
  beforeEach(() => {
    const { container } = render(CvClaim, {
      claim: claim({ module_no: 4, state: 'acreditado', exempt_score: 85 }),
      passScore: 70,
    });
    credited = flat(container);
  });

  it('shows its score', () => expect(credited).toMatch(/Acreditado 85/));
  // It was earned by passing a reto. Nothing on this screen may take it back.
  it('is NOT undoable', () => expect(credited).not.toMatch(/Mejor ens[ée][ñn]amelo/));
  it('offers no skip button either', () => expect(credited).not.toMatch(/s[áa]ltalo/i));
  it('stays open', () => expect(credited).toMatch(/sigue abierto/));
});

describe('when nothing can be cited', () => {
  it('says so plainly, and explains the evidence rule', async () => {
    const none = await cvScreen({
      ...BASE, headline: 'Sin coincidencias', years_experience: 2,
      proposed_modules: 0, proposed_lessons: 0, claims: [], fuera_del_catalogo: [],
    });
    expect(none).toMatch(/no dice nada malo de tu experiencia/);
    expect(none).toMatch(/sin cita no damos nada por sabido/);
  });
});

describe('the temario honours the exemption', () => {
  let temario;
  beforeEach(async () => {
    stubApi({
      '/course/': {
        slug: 'curso-meta-ads', title: 'Meta Ads', description: '', done: 0, total: 12,
        modules: [
          {
            module_no: 1, module_title: 'Cuenta y pixel', module_description: '',
            exempt: 'declarado',
            lessons: [{ id: 1, position: 1, title: 'El pixel', status: 'current', objectives: '' }],
            capstone: { id: 9, title: 'Reto: medir de verdad', status: 'available', test_out: true },
          },
          {
            module_no: 2, module_title: 'Campañas', module_description: '',
            lessons: [{ id: 2, position: 2, title: 'Estructura', status: 'locked', objectives: 'x' }],
            capstone: null,
          },
        ],
      },
      '/project-doc/': { detail: 'none' },
      '/case-study/': { detail: 'none' },
    });
    const { container } = render(Outline, { slug: 'curso-meta-ads' });
    await waitFor(() => expect(container.textContent).toContain('Meta Ads'));
    temario = flat(container);
  });

  it('flags the skipped module', () => expect(temario).toMatch(/Ya lo sabes/));
  it('still lets it be opened', () => expect(temario).toMatch(/Ver igual/));
  // The ask was "no me hagas ver de nuevo lo que ya sé". Collapsed answers it;
  // locked would answer a different, worse question.
  it('never calls a skipped module locked', () =>
    expect(temario).not.toMatch(/Ya lo sabes[\s\S]{0,80}Bloqueada/));
  it('offers its reto as the way to credit it', () =>
    expect(temario).toMatch(/Acredita este m[óo]dulo/));
  it('leaves a normal module untouched', () => {
    expect(temario).toContain('Campañas');
    expect(temario).toContain('Bloqueada'); // module 2 genuinely is
  });
});
