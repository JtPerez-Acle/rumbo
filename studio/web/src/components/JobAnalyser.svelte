<script>
  /* Paste a posting, get a route.
   *
   * docs/08 calls this the acquisition asset: it is the one claim a competitor
   * cannot truthfully copy, because it ends by naming what the job needs and we
   * do NOT teach.
   *
   * The analysis genuinely takes about two minutes — the model reads the whole
   * posting and crosses it against every module contract. We say so before they
   * start, show what is actually happening at each step, and run a real elapsed
   * clock. No fake percentage: the house rule is that we do not lie to people.
   *
   * This island covers all three states (form, working, result) because they are
   * one flow over one piece of state. Splitting them would mean lifting the
   * analysis into a store and coordinating three components around a value that
   * only ever has one owner.
   */
  import { PATHS } from '../lib/icons.js';
  import { JOB_STAGES, JOB_SLOW_AT, modLabel } from '../lib/route.js';

  let phase = $state('form'); // form | working | result | failed
  let mode = $state('oferta'); // oferta | puesto
  let posting = $state('');
  let goal = $state('');
  let company = $state(''); // honeypot
  let msg = $state('');

  let elapsed = $state(0);
  let analysis = $state(null);
  let token = $state('');
  let progress = $state(null);
  let failure = $state('');
  let shareLabel = $state('Copiar enlace');
  let coverageWidth = $state(0);

  const isGoal = $derived(mode === 'puesto');

  /* The first stage is worded for the door they came in by. Everything after it
     is the same work either way. */
  const stages = $derived(
    JOB_STAGES.map((s, i) =>
      i === 0 && isGoal
        ? [s[0], 'Entendiendo qué exige ese rol hoy',
           'Lo que se le pide típicamente a alguien en ese puesto en LatAm.']
        : s,
    ),
  );

  const activeStage = $derived.by(() => {
    let active = 0;
    JOB_STAGES.forEach(([at], i) => { if (elapsed >= at) active = i; });
    return active;
  });

  const clock = $derived(
    Math.floor(elapsed / 60) + ':' + String(elapsed % 60).padStart(2, '0'),
  );

  async function start() {
    if (isGoal) {
      if (goal.trim().length < 5) {
        msg = 'Dinos el puesto o la habilidad en una frase.';
        return;
      }
    } else if (posting.trim().length < 200) {
      msg = 'Pega la oferta completa: necesitamos los requisitos para armarte una ruta real.';
      return;
    }
    msg = '';
    phase = 'working';
    elapsed = 0;
    const t0 = Date.now();
    const tick = setInterval(() => { elapsed = Math.floor((Date.now() - t0) / 1000); }, 1000);

    const body = isGoal ? { goal: goal.trim() } : { posting: posting.trim() };
    let res, data;
    try {
      res = await fetch('/api/learn/public/job-analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...body, company }),
      });
      data = await res.json();
    } catch {
      data = { __net: true };
    }
    clearInterval(tick);

    if (!res || !res.ok || data.__net) {
      failure = data && data.__net
        ? 'Se cortó la conexión.'
        : res && res.status === 429
          ? 'Ya analizamos varias ofertas desde aquí. Espera un rato.'
          : res && res.status === 503
            ? 'Estamos analizando varias ofertas ahora mismo. Intenta en un par de minutos.'
            : (data && data.detail) || 'No pudimos analizar esa oferta.';
      phase = 'failed';
      return;
    }

    /* A route analysed before signing up is the reason many people sign up at
       all. It lives in localStorage until there is a session to attach it to;
       without this the most motivating artifact we can produce evaporates at
       the door. */
    try { localStorage.setItem('aprende_job_token', data.token); } catch { /* private mode */ }
    analysis = data.analysis;
    token = data.token;
    progress = data.progress;
    phase = 'result';
    // The coverage bar fills from zero, so it has to start there and be moved
    // once the element exists.
    coverageWidth = 0;
    setTimeout(() => { coverageWidth = analysis.coverage; }, 60);
  }

  const shareUrl = $derived(token ? location.origin + '/aprende/ruta/' + token : '');

  async function share() {
    try {
      if (navigator.share) {
        await navigator.share({ title: 'Mi ruta de estudio', url: shareUrl });
        return;
      }
      await navigator.clipboard.writeText(shareUrl);
      shareLabel = 'Enlace copiado';
    } catch {
      shareLabel = shareUrl;
    }
  }

  function wantRoute() {
    // The role IS the answer to "what do you want to achieve", so carry it to
    // the waitlist rather than asking again.
    try { sessionStorage.setItem('aprende_job_role', analysis.role_title || ''); } catch { /* private mode */ }
    location.href = '/lista';
  }

  function retry() {
    phase = 'form';
    failure = '';
  }

  const nucleo = $derived(analysis ? analysis.ruta.filter((r) => r.phase === 'nucleo') : []);
  const later = $derived(analysis ? analysis.ruta.filter((r) => r.phase !== 'nucleo') : []);
</script>

{#snippet icon(name, cls = 'ic ic-s')}
  <svg class={cls} viewBox="0 0 24 24" aria-hidden="true"><path d={PATHS[name]} /></svg>
{/snippet}

{#snippet courseCard(r)}
  <div class="jcourse">
    <div class="jtitle">{r.course_title}</div>
    <div class="jdepth">{modLabel(r)} · {r.lessons} lecciones</div>
    {#if r.why}<div class="jwhy">{r.why}</div>{/if}
  </div>
{/snippet}

{#if phase === 'form' || phase === 'failed'}
  {#if phase === 'failed'}
    <div class="note note-warn" style="margin-top:14px">
      {@render icon('alert')}<span>{failure}</span>
    </div>
  {/if}

  <div style="margin-top:14px;display:flex;flex-direction:column;gap:15px">
    <div>
      <div class="eyebrow">Tu próximo trabajo</div>
      <h1 style="margin-top:10px">Dinos qué quieres.</h1>
      <!-- These three paragraphs used to exist only in the server-rendered
           version of this page, and hydration replaced them with the bare form.
           So a crawler read the argument and a person got a 560px textarea —
           two documents again. The island SSRs, so keeping them here means both
           see the same page. -->
      <p class="muted" style="margin-top:8px">
        Pega la oferta de trabajo que te interesa, o escribe sólo el nombre del
        puesto. En unos dos minutos sabes qué pide de verdad, qué parte de eso
        cubrimos, qué no, y tu ruta: qué cursos y qué módulos, en qué orden.
      </p>
      <p class="muted" style="margin-top:8px">
        Si el puesto pide algo que no enseñamos, te lo decimos y te lo listamos.
        Preferimos eso a venderte un curso que no lo cubre.
      </p>
      <p class="muted" style="margin-top:8px">
        No necesitas cuenta para probarlo.
      </p>
    </div>

    <!-- Two front doors, one matcher (docs/09 item 4): a real posting, or just
        the role the person wants. Same honesty either way. -->
    <div class="seg" role="tablist" aria-label="Cómo quieres empezar">
      <button
        type="button" role="tab" id="tab-oferta" aria-controls="panel-oferta"
        class={mode === 'oferta' ? 'on' : ''}
        aria-selected={mode === 'oferta'}
        onclick={() => (mode = 'oferta')}>Tengo una oferta</button>
      <button
        type="button" role="tab" id="tab-puesto" aria-controls="panel-puesto"
        class={mode === 'puesto' ? 'on' : ''}
        aria-selected={mode === 'puesto'}
        onclick={() => (mode = 'puesto')}>Solo sé el puesto</button>
    </div>

    {#if mode === 'oferta'}
      <div id="panel-oferta" role="tabpanel" aria-labelledby="tab-oferta">
        <label for="jtext">La oferta de trabajo</label>
        <textarea
          id="jtext" rows="10" maxlength="12000" bind:value={posting}
          placeholder="Pega aquí las funciones y los requisitos de la oferta…"
        ></textarea>
        <p class="faint t-sm" style="margin-top:6px">
          Mientras más completa la pegues, mejor la ruta. Solo funciones y
          requisitos basta.
        </p>
      </div>
    {:else}
      <div id="panel-puesto" role="tabpanel" aria-labelledby="tab-puesto">
        <label for="jgoal">El puesto o la habilidad que quieres</label>
        <input
          id="jgoal" maxlength="140" bind:value={goal}
          placeholder="Ej: community manager / especialista en Google Ads" />
        <p class="faint t-sm" style="margin-top:6px">
          Armamos la ruta con lo que ese rol exige típicamente hoy. Con una
          oferta real la ruta sale más precisa.
        </p>
      </div>
    {/if}

    <input
      bind:value={company} tabindex="-1" autocomplete="off" aria-hidden="true"
      style="position:absolute;left:-9999px;opacity:0;height:0;width:0" />

    <div class="note note-warn">
      {@render icon('clock')}
      <span>El análisis tarda <b>cerca de dos minutos</b>. Tu tutora lo cruza con
      las lecciones del catálogo, módulo por módulo. No cierres esta pestaña.</span>
    </div>

    <button class="btn btn-primary" type="button" onclick={start}>
      Armar mi ruta {@render icon('arrow')}
    </button>
    <div class="center muted t-sm" role="status" aria-live="polite">{msg}</div>
  </div>

{:else if phase === 'working'}
  <div style="margin-top:10px">
    <div class="eyebrow">{isGoal ? 'Analizando tu objetivo' : 'Analizando tu oferta'}</div>
    <h2 style="margin-top:10px">Tu tutora está trabajando.</h2>
    <p class="muted t-sm" style="margin-top:8px">
      Esto tarda cerca de dos minutos. No es una barra de adorno: abajo ves en qué va.
    </p>
  </div>

  <div class="card" style="margin-top:14px">
    {#each stages as [, title, sub], i}
      <div class="jstage" class:done={i < activeStage} class:now={i === activeStage}>
        <div class="jdot">{@render icon('check')}</div>
        <div class="jtxt">
          <div>{title}</div>
          <div class="jsub">
            <p class="faint t-sm" style="margin:0 0 8px">{sub}</p>
            <div class="readline"><i></i></div>
          </div>
        </div>
      </div>
    {/each}
  </div>

  <div class="row" style="justify-content:space-between;margin-top:10px">
    <span class="faint t-sm">No cierres esta pestaña</span>
    <span class="jclock">{clock}</span>
  </div>

  {#if elapsed >= JOB_SLOW_AT}
    <div class="note note-warn">
      {@render icon('alert')}
      <span>Está tardando más de lo normal. Sigue trabajando — a veces la oferta
      es larga y hay más que cruzar.</span>
    </div>
  {/if}

{:else if phase === 'result'}
  <button class="back" type="button" onclick={retry}>‹ Analizar otra oferta</button>

  <div style="margin-top:6px">
    <div class="eyebrow">Tu ruta</div>
    <h1 style="margin-top:10px">{analysis.role_title || 'Esta oferta'}</h1>
    {#if analysis.company}
      <p class="muted t-sm" style="margin-top:6px">{analysis.company}</p>
    {/if}
  </div>

  <!-- Coverage, stated plainly in both directions. -->
  <div class="card" style="margin-top:14px">
    <div class="row" style="justify-content:space-between">
      <b class="t-md">Cubrimos {analysis.coverage}% de lo que pide</b>
      <span class="faint t-sm">{analysis.competencies.length} competencias</span>
    </div>
    <div class="covbar"><i style={`width:${coverageWidth}%`}></i></div>
    <p class="muted t-sm" style="margin-top:10px">
      {#if analysis.ruta.length}
        Tu ruta son <b>{analysis.total_lessons} lecciones</b>. Empiezas por
        {analysis.core_lessons} — con eso ya tienes algo que mostrar.
      {:else}
        Para este puesto no tenemos con qué prepararte todavía. Preferimos decírtelo.
      {/if}
    </p>
  </div>

  {#if nucleo.length}
    <div class="phasehead">Empieza por aquí · {analysis.core_lessons} lecciones</div>
    {#each nucleo as r}{@render courseCard(r)}{/each}
  {/if}
  {#if later.length}
    <div class="phasehead later">Después, para completar el perfil</div>
    {#each later as r}{@render courseCard(r)}{/each}
  {/if}

  {#if analysis.gaps.length}
    <div class="microlabel" style="margin-top:16px">Esto lo pide el puesto y no lo cubrimos</div>
    <div class="card">
      {#each analysis.gaps as g}
        <div class="gaprow"><span class="gx">{@render icon('alert')}</span><span>{g.name}</span></div>
      {/each}
      <p class="faint t-sm" style="margin:10px 0 0">
        Preferimos decírtelo a venderte un curso que no lo enseña.
      </p>
    </div>
  {/if}

  {#if analysis.doc_type}
    <div class="microlabel" style="margin-top:16px">Lo que vas a llevar a la entrevista</div>
    <div class="card card-paper">
      <div class="row" style="gap:8px">{@render icon('doc')}<b class="t-md">{analysis.doc_type}</b></div>
      {#if analysis.doc_title}
        <p class="t-sm" style="margin-top:8px;font-family:var(--serif)">«{analysis.doc_title}»</p>
      {/if}
      {#if analysis.pitch}
        <p class="t-sm" style="margin-top:10px;opacity:.8">{analysis.pitch}</p>
      {/if}
    </div>
  {/if}

  {#if token}
    <!-- Shareable at first contact — the portfolio document needs 3+ submissions
        to exist, this exists two minutes in, and the gap list is the part worth
        sharing. -->
    <div class="card" style="margin-top:16px">
      <div class="row" style="gap:8px">{@render icon('send')}<b class="t-md">Comparte esta ruta</b></div>
      <p class="muted t-sm" style="margin-top:8px">
        Un enlace público con lo que pide el puesto, lo que cubrimos y lo que no.
        Útil si estás buscando trabajo y quieres mostrar tu plan.
      </p>
      <button class="btn btn-ghost" type="button" style="margin-top:10px" onclick={share}>{shareLabel}</button>
    </div>
  {/if}

  <div style="display:flex;flex-direction:column;gap:8px;margin-top:18px">
    <button class="btn btn-primary" type="button" onclick={wantRoute}>
      {analysis.ruta.length ? 'Quiero esta ruta' : 'Avísame cuando lo cubran'}
      {@render icon('arrow')}
    </button>
    <a class="btn btn-ghost" href="/login">Tengo una invitación</a>
  </div>
{/if}
