FROM python:3.11-slim-bullseye

WORKDIR /app
ENV PYTHONPATH="/app/MoneyPrinterTurbo" \
    PYTHONUNBUFFERED=1 \
    TZ=America/Santiago

RUN apt-get update && apt-get install -y --no-install-recommends git ffmpeg tzdata \
    && rm -rf /var/lib/apt/lists/*

# The render engine is an untracked clone beside this repo (docs/03), so it is
# NOT in the `railway up` upload context — the CLI honours .gitignore, which
# excludes it. This build survived on a BuildKit cache of the two COPY layers
# below until that cache aged out, at which point the deploy failed with
# "/MoneyPrinterTurbo: not found".
#
# The serving container never needed the engine's source. Nothing imports from
# it, `REPO` is used only to write config.toml and to read
# MoneyPrinterTurbo/storage (which .railwayignore already excluded, so it was
# never in the image), and the producer/publisher shell out to it on the
# operator's machine rather than in the container. Only the dependency list
# ships, as a tracked copy at the repo root.
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --retries 3 --timeout 60 -r requirements.txt \
    && pip install --no-cache-dir "psycopg[binary]" apscheduler

# entrypoint.py writes MoneyPrinterTurbo/config.toml here on boot, and
# PYTHONPATH points at it; the directory has to exist even though it is empty.
RUN mkdir -p /app/MoneyPrinterTurbo

COPY studio ./studio

# Renders and their approve/publish state live on the Railway volume, which the
# platform mounts at /app/studio/output (configured on the service, not here).
EXPOSE 8765
CMD ["python", "studio/cloud/entrypoint.py"]
