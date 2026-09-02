<script>
  /* Perfil: who they are, what they have done, and the one thing every exercise
     is written against.
   */
  import Icon from '../Icon.svelte';
  import Flame from '../Flame.svelte';
  import { api, toLogin } from '../../../lib/api.js';
  import { session } from '../../../lib/session.svelte.js';
  import { nav } from '../../../lib/router.svelte.js';

  let data = $state(null);
  let saving = $state(false);
  let msg = $state('');
  let project = $state({ project_name: '', project_desc: '', goal: '' });

  $effect(() => {
    (async () => {
      const d = await api('/profile');
      if (d.__unauth) return toLogin();
      data = d;
      project = {
        project_name: d.project_name || '',
        project_desc: d.project_desc || '',
        goal: d.goal || '',
      };
    })();
  });

  async function save() {
    saving = true;
    msg = '';
    const r = await api('/profile', { method: 'POST', body: JSON.stringify(project) });
    saving = false;
    msg = r && r.ok ? 'Guardado ✓' : 'No se pudo guardar, intenta de nuevo.';
    // The exercise step reads the project off the session, so a save here has
    // to reach it without a reload.
    if (r && r.ok) Object.assign(session.me, project);
  }

  async function logout() {
    await api('/logout', { method: 'POST' });
    location.href = '/aprende';
  }
</script>

{#if data}
  <div class="topbar">
    <div class="brandrow">
      <div class="brandmark"></div>
      <div class="brandname">Perfil</div>
    </div>
    <Flame days={data.streak} />
  </div>

  <div class="card" style="text-align:center;padding:24px">
    <div class="avatar">{(data.name || '?')[0].toUpperCase()}</div>
    <h2 style="font-size:var(--fs-xl)">{data.name}</h2>
    <p class="muted t-sm">{data.email}</p>
  </div>

  <div class="row" style="gap:12px">
    <div class="card" style="flex:1;text-align:center">
      <div class="bigstreak" style="font-size:var(--fd-lg);margin:0">{data.streak}</div>
      <div class="microlabel">días seguidos</div>
    </div>
    <div class="card" style="flex:1;text-align:center">
      <div class="bigstreak" style="font-size:var(--fd-lg);margin:0">{data.lessons_done}</div>
      <div class="microlabel">lecciones hechas</div>
    </div>
  </div>

  <!-- The transversal project: learner-level, editable here (docs/09). It is
       what lets work compile across courses into one document, and what the
       evaluator judges Aplicación against. -->
  <div class="card" style="margin-top:6px">
    <div class="row" style="gap:10px;color:var(--amber)">
      <Icon name="target" /><b class="t-md" style="color:var(--text)">Tu proyecto</b>
    </div>
    <p class="muted t-sm" style="margin:8px 0 12px">
      El proyecto real sobre el que trabajan todos tus ejercicios. Tu tutora
      evalúa contra este contexto.
    </p>
    <form style="display:flex;flex-direction:column;gap:10px"
          onsubmit={(e) => { e.preventDefault(); save(); }}>
      <div>
        <label for="ppn">Proyecto o marca</label>
        <input id="ppn" maxlength="120" bind:value={project.project_name}
               placeholder="Tu negocio, o una marca donde quieres trabajar" />
      </div>
      <div>
        <label for="ppd">De qué se trata</label>
        <input id="ppd" maxlength="500" bind:value={project.project_desc}
               placeholder="Una línea de contexto" />
      </div>
      <div>
        <label for="ppg">Tu meta</label>
        <input id="ppg" maxlength="200" bind:value={project.goal}
               placeholder="Conseguir trabajo, vender más…" />
      </div>
      <button class="btn btn-ghost" type="submit" disabled={saving}>Guardar</button>
      <div class="center muted t-sm" role="status" aria-live="polite">{msg}</div>
    </form>
  </div>

  {#if data.courses.length}
    <div class="microlabel" style="margin-top:6px">Tu progreso</div>
    {#each data.courses as c}
      <div class="card">
        <div class="row" style="justify-content:space-between;margin-bottom:8px">
          <span style="font-weight:700;font-size:var(--fs-base)">{c.title}</span>
          <span class="muted t-sm">{c.done}/{c.total}</span>
        </div>
        <div class="prog"><i style={`clip-path:inset(0 ${100 - (c.total ? c.done / c.total : 0) * 100}% 0 0)`}></i></div>
      </div>
    {/each}
  {/if}

  <!-- A real link to the real page, in a new tab. It used to re-render a copy
       of the landing inside the app; there is one landing now and it has an
       address. `?publica=1` stops the server bouncing a signed-in visitor
       straight back in here. -->
  <a class="btn btn-ghost" style="margin-top:8px" href="/?publica=1"
     target="_blank" rel="noopener">Ver la portada pública</a>
  <button class="btn btn-ghost" style="margin-top:8px"
          onclick={() => nav('#/como-funciona')}>¿Cómo funciona Rumbo?</button>
  <button class="btn btn-ghost" style="margin-top:2px" onclick={logout}>Salir</button>
{/if}
