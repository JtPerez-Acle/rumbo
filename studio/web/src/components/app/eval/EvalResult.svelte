<script>
  /* Feedback is an invitation, not a verdict.
   *
   * Below 90 the primary action is to improve the answer; the path forward is
   * always available but never pushy. Above it, the order flips. The platform
   * gates on doing, never on passing — punishment churns, feedback teaches.
   */
  import Icon from '../Icon.svelte';
  import ScoreCard from './ScoreCard.svelte';
  import VerdictCard from './VerdictCard.svelte';
  import DefenseCard from './DefenseCard.svelte';

  let { ev, nodeId, onretry, onnext, nextLabel, animate = true } = $props();

  let headline = $state(null);

  const isVerdict = $derived(!!ev.verdict || ev.kind === 'explain');
  const good = $derived(isVerdict ? ev.verdict === 'lo_tienes' : (ev.score ?? 0) >= 90);
</script>

{#if isVerdict}
  <VerdictCard {ev} {nodeId} />
{:else}
  <ScoreCard {ev} {animate} bind:headline />
{/if}

<!-- The defensa has its own card, and it is retryable. Never duplicated inside
     the score card: two places showing the same bonus drift. -->
<DefenseCard {ev} onscore={(n) => (headline = n)} />

{#snippet retryButton()}
  <button class={`btn ${good ? 'btn-ghost' : 'btn-primary'}`} onclick={onretry}>
    <Icon name="pen" class="ic ic-s" /> {isVerdict ? 'Explicarlo de nuevo' : 'Mejorar mi respuesta'}
  </button>
{/snippet}

{#snippet nextButton()}
  <button class={`btn ${good ? 'btn-primary' : 'btn-ghost'}`} onclick={onnext}>{nextLabel}</button>
{/snippet}

{#if good}
  {@render nextButton()}
  {@render retryButton()}
{:else}
  {@render retryButton()}
  {@render nextButton()}
{/if}
