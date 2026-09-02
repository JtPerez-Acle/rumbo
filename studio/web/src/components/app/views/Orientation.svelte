<script>
  /* Thirty seconds on how this works, and the one decision that shapes every
   * later evaluation.
   *
   * THE PROJECT FORM COMES FIRST. On a phone the four how-it-works cards ran
   * ~1700px and buried the form and its buttons below them: every learner so
   * far scrolled past it and took "lo defino después". The decision leads now
   * and the explainer sits underneath it.
   */
  import Icon from '../Icon.svelte';
  import HowItWorks from './HowItWorks.svelte';
  import { api } from '../../../lib/api.js';
  import { nav } from '../../../lib/router.svelte.js';
  import { session, markOnboarded } from '../../../lib/session.svelte.js';

  let { revisit = false } = $props();

  let project = $state({ project_name: '', project_desc: '', goal: '' });
  let saving = $state(false);

  async function done(save) {
    if (save) {
      const filled = project.project_name || project.project_desc || project.goal;
      if (filled) {
        saving = true;
        await api('/profile', { method: 'POST', body: JSON.stringify(project) });
        Object.assign(session.me, project);
        saving = false;
      }
    }
    markOnboarded();
    nav('#/hoy');
  }
</script>

{#if revisit}
  <button class="back" onclick={() => nav('#/perfil')}>‹ Perfil</button>
{/if}

<div style="margin-top:10px">
  <div class="eyebrow">{revisit ? 'Cómo funciona' : 'Bienvenida a Rumbo'}</div>
  <h1 style="margin-top:10px">Así vas a trabajar aquí.</h1>
</div>

{#if !revisit}
  <!-- The transversal project, declared ONCE at the learner level (docs/09):
       every exercise in every course builds on it, the tutor evaluates against
       it, and it is what lets work compile across courses into one document. -->
  <div class="card" style="margin-top:8px">
    <div class="row" style="gap:10px;color:var(--amber)">
      <Icon name="target" /><b class="t-md" style="color:var(--text)">Tu proyecto, antes de empezar</b>
    </div>
    <p class="muted t-sm" style="margin:8px 0 12px">
      Todos tus ejercicios construyen sobre UN proyecto real: tu negocio, o una
      marca o empresa donde te gustaría trabajar. Tu tutora evalúa contra este
      contexto y tu trabajo se acumula en un documento profesional.
    </p>
    <div style="display:flex;flex-direction:column;gap:10px">
      <div>
        <label for="pname">Tu proyecto o marca</label>
        <input id="pname" maxlength="120" bind:value={project.project_name}
               placeholder="Ej: Dulce Rosa, mi pastelería / Falabella (propuesta)" />
      </div>
      <div>
        <label for="pdesc">De qué se trata (una línea)</label>
        <input id="pdesc" maxlength="500" bind:value={project.project_desc}
               placeholder="Ej: pastelería artesanal en Santiago, vende por Instagram" />
      </div>
      <div>
        <label for="pgoal">Tu meta</label>
        <input id="pgoal" maxlength="200" bind:value={project.goal}
               placeholder="Ej: conseguir trabajo en marketing digital / vender más" />
      </div>
    </div>
  </div>

  <button class="btn btn-primary" style="margin-top:8px" disabled={saving} onclick={() => done(true)}>
    Guardar y empezar <Icon name="arrow" class="ic ic-s" />
  </button>
  <button class="btn btn-ghost" style="margin-top:2px" onclick={() => done(false)}>
    Lo defino después
  </button>

  <div class="microlabel" style="margin-top:22px">Y así funciona el día a día</div>
{/if}

<HowItWorks />
