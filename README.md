# Synapse

Inference Server (STT, TTS, ...)

## Run the API server

Install dependencies:
```bash
uv sync
```

Start the server:
```bash
uv run main.py
```

## Connect to the server

The server listens on `http://localhost:8000` by default.

## API specification

Base URL: `http://localhost:8000`

### `POST /stt`

Transcribe a WAV file to text.

Request:
- Content-Type: `multipart/form-data`
- Form field: `file` (WAV audio)

Response (200):
```json
{"text": "transcribed text"}
```

Errors:
- 400: `{"error": "file is required"}`
- 500: `{"error": "stt provider failure"}`

Example:
```bash
curl -X POST http://localhost:8000/stt \
  -F "file=@/path/to/audio.wav"
```

### `POST /tts`

Synthesize speech from text.

Request:
- Content-Type: `application/json`
- Body: `{"text": "hello world"}`

Response (200):
- Content-Type: `audio/wav`
- Body: WAV audio bytes

Errors:
- 400: `{"error": "text is required"}`
- 500: `{"error": "tts provider failure"}`

Example:
```bash
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"hello world"}' \
  --output speech.wav
```
