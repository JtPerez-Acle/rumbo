<script>
  /* THE NUMBER ON SCREEN IS THEIR NOTA — the best they have earned — and never
   * the attempt they happen to have just sent.
   *
   * A learner watched 79 become 50 become 30 on the same work and stopped. The
   * score was safe in the database the whole time, which helped nobody: the
   * screen, not the schema, is where "nothing you earn may ever go down" has to
   * be visible. A weaker attempt is DIAGNOSTIC — we say what it would have
   * scored and why, and the nota does not move. Retrying can only teach you
   * something, never cost you something.
   */
  import Icon from '../Icon.svelte';

  let { ev, animate = false, headline = $bindable(null) } = $props();

  const mine = $derived(ev.final_score ?? ev.score);              // this attempt
  const best = $derived(ev.best_score != null ? ev.best_score : mine); // what they keep
  const shown = $derived(
    mine != null && best != null ? Math.max(mine, best) : (mine ?? best),
  );
  const lower = $derived(mine != null && best != null && mine < best);
  const band = (n) => (n >= 80 ? 'hi' : n >= 60 ? 'mid' : 'lo');

  /* The headline can RISE from a conversation bonus — the defensa's award is
     part of the nota — but it can never fall because a learner defended an
     older attempt. Same rule as the score itself. */
  const displayed = $derived(Math.max(shown ?? 0, headline ?? 0));

  const D = $derived(ev.dimensions);
  const gap = $derived(
    ev.predicted != null && ev.score != null ? ev.predicted - ev.score : null,
  );

  /* Bars fill in sequence, then the serif number counts up. `animate` is off on
     a re-render of an evaluation the learner has already seen — replaying the
     reveal every time they navigate back is a celebration that stops meaning
     anything. */
  let counted = $state(animate ? 0 : null);
  let barsOut = $state(animate);

  $effect(() => {
    if (!animate) return;
    const target = displayed || 0;
    const t0 = performance.now();
    const dur = 850;
    let raf;
    const tick = (t) => {
      const p = Math.min(1, (t - t0) / dur);
      counted = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    const bars = setTimeout(() => (barsOut = false), 150);
    return () => { cancelAnimationFrame(raf); clearTimeout(bars); };
  });

  const width = (v, max) => Math.max(2, Math.round((v / max) * 100));
  const DIMS = [['Aplicación', 'aplicacion', 40], ['Criterio', 'criterio', 30], ['Ejecución', 'ejecucion', 30]];
</script>

<div class="card" style="margin-top:4px">
  <div class="row" style="justify-content:space-between;align-items:flex-start;margin-bottom:8px">
    <div class="microlabel" style="color:var(--amber);padding-top:10px">
      {lower ? 'Tu nota' : 'Tu evaluación'}{ev.attempt && ev.attempt > 1 ? ` · intento ${ev.attempt}` : ''}
    </div>
    <div class={`scorebig ${band(displayed)}`}>
      {counted != null ? counted : (displayed ?? '—')}
    </div>
  </div>

  {#if ev.unchanged}
    <div class="note note-warn" style="margin-bottom:8px">
      <Icon name="alert" class="ic ic-s" /> Es la misma entrega de antes, así que
      mantiene su nota. Cambia lo que te señalé abajo y vuelve a enviarla.
    </div>
  {/if}

  {#if lower}
    <!-- Framed as what it IS — a version that would have scored less — instead
         of as a new, lower grade. The nota above it does not move. -->
    <div class="note note-warn" style="margin-bottom:8px">
      <Icon name="alert" class="ic ic-s" />
      <span><b>Tu nota sigue siendo {best}.</b> Esta versión habría sacado {mine};
      abajo te explico por qué, para que la siguiente suba y no para restarte.</span>
    </div>
    <div class="microlabel" style="margin:6px 0 2px">Cómo puntuaría esta versión</div>
  {/if}

  {#if D}
    <div style="margin:2px 0 10px">
      {#each DIMS as [label, key, max]}
        <div class="dimrow">
          <span>{label}</span>
          <div class="prog"><i style={`clip-path:inset(0 ${100 - (barsOut ? 0 : width(D[key], max))}% 0 0)`}></i></div>
          <span>{D[key]}/{max}</span>
        </div>
      {/each}
    </div>
  {/if}

  <p class="t-base">{ev.feedback || ''}</p>

  {#if ev.misconception}
    <div class="note note-warn"><Icon name="alert" class="ic ic-s" /> {ev.misconception}</div>
  {/if}

  {#if ev.missing?.length}
    <div class="note note-goal">
      <b><Icon name="target" class="ic ic-s" />
        {lower ? 'Lo que le falta a esta versión:' : 'Para llegar a 100 te falta:'}</b>
      <ul style="margin:6px 0 0 18px">
        {#each ev.missing as m}<li style="margin-bottom:4px">{m}</li>{/each}
      </ul>
    </div>
  {:else if ev.improve}
    <div class="note note-goal">→ {ev.improve}</div>
  {/if}

  {#if gap != null}
    <p class="faint" style="font-size:var(--fs-xs);margin-top:8px">
      Tu predicción: {ev.predicted} · Nota: {ev.score}{Math.abs(gap) >= 15
        ? (gap > 0
          ? ' — esta vez fuiste optimista; saber autoevaluarse también se entrena.'
          : ' — te subestimaste; tu trabajo vale más de lo que crees.')
        : ' — bien calibrada.'}
    </p>
  {/if}
</div>
