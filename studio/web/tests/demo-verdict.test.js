// @vitest-environment jsdom
/* The verdict: the one thing on the public site that has to be alive.
 *
 * A stranger writes their own explanation and the REAL evaluator answers it
 * before they meet any wall. That is the surface's whole argument, so what it
 * does with the answer is worth testing properly rather than by reading markup.
 *
 * These assertions came from the SPA's renderDemoVerdict() suite and are
 * unchanged in substance. What changed is that they now drive the actual
 * component with an actual click, so they also cover the parts a string test
 * could not: that the button validates before spending an evaluation, that a
 * failure leaves a door open, and that the draft is kept on failure and cleared
 * on success.
 *
 * fetch is stubbed. This must never call the real evaluator: it costs money, it
 * spends the visitor rate limit, and it writes a row into demo_attempts, which
 * exists to record what STRANGERS write.
 */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor, cleanup } from '@testing-library/svelte';
import fs from 'node:fs';
import path from 'node:path';
import DemoAsk from '../src/components/DemoAsk.svelte';
import { REPO } from './harness.js';

const lesson = JSON.parse(
  fs.readFileSync(path.join(REPO, 'studio/web/src/data/demo.json'), 'utf8'),
);

const EVALUATION = {
  verdict: 'casi',
  feedback: 'Vas bien, pero te falta el plazo.',
  misconception: 'SMART no es solo "ser específico".',
  missing: ['un número', 'una fecha'],
};

const GOOD_ANSWER =
  'Un objetivo SMART es específico, medible, alcanzable, relevante y con plazo, ' +
  'y sirve para no gastar de más porque sabes qué estás midiendo.';

function stubFetch(response) {
  return vi.fn(async () => response);
}
const ok = (body) => ({ ok: true, status: 200, json: async () => body });
const fail = (status, body = {}) => ({ ok: false, status, json: async () => body });

/* The textarea, by role. NOT by label text: it carries aria-labelledby
   pointing at the question, so its accessible name IS the question — which is
   correct (a screen reader should hear what is being asked) and makes
   getByLabelText('Tu explicación') wrong. */
const box = () => screen.getByRole('textbox');

/* The verdict word, scoped to the verdict. A bare getByText('Casi') also
   matches the intro's "se responde con Lo tienes, Casi o Todavía no" — which is
   the page explaining the scale, not the page answering. */
const verdictWord = () => screen.getByText('Casi', { selector: '.verdict' });

async function answer(text = GOOD_ANSWER) {
  await fireEvent.input(box(), { target: { value: text } });
  await fireEvent.click(screen.getByRole('button', { name: /Que la tutora lo lea/ }));
}

beforeEach(() => {
  localStorage.clear();
  // jsdom implements neither, and neither failing is a reason for a test to fail.
  Element.prototype.scrollIntoView = vi.fn();
  window.matchMedia ??= () => ({ matches: false });
});
afterEach(() => {
  // Auto-cleanup only registers itself when vitest runs with globals:true, and
  // it does not here — without this every render stacks another copy of the
  // component into the same document and every query finds two of everything.
  cleanup();
  vi.unstubAllGlobals();
});

describe('the demo question', () => {
  it('asks the lesson its real question', () => {
    render(DemoAsk, { lesson });
    expect(screen.getByRole('heading', { level: 2 }).textContent)
      .toContain(lesson.explain_prompt);
  });

  it('refuses to spend an evaluation on two words', async () => {
    const f = stubFetch(ok({ evaluation: EVALUATION }));
    vi.stubGlobal('fetch', f);
    render(DemoAsk, { lesson });
    await answer('muy corto');
    await waitFor(() =>
      expect(screen.getByText(/unas dos o tres frases bastan/)).toBeTruthy());
    expect(f).not.toHaveBeenCalled();
  });

  it('keeps a draft while they type, and clears it once it is answered', async () => {
    vi.stubGlobal('fetch', stubFetch(ok({ evaluation: EVALUATION })));
    render(DemoAsk, { lesson });
    await fireEvent.input(box(), { target: { value: GOOD_ANSWER } });
    // Evaluations take 25-35 seconds on a phone in stolen time; losing the text
    // to a backgrounded tab is the cheapest possible way to lose the person.
    expect(localStorage.getItem('aprende_draft_demo_0')).toBe(GOOD_ANSWER);

    await fireEvent.click(screen.getByRole('button', { name: /Que la tutora lo lea/ }));
    await waitFor(() => expect(verdictWord()).toBeTruthy());
    expect(localStorage.getItem('aprende_draft_demo_0')).toBeNull();
  });
});

describe('the verdict', () => {
  beforeEach(() => vi.stubGlobal('fetch', stubFetch(ok({ evaluation: EVALUATION }))));

  it('is a word, not a number', async () => {
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(verdictWord()).toBeTruthy());
    const card = document.querySelector('.card-spot');
    expect(card.textContent).not.toMatch(/\b\d{1,3}\s*\/\s*100\b/);
  });

  it('renders the tutor feedback', async () => {
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(screen.getByText(/te falta el plazo/)).toBeTruthy());
  });

  it('surfaces a misconception', async () => {
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(screen.getByText(/SMART no es solo/)).toBeTruthy());
  });

  it('names what is missing', async () => {
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(screen.getByText('un número')).toBeTruthy());
    expect(screen.getByText('una fecha')).toBeTruthy();
  });

  it('announces the result to a screen reader', async () => {
    const { container } = render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(verdictWord()).toBeTruthy());
    expect(container.querySelector('[aria-live="polite"]')).toBeTruthy();
  });
});

describe('what follows the verdict is real content, not claims', () => {
  beforeEach(() => vi.stubGlobal('fetch', stubFetch(ok({ evaluation: EVALUATION }))));

  it('numbers the rows it actually shows', async () => {
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(screen.getByText(/dos de los cinco pasos/)).toBeTruthy());
  });

  it("shows this lesson's real exercise", async () => {
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(verdictWord()).toBeTruthy());
    expect(document.body.textContent).toContain(lesson.exercise.instruction.slice(0, 60));
  });

  it("shows this module's real reto", async () => {
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(verdictWord()).toBeTruthy());
    expect(document.body.textContent).toContain(lesson.reto.scenario.slice(0, 60));
  });

  it('names the real document type', async () => {
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(screen.getByText(lesson.doc_type)).toBeTruthy());
  });

  it('promises no certificate', async () => {
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(screen.getByText(/No damos certificados/)).toBeTruthy());
  });
});

describe('when the evaluator will not answer', () => {
  it('explains the rate cap in the visitor’s terms, not the limiter’s', async () => {
    // "demasiadas peticiones" describes our infrastructure, not their situation.
    vi.stubGlobal('fetch', stubFetch(fail(429)));
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(screen.getByText(/es una alfa/)).toBeTruthy());
  });

  it('leaves a door open instead of a dead end', async () => {
    // This branch used to set a message and stop, so someone who did exactly
    // what the page asked got a lowercase server fragment and nowhere to go.
    vi.stubGlobal('fetch', stubFetch(fail(503, { detail: 'no disponible' })));
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() =>
      expect(screen.getByRole('link', { name: /Dinos qué quieres ser/ })).toBeTruthy());
  });

  it('keeps what they wrote when it fails', async () => {
    vi.stubGlobal('fetch', stubFetch(fail(500)));
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(screen.getByText(/No pudimos evaluarla/)).toBeTruthy());
    expect(localStorage.getItem('aprende_draft_demo_0')).toBe(GOOD_ANSWER);
  });

  it('survives the connection dropping', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => { throw new TypeError('network'); }));
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(screen.getByText(/No pudimos evaluarla/)).toBeTruthy());
  });
});

describe('honesty — PRODUCT.md records that none of these exist', () => {
  beforeEach(() => vi.stubGlobal('fetch', stubFetch(ok({ evaluation: EVALUATION }))));

  it('invents no testimonial, customer count or price', async () => {
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(verdictWord()).toBeTruthy());
    const text = document.body.textContent;
    expect(text).not.toMatch(
      /(testimonio|alumnas? satisfech|\d+\s*(alumnos|estudiantes|usuarios)\b)/i);
    expect(text).not.toMatch(/(\$\s?\d+\s*\/\s*mes|precio|suscripción)/i);
  });

  it('leaks no undefined and no [object Object]', async () => {
    render(DemoAsk, { lesson });
    await answer();
    await waitFor(() => expect(verdictWord()).toBeTruthy());
    expect(document.body.textContent).not.toMatch(/\bundefined\b/);
    expect(document.body.textContent).not.toContain('[object Object]');
  });
});
