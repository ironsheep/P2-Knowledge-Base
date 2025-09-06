#!/usr/bin/env python3
"""
Simple black image detector using just PIL and file sizes.
Usage: python simple_black_detector.py <directory>
"""

import os
import sys
from PIL import Image, ImageStat

def analyze_image(image_path):
    """
    Analyze image for potential extraction failure.
    Returns: (is_likely_failed, file_size_kb, mean_brightness, width, height)
    """
    try:
        file_size = os.path.getsize(image_path) / 1024  # KB
        
        with Image.open(image_path) as img:
            width, height = img.size
            
            # Convert to grayscale for analysis
            gray = img.convert('L')
            stat = ImageStat.Stat(gray)
            mean_brightness = stat.mean[0]  # Mean pixel value (0-255)
            
            # Heuristics for failed extraction:
            # 1. Very low file size for large dimensions
            # 2. Very low brightness (nearly black)
            size_ratio = file_size / (width * height / 1000)  # KB per 1000 pixels
            
            is_likely_failed = (
                mean_brightness < 10 or  # Very dark
                (size_ratio < 0.5 and mean_brightness < 50)  # Small file + dark
            )
            
            return is_likely_failed, file_size, mean_brightness, width, height
            
    except Exception as e:
        return None, 0, 0, 0, 0, f"Error: {e}"

def analyze_directory(directory):
    """Analyze all PNG files in directory."""
    failed_images = []
    valid_images = []
    errors = []
    
    for filename in sorted(os.listdir(directory)):
        if filename.lower().endswith('.png'):
            filepath = os.path.join(directory, filename)
            result = analyze_image(filepath)
            
            if len(result) == 6:  # Error case
                errors.append((filename, result[5]))
            else:
                is_failed, size, brightness, w, h = result
                if is_failed:
                    failed_images.append((filename, size, brightness, w, h))
                else:
                    valid_images.append((filename, size, brightness, w, h))
    
    return failed_images, valid_images, errors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python simple_black_detector.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        sys.exit(1)
    
    failed_images, valid_images, errors = analyze_directory(directory)
    
    print(f"🔍 P2 DATASHEET IMAGE ANALYSIS")
    print("=" * 50)
    
    if failed_images:
        print(f"❌ LIKELY FAILED EXTRACTIONS ({len(failed_images)}):")
        for filename, size, brightness, w, h in failed_images:
            print(f"   {filename}")
            print(f"      Size: {size:.1f}KB, Brightness: {brightness:.1f}, Dims: {w}×{h}")
        print()
    
    print(f"✅ VALID EXTRACTIONS ({len(valid_images)}):")
    for filename, size, brightness, w, h in valid_images:
        print(f"   {filename} - {size:.1f}KB, {brightness:.1f} brightness, {w}×{h}")
    
    if errors:
        print(f"\n⚠️  ANALYSIS ERRORS ({len(errors)}):")
        for filename, error in errors:
            print(f"   {filename}: {error}")
    
    total_images = len(failed_images) + len(valid_images)
    success_rate = len(valid_images) / total_images * 100 if total_images > 0 else 0
    
    print(f"\n📊 EXTRACTION SUMMARY:")
    print(f"   Total images: {total_images}")
    print(f"   Failed extractions: {len(failed_images)}")
    print(f"   Actual success rate: {success_rate:.1f}%")
    
    if failed_images:
        print(f"\n🔧 RECOVERY RECOMMENDATIONS:")
        print(f"   1. Try pdf2image rescue on failed extractions")
        print(f"   2. Check original PDF pages {', '.join([f.split('_page')[1].split('_')[0] for f, _, _, _, _ in failed_images])}")
        print(f"   3. Consider manual screenshot as fallback")