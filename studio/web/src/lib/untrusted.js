/* Rendering content this product did not write.
 *
 * Two sources reach these functions and both are untrusted: learner
 * submissions, and model output. `content_md` on a portfolio page is compiled
 * from what learners typed, and marked emits raw HTML by design — assigning
 * marked.parse() straight to innerHTML was a live stored-XSS sink on the public
 * share pages (2026-08-12 audit).
 *
 * WHAT CHANGED WITH THE BUILD STEP: marked and DOMPurify are bundled from
 * node_modules instead of fetched from a CDN with an SRI hash. The version is
 * in package-lock.json, it cannot be swapped under us by a compromised CDN, it
 * costs no third-party connection on a phone, and — the part that matters most —
 * `script-src` no longer needs a CDN origin at all.
 *
 * The public pages do NOT use this. They render their Markdown at build time
 * with markdown-it and `html:false`, which never parses raw HTML in the first
 * place (lib/markdown.js). That is strictly stronger and ships no sanitiser.
 * This exists for the app, where the content arrives at runtime.
 */
import { marked } from 'marked';
import DOMPurify from 'dompurify';

/** Sanitised HTML for untrusted Markdown. The ONLY way this content may render. */
export function renderMarkdownUntrusted(md) {
  return DOMPurify.sanitize(marked.parse(md || ''));
}

/* Mermaid is LAZY and it is a local chunk, and both words are load-bearing.
 *
 * It used to be an eager import in <head> from a floating `mermaid@11` tag:
 * ~215 KB over 19 chunk requests, on every page load, resolving to whatever the
 * CDN served that day. The public landing paid that on every visit for a lesson
 * containing no diagram at all — on a product that re-encodes every lesson video to
 * ~5 MB each so a learner on LatAm mobile data does not pay the difference.
 *
 * Now nothing loads until a lesson actually renders a diagram, and when it does
 * the bytes come from our own origin with the deploy's cache headers.
 *
 * securityLevel stays 'loose': 38 of our 402 diagrams use <br> in labels and
 * 'strict' renders those as literal text. Diagrams come from writer.py, never
 * from a learner. 'antiscript' would keep the <br> and drop the script surface
 * at the cost of 3 diagrams that use click handlers — a separate decision, not
 * a free win.
 */
let mermaidLoading = null;

const loadMermaid = () =>
  (mermaidLoading ??= import('mermaid').then((m) => {
    m.default.initialize({ startOnLoad: false, theme: 'default', securityLevel: 'loose' });
    return m.default;
  }));

/** Render one mermaid node in place. Never throws: says so in the element instead. */
export async function renderMermaid(el) {
  if (!el) return;
  try {
    const mermaid = await loadMermaid();
    await mermaid.run({ nodes: [el] });
  } catch {
    el.textContent = '(diagrama no disponible)';
  }
}
