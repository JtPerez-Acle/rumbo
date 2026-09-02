<script>
  /* Explain it back. The comprehension check, and it never carries a number.
   *
   * "Esto no lleva nota" is on screen because it is true and because it changes
   * what people write: asked for a grade they write for the grader, asked to
   * explain they explain.
   */
  import ReadingCard from '../eval/ReadingCard.svelte';
  import EvalResult from '../eval/EvalResult.svelte';
  import ScoreCard from '../eval/ScoreCard.svelte';
  import DefenseCard from '../eval/DefenseCard.svelte';
  import { postWithTimeout } from '../../../lib/api.js';
  import { loadDraft, draftSaver, clearDraft } from '../../../lib/drafts.js';

  let { lesson, onquiz } = $props();

  let content = $state(loadDraft('explain', lesson.id) || lesson.last_explain?.content || '');
  let msg = $state('');
  let sending = $state(false);
  let evaluation = $state(null);
  const save = draftSaver('explain', lesson.id);

  async function send() {
    if (content.trim().length < 20) {
      msg = 'Escribe al menos un par de frases.';
      return;
    }
    msg = '';
    sending = true;
    const { res, data } = await postWithTimeout('/api/learn/submit', {
      node_id: lesson.id, kind: 'explain', content: content.trim(),
    });
    sending = false;
    if (!res || !res.ok) {
      msg = data.detail || 'No pudimos evaluar, intenta de nuevo.';
      return;
    }
    clearDraft('explain', lesson.id);
    evaluation = data.evaluation;
  }

  function again() {
    evaluation = null;
    msg = 'Ajusta tu respuesta con el feedback en mente y envíala de nuevo.';
  }
</script>

<div style="display:flex;flex-direction:column;gap:14px">
  <div>
    <div class="eyebrow">Antes del quiz</div>
    <h2 style="margin-top:8px">Explícalo en tus palabras</h2>
    {#if lesson.explain_prompt}
      <div class="card" style="margin-top:10px;border-color:rgba(240,164,60,.35)">
        <p class="t-md" style="font-weight:600">{lesson.explain_prompt}</p>
      </div>
      <p class="muted t-sm" style="margin-top:8px">
        Respóndelo como se lo contarías a un amigo, con tus palabras y tu ejemplo.
      </p>
    {:else}
      <p class="muted t-sm" style="margin-top:6px">
        Como si se lo contaras a un amigo que no vio el video. Si puedes
        explicarlo, lo entendiste de verdad.
      </p>
    {/if}
  </div>

  <label class="hide" for="expl">Tu explicación</label>
  <textarea id="expl" maxlength="5000" bind:value={content} disabled={sending || !!evaluation}
            oninput={() => save(content)} placeholder="Lo que entendí es que..."></textarea>
  <p class="faint" style="font-size:var(--fs-xs)">
    Esto no lleva nota: es para ver si el concepto te quedó claro. Explícalo en
    abstracto o con un ejemplo, como prefieras.
  </p>

  {#if !sending && !evaluation}
    <button class="btn btn-primary" onclick={send}>
      {lesson.last_explain ? 'Enviar de nuevo' : 'Enviar mi explicación'}
    </button>
    <button class="btn btn-ghost" onclick={onquiz}>Ir directo al quiz ›</button>
  {/if}

  <div class="center muted t-sm" role="status" aria-live="polite">{msg}</div>

  <div style="display:flex;flex-direction:column;gap:12px">
    {#if sending}
      <ReadingCard message="Tu tutora está leyendo tu explicación…" />
    {:else if evaluation}
      <EvalResult ev={evaluation} nodeId={lesson.id}
                  onretry={again} onnext={onquiz} nextLabel="Continuar al quiz ›" />
    {:else if lesson.last_explain}
      <div class="microlabel">Tu entrega anterior</div>
      <ScoreCard ev={lesson.last_explain.evaluation} />
      <DefenseCard ev={lesson.last_explain.evaluation} />
    {/if}
  </div>
</div>
