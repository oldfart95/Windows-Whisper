#!/bin/bash

# Install required system packages
sudo apt update
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    devscripts \
    debhelper \
    dh-python \
    fakeroot

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install stdeb

# Clean previous builds
rm -rf dist/ build/ deb_dist/ *.egg-info/

# Build source distribution and wheel
python3 setup.py sdist bdist_wheel

# Build .deb package
python3 setup.py --command-packages=stdeb.command bdist_deb

echo "Build complete. Packages available in dist/ and deb_dist/"
