# CLAUDE.md — Rumbo

System map for a fresh session. Read this first; it points to deeper docs and a
queryable code graph so you don't have to grep the whole tree.

**Full product documentation lives in `docs/`** (vision, product, architecture,
course factory, operations runbooks, status/roadmap, engineering notes) — start at
`docs/README.md`; this file stays the operational quick-reference.
**Before your first edit read `docs/07-engineering-notes.md`** — the verification
ritual, tooling traps, and every bug pattern this codebase has already produced,
each stated as a rule.

## Start here if you are new

1. Read this file, then `docs/07` (bug patterns), then `docs/06` (what is actually
   true right now, which should drive what you work on).
2. **Verify before you trust.** This file is a snapshot; the database and Railway
   are the truth. `railway variables --kv`, and query Postgres — do not assume a
   count in any doc is current.
3. **"Exit 0" is not verification.** After any batch operation, count rows. After
   any deploy, fetch the live URL and assert the change is present.

## What this is  *(verified 2026-08-25)*

**One engine, two products**, both in Spanish for LatAm:

1. **Rumbo — the learning platform.** **LIVE and the whole focus.**
   **14 courses · 420 lessons · 420 videos.** Deep docs: `docs/`.
2. **Social content factory** (`studio/channels/*.toml`, 4 channels) — short-form
   video + auto-publishing. **Built, DORMANT since July** (scheduler off, no
   Upload-Post credentials). Deep doc: `studio/README.md`.

> **The name.** The product was built as *Aprende IA*; it is being renamed
> **Rumbo**. Docs and the public repo say Rumbo. The **running app, its URL, the
> email templates and the launch video still say Aprende IA** — rebranding a live
> UI is a deliberate, separate change. Expect that mismatch; it is intentional.

### The learner product in one paragraph

A learner says **what they want to be** — pastes a real job posting, or just names
a role — and the platform returns a **route**: which modules, in what order, plus
an honest list of what the job needs and we **don't** teach. They pick one real
**transversal project** every exercise builds on. Each lesson is a 45–60 s video
(the why) + a written guide (the how) + explain-it-back + quiz + an exercise where
they paste actual work. An AI tutor scores work products on three dimensions,
names what's missing to reach 100, allows unlimited retries keeping the best, and
asks one ownership question only the person who did the work can answer. Their
submissions compile into a **work document** under their byline — not a certificate.

### The thesis, and where it actually stands

Generating courses is a commodity; **verifying learning and composing the path** is
the defensible half (`docs/01`, `docs/09`). The machinery is complete and heavily
hardened. **The evidence is not: 5 learners, 16 submissions, nobody has completed a
lesson 2.** Weigh every roadmap decision against that (`docs/06`). Do not mistake
shipped features for traction — this project's documented failure mode is building
roughly seventy times faster than it learns.

### The pieces, and which doc owns each

| Piece | Where |
|---|---|
| Goal engine: posting *or* role → prereq-aware module route, honest gaps | `docs/08` |
| Route-aware access, goal documents, the "quiero ser X" north star | `docs/09` |
| CV intake: proposed module skips, credited only by a passed reto | `docs/10` |
| The public landing: a real lesson for strangers, and its demo endpoints | `docs/11` |
| Lesson loop, rubrics, verdicts vs scores, the prediction beat | `docs/02` |
| Schema (20 tables), API surface, request flows, **security controls** | `docs/03` |
| Course factory pipeline + the authoring standard | `docs/04`, `.claude/skills/course-factory/` |
| Runbooks (deploy, ship a course, **turn on email**, invites, backups) | `docs/05` |
| **Bug patterns and the verification ritual — read before editing** | `docs/07` |

## Repo layout

- `studio/` — **our system.**
  - `cloud/` — `db.py` (schema + every helper), `writer.py` (**every LLM call**),
    `course_factory.py`, `check_job_matcher.py` (matcher calibration),
    `check_tutor.py` (**tutor calibration**), `upload_videos.py`, `invites.py`,
    `backup_db.py`, `producer/publisher/scheduler.py` (dormant), `entrypoint.py`.
  - `dashboard/` — `app.py` (admin API + token gate + share pages),
    `learn_routes.py` (**the entire learner API**), `admin_paths.py` (the admin
    allowlist predicate), `prerender.py` (**server-rendered bodies for the public
    surfaces** — both are dependency-free so they can be audited and tested under
    any interpreter), `check_job_render.js` + `check_how_section.js` (**frontend
    checks — no bundler, no test runner**),
    `static/{index,learn,doc,caso,ruta}.html`.
  - `channels/*.toml` — course profiles. **Single source of truth** for learner copy.
  - `research/*.md` — grounding material for generation. `fixtures/` — matcher fixtures.
  - `output/`, `queue/` — rendered videos and render queue (**git-ignored**).
- `MoneyPrinterTurbo/` — upstream render engine, a clean clone (**git-ignored**, 45 GB).
- `brag-output/` — the launch video, its plan, and the Hyperframes composition.
- Published at **https://github.com/JtPerez-Acle/rumbo** (public, source-available;
  see `LICENSE` — evaluation only, not open source). `.gitignore` excludes the
  upstream clone, rendered videos, and `backups/` (**real learner data**).

## Infrastructure (Railway project `estudio-ia`)

- Project `8a2e90fe-e597-45d4-92c0-f274ece96af6`, service `estudio`, Postgres addon,
  volume at `/app/studio/output`.
- **Learner app:** https://estudio-production-1b8c.up.railway.app/aprende
- **Admin dashboard:** same host `/panel` — gated by `DASHBOARD_TOKEN`.
- **Public site:** the root `/` (docs/11). It used to 401: the dashboard held
  the most valuable URL in the product and served it to an audience of one.
- **Secrets are NOT in this repo.** Read at runtime: `railway variables --kv`, and
  `railway variables --service Postgres --kv` (`DATABASE_PUBLIC_URL` is how a local
  script reaches the cloud DB). Never hardcode keys, tokens, or invite codes.
- Model: `LLM_MODEL=deepseek/deepseek-v4-pro` via OpenRouter. Pennies per script.

## Common tasks

```bash
# Local dev server against the CLOUD db:
powershell -NoProfile -ExecutionPolicy Bypass -File studio/dashboard/run_local.ps1
# → http://localhost:8799/aprende

# Deploy. The CLI often reports a timeout AFTER a successful upload — check
# `railway deployment list` before retrying, then verify by fetching the live URL.
railway up --detach

# Add a course (judgment lives in .claude/skills/course-factory/):
python studio/cloud/course_factory.py <slug> preflight   # validate BEFORE burning hours
python studio/cloud/course_factory.py <slug> all         # gated by preflight, ends in verify
python studio/cloud/course_factory.py <slug> verify      # counts rows; non-zero if incomplete
python studio/cloud/course_factory.py <slug> backfill-written    # written guide + diagrams
python studio/cloud/course_factory.py <slug> check-narration     # page-only devices in scripts
DASHBOARD_TOKEN=… PUBLIC_BASE_URL=… python studio/cloud/upload_videos.py <slug>

# Checks — run the relevant one BEFORE deploying a change to that area:
python studio/cloud/check_job_matcher.py    # matcher, 5 fixtures, ~15 min (real LLM)
python studio/cloud/check_tutor.py          # tutor, 6 properties, ~5 min (real LLM)
python studio/cloud/check_cv_matcher.py     # CV matcher; reads REAL CVs from ./cvs (git-ignored)
python studio/cloud/check_public_surface.py [base_url]   # HTTP: public routes + every admin gate
node studio/dashboard/check_job_render.js studio/dashboard/static/learn.html \
     studio/fixtures/job-postings/sample-analysis.json
node studio/dashboard/check_how_section.js
node studio/dashboard/check_cv_render.js studio/dashboard/static/learn.html
node studio/dashboard/check_demo_render.js studio/dashboard/static/learn.html

# Offsite backup (all 20 tables) — before anything risky:
DATABASE_URL=$DB python studio/cloud/backup_db.py --keep 14
```

## Live operational state you must know

- **Email WORKS as of 2026-08-31.** The domain is **`ponrumbo.com`** (registered
  through Railway, DNS managed there, sending region **São Paulo / sa-east-1** —
  keep it, it is the right region for LatAm receivers). Resend verified, DKIM +
  SPF-by-CNAME + DMARC `p=none` in place, `EMAIL_FROM=Rumbo <hola@ponrumbo.com>`.
  A real magic link was sent and received. This was the #1 blocker for a month;
  it is gone. *(The old note said `aprende-ia.app` needed verifying — that domain
  was never registered at all, which is why the runbook never worked.)*
- **The magic link lives 60 minutes** (`LOGIN_TOKEN_TTL_MIN`), and the email
  **states the duration, reading it from that constant**. Never hardcode the
  number in the copy. Two token paths exist and only the first sends mail:
  self-service login (`learn_routes.py`, `LOGIN_TOKEN_TTL_MIN`, emailed) and the
  operator-minted link (`app.py`, 24 h, returned to the dashboard, not emailed).
- **`ponrumbo.com` has no inbound MX** — nobody can reply to a Rumbo email. The
  footer says so. Adding a real inbox is a decision, not an oversight.
- **Returning-user login is deliberately restricted.** An existing account cannot
  be entered without proving inbox control — self-service re-login returns **409**
  and queues the learner. This closed a live account-takeover hole; do not "fix" it
  by handing the magic link back to the caller.
- **`ENABLE_SCHEDULER=0`** — the social channels are off.
- The **demand ledger** (`GET /api/demand`, admin) aggregates every analysis's gaps
  and reports how many library modules no route has ever selected. It exists to
  stop course #15 being built on intuition; `build_candidates` only populates past
  `GAP_BUILD_THRESHOLD` (default 3).

## Gotchas learned the hard way

- **The Railway CLI is a global npm package, so `nvm use` can vanish it.** Switching
  Node versions moves the global dir and `railway` drops off PATH — every runbook
  breaks with `command not found`. Fix: `npm i -g @railway/cli` under the current
  Node. (Node 22+ is required by the `/brag` video toolchain; the CLI was installed
  under Node 20.)
- **`db.connect()` forces `client_encoding=utf-8`** — Windows locale otherwise
  double-encodes accents on the wire. Keep it.
- **`course_factory` reconnects to Postgres per lesson** — a long-held connection
  dies over Railway's public proxy during ~30-min runs.
- **Pexels free tier = 200 req/hr** → >~30 videos needs multiple passes; the queue
  is idempotent, re-run `render`.
- **The render queue gets `writer.narration_text(script)`, not the raw script.** One
  string cannot serve a reader and a voice: a script teaching with fill-in-the-blanks
  reads fine and narrates as "guion bajo, guion bajo". `transcript` keeps the
  readable form. `check-narration` fails the build on unrendered lessons that still
  contain page-only devices.
- **New renders default to 1080p ~4 Mbps (≈18 MB/lesson).** The catalog is 720p/CRF27
  (~5 MB). Always shrink before uploading — the 5 GB volume filled once already
  (`docs/05` → shrink flow).
- **A CV is a claim, and claims do not grant access** (`docs/10`). CV intake
  produces *proposals*; only passing a module's reto (≥`EXEMPTION_PASS_SCORE`)
  credits it. Exemptions live in `module_exemptions`, never in `progress` —
  writing fake completions would corrupt the streak, the SM-2 ladder and the
  Module-1 gate. `_accessible_for` is the one place access is computed and every
  widener there only ever ADDS: **skipped is not locked.**
- **Real CVs never enter the repo.** `.gitignore` blocks `*.pdf` and `cvs/`;
  this repo is public and those are other people's names and employment history.
- **Admin routes are gated by an ALLOWLIST** in `studio/dashboard/admin_paths.py`.
  A new `/api/*` route not added to it ships **public**. Add the prefix in the
  same edit as the route, add a row to `check_public_surface.py`'s audit, and
  curl it tokenless before deploying. The gate also **fails closed** in
  production if `DASHBOARD_TOKEN` is unset. The predicate lives in its own
  dependency-free module so the audit runs under any Python — it used to live in
  `app.py`, and a checker run under an interpreter without FastAPI silently
  skipped all 25 assertions while still printing a mostly-passing score.
- **Course TOML = single source of truth for learner-facing copy.** `name` (no
  duration claim), `niche` (≤110 chars), `category` (in `course_factory.CATEGORIES`),
  `course_brief` (internal). After editing a TOML run `<slug> sync`. Never hand-patch
  `courses` rows in SQL.
- **`_chat` sends `max_tokens: 16000`** — deepseek-v4-pro is a reasoning model and
  reasoning shares that budget. Empty `content` is retried, not crashed.
- **Every learner-authored string reaching a model goes through `writer._fenced()`**
  and the system prompt carries `UNTRUSTED_RULE`. Without it a submission could
  dictate its own grade — verified at 100/100 on garbage before the fix.
- **Untrusted Markdown renders through `renderMD()`** (marked → DOMPurify), never
  straight to `innerHTML`. That was a stored-XSS sink on the public paper pages.
- **Portfolio compilers only see real work** (`MIN_PORTFOLIO_SCORE`, 3 distinct
  items). Fed a non-attempt they do not produce a short document — they **fabricate**.

## Comprehending the code

Run `/graphify .` (skill installed) or query the prebuilt graph:
`graphify query "..."`, `graphify explain "X"`, `graphify god-nodes`. Report:
`graphify-out/GRAPH_REPORT.md`.

**The checked-in graph is stale — regenerate before trusting it.** It was built
**2026-08-05** (171 nodes, 395 edges) and therefore predates CV intake,
`admin_paths.py`, the public-surface restructure and the Rumbo rename: roughly
4,500 lines of the current tree are invisible to it, including the security
predicate the whole admin gate rests on. Run `/graphify .` first, then query.
Once regenerated it is still the faster way in than grepping.

## gstack

**All web browsing goes through the `/browse` skill from gstack. Never use the
`mcp__claude-in-chrome__*` tools.** `/browse` drives a headless Chromium built at
`~/.claude/skills/gstack/browse/dist/browse.exe` and is the only sanctioned
browsing path in this repo — for QA, dogfooding the live site, and reading docs.

Installed at `~/.claude/skills/gstack` (v1.77.0.0, solo install, short names).
**Windows installs by file copy, so re-run `~/.claude/skills/gstack/setup` after
every `git pull` of gstack** or the skill files go stale. `/gstack-upgrade` does
both.

Available skills:

| | |
|---|---|
| Planning | `/office-hours` `/autoplan` `/plan-ceo-review` `/plan-eng-review` `/plan-design-review` `/plan-devex-review` |
| Design | `/design-consultation` `/design-shotgun` `/design-html` `/design-review` |
| Ship | `/review` `/ship` `/land-and-deploy` `/canary` `/benchmark` |
| Browser | `/browse` `/qa` `/qa-only` `/connect-chrome` `/setup-browser-cookies` |
| Diagnose | `/investigate` `/retro` `/devex-review` `/cso` |
| Docs | `/document-release` `/document-generate` `/learn` |
| Safety | `/careful` `/freeze` `/guard` `/unfreeze` |
| Setup | `/setup-deploy` `/setup-gbrain` `/gstack-upgrade` `/codex` |

`/connect-chrome` and `/open-gstack-browser` are the same thing under two names:
they launch GStack Browser, an AI-controlled Chromium with the sidebar extension.
Use them (or `/pair-agent`) when a task genuinely needs a real, logged-in browser
rather than the headless `/browse` session; `/setup-browser-cookies` imports your
Chromium cookies into the headless session and usually removes the need.

The install also registers skills this list does not cover — `/spec`, `/scrape`,
`/diagram`, `/health`, `/make-pdf`, `/context-save`, `/context-restore`,
`/skillify`, `/plan-tune`, `/landing-report`, `/benchmark-models`, and the
`/ios-*` family. Run `/gstack` for the router.
