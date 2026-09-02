// @ts-check
import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';

/* Rumbo's frontend build.
 *
 * STATIC, and that is the whole architectural decision. Astro runs in a Docker
 * build stage and emits plain files; FastAPI serves them. Production stays one
 * Python process — no Node runtime, no second service, no new way for a product
 * run by one person to break at 2am.
 *
 * The cost is named rather than hidden: the fourteen /curso/<slug> pages are
 * generated from the database, so their data has to ship as a file and a new
 * course goes live on deploy rather than on a database write. Courses arrive
 * roughly monthly and already need a deploy for their videos, so the change is
 * close to free — see docs/04 for the export step that feeds it.
 *
 * Svelte, not React: this product re-encoded 420 videos to ~5MB each so a
 * learner in LatAm on metered mobile data would not pay the difference. Shipping
 * a component runtime to those same phones would undo that care. Svelte compiles
 * away, and the public pages are islands-only — most of them ship no JS at all.
 */
export default defineConfig({
  output: 'static',
  outDir: './dist',
  integrations: [svelte()],

  build: {
    // FastAPI serves these; a flat, predictable asset directory keeps the
    // StaticFiles mount and the CSP hash list simple.
    assets: 'assets',
    // One CSS file rather than per-page chunks. The whole stylesheet is smaller
    // than a single lesson video frame, and one cached file beats six requests
    // on a slow connection.
    inlineStylesheets: 'never',
  },

  vite: {
    build: {
      // Loud rather than convenient: a public page that quietly grows a large
      // bundle is exactly the regression this stack was chosen to prevent, so
      // the build warns well below anything a phone would notice.
      chunkSizeWarningLimit: 150,
    },
  },
});
