<script>
  /* The waitlist.
   *
   * A real <form> for the same reason as the login one: Enter submits, and the
   * browser can fill the name and email it already knows.
   */
  import { PATHS } from '../lib/icons.js';

  let name = $state('');
  let email = $state('');
  let motivo = $state('');
  let company = $state(''); // honeypot
  let msg = $state('');
  let busy = $state(false);
  let done = $state(false);

  /* If they came from a job analysis, the role IS the answer. Prefilling it
     costs them nothing and turns the waitlist into a real demand signal. */
  $effect(() => {
    try {
      const role = sessionStorage.getItem('aprende_job_role');
      if (role && !motivo) motivo = 'Quiero postular a: ' + role;
    } catch {
      /* private mode, or storage disabled — the field just stays empty */
    }
  });

  async function submit(event) {
    event.preventDefault();
    if (!email.includes('@')) {
      msg = 'Escribe un correo válido.';
      return;
    }
    busy = true;
    msg = '';
    try {
      const res = await fetch('/api/learn/waitlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, motivo, company }),
      });
      if (!res.ok) {
        msg = 'No pudimos anotarte, intenta de nuevo.';
        return;
      }
      done = true;
    } catch {
      msg = 'No pudimos conectarnos. Revisa tu conexión e intenta de nuevo.';
    } finally {
      busy = false;
    }
  }
</script>

{#if done}
  <div class="celebrate">
    <div class="medal">
      <svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d={PATHS.send} /></svg>
    </div>
    <h2 style="margin-top:18px">¡Listo!</h2>
    <p class="muted">Te escribiremos cuando tu cupo esté disponible.</p>
  </div>
{:else}
  <form style="margin-top:14px;display:flex;flex-direction:column;gap:15px" onsubmit={submit}>
    <div>
      <label for="wl-name">Tu nombre</label>
      <input id="wl-name" bind:value={name} placeholder="Ana" autocomplete="name" />
    </div>
    <div>
      <label for="wl-email">Tu correo</label>
      <input id="wl-email" type="email" bind:value={email} placeholder="tu@correo.com" autocomplete="email" />
    </div>
    <div>
      <label for="wl-motivo">¿Qué quieres lograr? (opcional)</label>
      <textarea
        id="wl-motivo"
        bind:value={motivo}
        maxlength="500"
        placeholder="Ej: conseguir trabajo en marketing digital, hacer crecer mi tienda…"
      ></textarea>
    </div>

    <input
      bind:value={company}
      tabindex="-1"
      autocomplete="off"
      aria-hidden="true"
      style="position:absolute;left:-9999px;opacity:0;height:0;width:0"
    />

    <button class="btn btn-primary" type="submit" disabled={busy}>Anotarme</button>
    <div class="center muted t-sm" role="status" aria-live="polite">{msg}</div>
  </form>
{/if}
