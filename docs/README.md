# Rumbo — Documentation

**Rumbo** is a Spanish-language learning platform for Latin America that
turns deep research into complete video courses — and turns each learner's
coursework into a **real, client-grade portfolio document** they can put in
front of an employer.

One AI content engine powers two products:

1. **Rumbo** (live) — the learning platform. **14 courses, 420 lessons.**
   A learner names the job they want and gets a route through the module library;
   each lesson is a short vertical video + written guide + a comprehension check +
   a hands-on exercise evaluated by an AI tutor. Every course ends in a
   professional deliverable (a strategy, a campaign plan, an audit) compiled
   from the learner's own work.
2. **Estudio IA** (built, dormant) — a 4-channel social video factory for
   TikTok/Reels/Shorts, intended as the acquisition funnel. Waiting on
   publishing credentials; everything else is production-tested.

## Quick facts

| | |
|---|---|
| Live URL | https://estudio-production-1b8c.up.railway.app/aprende |
| Admin dashboard | same host, `/` — needs `?token=<DASHBOARD_TOKEN>` once |
| Courses | **14 × 30 lessons** across 6 clusters: marketing/ads/SEO/email/automatización + Ciencias sociales (grafos, cultura latam) + Deporte (gestión, vóleibol) + Redes y creadores (influencers, social media) + analítica |
| Videos | 420 rendered — 720p/CRF27 (~5MB per lesson; re-encoded 2026-08-12 for LatAm mobile data and volume capacity) |
| Goal engine | paste a job posting **or name a role** → module-level route (prereq-aware) → verified learning → one goal document (docs 08–09) |
| Marginal cost per course | ≈ $0.35 of LLM + ~2 h of local render compute |
| Marginal cost per learner | ≈ $0 (videos are canonical; personalization lives in each learner's path) |
| Cost per AI evaluation | fractions of a cent (DeepSeek V4 Pro via OpenRouter) |
| Stack | Python/FastAPI · Postgres (20 tables) · vanilla-JS single-file frontends · MoneyPrinterTurbo render engine · Railway |
| Access | Invite-gated alpha; public landing + waitlist for strangers |
| **Real usage** | **5 learners · 16 submissions · 3 completions, all of them a lesson 1** — see doc 06 |

## Reading map

| Document | Read it to understand |
|---|---|
| [01 — Vision](01-vision.md) | Why this exists, the strategy, what makes it defensible |
| [02 — Product](02-product.md) | What a learner experiences, screen by screen, and why each piece is there |
| [03 — Architecture](03-architecture.md) | Components, data model, API surface, request flows, design decisions |
| [04 — Course factory](04-course-factory.md) | How a research document becomes a 30-lesson course with videos |
| [05 — Operations](05-operations.md) | Runbooks: deploy, ship a course, invite, triage, backup, troubleshoot |
| [06 — Status & roadmap](06-roadmap.md) | Where we actually are, success gates, what's next, parked designs |
| [07 — Engineering notes](07-engineering-notes.md) | **Read before your first edit.** Verification ritual, tooling traps, bug patterns |
| [08 — Job target](08-job-target.md) | The acquisition wedge: a pasted job posting → a study route + the interview document |
| [09 — World of knowledge](09-world-of-knowledge.md) | **North star.** "Quiero ser X" → route → verified learning → proof. What has to become true, in order |
| [10 — CV intake](10-cv-intake.md) | Paste a CV → proposed module skips, credited only by passing the reto. The first feature a real learner asked for |
| [11 — Public surface](11-public-surface.md) | The landing that runs a real lesson for strangers: the demo endpoints, their security model, and the honesty constraints |

## If you are a coding agent starting fresh

1. `/CLAUDE.md` (repo root) is the operational quick-reference — secrets,
   common commands, gotchas.
2. **[07 — Engineering notes](07-engineering-notes.md)** before you change
   anything. Every entry was learned by breaking something.
3. [03 — Architecture](03-architecture.md) for the map, then
   [06](06-roadmap.md) for what matters next.
4. The code graph in `graphify-out/` answers structural questions faster than
   grepping (`graphify query "..."`, `graphify explain "X"`).

Two invariants worth internalizing immediately: **the course TOML is the single
source of truth** for anything learner-facing, and **nothing a learner has
earned may ever go down** — retries, reviews and re-scores all keep the best.
