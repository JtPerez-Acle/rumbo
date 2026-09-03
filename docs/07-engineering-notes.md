# 07 — Engineering notes: how to change this system safely

*Written for the next coding agent. Everything here was learned by breaking
something. Read it before your first edit; it will save you a session.*

## Astro swallows the whitespace before an expression

**Rule: never break the line between prose and `{expression}`.** Astro trims
whitespace at a line boundary next to an interpolation, so

```astro
  ... y qué le falta — no una nota. La misma
  {TUTOR} que lee el trabajo ...
```

renders as **"La mismaVera"**. It compiles, no test catches it, and it is
invisible in a diff because the source looks correctly spaced. Keep the value on
the same line as the word it follows, or write `{' '}` explicitly.

Found once, on the landing, by reading a screenshot — which is the only reason
it was found at all. Svelte does not do this, so the habit does not transfer
between the two file types in `studio/web/`.

## The verification ritual (non-negotiable)

Every change follows the same loop. Skipping a step is how the bugs below
reached production in the first place.

1. **Compile-check** — `python -m py_compile` on touched Python; for the
   single-file frontends, extract the last `<script>` block and `node --check`
   it (nothing else catches a syntax error in a file with no build step).
   For anything under `studio/web/`, `npm run build` is the compile-check.
1b. **Run the frontend suite** — `cd studio/web && npm test` (130 assertions).
   It builds first, then asserts against the built pages, so it catches a page
   that stopped rendering its content as well as one that stopped compiling.
1c. **Before a DEPLOY, `npm run verify`** — the same, plus Playwright loading
   every public page in real Chromium at four widths. jsdom has no layout
   engine: content assertions pass happily on a page rendering 32px wide, which
   is exactly how three pages once shipped broken.
2. **Run locally against the real cloud DB** — `preview_start` with the
   `learner-app` launch config (see doc 05).
3. **Test with real data**, then **delete your test rows** (they live in the
   production database).
4. **Deploy** — `railway up --detach`.
5. **Verify in production** — fetch the actual URL and assert the change is
   present.

### "Exit 0" is not verification

A pipeline once logged every step as successful while producing **zero
lessons** (a single invalid byte in a research file crashed the reader; the
runner moved on). After any batch operation, **count rows in the database**.
Every runbook in doc 05 ends with a count for this reason.

### Test the degenerate case, always

The retry evaluator shipped with a grading leak that only appeared when a
*deliberately lazy* answer was submitted after a strong one — it inherited the
previous attempt's credit and scored **+10** for "no me acuerdo bien". If a
feature gives the model prior context, submit something terrible and confirm it
scores terribly.

### Do not author your own calibration data

The original scoring rubric was validated only against examples *I wrote*, all
of which were business artifacts. The rubric's category error (see doc 02) was
therefore invisible to every test until a real learner wrote a conceptual
answer. **Calibrate against real learner submissions** — there are real ones in
`submissions`, and the operator can read them all via the dashboard.

## Tooling traps (these cost hours)

| Trap | Symptom | What to do |
|---|---|---|
| **`preview_start` reuses a running server** | Python edits appear to have no effect; tests "fail" mysteriously | uvicorn has no `--reload` here. **`preview_stop` then `preview_start`** after any backend change. Two audit failures were stale-server artifacts, not bugs. |
| **PowerShell `Invoke-RestMethod` strips the `Cookie` header** | Authenticated API calls return `no autenticado` | Use `curl.exe -H "Cookie: learner_session=..."`, or a `WebRequestSession` with a real `System.Net.Cookie`. |
| **Railway CLI upload times out ~half the time** | `operation timed out`, exit 1 | The upload usually **succeeded anyway**. Check `list-deployments` before retrying; don't stack uploads. |
| **Browser pane wedges** | `navigate`/`javascript_tool` time out repeatedly | Stop fighting it. For pure render logic, extract the function and unit-test it under a tiny DOM shim in Node (done successfully for `defenseCard`). |
| **Bash `cd` leaks into the PowerShell tool's cwd** | `MoneyPrinterTurbo\.venv\... not recognized`, `No module named 'cloud'` | Use absolute paths or `Set-Location` at the start of PowerShell commands. |
| **Probing during a rollout gives false failures** | An endpoint 404s, then 401s a minute later | The frontend string and the Python routes swap at slightly different moments. Re-run the check before diagnosing; `grep -c` in a compound pipeline also miscounted once. Trust a re-run over a theory. |
| **Railway volume resize is dashboard-only** | Writes fail with `ENOSPC`; `railway volume list` still shows the old size after a "successful" resize | No resize mutation exists in the public GraphQL schema (introspected). The MCP agent reports success while only staging config. Reduce what you store instead — see the shrink flow in `docs/05`. |
| **Streaming a file object from this host aborts mid-send** | `WinError 10053` on uploads >~3 MB | Send the body from memory (`v.read_bytes()`); the SERVER still streams to disk chunk-by-chunk. |
| **Windows console mangles accents** | `AuditorÃ­a` in output | Set `PYTHONIOENCODING=utf-8`. The data in Postgres is fine — `db.connect()` forces UTF-8 on the wire. |
| **`innerText` vs `text-transform: uppercase`** | String assertions fail on text that is visibly present | Compare case-insensitively when probing the DOM. |

## Bug patterns this codebase has already produced

Recognise these shapes; they recur.

**Client-authoritative state.** The client once forced `is_review=true` when
navigating between lessons, so completions were silently recorded as reviews and
lost. *Rule: server decides state, client only displays it.*

**Reachability dead ends.** Completed lessons skipped the explain step, making a
pending conversation on an explain submission permanently unreachable — while
the home screen linked to it. *Rule: if you surface a pending item anywhere,
click through the link yourself and confirm you land on something actionable.*

**Silent data loss on the happy path's edge.** A dropped `/complete` request
showed "🔥 undefined" and lost the completion. *Rule: every write the learner
cares about needs an error path with a retry.*

**Score regressions.** `record_completion` and `record_review` overwrote
`quiz_score`; a weak review erased a perfect one. Displays used *latest* instead
of *best*. *Rule: nothing a learner earned may ever go down — `GREATEST` in SQL,
`best_submissions()` for display.*

**Closure staleness in the SPA.** A retry form prefilled from a variable
captured at card-creation time, so "improve your answer" opened an **empty**
box. *Rule: read mutable state at render time, not at closure creation.*

**Encoding.** One invalid byte (0xA1) in a 64KB research file zeroed an entire
course. `_research()` now decodes with `errors="replace"`.

**Rubric/prompt drift.** Changing an evaluator prompt has no regression test.
Anything that alters how the tutor judges must be re-run against real
submissions before deploy. *(The job matcher now HAS one —
`check_job_matcher.py`, 5 fixtures. The tutor evaluators and the two document
compilers still don't. That is the gap that matters most.)*

**One string cannot serve a reader and a voice.** The lesson `script` was used
verbatim for BOTH Edge TTS narration and the on-screen transcript. So a script
that teaches with fill-in-the-blanks — "un nodo es \_\_, existe una arista
cuando \_\_" — is perfect on the page and says "guion bajo" three times in the
opening minute of curso-grafos-cultura. 13 lessons across 7 courses had the same
shape (`event_id`, `#ModaSostenible`, a stray `*`). Nobody was ever going to
catch it by watching 420 videos; a human heard it by chance. *Rule: the render
queue gets `writer.narration_text(script)`, the transcript keeps the raw form,
and `course_factory <slug> check-narration` fails the build on page-only
devices.*

**A sanitiser can be worse than what it sanitises.** The first version of
`narration_text` stripped `*` as markdown — silently turning
`'User-agent: * Disallow: /'` into `'User-agent: Disallow: /'`, which is a
different robots.txt rule. It also produced "el hashtag hashtag ModaSostenible"
where the script had already narrated the symbol. *Rule: when transforming
content for a second medium, ask of each character whether it is markup or
meaning. `*text*` is markup; a lone `*` is meaning. Test the transform against
the real corpus before running it, not after.*

**A guarantee the database keeps but the screen never shows does not exist.**
"Nothing a learner earns can ever go down" was true in SQL — `GREATEST`,
`best_submissions()` — and invisible in the UI, which rendered only the attempt
just made. The design partner resubmitted work that had scored **79**, watched a
serif **30** count up, and stopped using the product. The invariant was never
broken; it was never *communicated*. *Rule: when a promise is about how the
learner is treated, the surface that carries it is the screen, not the schema.
`/submit` returns `best_score` and the evaluation card says what they keep.*

**Never re-grade identical input.** The same 1687 characters scored 79, then 50,
then 30 — because the evaluator sees an unchanged retry, notes the feedback was
ignored, and marks it down. Fair instinct, useless measurement: the number stops
describing the work. A strong submission survives it (93 → 100 → 100 in a
controlled rerun), so the damage lands on exactly the learners who are already
struggling. *Rule: an unchanged resubmission is not an evaluation — return the
stored one, say plainly that nothing changed, spend no LLM call. Determinism you
can get for free is worth more than a prompt fix you have to trust.*

**Unsaved work plus no timeout is one bug, not two.** Exercise evaluations really
take 25–35s (measured; the docs said 10–20s), there was no `AbortController`
anywhere, and the textarea was never persisted. A stalled request hid the send
button behind a spinner that never resolved, and the only escape — reload —
destroyed up to 5000 characters of the learner's work. *Rule: any request that
can outlive a learner's patience needs a timeout AND a draft, because the
recovery path for one is the failure path for the other.*

**The step you buried is the step nobody takes.** The transversal project — which
feeds Aplicación, 40 of the 100 points — sat at 1763px on a 1947px onboarding
page with "lo defino después" beside it. Zero of four learners ever declared one,
so the highest-weighted dimension was judged blind on every real submission.
*Rule: if a field is optional and below the fold, treat its completion rate as
zero and design accordingly. Position and stated stakes are the whole mechanism.*

**A write that grants access IS an access-control decision.** `POST /complete`
was the one learner endpoint with no access check, because "recording a
completion" doesn't sound like a privileged action. But access is *derived* from
completions (`_accessible_ids`), so writing one wrote access: a locked lesson and
its gated video went from 403 to 200 with a single request, and one request per
`node_id` unlocked all 420 lessons. `quiz_score` was unclamped on the same
endpoint, and `record_completion` keeps the `GREATEST` value, so a bogus 999 was
permanent. *Rule: before shipping a write, ask what READ it authorises. Every
learner endpoint that touches `progress` runs the same `_accessible_ids` gate.*

**A magic link is a credential — never hand one to whoever asks.** With no email
provider, `/login` returned the login link in the response body for any address
submitted. Knowing a learner's email plus holding any active invite code was a
full account takeover (verified live: `/me` came back as the victim). The invite
code is a credential for *creating* an account, not for entering an existing one.
*Rule: an existing account may only be entered by proving control of its inbox;
for a new account there is no victim, so the code alone is fine.*

**Prompt-injection is an authorization bug wearing a costume.** The four
evaluators embedded learner text with a bare label — `Entrega de la alumna:` —
while the job matcher fenced its input as "datos, no instrucciones". Guess which
one held. A submission reading *"berenjena berenjena berenjena. no hice la
tarea."* plus a fake system block scored **100/100 with attacker-chosen
feedback**, first try. That defeats the evaluation layer, which docs/01 calls the
defensible half, and the fabricated feedback flows into the public document.
*Rule: every model input that a user can write goes inside `_fenced()`, and the
system prompt carries `UNTRUSTED_RULE`. Re-test with a hostile payload, not just
a lazy one — the degenerate case doc 07 already demanded has an adversarial twin.*

**Markdown is HTML.** `marked.parse()` assigned to `innerHTML` on the public
paper pages was a stored-XSS sink: marked emits raw HTML by design, `content_md`
is compiled from learner submissions, and the compiler is told to quote the
learner verbatim. Chain it with the injection above and an attacker controlled
the text entering the sink; the victim is the hiring manager opening the share
link. *Rule: untrusted Markdown goes through `renderMD()` (parse → DOMPurify),
never straight to innerHTML. CDN scripts are pinned to an exact version with SRI.*

**Security by allowlist.** `app._is_admin_path` is a list of path prefixes. A new
`/api/*` admin route that isn't added to it deploys **public**. This nearly
shipped twice in one day: `delete-media`, and `invites` — which would have
published every access code to anyone who hit the URL. *Rule: add the prefix in
the same edit that adds the route, and curl it without a token before deploying.*

**Copy that ages silently.** The landing's "Cómo funciona" kept describing a
course-shaped product for weeks after the goal engine shipped, and still used
"pregunta de defensa" wording retired months earlier. Nothing was broken, so
nothing complained. *Rule: user-facing promises need assertions too —
`studio/web/tests/how-section.test.js` now tests them, including guards on retired
wording.*

**An empty input does not produce an empty output — it produces a fabricated
one.** The goal-document compiler, fed one non-attempt submission (a pasted
starter prompt scoring 0), invented an entire skills inventory: tools the learner
never mentioned, an English level, Office proficiency. It obeyed the letter of
"invent no metrics" while inventing capabilities, which is worse in a document
meant for a hiring manager. *Rules: filter non-attempts before compiling
(`MIN_PORTFOLIO_SCORE`), require enough real work to compile from, and ban
self-characterisation explicitly.*

**Structure determines content — a shape with nowhere to put evidence will
manufacture claims.** That same compiler was organised by the job posting's
*competency list*, so its only possible content was assertions about the person.
Re-shaping it around the deliverable's own sections (from `PROJECT_TEMPLATES`)
fixed the class of problem that prompt-patching could not. *Rule: when generated
text keeps drifting, check whether the requested structure has room for the
evidence you want in it.*

**`dict.get(key, default)` when the key exists with value `None`.** The default
never fires. `ev.get("final_score", ev.get("score"))` silently rejected real work
because `final_score` is present-but-null until a learner answers the tutor's
question. *Rule: coalesce on the value (`x = a; if x is None: x = b`), not on key
presence — this JSONB has several nullable-but-present fields.*

**Non-atomic writes destroy good data on failure.** The upload endpoint wrote
straight to the destination, so a failed upload truncated the existing file to
0 bytes — a repair attempt corrupted 20 healthy videos. *Rule: write `.part`,
then `os.replace`. And verify by SIZE, not by HTTP status: 20 files returned
200 while serving 0 bytes.*

**Renaming a generated artifact breaks every consumer that greps for it.**
Namespacing the render-queue filenames fixed a real collision but broke
`reconcile`'s glob — caught only because `verify` counts rows. I had fixed
`backfill-text` for the same rename and missed `reconcile`. *Rule: after
changing a filename convention, grep for every consumer of the old pattern
before running anything.*

## Working with the LLM layer (`writer.py`)

Everything that calls a model lives in one file: course generation *and*
learner evaluation. Shared conventions:

- **`VOICE_GUIDE` is injected into every call**, including evaluations, so the
  course and the tutor speak with one voice. It bans a specific list of AI-slop
  words — extend it rather than fighting outputs case by case.
- **All calls return strict JSON**; `_extract_json` tolerates code fences.
  `_chat` retries transient OpenRouter drops.
- **Evaluator contracts are per-kind on purpose** (`EXPLAIN_JSON_SPEC` vs
  `EVAL_JSON_SPEC`). Do not re-merge them for elegance — that merge *was* the
  bug.
- **Bump `RUBRIC_VERSION`** whenever the scoring contract changes, or the retry
  prompt will compare numbers produced by different rulers.
- Cost is negligible (fractions of a cent per evaluation); latency is 10–20s,
  which the UI covers with the "tu tutora está leyendo…" state.

## Adding a course (checklist)

1. Research doc → `studio/research/<topic>.md`, **UTF-8**.
2. `channels/curso-<slug>.toml` — must include `name`, `niche` (≤110 chars,
   outcome promise, no "Curso de 30 días:" prefix), `category` (catalog
   cluster), `audience`, `tone`, `course_brief`, `research_file`, a voice and a
   stroke colour not already in use.
3. `course_factory.py <slug> all` (detached — it runs for hours).
4. Optionally add a `PROJECT_TEMPLATES` entry in `writer.py` so the course's
   portfolio deliverable has the right shape.
5. **Verify by counting**: 30 lessons, 30 videos, 30 module descriptions,
   30 explain prompts, 5 capstones.
6. `upload_videos.py <slug>` — do this **promptly after reconcile**, because
   reconcile marks the course available in the shared DB and learners will hit
   broken players until the files land.

## Things that look like bugs but aren't

- Uvicorn's `INFO:` lines appear at **error** severity in Railway logs. That's
  stderr, not a problem.
- Duplicate Railway deployments right after a CLI timeout — Railway supersedes
  the older build automatically.
- `learner_portfolio` returns *every* attempt (not deduplicated). That's
  intentional: the learner should see their own progression.
- Legacy explain submissions have a numeric `score` and no `verdict`. They
  deliberately render without any number rather than having one invented.
