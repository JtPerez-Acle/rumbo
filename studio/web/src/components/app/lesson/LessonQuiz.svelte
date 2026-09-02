<script>
  /* The quiz. Three questions where the wrong answers also teach: picking one
     reveals the explanation rather than just marking it red, and the question
     locks so the learner cannot fish for the right answer.
   */
  import Icon from '../Icon.svelte';

  let { lesson, answers, onexercise } = $props();

  const done = $derived(Object.keys(answers).length === lesson.quiz.length);

  function pick(qi, oi) {
    if (answers[qi] !== undefined) return; // locked once answered
    answers[qi] = oi;
  }
</script>

<div style="display:flex;flex-direction:column;gap:16px">
  <div class="eyebrow">Quiz · {lesson.quiz.length} preguntas</div>

  {#each lesson.quiz as q, qi}
    <div class="qblock">
      <h4>{qi + 1}. {q.q}</h4>
      {#each q.options as opt, oi}
        {@const answered = answers[qi] !== undefined}
        <button
          class={`opt ${answered && oi === q.answer ? 'correct' : ''} ${answered && oi === answers[qi] && oi !== q.answer ? 'wrong' : ''}`}
          disabled={answered}
          onclick={() => pick(qi, oi)}
        >
          <span class="key">{String.fromCharCode(65 + oi)}</span><span>{opt}</span>
        </button>
      {/each}
      {#if answers[qi] !== undefined}
        <div class="explain">{q.explain || ''}</div>
      {/if}
    </div>
  {/each}

  {#if done}
    <button class="btn btn-primary" onclick={onexercise}>
      Ir al ejercicio <Icon name="arrow" class="ic ic-s" />
    </button>
  {/if}
</div>
