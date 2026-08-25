# Estudio IA — Automated Spanish AI Shorts Factory

A fully automated pipeline that produces Spanish-language short-form videos (TikTok,
Reels, YouTube Shorts) teaching Spanish speakers about AI, across four themed
channels. Claude/DeepSeek writes the scripts, [MoneyPrinterTurbo](../MoneyPrinterTurbo)
renders the videos, and (once credentials are connected) Upload-Post publishes them
on a schedule — with a human approval gate in between.

This document is the single source of truth for picking the project back up. It
covers what exists, how it runs, what's live vs. dormant, and the exact steps to
launch when the missing credentials arrive.

---

## 1. Current status (as of 2026-07-24)

| Thing | State |
|-------|-------|
| Local studio (render + dashboard) | ✅ Working |
| Cloud deployment (Railway) | ✅ Deployed, healthy |
| Cloud scheduler | ⏸️ **OFF** (`ENABLE_SCHEDULER=0`) until Upload-Post is connected |
| Script generation (DeepSeek via OpenRouter) | ✅ Working, incl. live web search for news |
| Postgres topic dedup + publish log | ✅ Working |
| Approve-first publishing gate | ✅ Working |
| Auto-publishing (Upload-Post) | ❌ **BLOCKED** — needs account + credentials (see §7) |

**The one thing standing between here and full autopilot: an Upload-Post account
with the 4 social profiles connected.** Everything else is built and tested.

**Test videos rendered so far** (in `studio/output/`, for quality review): 4 written
by Claude Opus, 3 by DeepSeek V4 Pro (including one news video built from live web
search that was fact-checked against real coverage).

---

## 2. The four channels

Each channel is a self-contained identity defined in `channels/<slug>.toml`. Distinct
voice + subtitle color per channel so the network doesn't read as one bot. Overlap is
intentional: one hot topic can be angled four ways.

| Slug | Canal | Nicho | Voz (Edge TTS) | Color | Publish slot |
|------|-------|-------|----------------|-------|--------------|
| `ia-facil` | IA Fácil | Alfabetización IA, público general | Dalia (es-MX, F) | Azul `#0284C7` | 19:00 |
| `codigo-ia` | Código IA | Programar con IA / Claude Code | Jorge (es-MX, M) | Verde `#16A34A` | 21:00 |
| `oficina-ia` | Oficina IA | Productividad IA en el trabajo | Paloma (es-US, F) | Morado `#7C3AED` | 12:00 |
| `ia-al-dia` | IA al Día | Noticias y tendencias IA (usa búsqueda web) | Gonzalo (es-CO, M) | Rojo `#DC2626` | 12:00 |

Publish slots (America/Santiago) are algorithm-informed: LatAm engagement peaks at
midday (12–15h) and evening (19–22h). `ia-al-dia` is the news channel — its producer
uses OpenRouter's `:online` mode to pull real current events before writing.

To change a channel's identity (voice, colors, tone, CTA, slot), edit its TOML —
changes apply to every future render. No code change needed to add a 5th channel:
drop a new `channels/<slug>.toml` and it's picked up automatically.

---

## 3. Architecture

```
                    ┌────────────────── one Railway service: "estudio" ──────────────────┐
                    │                                                                     │
  APScheduler ──────┤  06:00 → producer.py ──┐                                            │
  (in dashboard     │                        │  ideate topics (dedup vs Postgres history) │
   process, when    │                        │  write scripts (DeepSeek/OpenRouter)       │
   ENABLE_SCHEDULER)│                        └→ generate_batch.py → MoneyPrinterTurbo      │
                    │                                                 (TTS+Pexels+ffmpeg)  │
                    │  12/19/21h → publisher.py → Upload-Post (only APPROVED videos)       │
                    │                                                                     │
                    │  dashboard/app.py (FastAPI) ── observability + approve + manual jobs │
                    └──────────────┬──────────────────────────────┬─────────────────────┘
                                   │                              │
                          Postgres (topics, publish_log)   Volume /app/studio/output
                                                            (rendered mp4 + .json sidecars)
```

**Key design decision — production and publishing are decoupled.** Rendering (heavy,
failure-prone) runs once each morning and fills a buffer. Publishing (trivial, must be
reliable) drains the approved buffer at the peak slots. A broken render never silences
a channel; you always have a review window.

**Source-of-truth split:**
- **Filesystem** (`output/<channel>/<date>-<slug>.mp4` + `.json` sidecar) = video
  artifacts and their approve/publish state.
- **Postgres** = topic backlog with no-repeat history (`topics`) and publish audit
  log (`publish_log`).

---

## 4. File map

```
studio/
  channels/*.toml          Channel identities (voice, style, publish slot, upload_post_username)
  generate_batch.py        Core renderer: reads queue/pending/*.json → MoneyPrinterTurbo CLI → output/
  dashboard/
    app.py                 FastAPI: /api/state, approve/publish endpoints, manual job triggers, token gate
    static/index.html      Single-page dashboard (stat tiles, channel cards, chart, library, approve UI)
  cloud/
    entrypoint.py          Container start: render config.toml from env, init DB, serve dashboard
    db.py                  Postgres schema + topic/publish helpers
    writer.py              DeepSeek/OpenRouter ideation + script writing (hooks, length, CTA rotation)
    producer.py            Daily run: pick/generate topic → write → render → mark used
    publisher.py           Publish slot: take oldest APPROVED video → Upload-Post → log
    scheduler.py           APScheduler wiring (06:00 produce + publish slots)
  queue/
    pending/*.json         Video specs waiting to render
    done/*.json            Rendered specs (archive)
  output/<channel>/        Rendered videos + metadata sidecars (the Railway volume)

Dockerfile                 Repo root — builds MoneyPrinterTurbo + studio into one image
.dockerignore/.railwayignore  Exclude venv, storage, outputs from image
MoneyPrinterTurbo/         The upstream video engine (git clone, kept clean for updates)
```

The channel TOML, queue JSON, and sidecar JSON are the only data formats. Deleting a
video's `.mp4`+`.json` removes it from the dashboard. There is no hidden state.

---

## 5. Running locally

Prereqs: the `MoneyPrinterTurbo/.venv` (Python 3.11) already exists with deps installed,
ffmpeg is on PATH, and `MoneyPrinterTurbo/config.toml` has the Pexels key.

```bash
# Dashboard (observe library, approve, trigger manual jobs)
MoneyPrinterTurbo/.venv/Scripts/python.exe studio/dashboard/app.py
# → http://localhost:8765

# Render whatever is queued in queue/pending/
python studio/generate_batch.py                 # all channels
python studio/generate_batch.py --channel codigo-ia
python studio/generate_batch.py --dry-run       # preview

# Full cloud-style produce run locally (needs OPENROUTER_API_KEY + DATABASE_URL env)
MoneyPrinterTurbo/.venv/Scripts/python.exe studio/cloud/producer.py
```

To manually queue a video without the LLM, drop a JSON into `queue/pending/`:
`{channel, subject, title, description, hashtags, script, terms}` (terms = comma-
separated English Pexels search terms), then run `generate_batch.py`.

---

## 6. The cloud deployment (Railway)

- **Project:** `estudio-ia` (id `8a2e90fe-e597-45d4-92c0-f274ece96af6`)
- **Services:** `estudio` (the app, Dockerfile at repo root) + `Postgres` (addon)
- **Volume:** `estudio-volume` mounted at `/app/studio/output`
- **Dashboard URL:** https://estudio-production-1b8c.up.railway.app
  (token-gated — append `?token=<DASHBOARD_TOKEN>` once, then a cookie remembers you)

### Deploy / redeploy

```bash
# from repo root (already linked to the project/environment/service)
railway up --detach
```

CLI is already linked. If a fresh machine needs linking:
`railway link --project 8a2e90fe-e597-45d4-92c0-f274ece96af6 --environment production`
then `railway service estudio`.

### Environment variables (set via `railway variables --set "K=V"`)

| Variable | Purpose | Current |
|----------|---------|---------|
| `DATABASE_URL` | Postgres (Railway reference `${{Postgres.DATABASE_URL}}`) | set |
| `OPENROUTER_API_KEY` | Script generation | set |
| `LLM_MODEL` | Which model writes scripts | `deepseek/deepseek-v4-pro` |
| `PEXELS_API_KEY` | Stock footage | set |
| `DASHBOARD_TOKEN` | Dashboard access gate | set (saved at `%TEMP%\studio_token.txt` locally) |
| `PORT` | Web port | `8765` |
| `SCHEDULE_TZ` / `TZ` | Scheduler timezone | `America/Santiago` |
| `ENABLE_SCHEDULER` | Master on/off for produce+publish crons | **`0` (OFF)** |
| `UPLOAD_POST_API_KEY` | Cross-posting | ❌ **not set — needed to launch** |
| `AUTO_APPROVE` | Skip the approval gate (publish everything) | unset = gate ON |
| `BUFFER_MAX` | Max unpublished videos buffered per channel | default 5 |

### Useful ops

```bash
railway logs                     # tail service logs
railway variables --kv           # list all env vars
```

Cost note: DeepSeek V4 Pro ≈ **$0.30/month** at 4 videos/day (vs ~$4–5 on Opus).
Model is a one-variable swap: `railway variables --set "LLM_MODEL=anthropic/claude-opus-4.8"`.

---

## 7. 🚀 Launch checklist (do this when Upload-Post credentials arrive)

Upload-Post (https://upload-post.com) is the third-party service that cross-posts to
TikTok/Instagram/YouTube. You create the account, connect the 4 social profiles there
(one "user" profile per channel), and get one API key.

1. **Add the API key** to Railway:
   ```bash
   railway variables --set "UPLOAD_POST_API_KEY=<your key>"
   ```
2. **Set each channel's Upload-Post username** in its TOML `[publish]` block
   (`upload_post_username = "..."`), for all four:
   `channels/ia-facil.toml`, `codigo-ia.toml`, `oficina-ia.toml`, `ia-al-dia.toml`.
3. **Turn on the scheduler:**
   ```bash
   railway variables --set "ENABLE_SCHEDULER=1"
   ```
4. **Redeploy** so the TOML changes ship: `railway up --detach`.
5. **Smoke-test before trusting the cron:** open the dashboard → "▶ Producir ahora"
   to generate today's videos, approve one, then "▶ Publicar ahora" to confirm the
   Upload-Post round-trip works for that channel's profile.

After that it's autonomous: 06:00 produce → you approve in the dashboard → 12/19/21h
publish. Keep the approval gate on (`AUTO_APPROVE` unset) for the first 2–3 weeks.

---

## 8. Daily operating loop (once live)

1. Morning: 4 fresh videos are rendered and waiting (dashboard "Aprobados en espera"
   tile shows 0 until you act).
2. You review each, tap **Aprobar** on the good ones (veto the rest — just leave them).
3. Approved videos auto-publish at their channel's slot; the rest never post.
4. Watch retention/views. After 2–3 weeks, use each platform's "peak activity"
   analytics to recalibrate the publish slots in the TOMLs.

Cadence is deliberately 1/day/channel to warm up new accounts safely. Ramp to 2–3/day
on channels that land by adding entries — the buffer architecture makes cadence a
config value.

---

## 9. Content strategy baked in (why it's built this way)

**Algorithm priorities** (from 2026 research across TikTok/Reels/Shorts):
- Completion rate is the #1 signal. Videos target **35–45s** (scripts 100–120 words) —
  short enough to clear retention thresholds (TikTok wants >70%; Shorts ~65% under 30s).
- The **first 3 seconds** decide everything → the writer forces a tension/curiosity hook
  in the first 8 words, with pattern variation (no repeated "¿Sabías que...?").
- **DM shares rank 3–5× above likes** on Reels → CTAs rotate ~40% follow / 40% share /
  20% save (share CTAs ask viewers to send it to a specific person). Rotation is
  deterministic on the topic slug (`writer.py:_cta_style`).
- All metadata (titles, hashtags, descriptions) stays in Spanish — a ranking factor
  for Spanish-audience distribution.

**No-repeat topics:** the full topic history per channel is injected into the ideation
prompt as a do-not-repeat list (catches semantic repeats), with a
`UNIQUE(channel, slug)` DB constraint as backstop. News channel never repeats by
construction (fresh web search daily).

---

## 10. Known limitations / roadmap

- **Stock footage, not screen recordings.** Works for AI news/concepts/tips. Real
  hands-on Claude Code tutorials would need screen captures fed in as local materials
  (MoneyPrinterTurbo supports this via `video_source=local`) — decided out of scope;
  long-form tutorials handled separately by the user.
- **Cloud render speed unproven at scale.** Railway CPU renders are slower than local;
  if the 06:00 batch is too slow, bump the service resources or stagger channels.
- **Moderation.** News videos are fact-checkable but the approval gate is the safety
  net — keep it on. AI-content disclosure is set for YouTube automatically.
- **Bigger vision (discussed, not built):** this same engine is ~80% of a multi-tenant
  SaaS where brands plug in their identity/assets and get generated content. A channel
  profile == a tenant. Deliberately deferred until the 4 owned channels validate that
  the content performs. Everything is kept tenant-shaped (profiles as data, per-channel
  everything) so that door stays open.

---

## 11. Quick reference — IDs & endpoints

- Railway project: `8a2e90fe-e597-45d4-92c0-f274ece96af6`
- Railway service `estudio`: `2c6fd4d0-70f7-45d0-9577-4d81de3a02a4`
- Production environment: `e7c5a35e-786f-4ea0-8f1a-03586df42c23`
- Dashboard: https://estudio-production-1b8c.up.railway.app (needs `?token=`)
- Local dashboard: http://localhost:8765
- OpenRouter models: `deepseek/deepseek-v4-pro` (live), `anthropic/claude-opus-4.8` (fallback)
