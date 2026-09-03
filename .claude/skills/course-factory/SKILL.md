---
name: course-factory
description: "Build and ship a new Aprende IA course end to end — research document → TOML → 30 lessons → videos → live on the platform. Use whenever a new course is requested, a research document lands in studio/research/ or researches/, someone asks to add a topic to the catalog, or a course_requests entry needs fulfilling. Also use when regenerating or repairing an existing course."
---

# Course factory

Turns a research document into a 30-lesson course with videos, quizzes,
exercises, capstones and a portfolio deliverable. Cost: ≈ $0.35 of LLM plus
~2–3 hours of mostly unattended render time.

**The mechanical checks live in code, not here.** `preflight` and `verify` do the
counting; this skill covers the judgment they can't. Never restate what those
commands check — run them.

Read `docs/04-course-factory.md` for the pipeline internals and
`docs/07-engineering-notes.md` before editing anything.

## The five phases

### 1 · Judge the research (the quality ceiling)

**A course is exactly as good as its research document.** This is the only phase
where stopping is cheap, so be honest here.

Run `preflight` first — it catches encoding, length and wiring. Then read enough
of the document to answer:

- **Is it operational?** Steps, numbers, procedures, real cases — or think-piece
  prose? Thirty lessons need thirty concrete things to *do*. Prose yields
  thirty lessons of paraphrase.
- **Is evidence classified?** The house standard tags every claim `[P]` primary /
  `[S]` secondary / `[X]` unverifiable-discard. Adapt the tiers per domain
  (for social theory: the author's own text vs commentary vs popular
  misattribution). A doc without them will smuggle folklore into the course.
- **Does it carry exercise seeds and diagram-ready structures?** The compiler
  generates exercises and Mermaid diagrams from this text. If the research has
  no tables and no artifact ideas, the lessons come out shapeless.
- **Is it dated?** Anything about platforms, regulations or funding instruments
  rots within a year.

If it fails, ask for a better document. Do not generate on top of weak research
and plan to fix it later — 30 lessons of drift cost far more than a rewrite.

### 2 · Author the TOML

`studio/channels/curso-<slug>.toml` is the **single source of truth** for
everything learner-facing. Nobody edits course copy in SQL.

```toml
kind = "course"
name = "<Tema> en 30 días"        # learner-facing title
slug = "curso-<slug>"
niche = "…"                        # THE PROMISE: outcome only, ≤110 chars,
                                   # no "Curso de 30 días:" prefix — the title says it
category = "…"                     # must be in course_factory.CATEGORIES
audience = "…"                     # who it is for; steers generation
tone = "…"                         # the teacher's voice for this subject
cta = "Ahora hazlo tú: …"          # closing line of every video
course_brief = "…"                 # INTERNAL generation spec, never shown
research_file = "<file>.md"
[voice]  # unused Edge TTS voice   [style]  # unused stroke colour, 9:16
```

Two judgment calls preflight can only partly check:

- **Category.** Coarse on purpose. A category with a single course looks broken,
  so add a new one only when at least two courses will sit in it, and add it to
  `CATEGORIES` deliberately.
- **Voice and colour.** Must be unused *by another course*. Pick a voice whose
  accent suits the subject and keep the roster gender-balanced.

### 3 · Name the deliverable, then check the rubric fits

Add a `PROJECT_TEMPLATES` entry in `cloud/writer.py` **before** generating.
Without one the course silently ships the default audit template.

Ask: **what would a client have paid for here?** A strategy, a campaign plan, an
audit, a formulated project, a scouting report. If you cannot name it, the course
has no portfolio payoff and the whole premise of the platform is missing for that
course — resolve it now, not after 30 lessons exist.

**Then check the rubric fits the domain.** Exercises are scored on
**Aplicación 0–40** — *"grounded in YOUR numbers/brand/context, generic caps at
15"*. That is business-shaped. On a conceptual or humanities course it punishes
correct work, which is exactly the category error documented in `docs/02` that
already made a learner's best answer score lower than a weaker one.

Mitigate by framing every exercise around a **concrete object the learner
chooses** — a real dataset, a specific cultural phenomenon, their own club, a
named team — so "grounded in your context" has something real to bite on. Say so
explicitly in `course_brief`. If even that doesn't fit, raise it before
generating rather than discovering it in production.

### 4 · Generate

```bash
# NOT bare `python`: the system interpreter lacks the deps (loguru) and the
# factory needs DATABASE_URL / OPENROUTER_API_KEY / PEXELS_API_KEY. The
# wrapper reads them from Railway and uses the repo's venv.
$F = "powershell -NoProfile -ExecutionPolicy Bypass -File studio/cloud/run_factory.ps1"
$F <slug> preflight   # gate; exits non-zero
$F <slug> all         # runs preflight, then everything
```

`all` runs preflight → syllabus → compile → render → reconcile → backfills →
capstones → verify, and exits non-zero if the result is incomplete. Run it
**detached** — it takes hours. Stage by stage is fine too (`docs/04`).

Everything is idempotent. Re-running is the recovery model, always.

### 5 · Verify, then ship — in this order

```bash
python studio/cloud/course_factory.py <slug> verify
DASHBOARD_TOKEN=… PUBLIC_BASE_URL=… python studio/cloud/upload_videos.py <slug>
python studio/cloud/course_factory.py <slug> verify   # again, after upload
```

> **The ordering hazard.** `reconcile` marks videos in the **shared production
> database**, so the course flips to "available" the moment it runs — before the
> files exist on the volume. Between reconcile and upload, learners meet broken
> players. Upload promptly, and re-run `verify`: it compares DB video count to
> files on disk and tells you when they disagree.

Finally, spot-check one video actually streams:
`HEAD /media/<slug>/<file>?token=…` → 200. And if the course fulfils a
`course_requests` entry, mark it **Disponible** with the slug in the dashboard —
that is what lights up the requester's app.

## Non-negotiables

- **"exit 0" is not verification.** Count rows. A pipeline once logged every step
  as successful while producing zero lessons. That is what `verify` is for.
- **TOML is the source of truth.** After editing one, run `<slug> sync`.
- **Never hardcode secrets.** Read them from Railway at runtime (`docs/05`).
- **Research must be UTF-8.** One stray byte once zeroed an entire course.

## When something breaks

`docs/05-operations.md` has the troubleshooting table. The three you will hit:

| Symptom | Fix |
|---|---|
| Renders stall part-way | Pexels free tier is 200 req/hr. Wait, re-run `render` — idempotent. |
| One lesson fails repeatedly | Reset that node (`status='draft', video_file=NULL`), recompile + render. A fresh script renders fine. |
| Factory dies mid-compile | Railway's public proxy kills long connections; the factory reconnects per lesson. Just re-run. |
