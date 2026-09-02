<script>
  /* The temario, with this learner's state on it.
   *
   * Two rules from docs/10 are visible here and both are easy to get wrong:
   * a SKIPPED module is collapsed, never removed and never locked — the ask was
   * "no me hagas ver de nuevo lo que ya sé", and hiding it for good would be the
   * opposite failure — and an ACCREDITED one says so with its score, because it
   * was earned by passing the reto rather than claimed on a CV.
   */
  import Icon from '../Icon.svelte';
  import DeliverableCard from './DeliverableCard.svelte';
  import { api, toLogin } from '../../../lib/api.js';
  import { nav } from '../../../lib/router.svelte.js';

  let { slug } = $props();

  let course = $state(null);
  let shown = $state(new Set());   // skipped modules the learner opened
  let expanded = $state(new Set()); // locked lessons showing their objectives

  $effect(() => {
    (async () => {
      const d = await api('/course/' + slug);
      if (d.__unauth) return toLogin();
      course = d;
    })();
  });

  const pct = $derived(course?.total ? Math.round((course.done / course.total) * 100) : 0);

  const STATUS = { done: 'Completada', current: 'Disponible', coming: 'En producción', locked: 'Bloqueada' };
  const MARK = { done: 'check', locked: 'lock', coming: 'clock' };

  function toggle(set, key, assign) {
    const next = new Set(set);
    next.has(key) ? next.delete(key) : next.add(key);
    assign(next);
  }

  const capstoneLabel = (c) =>
    c.status === 'done'
      ? (c.score != null ? c.score + '/100' : 'Completado')
      : c.test_out ? 'Pruébalo'
      : c.status === 'available' ? 'Disponible'
      : 'Bloqueado';
</script>

{#if course}
  <button class="back" onclick={() => nav('#/cursos')}>‹ Cursos</button>

  <div>
    <h2>{course.title}</h2>
    {#if course.description}
      <p class="muted t-sm" style="margin-top:8px">{course.description}</p>
    {/if}
    <div class="row" style="justify-content:space-between;margin:12px 0 8px">
      <span class="microlabel">Tu avance</span>
      <span class="microlabel">{course.done}/{course.total} · {pct}%</span>
    </div>
    <div class="prog"><i style={`clip-path:inset(0 ${100 - (pct)}% 0 0)`}></i></div>
    <p class="faint" style="font-size:var(--fs-xs);margin-top:8px">
      Toca cualquier lección bloqueada para ver qué aprenderás en ella.
    </p>
  </div>

  {#each course.modules as m}
    <div class="modhead">
      Módulo {m.module_no} · {m.module_title}
      {#if m.exempt === 'acreditado'}
        <span class="pill go" style="margin-left:8px">Acreditado {m.exempt_score || ''}</span>
      {:else if m.exempt}
        <span class="pill soon" style="margin-left:8px">Ya lo sabes</span>
      {/if}
    </div>
    {#if m.module_description}
      <p class="muted t-sm" style="margin:-2px 0 10px">{m.module_description}</p>
    {/if}

    {#if m.exempt}
      <button class="lrow clickable" style="opacity:.75"
              aria-expanded={shown.has(m.module_no)}
              onclick={() => toggle(shown, m.module_no, (v) => (shown = v))}>
        <div class="num"><Icon name="check" class="ic ic-s" /></div>
        <div class="lt">
          {m.exempt === 'acreditado' ? 'Lo acreditaste con su reto' : 'Te saltaste este módulo'}
        </div>
        <div class="st">Ver igual</div>
      </button>
    {/if}

    {#if !m.exempt || shown.has(m.module_no)}
      {#each m.lessons as l}
        {@const clickable = l.status === 'done' || l.status === 'current'}
        <svelte:element
          this={clickable || l.objectives ? 'button' : 'div'}
          class={`lrow ${l.status} ${clickable ? 'clickable' : ''}`}
          style={l.objectives ? 'flex-wrap:wrap' : undefined}
          aria-expanded={!clickable && l.objectives ? expanded.has(l.id) : undefined}
          onclick={clickable
            ? () => nav('#/leccion/' + l.id)
            : l.objectives
              ? () => toggle(expanded, l.id, (v) => (expanded = v))
              : undefined}
        >
          <div class="num">
            {#if MARK[l.status]}<Icon name={MARK[l.status]} class="ic ic-s" />{:else}{l.position}{/if}
          </div>
          <div class="lt">{l.title}</div>
          <div class="st">{STATUS[l.status]}</div>
          {#if l.objectives && (clickable || expanded.has(l.id))}
            <div class="obj">Al terminar podrás: {l.objectives}</div>
          {/if}
        </svelte:element>
      {/each}
    {/if}

    {#if m.capstone}
      {@const c = m.capstone}
      <svelte:element
        this={c.status === 'locked' ? 'div' : 'button'}
        class={`lrow caprow ${c.status === 'locked' ? 'locked' : 'clickable'}`}
        style={c.test_out ? 'border-color:var(--amber)' : undefined}
        onclick={c.status === 'locked' ? undefined : () => nav('#/reto/' + c.id)}
      >
        <div class="num"><Icon name="flag" class="ic ic-s" /></div>
        <div class="lt">
          {c.test_out ? 'Acredita este módulo: ' : 'Reto: '}{(c.title || '').replace(/^reto:?\s*/i, '')}
        </div>
        <div class="st">{capstoneLabel(c)}</div>
      </svelte:element>
    {/if}
  {/each}

  <DeliverableCard {slug} />
{/if}
