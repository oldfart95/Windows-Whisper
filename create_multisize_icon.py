from PIL import Image
import os

def create_multisize_ico():
    # Load the existing ICO file
    ico_path = os.path.join('assets', 'icon.ico')
    img = Image.open(ico_path)
    
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Create different sizes
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    icons = []
    
    for size in sizes:
        resized = img.resize(size, Image.Resampling.LANCZOS)
        icons.append(resized)
    
    # Save as ICO with multiple sizes
    icons[0].save(ico_path, format='ICO', sizes=[(i.width, i.height) for i in icons], append_images=icons[1:])
    print(f"Created multi-size icon at {ico_path}")

if __name__ == '__main__':
    create_multisize_ico()
