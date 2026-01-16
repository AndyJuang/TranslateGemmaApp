import sys
import threading
import time
import numpy as np
import psutil
from PyQt6.QtWidgets import QApplication

from audio_processor import AudioProcessor
from transcriber import Transcriber
from translator import Translator
from overlay_ui import SubtitleOverlay, run_ui
from global_input import GlobalInput

def main():
    # 1. Initialize UI Environment
    app = QApplication(sys.argv)
    overlay = SubtitleOverlay()
    overlay.show()
    
    # Force UI update
    app.processEvents()
    
    # 2. Initialize Components
    print("Initializing components...")
    overlay.signals.update_stats.emit("Loading Models...", "0%", "0%")
    app.processEvents() # Ensure UI shows loading state
    
    # Audio
    audio_proc = AudioProcessor()
    
    # Models
    try:
        overlay.signals.update_stats.emit("Loading Whisper...", "...", "...")
        app.processEvents()
        transcriber = Transcriber(model_size="base", device="cpu", compute_type="float32") 
        
        overlay.signals.update_stats.emit("Loading TranslateGemma...", "...", "...")
        app.processEvents()
        translator = Translator(model_path="google/translategemma-4b-it")
        
        overlay.signals.update_stats.emit("Models Loaded. Ready.", "...", "...")
    except Exception as e:
        print(f"Error loading models: {e}")
        overlay.signals.update_text.emit(f"Error loading models: {e}")
        return

    # shared state
    state = {"recording": False}
    
    # 3. Define Logic
    def toggle_recording():
        state["recording"] = not state["recording"]
        if state["recording"]:
            print("Toggle ON")
            overlay.signals.update_text.emit("Listening...")
            audio_proc.start_recording()
        else:
            print("Toggle OFF")
            overlay.signals.update_text.emit("Paused")
            audio_proc.stop_recording()

    # 4. Input Listener
    global_input = GlobalInput(toggle_callback=toggle_recording)
    global_input.start()

    # 5. Stats Monitoring Loop
    def stats_loop():
        while True:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            
            status_text = "" # Don't overwrite status unless changed
            if state["recording"]:
                status_text = "Recording..."
            else:
                status_text = "Ready" 
                
            overlay.signals.update_stats.emit(status_text, f"{cpu}%", f"{mem}%")
            time.sleep(1) # Update every second

    stats_thread = threading.Thread(target=stats_loop, daemon=True)
    stats_thread.start()

    # 6. Processing Loop
    def processing_loop():
        buffer = np.array([], dtype=np.float32)
        SAMPLE_RATE = 16000
        CHUNK_THRESHOLD = SAMPLE_RATE * 3 # 3 seconds
        
        print("Ready to record. Press Option+Space.")
        
        while True:
            chunk = audio_proc.get_audio_chunk()
            if chunk is not None:
                buffer = np.append(buffer, chunk)
                
                # Check if buffer is long enough
                if len(buffer) >= CHUNK_THRESHOLD:
                    # Transcribe
                    try:
                        overlay.signals.update_stats.emit("Transcribing...", "", "")
                        text, lang = transcriber.transcribe(buffer)
                        if text.strip():
                            print(f"Detected ({lang}): {text}")
                            
                            # Translate
                            overlay.signals.update_stats.emit("Translating...", "", "")
                            translation = translator.translate(text, source_lang=lang, target_lang="en")
                            print(f"Translated: {translation}")
                            
                            overlay.signals.update_text.emit(translation)
                        else:
                            pass
                            
                    except Exception as e:
                        print(f"Error processing: {e}")
                    
                    # Reset buffer
                    buffer = np.array([], dtype=np.float32)
            else:
                time.sleep(0.01)

    # Start processing thread
    proc_thread = threading.Thread(target=processing_loop, daemon=True)
    proc_thread.start()

    # 7. Run UI Loop
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        pass
    finally:
        audio_proc.terminate()
        global_input.stop()

if __name__ == "__main__":
    main()
