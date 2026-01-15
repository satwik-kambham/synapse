from __future__ import annotations

import argparse
import sys
from pathlib import Path

from providers import (
    SuperTonicTTSProvider,
    ProviderError,
    WhisperTurboSTTProvider,
    WhisperSTTProvider,
)


def _handle_stt(args: argparse.Namespace) -> int:
    file_path = Path(args.audio_path)
    if not file_path.exists():
        print(f"audio file not found: {file_path}", file=sys.stderr)
        return 2

    provider = WhisperSTTProvider()
    try:
        text = provider.transcribe(file_path)
    except ProviderError:
        print("stt provider failure", file=sys.stderr)
        return 1

    print(text)
    return 0


def _handle_tts(args: argparse.Namespace) -> int:
    provider = SuperTonicTTSProvider()
    try:
        output_path = provider.synthesize(args.text)
    except ProviderError:
        print("tts provider failure", file=sys.stderr)
        return 1

    print(output_path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Synapse CLI for speech-to-text and text-to-speech.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    stt_parser = subparsers.add_parser("stt", help="Transcribe a WAV file.")
    stt_parser.add_argument("audio_path", help="Path to a .wav file to transcribe.")
    stt_parser.set_defaults(func=_handle_stt)

    tts_parser = subparsers.add_parser("tts", help="Synthesize text to a WAV file.")
    tts_parser.add_argument("text", help="Text to synthesize.")
    tts_parser.set_defaults(func=_handle_tts)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
