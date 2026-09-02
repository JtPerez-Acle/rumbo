<script>
  /* Cursos: the library, grouped by area, with the learner's progress on it.
     Distinct from the PUBLIC catalog — this one knows where they are. */
  import Icon from '../Icon.svelte';
  import Flame from '../Flame.svelte';
  import Concierge from './Concierge.svelte';
  import { api, toLogin } from '../../../lib/api.js';
  import { nav } from '../../../lib/router.svelte.js';
  import { clusterize, CAT_ICON } from '../../../lib/icons.js';

  let data = $state(null);
  let reloadKey = $state(0);

  $effect(() => {
    reloadKey; // a submitted course request re-reads the catalog
    (async () => {
      const d = await api('/courses');
      if (d.__unauth) return toLogin();
      data = d;
    })();
  });

  const clusters = $derived(data ? clusterize(data.courses) : []);
  // Open the cluster where the learner is working; otherwise the first one.
  const openCat = $derived.by(() => {
    if (!data) return null;
    const active = data.courses.find((c) => c.done > 0);
    return active ? active.category || 'Más cursos' : clusters[0]?.[0] ?? null;
  });

  const pctOf = (c) => (c.total ? Math.round((c.done / c.total) * 100) : 0);
</script>

{#if data}
  <div class="topbar">
    <div class="brandrow">
      <div class="brandmark"></div>
      <div class="brandname">Rumbo<small>Tus cursos</small></div>
    </div>
    <Flame days={data.streak} />
  </div>

  <h2 style="margin-top:6px">Cursos</h2>

  {#each clusters as [category, courses]}
    <details class="cluster-wrap" open={category === openCat}>
      <summary class="cluster">
        <Icon name={CAT_ICON[category] || 'book'} />
        <h3 class="ct">{category}</h3>
        <span class="cn">{courses.length} {courses.length === 1 ? 'CURSO' : 'CURSOS'}</span>
        <span class="chev"><Icon name="arrow" class="ic ic-s" /></span>
      </summary>
      <div class="cluster-body">
        {#each courses as c}
          {#if c.available}
            <button class="card course-card" onclick={() => nav('#/curso/' + c.slug)}>
              <div class="pill go" style="position:absolute;top:14px;right:14px">
                {c.done > 0 ? pctOf(c) + '%' : 'Empezar'}
              </div>
              <h3>{c.title}</h3>
              {#if c.description}<p class="desc">{c.description}</p>{/if}
              {#if c.doc_type}
                <p class="delivers"><Icon name="doc" class="ic ic-s" /> Termina con: {c.doc_type}</p>
              {/if}
              <div class="prog"><i style={`clip-path:inset(0 ${100 - (pctOf(c))}% 0 0)`}></i></div>
              <div class="meta">
                <span>{c.done} de {c.total} lecciones · {c.modules} módulos</span>
                <Icon name="arrow" class="ic ic-s" />
              </div>
            </button>
          {:else}
            <div class="card course-card soon">
              <div class="pill soon" style="position:absolute;top:14px;right:14px">Próximamente</div>
              <h3>{c.title}</h3>
              {#if c.description}<p class="desc">{c.description}</p>{/if}
              {#if c.doc_type}
                <p class="delivers"><Icon name="doc" class="ic ic-s" /> Termina con: {c.doc_type}</p>
              {/if}
              <div class="meta">
                <span>{c.total} lecciones · {c.modules} módulos · en producción</span>
              </div>
            </div>
          {/if}
        {/each}
      </div>
    </details>
  {/each}

  <Concierge onsubmitted={() => (reloadKey += 1)} />
{/if}
