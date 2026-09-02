// @vitest-environment jsdom
/* The job analyser: the paste box and the route it renders.
 *
 * docs/08 calls this the acquisition asset — it carries the only claim a
 * competitor cannot truthfully make, that we name what the posting demands and
 * we do NOT teach. So the honesty line and the gap list are asserted, not
 * assumed, and so is the wait: the analysis really takes about two minutes and
 * the page has to say so before anyone commits to it.
 *
 * Assertions unchanged from the DOM-shim version. What changed is that they now
 * drive the real component with a stubbed fetch, so they cover the flow as well
 * as the markup — including that the same component serves a stranger and a
 * signed-in learner with different endings.
 */
import { describe, it, expect, beforeAll, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor, cleanup } from '@testing-library/svelte';
import fs from 'node:fs';
import path from 'node:path';
import JobAnalyser from '../src/components/JobAnalyser.svelte';
import { JOB_STAGES, JOB_SLOW_AT, modLabel } from '../src/lib/route.js';
import { REPO } from './harness.js';

const FIXTURE = path.join(REPO, 'studio/fixtures/job-postings/sample-analysis.json');
const analysis = JSON.parse(fs.readFileSync(FIXTURE, 'utf8')).analysis;

const POSTING = 'x'.repeat(400); // past the 200-char minimum

/* A component's textContent carries the template's own line breaks and
   indentation, so a sentence that wraps in the source arrives with newlines
   inside it. Normalising is not cosmetic: without it an assertion fails on how
   the markup is formatted rather than on what the page says. */
const flat = (el) => (typeof el === 'string' ? el : el.textContent).replace(/\s+/g, ' ').trim();


async function analyse({ token = 'TESTTOKEN123', signedIn = false, progress = null } = {}) {
  vi.stubGlobal('fetch', vi.fn(async () => ({
    ok: true, status: 200, json: async () => ({ analysis, token, progress }),
  })));
  const { container } = render(JobAnalyser, { signedIn });
  await fireEvent.input(screen.getByLabelText(/La oferta de trabajo/), {
    target: { value: POSTING },
  });
  await fireEvent.click(screen.getByRole('button', { name: /Armar mi ruta/ }));
  await waitFor(() => expect(screen.getByText(/Cubrimos/)).toBeTruthy());
  return flat(container);
}

afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe('the paste box', () => {
  beforeAll(() => vi.stubGlobal('fetch', vi.fn()));

  it('has a textarea', () => {
    render(JobAnalyser);
    expect(screen.getByLabelText(/La oferta de trabajo/)).toBeTruthy();
  });

  it('offers the goal-only mode, with its own input', async () => {
    render(JobAnalyser);
    await fireEvent.click(screen.getByRole('tab', { name: /Solo sé el puesto/ }));
    expect(screen.getByLabelText(/El puesto o la habilidad/)).toBeTruthy();
  });

  it('has the honeypot', () => {
    const { container } = render(JobAnalyser);
    expect(container.querySelector('input[aria-hidden="true"]')).toBeTruthy();
  });

  // A two-minute wait that is not declared is a bounce. This is the one
  // interaction the whole category gets wrong.
  it('declares the wait up front', () => {
    const { container } = render(JobAnalyser);
    expect(flat(container)).toMatch(/dos minutos/);
  });

  it('tells them not to close the tab', () => {
    const { container } = render(JobAnalyser);
    expect(flat(container)).toMatch(/No cierres esta pesta/);
  });

  it('refuses to spend two minutes on four words', async () => {
    const f = vi.fn();
    vi.stubGlobal('fetch', f);
    render(JobAnalyser);
    await fireEvent.input(screen.getByLabelText(/La oferta de trabajo/), { target: { value: 'hola' } });
    await fireEvent.click(screen.getByRole('button', { name: /Armar mi ruta/ }));
    await waitFor(() => expect(screen.getByText(/Pega la oferta completa/)).toBeTruthy());
    expect(f).not.toHaveBeenCalled();
  });
});

describe('the progress stages', () => {
  it('defines at least four stages', () => expect(JOB_STAGES.length).toBeGreaterThanOrEqual(4));
  it('starts at 0s', () => expect(JOB_STAGES[0][0]).toBe(0));
  it('ascends', () =>
    JOB_STAGES.forEach((s, i) => {
      if (i) expect(s[0]).toBeGreaterThan(JOB_STAGES[i - 1][0]);
    }));
  it('explains every stage', () =>
    JOB_STAGES.forEach((s) => {
      expect(s[1].length).toBeGreaterThan(8);
      expect(s[2].length).toBeGreaterThan(20);
    }));
  it('puts the slow threshold past the last stage', () =>
    expect(JOB_SLOW_AT).toBeGreaterThan(JOB_STAGES[JOB_STAGES.length - 1][0]));
});

describe('the result', () => {
  let out;
  beforeAll(async () => { out = await analyse(); });

  it('names the role', () => expect(out).toContain(analysis.role_title));
  it('states coverage', () => expect(out).toContain(`Cubrimos ${analysis.coverage}%`));

  it('separates núcleo from later', () => {
    expect(out).toContain('Empieza por aquí');
    if (analysis.ruta.some((r) => r.phase !== 'nucleo')) {
      expect(out).toContain('Después, para completar el perfil');
    }
  });

  it('shows every course on the route', () =>
    analysis.ruta.forEach((r) => expect(out).toContain(r.course_title)));

  it('labels every module selection correctly', () =>
    analysis.ruta.forEach((r) => expect(out).toContain(modLabel(r))));

  it('names what we do not cover', () => {
    // The single most defensible thing this surface says.
    if (analysis.gaps.length) {
      expect(out).toContain('no lo cubrimos');
      analysis.gaps.forEach((g) => expect(out).toContain(g.name));
    }
  });

  it('names the document', () => {
    if (analysis.doc_type) expect(out).toContain(analysis.doc_type);
  });

  describe('the share card', () => {
    it('appears when a token exists', () => expect(out).toMatch(/Comparte esta ruta/));
    it('is absent without one', async () => {
      cleanup();
      const noToken = await analyse({ token: '' });
      expect(noToken).not.toMatch(/Comparte esta ruta/);
    });
  });

  describe('regression guards', () => {
    it('leaks no undefined', () => expect(out).not.toMatch(/\bundefined\b/));
    it('leaks no [object Object]', () => expect(out).not.toContain('[object Object]'));
  });
});

describe('who is reading it', () => {
  it('offers a stranger the door', async () => {
    const out = await analyse({ signedIn: false });
    expect(out).toMatch(/Quiero esta ruta|Avísame cuando lo cubran/);
    expect(out).not.toMatch(/Hacer este mi objetivo/);
  });

  it('offers a learner a decision', async () => {
    const out = await analyse({ signedIn: true });
    expect(out).toMatch(/Hacer este mi objetivo/);
    expect(out).not.toMatch(/Tengo una invitación/);
  });

  it('tells a learner their finished work carries over', async () => {
    // Changing objective is non-destructive, and saying so BEFORE they decide is
    // the difference between switching and believing they start over.
    const out = await analyse({ signedIn: true, progress: { done: 7, total: 24 } });
    expect(out).toMatch(/No empiezas de cero/);
    expect(out).toContain('7 de 24');
  });
});
