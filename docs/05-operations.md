# 05 — Operations: runbooks

Everything here assumes the operator machine (Windows, repo at
`C:\Users\joset\Projects\MoneyPrinterTurbo`, Railway CLI linked) and reads secrets
at runtime from Railway. **Never hardcode keys, tokens, or invite codes.**

## Secrets & environment

```bash
railway variables --kv                      # service env (OPENROUTER_API_KEY, LLM_MODEL,
                                            # DASHBOARD_TOKEN, PEXELS_API_KEY, …)
railway variables --service Postgres --kv   # DATABASE_PUBLIC_URL = cloud DB from local scripts
```

| Variable | Purpose | Notes |
|---|---|---|
| `DATABASE_URL` | Postgres | container uses internal ref; local scripts use the PUBLIC proxy URL |
| `OPENROUTER_API_KEY` / `LLM_MODEL` | all generation & evaluation | `deepseek/deepseek-v4-pro` |
| `DASHBOARD_TOKEN` | admin gate | append `?token=` once; cookie persists |
| `PEXELS_API_KEY` | stock footage | free tier: 200 req/hr |
| `ENABLE_SCHEDULER` | social channel crons | **0 (off)** until Upload-Post connected |
| `EVAL_RATE_MAX` / `EVAL_RATE_WINDOW` | evaluation rate limit | default **60/hr** per learner |
| `MIN_CASE_STUDY_SUBMISSIONS` | portfolio unlock threshold | default 3 |
| `RESEND_API_KEY` / `EMAIL_FROM` | email magic links | **unset** — returning learners get a 409 and queue in *Esperando acceso* until set. See the runbook above. |
| `MAX_OPEN_REQUESTS` | concierge requests per learner | default 3 |
| `MODULE_GATE_DAYS` | module time-gate | **not implemented** — design parked, see doc 06 |

## Runbook: local development

```bash
# Learner app against the cloud DB (uvicorn on :8799):
DB=$(railway variables --service Postgres --kv | grep DATABASE_PUBLIC_URL= | sed 's/.*=//')
DATABASE_URL="$DB" PYTHONIOENCODING=utf-8 \
  MoneyPrinterTurbo/.venv/Scripts/python.exe -m uvicorn app:app --port 8799 --app-dir studio/dashboard
# → http://localhost:8799/aprende   (admin at / — token gate off when DASHBOARD_TOKEN unset)
```

For AI evaluations locally, also export `OPENROUTER_API_KEY` and `LLM_MODEL` from
the service env. **Caution:** local runs point at the PRODUCTION database.
Create test data under clearly-fake emails and delete it when done
(`submissions`, `progress`, `learner_sessions`, `login_tokens`, `project_docs`,
`case_studies`, then the `learners` row, then the invite).

## Runbook: deploy

```bash
railway up --detach     # from repo root; ~200MB upload, image builds in ~2 min
```

- The CLI **frequently times out during upload while the upload actually
  succeeded**. Before retrying, check whether a new deployment appeared
  (Railway dashboard or MCP `list-deployments`). Duplicate uploads are harmless —
  Railway supersedes older builds — but don't stack them blindly.
- `db.init_db()` runs on container boot: schema + additive migrations apply
  automatically. New columns/tables ship as `IF NOT EXISTS` statements in `db.py`.
- Post-deploy check: `GET /aprende` → 200, deploy logs show `postgres schema ready`
  (uvicorn's INFO lines appear at "error" severity in Railway logs — that's just
  stderr, not a problem).

## Runbook: create & ship a new course

1. Obtain the research document (deep-research run or in-session, web-grounded).
   Standards in doc 04. Save as `studio/research/<topic>.md` — **UTF-8**.
2. Create `channels/curso-<slug>.toml` (copy an existing course profile; set
   name/niche/audience/tone/brief/research_file, pick an unused voice+color).
3. Run the pipeline (detached for long runs):
   `course_factory.py <slug> all` — or stage by stage per doc 04.
4. **Verify by counting, not by exit codes:** every lesson row should have video,
   module description, explain prompt; capstones = 5:
   lessons=30 / video=30 / moddesc=30 / explain=30 / retos=5.
5. Upload videos: `DASHBOARD_TOKEN=… PUBLIC_BASE_URL=… python studio/cloud/upload_videos.py <slug>`.
   ⚠️ Reconcile marks videos in the **shared** DB, so the course shows "available"
   in production the moment reconcile runs — upload promptly after reconciling,
   or learners meet broken players.
6. Spot-check a video streams: `HEAD /media/<slug>/<file>?token=…` → 200.
7. If the course fulfills a concierge request: mark it **Disponible** with the
   course slug in the dashboard — the requester's app lights up.

## Runbook: keep videos light (and why the volume filled)

Videos render at ~7 Mbps by default — **19–50 MB per 50-second lesson**. That
filled the 5 GB volume on 2026-08-12 and costs a LatAm learner real mobile data.
Every course is now re-encoded to **720×1280 / CRF 27 (~5 MB per lesson)**; the
whole 420-video catalog is 2.3 GB.

```bash
ffmpeg -y -i "$f" -vf scale=720:1280 -c:v libx264 -crf 27 -preset veryfast \
  -c:a copy -movflags +faststart "$f.tmp.mp4"   # then verify duration, then swap
```

Do this for any newly rendered course before it accumulates. Check duration
matches within 1 s before replacing, keep originals as `*.mp4orig` (not `.mp4`,
which `verify` globs), and cap `-threads` if a render is running.

> **Railway volume resize is dashboard-only.** There is no resize mutation in the
> public GraphQL API (introspected), and the Railway MCP agent will report a
> successful resize while only staging config that never applies. If space runs
> out, shrink what you store or resize by hand in the dashboard.

Uploads stream the raw body to `.part` then `os.replace`, so a failed upload can
no longer truncate a good file — it did, zeroing 20 videos, before that fix.
**Verify uploads by SIZE, not status code:** 20 of those returned HTTP 200 while
serving 0 bytes.

## Runbook: invite a learner

**Use the dashboard.** *Códigos de invitación* (above Alumnos) lists every code
with its usage, a status chip, **the names of everyone who redeemed it**, a
one-tap "Copiar enlace", and a deactivate toggle that revokes without deleting
(the audit trail survives). A form below mints new ones. Usable codes sort first.

Multi-use codes are fine now that the panel shows who redeemed each one — you
keep attribution without minting one code per person.

```bash
# The CLI still works for scripted use:
DATABASE_URL=$DB python studio/cloud/invites.py create "Label" 3
python studio/cloud/invites.py list | purge-test
```

Until `RESEND_API_KEY` is set, **the code gates EVERY login, not just the first**
— recipients must keep the link, and deactivating a code locks out everyone who
joined with it. That scales badly the moment you share a multi-use code widely;
it is the strongest argument for setting that key (`docs/06`).

## Runbook: backups

Railway's managed Postgres includes automatic backups; per Railway's own
defense-in-depth guidance we keep an operator-controlled copy **outside**
Railway as well. Videos are re-renderable — the database is the only
irreplaceable data.

```bash
DATABASE_URL=$DB python studio/cloud/backup_db.py --keep 14
# → backups/aprende-<utc-stamp>.json.gz (all learner work + course content)
```

Run it weekly (or before any risky operation). The export is plain
table→rows JSON — restorable by hand with any JSON tool; it is a lifeboat,
not a migration system.

## Runbook: turn on email (the cohort blocker)

Until `RESEND_API_KEY` is set, **a returning learner cannot let themselves back
in** — closing the account-takeover hole (docs/07) means an existing account can
only be entered by proving inbox control. They get a 409, land in the
**Esperando acceso** panel, and wait for you to send a link by hand. That is fine
for four alpha users and it does not survive a cohort.

Everything on our side is already wired; this is the whole change:

1. Create the Resend account and add the sending domain (`aprende-ia.app` or
   whichever you use). **This is yours to do — it needs your account.**
2. Add Resend's DNS records to the domain and wait for verification. An
   unverified domain is the most common cause of "the key is set and nothing
   arrives".
3. `railway variables --set RESEND_API_KEY=re_…` on service `estudio`.
   Set `EMAIL_FROM` too if the address is not `Aprende IA <hola@aprende-ia.app>`
   — it must be **on the verified domain** or Resend rejects every send.
4. Verify by locking yourself out: log in with an email that already exists.
   Before: 409 + a row in *Esperando acceso*. After: `{"sent": true}` and a real
   email. **Check the inbox, not the status code** — that distinction is the
   whole point of the next paragraph.

`_send_email` now checks the response and returns whether delivery was accepted.
A failure is logged with Resend's own reason (`resend send failed [403] …`) and
the learner is queued instead of being told to check an inbox that will stay
empty. So the *Esperando acceso* panel doubles as the email health check: it
should sit at zero once the key is live, and anything appearing there afterwards
means delivery is broken.

## Runbook: a learner is locked out

Dashboard → **Alumnos** → "🔗 Enlace de acceso" next to the learner: mints a
24-hour magic link and copies it to the clipboard — send it over WhatsApp or
email. No invite code needed. (This is the manual bridge until
`RESEND_API_KEY` automates returning-user login.)

## Runbook: read learner work (do this weekly)

Dashboard → **Alumnos** → **📖 Leer su trabajo**. You get the learner's whole
journey in chronological order: their actual text, the verdict or score with its
dimensions, the tutor's feedback, misconceptions, gap lists, conversation Q&A
with attempts, their documents and course requests. Retries appear in sequence,
so you watch them improve.

Flag any evaluation the tutor got wrong (**⚑ Evaluación incorrecta** + a note).
Those flags are the labelled set for tuning the evaluator prompts — without
them, reading only produces impressions.

At alpha scale this is *100% of the product's real usage* and takes about
fifteen minutes. It is the highest-signal activity available, and it stops being
possible around 50 learners.

## Runbook: changing how the tutor judges

Anything touching `writer.py`'s evaluation prompts:

0. **Run the calibration suite first, and again after:**
   `DATABASE_URL=… OPENROUTER_API_KEY=… LLM_MODEL=… python studio/cloud/check_tutor.py`
   Six cases, ~5 minutes, exits non-zero on failure. It asserts the three
   properties the product's promise rests on — identical work scores the same
   (STABLE), better work scores higher (ORDERED), and restoring what the rubric
   rewards actually raises the score (ACTIONABLE) — plus the floor that keeps
   non-attempts out of compiled documents.
1. Bump `RUBRIC_VERSION` if the scoring contract changes.
2. Re-run the changed evaluator **against real learner submissions** (the suite
   pulls them live from `submissions` — never invent your own test cases; that is
   exactly how the last rubric bug survived).
3. Include a degenerate input (empty-ish, lazy, off-task) and confirm it scores
   badly — leniency leaks are invisible otherwise.
4. Restart the preview server before testing (Python edits are not hot-reloaded).
5. Check the learner-visible result end to end, not just the JSON.

## Runbook: concierge triage

Dashboard → *Solicitudes de cursos*. Statuses: Recibida → En revisión →
En producción → **Disponible** (requires the course slug — that's what links the
request to the temario in the learner's app) or Descartada. The request log is the
demand signal: build what accumulates.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Course shows "available" but videos 404 | reconcile ran before upload | run `upload_videos.py <slug>` |
| Single lesson render fails repeatedly | upstream script-stage edge case | reset node to draft + NULL video_file, recompile+render |
| Renders stall mid-course | Pexels 200/hr exhausted | wait for the hour; re-run `render` (idempotent) |
| Pipeline "done" but course empty | a step crashed and the runner moved on | check the step's log; **verify with row counts**; re-run (idempotent) |
| Accented text garbled in a terminal | Windows console encoding | set `PYTHONIOENCODING=utf-8`; data in DB is fine |
| Factory dies mid-compile over proxy | long-held connection killed | already handled (per-lesson reconnect); just re-run |
| Learner completion "didn't count" | pre-fix client forced review mode | fixed **server-side 2026-08-12**: `/complete` ignores the client's `is_review` and derives it from `completed_at` |
| 429 on login | per-IP rate limit (8/5min) | wait; it protects the invite gate |
| 429 on submitting work | per-learner evaluation limit | `EVAL_RATE_MAX` (default 60/h); in-memory, resets on redeploy |
| Local edits seem to do nothing | preview server was reused, no hot reload | `preview_stop` then `preview_start` — see doc 07 |
| Authed API test returns "no autenticado" | PowerShell strips the Cookie header | use `curl.exe -H "Cookie: learner_session=…"` |
| Deploy command times out | Railway CLI flakiness | the upload usually landed — check `list-deployments` before retrying |

## Verification culture

The house rule, earned from a silent failure: **"exit 0" is not verification.**
After any batch operation, count what exists — rows in the database, files on the
volume, HTTP 200s on real URLs. Every runbook above ends with a check for this
reason, and any new automation should too.
