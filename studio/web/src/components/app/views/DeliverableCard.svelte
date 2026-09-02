<script>
  /* The document this course compiles into, at the foot of its temario.
   *
   * THE GATE IS DELIBERATE, NOT A TEASE. Fed one or two pieces the compiler does
   * not produce a short document — it fills the vacuum by inventing. It once
   * wrote a skills inventory for a learner whose only submission was the starter
   * prompt. So the screen says what it needs and why, and shows progress toward
   * it, so it reads as a countdown rather than a locked door.
   */
  import Icon from '../Icon.svelte';
  import { api } from '../../../lib/api.js';
  import { nav } from '../../../lib/router.svelte.js';

  let { slug } = $props();

  let doc = $state(null);
  let study = $state(null);
  let busy = $state('');
  let error = $state('');

  $effect(() => {
    (async () => {
      const [d, cs] = await Promise.all([
        api('/project-doc/' + slug),
        api('/case-study/' + slug),
      ]);
      if (d.__unauth || d.detail) return;
      doc = d;
      study = cs && !cs.detail ? cs : null;
    })();
  });

  async function compile(kind, path) {
    busy = kind;
    error = '';
    const res = await fetch(`/api/learn/${kind}/${slug}`, { method: 'POST' });
    const r = await res.json().catch(() => ({}));
    busy = '';
    if (!res.ok) {
      // This was an alert(), which on a phone is a modal the learner has to
      // dismiss before they can even read the screen behind it.
      error = r.detail || 'No se pudo compilar. Intenta de nuevo.';
      return;
    }
    nav(path);
  }
</script>

{#if doc}
  <div class="card-paper" style="margin-top:14px">
    <div class="ai-tag"><span class="dot"></span> Tu portafolio</div>
    <h3 style="margin-top:8px">{doc.doc_type}</h3>
    <p class="muted t-sm" style="margin-top:6px">
      Tus ejercicios y retos, compilados en el documento que un cliente pagaría
      por recibir: tuyo, descargable en PDF, listo para tu portafolio o para
      enviar.
    </p>

    <div style="margin-top:12px;display:flex;flex-direction:column;gap:8px">
      {#if doc.exists}
        <button class="btn btn-paper" onclick={() => nav('#/documento/' + slug)}>
          <Icon name="doc" class="ic ic-s" /> Ver mi documento
        </button>
      {:else if doc.eligible}
        <button class="btn btn-paper" disabled={busy === 'project-doc'}
                onclick={() => compile('project-doc', '#/documento/' + slug)}>
          <Icon name="doc" class="ic ic-s" />
          {busy === 'project-doc' ? 'Compilando tu documento… (unos segundos)' : 'Compilar mi documento'}
        </button>
      {:else}
        {@const have = doc.submissions || 0}
        {@const need = doc.needed || 3}
        <div>
          <div class="row" style="gap:6px;align-items:center;margin-bottom:8px">
            {#each Array(need) as _, i}
              <span class={`pip ${i < have ? 'on' : ''}`}></span>
            {/each}
            <span class="faint" style="font-size:var(--fs-xs);margin-left:6px">
              {have} de {need} trabajos
            </span>
          </div>
          <p class="faint t-sm" style="margin:0">
            Con {need} entregas tuyas ya hay material real para compilar. Con
            menos, el documento tendría que inventar — y este lo vas a mostrar.
            {have === 0
              ? 'Envía el ejercicio de cualquier lección para empezar.'
              : `Te ${need - have === 1 ? 'falta 1' : 'faltan ' + (need - have)}.`}
          </p>
        </div>
      {/if}

      <!-- Companion narrative: the STAR case study about how the work was done. -->
      {#if study && (study.exists || study.eligible)}
        <button class="btn btn-ghost btn-sm" style="width:100%" disabled={busy === 'case-study'}
                onclick={() => study.exists
                  ? nav('#/caso-view/' + slug)
                  : compile('case-study', '#/caso-view/' + slug)}>
          {busy === 'case-study'
            ? 'Redactando tu caso…'
            : study.exists ? 'Ver mi caso de estudio (STAR) ›' : 'Generar caso de estudio (STAR)'}
        </button>
      {/if}

      {#if error}
        <p class="t-sm" style="color:var(--terra);margin:0" role="alert">{error}</p>
      {/if}
    </div>
  </div>
{/if}
