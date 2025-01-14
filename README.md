# XWhisper

A cross-platform desktop application for real-time speech recognition using OpenAI's Whisper model.

## Features

- Real-time speech recognition using the Whisper model
- Clean and intuitive user interface
- Start/Stop recording with a single click
- Displays transcribed text in real-time
- Copy transcribed text to clipboard

## Installation

### Option 1: Direct Download (Recommended)
1. Download the latest release from the releases page
2. Extract the ZIP file to your desired location
3. Run `XWhisper.exe` (Windows) or `XWhisper` (Linux/Mac)

### Option 2: Build from Source
1. Clone this repository:
   ```bash
   git clone https://github.com/oldfart95/XWhisper.git
   cd XWhisper
   ```

2. Create a conda environment (recommended):
   ```bash
   conda env create -f environment.yml
   conda activate whisper_env
   ```

   Or install requirements using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. Build the executable:
   ```bash
   pyinstaller xwhisper.spec
   ```

4. The executable will be created in the `dist` folder

## Usage

1. Launch the application by running `XWhisper.exe` (Windows) or `XWhisper` (Linux/Mac)
2. Click the "Start Recording" button to begin speech recognition
3. Speak into your microphone
4. The transcribed text will appear in the text area
5. Click "Stop Recording" to stop the recognition
6. Use the "Copy" button to copy the transcribed text to your clipboard

## System Requirements

- Windows 10/11, Linux, or macOS
- 4GB RAM minimum (8GB recommended)
- Microphone
- Internet connection (for first run to download the Whisper model)

## Technical Details

- Built with Python 3.12
- Uses faster-whisper for speech recognition
- GUI built with PyQt6
- Packaged with PyInstaller

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for the Whisper model
- faster-whisper team for the optimized implementation
- PyQt team for the GUI framework
