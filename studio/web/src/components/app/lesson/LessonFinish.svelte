<script>
  /* Completing the lesson, and the one place a dropped request must never pass
   * silently.
   *
   * If /complete fails the learner is told, and given a retry. Swallowing it
   * would mean a lesson they did that the streak and the SM-2 ladder never saw.
   */
  import Icon from '../Icon.svelte';
  import { api } from '../../../lib/api.js';
  import { nav } from '../../../lib/router.svelte.js';

  let { lesson, answers, onquiz } = $props();

  let result = $state(null);
  let failed = $state(false);

  const correct = $derived(
    lesson.quiz.reduce((n, q, i) => n + (answers[i] === q.answer ? 1 : 0), 0),
  );

  async function complete() {
    failed = false;
    /* Deep-linked past the quiz — e.g. from a pending conversation on Hoy —
       means there is no quiz result from this session. Never record a phantom
       0: either there is nothing to add (already completed) or they go through
       the quiz first. */
    if (lesson.quiz.length && !Object.keys(answers).length) {
      if (lesson.is_review) return nav('#/curso/' + lesson.course_slug);
      return onquiz();
    }
    const score = lesson.quiz.length ? correct / lesson.quiz.length : 1;
    try {
      const r = await api('/complete', {
        method: 'POST',
        body: JSON.stringify({ node_id: lesson.id, quiz_score: score, is_review: !!lesson.is_review }),
      });
      if (!r || r.ok !== true) throw new Error('not ok');
      result = r;
    } catch {
      failed = true;
    }
  }

  $effect(() => { complete(); });
</script>

{#if failed}
  <div class="celebrate">
    <h2 style="margin-top:30px">No pudimos guardar tu avance</h2>
    <p class="muted t-sm">
      Revisa tu conexión — tu lección no se pierde, solo falta registrarla.
    </p>
  </div>
  <button class="btn btn-primary" style="margin-top:18px" onclick={complete}>Reintentar</button>
{:else if result}
  <div class="celebrate">
    <div class="medal"><Icon name={lesson.is_review ? 'redo' : 'spark'} class="ic" /></div>
    <h2 style="font-size:var(--fd-lg);margin-top:18px">
      {lesson.is_review ? 'Repaso listo' : 'Lección ' + lesson.position + ' completada'}
    </h2>
    <p class="muted">{correct} de {lesson.quiz.length} en el quiz.</p>
    <div class="bigstreak">{result.streak}</div>
    <div class="microlabel">días seguidos</div>
  </div>
  <button class="btn btn-primary" style="margin-top:24px"
          onclick={() => (lesson.next_id
            ? nav('#/leccion/' + lesson.next_id)
            : nav('#/curso/' + lesson.course_slug))}>
    {lesson.next_id ? 'Siguiente lección ›' : 'Volver al temario'}
  </button>
  <button class="btn btn-ghost" style="margin-top:10px"
          onclick={() => nav('#/curso/' + lesson.course_slug)}>Ver el temario</button>
{/if}
