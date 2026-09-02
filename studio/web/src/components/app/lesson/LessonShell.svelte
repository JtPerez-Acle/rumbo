<script>
  /* The frame every lesson step sits in.
   *
   * Prev/next appear ONLY on the lesson's entry screen. Mid-flow — explain,
   * quiz, exercise — they invited wandering off and losing progress, which on a
   * step that has just taken thirty seconds of evaluation is expensive.
   */
  import { nav } from '../../../lib/router.svelte.js';

  let { lesson, showNav = false, children } = $props();
</script>

<div class="lesson-head">
  <button class="back" onclick={() => nav('#/curso/' + lesson.course_slug)}>‹ Temario</button>
  <span class="microlabel">Lección {lesson.position} de {lesson.total}</span>
</div>

{@render children()}

{#if showNav}
  <div class="navbtns">
    <button disabled={!lesson.prev_id}
            onclick={() => lesson.prev_id && nav('#/leccion/' + lesson.prev_id)}>‹ Anterior</button>
    <button disabled={!lesson.next_id}
            onclick={() => lesson.next_id && nav('#/leccion/' + lesson.next_id)}>Siguiente ›</button>
  </div>
{/if}
