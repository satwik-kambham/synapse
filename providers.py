from __future__ import annotations

from abc import ABC, abstractmethod
import io
import threading
import wave


class ProviderError(RuntimeError):
    pass


class STTProvider(ABC):
    @abstractmethod
    def transcribe(self, wav_bytes: bytes) -> str:
        raise NotImplementedError


class TTSProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        raise NotImplementedError


class _LazyLoadMixin:
    def __init__(self) -> None:
        self._load_lock = threading.Lock()
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        with self._load_lock:
            if self._loaded:
                return
            self._load()
            self._loaded = True
            self._warmup()

    def _load(self) -> None:
        pass

    def _warmup(self) -> None:
        pass


class DummySTTProvider(_LazyLoadMixin, STTProvider):
    def __init__(self, transcript: str = "") -> None:
        super().__init__()
        self._transcript = transcript

    def transcribe(self, wav_bytes: bytes) -> str:
        self._ensure_loaded()
        return self._transcript


class DummyTTSProvider(_LazyLoadMixin, TTSProvider):
    def __init__(self, sample_rate: int = 16000) -> None:
        super().__init__()
        self._sample_rate = sample_rate

    def synthesize(self, text: str) -> bytes:
        self._ensure_loaded()
        return _silence_wav(sample_rate=self._sample_rate, duration_sec=1.0)


def _silence_wav(sample_rate: int, duration_sec: float) -> bytes:
    frame_count = int(sample_rate * duration_sec)
    silence = b"\x00\x00" * frame_count
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(silence)
    return buffer.getvalue()
