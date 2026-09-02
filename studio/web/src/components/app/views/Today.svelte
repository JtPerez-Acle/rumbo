<script>
  /* Hoy: the zero-decision daily entry point.
   *
   * The whole screen answers one question — what do I do now — and it answers
   * it from the GOAL rather than from a course. A learner with no goal used to
   * land on "elige tu primer curso", which is the opposite of what the landing
   * promised them, and choosing blind from fourteen courses is exactly what the
   * route exists to prevent. The one real learner who saw that screen did
   * lesson 1 of two unrelated courses and stopped.
   */
  import Icon from '../Icon.svelte';
  import Flame from '../Flame.svelte';
  import { api, toLogin } from '../../../lib/api.js';
  import { nav } from '../../../lib/router.svelte.js';
  import { session } from '../../../lib/session.svelte.js';

  let today = $state(null);
  let goal = $state(null);

  $effect(() => {
    (async () => {
      const [d, jt] = await Promise.all([api('/today'), api('/job-target')]);
      if (d.__unauth) return toLogin();
      today = d;
      goal = jt;
    })();
  });

  // The continue-card measures the ROUTE, not the course.
  const onRoute = $derived(goal && goal.exists && goal.total > 0);
  const goalPct = $derived(onRoute ? Math.round((100 * goal.done) / goal.total) : 0);
  const step = $derived(onRoute ? Math.min(goal.done + 1, goal.total) : null);
</script>

{#if today}
  <div class="topbar">
    <div class="brandrow">
      <div class="brandmark"></div>
      <div class="brandname">Rumbo<small>Hola, {today.name}</small></div>
    </div>
    <Flame days={today.streak} />
  </div>

  {#if onRoute}
    <!-- The goal is the spine of the experience (docs/09): with an active job
         target the day starts from it, not from a loose course. -->
    <div class="card card-spot" style="margin-top:6px">
      <div class="eyebrow">Tu objetivo</div>
      <h2 style="margin-top:6px">{goal.role_title || 'Tu próximo trabajo'}</h2>
      <div class="row" style="justify-content:space-between;margin:10px 0 6px">
        <span class="muted t-sm">{goal.done} de {goal.total} lecciones de tu ruta</span>
        <span class="muted t-sm">{goalPct}%</span>
      </div>
      <div class="prog"><i style={`clip-path:inset(0 ${100 - (goalPct)}% 0 0)`}></i></div>
      <button class="btn btn-ghost" style="margin-top:12px" onclick={() => nav('#/objetivo')}>
        Ver mi ruta y mi documento <Icon name="arrow" class="ic ic-s" />
      </button>
    </div>
  {:else if session.me && !session.me.project_name}
    <!-- Aplicación is 40 of the 100 points and is judged against this. Every
         learner so far has skipped it, because the old nudge sounded like a
         nicety. Say what it actually costs. -->
    <button class="lrow clickable" style="margin-top:6px" onclick={() => nav('#/perfil')}>
      <div class="num"><Icon name="target" class="ic ic-s" /></div>
      <div class="lt">Elige tu proyecto real
        <div style="font-size:var(--fs-xs);color:var(--faint);font-weight:600;margin-top:2px">
          Sin él tu tutora evalúa a ciegas: 40 de los 100 puntos miden qué tan
          anclado está tu trabajo en un proyecto tuyo
        </div>
      </div>
      <div class="st">Definir</div>
    </button>
  {/if}

  {#if today.continue && !today.continue.finished}
    <!-- With a goal set the headline is the GOAL and the measure is the route.
         "Lección 4 de 30 de Marketing con IA" frames the work as consuming a
         course, which is the shop-shaped reading the route exists to replace.
         "Lección", not "paso": #/objetivo counts MODULE steps, and one word
         with two denominators reads as a bug. -->
    <div class="card-hero" style="margin-top:6px">
      <div class="eyebrow">
        {onRoute ? 'Tu ruta hacia ' + (goal.role_title || 'tu objetivo') : 'Continúa donde quedaste'}
      </div>
      <h2 style="margin-top:8px">{today.continue.lesson_title}</h2>
      <p class="muted t-sm" style="margin:6px 0 14px">
        {onRoute
          ? `Lección ${step} de ${goal.total} de tu ruta · ${today.continue.course_title}`
          : `Lección ${today.continue.position} de ${today.continue.total} · ${today.continue.course_title}`}
      </p>
      {#if onRoute}
        <div class="prog" style="margin-bottom:12px"><i style={`clip-path:inset(0 ${100 - (goalPct)}% 0 0)`}></i></div>
      {/if}
      <button class="btn btn-primary" onclick={() => nav('#/leccion/' + today.continue.lesson_id)}>
        <Icon name="play" class="ic ic-s" />
        {today.done_today > 0 ? 'Sigue con tu clase' : 'Empieza tu clase de hoy'}
      </button>
    </div>
  {:else if today.continue && today.continue.finished}
    <div class="card-hero" style="margin-top:6px">
      <div class="eyebrow">Curso completado</div>
      <h2 style="margin-top:8px">{today.continue.course_title}</h2>
      <p class="muted t-sm" style="margin:6px 0 14px">
        Compila tu documento final y elige tu próximo curso.
      </p>
      <button class="btn btn-primary" onclick={() => nav('#/cursos')}>
        Elegir mi próximo curso <Icon name="arrow" class="ic ic-s" />
      </button>
    </div>
  {:else}
    <div class="card-hero" style="margin-top:6px">
      <div class="eyebrow">Empieza por aquí</div>
      <h2 style="margin-top:8px">Dinos qué quieres ser</h2>
      <p class="muted t-sm" style="margin:6px 0 14px">
        Pega una oferta de trabajo real, o solo el puesto que quieres. Te armamos
        la ruta: qué cursos, qué módulos y en qué orden — y qué no cubrimos.
      </p>
      <button class="btn btn-primary" onclick={() => nav('#/oferta')}>
        <Icon name="target" class="ic ic-s" /> Armar mi ruta
      </button>
    </div>
    <!-- Browsing stays as the secondary door, for people who already know. -->
    <button class="lrow clickable" style="margin-top:6px" onclick={() => nav('#/cursos')}>
      <div class="num"><Icon name="book" class="ic ic-s" /></div>
      <div class="lt">Ya sé qué quiero estudiar
        <div style="font-size:var(--fs-xs);color:var(--faint);font-weight:600;margin-top:2px">
          Ver los cursos y sus temarios
        </div>
      </div>
      <div class="st">Cursos</div>
    </button>
  {/if}

  {#if today.reviews?.length}
    <div class="microlabel" style="margin-top:10px">Repasos de hoy · fijan lo aprendido</div>
    {#each today.reviews as r}
      <button class="lrow clickable" onclick={() => nav('#/leccion/' + r.lesson_id)}>
        <div class="num"><Icon name="redo" class="ic ic-s" /></div>
        <div class="lt">{r.lesson_title}
          <div style="font-size:var(--fs-xs);color:var(--faint);font-weight:600;margin-top:2px">
            {r.course_title}
          </div>
        </div>
        <div class="st">Repasar</div>
      </button>
    {/each}
  {/if}

  {#if today.defenses?.length}
    <div class="microlabel" style="margin-top:10px">
      Tu tutora te hizo una pregunta · suma hasta 10 pts
    </div>
    {#each today.defenses as f}
      <!-- The step deep-link is load-bearing: a pending conversation shown here
           must land exactly on the step where it can be answered. Without it,
           completed lessons skipped the explain step and the conversation was
           unreachable. -->
      <button class="lrow clickable caprow"
              onclick={() => nav(f.kind === 'capstone'
                ? '#/reto/' + f.capstone_id
                : '#/leccion/' + f.lesson_id + '/' + f.step)}>
        <div class="num"><Icon name="mic" class="ic ic-s" /></div>
        <div class="lt">{f.lesson_title}</div>
        <div class="st">Responder</div>
      </button>
    {/each}
  {/if}

  {#if today.done_today > 0}
    <p class="faint t-sm center" style="margin-top:14px">
      Hoy: {today.done_today}
      {today.done_today === 1 ? 'lección completada' : 'lecciones completadas'} ✓
    </p>
  {/if}
{/if}
