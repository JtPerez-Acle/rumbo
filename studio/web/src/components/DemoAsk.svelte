<script>
  /* The question, and the real verdict.
   *
   * This is the surface's whole argument: a stranger writes their own
   * explanation and the same evaluator a paying learner uses answers it, before
   * anything is asked of them. Everything else on the landing is static; this
   * is the one part that has to be alive.
   */
  import { PATHS } from '../lib/icons.js';
  import { TUTOR, VERDICT_WORD } from '../lib/site.js';

  /* The demo lesson, already loaded at build time by the page. The SPA fetched
     it here and the page waited on the network to know what question to ask. */
  let { lesson } = $props();

  const EVAL_TIMEOUT_MS = 90000;
  const DRAFT_KEY = 'aprende_draft_demo_0';

  let answer = $state('');
  let company = $state(''); // honeypot
  let msg = $state('');
  let busy = $state(false);
  let evaluation = $state(null);
  let showDoors = $state(false);
  let result;

  /* Drafts survive a reload. An evaluation takes 25–35 seconds and this
     audience studies on a phone in stolen time; losing what they typed to a
     backgrounded tab is the cheapest possible way to lose them. */
  $effect(() => {
    try {
      const saved = localStorage.getItem(DRAFT_KEY);
      if (saved && !answer) answer = saved;
    } catch { /* private mode */ }
  });

  function saveDraft() {
    try { localStorage.setItem(DRAFT_KEY, answer); } catch { /* private mode */ }
  }

  async function submit() {
    const content = answer.trim();
    if (content.length < 40) {
      msg = 'Escríbelo con tus palabras: unas dos o tres frases bastan.';
      return;
    }
    busy = true;
    msg = '';
    showDoors = false;

    /* A hard timeout, not just the server's. Without one this button stays
       disabled forever on a dropped connection, which reads as a broken page. */
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), EVAL_TIMEOUT_MS);
    let res, data;
    try {
      res = await fetch('/api/learn/public/demo-explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, company }),
        signal: ctrl.signal,
      });
      data = await res.json();
    } catch {
      data = null;
    } finally {
      clearTimeout(timer);
      busy = false;
    }

    if (!res || !res.ok) {
      /* This used to be a dead end: the failure branch set a message and
         stopped, so a visitor who did exactly what the page asked and hit the
         rate cap got a lowercase server fragment under a re-enabled button,
         with nowhere to go. The 429 gets its own sentence because "demasiadas
         peticiones" describes our rate limiter, not their situation — and the
         door that is still open is the one this page is pointing at anyway. */
      msg = res && res.status === 429
        ? `Ya evaluamos varias respuestas desde aquí en la última hora: es una alfa y ${TUTOR} corre de a poco. Vuelve en un rato — o dinos qué quieres ser y te armamos la ruta ahora, que eso sí está abierto.`
        : (data && data.detail) || 'No pudimos evaluarla ahora. Intenta en un momento.';
      showDoors = true;
      return;
    }

    try { localStorage.removeItem(DRAFT_KEY); } catch { /* private mode */ }
    evaluation = data.evaluation || {};
    await Promise.resolve();
    const quiet = window.matchMedia?.('(prefers-reduced-motion:reduce)').matches;
    result?.scrollIntoView({ behavior: quiet ? 'auto' : 'smooth', block: 'start' });
  }

  const verdict = $derived(evaluation?.verdict || 'casi');
  const missing = $derived(evaluation?.missing || []);
</script>

{#snippet icon(name, cls = 'ic ic-s')}
  <svg class={cls} viewBox="0 0 24 24" aria-hidden="true"><path d={PATHS[name]} /></svg>
{/snippet}

{#snippet doors(kind)}
  <div class="doors" style="margin-top:var(--s5)">
    <a class={`btn ${kind === 'lit' ? 'btn-primary' : 'btn-ghost'}`} href="/oferta">
      Dinos qué quieres ser {@render icon('arrow')}
    </a>
    <a class="doorlink" href="/lista">o pide tu acceso</a>
  </div>
{/snippet}

<div class="demoq">
  <div class="eyebrow">Ahora tú</div>
  <h2 id="dqq" class="askq" style="margin:8px 0 4px">
    {lesson.explain_prompt || 'Explícalo en tus palabras.'}
  </h2>
  <p class="muted t-sm" style="margin-top:6px">
    Con tus palabras, como se lo explicarías a alguien. No hay nota: esto se
    responde con <b>Lo tienes</b>, <b>Casi</b> o <b>Todavía no</b>, y con lo que
    te falta.
  </p>

  <label for="dq" class="hide">Tu explicación</label>
  <textarea
    id="dq" maxlength="4000" aria-labelledby="dqq" bind:value={answer}
    oninput={saveDraft} placeholder="Escribe aquí tu explicación…"
  ></textarea>

  <p class="faint t-sm" style="margin-top:8px">
    Guardamos lo que escribes, sin tu nombre ni tu correo, solo para saber si la
    lección enseña.
  </p>

  <input
    bind:value={company} tabindex="-1" autocomplete="off" aria-hidden="true"
    style="position:absolute;left:-9999px;opacity:0;height:0;width:0" />

  <button class="btn btn-primary" type="button" style="margin-top:var(--s3)"
          onclick={submit} disabled={busy}>
    Que la tutora lo lea {@render icon('arrow')}
  </button>

  {#if busy}
    <!-- The tutor is reading: the anticipation state every evaluation wait uses. -->
    <div class="card reading">
      <div class="row" style="gap:8px;color:var(--dim);font-size:var(--fs-base)">
        {@render icon('spark')}<span>Tu tutora está leyendo tu respuesta…</span>
      </div>
      <div class="readline"><i></i></div>
    </div>
  {/if}

  <div class="center muted t-sm" style="margin-top:8px" role="status" aria-live="polite">{msg}</div>
  {#if showDoors}{@render doors('ghost')}{/if}
</div>

<div bind:this={result} role="status" aria-live="polite">
  {#if evaluation}
    <div class="card card-spot" style="margin-top:var(--s4)">
      <div class="row" style="justify-content:space-between;align-items:flex-start;gap:10px">
        <div class={`verdict ${verdict}`}>{VERDICT_WORD[verdict] || 'Casi'}</div>
        <span class={`vchip ${verdict}`}>tu tutora</span>
      </div>
      <p class="t-base" style="margin-top:var(--s3);white-space:pre-wrap">{evaluation.feedback || ''}</p>
      {#if evaluation.misconception}
        <div class="note note-warn" style="margin-top:var(--s3)">
          {@render icon('alert')}<span>{evaluation.misconception}</span>
        </div>
      {/if}
    </div>

    {#if missing.length}
      <div class="microlabel" style="margin-top:var(--s3)">Para redondearlo te falta</div>
      <div class="card">
        {#each missing as x}
          <div class="gaprow"><span class="gx">{@render icon('alert')}</span><span>{x}</span></div>
        {/each}
      </div>
    {/if}

    <!-- What the rest of the loop actually is — shown with this lesson's real
        exercise, this module's real reto and the real document the course ends
        in. Sections that restate a claim in different words add length, not
        substance. -->
    <div class="microlabel" style="margin-top:var(--s5)">Llevas dos de los cinco pasos. Así sigue</div>
    <div class="card">
      <div class="nextup">
        <div class="nn">3</div>
        <div>
          <div style="font-weight:700;font-size:var(--fs-md)">El quiz</div>
          <div class="muted t-sm" style="margin-top:3px">Tres preguntas donde las respuestas equivocadas también enseñan.</div>
        </div>
      </div>
      <div class="nextup">
        <div class="nn">4</div>
        <div>
          <div style="font-weight:700;font-size:var(--fs-md)">
            {lesson.exercise?.instruction ? 'El ejercicio, sobre tu proyecto real' : 'El ejercicio'}
          </div>
          <div class="muted t-sm" style="margin-top:3px">
            {lesson.exercise?.instruction
              ? lesson.exercise.instruction.slice(0, 190)
              : 'Produces algo real y lo pegas; tu tutora lo evalúa en tres dimensiones.'}
          </div>
        </div>
      </div>
      <div class="nextup">
        <div class="nn">5</div>
        <div>
          <div style="font-weight:700;font-size:var(--fs-md)">El reto del módulo</div>
          <div class="muted t-sm" style="margin-top:3px">
            {lesson.reto ? lesson.reto.scenario.slice(0, 190) : 'Un caso nuevo que las lecciones no cubrieron.'}
          </div>
        </div>
      </div>
    </div>

    <div class="card card-paper" style="margin-top:var(--s3)">
      <div class="ai-tag"><span class="dot"></span> Al final</div>
      <h3 style="margin-top:8px">{lesson.doc_type || 'Un documento profesional tuyo'}</h3>
      <p class="t-sm" style="margin-top:6px;opacity:.85">
        Tu trabajo evaluado se compila en el documento que un cliente habría
        pagado por recibir, con tu firma. No damos certificados: damos el trabajo.
      </p>
    </div>

    {@render doors('lit')}
    <p class="faint t-sm center" style="margin:10px 0 0">
      Pega una oferta real o solo el puesto y te armamos la ruta completa —
      también sin cuenta.
    </p>
  {/if}
</div>
