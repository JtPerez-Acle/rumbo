"""Which request paths are the admin surface. One pure function, no imports.

This lives in its own module for one reason: it is the security predicate the
whole admin gate rests on, and it has to be auditable by anything that can run
Python — a check script, a CI step, a REPL — without dragging in FastAPI or the
rest of the app. It used to live in app.py, where auditing it meant importing a
web framework, and a checker run under the wrong interpreter silently skipped
the audit entirely and still printed a mostly-passing score.

THE RULE (docs/07): this is an ALLOWLIST. A new /api/* route that is not named
here ships PUBLIC. It nearly happened twice in one day, once with the invite-code
list, which would have published every access code to anyone who hit the URL.
Add the prefix in the same edit that adds the route, add a row to
check_public_surface.py's audit, and curl it tokenless before deploying.
"""
from __future__ import annotations

# The operator dashboard. "/" is deliberately NOT here: the root is the public
# site (docs/11). It used to be admin, which meant the most valuable URL in the
# product returned 401 to everyone who typed the domain.
_ADMIN_EXACT = ("/panel",)

_ADMIN_PREFIXES = (
    "/panel/",
    "/api/state",
    "/api/jobs",
    "/api/videos",
    "/media",                 # every rendered lesson on the volume
    "/api/upload-media",
    "/api/delete-media",
    "/api/requests",
    "/api/learners",          # names, emails, and everything they ever wrote
    "/api/waitlist",
    # Invite codes ARE the access gate — leaking this route would let anyone
    # mint themselves a login.
    "/api/invites",
    # The demand ledger: every posting strangers pasted, the roles they want and
    # what we cannot teach them. Competitive intelligence about our own catalog.
    "/api/demand",
    # Locked-out learners waiting for an access link — their email addresses.
    "/api/access-requests",
    "/api/submissions",
)


def is_admin_path(path: str) -> bool:
    """True when `path` belongs to the token-gated operator surface.

    Everything else — the public site, the learner app and its /api/learn/*
    routes — authenticates itself (session cookie) or is public by design.
    """
    if path in _ADMIN_EXACT:
        return True
    return path.startswith(_ADMIN_PREFIXES)
