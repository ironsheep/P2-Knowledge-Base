#!/usr/bin/env python3
"""
Smart Pins-specific PDF Image Extractor
Captures mode context and Smart Pin-specific patterns for rich metadata.
"""

import fitz  # PyMuPDF
import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class SmartPinsImageExtractor:
    """Smart Pins-aware extractor that understands modes and context."""
    
    # Smart Pin modes (5-bit binary patterns)
    SMART_PIN_MODES = {
        "%00000": "repository",
        "%00001": "dac_noise", 
        "%00010": "dac_16bit_dither",
        "%00011": "dac_pwm_dither",
        "%00100": "pulse_cycle_output",
        "%00101": "transition_output",
        "%00110": "nco_frequency",
        "%00111": "nco_duty",
        "%01000": "pwm_triangle",
        "%01001": "pwm_sawtooth",
        "%01010": "pwm_smps",
        "%01011": "periodic_polling",
        "%01100": "periodic_polling_with_trigger",
        "%01101": "time_accumulator",
        "%01110": "time_accumulator_with_feedback",
        "%01111": "time_gated_accumulator",
        "%10000": "continuous_adc_filter",
        "%10001": "continuous_adc_scope",
        "%10010": "adc_scope_trigger",
        "%10011": "adc_scope_trigger_plus",
        "%10100": "usb_host",
        "%10101": "usb_device",
        "%10110": "sync_serial_tx",
        "%10111": "sync_serial_rx",
        "%11000": "async_serial_tx",
        "%11001": "async_serial_rx",
        "%11010": "async_serial_duplex",
        "%11011": "sync_serial_duplex",
        "%11100": "pulse_width_measurement",
        "%11101": "quadrature_decoder",
        "%11110": "sensor_calibration",
        "%11111": "adc_reader"
    }
    
    def __init__(self, pdf_path: str, output_dir: str = "extracted_images_smartpins"):
        """Initialize the Smart Pins extractor."""
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.pdf_name = Path(pdf_path).stem
        self.doc_id = "SP"
        self.global_id_counter = 1
        self.image_catalog = []
        
        # Track mode context as we go through pages
        self.current_mode = None
        self.mode_page_map = {}  # page_num -> mode
        self.mode_descriptions = {}  # mode -> description text
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
    def _generate_global_id(self) -> str:
        """Generate globally unique image ID."""
        global_id = f"{self.doc_id}-IMG-{self.global_id_counter:03d}"
        self.global_id_counter += 1
        return global_id
    
    def extract_mode_context(self, doc) -> Dict:
        """Pre-scan document to map pages to Smart Pin modes."""
        print("🔍 Scanning for Smart Pin modes...")
        mode_map = {}
        current_mode = None
        current_mode_name = None
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            
            # Look for mode patterns
            # Pattern 1: Mode header like "%00011: DAC output with PWM dither"
            mode_header_pattern = r'(%[01]{5})\s*:\s*([^\n]+)'
            mode_matches = re.findall(mode_header_pattern, text)
            
            if mode_matches:
                # Found new mode on this page
                current_mode = mode_matches[0][0]
                current_mode_name = mode_matches[0][1].strip()
                self.mode_descriptions[current_mode] = current_mode_name
                print(f"  📍 Page {page_num + 1}: Found mode {current_mode} - {current_mode_name}")
            
            # Pattern 2: Just the mode number in various contexts
            simple_mode_pattern = r'(%[01]{5})\b'
            simple_matches = re.findall(simple_mode_pattern, text)
            if simple_matches and not mode_matches:
                # Might be continuing previous mode or referencing it
                for mode in simple_matches:
                    if mode in self.SMART_PIN_MODES:
                        if current_mode != mode:
                            current_mode = mode
                            print(f"  📍 Page {page_num + 1}: Mode reference {current_mode}")
                        break
            
            # Pattern 3: Look for "Mode %xxxxx" or "Smart Pin Mode"
            mode_ref_pattern = r'[Mm]ode\s+(%[01]{5})'
            mode_refs = re.findall(mode_ref_pattern, text)
            if mode_refs:
                current_mode = mode_refs[0]
                print(f"  📍 Page {page_num + 1}: Mode reference {current_mode}")
            
            # Store the current mode for this page
            if current_mode:
                mode_map[page_num + 1] = {
                    "mode": current_mode,
                    "mode_name": self.mode_descriptions.get(current_mode, 
                                  self.SMART_PIN_MODES.get(current_mode, "unknown")),
                    "full_description": current_mode_name if current_mode_name else ""
                }
        
        self.mode_page_map = mode_map
        return mode_map
    
    def _extract_image_context_with_mode(self, page, img, page_num: int) -> Dict:
        """Extract context with Smart Pins-specific understanding."""
        try:
            # Get basic context first
            image_rects = page.get_image_rects(img[0])
            if not image_rects:
                return {"error": "No image position found"}
            
            img_rect = image_rects[0]
            page_text = page.get_text()
            text_blocks = page.get_text("dict")
            
            # Get the mode for this page
            page_mode_info = self.mode_page_map.get(page_num, {})
            current_mode = page_mode_info.get("mode", None)
            mode_name = page_mode_info.get("mode_name", "")
            
            # Find text near the image
            nearby_text = []
            potential_captions = []
            technical_context = []
            instruction_refs = []
            
            for block in text_blocks["blocks"]:
                if "lines" not in block:
                    continue
                
                block_rect = fitz.Rect(block["bbox"])
                
                # Calculate distance from image
                distance = min(
                    abs(block_rect.y1 - img_rect.y0),  # Above
                    abs(block_rect.y0 - img_rect.y1),  # Below
                    abs(block_rect.x1 - img_rect.x0),  # Left
                    abs(block_rect.x0 - img_rect.x1)   # Right
                )
                
                # Extract text from block
                block_text = ""
                for line in block["lines"]:
                    for span in line["spans"]:
                        block_text += span["text"] + " "
                
                block_text = block_text.strip()
                if not block_text:
                    continue
                
                # Collect text within 200 points (expanded for better context)
                if distance < 200:
                    position = (
                        "above" if block_rect.y1 < img_rect.y0 else
                        "below" if block_rect.y0 > img_rect.y1 else
                        "left" if block_rect.x1 < img_rect.x0 else "right"
                    )
                    
                    nearby_text.append({
                        "text": block_text,
                        "distance": distance,
                        "position": position
                    })
                    
                    # Look for Smart Pin-specific patterns
                    # Instructions
                    instr_pattern = r'\b(WRPIN|WXPIN|WYPIN|RDPIN|RQPIN|AKPIN|TESTP[N]?|DIRH|DIRL|DRVH|DRVL|FLTL|FLTH|OUTL|OUTH)\b'
                    instr_matches = re.findall(instr_pattern, block_text, re.IGNORECASE)
                    if instr_matches:
                        instruction_refs.extend(instr_matches)
                    
                    # Technical patterns (X/Y/Z registers, bit patterns)
                    tech_pattern = r'\b([XYZ])\[(\d+):(\d+)\]|\b([XYZ])\s*=\s*([^\s,]+)'
                    tech_matches = re.findall(tech_pattern, block_text)
                    if tech_matches:
                        technical_context.append(block_text[:100])
                    
                    # Timing references
                    if any(word in block_text.lower() for word in ['clock', 'cycle', 'timing', 'edge', 'rise', 'fall']):
                        technical_context.append(f"Timing: {block_text[:100]}")
                    
                    # Potential captions (very close and short)
                    if distance < 50 and len(block_text) < 200:
                        potential_captions.append(block_text)
            
            # Sort by distance
            nearby_text.sort(key=lambda x: x["distance"])
            
            # Determine semantic type based on Smart Pins context
            semantic_type = self._classify_smartpins_image(
                nearby_text, instruction_refs, technical_context, current_mode
            )
            
            # Extract what they were talking about
            discussion_context = self._extract_discussion_context(nearby_text, page_text, img_rect)
            
            return {
                "smart_pin_mode": current_mode,
                "mode_name": mode_name,
                "mode_description": page_mode_info.get("full_description", ""),
                "caption": potential_captions[0] if potential_captions else "",
                "nearby_text": nearby_text[:10],
                "instructions_referenced": list(set(instruction_refs)),
                "technical_context": technical_context[:3],
                "semantic_type": semantic_type,
                "discussion_context": discussion_context,
                "potential_captions": potential_captions[:3]
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _classify_smartpins_image(self, nearby_text, instructions, tech_context, mode):
        """Classify image based on Smart Pins-specific patterns."""
        combined_text = " ".join([t.get("text", "") for t in nearby_text]).lower()
        
        # Smart Pins-specific classification
        if "timing" in combined_text or "clock" in combined_text or "cycle" in combined_text:
            if "waveform" in combined_text or "signal" in combined_text:
                return "timing_waveform"
            return "timing_diagram"
        
        if any(instr in ["WRPIN", "WXPIN", "WYPIN"] for instr in instructions):
            return "pin_configuration"
        
        if "register" in combined_text or "bit field" in combined_text or "[31:0]" in combined_text:
            return "register_layout"
        
        if mode and mode in ["%10110", "%10111", "%11000", "%11001"]:  # Serial modes
            return "serial_timing"
        
        if mode and mode in ["%00001", "%00010", "%00011"]:  # DAC modes
            return "dac_output"
        
        if mode and mode == "%11101":  # Quadrature decoder
            return "quadrature_diagram"
        
        if "state" in combined_text or "machine" in combined_text:
            return "state_machine"
        
        # Default based on mode if we have one
        if mode:
            return f"mode_{mode[1:]}_diagram"  # Remove % for cleaner name
        
        return "smart_pin_diagram"
    
    def _extract_discussion_context(self, nearby_text, page_text, img_rect):
        """Extract what was being discussed when the image was referenced."""
        # Look for the paragraph before and after the image
        context_snippets = []
        
        # Get text immediately before image (likely the setup)
        before_texts = [t for t in nearby_text if t["position"] == "above" and t["distance"] < 100]
        if before_texts:
            # Take the closest one
            context_snippets.append({
                "position": "before",
                "text": before_texts[0]["text"][:200],
                "type": "introduction"
            })
        
        # Get text immediately after (likely the explanation)
        after_texts = [t for t in nearby_text if t["position"] == "below" and t["distance"] < 100]
        if after_texts:
            context_snippets.append({
                "position": "after", 
                "text": after_texts[0]["text"][:200],
                "type": "explanation"
            })
        
        # Look for "as shown" or "see figure" references
        for text_block in nearby_text[:5]:
            text = text_block.get("text", "").lower()
            if any(phrase in text for phrase in ["as shown", "see figure", "illustrated", "following diagram", "example below"]):
                context_snippets.append({
                    "position": "reference",
                    "text": text_block["text"][:150],
                    "type": "direct_reference"
                })
                break
        
        return context_snippets
    
    def extract_images(self) -> List[Dict]:
        """Extract all images with Smart Pins-specific metadata."""
        print(f"🚀 Smart Pins Extraction Starting: {self.pdf_name}")
        print(f"📋 Document ID: {self.doc_id}")
        
        try:
            doc = fitz.open(self.pdf_path)
            print(f"✅ Opened PDF: {self.pdf_path}")
            print(f"📄 Total pages: {len(doc)}")
            
            # First extract mode context
            self.extract_mode_context(doc)
            # Count unique modes
            unique_modes = set()
            for page_info in self.mode_page_map.values():
                if isinstance(page_info, dict) and 'mode' in page_info:
                    unique_modes.add(page_info['mode'])
            print(f"📊 Found {len(unique_modes)} unique modes across document")
            
        except Exception as e:
            print(f"❌ Error opening PDF: {e}")
            return []
        
        total_images = 0
        mode_image_counts = {}  # Track images per mode
        
        # Extract images from each page
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)
            
            if not image_list:
                continue
            
            # Get mode for this page
            page_mode_info = self.mode_page_map.get(page_num + 1, {})
            current_mode = page_mode_info.get("mode", "no_mode")
            
            print(f"\n📄 Page {page_num + 1}: Found {len(image_list)} images [Mode: {current_mode}]")
            
            for img_index, img in enumerate(image_list):
                # Get image data
                xref = img[0]
                try:
                    pix = fitz.Pixmap(doc, xref)
                except:
                    print(f"  ⚠️ Failed to load image xref {xref}")
                    continue
                
                # Skip small images
                if pix.width < 50 or pix.height < 50:
                    print(f"  ⏭️ Skipping small image: {pix.width}×{pix.height}")
                    pix = None
                    continue
                
                # Track images per mode
                if current_mode not in mode_image_counts:
                    mode_image_counts[current_mode] = 0
                mode_image_counts[current_mode] += 1
                
                # Generate filenames
                global_id = self._generate_global_id()
                local_ref = f"page{page_num+1:02d}_img{img_index+1:02d}"
                
                # Add mode to filename for easier identification
                if current_mode and current_mode != "no_mode":
                    mode_suffix = current_mode.replace("%", "mode")
                    img_filename = f"{self.pdf_name}_{mode_suffix}_{local_ref}.png"
                else:
                    img_filename = f"{self.pdf_name}_{local_ref}.png"
                
                img_path = os.path.join(self.output_dir, img_filename)
                
                # Save image
                if pix.n - pix.alpha < 4:  # GRAY or RGB
                    pix.save(img_path)
                else:  # CMYK: convert to RGB
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.save(img_path)
                    pix1 = None
                
                # Extract Smart Pins-specific context
                context = self._extract_image_context_with_mode(page, img, page_num + 1)
                
                # Build enhanced metadata
                metadata = {
                    "global_id": global_id,
                    "document_id": self.doc_id,
                    "local_ref": local_ref,
                    "filename": img_filename,
                    "source_pdf": os.path.basename(self.pdf_path),
                    "page_number": page_num + 1,
                    "image_index": img_index + 1,
                    "image_number_in_mode": mode_image_counts[current_mode],
                    "dimensions": {
                        "width": pix.width,
                        "height": pix.height,
                        "display": f"{pix.width}×{pix.height}"
                    },
                    "smart_pin_context": {
                        "mode": context.get("smart_pin_mode"),
                        "mode_name": context.get("mode_name"),
                        "mode_description": context.get("mode_description"),
                        "instructions": context.get("instructions_referenced", []),
                        "technical_context": context.get("technical_context", []),
                        "discussion_context": context.get("discussion_context", [])
                    },
                    "semantic_type": context.get("semantic_type", "smart_pin_diagram"),
                    "caption": context.get("caption", ""),
                    "nearby_text": context.get("nearby_text", [])[:5],
                    "search_keywords": self._generate_search_keywords(context, current_mode),
                    "consumption_hints": {
                        "ideal_size": "full_width" if pix.width > 1500 else "half_page",
                        "mode_specific": True,
                        "image_sequence": f"{mode_image_counts[current_mode]} of ? in {current_mode}"
                    }
                }
                
                self.image_catalog.append(metadata)
                total_images += 1
                
                print(f"  ✅ {global_id}: {context.get('semantic_type')} for {current_mode} ({pix.width}×{pix.height})")
                
                pix = None  # Free memory
        
        doc.close()
        
        # Report mode distribution
        print(f"\n📊 Mode Distribution:")
        for mode, count in sorted(mode_image_counts.items()):
            mode_name = self.mode_descriptions.get(mode, self.SMART_PIN_MODES.get(mode, "unknown"))
            print(f"  {mode}: {count} images - {mode_name}")
        
        print(f"\n🎯 Extraction Complete: {total_images} images")
        return self.image_catalog
    
    def _generate_search_keywords(self, context, mode):
        """Generate Smart Pins-specific search keywords."""
        keywords = set()
        
        # Add mode
        if mode:
            keywords.add(mode)
            keywords.add(mode.replace("%", "mode_"))
            
            # Add mode name if known
            mode_name = self.SMART_PIN_MODES.get(mode)
            if mode_name:
                keywords.add(mode_name)
        
        # Add instructions
        keywords.update([i.lower() for i in context.get("instructions_referenced", [])])
        
        # Add semantic type
        keywords.add(context.get("semantic_type", "diagram"))
        
        # Extract from caption
        caption = context.get("caption", "")
        if caption:
            # Extract significant words
            words = re.findall(r'\b[a-zA-Z]{3,}\b', caption)
            keywords.update([w.lower() for w in words[:10]])
        
        return list(keywords)[:25]
    
    def save_catalogs(self):
        """Save both JSON and Markdown catalogs with Smart Pins organization."""
        # Save JSON catalog
        json_path = os.path.join(self.output_dir, f"{self.pdf_name}_smartpins_catalog.json")
        with open(json_path, 'w') as f:
            json.dump({
                "metadata": {
                    "source_pdf": self.pdf_path,
                    "document_id": self.doc_id,
                    "extraction_date": datetime.now().isoformat(),
                    "total_images": len(self.image_catalog),
                    "extractor_version": "3.0-smartpins"
                },
                "mode_mapping": self.mode_page_map,
                "mode_descriptions": self.mode_descriptions,
                "images": self.image_catalog
            }, f, indent=2)
        print(f"📋 JSON catalog saved: {json_path}")
        
        # Save Markdown catalog
        md_path = os.path.join(self.output_dir, f"{self.pdf_name}_smartpins_catalog.md")
        self._save_markdown_catalog(md_path)
        print(f"📖 Markdown catalog saved: {md_path}")
    
    def _save_markdown_catalog(self, md_path: str):
        """Save Smart Pins-organized Markdown catalog."""
        with open(md_path, 'w') as f:
            # Header
            f.write(f"# {self.pdf_name} - Smart Pins Image Catalog\n\n")
            f.write(f"**Document ID**: {self.doc_id}  \n")
            f.write(f"**Extraction Date**: {datetime.now().strftime('%Y-%m-%d')}  \n")
            f.write(f"**Total Images**: {len(self.image_catalog)}  \n")
            f.write(f"**Purpose**: Mode-aware extraction for Smart Pins consumption  \n\n")
            
            # Quick Reference - Organize by Mode
            f.write("## 📚 Images by Smart Pin Mode\n\n")
            
            mode_groups = {}
            for img in self.image_catalog:
                mode = img["smart_pin_context"]["mode"]
                if mode not in mode_groups:
                    mode_groups[mode] = []
                mode_groups[mode].append(img)
            
            # Sort modes, handling None values
            sorted_modes = sorted([m for m in mode_groups.keys() if m is not None])
            if None in mode_groups:
                sorted_modes.insert(0, None)  # Put None first
            
            for mode in sorted_modes:
                if mode and mode != "no_mode":
                    images = mode_groups[mode]
                    mode_name = self.mode_descriptions.get(mode, self.SMART_PIN_MODES.get(mode, ""))
                    f.write(f"### {mode}: {mode_name}\n")
                    f.write(f"**{len(images)} images** - Pages: ")
                    pages = sorted(set(img["page_number"] for img in images))
                    f.write(f"{', '.join(map(str, pages))}\n")
                    
                    for img in images:
                        f.write(f"- {img['global_id']}: {img['semantic_type']} (page {img['page_number']})\n")
                    f.write("\n")
            
            # Images without mode
            if "no_mode" in mode_groups or None in mode_groups:
                f.write("### Images without specific mode\n")
                for key in ["no_mode", None]:
                    if key in mode_groups:
                        for img in mode_groups[key]:
                            f.write(f"- {img['global_id']}: Page {img['page_number']}\n")
                f.write("\n")
            
            f.write("---\n\n")
            
            # Individual image entries organized by mode
            f.write("## 🖼️ Complete Image Inventory\n\n")
            
            # Handle None values when sorting modes
            sorted_modes_detail = sorted([m for m in mode_groups.keys() if m is not None])
            if None in mode_groups:
                sorted_modes_detail.insert(0, None)
            
            for mode in sorted_modes_detail:
                if mode and mode != "no_mode":
                    images = mode_groups[mode]
                    mode_name = self.mode_descriptions.get(mode, self.SMART_PIN_MODES.get(mode, ""))
                    
                    f.write(f"## {mode}: {mode_name}\n\n")
                    
                    for img in images:
                        f.write("---\n\n")
                        f.write(f"### {img['global_id']}: Image {img['image_number_in_mode']} for {mode}\n\n")
                        
                        # Display the image
                        f.write(f"![{img['global_id']}](./{img['filename']})\n\n")
                        
                        # Core metadata
                        f.write(f"**Page**: {img['page_number']} | ")
                        f.write(f"**Type**: {img['semantic_type']} | ")
                        f.write(f"**Dimensions**: {img['dimensions']['display']}  \n\n")
                        
                        # Smart Pin specific context
                        sp_context = img['smart_pin_context']
                        
                        if sp_context.get('instructions'):
                            f.write(f"**Instructions Referenced**: {', '.join(sp_context['instructions'])}  \n")
                        
                        if sp_context.get('discussion_context'):
                            f.write("\n**Discussion Context**:  \n")
                            for ctx in sp_context['discussion_context']:
                                f.write(f"- **{ctx['type']}**: {ctx['text'][:150]}...  \n")
                            f.write("\n")
                        
                        if sp_context.get('technical_context'):
                            f.write("**Technical Context**:  \n")
                            for tech in sp_context['technical_context'][:2]:
                                f.write(f"- {tech[:100]}  \n")
                            f.write("\n")
                        
                        # Caption if meaningful
                        if img.get('caption') and len(img['caption']) > 10:
                            f.write(f"**Caption**: {img['caption'][:200]}  \n\n")
                        
                        # Keywords for searching
                        if img['search_keywords']:
                            f.write(f"**Search**: `{' | '.join(img['search_keywords'][:15])}`  \n\n")
            
            # Footer with summary
            f.write("---\n\n")
            f.write("## 📊 Extraction Summary\n\n")
            f.write(f"- **Total Images**: {len(self.image_catalog)}\n")
            f.write(f"- **Unique Modes**: {len(mode_groups)}\n")
            f.write(f"- **Modes with Images**: {', '.join(sorted([m for m in mode_groups.keys() if m and m != 'no_mode']))}\n")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Smart Pins-aware PDF Image Extractor')
    parser.add_argument('--extract', action='store_true',
                      help='Extract Smart Pins document with mode awareness')
    
    args = parser.parse_args()
    
    if args.extract:
        # Extract Smart Pins document
        smartpins_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/smart-pins/P2 SmartPins-220809.pdf"
        
        if not os.path.exists(smartpins_path):
            print(f"❌ Smart Pins PDF not found at: {smartpins_path}")
            sys.exit(1)
        
        print("🎯 Extracting Smart Pins with mode awareness...")
        
        # Use smart-pins specific output directory
        output_dir = os.path.join(
            "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/smart-pins/assets",
            f"images-smartpins-{datetime.now().strftime('%Y%m%d')}"
        )
        
        extractor = SmartPinsImageExtractor(smartpins_path, output_dir)
        extractor.extract_images()
        extractor.save_catalogs()
    else:
        print("Use --extract to run Smart Pins extraction with mode awareness")

if __name__ == "__main__":
    main()