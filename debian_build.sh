#!/bin/bash

# Install required build tools
sudo apt update
sudo apt install -y \
    build-essential \
    devscripts \
    debhelper \
    dh-python \
    fakeroot

# Clean previous builds
rm -rf dist/ build/ deb_dist/ *.egg-info/

# Create source distribution
python3 setup.py sdist

# Build Debian package
DEB_BUILD_OPTIONS=nocheck debuild -b -uc -us

# Move package to dist directory
mkdir -p dist
mv ../xwhisper_*.deb dist/

echo "Debian package built successfully. Find it in dist/ directory"