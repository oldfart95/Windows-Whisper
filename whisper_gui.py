import tkinter as tk
from tkinter import ttk, messagebox
import faster_whisper
import sounddevice as sd
import numpy as np
import queue
import threading
import platform
import torch
import pyperclip

class WhisperApp:
    def __init__(self, root):
        self.root = root
        self.text_history = []
        self.history_index = -1
        self.setup_ui()
        self.setup_audio()
        self.setup_model()
        
    def save_text_state(self):
        """Save current text state to history"""
        try:
            current_text = self.text_area.get("1.0", tk.END).strip()
            if current_text:
                # Initialize history if empty
                if not self.text_history:
                    self.text_history = [current_text]
                    self.history_index = 0
                    self.logger.debug("Initialized text history")
                    return
                
                # Only save if text has changed
                if current_text != self.text_history[self.history_index]:
                    # If we're not at the end of history, truncate future states
                    if self.history_index < len(self.text_history) - 1:
                        self.text_history = self.text_history[:self.history_index + 1]
                        self.logger.debug("Truncated future history states")
                    
                    self.text_history.append(current_text)
                    self.history_index = len(self.text_history) - 1
                    self.logger.debug(f"Saved new state. History length: {len(self.text_history)}")
                    
                    # Limit history to 50 states
                    if len(self.text_history) > 50:
                        self.text_history.pop(0)
                        self.history_index -= 1
                        self.logger.debug("Trimmed history to 50 states")
        except Exception as e:
            self.logger.error(f"Failed to save text state: {str(e)}", exc_info=True)
        
    def setup_ui(self):
        self.root.title("Whisper Speech-to-Text")
        self.root.geometry("800x600")
        
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Settings frame
        settings_frame = ttk.Frame(self.root)
        settings_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        # Model size selection
        ttk.Label(settings_frame, text="Model:").grid(row=0, column=0, padx=5)
        self.model_var = tk.StringVar(value="base")
        model_menu = ttk.OptionMenu(
            settings_frame,
            self.model_var,
            "base",
            "tiny", "base", "small", "medium", "large"
        )
        model_menu.grid(row=0, column=1, padx=5)
        
        # Add logging
        import logging
        logging.basicConfig(
            filename='whisper.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger()
        self.logger.debug("Logging initialized at DEBUG level")
        
        # Main text area
        self.text_area = tk.Text(self.root, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Control frame
        control_frame = ttk.Frame(self.root)
        control_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        # Buttons
        self.listen_btn = ttk.Button(
            control_frame,
            text="Press to Listen",
            command=self.toggle_listen
        )
        self.listen_btn.grid(row=0, column=0, padx=5)
        
        ttk.Button(
            control_frame,
            text="Copy Text",
            command=self.copy_text
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            control_frame,
            text="Undo Last",
            command=self.undo_text
        ).grid(row=0, column=2, padx=5)
        
        ttk.Button(
            control_frame,
            text="Clear All",
            command=self.clear_text
        ).grid(row=0, column=3, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, sticky="ew")
        
    def setup_audio(self):
        """Initialize audio settings and verify device availability"""
        self.sample_rate = 16000
        self.audio_queue = queue.Queue()
        self.is_recording = False
        
        # Get available audio devices
        try:
            self.audio_devices = sd.query_devices()
            input_devices = [i for i, dev in enumerate(self.audio_devices)
                           if dev['max_input_channels'] > 0]
            
            # Default to HyperX if available, else first input device
            self.default_device = next((i for i in input_devices
                                      if 'HyperX' in self.audio_devices[i]['name']),
                                     input_devices[0] if input_devices else None)
            
            if self.default_device is not None:
                print(f"Using audio device: {self.audio_devices[self.default_device]['name']}")
            else:
                raise RuntimeError("No input devices found")
        except sd.PortAudioError as e:
            messagebox.showerror(
                "Audio Error",
                f"Could not access audio devices: {str(e)}"
            )
            self.audio_devices = []
            self.default_device = None
        
    def on_model_select(self, *args):
        """Handle model selection changes"""
        selected_model = self.model_var.get()
        self.logger.info(f"Selected model: {selected_model}")
        try:
            self.setup_model()
        except Exception as e:
            self.logger.error(f"Failed to load model: {str(e)}")
            messagebox.showerror("Model Error", f"Failed to load model: {str(e)}")
        
    def setup_model(self):
        """Initialize or reload the Whisper model"""
        self.model_size = self.model_var.get()
        self.logger.info(f"Loading model: {self.model_size}")
        
        # Set custom cache directory
        import os
        os.environ['HF_HOME'] = '/tmp/huggingface'
        self.logger.debug(f"Cache directory set to: {os.environ['HF_HOME']}")
        
        # Show loading status
        self.status_var.set(f"Loading {self.model_size} model...")
        self.root.update()
        
        try:
            # Use CPU only
            self.logger.debug("Initializing Whisper model...")
            self.model = faster_whisper.WhisperModel(
                self.model_size,
                device="cpu",
                compute_type="int8",
                download_root='/tmp/huggingface'
            )
            self.status_var.set(f"Model loaded: {self.model_size}")
            self.logger.info(f"Successfully loaded {self.model_size} model")
            self.logger.debug(f"Model details: {self.model}")
        except Exception as e:
            error_msg = f"Failed to load model: {str(e)}"
            self.logger.error(error_msg)
            messagebox.showerror("Model Error", error_msg)
            self.status_var.set("Model load failed")
        except Exception as e:
            messagebox.showerror("Model Error", f"Failed to load model: {str(e)}")
            self.status_var.set("Model load failed")
        
    def toggle_listen(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        self.is_recording = True
        self.listen_btn.config(text="Stop")
        self.status_var.set("Recording...")
        self.audio_thread = threading.Thread(target=self.record_audio)
        self.audio_thread.start()
        
    def stop_recording(self):
        self.is_recording = False
        self.listen_btn.config(text="Listen")
        self.status_var.set("Processing...")
        
    def record_audio(self):
        """Record audio from default input device"""
        def callback(indata, frames, time, status):
            if self.is_recording:
                # Calculate RMS level for debugging
                rms_level = np.sqrt(np.mean(indata**2))
                if rms_level > 0.01:  # Only store audio above threshold
                    self.audio_queue.put(indata.copy())
                self.status_var.set(f"Recording... Level: {rms_level:.2f}")
                
        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                callback=callback,
                device=self.default_device
            ):
                while self.is_recording:
                    sd.sleep(100)
                    
            self.process_audio()
        except sd.PortAudioError as e:
            messagebox.showerror(
                "Audio Error",
                f"Could not access audio device: {str(e)}"
            )
            self.status_var.set("Audio device error")
            self.is_recording = False
            self.listen_btn.config(text="Press to Listen")
        
    def process_audio(self):
        """Process recorded audio through Whisper model"""
        audio_data = []
        while not self.audio_queue.empty():
            audio_data.append(self.audio_queue.get())
            
        if audio_data:
            audio_array = np.concatenate(audio_data)
            try:
                # Verify model is loaded
                if not hasattr(self, 'model') or self.model is None:
                    raise RuntimeError("Whisper model not loaded")
                    
                # Transcribe audio with more detailed settings
                segments, info = self.model.transcribe(
                    audio_array.flatten(),
                    language="en",
                    vad_filter=True,  # Enable voice activity detection
                    vad_parameters=dict(
                        threshold=0.5,  # More sensitive to speech
                        min_speech_duration_ms=500,
                        max_speech_duration_s=20
                    )
                )
                
                # Combine segments into final text
                if segments:
                    text = " ".join(segment.text for segment in segments).strip()
                    if text:
                        self.text_area.insert(tk.END, text + "\n")
                        self.save_text_state()  # Save the new text state
                        self.status_var.set(f"Transcription complete ({info.language})")
                        self.logger.debug(f"Text state saved after transcription. History length: {len(self.text_history)}")
                    else:
                        self.status_var.set("No speech detected (low confidence)")
                else:
                    self.status_var.set("No speech segments found")
                    
            except RuntimeError as e:
                messagebox.showerror("Model Error", str(e))
                self.status_var.set("Model error")
            except Exception as e:
                messagebox.showerror("Transcription Error", str(e))
                self.status_var.set("Transcription failed")
                
    def copy_text(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if text:
            pyperclip.copy(text)
            self.status_var.set("Text copied to clipboard")
            
    def clear_text(self):
        self.save_text_state()
        self.text_area.delete("1.0", tk.END)
        self.status_var.set("Text cleared")
        
    def undo_text(self):
        """Revert to previous text state"""
        try:
            self.logger.debug(f"Undo requested. History length: {len(self.text_history)}, Index: {self.history_index}")
            
            if len(self.text_history) > 1:
                # Save current state before undo if it's different
                current_text = self.text_area.get("1.0", tk.END).strip()
                if current_text != self.text_history[self.history_index]:
                    self.text_history.append(current_text)
                    self.history_index += 1
                    self.logger.debug(f"Saved current state. New history length: {len(self.text_history)}")
                    
                # Perform undo
                self.history_index -= 1
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", self.text_history[self.history_index])
                
                status = f"Undo successful (step {self.history_index + 1}/{len(self.text_history)})"
                self.status_var.set(status)
                self.logger.info(status)
                self.logger.debug(f"Current text length: {len(self.text_history[self.history_index])} chars")
            elif len(self.text_history) == 1:
                # If we have one state, we can clear the text
                self.text_area.delete("1.0", tk.END)
                self.text_history = []
                self.history_index = -1
                status = "Text cleared (initial state)"
                self.status_var.set(status)
                self.logger.info(status)
                self.logger.debug("Cleared text and reset history")
            else:
                status = "Nothing to undo (no history)"
                self.status_var.set(status)
                self.logger.info(status)
                self.logger.debug(f"History state: {self.text_history}")
        except Exception as e:
            error_msg = f"Undo failed: {str(e)}"
            self.status_var.set(error_msg)
            self.logger.error(error_msg, exc_info=True)
            def save_text_state(self):
                """Save current text state to history"""
                try:
                    current_text = self.text_area.get("1.0", tk.END).strip()
                    if current_text:
                        # Initialize history if empty
                        if not self.text_history:
                            self.text_history = [current_text]
                            self.history_index = 0
                            self.logger.debug("Initialized text history")
                            return
                        
                        # Only save if text has changed
                        if current_text != self.text_history[self.history_index]:
                            # If we're not at the end of history, truncate future states
                            if self.history_index < len(self.text_history) - 1:
                                self.text_history = self.text_history[:self.history_index + 1]
                                self.logger.debug("Truncated future history states")
                            
                            self.text_history.append(current_text)
                            self.history_index = len(self.text_history) - 1
                            self.logger.debug(f"Saved new state. History length: {len(self.text_history)}")
                            
                            # Limit history to 50 states
                            if len(self.text_history) > 50:
                                self.text_history.pop(0)
                                self.history_index -= 1
                                self.logger.debug("Trimmed history to 50 states")
                except Exception as e:
                    self.logger.error(f"Failed to save text state: {str(e)}", exc_info=True)
                    self.history_index -= 1
        
if __name__ == "__main__":
    root = tk.Tk()
    app = WhisperApp(root)
    root.mainloop()