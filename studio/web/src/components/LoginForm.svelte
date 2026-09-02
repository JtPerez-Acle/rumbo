<script>
  /* Sign-in.
   *
   * A real <form>: it submits on Enter, the browser offers to save the
   * credentials, and every field is labelled. The SPA's version was three
   * inputs and a button with a click handler — Enter did nothing, which on a
   * three-field form is the single most common way to try to submit one.
   *
   * The two query parameters this page reads are handled here rather than by
   * the server, because the page itself is a static file: ?invite= prefills
   * the code (invite links land straight on it) and ?error= means an expired
   * magic link bounced back.
   */
  let name = $state('');
  let email = $state('');
  let invite = $state('');
  let company = $state(''); // honeypot
  let msg = $state('');
  let expired = $state(false);
  let busy = $state(false);

  $effect(() => {
    const q = new URLSearchParams(location.search);
    invite = q.get('invite') || '';
    expired = !!q.get('error');
  });

  async function submit(event) {
    event.preventDefault();
    if (!email.includes('@')) {
      msg = 'Escribe un correo válido.';
      return;
    }
    busy = true;
    msg = 'Un momento…';
    try {
      const res = await fetch('/api/learn/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, name, invite, company }),
      });
      if (res.status === 429) {
        msg = 'Demasiados intentos. Espera unos minutos.';
        return;
      }
      if (res.status === 403) {
        msg = 'Necesitas un código de invitación válido para entrar.';
        return;
      }
      /* 409 is the returning learner. Self-service re-login into an existing
         account is deliberately refused — it closed a live account-takeover
         hole — and the learner is queued instead. Saying that plainly beats
         the generic failure this branch used to fall through to. */
      const r = await res.json();
      if (res.status === 409) {
        msg = r.detail || 'Ya existe una cuenta con ese correo. Te escribimos para devolverte el acceso.';
        return;
      }
      if (r.sent) msg = 'Te enviamos un enlace a tu correo. Ábrelo para entrar.';
      else if (r.dev_link) window.location = r.dev_link;
      else msg = 'No pudimos generar tu acceso.';
    } catch {
      msg = 'No pudimos conectarnos. Revisa tu conexión e intenta de nuevo.';
    } finally {
      busy = false;
    }
  }
</script>

<form style="margin:auto 0;display:flex;flex-direction:column;gap:15px" onsubmit={submit}>
  {#if expired}
    <div class="card" style="border-color:var(--terra);color:var(--terra);font-size:var(--fs-sm)">
      El enlace no es válido o expiró. Pide uno nuevo.
    </div>
  {/if}

  <div>
    <label for="lg-name">Tu nombre</label>
    <input id="lg-name" bind:value={name} placeholder="Ana" autocomplete="name" />
  </div>
  <div>
    <label for="lg-email">Tu correo</label>
    <input id="lg-email" type="email" bind:value={email} placeholder="tu@correo.com" autocomplete="email" />
  </div>
  <div>
    <label for="lg-invite">Código de invitación</label>
    <input id="lg-invite" bind:value={invite} placeholder="Tu código de acceso" />
  </div>

  <input
    bind:value={company}
    tabindex="-1"
    autocomplete="off"
    aria-hidden="true"
    style="position:absolute;left:-9999px;opacity:0;height:0;width:0"
  />

  <button class="btn btn-primary" type="submit" disabled={busy}>Entrar</button>
  <div class="center muted t-sm" role="status" aria-live="polite">{msg}</div>
</form>
