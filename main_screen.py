from threading import Thread
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from recorder import Recorder
from stt import STT
from idioms import IDIOMS
from path_utils import remove_path


class MainScreen(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        try:
            self.title('Speech To Text')
            self.geometry('400x300')
            self.recorder = Recorder()
            self.stt = STT()
            if (self.stt.model):
                self.idioms_options = list(IDIOMS.keys())
                
                buttons_frame = ttk.Frame(self)
                buttons_frame.pack(fill=tk.X, padx=10, pady=10)
                self.start_record_button = ttk.Button(buttons_frame, text='Record', command=self.start_record)
                self.stop_record_button = ttk.Button(buttons_frame, text='Stop', command=self.stop_record)
                self.start_record_button.pack(side=tk.LEFT, expand=True, fill=tk.X)
                self.stop_record_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

                source_language_frame = ttk.Frame(self)
                source_language_frame.pack(anchor='w', pady=5, padx=10)
                source_language_label = ttk.Label(source_language_frame, text='Source Language:')
                source_language_label.pack(side=tk.LEFT)
                self.source_language_idioms = tk.StringVar(self)
                self.source_language_menu = ttk.OptionMenu(source_language_frame, self.source_language_idioms, *self.idioms_options)
                self.source_language_menu.pack(side=tk.LEFT, padx=5)
                self._deactivate_widget(self.stop_record_button)

                image_frame = ttk.Frame(self)
                image_frame.pack(anchor='w', pady=5, padx=10)
                image_label = ttk.Label(image_frame, text='Select Audio:')
                image_label.pack(side=tk.LEFT, padx=5)

                self.audio_entry = tk.Entry(image_frame)
                self.audio_entry.pack(side=tk.LEFT, padx=5)
                self.select_audio_button = ttk.Button(image_frame, text='Select', command=self.select_audio)
                self.select_audio_button.pack(side=tk.LEFT, padx=5)
                self._deactivate_widget(self.audio_entry)

                play_audio_frame = ttk.Frame(self)
                play_audio_frame.pack(fill=tk.X, padx=10, pady=10)
                self.play_audio_button = ttk.Button(play_audio_frame, text='Play Audio', command=self.play_audio)
                self.play_audio_button.pack(side=tk.LEFT, expand=True, fill=tk.X)
                self.transcribe_button = ttk.Button(play_audio_frame, text='Transcribe', command=self.transcribe)
                self.transcribe_button.pack(side=tk.LEFT, expand=True, fill=tk.X)
                self._deactivate_widget(self.play_audio_button)
                self._deactivate_widget(self.transcribe_button)

                self.status_label = ttk.Label(self)
                self.status_label.pack(anchor='w', padx=10)

                text_frame = ttk.Frame(self)
                text_frame.pack(fill=tk.X, padx=10, pady=10)
                self.text_entry = tk.Text(text_frame, width=50, height=5)
                self.text_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
                self._deactivate_widget(self.text_entry)

                self.mainloop()

        except Exception as e:
            messagebox.showerror('Error', e)

    def start_record(self):
        self._deactivate_widget(self.transcribe_button)
        self._deactivate_widget(self.select_audio_button)
        self._deactivate_widget(self.play_audio_button)
        Thread(target=self.recorder.record_audio, daemon=True).start()
        self._deactivate_widget(self.start_record_button)
        self._activate_widget(self.stop_record_button)
        self.status_label.config(text='Recording...')

    def stop_record(self):
        self.recorder.stop_record()
        self._deactivate_widget(self.stop_record_button)
        self._activate_widget(self.start_record_button)
        self._activate_widget(self.play_audio_button)
        self._activate_widget(self.transcribe_button)
        self._activate_widget(self.select_audio_button)
        self._activate_widget(self.audio_entry)
        self.audio_entry.delete(0, tk.END)
        self._deactivate_widget(self.audio_entry)
        self.status_label.config(text='')

    def select_audio(self):
        audio_path = filedialog.askopenfilename()
        if(audio_path):
            self.recorder.audio_path = audio_path
            audio_name = remove_path(audio_path)
            self._activate_widget(self.audio_entry)
            self.audio_entry.delete(0, tk.END)
            self.audio_entry.insert(0, audio_name)
            self._deactivate_widget(self.audio_entry)
            self._activate_widget(self.play_audio_button)
            self._activate_widget(self.transcribe_button)

    def play_audio(self):
        if(self.recorder.is_audio_exists):
            Thread(target=self.recorder.play_audio, daemon=True).start()
        
    def transcribe_audio(self):
        source_language = self.source_language_idioms.get()
        source_language = IDIOMS[source_language]
        if(source_language):
            result = self.stt.transcribe_text(self.recorder.audio_path, source_language)
            self._activate_widget(self.text_entry)
            self.text_entry.delete('1.0', tk.END)
            self.text_entry.insert('1.0', result)
            self._deactivate_widget(self.text_entry)

        else:
            messagebox.showerror('Error', 'Select source language.')
        
        self._activate_widget(self.start_record_button)
        self._activate_widget(self.stop_record_button)
        self._activate_widget(self.transcribe_button)
        self._activate_widget(self.select_audio_button)
        self._activate_widget(self.source_language_menu)
        self.status_label.config(text='')

    def transcribe(self):
        self._deactivate_widget(self.start_record_button)
        self._deactivate_widget(self.stop_record_button)
        self._deactivate_widget(self.transcribe_button)
        self._deactivate_widget(self.select_audio_button)
        self._deactivate_widget(self.source_language_menu)
        self.status_label.config(text='Transcribing...')
        Thread(target=self.transcribe_audio, daemon=True).start()
        

    def _deactivate_widget(self, widget):
        widget.config(state='disabled')

    def _activate_widget(self, widget):
        widget.config(state='normal')