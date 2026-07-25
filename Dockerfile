FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# STAGE 2: RUNTIME
FROM python:3.11-slim AS runtime

WORKDIR /app

# Explicitly add /app to PYTHONPATH so src package imports resolve cleanly
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/root/.local/bin:$PATH"

COPY --from=builder /root/.local /root/.local
COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.agent_endpoint:app", "--host", "0.0.0.0", "--port", "8000"]