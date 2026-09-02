<script>
  /* What a long analysis is actually doing, with a real elapsed clock.
   *
   * Shared by the CV reader and the job matcher. No fake percentage: the house
   * rule is that we do not lie to people, and both of these genuinely take one
   * to two minutes. The stage timings are observed, not invented.
   */
  import Icon from './Icon.svelte';

  let { stages, slowAt = null, slowMessage = '' } = $props();

  let elapsed = $state(0);

  $effect(() => {
    const t0 = Date.now();
    const tick = setInterval(() => { elapsed = Math.floor((Date.now() - t0) / 1000); }, 1000);
    return () => clearInterval(tick);
  });

  const active = $derived.by(() => {
    let n = 0;
    stages.forEach(([at], i) => { if (elapsed >= at) n = i; });
    return n;
  });

  const clock = $derived(
    Math.floor(elapsed / 60) + ':' + String(elapsed % 60).padStart(2, '0'),
  );
</script>

<div class="card" style="margin-top:14px">
  {#each stages as [, title, sub], i}
    <div class="jstage" class:done={i < active} class:now={i === active}>
      <div class="jdot"><Icon name="check" class="ic ic-s" /></div>
      <div class="jtxt">
        <div>{title}</div>
        <div class="jsub">
          <p class="faint t-sm" style="margin:0 0 8px">{sub}</p>
          <div class="readline"><i></i></div>
        </div>
      </div>
    </div>
  {/each}
</div>

<div class="row" style="justify-content:space-between;margin-top:10px">
  <span class="faint t-sm">No cierres esta pestaña</span>
  <span class="jclock">{clock}</span>
</div>

{#if slowAt && elapsed >= slowAt}
  <div class="note note-warn">
    <Icon name="alert" class="ic ic-s" /><span>{slowMessage}</span>
  </div>
{/if}
