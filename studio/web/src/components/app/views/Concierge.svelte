<script>
  /* "Pide tu curso" — and the requests a learner already made.
   *
   * This is a demand signal as much as a feature: the demand ledger
   * (GET /api/demand) exists so the NEXT course is not built on intuition.
   * (It said "course #15" until #15 shipped on judgment instead — docs/06
   * records that, and the ledger is still the instrument to check first.)
   */
  import { api, toLogin } from '../../../lib/api.js';
  import { nav } from '../../../lib/router.svelte.js';

  let { onsubmitted } = $props();

  let requests = $state(null);
  let topic = $state('');
  let detail = $state('');
  let msg = $state('');
  let busy = $state(false);

  $effect(() => {
    (async () => {
      const d = await api('/requests');
      if (d.__unauth) return toLogin();
      requests = d.requests || [];
    })();
  });

  async function send(event) {
    event.preventDefault();
    if (topic.trim().length < 5) {
      msg = 'Cuéntanos el tema con un poco más de detalle.';
      return;
    }
    busy = true;
    msg = 'Enviando…';
    const res = await fetch('/api/learn/request', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic: topic.trim(), detail: detail.trim() }),
    });
    const r = await res.json().catch(() => ({}));
    busy = false;
    if (!res.ok) {
      msg = r.detail || 'No pudimos enviar tu solicitud.';
      return;
    }
    topic = '';
    detail = '';
    msg = '';
    onsubmitted?.();
  }
</script>

<div style="margin-top:14px">
  <div class="eyebrow">¿No está lo que buscas?</div>
  <h2 style="margin-top:8px">Pide tu curso</h2>
  <p class="muted t-sm" style="margin-top:6px">
    Cuéntanos qué quieres aprender y lo construimos para ti: video, guía y quiz
    por lección. Te avisamos aquí cuando esté listo.
  </p>
</div>

<form class="card" style="display:flex;flex-direction:column;gap:12px" onsubmit={send}>
  <div>
    <label for="reqtopic">¿Qué quieres aprender?</label>
    <input id="reqtopic" maxlength="200" bind:value={topic}
           placeholder="Ej: Ventas por WhatsApp con IA" />
  </div>
  <div>
    <label for="reqdetail">¿Para qué lo necesitas? (opcional)</label>
    <textarea id="reqdetail" maxlength="1000" bind:value={detail}
              placeholder="Tu meta, tu nivel, tu contexto — nos ayuda a armar mejor el curso"
    ></textarea>
  </div>
  <button class="btn btn-primary" type="submit" disabled={busy}>Enviar solicitud</button>
  <div class="center muted t-sm" role="status" aria-live="polite">{msg}</div>
</form>

{#if requests?.length}
  <div class="microlabel" style="margin-top:10px">Tus solicitudes</div>
  {#each requests as r}
    {@const ready = r.status === 'published' && r.course_slug}
    <svelte:element
      this={ready ? 'button' : 'div'}
      class={`req-row ${ready ? 'ready' : ''}`}
      onclick={ready ? () => nav('#/curso/' + r.course_slug) : undefined}
    >
      <div style="flex:1">
        <div class="rt">{r.topic}</div>
        <div class="rd">{r.created_at}{ready ? ' · toca para empezar' : ''}</div>
      </div>
      <span class={`pill st-${r.status}`}>{r.status_label}</span>
    </svelte:element>
  {/each}
{/if}
