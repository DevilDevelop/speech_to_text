from queue import Queue
from sounddevice import InputStream
from soundfile import SoundFile
from playaudio import playaudio
from path_utils import join_dirname, check_file_exists


class Recorder:
    def __init__(self):
        self.audio_path = join_dirname('audio.wav')
        self.is_recording = False
        self.sample_rate = 192000
        self.channels = 1
        self.queue = Queue()

    @property
    def is_audio_exists(self):
        return check_file_exists(self.audio_path)
        
    def _record_callback(self, indata, frames, time, status):
        self.queue.put(indata.copy())
    
    def record_audio(self):
        self.is_recording = True
        with SoundFile(self.audio_path, mode='w', samplerate=self.sample_rate, channels=self.channels, subtype='PCM_16') as file:
            with InputStream(samplerate=self.sample_rate, channels=self.channels, callback=self._record_callback):
                while self.is_recording:
                    file.write(self.queue.get())

    def play_audio(self):
        playaudio(self.audio_path)

    def stop_record(self):
        self.is_recording = False
    
