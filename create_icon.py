from cairosvg import svg2png
from PIL import Image
import io

# Convert SVG to PNG in memory
png_data = svg2png(url='assets/icon.svg', output_width=256, output_height=256)

# Create PIL Image from PNG data
img = Image.open(io.BytesIO(png_data))

# Convert to ICO
img.save('assets/icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])
