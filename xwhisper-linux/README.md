# XWhisper - Linux Version

XWhisper is a real-time speech recognition application using OpenAI's Whisper model, optimized for Ubuntu/Kubuntu Linux systems.

## Features
- Real-time speech-to-text transcription
- Simple graphical interface
- Systemd service integration
- Desktop menu integration
- High-quality transcription using Whisper

## Installation

### From Source
1. Install dependencies:
```bash
sudo apt install python3-dev python3-pip python3-venv \
    libportaudio2 portaudio19-dev libasound2-dev
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/xwhisper-linux.git
cd xwhisper-linux
```

3. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Build and install:
```bash
./build.py
```

### From Debian Package
1. Download the .deb package
2. Install using:
```bash
sudo apt install ./xwhisper_0.1.0_all.deb
```

## Usage
Run from terminal:
```bash
xwhisper
```

Or launch from your desktop environment's application menu.

## Service Mode
To run as a background service:
```bash
sudo systemctl enable xwhisper
sudo systemctl start xwhisper
```

## Uninstallation
```bash
sudo apt remove xwhisper
sudo rm -rf /usr/share/xwhisper
```

## License
MIT License