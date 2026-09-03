/* Layout tests, in a real browser.
 *
 * WHY THIS EXISTS. vitest reads the built HTML and mounts components under
 * jsdom, and jsdom has no layout engine — it can tell you a word is on the page
 * and never that the page is 32 pixels wide. That is exactly how /oferta,
 * /lista and /login shipped broken: every content assertion passed while the
 * whole form rendered as a strip against the right edge.
 *
 * So this suite asserts GEOMETRY and nothing else. It does not check copy —
 * vitest already does, faster — and it does not diff screenshots, which are
 * famously noisy across machines and would train everyone to ignore a red run.
 *
 * Chromium only. The audience is phone-first LatAm on low-end Android, so
 * Chromium IS the target; adding Firefox and WebKit would triple the runtime to
 * cover browsers this product's users do not have.
 */
import { defineConfig, devices } from '@playwright/test';

const PORT = 4321;

export default defineConfig({
  testDir: './tests-layout',
  fullyParallel: true,
  reporter: process.env.CI ? 'list' : [['list']],
  // A layout assertion either holds immediately or the page is broken. Waiting
  // five seconds for a box to become the right width just makes a red run slow.
  expect: { timeout: 2000 },
  use: {
    baseURL: `http://localhost:${PORT}`,
    // Every failure gets a screenshot: "the h1 is 32px wide" is a fact, and a
    // picture is what makes it obvious WHY in one glance.
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],

  /* Serves dist/ the way FastAPI does — directory-style URLs, so /cursos
     resolves to cursos/index.html. Testing the built output rather than a dev
     server is the point: the dev server is not what anybody is served, and
     `astro preview` daemonizes, which Playwright reads as a crashed server. */
  webServer: {
    command: `node tests-layout/serve-dist.js`,
    port: PORT,
    reuseExistingServer: true,
    timeout: 60_000,
  },
});
