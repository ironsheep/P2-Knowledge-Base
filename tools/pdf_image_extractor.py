#!/usr/bin/env python3
"""
PDF Image Extractor for P2 Knowledge Base
Extracts images from PDF documents at original quality with metadata cataloging.
"""

import fitz  # PyMuPDF
import os
import sys
import json
from pathlib import Path
import argparse
from pdf2image import convert_from_path
from PIL import Image

def extract_images_from_pdf(pdf_path, output_dir="extracted_images"):
    """
    Extract all images from a PDF document at original quality with context.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save extracted images
        
    Returns:
        list: Catalog of extracted images with metadata and context
    """
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Open PDF document
    try:
        doc = fitz.open(pdf_path)
        print(f"✅ Opened PDF: {pdf_path}")
        print(f"📄 Pages: {len(doc)}")
    except Exception as e:
        print(f"❌ Error opening PDF: {e}")
        return []
    
    image_catalog = []
    total_images = 0
    
    # Extract images from each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        
        print(f"\n📄 Page {page_num + 1}: Found {len(image_list)} images")
        
        for img_index, img in enumerate(image_list):
            # Get image data
            xref = img[0]  # Image reference number
            pix = fitz.Pixmap(doc, xref)
            
            # Skip if image is too small (likely decorative)
            if pix.width < 50 or pix.height < 50:
                print(f"  ⏭️  Skipping small image: {pix.width}×{pix.height}")
                pix = None
                continue
            
            # Generate filename
            pdf_name = Path(pdf_path).stem
            img_filename = f"{pdf_name}_page{page_num+1:02d}_img{img_index+1:02d}"
            
            # Determine format and save
            if pix.n - pix.alpha < 4:  # GRAY or RGB
                img_filename += ".png"
                img_path = os.path.join(output_dir, img_filename)
                pix.save(img_path)
            else:  # CMYK: convert to RGB
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                img_filename += ".png"
                img_path = os.path.join(output_dir, img_filename)
                pix1.save(img_path)
                pix1 = None
            
            # Check if this is a warning triangle placeholder
            file_size = os.path.getsize(img_path)
            is_placeholder = detect_placeholder_image(img_path, file_size)
            
            if is_placeholder:
                print(f"  ⚠️  WARNING: Placeholder detected - {img_filename} (extraction failed)")
                
                # Attempt rescue with pdf2image
                rescue_success = attempt_image_rescue(pdf_path, page_num, img_index, img_filename, output_dir, img)
                if rescue_success:
                    # Update file size and status after rescue
                    file_size = os.path.getsize(img_path)
                    is_placeholder = False
                    print(f"  🚀 RESCUE SUCCESS: {img_filename} recovered with pdf2image!")
            
            # Extract surrounding text for context/captions (skip for placeholders)
            text_context = {} if is_placeholder else extract_image_context(page, img)
            
            # Collect metadata with context
            image_metadata = {
                "filename": img_filename,
                "source_pdf": os.path.basename(pdf_path),
                "page_number": page_num + 1,
                "image_index": img_index + 1,
                "dimensions": f"{pix.width}×{pix.height}",
                "width": pix.width,
                "height": pix.height,
                "colorspace": pix.colorspace.name if pix.colorspace else "Unknown",
                "alpha": bool(pix.alpha),
                "file_path": img_path,
                "xref": xref,
                "extraction_status": "failed" if is_placeholder else "success",
                "file_size_bytes": file_size,
                "context": text_context,
                "suggested_tags": []
            }
            
            # Add suggested tags based on content analysis
            if pix.width > 800 or pix.height > 800:
                image_metadata["suggested_tags"].append("high-resolution")
            if pix.width / pix.height > 3 or pix.height / pix.width > 3:
                image_metadata["suggested_tags"].append("diagram")
            if "64019" in pdf_name or "64029" in pdf_name or "64020" in pdf_name:
                image_metadata["suggested_tags"].append("breakout-board")
            if "P2-EC" in pdf_name:
                image_metadata["suggested_tags"].append("edge-module")
            
            image_catalog.append(image_metadata)
            total_images += 1
            
            if not is_placeholder:
                print(f"  ✅ Extracted: {img_filename} ({pix.width}×{pix.height})")
            
            # Track extraction statistics
            if is_placeholder:
                print(f"  ❌ Failed extraction (placeholder): {img_filename}")
            
            pix = None  # Free memory
    
    # Save catalog as JSON before closing document
    catalog_path = os.path.join(output_dir, f"{Path(pdf_path).stem}_image_catalog.json")
    page_count = len(doc)  # Get page count before closing
    doc.close()
    
    with open(catalog_path, 'w') as f:
        json.dump({
            "source_pdf": pdf_path,
            "extraction_summary": {
                "total_images": total_images,
                "total_pages": page_count,
                "output_directory": output_dir
            },
            "images": image_catalog
        }, f, indent=2)
    
    print(f"\n🎯 EXTRACTION COMPLETE:")
    print(f"   📊 Total images extracted: {total_images}")
    print(f"   📁 Output directory: {output_dir}")
    print(f"   📋 Catalog saved: {catalog_path}")
    
    return image_catalog

def detect_placeholder_image(img_path, file_size):
    """
    Detect if an extracted image is a PyMuPDF warning triangle placeholder.
    
    Args:
        img_path (str): Path to the extracted image
        file_size (int): Size of the image file in bytes
        
    Returns:
        bool: True if this appears to be a placeholder image
    """
    # Common PyMuPDF placeholder size (warning triangle)
    KNOWN_PLACEHOLDER_SIZES = [16232, 16240, 16250]  # Allow small variations
    
    if file_size in KNOWN_PLACEHOLDER_SIZES:
        return True
    
    # Could add more sophisticated detection here:
    # - Check if multiple images have identical checksums
    # - Analyze image content for warning triangle pattern
    # - Check image dimensions for common placeholder sizes
    
    return False

def attempt_image_rescue(pdf_path, page_num, img_index, img_filename, output_dir, img_info):
    """
    Attempt to rescue a failed image extraction using pdf2image page rasterization.
    
    Args:
        pdf_path (str): Path to the PDF file
        page_num (int): Page number (0-indexed)
        img_index (int): Image index on the page (0-indexed)
        img_filename (str): Target filename for rescued image
        output_dir (str): Output directory
        img_info: Original image info from PyMuPDF
        
    Returns:
        bool: True if rescue was successful
    """
    try:
        print(f"    🔧 Attempting pdf2image rescue for {img_filename}...")
        print(f"    📍 Target: Page {page_num + 1}, Image {img_index + 1}, xref {img_info[0]}")
        
        # Convert specific page to high-resolution image (300 DPI)
        page_images = convert_from_path(pdf_path, 
                                      first_page=page_num + 1, 
                                      last_page=page_num + 1,
                                      dpi=300)
        
        if not page_images:
            print(f"    ❌ Failed to convert page {page_num + 1} to image")
            return False
            
        page_img = page_images[0]
        
        # Try to find the image region using PyMuPDF coordinates
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_num)
        
        # Get image rectangles for this image reference
        image_rects = page.get_image_rects(img_info[0])  # img_info[0] is xref
        print(f"    📐 Found {len(image_rects)} rectangles for xref {img_info[0]}")
        
        if image_rects:
            # Use the specific rectangle occurrence based on image index
            if len(image_rects) > img_index:
                img_rect = image_rects[img_index]
                print(f"    🎯 Using rectangle {img_index + 1}: {img_rect}")
            else:
                img_rect = image_rects[0]
                print(f"    ⚠️  Using first rectangle (only {len(image_rects)} available): {img_rect}")
            
            # Convert PDF coordinates to image pixel coordinates
            # PDF page size in points
            page_rect = page.rect
            pdf_width = page_rect.width
            pdf_height = page_rect.height
            
            # Image size in pixels (at 300 DPI)
            img_width, img_height = page_img.size
            
            # Scale factors
            scale_x = img_width / pdf_width
            scale_y = img_height / pdf_height
            
            # Convert coordinates
            left = int(img_rect.x0 * scale_x)
            top = int(img_rect.y0 * scale_y)
            right = int(img_rect.x1 * scale_x)
            bottom = int(img_rect.y1 * scale_y)
            
            # Crop the image region
            cropped_img = page_img.crop((left, top, right, bottom))
            
            # Save the rescued image
            img_path = os.path.join(output_dir, img_filename)
            cropped_img.save(img_path, "PNG", optimize=False)
            
            # Verify the rescue actually worked by checking it's not a tiny placeholder
            if cropped_img.size[0] < 50 or cropped_img.size[1] < 50:
                print(f"    ❌ Rescue failed: Cropped region too small ({cropped_img.size[0]}×{cropped_img.size[1]})")
                doc.close()
                return False
                
            print(f"    ✅ Rescue successful: {cropped_img.size[0]}×{cropped_img.size[1]} pixels")
            doc.close()
            return True
        
        doc.close()
        print(f"    ❌ No image rectangle found for rescue")
        return False
        
    except Exception as e:
        print(f"    ❌ Rescue failed: {e}")
        return False

def extract_image_context(page, img):
    """
    Extract text context around an image for captions/titles.
    
    Args:
        page: PDF page object
        img: Image tuple from page.get_images()
        
    Returns:
        dict: Context information including nearby text
    """
    try:
        # Get image position on page
        image_rects = page.get_image_rects(img[0])
        if not image_rects:
            return {"caption": "", "nearby_text": "", "error": "No image position found"}
            
        img_rect = image_rects[0]  # Use first occurrence
        
        # Get all text blocks on the page
        text_blocks = page.get_text("dict")
        
        # Find text near the image (within reasonable distance)
        nearby_text = []
        potential_captions = []
        
        for block in text_blocks["blocks"]:
            if "lines" not in block:
                continue
                
            block_rect = fitz.Rect(block["bbox"])
            
            # Calculate distance from image
            distance = min(
                abs(block_rect.y1 - img_rect.y0),  # Text above image
                abs(block_rect.y0 - img_rect.y1),  # Text below image
                abs(block_rect.x1 - img_rect.x0),  # Text left of image
                abs(block_rect.x0 - img_rect.x1)   # Text right of image
            )
            
            # Collect text within 100 points of image
            if distance < 100:
                block_text = ""
                for line in block["lines"]:
                    for span in line["spans"]:
                        block_text += span["text"] + " "
                
                block_text = block_text.strip()
                if block_text:
                    nearby_text.append({
                        "text": block_text,
                        "distance": distance,
                        "position": "above" if block_rect.y1 < img_rect.y0 else 
                                   "below" if block_rect.y0 > img_rect.y1 else
                                   "left" if block_rect.x1 < img_rect.x0 else "right"
                    })
                    
                    # Potential captions (short text close to image)
                    if distance < 50 and len(block_text) < 200:
                        potential_captions.append(block_text)
        
        # Sort by distance and get closest text
        nearby_text.sort(key=lambda x: x["distance"])
        
        # Best guess at caption (closest short text)
        caption = potential_captions[0] if potential_captions else ""
        
        return {
            "caption": caption,
            "nearby_text": nearby_text[:5],  # Top 5 closest text blocks
            "potential_captions": potential_captions[:3]
        }
        
    except Exception as e:
        return {"caption": "", "nearby_text": "", "error": str(e)}

def main():
    parser = argparse.ArgumentParser(description='Extract images from PDF at original quality')
    parser.add_argument('pdf_path', help='Path to PDF file')
    parser.add_argument('-o', '--output', default='extracted_images', 
                      help='Output directory (default: extracted_images)')
    parser.add_argument('--test', action='store_true', 
                      help='Test mode: extract from first P2 Edge PDF found')
    
    args = parser.parse_args()
    
    if args.test:
        # Test with P2 Edge PDFs
        sources_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/sources/originals"
        test_pdfs = [
            "64019-P2-Edge-MiniBreakoutBoardGuide-v1.1.pdf",
            "64029-P2-Edge-Breakout-Board-Guide-20230301.pdf", 
            "64020-P2-Edge-Module-Breadboard-Product-Guide-REVB.pdf"
        ]
        
        for pdf_name in test_pdfs:
            pdf_path = os.path.join(sources_dir, pdf_name)
            if os.path.exists(pdf_path):
                print(f"\n🧪 TESTING with: {pdf_name}")
                extract_images_from_pdf(pdf_path, f"test_extraction_{Path(pdf_name).stem}")
                break
        else:
            print("❌ No test PDFs found in sources/originals/")
    else:
        if not os.path.exists(args.pdf_path):
            print(f"❌ PDF file not found: {args.pdf_path}")
            sys.exit(1)
        
        extract_images_from_pdf(args.pdf_path, args.output)

if __name__ == "__main__":
    main()