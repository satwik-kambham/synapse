FROM ghcr.io/astral-sh/uv:python3.13-trixie

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_NO_DEV=1 \
    PORT=8000

WORKDIR /app

COPY . /app
RUN uv sync --frozen --no-dev
RUN mkdir -p /app/uploads

VOLUME ["/app/uploads"]

EXPOSE 8000

CMD ["uv", "run", "main.py"]
