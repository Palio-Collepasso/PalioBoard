FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

RUN pip install --no-cache-dir "uv>=0.8.15,<0.9.0"

COPY apps/api/pyproject.toml /app/pyproject.toml
COPY apps/api/uv.lock /app/uv.lock
COPY apps/api/README.md /app/README.md
RUN uv sync --frozen --no-install-project

COPY apps/api /app
RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "src/palio/app/main.py", "--host", "0.0.0.0", "--port", "8000"]
