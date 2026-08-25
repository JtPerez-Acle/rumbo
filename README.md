# Aprende IA

**Tell it what you want to be. It compiles the route, verifies you learned it, and
hands you the work document that proves it.**

A Spanish-language learning platform for Latin America. Paste a real job posting —
or just name the role — and the system matches it against a library of 70 module
contracts, returns a prerequisite-closed study route, and states plainly which of
the job's demands it *cannot* teach you. You then do real work against your own
business or brand; an AI tutor evaluates it on three dimensions and asks one
question only the person who did the work can answer. Your submissions compile
into a client-grade document under your byline.

Not a certificate. The work.

https://estudio-production-1b8c.up.railway.app/aprende

https://github.com/user-attachments/assets/brag.mp4

---

## Where this actually stands

It is running in production, and it is an **alpha with five learners**. The
machinery is complete and the demand thesis is unproven — no stranger has yet
finished lesson one. That gap is stated throughout the documentation rather than
papered over, because deciding what to build next depends on it.

| | |
|---|---|
| Courses live | 14 (420 lessons, 420 rendered videos) |
| Route library | 70 module contracts with declared prerequisites |
| Real learners | 5 · 16 submissions · 1 lesson-2 completion |
| Marginal cost per course | ≈ $0.35 of LLM + ~2 h unattended render |
| Marginal cost per learner | ≈ $0 |
| Stack | Python · FastAPI · Postgres · vanilla-JS single-file frontends · Railway |

---

## The interesting problems

**Composing a route, not selling a course.** The unit is the *module*, not the
course. A job posting decomposes into competencies; those match module outcome
contracts; the selection is closed transitively over declared prerequisites
server-side, so a route can skip a module the learner genuinely does not need
without stranding them in a lesson that says "as we saw in module 2."
→ [docs/08](docs/08-job-target.md), [docs/09](docs/09-world-of-knowledge.md)

**Publishing the gaps.** Coverage is computed so that a gap always costs coverage,
and below a floor the system refuses to promise a deliverable at all. A matcher
has a standing incentive to flatter its own catalog; a five-fixture calibration
suite exists to catch it when it does.
→ [`check_job_matcher.py`](studio/cloud/check_job_matcher.py)

**Verifying learning, not attendance.** Comprehension checks return a *verdict*
and never a score — scoring a conceptual explanation on "is it grounded in your
business" punished learners for doing exactly what was asked. Work products get
three dimensions plus an ownership probe. Identical text is never re-graded, and
the number on screen is always the learner's best, because a retry that costs you
something is not a retry.
→ [docs/02](docs/02-product.md), [`check_tutor.py`](studio/cloud/check_tutor.py)

**Making an LLM's judgement testable.** Two calibration suites make real model
calls and exit non-zero: the matcher against real job postings, and the tutor
against six properties — stability on identical input, ordering, and whether
acting on the tutor's own feedback actually raises the score.

---

## Repository map

```
docs/                     Ten documents: vision, product, architecture, the course
                          factory, operations runbooks, roadmap, engineering notes,
                          and the two specs behind the routing engine.
                          → start at docs/README.md

studio/cloud/             The engine.
  db.py                   Schema + every Postgres helper
  writer.py               Every LLM call: generation, evaluation, compilation
  course_factory.py       research doc → syllabus → lessons → video → live
  check_job_matcher.py    Route-matcher calibration (5 fixtures, real calls)
  check_tutor.py          Tutor calibration (6 properties, real calls)

studio/dashboard/         The application.
  app.py                  FastAPI: admin API, token gate, share pages
  learn_routes.py         The entire learner API
  static/learn.html       The learner app — one file, no build step

studio/channels/*.toml    Course definitions. Single source of truth for anything
                          a learner sees.
studio/research/          The deep-research documents courses are generated from.
studio/fixtures/          Calibration fixtures for the matcher.
```

Two invariants worth knowing before reading the code: **the course TOML is the
single source of truth** for learner-facing copy, and **nothing a learner has
earned may ever go down** — enforced in SQL, not by convention.

---

## Not included

- **`MoneyPrinterTurbo/`** — the video render engine, a separate
  [MIT-licensed project](https://github.com/harry0703/MoneyPrinterTurbo) kept as a
  clean clone. It is a dependency, not this repository's source.
- **Rendered videos** (10.6 GB) and **database backups** — the latter contain real
  learners' coursework and email addresses, and will never be published.
- **Every credential.** Nothing in this tree holds a secret; the running service
  reads them from Railway at runtime. See `.env.example` for the shape.

---

## Documentation

The docs are the best part of this repository, and they were written to be read
by whoever maintains it next.

| | |
|---|---|
| [01 — Vision](docs/01-vision.md) | Why this exists and what makes it defensible |
| [02 — Product](docs/02-product.md) | The learner experience, screen by screen |
| [03 — Architecture](docs/03-architecture.md) | Components, data model, API, security |
| [04 — Course factory](docs/04-course-factory.md) | Research in, 30-lesson course out |
| [05 — Operations](docs/05-operations.md) | Runbooks: deploy, ship a course, backup |
| [06 — Status & roadmap](docs/06-roadmap.md) | Where it honestly stands |
| [07 — Engineering notes](docs/07-engineering-notes.md) | Every bug pattern this codebase has produced, as rules |
| [08 — Job target](docs/08-job-target.md) | Posting → route → interview document |
| [09 — World of knowledge](docs/09-world-of-knowledge.md) | The north star |

[docs/07](docs/07-engineering-notes.md) is the one to read if you only read one.
It is a list of things that broke in production and the rule each one produced.

---

## License

**Source-available, evaluation only.** You are welcome to read this repository and
assess the work. You may not use, run, copy, modify, or redistribute it without
written permission. See [LICENSE](LICENSE).

© 2026 José Tomás Pérez-Acle
