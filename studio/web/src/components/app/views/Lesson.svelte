<script>
  /* One lesson, and the five steps it runs through.
   *
   * The step lives in this component rather than in the URL for everything past
   * the entry point, but the URL can still ADDRESS each one — `#/leccion/12/
   * ejercicio` lands there. That is load-bearing: a pending conversation
   * surfaced on Hoy must arrive exactly where it can be answered, and before
   * those deep links existed a completed lesson skipped the explain step and
   * the conversation was unreachable.
   */
  import LessonShell from '../lesson/LessonShell.svelte';
  import LessonVideo from '../lesson/LessonVideo.svelte';
  import LessonExplain from '../lesson/LessonExplain.svelte';
  import LessonQuiz from '../lesson/LessonQuiz.svelte';
  import LessonExercise from '../lesson/LessonExercise.svelte';
  import LessonFinish from '../lesson/LessonFinish.svelte';
  import { api, toLogin } from '../../../lib/api.js';

  let { id, step: initialStep } = $props();

  const STEP_OF = { explica: 'explain', quiz: 'quiz', ejercicio: 'exercise' };

  let lesson = $state(null);
  let step = $state(STEP_OF[initialStep] || 'video');
  /* Quiz answers live here, not in the quiz component: LessonFinish scores them
     and has to be able to tell "answered nothing" from "answered wrong". */
  let answers = $state({});

  $effect(() => {
    (async () => {
      const l = await api('/lesson/' + id);
      if (l.__unauth) return toLogin();
      // is_review comes ONLY from the server (completed = review). Deciding it
      // client-side made completions reached via prev/next silently not count.
      lesson = l;
      answers = {};
      step = STEP_OF[initialStep] || 'video';
    })();
  });
</script>

{#if lesson}
  <LessonShell {lesson} showNav={step === 'video'}>
    {#if step === 'video'}
      <LessonVideo {lesson} onexplain={() => (step = 'explain')} />
    {:else if step === 'explain'}
      <LessonExplain {lesson} onquiz={() => (step = 'quiz')} />
    {:else if step === 'quiz'}
      <LessonQuiz {lesson} {answers} onexercise={() => (step = 'exercise')} />
    {:else if step === 'exercise'}
      <LessonExercise {lesson} onfinish={() => (step = 'finish')} />
    {:else}
      <LessonFinish {lesson} {answers} onquiz={() => (step = 'quiz')} />
    {/if}
  </LessonShell>
{/if}
