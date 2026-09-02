<script>
  /* Mi objetivo: the route, as the learner's spine (docs/09).
   *
   * THE STEP LIST IS THE POINT. It used to render one card per COURSE with a
   * module range — a bill of materials. docs/09 settled that the module is the
   * unit and the matcher has reasoned in modules ever since; only the screen
   * still sold courses. It is an ordered path now, each step labelled by what
   * you will be able to DO, with the course demoted to provenance.
   */
  import Icon from '../Icon.svelte';
  import ReadingCard from '../eval/ReadingCard.svelte';
  import { api, toLogin } from '../../../lib/api.js';
  import { nav } from '../../../lib/router.svelte.js';

  let goal = $state(null);
  let cv = $state(null);
  let goalDoc = $state(null);
  let others = $state([]);
  let compiling = $state(false);
  let msg = $state('');
  let reload = $state(0);

  async function load() {
    const jt = await api('/job-target');
    if (jt.__unauth) return toLogin();
    goal = jt;
    if (!jt.exists) return;
    const [cvs, gd, hist] = await Promise.all([
      api('/cv'), api('/goal-doc'), api('/job-targets'),
    ]);
    cv = cvs;
    goalDoc = gd;
    others = ((hist && hist.targets) || []).filter((t) => !t.active);
  }

  $effect(() => { reload; load(); });

  const steps = $derived(goal?.steps || []);
  const firstPending = $derived(steps.findIndex((s) => s.done < s.lessons && !s.exempt));

  const PHASES = [['nucleo', 'Empieza por aquí'], ['despues', 'Después, para completar el perfil']];

  async function compileDoc() {
    compiling = true;
    msg = '';
    const res = await api('/goal-doc', { method: 'POST' });
    compiling = false;
    if (res && res.share_url) {
      window.open(res.share_url, '_blank');
      reload += 1;
    } else {
      msg = (res && res.detail) || 'No pudimos compilarlo, intenta de nuevo.';
    }
  }

  async function resume(token) {
    const r = await api('/job-target/claim', { method: 'POST', body: JSON.stringify({ token }) });
    if (r && r.ok) reload += 1;
  }
</script>

<button class="back" onclick={() => nav('#/hoy')}>‹ Hoy</button>

{#if goal && !goal.exists}
  <div style="margin-top:14px">
    <div class="eyebrow">Tu objetivo</div>
    <h1 style="margin-top:10px">Aún no tienes un objetivo activo.</h1>
    <p class="muted" style="margin-top:8px">
      Pega la oferta del trabajo que quieres y armamos tu ruta de estudio y el
      documento para la entrevista.
    </p>
  </div>
  <button class="btn btn-primary" style="margin-top:14px" onclick={() => nav('#/oferta')}>
    Pega tu oferta <Icon name="arrow" class="ic ic-s" />
  </button>

{:else if goal}
  <div style="margin-top:6px">
    <div class="eyebrow">Tu objetivo</div>
    <h1 style="margin-top:10px">{goal.role_title || 'Tu próximo trabajo'}</h1>
    {#if goal.company}<p class="muted t-sm" style="margin-top:6px">{goal.company}</p>{/if}
    {#if goal.exempt_lessons}
      <p class="muted t-sm" style="margin-top:8px">
        Te saltaste <b>{goal.exempt_modules} módulo{goal.exempt_modules > 1 ? 's' : ''}</b>
        que ya sabías: te quedan <b>{goal.remaining} lecciones</b> en vez de
        {goal.total - goal.done}.
      </p>
    {/if}
  </div>

  {#if goal.next_lesson}
    <div class="card-hero" style="margin-top:12px">
      <div class="eyebrow">Siguiente paso de tu ruta</div>
      <p class="muted t-sm" style="margin:8px 0 4px">{goal.next_lesson.course_title}</p>
      <h3 style="margin-bottom:12px">{goal.next_lesson.title}</h3>
      <button class="btn btn-primary" onclick={() => nav('#/leccion/' + goal.next_lesson.node_id)}>
        <Icon name="play" class="ic ic-s" /> Continuar mi ruta
      </button>
    </div>
  {/if}

  {#each PHASES as [phase, label]}
    {@const rows = steps.filter((s) => s.phase === phase)}
    {#if rows.length}
      <div class="microlabel" style="margin-top:16px">{label}</div>
      {#each rows as st}
        {@const idx = steps.indexOf(st)}
        {@const complete = st.done >= st.lessons}
        {@const current = idx === firstPending}
        {@const pct = st.lessons ? Math.round((100 * st.done) / st.lessons) : 0}
        <!-- docs/10: a skipped module stays IN the route — the job still needs
             it — and its lessons stay open. It just is not where we start. -->
        <svelte:element
          this={st.next_lesson_id || complete ? 'button' : 'div'}
          class={`card ${st.next_lesson_id ? 'clickable' : ''}`}
          style={`${current ? 'border-color:var(--amber);' : ''}${st.exempt ? 'opacity:.72' : ''}`}
          onclick={st.next_lesson_id
            ? () => nav('#/leccion/' + st.next_lesson_id)
            : complete ? () => nav('#/curso/' + st.course_slug) : undefined}
        >
          <div class="row" style="justify-content:space-between;align-items:flex-start;gap:10px">
            <div class="row" style="gap:8px;align-items:center">
              <span style={`color:${complete || st.exempt ? 'var(--amber)' : 'var(--faint)'}`}>
                <Icon name={complete || st.exempt ? 'check' : current ? 'play' : 'lock'} class="ic ic-s" />
              </span>
              <span class="microlabel">Paso {idx + 1} de {steps.length}</span>
            </div>
            {#if st.exempt === 'acreditado'}
              <span class="pill go">Acreditado {st.exempt_score || ''}</span>
            {:else if st.exempt}
              <span class="pill soon">Ya lo sabes</span>
            {:else}
              <span class="muted t-sm">{st.done}/{st.lessons}</span>
            {/if}
          </div>
          <p class="t-base" style="font-weight:600;margin:8px 0 4px">
            {st.outcome || st.module_title || ''}
          </p>
          <p class="faint" style="font-size:var(--fs-xs);margin:0 0 8px">
            {st.course_title} · módulo {st.module_no}
          </p>
          <div class="prog"><i style={`clip-path:inset(0 ${100 - (pct)}% 0 0)`}></i></div>
        </svelte:element>
      {/each}
    {/if}
  {/each}

  <!-- docs/10. Offered AFTER the route, on purpose: the objection this answers
       ("son muchísimas lecciones, la mitad ya la sé") only exists once they
       have seen the length. Before the route it is a form; after it, a fix. -->
  {#if cv}
    <div class="microlabel" style="margin-top:18px">Lo que ya sabes</div>
    <button class="card clickable" onclick={() => nav('#/cv')}>
      <div class="row" style="gap:8px">
        <Icon name="doc" class="ic ic-s" />
        <b class="t-md">{cv.exists ? 'Tu CV, leído' : '¿Ya sabes parte de esto?'}</b>
      </div>
      <p class="t-sm muted" style="margin-top:8px">
        {#if cv.exists}
          Encontramos {cv.proposed_modules} módulo{cv.proposed_modules === 1 ? '' : 's'}
          que tu CV muestra que ya hiciste.{goal.exempt_modules ? '' : ' Todavía no te saltaste ninguno.'}
        {:else}
          Pega tu CV y te decimos qué módulos de esta ruta ya hiciste en tu
          trabajo. Tú decides cuáles saltarte — y puedes acreditarlos con su reto.
        {/if}
      </p>
    </button>
  {/if}

  {#if goal.gaps?.length}
    <div class="microlabel" style="margin-top:16px">Esto lo pide el puesto y no lo cubrimos</div>
    <div class="card">
      {#each goal.gaps as x}
        <div class="gaprow"><span class="gx"><Icon name="alert" class="ic ic-s" /></span><span>{x.name}</span></div>
      {/each}
    </div>
  {/if}

  <!-- The goal document: the learner's best work across the WHOLE route, aimed
       at this posting. Eligible from the first submission — it grows. -->
  {#if goalDoc}
    <div class="microlabel" style="margin-top:16px">Tu documento para la entrevista</div>
    <div class="card card-paper">
      <div class="row" style="gap:8px">
        <Icon name="doc" class="ic ic-s" />
        <b class="t-md">{goal.doc_type || 'Documento profesional'}</b>
      </div>
      <p class="t-sm" style="margin-top:8px;opacity:.85">
        {#if goalDoc.exists}
          Compilado con tu trabajo real. Se actualiza cada vez que lo regeneres.
        {:else if goalDoc.eligible}
          Ya tienes trabajo suficiente: compila tu primera versión.
        {:else}
          Se arma con tu trabajo real: llevas
          <b>{goalDoc.submissions || 0} de {goalDoc.needed || 3}</b> entregas de
          los cursos de tu ruta. Con menos tendría que inventar, y este documento
          lo vas a mostrar. No es un CV — es el trabajo que hiciste, con tus
          decisiones y tus números.
        {/if}
      </p>
      <div style="display:flex;flex-direction:column;gap:8px;margin-top:12px">
        {#if goalDoc.eligible}
          <button class="btn btn-paper" disabled={compiling} onclick={compileDoc}>
            {goalDoc.exists ? 'Actualizar mi documento' : 'Compilar mi documento'}
          </button>
        {/if}
        {#if goalDoc.exists}
          <button class="btn btn-ghost" onclick={() => window.open(goalDoc.share_url, '_blank')}>
            Ver y compartir
          </button>
        {/if}
      </div>
      {#if compiling}
        <ReadingCard message="Tu tutora está compilando tu documento…" />
      {/if}
      <div class="center muted t-sm" style="margin-top:8px" role="status" aria-live="polite">{msg}</div>
    </div>
  {/if}

  <!-- Changing goal is normal, not an edge case: people find new offers. It is
       also non-destructive — completed lessons carry over and the old goal keeps
       its document — so the entry point can be plainly visible. -->
  <div class="microlabel" style="margin-top:18px">¿Encontraste otra oferta?</div>
  <button class="btn btn-ghost" onclick={() => nav('#/oferta')}>
    Analizar otra oferta <Icon name="arrow" class="ic ic-s" />
  </button>
  <p class="faint t-sm" style="margin:8px 2px 0">
    Tu avance no se pierde: las lecciones que ya hiciste cuentan para cualquier
    ruta que las incluya, y este objetivo queda guardado con su documento.
  </p>

  {#if others.length}
    <div class="microlabel" style="margin-top:16px">Tus otros objetivos</div>
    {#each others as t}
      <button class="lrow clickable" onclick={() => resume(t.token)}>
        <div class="num"><Icon name="target" class="ic ic-s" /></div>
        <div class="lt">{t.role_title || 'Objetivo'}
          <div style="font-size:var(--fs-xs);color:var(--faint);font-weight:600;margin-top:2px">
            {t.done}/{t.total} lecciones · {t.coverage}% cubierto{t.has_doc ? ' · tiene documento' : ''}
          </div>
        </div>
        <div class="st">Retomar</div>
      </button>
    {/each}
  {/if}
{/if}
