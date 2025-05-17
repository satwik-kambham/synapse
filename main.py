from flask import Flask, request, send_file

from whisper import load_whisper, whisper_transcribe
from kokoro_tts import load_kokoro, kokoro_tts

CACHE_DIR = ""

whisper_pipeline = load_whisper()
kokoro_pipeline = load_kokoro()
app = Flask(__name__)


@app.route("/transcribe", methods=["POST"])
def transcribe():
    file = request.files["file"]
    file_bytes = file.read()
    transcription = whisper_transcribe(whisper_pipeline, file_bytes)
    return transcription

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text", "No text given")
    kokoro_tts(kokoro_pipeline, text)
    return send_file("tts.wav", mimetype="audio/wav")
