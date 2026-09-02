<script>
  /* The lesson's entry screen: the video, its transcript, and the guide.
   *
   * Three ways into the same lesson, because the audience is on metered mobile
   * data in stolen time: watch it, read the summary, or work through the
   * written guide. The guide is built on first open rather than on load —
   * mermaid is a lazy chunk and most lessons are read without ever touching it.
   */
  import Icon from '../Icon.svelte';
  import Guide from './Guide.svelte';

  let { lesson, onexplain } = $props();

  const hasGuide = $derived(
    (lesson.written && lesson.written.trim()) || (lesson.diagrams && lesson.diagrams.length),
  );

  let mode = $state(lesson.video_url ? 'ver' : 'leer');
  let guideOpened = $state(false);

  function show(m) {
    mode = m;
    if (m === 'guia') guideOpened = true;
  }

  /* A poster that is ours rather than the first frame, which on a 1080p vertical
     video is usually a blur. Inline SVG: no request, no layout shift. */
  const POSTER =
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 720 1280'%3E" +
    "%3Crect width='720' height='1280' fill='%23161310'/%3E" +
    "%3Ccircle cx='360' cy='640' r='54' fill='none' stroke='%23c98a2b' stroke-width='4'/%3E" +
    "%3Cpath d='M342 610l46 30-46 30z' fill='%23c98a2b'/%3E%3C/svg%3E";
</script>

<div style="display:flex;flex-direction:column;gap:14px">
  <div>
    <div class="eyebrow">
      {lesson.is_review ? 'Repaso' : 'Módulo ' + lesson.module_no} · Día {lesson.position}
    </div>
    <h2 style="margin-top:8px">{lesson.title}</h2>
    {#if lesson.objectives}
      <p class="muted t-sm" style="margin-top:8px">Al terminar podrás: {lesson.objectives}</p>
    {/if}
  </div>

  <div class="seg" role="tablist" aria-label="Cómo seguir la lección">
    <button role="tab" class={mode === 'ver' ? 'on' : ''} aria-selected={mode === 'ver'}
            onclick={() => show('ver')}><Icon name="play" class="ic ic-s" /> Ver</button>
    <button role="tab" class={mode === 'leer' ? 'on' : ''} aria-selected={mode === 'leer'}
            onclick={() => show('leer')}><Icon name="book" class="ic ic-s" /> Resumen</button>
    {#if hasGuide}
      <button role="tab" class={mode === 'guia' ? 'on' : ''} aria-selected={mode === 'guia'}
              onclick={() => show('guia')}><Icon name="tool" class="ic ic-s" /> Guía</button>
    {/if}
  </div>

  {#if mode === 'ver'}
    {#if lesson.video_url}
      <!-- svelte-ignore a11y_media_has_caption -- the transcript IS the caption
           track here, and it is one tab away rather than buried in a menu. -->
      <video src={lesson.video_url} controls playsinline preload="metadata" poster={POSTER}></video>
    {:else}
      <div class="card muted">Video en producción — por ahora usa Resumen y Guía.</div>
    {/if}
  {:else if mode === 'leer'}
    <div style="display:flex;flex-direction:column;gap:12px">
      {#if lesson.key_points?.length}
        <div class="card">
          <div class="microlabel" style="color:var(--amber)">Puntos clave</div>
          <ul style="margin:10px 0 0 18px;font-size:var(--fs-base)">
            {#each lesson.key_points as p}<li style="margin-bottom:7px">{p}</li>{/each}
          </ul>
        </div>
      {/if}
      <div class="card">
        <div class="microlabel">Lección completa</div>
        <p class="t-base" style="margin-top:10px;white-space:pre-wrap">{lesson.transcript || '—'}</p>
      </div>
    </div>
  {:else if guideOpened}
    <Guide {lesson} />
  {/if}

  <!-- Reviews go through explain too: it is retrieval practice, it keeps a
       pending conversation reachable after completion, and it has a skip
       straight to the quiz. -->
  <button class="btn btn-primary" onclick={onexplain}>
    Continuar <Icon name="arrow" class="ic ic-s" />
  </button>
</div>
