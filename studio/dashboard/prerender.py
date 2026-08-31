"""Server-rendered bodies for the public surfaces. No imports beyond stdlib.

WHY THIS EXISTS
---------------
Every public page used to send exactly eleven characters of body text to
anything that does not run JavaScript: `Cargando…`. Meta tags were rendered
server-side, so WhatsApp previews worked, but the *content* — fourteen course
temarios, 420 lesson objectives, the whole argument of the landing — existed
only after hydration. A crawler saw a loading spinner. So did an AI answer
engine, which matters more than usual here: one of the fourteen courses we sell
is SEO + AEO, promising learners they will appear in Google and in ChatGPT and
Perplexity answers. The page selling it could not do it.

It is also a load-time fix. The landing takes ~7.5s to hydrate on an unthrottled
desktop connection, and the intended reader is on a phone on LatAm mobile data.
Until now that whole window showed a spinner. Now it shows the real thing.

HOW IT PLUGS IN
---------------
`_spa_shell` swaps this markup in for the `Cargando…` node *inside* `#app`.
Every SPA view begins with `app.innerHTML=''`, so hydration erases whatever is
here — there is no double-render and no reconciliation to get wrong. That is the
entire integration contract, and it is why this module renders a self-contained
block rather than trying to match what the SPA will build.

RULES
-----
- Dependency-free on purpose (see `admin_paths.py` for the same reasoning): it
  renders from plain dicts, so it can be tested under any interpreter without
  importing FastAPI or opening a database connection.
- Everything interpolated goes through `_esc`. The inputs are our own course
  copy today, but this lands in a document that is served to strangers.
- Real `<a href>` anchors, never JS navigation. The point is that a crawler can
  walk from the catalog to all fourteen temarios; a `<div onclick>` is invisible
  to it and this whole module would be pointless.
"""
from __future__ import annotations

import html

# Inline styles only. This block is replaced within a second of hydration, so it
# must not depend on class names the SPA might rename, and it must not add a
# stylesheet the browser has to fetch before showing anything.
_WRAP = "max-width:900px;margin:0 auto;padding:28px 18px 60px"
_H1 = ("font-family:Fraunces,Georgia,serif;font-weight:600;font-size:30px;"
       "line-height:1.1;letter-spacing:-0.015em;margin:0 0 12px;color:#F2EFE9")
_H2 = ("font-family:Fraunces,Georgia,serif;font-weight:600;font-size:21px;"
       "line-height:1.15;margin:30px 0 10px;color:#F2EFE9")
_H3 = ("font-family:Archivo,system-ui,sans-serif;font-weight:700;font-size:15px;"
       "margin:18px 0 6px;color:#F2EFE9;letter-spacing:-0.01em")
_P = ("font-family:Archivo,system-ui,sans-serif;font-size:15px;line-height:1.55;"
      "color:#B2AABB;margin:0 0 14px;max-width:65ch")
_SMALL = ("font-family:Archivo,system-ui,sans-serif;font-size:13px;"
          "line-height:1.5;color:#8B8296;margin:0 0 8px")
_LINK = "color:#F0A43C;text-decoration:none;border-bottom:1px solid #AD7423"
_CARD = ("display:block;border:1px solid #2F2839;border-radius:3px;"
         "padding:16px 18px;margin:0 0 10px;text-decoration:none;background:#191521")
_LABEL = ("font-family:Archivo,system-ui,sans-serif;font-weight:700;font-size:10.5px;"
          "text-transform:uppercase;letter-spacing:0.13em;color:#8B8296")


def _esc(value: object) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def _nav() -> str:
    """The same three doors the SPA shows, as real links.

    Present on every prerendered page so a crawler that lands on any one of them
    can reach the rest without executing anything.
    """
    return (
        f'<p style="{_SMALL}">'
        f'<a href="/" style="{_LINK}">Rumbo</a> · '
        f'<a href="/cursos" style="{_LINK}">Cursos</a> · '
        f'<a href="/oferta" style="{_LINK}">Tu ruta</a>'
        f'</p>'
    )


def landing_html(courses: list[dict] | None = None) -> str:
    """The landing's argument, in text, above whatever the SPA later builds."""
    courses = courses or []
    items = "".join(
        f'<li style="{_SMALL}"><a href="/curso/{_esc(c.get("slug"))}" style="{_LINK}">'
        f'{_esc(c.get("title"))}</a> — {_esc(c.get("description"))}</li>'
        for c in courses
    )
    catalog = (f'<h2 style="{_H2}">Los cursos</h2><ul style="padding-left:18px;margin:0 0 14px">{items}</ul>'
               if items else "")
    return f"""<div style="{_WRAP}">
{_nav()}
<h1 style="{_H1}">Aprende haciendo, con tutora IA</h1>
<p style="{_P}">Dinos qué quieres ser: pega la oferta de trabajo que te interesa, o solo el nombre del puesto. Te armamos la ruta — qué módulos, en qué orden — y te decimos con nombre y apellido lo que ese puesto pide y nosotros no enseñamos.</p>
<p style="{_P}">Cada lección es un video corto con el porqué, una guía escrita con el cómo, y un ejercicio donde pegas el trabajo que hiciste de verdad. Tu tutora lo lee, te puntúa, te dice qué te falta para llegar a 100 y te hace una pregunta que solo puede contestar quien hizo el trabajo. Reintentas sin límite y siempre se queda tu mejor intento.</p>
<p style="{_P}">No damos certificados. Damos el trabajo que hiciste, con tu nombre: una estrategia, un plan de campaña, una auditoría — con enlace para compartir y PDF para imprimir.</p>
<h2 style="{_H2}">Haz una clase ahora, sin cuenta</h2>
<p style="{_P}">La primera lección del curso de Marketing con IA está abierta en esta página, entera. Mira el video, lee la guía y explícala con tus palabras: la tutora te responde de verdad antes de pedirte nada.</p>
{catalog}
<p style="{_SMALL}"><a href="/oferta" style="{_LINK}">Arma tu ruta desde una oferta de trabajo</a> · <a href="/login" style="{_LINK}">Ya tengo una invitación</a></p>
</div>"""


def catalog_html(courses: list[dict]) -> str:
    """The catalog as a link graph. This is how a crawler reaches all fourteen."""
    by_cat: dict[str, list[dict]] = {}
    for c in courses:
        by_cat.setdefault(c.get("category") or "Otros", []).append(c)

    blocks = []
    for cat in sorted(by_cat):
        cards = "".join(
            f'<a href="/curso/{_esc(c.get("slug"))}" style="{_CARD}">'
            f'<span style="font-family:Archivo,system-ui,sans-serif;font-weight:700;'
            f'font-size:16px;color:#F2EFE9;display:block;margin-bottom:4px">{_esc(c.get("title"))}</span>'
            f'<span style="{_P};margin:0">{_esc(c.get("description"))}</span>'
            f'<span style="{_SMALL};display:block;margin-top:8px">'
            f'{_esc(c.get("total"))} lecciones · {_esc(c.get("modules"))} módulos · '
            f'termina con: {_esc(c.get("doc_type"))}</span></a>'
            for c in by_cat[cat]
        )
        blocks.append(f'<h2 style="{_H2}">{_esc(cat)}</h2>{cards}')

    return f"""<div style="{_WRAP}">
{_nav()}
<h1 style="{_H1}">Cursos</h1>
<p style="{_P}">{len(courses)} cursos, cada uno de 30 lecciones en 5 módulos, todos en español. Cada curso termina en un entregable profesional hecho con tu propio trabajo. Puedes leer el temario completo antes de entrar.</p>
{"".join(blocks)}
</div>"""


def course_html(course: dict) -> str:
    """One temario: every module and every lesson objective, as readable text.

    This is the highest-value page in the set. A learner searching "curso de
    Meta Ads en español" is looking for exactly this, and there are fourteen of
    them, each carrying thirty real lesson titles.
    """
    mods = []
    for m in course.get("modules") or []:
        lessons = "".join(
            f'<li style="{_SMALL};margin-bottom:5px"><strong style="color:#B2AABB">'
            f'{_esc(l.get("title"))}</strong>'
            + (f' — {_esc(l.get("objectives"))}' if l.get("objectives") else "")
            + "</li>"
            for l in m.get("lessons") or []
        )
        desc = m.get("module_description")
        mods.append(
            f'<h3 style="{_H3}">Módulo {_esc(m.get("module_no"))} · {_esc(m.get("module_title"))}</h3>'
            + (f'<p style="{_P}">{_esc(desc)}</p>' if desc else "")
            + f'<ul style="padding-left:18px;margin:0 0 6px">{lessons}</ul>'
        )

    return f"""<div style="{_WRAP}">
{_nav()}
<p style="{_LABEL}">Temario completo</p>
<h1 style="{_H1}">{_esc(course.get("title"))}</h1>
<p style="{_P}">{_esc(course.get("description"))}</p>
<p style="{_SMALL}">{_esc(course.get("total"))} lecciones · {len(course.get("modules") or [])} módulos · termina con: <strong style="color:#B2AABB">{_esc(course.get("doc_type"))}</strong></p>
{"".join(mods)}
<p style="{_SMALL}"><a href="/cursos" style="{_LINK}">Ver todos los cursos</a> · <a href="/oferta" style="{_LINK}">Arma tu ruta desde una oferta de trabajo</a></p>
</div>"""


def simple_html(heading: str, paragraphs: list[str]) -> str:
    """For the surfaces whose value is the form, not the copy (/oferta, /lista,
    /login). They still need something a crawler can read and a link out."""
    body = "".join(f'<p style="{_P}">{_esc(p)}</p>' for p in paragraphs)
    return f"""<div style="{_WRAP}">
{_nav()}
<h1 style="{_H1}">{_esc(heading)}</h1>
{body}
</div>"""


def robots_txt(base_url: str) -> str:
    """Allow the public surfaces, keep crawlers out of the app and the API.

    `/aprende` and its share pages are excluded deliberately: they are a
    learner's own workspace and their documents live on unguessable tokens, and
    a token in a search index stops being unguessable.
    """
    base = (base_url or "").rstrip("/")
    lines = [
        "User-agent: *",
        "Allow: /$",
        "Allow: /cursos",
        "Allow: /curso/",
        "Allow: /oferta",
        "Allow: /lista",
        "Allow: /login",
        "Disallow: /api/",
        "Disallow: /panel",
        "Disallow: /media/",
        "Disallow: /aprende",
        "",
    ]
    if base:
        lines.append(f"Sitemap: {base}/sitemap.xml")
        lines.append("")
    return "\n".join(lines)


def sitemap_xml(base_url: str, slugs: list[str]) -> str:
    """Static surfaces plus one entry per course temario."""
    base = (base_url or "").rstrip("/")
    paths = ["/", "/cursos", "/oferta", "/lista", "/login"]
    paths += [f"/curso/{s}" for s in slugs]
    urls = "".join(
        f"<url><loc>{_esc(base + p)}</loc>"
        f"<changefreq>weekly</changefreq>"
        f"<priority>{'1.0' if p == '/' else '0.8' if p.startswith('/curso') else '0.6'}</priority>"
        f"</url>"
        for p in paths
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f"{urls}</urlset>")
