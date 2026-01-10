# Repository Guidelines

## Project Structure & Module Organization
- `main.py` boots the Flask app and reads `PORT` (defaults to 8000).
- `app.py` defines the HTTP API routes (`/stt`, `/tts`) and request handling.
- `providers.py` contains provider abstractions plus the Whisper STT and dummy TTS implementations.
- `uploads/` is created at runtime to store uploaded audio files.

## Build, Test, and Development Commands
- `uv sync` installs dependencies from `pyproject.toml`.
- `uv run main.py` starts the API server at `http://localhost:8000`.
- `uv run ruff check .` runs lint checks (ruff is listed in dev deps).

## Coding Style & Naming Conventions
- Python 3.13+ (see `pyproject.toml`); type hints are used throughout.
- Prefer snake_case for functions/variables and PascalCase for classes.
- Keep modules small and focused; add new providers in `providers.py` or a new module if it grows.
- Use ruff for linting; format is currently not enforced by a tool.

## Commit Guidelines
- Commits follow a Conventional Commits style (`feat:`, `chore:`). Keep messages short and scoped.
- If changing API behavior, include updated request/response examples in `README.md`.
