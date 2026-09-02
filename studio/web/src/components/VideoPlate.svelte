<script>
  /* The lesson video, behind a plate.
   *
   * A real frame from the lesson with our own play affordance over it. The
   * <video> element is created on click, so nobody who does not press play pays
   * 5.4 MB for it — this audience is on metered mobile data (PRODUCT.md), and a
   * marketing page is the worst place to spend it.
   */
  import { PATHS } from '../lib/icons.js';

  let playing = $state(false);
  let video;

  function play() {
    playing = true;
    /* iOS Safari only honours autoplay for muted video and wants the call
       inside the gesture; without this the tap does nothing on the product's
       stated primary device. */
    queueMicrotask(() => video?.play?.()?.catch?.(() => {}));
  }
</script>

{#if playing}
  <video bind:this={video} controls autoplay playsinline preload="auto"
         src="/api/learn/public/demo-video"><track kind="captions" /></video>
{:else}
  <button class="videoplate" type="button" aria-label="Reproducir la lección" onclick={play}>
    <img src="/api/learn/public/demo-poster" alt="" width="540" height="960"
         onerror={(e) => e.currentTarget.remove()} />
    <div class="playbtn">
      <svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d={PATHS.play} /></svg>
    </div>
    <div class="plate-meta">
      <div class="microlabel" style="color:var(--paper-dim)">Video · 59 segundos</div>
    </div>
  </button>
{/if}
