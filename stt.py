from whisper import load_audio, load_model, pad_or_trim
from torch import cuda

class STT:
    def __init__(self):
        device = 'cuda' if cuda.is_available() else 'cpu'
        self.model = load_model('large', device=device)

    def transcribe_text(self, audio_path: str, source_language: str):
        audio = load_audio(audio_path)
        audio = pad_or_trim(audio)
        result = self.model.transcribe(audio_path, language=source_language)
        return result['text']

