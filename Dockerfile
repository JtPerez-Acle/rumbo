FROM python:3.11-slim-bullseye

WORKDIR /app
ENV PYTHONPATH="/app/MoneyPrinterTurbo" \
    PYTHONUNBUFFERED=1 \
    TZ=America/Santiago

RUN apt-get update && apt-get install -y --no-install-recommends git ffmpeg tzdata \
    && rm -rf /var/lib/apt/lists/*

COPY MoneyPrinterTurbo/requirements.txt ./MoneyPrinterTurbo/requirements.txt
RUN pip install --no-cache-dir --retries 3 --timeout 60 -r MoneyPrinterTurbo/requirements.txt \
    && pip install --no-cache-dir "psycopg[binary]" apscheduler

COPY MoneyPrinterTurbo ./MoneyPrinterTurbo
COPY studio ./studio

# Renders and their approve/publish state live on the Railway volume, which the
# platform mounts at /app/studio/output (configured on the service, not here).
EXPOSE 8765
CMD ["python", "studio/cloud/entrypoint.py"]
