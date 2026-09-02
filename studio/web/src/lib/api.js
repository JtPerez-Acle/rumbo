/* Every call the learner app makes to its own API.
 *
 * One place, because two things must hold everywhere and neither is optional:
 * a 401 has to be recognisable rather than thrown, and any request that can
 * outlive a learner's patience needs a timeout AND a saved draft.
 */

/** A learner API call. Returns `{__unauth:true}` on 401 rather than throwing. */
export async function api(path, options) {
  const r = await fetch('/api/learn' + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (r.status === 401) return { __unauth: true };
  return r.json();
}

/* Evaluations really take 25-35 seconds (measured), and there was no timeout
   anywhere: a stalled request left the "tu tutora está leyendo" card spinning
   forever with the send button hidden, and the only way out — reload —
   destroyed the work, because nothing was ever saved. Both halves are fixed:
   this aborts, and drafts.js keeps what they wrote. */
export const EVAL_TIMEOUT_MS = 90000;

/** POST with a hard timeout. Never throws: returns `{res, data}`, res null on failure. */
export async function postWithTimeout(path, body, ms) {
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), ms || EVAL_TIMEOUT_MS);
  try {
    const res = await fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: ctl.signal,
    });
    return { res, data: await res.json().catch(() => ({})) };
  } catch (e) {
    return {
      res: null,
      data: {
        detail: e && e.name === 'AbortError'
          ? 'La evaluación está tardando más de lo normal. Tu trabajo sigue aquí — vuelve a enviarlo.'
          : 'Se cortó la conexión. Tu trabajo sigue aquí — vuelve a enviarlo cuando tengas señal.',
      },
    };
  } finally {
    clearTimeout(timer);
  }
}

/** Send a signed-out learner to the sign-in page. */
export function toLogin() {
  location.href = '/login';
}
