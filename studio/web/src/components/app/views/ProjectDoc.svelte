<script>
  /* The work document: the learner's own submissions compiled into the thing a
     client would have paid for. Not a certificate — the product refuses those. */
  import PaperDoc from './PaperDoc.svelte';
  let { slug } = $props();
</script>

<PaperDoc {slug} kind="project-doc" />
