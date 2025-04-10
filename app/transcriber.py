import whisper
from app.utils import download_audio
from app.vectorstore import store_segments

model = whisper.load_model("base")

def transcribe_and_store_segments(audio_url, episode_id):
    path = download_audio(audio_url, episode_id)
    result = model.transcribe(path, verbose=True)
    segments = result.get("segments", [])

    diarized_segments = [
        {"speaker": f"SPEAKER_{i % 2:02d}", "text": s["text"], "start": s["start"], "end": s["end"]}
        for i, s in enumerate(segments)
    ]

    store_segments(diarized_segments, episode_id)
    return diarized_segments