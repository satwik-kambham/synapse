from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import torch
from transformers import pipeline


class ProviderError(RuntimeError):
    pass


class STTProvider(ABC):
    @abstractmethod
    def transcribe(self, file_path: Path) -> str:
        raise NotImplementedError


class TTSProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str) -> Path:
        raise NotImplementedError


class WhisperSTTProvider(STTProvider):
    def __init__(
        self,
        model: str = "openai/whisper-small.en",
        chunk_length_s: int = 30,
    ) -> None:
        super().__init__()
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self._pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            chunk_length_s=chunk_length_s,
            device=device,
        )

    def transcribe(self, file_path: Path) -> str:
        try:
            return self._pipe(str(file_path))["text"]
        except (OSError, RuntimeError, ValueError, KeyError, TypeError) as exc:
            raise ProviderError("whisper provider failure") from exc


class DummyTTSProvider(TTSProvider):
    def synthesize(self, text: str) -> Path:
        return Path("nonexistent.wav")
