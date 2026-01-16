from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QColor
import sys
import psutil

class SubtitleSignal(QObject):
    update_text = pyqtSignal(str)
    update_stats = pyqtSignal(str, str, str) # status, cpu, ram

class SubtitleOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.signals = SubtitleSignal()
        self.signals.update_text.connect(self.set_text)
        self.signals.update_stats.connect(self.set_stats)

    def initUI(self):
        # Frameless and Always on Top
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False) # Allow dragging

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        # --- Status Bar (Top) ---
        self.status_bar = QFrame()
        self.status_bar.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 30, 200);
                border-radius: 8px;
            }
        """)
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(10, 5, 10, 5)

        # Status Label (Model Loading, etc.)
        self.status_label = QLabel("Initializing...")
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setStyleSheet("color: #00ff00;") # Green text
        
        # Stats Label (CPU / RAM)
        self.stats_label = QLabel("CPU: 0% | RAM: 0%")
        self.stats_label.setFont(QFont("Arial", 12))
        self.stats_label.setStyleSheet("color: #cccccc;") # Grey text
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.stats_label)
        self.status_bar.setLayout(status_layout)
        
        main_layout.addWidget(self.status_bar)

        # --- Subtitle Label (Center, Large) ---
        self.label = QLabel("Waiting for speech...")
        self.label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        # Large yellow text with black halo/background for readability
        self.label.setStyleSheet("""
            QLabel {
                color: #ffff00;
                background-color: rgba(0, 0, 0, 160);
                padding: 15px;
                border-radius: 12px;
            }
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        
        main_layout.addWidget(self.label)
        
        self.setLayout(main_layout)

        # Position at bottom center
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(100, screen.height() - 250, screen.width() - 200, 200)
        
        # Dragging variables
        self.oldPos = self.pos()

    def set_text(self, text):
        self.label.setText(text)

    def set_stats(self, status, cpu, ram):
        if status:
            self.status_label.setText(status)
        self.stats_label.setText(f"CPU: {cpu} | RAM: {ram}")

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

def run_ui(app):
    overlay = SubtitleOverlay()
    overlay.show()
    return overlay
