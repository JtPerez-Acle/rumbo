<script>
  /* "Seguir leyendo la guía".
   *
   * This is NOT a disclosure, which is why it is not a <details>. A disclosure
   * hides its content when closed; this control CLAMPS it — the guide is always
   * visible and always readable, and the button lifts a 560px cap. There is no
   * HTML primitive for that, and <details> was tried first: it hid the guide
   * entirely on the closed state, which is a worse page than the one it
   * replaced.
   *
   * The guide itself is slotted, so it is rendered by Astro at build time and
   * arrives in the HTML. It is never serialized into this island's props and
   * never shipped twice.
   */
  let { children } = $props();
  let open = $state(false);
</script>

<div class={open ? 'guide-open' : ''}>
  {@render children()}
  <button
    class="btn btn-ghost btn-sm"
    type="button"
    style="margin-top:var(--s2)"
    aria-expanded={open}
    onclick={() => (open = !open)}
  >
    {open ? 'Mostrar menos' : 'Seguir leyendo la guía'}
  </button>
</div>
