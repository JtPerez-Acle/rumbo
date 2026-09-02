"""The public site: serving the built frontend, and deciding who sees it.

WHAT CHANGED AND WHY. These six URLs used to be the learner SPA with a hand-
written body injected into it by prerender.py, plus a `window.__BOOT__` payload
so hydration would not immediately re-fetch what the server had just used. It
worked and it was still wrong: the served document and the hydrated one were
never the same markup, so a visitor watched one page turn into another. Four
attempts fixed how that transition looked. None of them could fix it, because
the problem was that there were two documents.

Now there is one, built by Astro at image-build time, and this module does two
things with it: find the file, and keep learners out of it.

THE REDIRECT RULE. A learner with a session never sees these pages. The public
header would otherwise have to discover their auth state after load and change
itself — which is the same flicker in a smaller frame. So a signed-in visitor is
sent into the app instead, at the view that corresponds to where they were going.
`/lista` is the exception: a waitlist form does nothing for someone already
inside, but it also breaks nothing, and it is the one page nobody arrives at
with a session.

This module is dependency-free apart from Starlette's responses, for the same
reason admin_paths.py is: it can be imported and asserted by a check script
running under any interpreter.
"""
from __future__ import annotations

from pathlib import Path

DIST = Path(__file__).parent / "static" / "web"

# Where a signed-in visitor goes instead of each public page. The app is still
# hash-routed internally, so these are fragments on /aprende (phase 3 turns them
# into real paths and this table is where that change lands).
SIGNED_IN_DESTINATION = {
    "/": "/aprende",
    "/cursos": "/aprende#/cursos",
    "/oferta": "/aprende#/oferta",
    "/login": "/aprende",
}


def page(route: str) -> Path:
    """The built HTML for a public route.

    Astro emits directory-style output — /cursos becomes cursos/index.html — so
    a URL maps to a path by appending index.html, and the root is the only
    special case.
    """
    rel = route.strip("/")
    return DIST / (f"{rel}/index.html" if rel else "index.html")


def exists(route: str) -> bool:
    return page(route).is_file()


def course_slugs() -> list[str]:
    """Slugs that have a built page, read off the build output itself.

    Deliberately NOT a database query and not the exported JSON either. The
    sitemap must list pages that EXIST, and after the build that set is decided
    by what Astro emitted — a course added to the database since the last deploy
    has no page, and advertising it to a crawler publishes a 404. Reading the
    directory cannot disagree with the directory.
    """
    return sorted(p.parent.name for p in DIST.glob("curso/*/index.html"))


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

    def esc(value: str) -> str:
        return (value.replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;").replace('"', "&quot;"))

    urls = "".join(
        f"<url><loc>{esc(base + p)}</loc>"
        f"<changefreq>weekly</changefreq>"
        f"<priority>{'1.0' if p == '/' else '0.8' if p.startswith('/curso') else '0.6'}</priority>"
        f"</url>"
        for p in paths
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f"{urls}</urlset>")
