<script>
  /* The exercise: they paste work they actually produced.
   *
   * This is the step the product exists for — everything before it is delivery.
   * Two things are load-bearing here: the declared project (Aplicación is 40 of
   * the 100 points and is judged against it), and the fact that using AI is
   * explicitly fine. We evaluate that the work is THEIRS, not who wrote the
   * first draft; AI detection is unreliable and would contradict a curriculum
   * that teaches AI use.
   */
  import Icon from '../Icon.svelte';
  import ReadingCard from '../eval/ReadingCard.svelte';
  import EvalResult from '../eval/EvalResult.svelte';
  import ScoreCard from '../eval/ScoreCard.svelte';
  import DefenseCard from '../eval/DefenseCard.svelte';
  import PredictionBeat from '../eval/PredictionBeat.svelte';
  import { postWithTimeout } from '../../../lib/api.js';
  import { loadDraft, draftSaver, clearDraft } from '../../../lib/drafts.js';
  import { session } from '../../../lib/session.svelte.js';
  import { nav } from '../../../lib/router.svelte.js';

  let { lesson, onfinish } = $props();

  const ex = $derived(lesson.exercise || {});
  let content = $state(loadDraft('exercise', lesson.id) || lesson.last_exercise?.content || '');
  let msg = $state('');
  let phase = $state('writing'); // writing | predicting | sending | done
  let evaluation = $state(null);
  let copyLabel = $state('Copiar prompt');
  const save = draftSaver('exercise', lesson.id);

  function start() {
    if (content.trim().length < 20) {
      msg = 'Pega tu trabajo completo, no solo una línea.';
      return;
    }
    msg = '';
    phase = 'predicting';
  }

  async function submit(predicted) {
    phase = 'sending';
    const { res, data } = await postWithTimeout('/api/learn/submit', {
      node_id: lesson.id, kind: 'exercise', content: content.trim(), predicted: predicted ?? null,
    });
    if (!res || !res.ok) {
      phase = 'writing';
      msg = data.detail || 'No pudimos evaluar, intenta de nuevo.';
      return;
    }
    clearDraft('exercise', lesson.id); // it is stored server-side now
    evaluation = data.evaluation;
    phase = 'done';
  }

  function again() {
    evaluation = null;
    phase = 'writing';
    msg = 'Mejora tu entrega con el feedback y envíala de nuevo.';
  }

  async function copyPrompt() {
    try {
      await navigator.clipboard.writeText(ex.starting_point);
      copyLabel = '✓ Copiado';
    } catch {
      copyLabel = 'Selecciónalo y cópialo a mano';
    }
  }
</script>

<div style="display:flex;flex-direction:column;gap:14px">
  <div class="ai-tag"><span class="dot"></span> Tu ejercicio de hoy</div>
  <h2>{lesson.title}</h2>
  <div class="card"><p class="t-base">{ex.instruction || ''}</p></div>

  {#if ex.starting_point}
    <div class="card ai-card">
      <div class="ai-tag"><span class="dot"></span> Pega esto en ChatGPT o Claude</div>
      <div class="prompt">{ex.starting_point}</div>
      <button class="copybtn" onclick={copyPrompt}>
        <Icon name="copy" class="ic ic-s" /> {copyLabel}
      </button>
    </div>
  {/if}

  {#if session.me?.project_name}
    <div class="note note-goal">
      <Icon name="target" class="ic ic-s" />
      <span>Tu proyecto: <b>{session.me.project_name}</b> — tu tutora evalúa contra
      este contexto. Haz el ejercicio sobre él.</span>
    </div>
  {:else}
    <!-- Without a declared project the exercise text still says "elige tu
         proyecto real", which is per-course wording from before the project
         moved to the learner (docs/09). Point them at the one place it lives. -->
    <div class="note note-warn">
      <Icon name="target" class="ic ic-s" />
      <span>Aún no definiste tu proyecto. <b>Aplicación vale 40 de 100 puntos</b>
      y mide qué tan anclado está esto en un proyecto tuyo —
      <button class="linklike" onclick={() => nav('#/perfil')}>defínelo en un minuto</button>.</span>
    </div>
  {/if}

  <div>
    <label for="work">Pega aquí lo que hiciste</label>
    <p class="faint" style="font-size:var(--fs-xs);margin:-2px 0 8px">
      Usar IA está perfecto — es parte del oficio. Suma puntos contar qué le
      cambiaste a su respuesta y por qué.
    </p>
    <textarea id="work" maxlength="5000" bind:value={content}
              disabled={phase === 'sending' || phase === 'done'}
              oninput={() => save(content)}
              placeholder="Tu brief, tus copys, tu plan... lo que produjo el ejercicio. Recibirás feedback al instante."
    ></textarea>
  </div>

  {#if phase === 'writing'}
    <button class="btn btn-primary" onclick={start}>
      {lesson.last_exercise ? 'Enviar de nuevo' : 'Enviar mi trabajo'}
    </button>
    <button class="btn btn-ghost" onclick={onfinish}>Terminar sin enviar</button>
  {/if}

  <div class="center muted t-sm" role="status" aria-live="polite">{msg}</div>

  <div style="display:flex;flex-direction:column;gap:12px">
    {#if phase === 'predicting'}
      <PredictionBeat onpick={submit} />
    {:else if phase === 'sending'}
      <ReadingCard message="Tu tutora está leyendo tu trabajo…" />
    {:else if phase === 'done'}
      <EvalResult ev={evaluation} nodeId={lesson.id}
                  onretry={again} onnext={onfinish} nextLabel="Completar lección ✓" />
    {:else if lesson.last_exercise}
      <div class="microlabel">Tu entrega anterior</div>
      <ScoreCard ev={lesson.last_exercise.evaluation} />
      <DefenseCard ev={lesson.last_exercise.evaluation} />
    {/if}
  </div>
</div>
