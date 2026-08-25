# Brag Plan: Aprende IA

## What is this app?
A Spanish-language learning platform for Latin America where you say what you want to
*be* — paste a real job posting or just name the role — and it compiles a study route
through a module library, verifies you actually learned it, and hands back a
client-grade work document under your own byline. Not a certificate. The work.

## The angle
**The platform that tells you what it can't teach you.**

Every course platform claims to cover everything. This one computes, publishes, and
defends its own gaps — on the public page, before you sign up. That is the single most
counter-intuitive thing in the product and it is real, not marketing: the route
engine's coverage number is derived so that a gap always costs coverage, and below a
floor of 25% it refuses to promise a deliverable at all.

So the video is not "look how much we offer." It is "look at what we admit." The
honesty *is* the product, and it earns the closing claim about the work document.

## Hook (first 2-3 seconds)
Black. One warm amber lamp resolves out of the dark — the product's actual brand
object ("la lámpara"). Over it, the app's real first line, in Fraunces serif:

> **Dinos qué quieres ser.**

No logo yet. No product shot. The question is the hook, because it is the entire
premise of the product and it is what the landing page actually says.

## Key moments (the middle)
1. **A job posting becomes a path.** Pasted posting text collapses into an ordered
   route. Steps labelled by capability, not by product — the real string from the app:
   *"Paso 1 de 13 · Sabrás pedirle a la IA exactamente lo que necesitas"*, with the
   course reduced to a small provenance line beneath. Coverage reads **83%**.
2. **The 17% it refuses to hide.** The gap panel, verbatim from `ruta.html`:
   *"Esto lo pide el puesto y no lo cubrimos"* — then, held long enough to read:
   *"Lo publicamos a propósito."* This is the beat the whole video exists for.
3. **The work turns into paper.** Dark interface → the learner's submission →
   the tutor's three dimensions (Aplicación 38/40 · Criterio 28/30 · Ejecución 27/30) →
   the page turns paper-white: the compiled document under their name. The design
   system's own rule made literal — *the interface is grotesk, the work is serif.*

## Outro / punchline
The paper document holds, then the line lands:

> **No un certificado. Tu trabajo.**

Amber lamp dims to a single point. Wordmark: **Aprende IA**.

## User flow worth showing
Entry → key action → result, exactly as the product runs:
1. **Entry** — paste the job posting you actually want (`#/oferta`, no account needed).
2. **Key action** — study a step and submit real work; the tutor scores it on three
   dimensions and asks one question only the person who did the work can answer.
3. **Result** — the submissions compile into a shareable document under your byline.

## Tone
- Preset: **polished**
- Creative direction: *quiet night-workshop product film* — the product's own design
  identity is "El Taller Nocturno": warm darkness, one lamp, and the learner's work as
  the only other light in the room.
- Interpretation: slow, confident cuts; generous holds on the two lines that matter
  (the gap admission and the closing claim); motion that reveals rather than performs.
  Restraint is the point — a video about honesty cannot look like an ad.

## Format: landscape — 1920x1080
## Duration: 20s

## Visual identity (from the project)
- Background: `#100D17` (`--ink`, "night")
- Panel / raised surface: `#191521`, `#221D2E`
- Accent: `#F0A43C` (`--amber`, "la lámpara") with `#FFC670` highlight
- Paper (the work): `#F1E6CE` on `#26200F` ink
- Text: `#F2EFE9`, dim `#B2AABB`
- Display font: **Fraunces** (serif — reserved for the work and for headlines)
- Body font: **Archivo** (grotesk — the interface)
- Strongest visual element: the dark-to-paper transition. Everything in the UI is
  night and amber; the learner's finished document is the only paper-white surface.

## Honesty constraints (non-negotiable for this project)
This is an invite-gated alpha: **five learners, one design partner**. The video must
not imply traction, scale, or social proof. Permitted claims, all verifiable in the repo:
14 courses · 420 lessons · routes composed from 70 module contracts · honest published
gaps · work evaluated on three dimensions · a document under the learner's byline.
Banned: user counts, testimonials, "trusted by", growth numbers, outcome promises.
A video that overclaims would contradict the exact property it is bragging about.

## Share copy (draft)
Construimos una plataforma que publica lo que *no* te puede enseñar. Le pegas la
oferta de trabajo que quieres y te arma la ruta, te evalúa el trabajo real, y terminas
con un documento tuyo — no un certificado. En español, para LatAm.

## Audio direction
- Role: warm restrained bed with sparse, motion-matched accents
- Music: `happy-beats-business-moves-vol-1-by-ende-dot-app.mp3` (120.19 BPM)
- Music treatment: start ~3.0s so the hook lands in near-silence; low bed under the
  route build; soften under the gap admission so the line reads in relative quiet;
  gentle fade from ~18.5s into the outro
- Music cue guidance: preset cue file read. Strong cues at **16.02s, 17.02s, 18.02s,
  18.52s, 20.02s**; beat grid every ~0.5s from 3.02s. Use 17.02s or 18.52s for the
  paper-turn reveal; sequence the three route steps on the beat grid between
  ~8.0-12.5s. Cue metadata is timing guidance only — readability wins over sync.
- Audio-reactive treatment: **subtle** — the amber lamp glow breathes with music RMS;
  the paper surface gains slight presence on bass at the reveal. No waveforms, no
  equalizer graphics, no text scaling.
- SFX posture: sparse. A soft `ui/click` on the paste action, one restrained
  `interface/drop` on the paper-turn. Nothing on every transition.
- Audio-coupled moments: the posting collapsing into steps; the paper-turn reveal.
- Restraint rule: audio must never overpower the two held lines. No riser before the
  gap admission — the point is that it is stated plainly, not sold.
