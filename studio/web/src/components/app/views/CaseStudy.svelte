<script>
  /* The companion narrative: how the work was done, in STAR form. */
  import PaperDoc from './PaperDoc.svelte';
  let { slug } = $props();
</script>

<PaperDoc {slug} kind="case-study" />
