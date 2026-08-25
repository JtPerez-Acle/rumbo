"""Container entrypoint: render MoneyPrinterTurbo's config.toml from env vars,
initialize the Postgres schema, then serve the dashboard (which also hosts the
scheduler when ENABLE_SCHEDULER=1).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

STUDIO = Path(__file__).resolve().parents[1]
ROOT = STUDIO.parent
REPO = ROOT / "MoneyPrinterTurbo"
sys.path.insert(0, str(STUDIO))

CONFIG_TEMPLATE = """\
log_level = "INFO"
listen_host = "127.0.0.1"
listen_port = 8080

[app]
hide_config = false
edge_tts_timeout = 30
tls_verify = true
video_source = "pexels"
pexels_api_keys = ["{pexels_key}"]
pixabay_api_keys = []
subtitle_provider = "edge"
endpoint = ""
material_directory = ""
enable_redis = false
max_concurrent_tasks = 2
max_queued_tasks = 50
llm_provider = "openai"

[whisper]
model_size = "large-v3"
device = "cpu"
compute_type = "int8"

[proxy]

[azure]
speech_key = ""
speech_region = ""

[siliconflow]
api_key = ""

[elevenlabs]
api_key = ""

[ui]
hide_log = false
"""


def render_config() -> None:
    pexels_key = os.environ.get("PEXELS_API_KEY", "")
    if not pexels_key:
        print("WARNING: PEXELS_API_KEY not set — rendering will fail", flush=True)
    (REPO / "config.toml").write_text(
        CONFIG_TEMPLATE.format(pexels_key=pexels_key), encoding="utf-8"
    )


def main() -> None:
    render_config()

    from cloud import db
    if db.enabled():
        db.init_db()
        print("postgres schema ready", flush=True)
    else:
        print("DATABASE_URL not set — running without topic DB", flush=True)

    port = int(os.environ.get("PORT", "8765"))
    import uvicorn
    sys.path.insert(0, str(STUDIO / "dashboard"))
    from app import app  # dashboard FastAPI app (starts scheduler if enabled)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


if __name__ == "__main__":
    main()
