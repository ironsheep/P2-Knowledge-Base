#!/usr/bin/env python3
"""
Replace full-page extracted images with properly cropped rescued versions.
This addresses the issue where PyMuPDF extracted full pages instead of individual images.
"""

import os
import shutil
from PIL import Image

def replace_with_cropped_images(original_dir, rescued_dir):
    """Replace original images with cropped rescued versions where available."""
    
    print("🔄 REPLACING FULL-PAGE IMAGES WITH CROPPED VERSIONS")
    print("=" * 60)
    
    replaced_count = 0
    rescued_files = [f for f in os.listdir(rescued_dir) if f.endswith('_RESCUED_CROPPED.png')]
    
    for rescued_file in rescued_files:
        # Get the original filename by removing the _RESCUED_CROPPED suffix
        base_name = rescued_file.replace('_RESCUED_CROPPED.png', '.png')
        original_path = os.path.join(original_dir, base_name)
        rescued_path = os.path.join(rescued_dir, rescued_file)
        
        if os.path.exists(original_path):
            # Get dimensions for comparison
            try:
                with Image.open(original_path) as orig_img:
                    orig_size = orig_img.size
                with Image.open(rescued_path) as rescued_img:
                    rescued_size = rescued_img.size
                
                print(f"📊 {base_name}:")
                print(f"   Original: {orig_size[0]}×{orig_size[1]} (full page)")
                print(f"   Cropped:  {rescued_size[0]}×{rescued_size[1]} (targeted)")
                
                # Create backup of original
                backup_path = original_path.replace('.png', '_FULLPAGE_BACKUP.png')
                shutil.copy2(original_path, backup_path)
                
                # Replace with cropped version
                shutil.copy2(rescued_path, original_path)
                
                print(f"   ✅ REPLACED with cropped version")
                print(f"   🗃️ Original saved as: {os.path.basename(backup_path)}")
                replaced_count += 1
                
            except Exception as e:
                print(f"   ❌ Error processing {base_name}: {e}")
        else:
            print(f"   ⚠️ Original file not found: {base_name}")
        
        print()
    
    print(f"📊 REPLACEMENT SUMMARY:")
    print(f"   Cropped images available: {len(rescued_files)}")
    print(f"   Successfully replaced: {replaced_count}")
    print(f"   Full-page backups created: {replaced_count}")
    
    return replaced_count

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python3 replace_with_cropped.py <original_dir> <rescued_dir>")
        sys.exit(1)
    
    original_dir = sys.argv[1]
    rescued_dir = sys.argv[2]
    
    if not os.path.exists(original_dir):
        print(f"❌ Original directory not found: {original_dir}")
        sys.exit(1)
    
    if not os.path.exists(rescued_dir):
        print(f"❌ Rescued directory not found: {rescued_dir}")
        sys.exit(1)
    
    replaced = replace_with_cropped_images(original_dir, rescued_dir)
    
    if replaced > 0:
        print(f"\n🎯 SUCCESS: {replaced} images replaced with properly cropped versions!")
        print(f"💡 Full-page backups saved with '_FULLPAGE_BACKUP.png' suffix")
    else:
        print(f"\n⚠️ No images were replaced. Check that rescued images exist.")