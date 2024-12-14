from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import sys
import queue
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QWidget, QTextEdit,
                           QLabel, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon
import pyperclip
import os

# Initialize the Whisper model
model = WhisperModel("base", device="cpu", compute_type="int8")

# Audio recording settings
SAMPLE_RATE = 16000
audio_queue = queue.Queue()

class AudioRecorder(QThread):
    transcription_done = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.stream = None
        self.recording = False
        self.audio_data = []
    
    def run(self):
        def audio_callback(indata, frames, time, status):
            if self.recording:
                self.audio_data.append(indata.copy())
        
        self.recording = True
        self.audio_data = []
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            callback=audio_callback
        )
        
        with self.stream:
            while self.recording:
                self.msleep(10)
        
        if self.audio_data:
            audio_array = np.concatenate(self.audio_data)
            segments, _ = model.transcribe(audio_array.flatten(), language="en")
            text = " ".join([segment.text for segment in segments])
            self.transcription_done.emit(text.strip())
    
    def stop_recording(self):
        self.recording = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.recorder = AudioRecorder()
        self.recorder.transcription_done.connect(self.on_transcription)
        self.transcription_history = []
        self.history_index = -1
        
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Windows Whisper")
        base_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_path, 'assets', 'icon.ico')
        self.setWindowIcon(QIcon(icon_path))
        self.setMinimumSize(600, 400)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Status label
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        # Text area
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Your speech will appear here. You can edit the text after transcription.")
        layout.addWidget(self.text_edit)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Record button
        self.record_button = QPushButton("Hold to Speak")
        self.record_button.pressed.connect(self.start_recording)
        self.record_button.released.connect(self.stop_recording)
        button_layout.addWidget(self.record_button)
        
        # Copy button
        copy_button = QPushButton("Copy")
        copy_button.clicked.connect(self.copy_text)
        button_layout.addWidget(copy_button)
        
        # Undo button
        undo_button = QPushButton("Undo")
        undo_button.clicked.connect(self.undo_last)
        button_layout.addWidget(undo_button)

        # Clear button
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_text)
        button_layout.addWidget(clear_button)
        
        layout.addLayout(button_layout)
        
        # Set up keyboard shortcuts
        self.shortcut_copy = self.create_shortcut("Ctrl+C", self.copy_text)
        self.shortcut_undo = self.create_shortcut("Ctrl+Z", self.undo_last)
    
    def create_shortcut(self, key, slot):
        from PyQt6.QtGui import QShortcut, QKeySequence
        return QShortcut(QKeySequence(key), self, slot)
    
    def start_recording(self):
        self.status_label.setText("Recording...")
        self.record_button.setStyleSheet("background-color: red")
        self.recorder.start()
    
    def stop_recording(self):
        self.status_label.setText("Processing...")
        self.record_button.setStyleSheet("")
        self.recorder.stop_recording()
    
    def on_transcription(self, text):
        if text:
            cursor = self.text_edit.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            if not self.text_edit.toPlainText().endswith('\n') and self.text_edit.toPlainText() != '':
                cursor.insertText('\n')
            cursor.insertText(text)
            self.text_edit.setTextCursor(cursor)
            # Store the current state for undo
            self.transcription_history.append(self.text_edit.toPlainText())
            self.history_index = len(self.transcription_history) - 1
        self.status_label.setText("Ready - You can now edit the text if needed")
    
    def copy_text(self):
        text = self.text_edit.toPlainText()
        if text:
            pyperclip.copy(text)
            self.status_label.setText("Text copied to clipboard!")
        else:
            self.status_label.setText("No text to copy")
    
    def undo_last(self):
        if self.history_index > 0:
            self.history_index -= 1
            # Store the current text before undo for potential redo
            current_text = self.text_edit.toPlainText()
            if current_text != self.transcription_history[-1]:
                self.transcription_history.append(current_text)
            
            self.text_edit.setPlainText(self.transcription_history[self.history_index])
            self.status_label.setText("Undo successful")
        else:
            self.text_edit.clear()
            self.status_label.setText("Nothing more to undo")

    def clear_text(self):
        if self.text_edit.toPlainText():
            # Store the current text before clearing for undo
            self.transcription_history.append(self.text_edit.toPlainText())
            self.history_index = len(self.transcription_history) - 1
        
        self.text_edit.clear()
        self.status_label.setText("Text cleared")
    
def main():
    app = QApplication(sys.argv)
    base_path = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_path, 'assets', 'icon.ico')
    app.setWindowIcon(QIcon(icon_path))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
