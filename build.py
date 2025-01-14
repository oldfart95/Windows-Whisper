import platform
import subprocess
import sys

def build_project():
    system = platform.system()
    
    if system == 'Windows':
        spec_file = 'xwhisper_win.spec'
    elif system == 'Darwin':
        spec_file = 'xwhisper_mac.spec'
    else:
        spec_file = 'xwhisper_linux.spec'
    
    try:
        subprocess.run(['pyinstaller', spec_file], check=True)
        print(f"Build completed successfully using {spec_file}")
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("PyInstaller not found. Please install it using: pip install pyinstaller")
        sys.exit(1)

if __name__ == '__main__':
    build_project()