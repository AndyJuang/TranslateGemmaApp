from pynput import keyboard
import threading

class GlobalInput:
    def __init__(self, toggle_callback):
        self.toggle_callback = toggle_callback
        self.listener = None
        # Default hotkey: Command + Option + Space (Mac friendly)
        # However, pynput on Mac might have permission issues if terminal doesn't have Input Monitoring.
        # Let's try a simple key data first, or a combo.
        # We'll use Option (Alt) + Space as requested in plan.
        
    def on_activate(self):
        print("Global hotkey pressed!")
        if self.toggle_callback:
            self.toggle_callback()

    def start(self):
        # <alt>+<space>
        self.listener = keyboard.GlobalHotKeys({
            '<alt>+<space>': self.on_activate
        })
        self.listener.start()
        print("Global input listener started. Press Option+Space to toggle recording.")

    def stop(self):
        if self.listener:
            self.listener.stop()
