/* The stylesheet exists twice during the migration, and this makes that safe.
 *
 * learn.html still carries the whole stylesheet inline because it is still the
 * frontend being served. The Astro pages need the same rules as real files.
 * Two copies of 45KB of CSS will fork — not might, will — and the symptom is a
 * public page that looks subtly unlike the app it leads into, which is exactly
 * the class of bug that started this migration.
 *
 * So the two are not allowed to be independent: tokens.css + app.css must
 * reassemble learn.html's <style> block. Editing one side alone fails here
 * rather than on a screen.
 *
 * DELETE THIS FILE when learn.html is deleted — the duplication it guards is
 * supposed to stop existing, and a guard outliving its subject is noise.
 */
import { describe, it, expect } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { REPO, LEARN_HTML } from './harness.js';

const STYLES = path.join(REPO, 'studio/web/src/styles');
const ROOT_BLOCK = /[ \t]*:root\{[\s\S]*?\n[ \t]*\}\n/g;

/* Line endings normalised on both sides. git rewrites them per-platform, so a
   byte comparison would fail on a fresh clone rather than on a real edit — and
   a test that fails for the wrong reason gets muted, after which it guards
   nothing at all. */
const read = (p) => fs.readFileSync(p, 'utf8').replace(/\r\n/g, '\n');

/** A stylesheet without this repo's own leading file comment. */
const body = (css) => css.replace(/^\/\*[\s\S]*?\*\/\n/, '');

describe('stylesheet parity with learn.html', () => {
  const inline = read(LEARN_HTML).match(/<style>([\s\S]*?)<\/style>/)[1];
  const appCss = body(read(path.join(STYLES, 'app.css')));

  it('found a real stylesheet, not an empty match', () => {
    // Without this, every comparison below passes on two empty strings.
    expect(inline.length).toBeGreaterThan(40000);
    expect(appCss.length).toBeGreaterThan(40000);
  });

  it('learn.html still has exactly the two :root blocks tokens.css covers', () => {
    // A third would mean tokens defined somewhere this split cannot see, and
    // app.css would swallow them silently.
    expect(inline.match(ROOT_BLOCK)).toHaveLength(2);
  });

  it('app.css is learn.html without its tokens', () => {
    expect(appCss).toBe(inline.replace(ROOT_BLOCK, ''));
  });
});
