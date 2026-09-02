/* The job analyser: the paste box and the route it renders.
 *
 * docs/08 calls this the acquisition asset — it carries the only claim a
 * competitor cannot truthfully make, that we name what the posting demands and
 * we do NOT teach. So the honesty line and the gap list are asserted, not
 * assumed, and so is the wait: the analysis really takes about two minutes and
 * the page has to say so before anyone commits to it.
 *
 * Ported from studio/dashboard/check_job_render.js — assertions unchanged.
 */
import { describe, it, expect, beforeAll } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { loadSpa, REPO } from './harness.js';

const FIXTURE = path.join(REPO, 'studio/fixtures/job-postings/sample-analysis.json');

describe('job analyser', () => {
  let spa, box, stages, slowAt, analysis, out, noToken;

  beforeAll(() => {
    spa = loadSpa();
    box = spa.run('renderJobBox()');
    stages = spa.evaluate('JOB_STAGES');
    slowAt = spa.evaluate('JOB_SLOW_AT');
    analysis = JSON.parse(fs.readFileSync(FIXTURE, 'utf8')).analysis;
    noToken = spa.run(`renderJobResult(${JSON.stringify(analysis)})`);
    out = spa.run(`renderJobResult(${JSON.stringify(analysis)}, "TESTTOKEN123")`);
  });

  describe('the paste box', () => {
    it('has a textarea', () => expect(box).toMatch(/<textarea[^>]*id="jtext"/));
    it('offers the goal-only mode', () => expect(box).toMatch(/Solo sé el puesto/));
    it('has the goal input', () => expect(box).toMatch(/id="jgoal"/));
    it('has the honeypot', () => expect(box).toMatch(/id="jcompany"/));

    // A two-minute wait that is not declared is a bounce. This is the one
    // interaction the whole category gets wrong.
    it('declares the wait up front', () => expect(box).toMatch(/dos minutos/));
    it('tells them not to close the tab', () => expect(box).toMatch(/No cierres esta pesta/));
  });

  describe('the staged clock', () => {
    it('defines at least four stages', () => {
      expect(Array.isArray(stages)).toBe(true);
      expect(stages.length).toBeGreaterThanOrEqual(4);
    });
    it('starts at 0s', () => expect(stages[0][0]).toBe(0));
    it('ascends', () => stages.forEach((s, i) => {
      if (i) expect(s[0]).toBeGreaterThan(stages[i - 1][0]);
    }));
    it('explains every stage', () => stages.forEach(s => {
      expect(s[2]?.length ?? 0).toBeGreaterThan(20);
    }));
    it('puts the slow threshold past the last stage', () =>
      expect(slowAt).toBeGreaterThan(stages[stages.length - 1][0]));
  });

  describe('the result', () => {
    it('names the role', () => expect(out).toContain(analysis.role_title));
    it('states coverage', () => expect(out).toContain(`Cubrimos ${analysis.coverage}%`));

    it('separates núcleo from later', () => {
      const nucleo = analysis.ruta.filter(r => r.phase === 'nucleo');
      const later = analysis.ruta.filter(r => r.phase !== 'nucleo');
      if (nucleo.length) expect(out).toContain('Empieza por aquí');
      if (later.length) expect(out).toContain('Después, para completar');
    });

    it('shows every course on the route', () =>
      analysis.ruta.forEach(r => expect(out).toContain(r.course_title)));

    // Mirrors modLabel in learn.html / ruta.html: v2 module sets read
    // "Módulos 1 y 3"; v1 rows without a modules list read "Hasta módulo N".
    it('labels every module selection correctly', () => analysis.ruta.forEach(r => {
      const m = r.modules?.length ? r.modules : null;
      if (!m) return expect(out).toContain(`Hasta módulo ${r.through_module}`);
      const sequential = m.length === m[m.length - 1] - m[0] + 1;
      if (sequential && m[0] === 1) {
        return expect(out).toContain(m.length === 1 ? 'Módulo 1' : `Hasta módulo ${m[m.length - 1]}`);
      }
      if (m.length === 1) return expect(out).toContain(`Módulo ${m[0]}`);
      expect(out).toContain(`Módulos ${m.slice(0, -1).join(', ')} y ${m[m.length - 1]}`);
    }));

    it('names what we do not cover', () => {
      if (!analysis.gaps.length) return;
      expect(out).toContain('no lo cubrimos');
      analysis.gaps.forEach(g => expect(out).toContain(g.name));
      expect(out).toContain('Preferimos decírtelo');
    });

    it('names the document', () => {
      if (analysis.doc_type) expect(out).toContain(analysis.doc_type);
    });
  });

  describe('the share affordance', () => {
    it('appears when a token exists', () => expect(out).toMatch(/Comparte esta ruta/));
    // An analysis re-rendered from storage has no token, and must not offer a
    // link that does not exist.
    it('is absent without one', () => expect(noToken).not.toMatch(/Comparte esta ruta/));
  });

  describe('regression guards', () => {
    it('leaks no undefined', () => expect(out).not.toMatch(/\bundefined\b/));
    it('leaks no [object Object]', () => expect(out).not.toContain('[object Object]'));
  });
});
