/* Markdown → HTML, at build time.
 *
 * `html: false` is the security control and it is stronger than the one it
 * replaces. The SPA rendered this content in the browser through marked →
 * DOMPurify, which parses raw HTML and then removes what is dangerous. Here the
 * raw HTML is never parsed at all: markdown-it escapes it, so a tag in the
 * source becomes visible text. Nothing to sanitise means nothing to get wrong,
 * and no sanitiser shipped to a phone on metered data.
 *
 * This runs over generated course content, which is model output. Model output
 * is exactly the kind of string that has surprised this codebase before
 * (docs/07), so it is treated as untrusted regardless of where it came from.
 */
import MarkdownIt from 'markdown-it';

const md = new MarkdownIt({
  html: false,     // raw HTML is escaped, never parsed
  linkify: false,  // a bare URL stays text; we do not invent links in lesson copy
  typographer: false,
  breaks: false,
});

/** Rendered HTML for a lesson guide. */
export function renderMarkdown(source) {
  return md.render(source || '');
}

/* The SPA loads mermaid on demand for ```mermaid fences in written guides. The
 * static pages do not, so a fence would silently degrade to a code block. Any
 * page rendering a guide calls this first and fails the BUILD instead — the
 * diagram going missing on a live marketing page is the outcome worth
 * preventing, and a build error is the cheapest place to find out.
 */
export function assertNoMermaid(source, where) {
  if (/```\s*mermaid/.test(source || '')) {
    throw new Error(
      `${where}: the guide contains a mermaid diagram, and the static pages ` +
      `do not render mermaid. Either add a build-time mermaid step or pick a ` +
      `demo lesson without one — do not ship the fence as a code block.`,
    );
  }
}
