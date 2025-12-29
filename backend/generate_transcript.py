from faster_whisper import WhisperModel

def generate_transcript(filename):
    # Load the model (you can use "tiny", "base", "small", etc.)
    model = WhisperModel("tiny", compute_type="int8")  # "int8" for speed, "float32" for accuracy

    # Transcribe with specified language (e.g., "hi" for Hindi)
    segments, _ = model.transcribe(filename)

    transcript = ""
    for segment in segments:
        transcript += segment.text.strip() + " "

    return transcript.strip()
