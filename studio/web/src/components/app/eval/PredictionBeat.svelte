<script>
  /* Predicting your own grade IS the metacognition this product claims to teach
     (docs/02: "the meta-skill of judging your own work").
   *
   * It used to be a bare number box beside the send button and was used in 2 of
   * 16 real submissions. So it is a beat instead: one tap between deciding to
   * submit and the work leaving your hands, phrased as a judgement rather than
   * a number. Shared by the exercise and the reto — two work products must not
   * ask differently. Always skippable: the platform gates on doing, never on
   * ceremony.
   */
  import Icon from '../Icon.svelte';

  let { onpick } = $props();

  const PREDICTIONS = [
    ['Le falta', 50, 'Sé que está incompleto'],
    ['Va bien', 70, 'Cumple, con huecos'],
    ['Está sólido', 85, 'Lo entregaría a un cliente'],
    ['Es mi mejor trabajo', 95, 'No sabría cómo mejorarlo'],
  ];
</script>

<div class="card-spot">
  <div class="eyebrow">
    <Icon name="target" class="ic ic-s" /> Antes de verla, ¿cómo la ves tú?
  </div>
  <p class="faint t-sm" style="margin:6px 0 12px">
    Acertar no suma puntos. Saber juzgar tu propio trabajo sí es parte del oficio.
  </p>
  <div style="display:flex;flex-direction:column;gap:8px">
    {#each PREDICTIONS as [label, value, hint]}
      <button class="btn btn-ghost" style="width:100%;text-align:left" onclick={() => onpick(value)}>
        <b>{label}</b>
        <span class="faint" style="font-size:var(--fs-xs);display:block;font-weight:500">{hint}</span>
      </button>
    {/each}
  </div>
  <button class="btn btn-ghost btn-sm" style="width:100%;margin-top:8px" onclick={() => onpick(null)}>
    Prefiero no adivinar
  </button>
</div>
