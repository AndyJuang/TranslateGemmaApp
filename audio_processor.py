import pyaudio
import queue
import threading
import numpy as np

class AudioProcessor:
    def __init__(self, rate=16000, chunk=1024, channels=1):
        self.rate = rate
        self.chunk = chunk
        self.channels = channels
        self.audio_interface = pyaudio.PyAudio()
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.stream = None
        self.thread = None

    def start_recording(self):
        if self.is_recording:
            return
        
        self.is_recording = True
        self.stream = self.audio_interface.open(
            format=pyaudio.paFloat32,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self._audio_callback
        )
        self.stream.start_stream()
        print("Recording started...")

    def stop_recording(self):
        if not self.is_recording:
            return
            
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        print("Recording stopped.")

    def _audio_callback(self, in_data, frame_count, time_info, status):
        if self.is_recording:
            audio_data = np.frombuffer(in_data, dtype=np.float32)
            self.audio_queue.put(audio_data)
        return (in_data, pyaudio.paContinue)

    def get_audio_chunk(self):
        try:
            return self.audio_queue.get(timeout=0.1)
        except queue.Empty:
            return None

    def terminate(self):
        self.stop_recording()
        self.audio_interface.terminate()
