from faster_whisper import WhisperModel
import numpy as np

class Transcriber:
    def __init__(self, model_size="medium", device="cpu", compute_type="int8"):
        print(f"Loading Whisper model: {model_size} on {device}...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print("Whisper model loaded.")

    def transcribe(self, audio_data):
        # audio_data should be a numpy array of float32
        segments, info = self.model.transcribe(audio_data, beam_size=5, vad_filter=True)
        
        text = ""
        for segment in segments:
            text += segment.text + " "
        
        return text.strip(), info.language
