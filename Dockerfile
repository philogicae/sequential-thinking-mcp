FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0
WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock README.md /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

# Install project
COPY sequential_thinking /app/sequential_thinking
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

FROM python:3.13-alpine
COPY --from=builder --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["sequential-thinking-mcp", "--mode", "sse"]