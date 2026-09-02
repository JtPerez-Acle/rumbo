<script>
  /* "Cómo funciona" on two axes, because those are the two questions someone
     actually has: QUÉ HAGO (numbered steps, in order) and QUÉ RECIBO.
   *
   * ONE source, rendered on the public landing AND in first-login orientation.
   * The previous single list had gone stale describing a course-shaped product
   * months after the goal engine shipped, on the one screen new learners read.
   */
  import Icon from '../Icon.svelte';
  import { STEPS, GETS } from '../../../lib/site.js';
</script>

<section class="u-full band-lo">
  <div class="microlabel">Cómo funciona · cuatro pasos</div>
  <div class="u-wide steps" style="margin-top:var(--s4)">
    {#each STEPS as [title, text], i}
      <div class="card">
        <div class="stephead">
          <span class="stepnum">{i + 1}</span>
          <b class="t-md">{title}</b>
        </div>
        <p class="muted t-sm" style="margin-top:8px">{text}</p>
      </div>
    {/each}
  </div>
</section>

<section class="u-wide" style="margin-top:var(--s6)">
  <div class="microlabel">Qué te llevas</div>
  <div class="takeaways" style="margin-top:var(--s4)">
    {#each GETS as [icon, title, text]}
      <div class="card">
        <div class="row" style="gap:10px;color:var(--amber)">
          <Icon name={icon} /><b class="t-md" style="color:var(--text)">{title}</b>
        </div>
        <p class="muted t-sm" style="margin-top:8px">{text}</p>
      </div>
    {/each}
  </div>
  <p class="faint t-sm" style="margin:var(--s4) 2px 0">
    No damos certificados: nadie contrata por uno nuestro. Damos el trabajo que
    hiciste, con tu nombre.
  </p>
</section>
