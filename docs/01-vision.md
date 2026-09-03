# 01 — Vision: why Rumbo exists

## The problem, stated honestly

AI made course *production* free. Anyone can generate a syllabus and thirty scripts
in an afternoon, which means "a course" as a product is collapsing toward zero value.
At the same time, the credential attached to courses — the certificate — was always
borrowed trust: it is worth exactly as much as the issuer's reputation, and a new
platform has none.

Meanwhile, the actual customer problem is unchanged: a marketer in Latin America
needs to *get hired* or *grow a business*, and what employers and clients respond to
is not certificates. It is **evidence of work**: a strategy document, a campaign
plan, an audit of a real brand.

## The thesis

> Generating courses is a commodity. **Verifying that someone learned — and turning
> their verified work into proof they can show — is the defensible half.**

Rumbo is built around that asymmetry. The course is the delivery mechanism;
the product is a loop:

```
research → course → lesson → learner DOES something real
                                  → AI tutor evaluates it against the lesson
                                  → the work accumulates
                                  → the platform compiles it into a client-grade document
                                  → the learner shows the document, not a certificate
```

### The three tiers of proof

Everything a learning product can give a learner falls into one of three tiers:

1. **A certificate** — "an institution says I learned." Worthless without issuer
   reputation. We do not issue certificates.
2. **A case study** — "a story about what I did." Useful narrative; we generate one
   (STAR methodology) as a companion piece.
3. **A work document** — "the thing a client would have paid for." A complete
   marketing strategy, a campaign plan, an SEO audit of a real brand. Its value is
   intrinsic — it needs no one's endorsement. **This is the product's endgame for
   every course.**

The unsolicited audit of a real, known brand (the *proyecto con marca real* path) is
the strongest form: a job seeker who walks into an interview with a genuine audit of
a brand the interviewer knows has demonstrated judgment, not attendance.

## Why the economics work

- **A course costs ≈ $0.35 of LLM plus ~2 hours of render compute** to produce, and
  is canonical: rendered once, served to every learner. Marginal cost per learner is
  effectively zero.
- **Every AI evaluation costs fractions of a cent** (DeepSeek V4 Pro via OpenRouter),
  so the expensive-sounding part — a personal tutor evaluating every exercise,
  explanation, capstone, and compiling documents — is economically trivial.
- The engine is **tenant-shaped by design** (a course/channel is a TOML profile),
  which keeps the door open to the larger play: content-and-learning infrastructure
  for brands, once the consumer product validates the format.

## Where the thesis actually stands (be honest about this)

As of 2026-09-03: **15 courses, 450 lessons, 450 videos — and 3 lessons completed
by a human.** Sixteen submissions, one design partner with real activity. Three
weeks and one more course later, that completion count has not moved. The
engine is proven; the thesis is not tested yet. Every strategic statement below
is a hypothesis, and the platform's bottleneck is evidence, not build capacity.
Read doc 06 before planning work.

The catalog doubling in one night is itself the evidence for that sentence: the
production side scales effortlessly and the learning side has not moved since
2026-08-07.

## Strategy: validation before scale

The platform deliberately runs **narrow and deep** right now:

- **n=1 alpha** with a real design partner (a marketer actively studying for a real
  job posting — her job posting literally became the course roadmap).
- **Invite-gated** access; every login requires a code. Professional, controlled,
  and it keeps the data clean.
- **The course concierge** ("Pide tu curso") turns demand into a queue we fulfill
  semi-manually with the factory. It is simultaneously a feature, a demand signal
  for what to build next, and a rehearsal for the eventual on-demand product.

The order of bets, each gated on the previous one:

1. **Format validation (now):** does a motivated learner finish Module 1 and produce
   a real artifact? (Alpha exit criterion.)
2. **Retention validation (beta, 50–100 users from the social channels):**
   Module-1 completion ≥ 60%, D7 ≥ 40%, exercise submission is real (now measurable —
   evidence is required, not self-reported).
3. **Price it** (LatAm-priced, ~$5–10/mo or per-course) only after the metrics clear.
4. **On-demand course generation** ("request → deep research → course") only when
   the concierge queue outgrows manual fulfillment — scaling is a solved problem the
   moment demand justifies it, because the factory already runs end-to-end.

## What makes it defensible

- **The evaluation layer.** Every exercise, explanation, and capstone is graded by an
  AI tutor against the lesson's actual objectives, with feedback that cites the
  learner's own words. Competitors generate content; almost none verify learning.
- **The portfolio compiler.** Submissions become documents. The document carries a
  one-line footer credit — every piece a learner sends to a hiring manager markets
  the platform to exactly the right audience.
- **Editorial honesty as a product feature.** The SEO course teaches evidence
  discipline (Primary/Vendor/Unverifiable source tiers) because its own research
  material was built that way. The AI tutor refuses to invent metrics in documents;
  unproven results are labeled projections. In a market drowning in AI slop, being
  the platform that *doesn't lie* is a brand.
- **A content flywheel we own.** The four social channels (dormant, ready) exist to
  acquire learners at zero CAC once switched on.

## Origin (one paragraph of history)

The project began (July 2026) as an automated Spanish-language shorts factory —
channel profiles, script generation, rendering, scheduled publishing. The strategic
turn was recognizing that the same engine that produces a 45-second educational
video could produce a *course* — and that the interactive loop around the video
(quiz → exercise → evaluation → portfolio), not the video itself, is where the value
lives. The shorts factory remains intact as the future acquisition funnel.
