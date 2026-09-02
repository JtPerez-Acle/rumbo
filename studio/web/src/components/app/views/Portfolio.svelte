<script>
  /* Portafolio: the deliverables first, the raw work under them.
   *
   * The ordering is the argument. What a learner shows someone is the compiled
   * document; the individual submissions are the evidence it was built from,
   * and they collapse.
   */
  import Icon from '../Icon.svelte';
  import { api, toLogin } from '../../../lib/api.js';
  import { nav } from '../../../lib/router.svelte.js';
  import { VERDICT } from '../../../lib/verdicts.js';

  const KIND = { explain: 'Explicación', exercise: 'Ejercicio', capstone: 'Reto de módulo' };

  let items = $state(null);
  let groups = $state([]);
  let open = $state(new Set());
  let compiling = $state('');

  $effect(() => {
    (async () => {
      const pf = await api('/portfolio');
      if (pf.__unauth) return toLogin();
      items = pf.items || [];

      // Group by course, preserving the order the API returned them in.
      const byCourse = new Map();
      for (const it of items) {
        const key = it.course_slug || 'otros';
        if (!byCourse.has(key)) {
          byCourse.set(key, { slug: key, title: it.course_title || 'Otros', items: [] });
        }
        byCourse.get(key).items.push(it);
      }
      const list = [...byCourse.values()];
      const statuses = await Promise.all(
        list.map((g) => (g.slug === 'otros' ? null : api('/project-doc/' + g.slug))),
      );
      groups = list.map((g, i) => ({ ...g, doc: statuses[i] && !statuses[i].detail ? statuses[i] : null }));
    })();
  });

  function toggle(id) {
    const next = new Set(open);
    next.has(id) ? next.delete(id) : next.add(id);
    open = next;
  }

  async function compile(slug) {
    compiling = slug;
    const res = await fetch('/api/learn/project-doc/' + slug, { method: 'POST' });
    compiling = '';
    if (res.ok) nav('#/documento/' + slug);
  }

  const scoreClass = (s) => (s >= 80 ? 'hi' : s >= 60 ? 'mid' : 'lo');
</script>

{#if items}
  <div class="topbar">
    <div class="brandrow">
      <div class="brandmark"></div>
      <div class="brandname">Portafolio<small>Tu trabajo, tu evidencia</small></div>
    </div>
  </div>

  {#if !items.length}
    <div class="card-paper" style="margin-top:6px">
      <h3>Todavía no hay piezas aquí</h3>
      <p class="muted t-sm" style="margin-top:8px">
        Cada ejercicio que envías se vuelve una sección de tu documento
        profesional. Empieza una lección y tu portafolio se construye solo.
      </p>
    </div>
    <button class="btn btn-primary" style="margin-top:8px" onclick={() => nav('#/cursos')}>
      Ir a mis cursos <Icon name="arrow" class="ic ic-s" />
    </button>
  {:else}
    {#each groups as g}
      <div class="modhead" style="margin-top:18px">{g.title}</div>

      {#if g.doc}
        <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:10px">
          {#if g.doc.exists}
            <button class="btn btn-paper" onclick={() => nav('#/documento/' + g.slug)}>
              <Icon name="doc" class="ic ic-s" /> {g.doc.doc_type}
            </button>
          {:else if g.doc.eligible}
            <button class="btn btn-paper" disabled={compiling === g.slug}
                    onclick={() => compile(g.slug)}>
              <Icon name="doc" class="ic ic-s" />
              {compiling === g.slug ? 'Compilando… (unos segundos)' : `Compilar mi ${g.doc.doc_type}`}
            </button>
          {:else}
            <!-- The gate is deliberate, not a tease: fed one or two pieces the
                 compiler does not produce a short document, it fills the vacuum
                 by inventing. -->
            <p class="faint t-sm">
              {g.doc.doc_type}: se desbloquea con {g.doc.needed} trabajos · llevas
              {g.doc.submissions}.
            </p>
          {/if}
        </div>
      {/if}

      {#each g.items as it (it.id ?? it.title + it.created_at)}
        <!-- A disclosure, not a div with a click handler. The feedback under
             each row is the point of the row, and it was unreachable by
             keyboard and unannounced to a screen reader. -->
        <details class="pf-row" open={open.has(it)} ontoggle={() => toggle(it)}>
          <summary>
            <div class="row" style="justify-content:space-between;gap:10px">
              <div style="flex:1;min-width:0">
                <div style="font-size:var(--fs-sm);font-weight:700;line-height:1.3">{it.title || ''}</div>
                <div style="font-size:var(--fs-xs);color:var(--faint);margin-top:2px">
                  {KIND[it.kind] || it.kind} · {it.created_at}
                </div>
              </div>
              {#if it.verdict}
                <div class={`vchip ${it.verdict}`}>{VERDICT[it.verdict] || ''}</div>
              {:else if it.score != null}
                <div class={`scorepill ${scoreClass(it.score)}`}>{it.score}</div>
              {/if}
            </div>
          </summary>
          <div class="fb">{it.feedback || ''}</div>
        </details>
      {/each}
    {/each}
  {/if}
{/if}
