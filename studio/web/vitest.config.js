/* Vitest, with Svelte compiled the same way Astro compiles it.
 *
 * Most suites read files — the built HTML, the stylesheets, learn.html through
 * a DOM shim — and need no browser at all. demo-verdict.test.js drives a real
 * component and declares `// @vitest-environment jsdom` at the top of the file,
 * which is why the default stays `node`: paying for a DOM in every suite to
 * serve one of them is how a fast suite stops being run.
 */
import { defineConfig } from 'vitest/config';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte({ hot: false })],
  resolve: {
    // @testing-library/svelte needs the browser build of Svelte's runtime;
    // without this, mounting a component in jsdom resolves the SSR one and
    // renders nothing, silently.
    conditions: ['browser'],
  },
  test: {
    environment: 'node',
    globals: false,
    /* tests/ only. Without this, vitest's default glob also collects
       tests-layout/*.spec.js — the Playwright suite — and dies on the first
       `test.beforeEach`, reporting "1 file failed, 130 tests passed", which is
       a failure people learn to scroll past. The two runners own separate
       directories and neither should try to run the other's work. */
    include: ['tests/**/*.test.js'],
  },
});
