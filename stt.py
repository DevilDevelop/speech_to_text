from whisper import load_audio, load_model, pad_or_trim


class STT:
    def __init__(self):
        self.model = load_model('turbo', device='cpu')

    def transcribe_text(self, audio_path: str, source_language: str):
        audio = load_audio(audio_path)
        audio = pad_or_trim(audio)
        result = self.model.transcribe(audio, language=source_language)
        return result['text']

