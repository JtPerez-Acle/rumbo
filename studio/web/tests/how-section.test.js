// @vitest-environment jsdom
/* "Cómo funciona": the promises this product makes, in the one place it makes
 * them twice.
 *
 * STEPS and GETS have a single definition and two renderers — the public
 * landing and first-login orientation — and this suite exists because the copy
 * HAS gone stale before: a single list went on describing a course-shaped
 * product for months after the goal engine shipped, on the screen new learners
 * read first.
 *
 * Assertions unchanged from the DOM-shim version; the subject moved from a
 * render function inside learn.html to the component that replaced it.
 */
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { render, cleanup } from '@testing-library/svelte';
import HowItWorks from '../src/components/app/views/HowItWorks.svelte';

describe('cómo funciona', () => {
  let out;

  beforeAll(() => {
    const { container } = render(HowItWorks);
    out = container.textContent.replace(/\s+/g, ' ').trim();
  });
  afterAll(cleanup);

  it('renders something at all', () => {
    // Guards the harness: every assertion below passes trivially on ''.
    expect(out.length).toBeGreaterThan(500);
  });

  it('shows four numbered steps', () => {
    expect(document.querySelectorAll('.stepnum')).toHaveLength(4);
  });

  it('leads with the goal, not the lesson', () => {
    // The route is the product and the courses are inventory. A first step that
    // said "elige un curso" would contradict the whole surface.
    expect(out).toContain('Dinos qué quieres ser');
  });

  it('keeps the transversal project step', () => {
    expect(out).toContain('Elige tu proyecto real');
  });

  it('states unlimited retries', () => expect(out).toContain('Reintentas sin límite'));
  it('states that using AI is allowed', () => expect(out).toContain('Usar IA está permitido'));

  it('has the "Qué te llevas" section', () => expect(out).toContain('Qué te llevas'));
  it('promises the deliverable', () => expect(out).toContain('El documento que vas a mostrar'));
  it('promises route visibility', () => expect(out).toContain('Tu ruta, siempre a la vista'));
  it('promises honest gaps', () => expect(out).toContain('Lo que te falta, dicho por su nombre'));
  it('refuses certificates out loud', () => expect(out).toContain('No damos certificados'));

  describe('regressions this copy has actually had', () => {
    it('never revives "pregunta de defensa"', () => expect(out).not.toMatch(/pregunta de defensa/));
    it('never revives a "30 días" duration claim', () => expect(out).not.toMatch(/30 d[ií]as/));
    it('leaks no undefined', () => expect(out).not.toMatch(/\bundefined\b/));
    it('leaks no [object Object]', () => expect(out).not.toContain('[object Object]'));
  });
});
