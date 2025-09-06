#!/usr/bin/env python3
"""
Detect black/failed image extractions by analyzing image content.
Usage: python detect_black_images.py <directory>
"""

import os
import sys
from PIL import Image
import numpy as np

def is_black_image(image_path, threshold=5):
    """
    Check if an image is essentially black (extraction failure).
    threshold: Mean pixel value below which image is considered black
    """
    try:
        with Image.open(image_path) as img:
            # Convert to grayscale for analysis
            gray = img.convert('L')
            pixels = np.array(gray)
            mean_brightness = np.mean(pixels)
            
            # Check if image is essentially black
            if mean_brightness < threshold:
                return True, mean_brightness
            return False, mean_brightness
    except Exception as e:
        return None, f"Error: {e}"

def analyze_directory(directory):
    """Analyze all PNG files in directory for black images."""
    black_images = []
    valid_images = []
    errors = []
    
    for filename in sorted(os.listdir(directory)):
        if filename.lower().endswith('.png'):
            filepath = os.path.join(directory, filename)
            result, brightness = is_black_image(filepath)
            
            if result is None:
                errors.append((filename, brightness))
            elif result:
                black_images.append((filename, brightness))
            else:
                valid_images.append((filename, brightness))
    
    return black_images, valid_images, errors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python detect_black_images.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        sys.exit(1)
    
    black_images, valid_images, errors = analyze_directory(directory)
    
    print(f"🔍 IMAGE ANALYSIS RESULTS for {directory}")
    print("=" * 60)
    
    if black_images:
        print(f"❌ BLACK/FAILED IMAGES ({len(black_images)}):")
        for filename, brightness in black_images:
            print(f"   {filename} (brightness: {brightness:.2f})")
        print()
    
    print(f"✅ VALID IMAGES ({len(valid_images)}):")
    for filename, brightness in valid_images:
        file_size = os.path.getsize(os.path.join(directory, filename)) / 1024
        print(f"   {filename} (brightness: {brightness:.2f}, {file_size:.1f}KB)")
    
    if errors:
        print(f"\n⚠️  ERRORS ({len(errors)}):")
        for filename, error in errors:
            print(f"   {filename}: {error}")
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total images: {len(black_images) + len(valid_images)}")
    print(f"   Failed extractions: {len(black_images)}")
    print(f"   Success rate: {len(valid_images)/(len(black_images)+len(valid_images))*100:.1f}%")