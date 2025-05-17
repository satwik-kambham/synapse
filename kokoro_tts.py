from kokoro import KPipeline
import soundfile as sf


def load_kokoro():
    pipeline = KPipeline(lang_code="a")
    return pipeline


def kokoro_tts(pipeline, text):
    generator = pipeline(text, voice="af_heart", split_pattern=None)
    for i, (gs, ps, audio) in enumerate(generator):
        print(i)
        sf.write("tts.wav", audio, 24000)
