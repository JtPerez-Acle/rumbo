<script>
  /* "Tu tutora está leyendo": the anticipation state for every evaluation wait.
     They really are 25-35 seconds, so this is not decoration — it is the only
     thing standing between a learner and the belief that the button broke. */
  import Icon from '../Icon.svelte';
  let { message } = $props();
</script>

<div class="card reading" role="status" aria-live="polite">
  <div class="row" style="gap:8px;color:var(--dim);font-size:var(--fs-base)">
    <Icon name="spark" class="ic ic-s" /> <span>{message}</span>
  </div>
  <div class="readline"><i></i></div>
</div>
