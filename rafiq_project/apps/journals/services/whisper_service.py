import whisper

model = whisper.load_model("small")

def transcribe_audio_file(file_path: str):
    """
    Transcribe audio in any language using Whisper.
    Returns (text, detected_language)
    """

    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    _, probs = model.detect_language(mel)
    detected_lang = max(probs, key=probs.get)

    result = whisper.decode(model, mel, whisper.DecodingOptions()
    )
    
    return result.text.strip(), detected_lang