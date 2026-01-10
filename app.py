from __future__ import annotations

import io
import wave
from typing import Tuple

from flask import Flask, Response, jsonify, request

from providers import DummySTTProvider, DummyTTSProvider, ProviderError, STTProvider, TTSProvider


def create_app(
    stt_provider: STTProvider | None = None,
    tts_provider: TTSProvider | None = None,
) -> Flask:
    app = Flask(__name__)

    stt = stt_provider or DummySTTProvider()
    tts = tts_provider or DummyTTSProvider()

    @app.post("/stt")
    def stt_endpoint() -> Tuple[Response, int] | Response:
        if "file" not in request.files:
            return _json_error("file is required", 400)

        uploaded = request.files["file"]
        if not _is_wav_mimetype(uploaded.mimetype):
            return _json_error("file must be audio/wav", 400)

        wav_bytes = uploaded.read()
        if not _has_wav_header(wav_bytes):
            return _json_error("file must be WAV", 400)

        if not _can_decode_wav(wav_bytes):
            return _json_error("unable to decode WAV", 422)

        try:
            text = stt.transcribe(wav_bytes)
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
            wav_bytes = tts.synthesize(text)
        except ProviderError:
            return _json_error("tts provider failure", 500)

        if not _has_wav_header(wav_bytes) or not _can_decode_wav(wav_bytes):
            return _json_error("tts provider returned invalid WAV", 500)

        return Response(wav_bytes, mimetype="audio/wav")

    return app


def _json_error(message: str, status_code: int) -> Tuple[Response, int]:
    return jsonify({"error": message}), status_code


def _is_wav_mimetype(mimetype: str | None) -> bool:
    return mimetype in {"audio/wav", "audio/x-wav", "audio/wave"}


def _has_wav_header(wav_bytes: bytes) -> bool:
    return len(wav_bytes) >= 12 and wav_bytes[:4] == b"RIFF" and wav_bytes[8:12] == b"WAVE"


def _can_decode_wav(wav_bytes: bytes) -> bool:
    try:
        with wave.open(io.BytesIO(wav_bytes), "rb") as wav_file:
            wav_file.getparams()
        return True
    except (wave.Error, EOFError, ValueError):
        return False
