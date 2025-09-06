#!/usr/bin/env python3
"""
Clean up failed extractions and replace with properly cropped rescued images.
Usage: python cleanup_and_replace.py <original_dir> <rescued_dir>
"""

import os
import sys
import shutil
from PIL import Image, ImageStat

def analyze_image_quality(image_path):
    """Quick image quality check."""
    try:
        file_size = os.path.getsize(image_path) / 1024  # KB
        with Image.open(image_path) as img:
            width, height = img.size
            gray = img.convert('L')
            stat = ImageStat.Stat(gray)
            mean_brightness = stat.mean[0]
            
            is_good_quality = mean_brightness > 50 and file_size > 10
            
            return {
                'valid': True,
                'file_size_kb': file_size,
                'dimensions': f"{width}×{height}",
                'brightness': mean_brightness,
                'is_good': is_good_quality
            }
    except Exception as e:
        return {'valid': False, 'error': str(e)}

def cleanup_and_replace(original_dir, rescued_dir):
    """Replace failed images with rescued versions and clean up."""
    
    print("🧹 CLEANUP AND REPLACEMENT OPERATION")
    print("=" * 50)
    
    if not os.path.exists(original_dir):
        print(f"❌ Original directory not found: {original_dir}")
        return
    
    if not os.path.exists(rescued_dir):
        print(f"❌ Rescued directory not found: {rescued_dir}")
        return
    
    # Find all rescued cropped images
    rescued_files = [f for f in os.listdir(rescued_dir) if f.endswith('_RESCUED_CROPPED.png')]
    
    if not rescued_files:
        print("❌ No rescued cropped images found!")
        return
    
    print(f"Found {len(rescued_files)} rescued cropped images")
    
    replacements_made = []
    cleanup_files = []
    
    for rescued_file in sorted(rescued_files):
        # Determine original filename
        original_file = rescued_file.replace('_RESCUED_CROPPED.png', '.png')
        
        original_path = os.path.join(original_dir, original_file)
        rescued_path = os.path.join(rescued_dir, rescued_file)
        
        if not os.path.exists(original_path):
            print(f"⚠️ Original not found for {rescued_file}")
            continue
        
        # Analyze both images
        original_info = analyze_image_quality(original_path)
        rescued_info = analyze_image_quality(rescued_path)
        
        print(f"\n📊 {original_file}:")
        print(f"   Original: {original_info.get('file_size_kb', 0):.1f}KB, {original_info.get('brightness', 0):.1f} brightness, {original_info.get('dimensions', 'unknown')}")
        print(f"   Rescued:  {rescued_info.get('file_size_kb', 0):.1f}KB, {rescued_info.get('brightness', 0):.1f} brightness, {rescued_info.get('dimensions', 'unknown')}")
        
        if rescued_info.get('valid') and rescued_info.get('is_good'):
            if not original_info.get('is_good'):
                # Replace the failed original with rescued version
                try:
                    # Backup failed original
                    backup_path = os.path.join(original_dir, original_file.replace('.png', '_FAILED.png'))
                    shutil.move(original_path, backup_path)
                    cleanup_files.append(backup_path)
                    
                    # Copy rescued to replace original
                    shutil.copy2(rescued_path, original_path)
                    replacements_made.append(original_file)
                    
                    print(f"   ✅ REPLACED - Failed original backed up and replaced with rescued version")
                    
                except Exception as e:
                    print(f"   ❌ REPLACEMENT FAILED: {e}")
            else:
                print(f"   ⚖️ BOTH GOOD - No replacement needed")
        else:
            print(f"   ❌ RESCUED IMAGE INVALID - Cannot replace")
    
    # Look for other cleanup candidates in original directory
    print(f"\n🔍 SCANNING FOR ADDITIONAL CLEANUP:")
    
    for filename in os.listdir(original_dir):
        if filename.lower().endswith('.png') and not filename.endswith('_FAILED.png'):
            filepath = os.path.join(original_dir, filename)
            info = analyze_image_quality(filepath)
            
            if info.get('valid') and not info.get('is_good'):
                # This is a failed image that wasn't rescued
                backup_path = os.path.join(original_dir, filename.replace('.png', '_FAILED.png'))
                if not os.path.exists(backup_path):  # Don't double-process
                    try:
                        shutil.move(filepath, backup_path)
                        cleanup_files.append(backup_path)
                        print(f"   🗑️ MOVED TO BACKUP: {filename} (failed extraction)")
                    except Exception as e:
                        print(f"   ❌ CLEANUP FAILED for {filename}: {e}")
    
    # Summary
    print(f"\n📊 CLEANUP SUMMARY:")
    print(f"   Rescued images processed: {len(rescued_files)}")
    print(f"   Successful replacements: {len(replacements_made)}")
    print(f"   Files moved to backup: {len(cleanup_files)}")
    
    if replacements_made:
        print(f"\n✅ SUCCESSFULLY REPLACED:")
        for filename in replacements_made:
            print(f"   • {filename}")
    
    if cleanup_files:
        print(f"\n🗑️ MOVED TO BACKUP (can be deleted):")
        for filepath in cleanup_files:
            filename = os.path.basename(filepath)
            file_size = os.path.getsize(filepath) / 1024
            print(f"   • {filename} ({file_size:.1f}KB)")
        
        print(f"\n💡 TO PERMANENTLY DELETE FAILED BACKUPS:")
        print(f"   rm {original_dir}/*_FAILED.png")
    
    # Count final good images
    good_images = []
    for filename in os.listdir(original_dir):
        if filename.lower().endswith('.png') and not filename.endswith('_FAILED.png'):
            filepath = os.path.join(original_dir, filename)
            info = analyze_image_quality(filepath)
            if info.get('valid') and info.get('is_good'):
                good_images.append(filename)
    
    print(f"\n🎯 FINAL STATUS:")
    print(f"   Good quality images: {len(good_images)}")
    print(f"   Extraction success rate after rescue: {len(good_images)/40*100:.1f}%")

def main():
    if len(sys.argv) != 3:
        print("Usage: python cleanup_and_replace.py <original_dir> <rescued_dir>")
        print("Example: python cleanup_and_replace.py original_images/ rescued_images/")
        sys.exit(1)
    
    original_dir = sys.argv[1]
    rescued_dir = sys.argv[2]
    
    cleanup_and_replace(original_dir, rescued_dir)

if __name__ == "__main__":
    main()