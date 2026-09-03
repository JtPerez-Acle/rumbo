/* Does the page fit on the screen, and is the content where the grid put it?
 *
 * THE BUG THIS SUITE EXISTS FOR. /oferta, /lista and /login shipped rendering
 * as a 32-pixel strip against the right edge of the browser. Astro gives an
 * island `display: contents`, so an island placed directly in `body.wide .app`
 * is not a grid item — its children are, they inherit no column, and they land
 * in the implicit track past `full-end`.
 *
 * Every test we had passed. The words were all on the page; a reader could not
 * get at a single one of them. jsdom has no layout engine, so no amount of
 * content assertion could have caught it. This runs real Chromium and measures.
 *
 * WHAT IT DOES NOT DO. It does not read copy — vitest does that in two seconds
 * and does it better. It does not diff screenshots: those go stale on a font
 * update and a suite people learn to ignore is worse than no suite.
 *
 * It catches BROKEN, not UGLY. Spacing rhythm, hierarchy and whether a page is
 * any good still need a person looking at it.
 */
import { test, expect } from '@playwright/test';

/* The static server behind these tests serves dist/ and nothing else, but the
   landing's poster comes from /api/learn/public/demo-poster in production. Left
   unstubbed it 404s, the img is removed by its own onerror, and the page under
   test is not the page anyone is served. Stubbing it is how the harness stops
   lying — and the plate is sized so it survives either way, which is a separate
   fix this test found. */
const POSTER = Buffer.from(
  'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
  'base64',
);

test.beforeEach(async ({ page }) => {
  await page.route('**/api/learn/public/demo-poster', (route) =>
    route.fulfill({ status: 200, contentType: 'image/png', body: POSTER }));
});

/* 320 is the narrowest phone still in real use and the one that hurts; 375 is
   the stated primary device; 768 is the breakpoint where the wide grid engages;
   1280 is where the text column should stop growing instead of sprawling. */
const WIDTHS = [
  { name: '320 · narrow phone', width: 320, height: 720 },
  { name: '375 · primary device', width: 375, height: 812 },
  { name: '768 · grid engages', width: 768, height: 1024 },
  { name: '1280 · laptop', width: 1280, height: 900 },
];

const PAGES = ['/', '/cursos', '/curso/curso-meta-ads', '/oferta', '/lista', '/login'];

/** The measurements, taken in the page. */
async function measure(page) {
  return page.evaluate(() => {
    const vw = window.innerWidth;

    const visible = (el) => {
      const s = getComputedStyle(el);
      return (
        s.visibility !== 'hidden' &&
        s.display !== 'none' &&
        parseFloat(s.opacity) >= 0.15 &&
        // Honeypots are parked off-screen on purpose and are aria-hidden.
        el.getAttribute('aria-hidden') !== 'true'
      );
    };
    const box = (el) => {
      const r = el.getBoundingClientRect();
      return { w: Math.round(r.width), h: Math.round(r.height), l: Math.round(r.left), r: Math.round(r.right) };
    };
    const label = (el) =>
      `${el.tagName.toLowerCase()}.${(el.className || '').toString().trim().split(/\s+/)[0] || ''}`;

    const escapes = [...document.querySelectorAll('body *')]
      .filter((el) => {
        const s = getComputedStyle(el);
        if (s.position === 'fixed' || !visible(el)) return false;
        const b = box(el);
        if (!b.w || !b.h) return false;
        // A container that scrolls its own overflow is doing its job — a wide
        // table inside a scrollable guide is reachable, not lost.
        for (let p = el.parentElement; p; p = p.parentElement) {
          const ps = getComputedStyle(p);
          if (ps.overflowX === 'auto' || ps.overflowX === 'scroll') return false;
        }
        return b.r > vw + 1 || b.l < -1;
      })
      .map((el) => ({ el: label(el), ...box(el) }));

    /* The /oferta shape, measured where it actually shows: the page's own
       heading and its longest paragraph. A generic "is any block narrow?" scan
       was the first attempt and it flagged the brand lockup and every text
       link — a guard with false positives gets muted, and a muted guard is the
       thing that let this bug ship. The heading was 32px wide when it broke and
       640px when it works; nothing about that is ambiguous. */
    const heading = document.querySelector('main.app h1');
    const longestPara = [...document.querySelectorAll('main.app p')]
      .filter((el) => visible(el) && (el.textContent || '').trim().length > 80)
      .sort((a, c) => c.getBoundingClientRect().width - a.getBoundingClientRect().width)[0];

    const smallTargets = [...document.querySelectorAll('a, button, input, textarea, summary, select')]
      .filter((el) => {
        if (!visible(el)) return false;
        const b = box(el);
        return b.w > 0 && b.h > 0 && (b.h < 32 || b.w < 32);
      })
      .map((el) => ({ text: (el.textContent || el.tagName).trim().slice(0, 24), ...box(el) }));

    const para = [...document.querySelectorAll('main.app p')].find(
      (p) => (p.textContent || '').trim().length > 80,
    );

    return {
      vw,
      pageScrollWidth: document.documentElement.scrollWidth,
      escapes,
      smallTargets,
      headingWidth: heading ? Math.round(heading.getBoundingClientRect().width) : null,
      contentWidth: longestPara ? Math.round(longestPara.getBoundingClientRect().width) : null,
      paragraphWidth: para ? Math.round(para.getBoundingClientRect().width) : null,
      bodyClasses: document.body.className,
    };
  });
}

for (const { name, width, height } of WIDTHS) {
  test.describe(name, () => {
    test.use({ viewport: { width, height } });

    for (const url of PAGES) {
      test(`${url} fits and is placed`, async ({ page }) => {
        await page.goto(url, { waitUntil: 'load' });
        // Islands hydrate after load; a layout that only breaks post-hydration
        // is still a broken layout.
        await page.waitForTimeout(400);
        const m = await measure(page);

        expect(m.pageScrollWidth,
          `the page scrolls sideways at ${m.vw}px`).toBeLessThanOrEqual(m.vw + 1);

        expect(m.escapes,
          'these boxes hang outside the viewport with nothing to scroll them').toEqual([]);

        /* The width a real column should have here. Generous on purpose: this
           is looking for collapse, not for a few pixels of drift. */
        const floor = Math.min(Math.round(m.vw * 0.5), 260);
        expect(m.headingWidth,
          'the heading collapsed — usually an island placed straight into the grid')
          .toBeGreaterThanOrEqual(floor);
        expect(m.contentWidth,
          'the body copy collapsed — usually an island placed straight into the grid')
          .toBeGreaterThanOrEqual(floor);

        expect(m.smallTargets,
          'below 32px these are hard to hit with a thumb, and this audience is on phones').toEqual([]);
      });
    }
  });
}

test.describe('the text column', () => {
  /* The measure is a product decision, not an accident: past ~1280px the page
     stops growing and the gutters absorb the rest, because a 1900px line is not
     a better page, it is a harder one to read. */
  test('stops growing once it reaches its token width', async ({ page }) => {
    const widths = [];
    for (const vw of [375, 768, 1280, 1920]) {
      await page.setViewportSize({ width: vw, height: 900 });
      await page.goto('/cursos', { waitUntil: 'load' });
      const m = await measure(page);
      widths.push({ vw, paragraph: m.paragraphWidth });
    }
    const token = await page.evaluate(() =>
      parseInt(getComputedStyle(document.documentElement).getPropertyValue('--w-text'), 10),
    );
    for (const { vw, paragraph } of widths) {
      expect(paragraph, `a paragraph at ${vw}px is wider than --w-text`).toBeLessThanOrEqual(token + 1);
    }
    // And it does grow up to the cap — a column stuck at phone width on a
    // laptop would pass the assertion above while looking broken.
    expect(widths.at(-1).paragraph, 'the column never reaches its measure').toBe(token);
  });
});
