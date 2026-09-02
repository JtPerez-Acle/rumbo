/* Who is using the app, and the one-time work that has to happen at boot.
 *
 * `me` carries the declared transversal project, which the exercise step and
 * Perfil both read — it is learner-level rather than per-course (docs/09),
 * because that is what lets work compile across courses into one document.
 */
import { api, toLogin } from './api.js';

export const session = $state({
  ready: false,
  authenticated: false,
  me: {},
  onboarded: false,
});

const ONBOARDED_KEY = 'aprende_onboarded';
const JOB_TOKEN_KEY = 'aprende_job_token';

export function markOnboarded() {
  try { localStorage.setItem(ONBOARDED_KEY, '1'); } catch { /* private mode */ }
  session.onboarded = true;
}

export async function boot() {
  /* One round trip before anything renders, and here that is correct: this is
     an app behind a session, so there is nothing to show until we know whose it
     is. The version of this that mattered was on the PUBLIC pages, where the
     same await made a fully-rendered page sit for 147ms and then be replaced by
     an empty one. Those are static files now and never call this. */
  const me = await api('/me');
  session.authenticated = !!me.authenticated;
  session.me = me;

  if (!session.authenticated) {
    // The server redirects a cookie-less request to /aprende, so reaching here
    // means the session expired between the document load and now.
    toLogin();
    return;
  }

  /* A route analysed before signing up is the reason many people sign up at
     all. It lives in localStorage until there is a session to attach it to;
     without this the most motivating artifact we can produce evaporates at the
     door. Never blocks boot: a failure here costs one claim, not the app. */
  let jobToken = null;
  try { jobToken = localStorage.getItem(JOB_TOKEN_KEY); } catch { /* private mode */ }
  if (jobToken) {
    try {
      await api('/job-target/claim', {
        method: 'POST',
        body: JSON.stringify({ token: jobToken }),
      });
      localStorage.removeItem(JOB_TOKEN_KEY);
    } catch { /* non-fatal */ }
  }

  try { session.onboarded = !!localStorage.getItem(ONBOARDED_KEY); } catch { /* private mode */ }
  session.ready = true;
}
