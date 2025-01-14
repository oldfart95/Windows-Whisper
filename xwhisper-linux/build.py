#!/usr/bin/env python3

import platform
import subprocess
import sys
import os

def install_dependencies():
    try:
        subprocess.run([
            'sudo', 'apt', 'install', '-y',
            'portaudio19-dev', 'libasound2-dev'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        sys.exit(1)

def build_project():
    system = platform.system()
    
    if system != 'Linux':
        print("This build script is only for Linux systems")
        sys.exit(1)
        
    try:
        # Install required dependencies
        install_dependencies()
        
        # Build the package
        subprocess.run(['dpkg-buildpackage', '-us', '-uc'], check=True)
        
        # Install systemd service
        if os.path.exists('debian/xwhisper.service'):
            subprocess.run([
                'sudo', 'cp', 
                'debian/xwhisper.service', 
                '/etc/systemd/system/'
            ], check=True)
            subprocess.run([
                'sudo', 'systemctl', 'daemon-reload'
            ], check=True)
            
        print("Build completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Required tools not found")
        sys.exit(1)

if __name__ == '__main__':
    build_project()