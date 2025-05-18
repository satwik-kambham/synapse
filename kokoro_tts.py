from kokoro import KPipeline
import soundfile as sf
import torch

def load_kokoro():
    pipeline = KPipeline(lang_code="a")
    return pipeline


def kokoro_tts(pipeline, text):
    generator = pipeline(text, voice="af_heart")
    audio_combined = []
    for i, (gs, ps, audio) in enumerate(generator):
        audio_combined.append(audio)
    audio_combined = torch.cat(audio_combined)
    sf.write("tts.wav", audio_combined, 24000)
