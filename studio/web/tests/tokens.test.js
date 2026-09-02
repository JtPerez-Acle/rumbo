/* The token layer has one source, and this proves it.
 *
 * During the migration the tokens exist twice: canonically in
 * src/styles/tokens.css, and inline in learn.html which is still the shipped
 * frontend until phase 3. Two copies of anything drift — that is not a risk,
 * it is a certainty given enough commits — so the drift fails here instead of
 * reaching a screen.
 *
 * DELETE THIS FILE when learn.html is deleted. It guards a duplication that is
 * supposed to stop existing, and a guard that outlives its subject becomes
 * noise the next person has to reason about.
 */
import { describe, it, expect } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { REPO, LEARN_HTML } from './harness.js';

const TOKENS_CSS = path.join(REPO, 'studio/web/src/styles/tokens.css');

/** Every `--name: value` pair in a stylesheet, comments and layout ignored. */
function tokensIn(css) {
  const stripped = css.replace(/\/\*[\s\S]*?\*\//g, '');
  const out = new Map();
  for (const [, name, value] of stripped.matchAll(/(--[a-z0-9-]+)\s*:\s*([^;}]+)/gi)) {
    out.set(name, value.trim().replace(/\s+/g, ' '));
  }
  return out;
}

describe('design tokens', () => {
  const canonical = tokensIn(fs.readFileSync(TOKENS_CSS, 'utf8'));
  const inlineCss = fs.readFileSync(LEARN_HTML, 'utf8').match(/<style>([\s\S]*?)<\/style>/)[1];
  // Only the :root declarations — component rules legitimately consume tokens
  // without redefining them.
  const roots = [...inlineCss.matchAll(/:root\{[\s\S]*?\n\s*\}/g)].map(m => m[0]).join('\n');
  const inline = tokensIn(roots);

  it('extracted a real token set, not an empty match', () => {
    // Guards the parser: every comparison below passes trivially on two empty maps.
    expect(canonical.size).toBeGreaterThan(40);
  });

  it('defines every token learn.html defines', () => {
    const missing = [...inline.keys()].filter(k => !canonical.has(k));
    expect(missing).toEqual([]);
  });

  it('agrees on every value', () => {
    const drifted = [...inline.entries()]
      .filter(([k, v]) => canonical.get(k) !== v)
      .map(([k, v]) => `${k}: ${v} (css has ${canonical.get(k)})`);
    expect(drifted).toEqual([]);
  });

  it('keeps the load-bearing identity intact', () => {
    // DESIGN.md's binding rules. If one of these changes, the change is a brand
    // decision and belongs in a commit that says so.
    expect(canonical.get('--amber')).toBe('#F0A43C');   // the one lamp
    expect(canonical.get('--paper')).toBe('#F1E6CE');   // the learner's own work
    expect(canonical.get('--ink')).toBe('#100D17');     // the workshop ground
    expect(canonical.get('--serif')).toMatch(/Fraunces/);   // the work
    expect(canonical.get('--sans')).toMatch(/Archivo/);     // the interface
  });
});
