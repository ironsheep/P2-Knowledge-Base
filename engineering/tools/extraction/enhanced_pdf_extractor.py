#!/usr/bin/env python3
"""
Enhanced PDF Image Extractor with coordinate tracking and intelligent rescue.
This version saves bounding box coordinates and can properly crop rescued images.
"""

import fitz  # PyMuPDF
import os
import sys
import json
from pathlib import Path
import argparse
from pdf2image import convert_from_path
from PIL import Image, ImageStat

def extract_images_with_coordinates(pdf_path, output_dir="extracted_images"):
    """
    Enhanced extraction that saves bounding box coordinates for proper cropping.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        doc = fitz.open(pdf_path)
        print(f"✅ Opened PDF: {pdf_path}")
        print(f"📄 Pages: {len(doc)}")
    except Exception as e:
        print(f"❌ Error opening PDF: {e}")
        return []
    
    image_catalog = []
    total_images = 0
    failed_extractions = []
    
    pdf_name = Path(pdf_path).stem
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        
        print(f"\n📄 Page {page_num + 1}: Found {len(image_list)} images")
        
        for img_index, img in enumerate(image_list):
            try:
                # Get image data
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                
                # Skip images that are too small (likely decorative)
                if pix.width < 50 or pix.height < 50:
                    pix = None
                    continue
                
                # Generate filename
                img_filename = f"{pdf_name}_page{page_num+1:02d}_img{img_index+1:02d}.png"
                img_path = os.path.join(output_dir, img_filename)
                
                # Get image rectangle coordinates
                image_rects = page.get_image_rects(xref)
                bbox_coords = None
                if image_rects:
                    # Use the first rectangle (most common case)
                    rect = image_rects[0]
                    bbox_coords = {
                        "x0": rect.x0,
                        "y0": rect.y0, 
                        "x1": rect.x1,
                        "y1": rect.y1,
                        "width": rect.width,
                        "height": rect.height
                    }
                
                # Try to save the image
                extraction_success = True
                extraction_error = None
                
                try:
                    if pix.n - pix.alpha < 4:  # GRAY or RGB
                        pix.save(img_path)
                    else:  # CMYK: convert to RGB
                        pix1 = fitz.Pixmap(fitz.csRGB, pix)
                        pix1.save(img_path)
                        pix1 = None
                    
                    # Check if extraction actually worked
                    file_size = os.path.getsize(img_path) / 1024  # KB
                    
                    # Test the saved image
                    with Image.open(img_path) as test_img:
                        gray = test_img.convert('L')
                        stat = ImageStat.Stat(gray)
                        mean_brightness = stat.mean[0]
                        
                        # Consider failed if very dark or suspiciously small
                        if mean_brightness < 10 or file_size < 5:
                            extraction_success = False
                            extraction_error = f"Black image detected (brightness: {mean_brightness:.1f}, size: {file_size:.1f}KB)"
                
                except Exception as e:
                    extraction_success = False
                    extraction_error = str(e)
                
                if not extraction_success:
                    failed_extractions.append({
                        "filename": img_filename,
                        "page_number": page_num + 1,
                        "image_index": img_index + 1,
                        "xref": xref,
                        "bbox": bbox_coords,
                        "error": extraction_error
                    })
                    print(f"  ❌ Failed extraction: {img_filename} - {extraction_error}")
                else:
                    print(f"  ✅ Extracted: {img_filename} ({pix.width}×{pix.height})")
                
                # Build catalog entry with coordinates
                catalog_entry = {
                    "filename": img_filename,
                    "page_number": page_num + 1,
                    "image_index": img_index + 1,
                    "dimensions": f"{pix.width}×{pix.height}",
                    "width": pix.width,
                    "height": pix.height,
                    "xref": xref,
                    "bbox": bbox_coords,
                    "extraction_status": "success" if extraction_success else "failed",
                    "extraction_error": extraction_error if not extraction_success else None,
                    "file_path": img_path if extraction_success else None
                }
                
                image_catalog.append(catalog_entry)
                total_images += 1
                
                pix = None
                
            except Exception as e:
                print(f"  ❌ Error processing image {img_index + 1}: {e}")
                failed_extractions.append({
                    "filename": f"{pdf_name}_page{page_num+1:02d}_img{img_index+1:02d}.png",
                    "page_number": page_num + 1,
                    "image_index": img_index + 1,
                    "error": str(e)
                })
    
    doc.close()
    
    # Save enhanced catalog with coordinates
    catalog_path = os.path.join(output_dir, f"{pdf_name}_enhanced_catalog.json")
    catalog_data = {
        "source_pdf": pdf_path,
        "extraction_summary": {
            "total_images": total_images,
            "successful_extractions": total_images - len(failed_extractions),
            "failed_extractions": len(failed_extractions),
            "success_rate": ((total_images - len(failed_extractions)) / total_images * 100) if total_images > 0 else 0,
            "output_directory": output_dir
        },
        "images": image_catalog,
        "failed_extractions": failed_extractions
    }
    
    with open(catalog_path, 'w') as f:
        json.dump(catalog_data, f, indent=2)
    
    print(f"\n🎯 ENHANCED EXTRACTION COMPLETE:")
    print(f"   📊 Total images found: {total_images}")
    print(f"   ✅ Successful extractions: {total_images - len(failed_extractions)}")
    print(f"   ❌ Failed extractions: {len(failed_extractions)}")
    print(f"   📈 Success rate: {((total_images - len(failed_extractions)) / total_images * 100):.1f}%")
    print(f"   📁 Output directory: {output_dir}")
    print(f"   📋 Enhanced catalog: {catalog_path}")
    
    return catalog_data

def rescue_with_coordinates(pdf_path, catalog_data, output_dir, dpi=200):
    """
    Use pdf2image + coordinate cropping to rescue failed extractions.
    """
    print(f"\n🔧 COORDINATE-AWARE RESCUE OPERATION")
    print("=" * 50)
    
    if not catalog_data.get("failed_extractions"):
        print("✅ No failed extractions to rescue!")
        return
    
    failed_extractions = catalog_data["failed_extractions"]
    print(f"Attempting to rescue {len(failed_extractions)} failed extractions...")
    
    doc = fitz.open(pdf_path)
    rescue_count = 0
    
    # Group failures by page for efficient processing
    failures_by_page = {}
    for failure in failed_extractions:
        page_num = failure["page_number"]
        if page_num not in failures_by_page:
            failures_by_page[page_num] = []
        failures_by_page[page_num].append(failure)
    
    for page_num, page_failures in failures_by_page.items():
        print(f"\n📄 Rescuing {len(page_failures)} images from page {page_num}")
        
        try:
            # Convert page to high-res image
            pages = convert_from_path(pdf_path, first_page=page_num, last_page=page_num, dpi=dpi)
            if not pages:
                print(f"   ❌ Failed to convert page {page_num}")
                continue
                
            page_img = pages[0]
            page_width, page_height = page_img.size
            
            # Get PDF page dimensions
            pdf_page = doc.load_page(page_num - 1)  # 0-indexed
            pdf_rect = pdf_page.rect
            pdf_width = pdf_rect.width
            pdf_height = pdf_rect.height
            
            # Calculate scale factors
            scale_x = page_width / pdf_width
            scale_y = page_height / pdf_height
            
            print(f"   📐 Page: {page_width}×{page_height} pixels, PDF: {pdf_width:.0f}×{pdf_height:.0f} pts")
            print(f"   📏 Scale factors: {scale_x:.2f}x, {scale_y:.2f}y")
            
            for failure in page_failures:
                if not failure.get("bbox"):
                    print(f"   ⚠️ {failure['filename']}: No coordinates available")
                    continue
                
                bbox = failure["bbox"]
                
                # Convert PDF coordinates to image pixel coordinates
                left = int(bbox["x0"] * scale_x)
                top = int(bbox["y0"] * scale_y)
                right = int(bbox["x1"] * scale_x)
                bottom = int(bbox["y1"] * scale_y)
                
                # Ensure coordinates are within image bounds
                left = max(0, min(left, page_width))
                right = max(0, min(right, page_width))
                top = max(0, min(top, page_height))
                bottom = max(0, min(bottom, page_height))
                
                # Crop the specific image region
                try:
                    cropped_img = page_img.crop((left, top, right, bottom))
                    
                    # Save rescued image
                    rescue_filename = failure["filename"].replace(".png", "_RESCUED_CROPPED.png")
                    rescue_path = os.path.join(output_dir, rescue_filename)
                    cropped_img.save(rescue_path, "PNG")
                    
                    print(f"   🚀 RESCUED: {rescue_filename} ({right-left}×{bottom-top})")
                    rescue_count += 1
                    
                except Exception as e:
                    print(f"   ❌ Crop failed for {failure['filename']}: {e}")
        
        except Exception as e:
            print(f"   ❌ Page {page_num} rescue failed: {e}")
    
    doc.close()
    
    print(f"\n📊 RESCUE SUMMARY:")
    print(f"   Failed extractions: {len(failed_extractions)}")
    print(f"   Successful rescues: {rescue_count}")
    print(f"   Rescue success rate: {rescue_count/len(failed_extractions)*100:.1f}%")

def main():
    parser = argparse.ArgumentParser(description='Enhanced PDF image extraction with coordinates and rescue')
    parser.add_argument('pdf_path', help='Path to PDF file')
    parser.add_argument('-o', '--output', default='extracted_images_enhanced', 
                      help='Output directory (default: extracted_images_enhanced)')
    parser.add_argument('--rescue', action='store_true',
                      help='Attempt coordinate-aware rescue of failed extractions')
    parser.add_argument('--dpi', type=int, default=200,
                      help='DPI for rescue operation (default: 200)')
    
    args = parser.parse_args()
    
    # Perform enhanced extraction
    catalog_data = extract_images_with_coordinates(args.pdf_path, args.output)
    
    # Perform rescue if requested
    if args.rescue and catalog_data.get("failed_extractions"):
        rescue_with_coordinates(args.pdf_path, catalog_data, args.output, args.dpi)

if __name__ == "__main__":
    main()