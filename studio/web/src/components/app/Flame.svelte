<script>
  /* The streak chip: ember (0) → lit (1-6) → roaring (7+).
     A daily streak with a one-day grace is the ONLY gamification in this
     product — no badges, no XP (PRODUCT.md). */
  import Icon from './Icon.svelte';
  let { days = 0 } = $props();
</script>

<div class={`flame ${days >= 7 ? 'hot' : days >= 1 ? 'lit' : ''}`}>
  <Icon name="flame" class="ic ic-s" /> {days}
</div>
