from __future__ import annotations

from pathlib import Path
from typing import Tuple
from uuid import uuid4

from flask import Flask, Response, jsonify, request, send_file

from providers import DummyTTSProvider, ProviderError, WhisperSTTProvider


def create_app(
    upload_dir: Path | None = None,
) -> Flask:
    app = Flask(__name__)

    stt = WhisperSTTProvider()
    tts = DummyTTSProvider()
    uploads = upload_dir or Path("uploads")
    uploads.mkdir(parents=True, exist_ok=True)

    @app.post("/stt")
    def stt_endpoint() -> Tuple[Response, int] | Response:
        if "file" not in request.files:
            return _json_error("file is required", 400)

        uploaded = request.files["file"]
        filename = f"{uuid4().hex}.wav"
        file_path = uploads / filename
        uploaded.save(file_path)

        try:
            text = stt.transcribe(file_path)
        except ProviderError:
            return _json_error("stt provider failure", 500)

        return jsonify({"text": text})

    @app.post("/tts")
    def tts_endpoint() -> Tuple[Response, int] | Response:
        payload = request.get_json(silent=True) or {}
        text = payload.get("text")
        if not isinstance(text, str) or not text.strip():
            return _json_error("text is required", 400)

        try:
            file_path = tts.synthesize(text)
        except ProviderError:
            return _json_error("tts provider failure", 500)

        if not file_path.exists():
            return _json_error("tts provider failure", 500)

        return send_file(file_path, mimetype="audio/wav")

    return app


def _json_error(message: str, status_code: int) -> Tuple[Response, int]:
    return jsonify({"error": message}), status_code
