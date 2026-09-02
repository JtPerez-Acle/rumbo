<script>
  /* The reto: a novel business case the lessons deliberately did not cover.
   *
   * It is a work product, so it uses the same prediction beat and the same
   * score card as the exercise. Two work products must not disagree about how
   * self-assessment is asked for, or about what a score means.
   */
  import ReadingCard from '../eval/ReadingCard.svelte';
  import EvalResult from '../eval/EvalResult.svelte';
  import ScoreCard from '../eval/ScoreCard.svelte';
  import DefenseCard from '../eval/DefenseCard.svelte';
  import PredictionBeat from '../eval/PredictionBeat.svelte';
  import { api, toLogin, postWithTimeout } from '../../../lib/api.js';
  import { loadDraft, draftSaver, clearDraft } from '../../../lib/drafts.js';
  import { nav } from '../../../lib/router.svelte.js';

  let { id } = $props();

  let capstone = $state(null);
  let unavailable = $state('');
  let content = $state('');
  let msg = $state('');
  let phase = $state('writing'); // writing | predicting | sending | done
  let evaluation = $state(null);
  const save = draftSaver('capstone', id);

  $effect(() => {
    (async () => {
      const d = await api('/capstone/' + id);
      if (d.__unauth) return toLogin();
      if (d.detail) {
        // Was an alert(), which on a phone is a modal blocking the screen it is
        // describing. This says the same thing in the page.
        unavailable = d.detail;
        return;
      }
      capstone = d;
      content = loadDraft('capstone', id) || d.last_content || '';
    })();
  });

  function start() {
    if (content.trim().length < 50) {
      msg = 'Desarrolla tu solución un poco más (mínimo 50 caracteres).';
      return;
    }
    msg = '';
    phase = 'predicting';
  }

  async function submit(predicted) {
    phase = 'sending';
    const { res, data } = await postWithTimeout('/api/learn/submit-capstone', {
      capstone_id: id, content: content.trim(), predicted: predicted ?? null,
    });
    if (!res || !res.ok) {
      phase = 'writing';
      msg = data.detail || 'No pudimos evaluar, intenta de nuevo.';
      return;
    }
    clearDraft('capstone', id);
    evaluation = data.evaluation;
    phase = 'done';
  }

  function again() {
    evaluation = null;
    phase = 'writing';
    msg = 'Mejora tu solución con el feedback y envíala de nuevo.';
  }
</script>

{#if unavailable}
  <button class="back" onclick={() => history.back()}>‹ Volver</button>
  <div class="note note-warn" style="margin-top:10px">{unavailable}</div>
{:else if capstone}
  <button class="back" onclick={() => nav('#/curso/' + capstone.course_slug)}>‹ Temario</button>

  <div>
    <div class="eyebrow">Reto del módulo {capstone.module_no}</div>
    <h2 style="margin-top:8px">{(capstone.title || '').replace(/^reto:?\s*/i, '')}</h2>
    <p class="muted t-sm" style="margin-top:6px">
      Un caso nuevo. Nada de teoría: demuestra que puedes aplicarlo.
    </p>
  </div>

  <div class="card">
    <div class="microlabel" style="color:var(--amber)">El caso</div>
    <p class="t-base" style="margin-top:8px;white-space:pre-wrap">{capstone.scenario}</p>
  </div>

  <div class="card ai-card">
    <div class="ai-tag"><span class="dot"></span> Tu entregable</div>
    <p class="t-base" style="margin-top:8px">{capstone.deliverable}</p>
  </div>

  {#if capstone.last && phase !== 'done'}
    <div class="microlabel">Tu último intento</div>
    <ScoreCard ev={capstone.last} />
    <DefenseCard ev={capstone.last} />
  {/if}

  <div style="display:flex;flex-direction:column;gap:12px">
    <div>
      <label for="cap">Tu solución</label>
      <textarea id="cap" maxlength="8000" style="min-height:120px" bind:value={content}
                disabled={phase === 'sending' || phase === 'done'}
                oninput={() => save(content)}
                placeholder="Escribe o pega tu solución completa"></textarea>
    </div>

    {#if phase === 'writing'}
      <button class="btn btn-primary" onclick={start}>
        {capstone.last ? 'Intentarlo de nuevo' : 'Enviar mi solución'}
      </button>
    {/if}

    <div class="center muted t-sm" role="status" aria-live="polite">{msg}</div>

    <div style="display:flex;flex-direction:column;gap:12px">
      {#if phase === 'predicting'}
        <PredictionBeat onpick={submit} />
      {:else if phase === 'sending'}
        <ReadingCard message="Tu tutora está leyendo tu solución…" />
      {:else if phase === 'done'}
        <EvalResult ev={evaluation} nodeId={capstone.node_id}
                    onretry={again}
                    onnext={() => nav('#/curso/' + capstone.course_slug)}
                    nextLabel="Volver al temario ›" />
      {/if}
    </div>
  </div>
{/if}
