# 02 — Product: the learner experience

Everything below is live at `/aprende`. The app is mobile-first, Spanish-only.
Hash-routing throughout: back button, refresh and deep links all work.

**Design identity — El Taller Nocturno.** The app is a night workshop: warm
darkness, one amber lamp, and the learner's work glowing paper-white — the only
light source that matters. The rule: *the interface is grotesk (Archivo), the
work is serif (Fraunces)* — headlines and scores are serif; documents and case
studies are paper-styled pages. All styling flows from a CSS token layer in
`learn.html` (`:root`: color, 6-step type scale, spacing, radii, motion) plus
component classes — a visual change is a token edit, never a hunt through
templates. Iconography is a drawn inline-SVG set (single stroke, currentColor);
no emoji in the chrome. The emotional moments are choreographed: staged
page-enters, a "tu tutora está leyendo tu entrega" reading state, an evaluation
reveal where dimension bars fill and the serif score counts up, and a spotlight
treatment for la defensa.

## The public face (no account)

A stranger — from a shared document, a bio link, word of mouth — lands on a
**landing page**, not a login wall: the promise ("termina cada curso con trabajo
real que mostrar"), how the loop works in three beats, a real sample document,
and the **full catalog with browsable temarios** (titles, module contracts,
per-lesson objectives — marketing content; lessons and videos stay gated). Two
doors: *"Tengo una invitación"* → login, *"Quiero entrar"* → waitlist (rate-
limited + honeypot), which lands in the admin dashboard as a demand signal.

## Entry

**Login** requires name + email + invite code (no password; a dev magic link logs
the user straight in until an email provider is configured). Invite codes are
created per person by the operator. Sessions last 90 days. **First login** shows
a three-card orientation (mira y haz / feedback que enseña / terminas con un
portafolio), revisitable from Perfil.

## Navigation: four tabs

**Hoy** — the zero-decision daily entry: a continue-card (course + next lesson,
one tap), **repasos due today** (the SM-2 spaced-repetition surface), pending
defensas, streak. **Cursos** — catalog + concierge. **Portafolio** — documents,
case studies, and all evaluated work grouped by course. **Perfil** — identity,
stats, how-it-works, logout.

**Catalog (Cursos tab).** Every course card has a fixed anatomy, top to bottom:

1. Title — the subject, with **no duration claim** ("Meta Ads", "Cultura
   latinoamericana"). Dropped 2026-08-12: a route may send a learner through only
   part of a course, so "en 30 días" contradicted the route on the next screen,
   and the meta line below already states scope truthfully. `preflight` rejects it.
2. Promise — one outcome line, ≤110 chars ("De cero a campañas rentables en
   Facebook e Instagram: píxel, públicos, creatividades y escalado")
3. Deliverable — "📄 Termina con: Plan de campaña en Meta Ads" (the portfolio hook)
4. Progress bar
5. Meta — "30 lecciones · 5 módulos"

Below the catalog sits the **course concierge**: *"¿Qué quieres aprender? Pide tu
curso."* Requests are tracked with statuses the learner can watch move
(Recibida → En revisión → En producción → Disponible), and a fulfilled request
links directly to its course. Max 3 open requests per learner.

## The temario (course outline)

- Course description + progress at the top.
- Every module shows its **outcome contract** — 1–2 sentences of what you can DO
  after it, generated from the module's actual lesson objectives.
- Every locked lesson is tappable to reveal *"Al terminar podrás: …"*. Nobody
  studies blind; the whole course's value is inspectable before any of it unlocks.
- After each module's six lessons: the **reto** row (capstone) with its state —
  locked until the module is complete, then scored (e.g. "82/100") once attempted.
- When the learner has 3+ submitted works: the **"Tu portafolio"** card — compile
  or view the project document, plus the STAR case study as a companion.

## The lesson loop (the pedagogy contract)

Lessons unlock strictly in sequence (progress-gated; a module time-gate is designed
but deliberately not active — see Roadmap). Each lesson:

1. **Video** (45–60s vertical) — carries the *concept and the why*. Deliberately
   calm pacing; works over stock footage. Tabs: ▶ Ver / 📖 Resumen (key points +
   transcript) / 🛠 Guía (written how-to with steps, tables, Mermaid diagrams —
   the *reference* half of the lesson, better read than watched).
2. **Explícalo en tus palabras** — a comprehension question *specific to this
   lesson* ("¿Qué significa que un objetivo sea SMART y por qué es clave para no
   malgastar dinero?"). The learner answers in their own words and gets a
   **verdict — Lo tienes / Casi / Todavía no** — plus what would round it out and
   any misconception, explicitly stated to carry **no grade**. Retryable without
   limit. Skippable — friction stays low, but skipping is a measured choice.
   On *Casi* or *Todavía no* a third move appears: **"Explícamelo de otra
   forma"**, which re-teaches the concept from a different angle, aimed at the
   misconception the tutor just diagnosed. It is never evaluated and cannot
   lower anything — admitting you are lost has to be safe. Without it the step
   only measured comprehension, which makes the tutor a grader; the first real
   verdict this product ever produced was on *"No entendí nada … ayudame"* and
   there was nothing to offer her.
3. **Quiz** — 3 multiple-choice questions where wrong answers teach too (every
   option gets an explanation).
4. **The exercise, with evidence.** Every exercise produces a real artifact
   (a brief, copys, a plan, an audit fragment) with a copy-paste starting prompt.
   The learner **pastes their actual work** and receives a scored evaluation:
   three dimensions, specific feedback, the gaps to 100, and then the
   **conversación con la tutora** (below). "Terminar sin enviar" exists as an
   escape hatch — the platform gates on engagement, never on passing.
5. **Completion** — celebration, streak, next lesson.

Reviews (a completed lesson reopened, or one surfaced by spaced repetition) run
the same path — the explain step is deliberately *not* skipped, both because
retrieval practice is the point of a review and because skipping it once made
pending conversations unreachable.

### Why this shape

- Multiple-choice measures *recognition*; explaining measures *understanding*;
  producing an artifact measures *ability*. The loop climbs that ladder every day.
- Nothing gates on passing. The design conviction: **feedback teaches, punishment
  churns.** All evaluation is formative; the only gate is doing.
- **Feedback is an invitation, not a verdict.** Every evaluation names 1–3
  concrete gaps ("para llegar a 100 te falta…") and offers a retry as the
  *primary* action when the work isn't there yet. On a resubmission the tutor
  sees the previous attempt and acknowledges progress explicitly ("subiste de 30
  a 90 porque ahora…") — while being instructed to grade the new text strictly on
  its own, so a lazy retry can't inherit an earlier attempt's credit. The
  revision loop is where concepts actually lock in; continuing without retrying
  is always allowed, never encouraged.
- **Nothing a learner earns can ever go down.** Work scores, the conversation
  bonus, quiz scores and the compiled document all keep the *best* attempt. That
  is what makes "try again" honest rather than a gamble — and it is enforced in
  SQL (`GREATEST`, `best_submissions()`), not by convention.
- **Comprehension checks get a verdict; work products get a score.** The
  explain step reports **Lo tienes / Casi / Todavía no** plus what's missing —
  never a number. A correct explanation of a concept is generic by nature, so
  scoring it on "is this grounded in your business" and "what decisions did you
  justify" punished learners for doing exactly what was asked (observed in
  production: a learner's *best* explanation scored lower than a weaker earlier
  one, while the tutor's own text said she had improved). Numbers also invite
  gaming a comprehension check, where the only way to game is to pad. Every
  evaluation carries a rubric version, and progress is only ever compared within
  one version.
- **Scores measure ownership, not authorship** (the AI-era rubric, for work
  products only). Using AI is
  explicitly permitted — it's the curriculum. Three dimensions sum to the score:
  **Aplicación** (0–40: grounded in YOUR numbers/brand/context — generic caps at
  15), **Criterio** (0–30: justified decisions, tradeoffs, what you *changed* in
  the AI's output), **Ejecución** (0–30: complete and usable). Then the
  **conversación con la tutora**: it asks one question only the decision-maker can
  answer ("¿cómo calculaste que 20 por semana es sostenible?") — a good answer
  earns up to +10. Pasted work collapses under one "why"; owned work shines. It is
  framed as a conversation, never a defense: the learner is invited to keep
  answering until they reach the full 10.
- **Every score is reachable.** Both the work and the conversation are
  retryable without limit, and each evaluation says *why*: the work gets "para
  llegar a 100 te falta…", the conversation gets "para llegar a los 10 puntos…".
  100 is genuinely attainable — verified end to end. We reward appropriation
  rather than policing AI, because detection is a losing arms race and ownership
  is the actual hiring signal. A self-predicted score (work products only) trains
  calibration — the meta-skill of judging your own work. It is asked as a
  **beat**, not a field: after pressing send, one tap on *Le falta / Va bien /
  Está sólido / Es mi mejor trabajo*, always skippable. As a bare number box
  beside the button it was used in 2 of 16 real submissions; the judgement is
  the point, so it is phrased as a judgement and shared by the exercise and the
  reto (`predictionBeat`).
- Evaluation latency is 10–20 seconds; the UI treats it as a moment of suspense
  ("Evaluando tu trabajo…"), not a spinner apology.

## The transversal project

In lesson 1, every course asks the learner to choose a project that every later
exercise builds on. Two explicitly equal paths:

- **Their own business** — the entrepreneur path.
- **A real, known brand they'd like to work with** — the *unsolicited audit* path,
  strictly better for job seekers: an audit of a brand the interviewer recognizes
  demonstrates judgment on day one.

## The capstone retos

At the end of each module: a novel scenario (a realistic LatAm business with a
name, a budget, a constraint) that was deliberately *not* covered in the lessons.
Transfer to an unseen case is the difference between knowing and understanding.
Solutions are graded against a rubric; retos are retryable; the score shows on the
temario. Retos feed the portfolio.

## The portfolio pieces (the endgame)

**The project document** — the headline deliverable. The platform compiles the
learner's real submissions into the document a client would have paid for,
organized by the *document's* logic, not lesson order:

| Course | Document |
|---|---|
| Marketing con IA | Estrategia de marketing digital |
| Meta / TikTok / Google Ads | Plan de campaña |
| SEO + AEO | Auditoría SEO + AEO |
| Email marketing | Programa de email marketing |
| Automatización IA | Plan de automatización con IA |

Hard rules of the compiler: every claim traces to the learner's work; missing
sections appear as honest "Por desarrollar" recommendations, never fabricated;
plans are presented as plans. The document lives on a **paper-styled public page**
under the learner's byline — serif, print-perfect ("Descargar PDF" built in),
Markdown export for Notion portfolios. Platform branding is one footer line:
the document must read as *theirs*, because it is.

**The STAR case study** — the companion narrative (Situación / Tarea / Acción /
Resultado) composed from the same submissions, first-person, for LinkedIn or an
interview story. Same honesty rules; results that don't exist yet are projections.

Both regenerate as the learner progresses, and share links are stable forever.

**Mi trabajo (Perfil tab)** — every submission with its score and feedback,
expandable. The learner's private ledger of everything they produced.

## Spaced repetition & habit

Completed lessons re-enter rotation on an SM-2-lite ladder (1 → 3 → 7 → 16 → 35
days). Reviews re-serve the lesson with its quiz; review completions never
overwrite first-completion records. A daily streak (with a one-day grace) is the
only gamification. No badges, no XP — measure first, decorate later.

## The admin side (operator dashboard)

Token-gated dashboard at `/panel`: production stats, per-channel/course cards, a
14-day production chart, the render queue, the video library with an
approve-before-publish gate (for the social channels), and **Solicitudes de
cursos** — the concierge triage table (status pipeline + course-slug linking,
learner identity attached to every request).
