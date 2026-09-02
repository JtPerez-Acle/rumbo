<script>
  /* Proves the Svelte island pipeline compiles and hydrates. Deleted in phase 2
     with the page that mounts it. */
  let lit = $state(false);
</script>

<button onclick={() => (lit = !lit)} style="color: var(--amber-ink); background: var(--amber)">
  {lit ? 'lit' : 'dark'}
</button>
