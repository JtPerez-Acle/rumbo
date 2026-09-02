<script>
  /* One thing the CV claims, and the three things a learner can do about it.
   *
   * The states are the whole policy in miniature: PENDIENTE (we proposed it),
   * DECLARADO (they took the skip — reversible, and worth nothing yet), and
   * ACREDITADO (they passed the module's reto, which is the only thing that
   * counts). `_accessible_for` is the one place access is computed and every
   * widener there only ever ADDS: skipped is not locked.
   */
  import Icon from '../Icon.svelte';
  import { api } from '../../../lib/api.js';
  import { nav } from '../../../lib/router.svelte.js';

  let { claim, passScore } = $props();

  let state_ = $state(claim.state);
  let msg = $state('');
  let busy = $state(false);

  const done = $derived(state_ === 'acreditado');
  const skipped = $derived(state_ === 'declarado');

  async function act(action) {
    busy = true;
    msg = '';
    const r = await api('/exemption', {
      method: 'POST',
      body: JSON.stringify({
        course_slug: claim.course_slug,
        module_no: claim.module_no,
        action,
        claim: claim.capability || '',
      }),
    });
    busy = false;
    if (r && r.ok) state_ = action === 'skip' ? 'declarado' : 'pendiente';
    else msg = (r && r.detail) || 'No pudimos guardarlo.';
  }

  async function toReto() {
    msg = 'Buscando su reto…';
    const course = await api('/course/' + claim.course_slug);
    const m = ((course && course.modules) || []).find((x) => x.module_no === claim.module_no);
    if (m?.capstone?.id) nav('#/reto/' + m.capstone.id);
    else msg = 'Ese módulo todavía no tiene reto. Puedes verlo desde el temario.';
  }
</script>

<div class="card" style={done ? 'border-color:var(--amber)' : undefined}>
  <div class="row" style="justify-content:space-between;align-items:flex-start;gap:10px">
    <span class="microlabel">{claim.course_title} · módulo {claim.module_no}</span>
    {#if done}
      <span class="pill go">Acreditado {claim.exempt_score || ''}</span>
    {:else if skipped}
      <span class="pill soon">Te lo saltas</span>
    {/if}
  </div>

  <p class="t-base" style="font-weight:600;margin:8px 0 4px">
    {claim.outcome || claim.module_title || ''}
  </p>
  <p class="faint t-sm" style="margin:0 0 8px">
    Lo decimos por esto que escribiste: “{claim.evidence || ''}”
  </p>

  <div style="display:flex;flex-direction:column;gap:8px">
    {#if done}
      <p class="faint t-sm" style="margin:0">
        Pasaste su reto. El módulo sigue abierto si alguna vez quieres verlo.
      </p>
      <button class="btn btn-ghost" onclick={() => nav('#/curso/' + claim.course_slug)}>
        Ver el módulo
      </button>
    {:else if skipped}
      <button class="btn btn-primary" disabled={busy} onclick={toReto}>
        <Icon name="target" class="ic ic-s" /> Pruébalo con el reto
      </button>
      <button class="btn btn-ghost" disabled={busy} onclick={() => act('teach')}>
        Mejor enséñamelo
      </button>
      <p class="faint t-sm" style="margin:2px 0 0">
        El reto es un caso nuevo que las lecciones no cubren. Si lo sacas
        {passScore}+ queda acreditado con tu trabajo, y ese trabajo cuenta para
        tu documento.
      </p>
    {:else}
      <button class="btn btn-primary" disabled={busy} onclick={() => act('skip')}>
        Ya lo sé, sáltalo
      </button>
      <button class="btn btn-ghost" disabled={busy}
              onclick={() => (msg = 'Listo: se queda en tu ruta.')}>
        Prefiero verlo igual
      </button>
    {/if}
  </div>

  <div class="center muted t-sm" style="margin-top:6px" role="status" aria-live="polite">{msg}</div>
</div>
