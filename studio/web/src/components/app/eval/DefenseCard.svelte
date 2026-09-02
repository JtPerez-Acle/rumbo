<script>
  /* The ownership probe: one question only the person who did the work can
   * answer.
   *
   * Optional, rewarded (+10 max), and RETRYABLE without limit — every
   * evaluation names what a +10 answer would add, and the best attempt is the
   * one that counts, so defending again can only help. We reward appropriation;
   * we never police AI use. AI detection is unreliable and would contradict a
   * curriculum that teaches people to use AI.
   */
  import Icon from '../Icon.svelte';

  let { ev, onscore } = $props();

  let answer = $state((ev.defense && ev.defense.answer) || '');
  let result = $state(ev.defense || null);
  let best = $state(ev.defense_best ?? ev.defense?.bonus ?? 0);
  let finalScore = $state(ev.final_score ?? '—');
  let busy = $state(false);
  let msg = $state('');

  const band = (n) => (n >= 7 ? 'hi' : n >= 4 ? 'mid' : 'lo');

  async function send() {
    if (answer.trim().length < 10) {
      msg = 'Desarrolla tu respuesta un poco más.';
      return;
    }
    busy = true;
    msg = '';
    const res = await fetch('/api/learn/defend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ submission_id: ev.id, answer: answer.trim() }),
    });
    const r = await res.json().catch(() => ({}));
    busy = false;
    if (!res.ok) {
      msg = r.detail || 'No se pudo evaluar, intenta de nuevo.';
      return;
    }
    result = r.defense;
    best = r.best;
    finalScore = r.final_score;
    // The headline score must reflect the bonus just earned. It may rise; the
    // ScoreCard's own rule keeps it from ever falling.
    onscore?.(Math.max(r.final_score ?? 0, r.best_score ?? 0));
  }

  /* A retry must never start blank: the learner is adding to what they said,
     not writing from nothing. */
  function retry() {
    answer = (result && result.answer) || answer;
    result = null;
    msg = '';
  }
</script>

{#if ev.defense_question}
  <div class="card-spot">
    {#if result}
      <div class="eyebrow">
        <Icon name="mic" class="ic ic-s" />
        {best >= 10 ? '¡Llegaste a los 10 puntos!' : 'Tu tutora te respondió'}
      </div>
      <div class="row" style="justify-content:space-between;align-items:flex-start;margin-top:8px">
        <p class="t-base" style="flex:1">{result.comment || ''}</p>
        <div class={`scorepill ${band(result.bonus)}`} style="margin-left:10px">+{result.bonus}</div>
      </div>

      {#if result.missing?.length}
        <div class="note note-goal">
          <b><Icon name="target" class="ic ic-s" /> Para llegar a los 10 puntos:</b>
          <ul style="margin:6px 0 0 18px">
            {#each result.missing as m}<li style="margin-bottom:4px">{m}</li>{/each}
          </ul>
        </div>
      {/if}

      {#if best > result.bonus}
        <div class="note note-goal">
          Se mantiene tu mejor respuesta: <b>+{best}</b> — nunca pierdes puntos
          por volver a intentarlo.
        </div>
      {/if}

      <p class="microlabel" style="margin-top:10px">Nota final: {finalScore}</p>

      {#if best < 10}
        <button class="btn btn-primary btn-sm" style="width:100%;margin-top:12px" onclick={retry}>
          <Icon name="send" class="ic ic-s" /> Responder de nuevo
        </button>
        <p class="faint center" style="font-size:var(--fs-xs);margin-top:6px">
          Intentos ilimitados · siempre se queda tu mejor respuesta
        </p>
      {/if}
    {:else}
      <div class="eyebrow">
        <Icon name="mic" class="ic ic-s" /> Conversa con tu tutora · suma hasta 10 pts
      </div>
      <p class="t-base" style="font-weight:600;margin-top:8px">{ev.defense_question}</p>
      <p class="faint" style="font-size:var(--fs-xs);margin-top:4px">
        {best > 0
          ? 'Suma lo que te faltó y respóndele otra vez. Puedes conversar las veces que quieras hasta llegar a los 10.'
          : 'Responde con tus palabras: solo quien tomó las decisiones contesta bien esto. Si usaste IA, contar qué le cambiaste y por qué también suma. Puedes responder las veces que quieras — se queda tu mejor respuesta.'}
      </p>
      <label class="hide" for="defans">Tu respuesta</label>
      <textarea id="defans" maxlength="2000" style="margin-top:10px"
                bind:value={answer} placeholder="Porque..."></textarea>
      <button class="btn btn-primary btn-sm" style="margin-top:8px;width:100%"
              disabled={busy} onclick={send}>
        <Icon name="send" class="ic ic-s" />
        {busy ? 'Evaluando tu defensa…' : 'Enviar mi respuesta'}
      </button>
      <div class="faint t-sm" style="margin-top:6px" role="status" aria-live="polite">{msg}</div>
    {/if}
  </div>
{/if}
