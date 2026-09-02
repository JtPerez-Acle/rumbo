<script>
  /* The written guide: the how, next to the video's why.
   *
   * Diagrams render through mermaid, which is loaded on demand — nothing pays
   * for it until a lesson actually has one.
   */
  import { renderMarkdownUntrusted, renderMermaid } from '../../../lib/untrusted.js';

  let { lesson } = $props();

  /* Ref-collecting rather than a query after render: mermaid rewrites the node
     in place, so it has to be the exact element, not one found by selector on a
     list that may have re-rendered underneath. */
  function diagram(node) {
    renderMermaid(node);
  }
</script>

{#if lesson.written}
  <div class="written">{@html renderMarkdownUntrusted(lesson.written)}</div>
{/if}

{#each lesson.diagrams || [] as d}
  <div>
    <div class="diagram-title">{d.title || ''}</div>
    <div class="diagram">
      <pre class="mermaid" use:diagram>{d.mermaid || ''}</pre>
    </div>
  </div>
{/each}
