<script>
  /* A CV is a CLAIM, and this product exists because claims are not trusted —
   * work is (docs/10).
   *
   * So nothing on this screen removes a lesson or locks anything. It PROPOSES
   * skips the learner accepts, every skip stays reversible, and the only thing
   * that turns "ya lo sé" into something that counts is passing that module's
   * reto — a case the lessons never covered. Exemptions live in
   * `module_exemptions`, never in `progress`: writing fake completions would
   * corrupt the streak, the SM-2 ladder and the Module-1 gate.
   */
  import Icon from '../Icon.svelte';
  import CvClaim from './CvClaim.svelte';
  import StageClock from '../StageClock.svelte';
  import { api, toLogin, postWithTimeout } from '../../../lib/api.js';
  import { loadDraft, draftSaver, clearDraft } from '../../../lib/drafts.js';
  import { nav } from '../../../lib/router.svelte.js';

  const CV_STAGES = [
    [0, 'Leyendo tu experiencia', 'Lo que hiciste en cada puesto, no los títulos.'],
    [20, 'Cruzando con los módulos', 'Uno por uno, contra lo que cada módulo promete que vas a saber hacer.'],
    [45, 'Buscando la cita', 'Nada cuenta como sabido si no está escrito en tu CV.'],
  ];
  const CV_TIMEOUT_MS = 180000;

  let phase = $state('loading'); // loading | form | reading | result | deleted
  let data = $state(null);
  let cv = $state(loadDraft('cv', 0));
  let company = $state('');
  let msg = $state('');
  let deleting = $state(false);
  const save = draftSaver('cv', 0);

  $effect(() => {
    (async () => {
      const d = await api('/cv');
      if (d.__unauth) return toLogin();
      if (d.exists) { data = d; phase = 'result'; }
      else phase = 'form';
    })();
  });

  // Kept in sync from the server (writer.EXEMPTION_PASS_SCORE) so the copy can
  // never promise a bar the backend does not enforce.
  const passScore = $derived(data?.pass_score ?? 70);

  async function run() {
    if (cv.trim().length < 200) {
      msg = 'Pega tu CV completo: con lo que hiciste en cada puesto, no solo los cargos.';
      return;
    }
    msg = '';
    phase = 'reading';
    const { res, data: r } = await postWithTimeout(
      '/api/learn/cv', { cv: cv.trim(), company }, CV_TIMEOUT_MS,
    );
    if (!res || !res.ok) {
      // The CV is still in the draft, so this reopens the form filled in.
      msg = (r && r.detail) || 'No pudimos leer tu CV. Vuelve a intentarlo en unos minutos.';
      phase = 'form';
      return;
    }
    clearDraft('cv', 0);
    data = r;
    phase = 'result';
  }

  async function remove() {
    deleting = true;
    const r = await api('/cv', { method: 'DELETE' });
    deleting = false;
    if (r && r.ok) phase = 'deleted';
    else msg = 'No pudimos borrarlo, intenta de nuevo.';
  }

  const claims = $derived(data?.claims || []);
  const strong = $derived(claims.filter((c) => c.proposed));
  const weak = $derived(claims.filter((c) => !c.proposed));
  const accredited = $derived(claims.filter((c) => c.state === 'acreditado'));
</script>

{#if phase !== 'reading'}
  <button class="back" onclick={() => nav('#/objetivo')}>‹ Mi objetivo</button>
{/if}

{#if phase === 'form'}
  <div style="margin-top:14px;display:flex;flex-direction:column;gap:15px">
    <div>
      <div class="eyebrow">Tu experiencia</div>
      <h1 style="margin-top:10px">¿Ya sabes parte de esto?</h1>
      <p class="muted" style="margin-top:8px">
        Pega tu CV y te decimos qué módulos de tu ruta ya hiciste en tu trabajo,
        con la frase de tu CV que lo dice. <b>Tú decides</b> cuáles saltarte, y
        puedes probarlos con su reto para dejarlos acreditados.
      </p>
    </div>

    <div>
      <label for="cvtext">Tu CV</label>
      <textarea id="cvtext" rows="12" maxlength="20000" bind:value={cv}
                oninput={() => save(cv)}
                placeholder="Pega aquí tu experiencia: cada puesto y qué hiciste en él…"></textarea>
      <p class="faint t-sm" style="margin-top:6px">
        Lo que importa es <b>qué hiciste</b>, no los títulos: "instalé el píxel
        en 12 tiendas" dice mucho más que "Media Buyer".
      </p>
    </div>

    <input bind:value={company} tabindex="-1" autocomplete="off" aria-hidden="true"
           style="position:absolute;left:-9999px;opacity:0;height:0;width:0" />

    <div class="note">
      <Icon name="lock" class="ic ic-s" />
      <span>Borramos tu correo y tu teléfono antes de guardar nada, tu CV no se
      muestra en ningún lado, y puedes borrarlo cuando quieras. No lo usamos en
      tu documento: ahí solo va trabajo tuyo evaluado.</span>
    </div>
    <div class="note note-warn">
      <Icon name="clock" class="ic ic-s" />
      <span>Leerlo tarda <b>cerca de un minuto</b>. No cierres esta pestaña.</span>
    </div>

    <button class="btn btn-primary" onclick={run}>
      Leer mi CV <Icon name="arrow" class="ic ic-s" />
    </button>
    <div class="center muted t-sm" role="status" aria-live="polite">{msg}</div>
  </div>

{:else if phase === 'reading'}
  <div style="margin-top:10px">
    <div class="eyebrow">Leyendo tu CV</div>
    <h2 style="margin-top:10px">Tu tutora está leyendo tu experiencia.</h2>
    <p class="muted t-sm" style="margin-top:8px">
      Busca en qué módulos ya hiciste el trabajo — y no da por sabido nada que
      tu CV no diga.
    </p>
  </div>
  <StageClock stages={CV_STAGES} />

{:else if phase === 'deleted'}
  <div style="margin-top:14px">
    <div class="eyebrow">Tu experiencia</div>
    <h1 style="margin-top:10px">Listo, lo borramos.</h1>
    <p class="muted" style="margin-top:8px">
      {accredited.length
        ? 'Los módulos que acreditaste con su reto siguen acreditados: eso lo probaste tú, no lo dijo tu CV.'
        : 'Los módulos que te habías saltado vuelven a tu ruta.'}
    </p>
  </div>
  <button class="btn btn-primary" style="margin-top:14px" onclick={() => nav('#/objetivo')}>
    Volver a mi objetivo
  </button>

{:else if phase === 'result' && data}
  <div style="margin-top:6px">
    <div class="eyebrow">Lo que ya traes</div>
    <h1 style="margin-top:10px">{data.headline || 'Leímos tu CV'}</h1>
    <p class="muted" style="margin-top:8px">
      {#if strong.length}
        Encontramos <b>{strong.length} módulo{strong.length > 1 ? 's' : ''}</b> de
        nuestro catálogo que tu CV muestra que ya hiciste — {data.proposed_lessons}
        lecciones. Decide tú qué hacer con cada uno.
      {:else}
        No encontramos módulos que tu CV demuestre haber hecho. Eso no dice nada
        malo de tu experiencia: solo significa que no podemos citarla, y sin cita
        no damos nada por sabido.
      {/if}
    </p>
  </div>

  {#if strong.length}
    <div class="microlabel" style="margin-top:18px">Tú decides</div>
    {#each strong as c (c.course_slug + ':' + c.module_no)}
      <CvClaim claim={c} {passScore} />
    {/each}
  {/if}

  {#if weak.length}
    <div class="microlabel" style="margin-top:18px">
      Lo leímos, pero no alcanza para saltártelo
    </div>
    <div class="card">
      {#each weak as c}
        <div class="gaprow">
          <span class="gx"><Icon name="alert" class="ic ic-s" /></span>
          <span>{c.course_title} · módulo {c.module_no} —
            <span class="faint">{c.capability || ''}</span></span>
        </div>
      {/each}
      <p class="faint t-sm" style="margin:10px 2px 0">
        Mencionar algo no es lo mismo que haberlo hecho. Si crees que sí lo
        dominas, entra al módulo y prueba su reto: se acredita solo.
      </p>
    </div>
  {/if}

  {#if data.fuera_del_catalogo?.length}
    <div class="microlabel" style="margin-top:18px">Esto traes y no lo enseñamos</div>
    <div class="card">
      {#each data.fuera_del_catalogo as x}
        <div class="gaprow">
          <span class="gx"><Icon name="check" class="ic ic-s" /></span>
          <span>{x.name}</span>
        </div>
      {/each}
      <p class="faint t-sm" style="margin:10px 2px 0">
        Si tu objetivo pide algo de esta lista, ya lo tienes: cuéntalo en la
        entrevista.
      </p>
    </div>
  {/if}

  <div style="margin-top:22px">
    <p class="faint t-sm">
      Leído el {data.created_at || ''}. Tu CV no aparece en tu documento ni en
      ninguna página pública — ahí solo va trabajo tuyo evaluado.
    </p>
    <div style="display:flex;flex-direction:column;gap:8px;margin-top:10px">
      <button class="btn btn-ghost" onclick={() => { phase = 'form'; msg = ''; }}>Pegar otro CV</button>
      <button class="btn btn-ghost" disabled={deleting} onclick={remove}>
        {deleting ? 'Borrando…' : 'Borrar mi CV'}
      </button>
    </div>
    <div class="center muted t-sm" style="margin-top:8px" role="status" aria-live="polite">{msg}</div>
  </div>
{/if}
