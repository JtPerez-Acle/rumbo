# CLAUDE.md — Estudio IA / Rumbo

System map for a fresh session. Read this first; it points to deeper docs and a
queryable code graph so you don't have to grep the whole tree.

**Full product documentation lives in `docs/`** (vision, product, architecture,
course factory, operations runbooks, status/roadmap, engineering notes) — start at
`docs/README.md`; this file stays the operational quick-reference.
**Before your first edit read `docs/07-engineering-notes.md`** — verification
ritual, tooling traps and the bug patterns this codebase has already produced.

## What this is  *(current state — 2026-08-12)*

**One AI engine, two products**, both in Spanish for LatAm:

1. **Rumbo — the learning platform.** **LIVE and the whole focus.**
   **14 courses · 420 lessons · 420 videos.** Deep docs: `docs/`.
2. **Social content factory** (`studio/channels/*.toml`, 4 channels) — short-form video
   + auto-publishing. **Built, DORMANT since July** (scheduler off, no Upload-Post
   credentials, only 7 clips ever rendered). Deep doc: `studio/README.md`.

### The learner product in one paragraph

A learner says **what they want to be** — pastes a real job posting, or just names a role
— and the platform returns a **route**: which courses, which *modules* of each, in what
order, plus an honest list of what the job needs and we **don't** teach. They pick one real
**transversal project** (their business, or a brand they want to work for) that every
exercise builds on. Each lesson is a 45–60 s video (the why) + a written guide (the how) +
explain-it-back + quiz + an exercise where they paste actual work. An AI tutor scores work
products on three dimensions, names what's missing to reach 100, allows unlimited retries
keeping the best, and asks one ownership question only the person who did the work can
answer. At the end their real submissions compile into a **work document** under their
byline — the deliverable a client would have paid for, not a certificate.

### The thesis, and where it actually stands

Generating courses is a commodity; **verifying learning and composing the path** is the
defensible half (`docs/01`, `docs/09`). The machinery is complete. **The evidence is not:
~1 real learner, 13 submissions, 0 strangers have completed lesson 1.** Every roadmap
decision should be weighed against that (`docs/06`). Do not mistake shipped features for
traction.

### The pieces, and which doc owns each

| Piece | Where |
|---|---|
| Goal engine: posting *or* role → prereq-aware module route, honest gaps | `docs/08` |
| Route-aware access, goal documents, the "quiero ser X" north star | `docs/09` |
| Lesson loop, rubrics, why verdicts vs scores | `docs/02` |
| Schema (17 tables), API surface, request flows | `docs/03` |
| Course factory pipeline + the authoring standard | `docs/04`, `.claude/skills/course-factory/` |
| Runbooks (deploy, ship a course, invites, backups, video weight) | `docs/05` |
| **Bug patterns and the verification ritual — read before editing** | `docs/07` |

Cross-session state lives in the auto-memory at
`~/.claude/projects/.../memory/` (`spanish-ai-shorts-business.md`,
`world-of-knowledge-vision.md`, `success-gates-unmeasurable.md`).

## Repo layout

- `studio/` — **our system.** Everything below is here.
  - `cloud/` — `db.py` (Postgres schema + every helper), `writer.py` (**every LLM call**:
    generation, evaluation, the job matcher, both document compilers, `VOICE_GUIDE`),
    `course_factory.py` (`<slug> preflight|all|syllabus|compile|render|reconcile|capstones|
    backfill-*|sync|verify`), `check_job_matcher.py` (**5-fixture matcher calibration**),
    `upload_videos.py`, `invites.py`, `backup_db.py`, `reset_course.py`,
    `producer/publisher/scheduler.py` (dormant channels), `entrypoint.py` (container boot).
  - `dashboard/` — `app.py` (FastAPI: admin API + token gate + share pages),
    `learn_routes.py` (**the entire learner API** `/api/learn/*`), `check_job_render.js` +
    `check_how_section.js` (**frontend checks — no bundler, no test runner**),
    `run_local.ps1` (local dev server), `static/{index,learn,doc,caso,ruta}.html`.
  - `fixtures/job-postings/` — real job postings + expected shapes for the matcher suite.
  - `channels/*.toml` — channel/course profiles. `kind="course"` marks a course (has
    `course_brief`, optional `research_file`). Social channels have `publish_slot`.
  - `research/*.md` — source material injected into course generation (grounding).
  - `output/<slug>/*.mp4` + `.json` — rendered videos (the Railway volume in prod).
  - `queue/pending|done/*.json` — render queue.
- `MoneyPrinterTurbo/` — **upstream video engine (git clone).** Kept clean for `git pull`.
  `generate_batch.py` (in `studio/`) drives its `cli.py`. Don't edit upstream unless needed.
- `Dockerfile` (repo root) — builds MPT + studio into one image for Railway.
- `graphify-out/` — queryable code knowledge graph (see "Comprehending the code" below).

## Infrastructure (Railway project `estudio-ia`)

- Project id `8a2e90fe-e597-45d4-92c0-f274ece96af6`, service `estudio`, + Postgres addon,
  + volume mounted at `/app/studio/output`.
- **Learner app (LIVE):** https://estudio-production-1b8c.up.railway.app/aprende
- **Admin dashboard:** same host `/` — gated by `DASHBOARD_TOKEN`.
- **Secrets are NOT in this repo.** Read them at runtime:
  `railway variables --kv` (service `estudio`) and `railway variables --service Postgres --kv`
  (the `DATABASE_PUBLIC_URL` proxy is how you reach the cloud DB from a local script).
  Local Pexels key is in `MoneyPrinterTurbo/config.toml`. Never hardcode keys/tokens/codes.
- Model: `LLM_MODEL=deepseek/deepseek-v4-pro` via OpenRouter (OpenAI-compatible). Scripts
  cost pennies. Anthropic SDK is NOT used for generation — it's OpenRouter chat completions.

## Common tasks

```bash
# Local dev server against the CLOUD db (reads Railway secrets itself; honours $PORT):
powershell -NoProfile -ExecutionPolicy Bypass -File studio/dashboard/run_local.ps1
# → http://localhost:8799/aprende   (or use preview_start with the "learner-app" config)

# Deploy (from repo root). The CLI often reports a timeout AFTER a successful upload —
# check `list-deployments` before retrying, and verify by fetching the live URL.
railway up --detach

# Add a course: research → studio/research/<file>.md, then channels/curso-<slug>.toml.
# The skill (.claude/skills/course-factory/) covers the judgment; these are the mechanics:
python studio/cloud/course_factory.py <slug> preflight   # validate BEFORE burning hours
python studio/cloud/course_factory.py <slug> all         # gated by preflight, ends in verify
python studio/cloud/course_factory.py <slug> verify      # counts rows; non-zero if incomplete
DASHBOARD_TOKEN=… PUBLIC_BASE_URL=… python studio/cloud/upload_videos.py <slug>

# Checks — run the relevant one before deploying a change to that area:
python studio/cloud/check_job_matcher.py                 # matcher, 5 fixtures, ~15 min (real LLM)
python studio/cloud/check_tutor.py                       # TUTOR calibration, 6 cases, ~5 min (real LLM)
node studio/dashboard/check_job_render.js studio/dashboard/static/learn.html \
     studio/fixtures/job-postings/sample-analysis.json   # result page renders
node studio/dashboard/check_how_section.js               # landing promises haven't gone stale

# Invite codes: the dashboard now has a panel (create, copy link, see who redeemed).
python studio/cloud/invites.py create "Label" 3          # CLI still works

# Offsite backup (all 17 tables) — before anything risky:
DATABASE_URL=$DB python studio/cloud/backup_db.py --keep 14
```

## Gotchas learned the hard way

- **`db.connect()` forces `client_encoding=utf-8`** — Windows locale otherwise double-encodes
  accents on the wire (data itself is always valid UTF-8). Keep it.
- **`course_factory` reconnects to Postgres per lesson** — a long-held connection dies over
  Railway's public proxy during ~30-min runs. `writer._chat` retries transient OpenRouter drops.
- **Single-lesson render failures** (rare upstream edge case, script-stage): reset the node
  (`status='draft', video_file=NULL`), recompile+render — a fresh script renders fine.
- **Pexels free tier = 200 req/hr** → rendering >~30 videos needs multiple passes; the queue
  is idempotent, re-run `render`.
- **Learner auth is invite-gated**: `/login` needs a valid code (no email provider yet, so the
  code gates every login; add `RESEND_API_KEY` to switch returning users to emailed magic links).
  Rate-limited per IP + honeypot. Active users stay in via a 90-day session cookie.
- **Course availability** is computed from rendered video count, so a course shows
  "Próximamente" until its videos are on the volume. Lessons without video show as "en producción".
- **`.hide{display:none!important}`** in learn.html — inline `display` styles otherwise beat the class.
- **Course TOML = single source of truth for learner-facing copy**: `name` (title — **no
  duration claim**; preflight rejects "en 30 días" because a route may use only part of a
  course), `niche` (outcome promise, ≤110 chars), `category` (must be in
  `course_factory.CATEGORIES`), `course_brief` (internal, generation only). `ensure_course`
  upserts on every factory command; after editing a TOML run `course_factory.py <slug> sync`.
  Never hand-patch `courses` rows in SQL.
- **Admin routes are gated by an ALLOWLIST** in `app._is_admin_path`. Adding an `/api/*`
  admin route and forgetting to list it ships it **public** — this nearly happened twice in
  one day (`delete-media`, and `invites`, which would have published every access code).
  Add the prefix in the same edit as the route.
- **Videos are 720p/CRF27 (~5 MB/lesson)**, re-encoded 2026-08-12. The 5 GB volume filled at
  7 Mbps and mobile data is a real cost in LatAm. Railway volume resize is **dashboard-only**
  — no public API mutation exists, and the MCP agent reports success while only staging
  config. Keep new renders at this weight (`shrink` flow in `docs/05`).
- **`_chat` sends `max_tokens: 16000`** because deepseek-v4-pro is a *reasoning* model and
  reasoning shares that budget (~5.3 k on a long prompt). Empty `content` is retried, not
  crashed.
- **Portfolio compilers only see real work** (`MIN_PORTFOLIO_SCORE`, ≥3 submissions). Fed a
  non-attempt they don't produce a short document — they **fabricate**. See `docs/07`.

## Comprehending the code

Run `/graphify .` (skill installed) or query the prebuilt graph:
`graphify query "..."`, `graphify explain "X"`, `graphify god-nodes`. Report:
`graphify-out/GRAPH_REPORT.md`. Prefer this over grepping the tree.
