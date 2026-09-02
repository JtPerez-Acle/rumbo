/* The landing's "Cómo funciona / Qué te llevas" block.
 *
 * These are promises made to a stranger, not layout. The block went stale once
 * already — it described a course-shaped product for weeks after the goal engine
 * shipped, and still used "pregunta de defensa" wording retired months earlier.
 * Nothing was broken, so nothing complained. That is why the copy is asserted
 * here rather than trusted to review, and why two of these are regression guards
 * against wording that must never come back.
 *
 * Ported from studio/dashboard/check_how_section.js — assertions unchanged.
 */
import { describe, it, expect, beforeAll } from 'vitest';
import { loadSpa } from './harness.js';

describe('landing: cómo funciona', () => {
  let out;

  beforeAll(() => {
    out = loadSpa().run('renderHow(app)');
  });

  it('renders something at all', () => {
    // Guards the harness itself: every assertion below passes trivially against
    // an empty string, so a broken shim would report a clean suite.
    expect(out.length).toBeGreaterThan(500);
  });

  it('shows four numbered steps', () => {
    for (const n of ['1', '2', '3', '4']) expect(out).toContain(`>${n}</span>`);
  });

  it('leads with the goal, not the lesson', () => {
    expect(out.indexOf('Dinos qué quieres ser')).toBeLessThan(out.indexOf('Una lección al día'));
  });

  it('keeps the transversal project step', () => {
    // 0 of 4 learners ever declared one, and it feeds 40 of the 100 points.
    expect(out).toContain('Elige tu proyecto real');
  });

  it('states unlimited retries', () => expect(out).toContain('Reintentas sin límite'));
  it('states that using AI is allowed', () => expect(out).toContain('Usar IA está permitido'));

  it('has the "Qué te llevas" section', () => expect(out).toContain('Qué te llevas'));
  it('promises the deliverable', () => expect(out).toContain('El documento que vas a mostrar'));
  it('promises route visibility', () => expect(out).toContain('Tu ruta, siempre a la vista'));
  it('promises honest gaps', () => expect(out).toContain('Lo que te falta, dicho por su nombre'));
  it('refuses certificates out loud', () => expect(out).toContain('No damos certificados'));

  describe('regression guards', () => {
    it('never revives "pregunta de defensa"', () => expect(out).not.toMatch(/pregunta de defensa/));
    it('never revives a "30 días" duration claim', () => expect(out).not.toMatch(/30 d[ií]as/));
    it('leaks no undefined', () => expect(out).not.toMatch(/\bundefined\b/));
    it('leaks no [object Object]', () => expect(out).not.toContain('[object Object]'));
  });
});
