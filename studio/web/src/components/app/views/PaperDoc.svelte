<script>
  /* A document under the learner's byline, on paper.
   *
   * ProjectDoc and CaseStudy were two 23-line functions that differed in three
   * strings and one endpoint. They are one component now, because the thing
   * they have in common is the part that matters: this is the deliverable, the
   * product's whole promise — "the thing a client would have paid for" — and it
   * should not be possible for one of them to gain a fix the other misses.
   *
   * `content_md` is compiled from learner submissions, so it renders through
   * the sanitiser and never through innerHTML directly. That was a live
   * stored-XSS sink on the public share pages.
   */
  import Icon from '../Icon.svelte';
  import { api, toLogin } from '../../../lib/api.js';
  import { renderMarkdownUntrusted } from '../../../lib/untrusted.js';

  let { slug, kind } = $props(); // kind: 'project-doc' | 'case-study'

  const COPY = {
    'project-doc': {
      tag: (d) => d.doc_type,
      recompile: 'Recompilar con mi trabajo más reciente',
      recompiling: 'Compilando de nuevo…',
      openLabel: 'Abrir para descargar en PDF',
    },
    'case-study': {
      tag: () => 'Caso de estudio · metodología STAR',
      recompile: 'Regenerar con mi trabajo más reciente',
      recompiling: 'Redactando de nuevo…',
      openLabel: null, // the STAR narrative has no PDF route of its own
    },
  };

  let doc = $state(null);
  let busy = $state(false);
  let shareLabel = $state('Copiar enlace del documento');
  let mdLabel = $state('Copiar Markdown (para Notion)');
  const copy = COPY[kind];

  async function load() {
    const d = await api(`/${kind}/${slug}`);
    if (d.__unauth) return toLogin();
    doc = d;
  }

  $effect(() => { load(); });

  const body = $derived(doc ? renderMarkdownUntrusted(doc.content_md) : '');

  async function recompile() {
    busy = true;
    const res = await fetch(`/api/learn/${kind}/${slug}`, { method: 'POST' });
    busy = false;
    if (res.ok) load();
  }

  async function toClipboard(text, set, done) {
    try {
      await navigator.clipboard.writeText(text);
      set(done);
    } catch {
      // Clipboard access is refused in plenty of ordinary situations (an
      // insecure origin, a denied permission). Saying nothing looks like a
      // broken button; the link itself is the fallback.
      set('No se pudo copiar — mantén pulsado el enlace');
    }
  }
</script>

{#if doc}
  <button class="back" onclick={() => history.back()}>‹ Volver</button>

  <div style="margin-top:4px">
    <div class="ai-tag"><span class="dot"></span> {copy.tag(doc)}</div>
  </div>

  <div class="card-paper">
    <!-- eslint-disable-next-line svelte/no-at-html-tags -- sanitised above -->
    <div class="written">{@html body}</div>
  </div>

  {#if copy.openLabel}
    <button class="btn btn-paper" onclick={() => window.open(doc.share_url, '_blank')}>
      <Icon name="down" class="ic ic-s" /> {copy.openLabel}
    </button>
  {/if}

  <button
    class={copy.openLabel ? 'btn btn-ghost' : 'btn btn-paper'}
    onclick={() => toClipboard(location.origin + doc.share_url,
                               (v) => (shareLabel = v), '✓ Enlace copiado')}>
    <Icon name="copy" class="ic ic-s" /> {shareLabel}
  </button>

  <button class="btn btn-ghost"
          onclick={() => toClipboard(doc.content_md, (v) => (mdLabel = v), '✓ Copiado')}>
    <Icon name="copy" class="ic ic-s" /> {mdLabel}
  </button>

  <button class="btn btn-ghost" disabled={busy} onclick={recompile}>
    {busy ? copy.recompiling : copy.recompile}
  </button>
{/if}
