import os
import sys
from configparser import RawConfigParser

def patch_stdeb():
    try:
        # Find stdeb installation path
        import stdeb
        stdeb_path = os.path.dirname(stdeb.__file__)
        cli_runner_path = os.path.join(stdeb_path, 'cli_runner.py')
        
        # Read the original file
        with open(cli_runner_path, 'r') as f:
            content = f.read()
        
        # Apply the patch
        content = content.replace(
            "from configparser import SafeConfigParser",
            "from configparser import RawConfigParser as SafeConfigParser"
        )
        
        # Write the modified file
        with open(cli_runner_path, 'w') as f:
            f.write(content)
            
        print(f"Successfully patched {cli_runner_path}")
        return True
        
    except Exception as e:
        print(f"Failed to patch stdeb: {str(e)}")
        return False

if __name__ == '__main__':
    if patch_stdeb():
        sys.exit(0)
    else:
        sys.exit(1)
