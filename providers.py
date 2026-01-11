from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
import tempfile

import torch
from supertonic import TTS
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
    def __init__(self, voice_style: str = "M1") -> None:
        super().__init__()
        self._tts = TTS()
        self._style = self._tts.get_voice_style(voice_style)

    def synthesize(self, text: str) -> Path:
        try:
            wav, _ = self._tts.synthesize(text, self._style)
            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False,
            ) as tmp:
                output_path = Path(tmp.name)
            self._tts.save_audio(wav, str(output_path))
            return output_path
        except (OSError, RuntimeError, ValueError, TypeError) as exc:
            raise ProviderError("tts provider failure") from exc
