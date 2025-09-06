#!/usr/bin/env python3
"""
Validate rescued images and replace failed originals.
Usage: python validate_and_replace_rescued.py <images_directory>
"""

import os
import sys
import shutil
from PIL import Image, ImageStat

def analyze_image_quality(image_path):
    """Analyze image for quality metrics."""
    try:
        file_size = os.path.getsize(image_path) / 1024  # KB
        with Image.open(image_path) as img:
            width, height = img.size
            gray = img.convert('L')
            stat = ImageStat.Stat(gray)
            mean_brightness = stat.mean[0]
            
            return {
                'valid': True,
                'file_size_kb': file_size,
                'dimensions': f"{width}×{height}",
                'brightness': mean_brightness,
                'pixel_count': width * height,
                'is_likely_good': mean_brightness > 50 and file_size > 10
            }
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_and_replace_rescued.py <images_directory>")
        sys.exit(1)
    
    images_dir = sys.argv[1]
    if not os.path.exists(images_dir):
        print(f"Directory not found: {images_dir}")
        sys.exit(1)
    
    print("🔍 RESCUED IMAGE VALIDATION & REPLACEMENT")
    print("=" * 50)
    
    # Find all rescued images
    rescued_files = [f for f in os.listdir(images_dir) if f.endswith('_RESCUED.png')]
    
    if not rescued_files:
        print("No rescued images found!")
        return
    
    print(f"Found {len(rescued_files)} rescued images")
    
    replacements = []
    validation_failures = []
    
    for rescued_file in sorted(rescued_files):
        original_file = rescued_file.replace('_RESCUED.png', '.png')
        
        rescued_path = os.path.join(images_dir, rescued_file)
        original_path = os.path.join(images_dir, original_file)
        
        if not os.path.exists(original_path):
            print(f"⚠️ Original not found for {rescued_file}")
            continue
        
        # Analyze both images
        rescued_info = analyze_image_quality(rescued_path)
        original_info = analyze_image_quality(original_path)
        
        print(f"\n📊 {original_file}:")
        print(f"   Original: {original_info['file_size_kb']:.1f}KB, brightness {original_info['brightness']:.1f}")
        print(f"   Rescued:  {rescued_info['file_size_kb']:.1f}KB, brightness {rescued_info['brightness']:.1f}")
        
        if rescued_info['valid'] and rescued_info['is_likely_good']:
            if not original_info['is_likely_good']:
                replacements.append((rescued_file, original_file))
                print(f"   ✅ WILL REPLACE - Rescued image is much better")
            else:
                print(f"   ⚖️ BOTH GOOD - Keeping original (rescued available as backup)")
        else:
            validation_failures.append(rescued_file)
            print(f"   ❌ RESCUED VALIDATION FAILED")
    
    if not replacements:
        print(f"\n✅ No replacements needed - all images are good!")
        return
    
    print(f"\n🔄 PERFORMING {len(replacements)} REPLACEMENTS:")
    
    replaced_count = 0
    for rescued_file, original_file in replacements:
        try:
            rescued_path = os.path.join(images_dir, rescued_file)
            original_path = os.path.join(images_dir, original_file)
            backup_path = os.path.join(images_dir, original_file.replace('.png', '_FAILED_BACKUP.png'))
            
            # Backup failed original
            shutil.move(original_path, backup_path)
            
            # Move rescued to replace original
            shutil.move(rescued_path, original_path)
            
            print(f"   ✅ {original_file} - Replaced with rescued version")
            replaced_count += 1
            
        except Exception as e:
            print(f"   ❌ {original_file} - Replacement failed: {e}")
    
    print(f"\n📊 REPLACEMENT SUMMARY:")
    print(f"   Rescued images found: {len(rescued_files)}")
    print(f"   Successful replacements: {replaced_count}")
    print(f"   Failed validations: {len(validation_failures)}")
    
    if replaced_count > 0:
        print(f"\n✅ {replaced_count} failed images successfully replaced with rescued versions!")
        print(f"   Failed originals backed up with '_FAILED_BACKUP.png' suffix")
    
    # Cleanup remaining rescued files that weren't used
    remaining_rescued = [f for f in os.listdir(images_dir) if f.endswith('_RESCUED.png')]
    if remaining_rescued:
        print(f"\n🧹 {len(remaining_rescued)} unused rescued images remain (backups)")

if __name__ == "__main__":
    main()