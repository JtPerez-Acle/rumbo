<script>
  /* The learner app.
   *
   * One component owns the session and the route; every view below is a plain
   * component that renders from data it fetches itself. That is the same shape
   * the 1,839-line script had — a router calling view functions — with two
   * differences that matter: a view can no longer leave the DOM in a state the
   * next one has to clean up, and each one can be tested on its own.
   *
   * There is nothing to server-render here. The app is behind a session, every
   * screen is per-learner, and robots.txt excludes it on purpose. So this is a
   * client-only island by design rather than by accident — which also means
   * there is exactly one document and no hydration seam to get wrong.
   */
  import TabBar from './TabBar.svelte';
  import { route, startRouter, nav } from '../../lib/router.svelte.js';
  import { session, boot } from '../../lib/session.svelte.js';

  import Today from './views/Today.svelte';
  import Catalog from './views/Catalog.svelte';
  import Outline from './views/Outline.svelte';
  import Lesson from './views/Lesson.svelte';
  import Capstone from './views/Capstone.svelte';
  import Portfolio from './views/Portfolio.svelte';
  import ProjectDoc from './views/ProjectDoc.svelte';
  import CaseStudy from './views/CaseStudy.svelte';
  import Profile from './views/Profile.svelte';
  import Objetivo from './views/Objetivo.svelte';
  import Cv from './views/Cv.svelte';
  import JobAnalyser from '../JobAnalyser.svelte';
  import Orientation from './views/Orientation.svelte';

  $effect(() => {
    const stop = startRouter();
    boot();
    return stop;
  });

  /* Already signed in and asked for #/login: it has nothing to offer, so send
     them where they were going. The hash form still arrives from old links and
     bookmarks. Redirecting in an effect, not in the markup — a navigation
     performed while rendering is a re-entrant render. */
  $effect(() => {
    if (session.ready && route.seg === 'login') nav('#/hoy');
  });

  /* Orientation before anything else on a first login, and reachable later from
     Perfil. It is the only screen that hides the tab bar, because a learner who
     has not chosen a project has nowhere useful to go yet. */
  const orienting = $derived(
    session.ready && (!session.onboarded || route.seg === 'como-funciona'),
  );
</script>

{#if !session.ready}
  <!-- Not "Cargando…": that string was on screen for the several seconds
       hydration took on the OLD public pages and became the symbol of the bug
       this migration removed. Here the wait is one real request for data that
       genuinely does not exist until the server answers. -->
  <div class="center muted" style="margin-top:40px" role="status">Abriendo tu taller…</div>
{:else if orienting}
  <Orientation revisit={route.seg === 'como-funciona'} />
{:else}
  {#key route.seg + '/' + route.arg + '/' + route.step}
    {#if route.seg === 'objetivo'}
      <Objetivo />
    {:else if route.seg === 'oferta'}
      <!-- Reachable while signed in: a learner who finds a new offer must be
           able to analyse it. This branch was missing once, and the "Pega tu
           oferta" button inside #/objetivo silently dropped them on Hoy. -->
      <JobAnalyser signedIn />
    {:else if route.seg === 'cv'}
      <Cv />
    {:else if route.seg === 'cursos'}
      <Catalog />
    {:else if route.seg === 'curso' && route.arg}
      <Outline slug={route.arg} />
    {:else if route.seg === 'leccion' && route.arg}
      <Lesson id={parseInt(route.arg, 10)} step={route.step} />
    {:else if route.seg === 'reto' && route.arg}
      <Capstone id={parseInt(route.arg, 10)} />
    {:else if route.seg === 'portafolio'}
      <Portfolio />
    {:else if route.seg === 'documento' && route.arg}
      <ProjectDoc slug={route.arg} />
    {:else if route.seg === 'caso-view' && route.arg}
      <CaseStudy slug={route.arg} />
    {:else if route.seg === 'perfil'}
      <Profile />
    {:else}
      <Today />
    {/if}
  {/key}
{/if}

{#if session.ready && !orienting}
  <TabBar />
{/if}
