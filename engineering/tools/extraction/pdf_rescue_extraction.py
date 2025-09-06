#!/usr/bin/env python3
"""
PDF Image Rescue - Attempt pdf2image recovery for failed PyMuPDF extractions.
Usage: python pdf_rescue_extraction.py <pdf_path> <failed_images_list>
"""

import os
import sys
import json
from PIL import Image, ImageStat
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

def is_extraction_failed(image_path):
    """Check if an image extraction failed (black or very small)."""
    try:
        file_size = os.path.getsize(image_path) / 1024  # KB
        with Image.open(image_path) as img:
            gray = img.convert('L')
            stat = ImageStat.Stat(gray)
            mean_brightness = stat.mean[0]
            
            # Consider failed if very dark or suspiciously small
            return mean_brightness < 10 or file_size < 8  # Adjust threshold as needed
    except:
        return True

def parse_image_filename(filename):
    """Extract page number and image index from filename."""
    # Expected format: Document_pageXX_imgYY.png
    try:
        parts = filename.split('_')
        page_part = [p for p in parts if p.startswith('page')][0]
        img_part = [p for p in parts if p.startswith('img')][0]
        
        page_num = int(page_part.replace('page', ''))
        img_index = int(img_part.replace('img', '').replace('.png', ''))
        
        return page_num, img_index
    except:
        return None, None

def rescue_with_pdf2image(pdf_path, page_num, output_path, base_filename):
    """Attempt to rescue extraction using pdf2image."""
    if not PDF2IMAGE_AVAILABLE:
        print(f"   ⚠️ pdf2image not available - skipping rescue")
        return False
    
    try:
        # Convert specific page to image
        pages = convert_from_path(pdf_path, first_page=page_num, last_page=page_num, dpi=200)
        if pages:
            page_img = pages[0]
            rescue_filename = base_filename.replace('.png', '_RESCUED.png')
            rescue_path = os.path.join(output_path, rescue_filename)
            page_img.save(rescue_path, 'PNG')
            
            print(f"   🚀 RESCUE SUCCESS: {rescue_filename}")
            return True
        return False
    except Exception as e:
        print(f"   ❌ RESCUE FAILED: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python pdf_rescue_extraction.py <pdf_path> <images_directory>")
        print("This will attempt to rescue all failed extractions found in the directory.")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    images_dir = sys.argv[2]
    
    if not os.path.exists(pdf_path):
        print(f"PDF not found: {pdf_path}")
        sys.exit(1)
    
    if not os.path.exists(images_dir):
        print(f"Images directory not found: {images_dir}")
        sys.exit(1)
    
    print(f"🔧 PDF RESCUE EXTRACTION")
    print(f"PDF: {pdf_path}")
    print(f"Images: {images_dir}")
    print(f"pdf2image available: {'✅ YES' if PDF2IMAGE_AVAILABLE else '❌ NO'}")
    print("=" * 60)
    
    # Find all PNG files and check for failures
    failed_images = []
    for filename in sorted(os.listdir(images_dir)):
        if filename.lower().endswith('.png') and not filename.endswith('_RESCUED.png'):
            filepath = os.path.join(images_dir, filename)
            if is_extraction_failed(filepath):
                page_num, img_index = parse_image_filename(filename)
                if page_num:
                    failed_images.append((filename, page_num, img_index))
    
    if not failed_images:
        print("✅ No failed extractions detected!")
        return
    
    print(f"Found {len(failed_images)} failed extractions:")
    
    rescue_count = 0
    for filename, page_num, img_index in failed_images:
        print(f"\n🔧 Attempting rescue: {filename} (Page {page_num})")
        
        if rescue_with_pdf2image(pdf_path, page_num, images_dir, filename):
            rescue_count += 1
    
    print(f"\n📊 RESCUE SUMMARY:")
    print(f"   Failed extractions found: {len(failed_images)}")
    print(f"   Successful rescues: {rescue_count}")
    print(f"   Rescue success rate: {rescue_count/len(failed_images)*100:.1f}%")
    
    if rescue_count > 0:
        print(f"\n✅ Rescued images saved with '_RESCUED.png' suffix")
        print(f"   Review rescued images and replace originals if successful")

if __name__ == "__main__":
    main()