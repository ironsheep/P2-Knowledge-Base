#!/usr/bin/env python3
"""
Get actual dimensions of all images in a directory for catalog updating.
"""

import os
from PIL import Image

def get_image_dimensions(directory):
    """Get dimensions of all PNG images in directory."""
    
    dimensions = {}
    
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.png') and not filename.endswith('_BACKUP.png'):
            filepath = os.path.join(directory, filename)
            try:
                with Image.open(filepath) as img:
                    dimensions[filename] = {
                        'width': img.size[0],
                        'height': img.size[1],
                        'size_kb': round(os.path.getsize(filepath) / 1024, 1)
                    }
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    return dimensions

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 get_image_dimensions.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    dimensions = get_image_dimensions(directory)
    
    for filename, info in dimensions.items():
        print(f"{filename}: {info['width']}×{info['height']} pixels, {info['size_kb']}KB")