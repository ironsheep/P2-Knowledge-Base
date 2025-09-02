#!/usr/bin/env python3
"""
Smart Pins-specific PDF Image Extractor V2
- ALWAYS includes all images, even without modes (marked as "Mode Not Known")
- Improved markdown catalog generation
- Better handling of images before mode sections
"""

import fitz  # PyMuPDF
import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class SmartPinsImageExtractorV2:
    """Enhanced Smart Pins extractor that includes ALL images."""
    
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
            mode_header_pattern = r'(%[01]{5})\s*:\s*([^\n]+)'
            mode_matches = re.findall(mode_header_pattern, text)
            
            if mode_matches:
                current_mode = mode_matches[0][0]
                current_mode_name = mode_matches[0][1].strip()
                self.mode_descriptions[current_mode] = current_mode_name
                print(f"  📍 Page {page_num + 1}: Found mode {current_mode} - {current_mode_name}")
            
            # Pattern 2: Just the mode number in various contexts
            simple_mode_pattern = r'(%[01]{5})\b'
            simple_matches = re.findall(simple_mode_pattern, text)
            if simple_matches and not mode_matches:
                for mode in simple_matches:
                    if mode in self.SMART_PIN_MODES:
                        if current_mode != mode:
                            current_mode = mode
                            print(f"  📍 Page {page_num + 1}: Mode reference {current_mode}")
                        break
            
            # Store the current mode for this page (can be None)
            mode_map[page_num + 1] = {
                "mode": current_mode,
                "mode_name": self.mode_descriptions.get(current_mode, 
                              self.SMART_PIN_MODES.get(current_mode, "Mode Not Known")),
                "full_description": current_mode_name if current_mode_name else ""
            }
        
        self.mode_page_map = mode_map
        return mode_map
    
    def _save_markdown_catalog(self, md_path: str):
        """Save Smart Pins-organized Markdown catalog that includes ALL images."""
        with open(md_path, 'w') as f:
            # Header
            f.write(f"# {self.pdf_name} - Smart Pins Image Catalog\n\n")
            f.write(f"**Document ID**: {self.doc_id}  \n")
            f.write(f"**Extraction Date**: {datetime.now().strftime('%Y-%m-%d')}  \n")
            f.write(f"**Total Images**: {len(self.image_catalog)}  \n")
            f.write(f"**Purpose**: Mode-aware extraction for Smart Pins consumption  \n\n")
            
            # Organize images by mode
            mode_groups = {}
            no_mode_images = []
            
            for img in self.image_catalog:
                mode = img["smart_pin_context"]["mode"]
                if mode and mode != "no_mode":
                    if mode not in mode_groups:
                        mode_groups[mode] = []
                    mode_groups[mode].append(img)
                else:
                    no_mode_images.append(img)
            
            # Quick Reference - Images by Mode
            f.write("## 📚 Images by Smart Pin Mode\n\n")
            
            # List images WITH modes first
            for mode in sorted(mode_groups.keys()):
                images = mode_groups[mode]
                mode_name = self.mode_descriptions.get(mode, self.SMART_PIN_MODES.get(mode, ""))
                f.write(f"### {mode}: {mode_name}\n")
                f.write(f"**{len(images)} images** - Pages: ")
                pages = sorted(set(img["page_number"] for img in images))
                f.write(f"{', '.join(map(str, pages))}\n")
                
                for img in images:
                    f.write(f"- {img['global_id']}: {img['semantic_type']} (page {img['page_number']})\n")
                f.write("\n")
            
            # List images WITHOUT modes
            if no_mode_images:
                f.write("### Images without specific mode\n")
                f.write(f"**{len(no_mode_images)} images** - Mode not identified\n")
                for img in no_mode_images:
                    f.write(f"- {img['global_id']}: Page {img['page_number']}\n")
                f.write("\n")
            
            f.write("---\n\n")
            
            # Complete Image Inventory
            f.write("## 🖼️ Complete Image Inventory\n\n")
            
            # ALWAYS include images without modes FIRST
            if no_mode_images:
                f.write("## Images Without Specific Mode\n\n")
                for img in no_mode_images:
                    f.write("---\n\n")
                    f.write(f"### {img['global_id']}: Page {img['page_number']}\n\n")
                    f.write(f"![{img['global_id']}](./{img['filename']})\n\n")
                    
                    # Core metadata
                    f.write(f"**Page**: {img['page_number']} | ")
                    f.write(f"**Type**: {img['semantic_type']} | ")
                    f.write(f"**Dimensions**: {img['dimensions']['display']}  \n")
                    f.write(f"**Mode**: Mode Not Known  \n\n")
                    
                    # Context if available
                    sp_context = img.get('smart_pin_context', {})
                    if sp_context.get('instructions'):
                        f.write(f"**Instructions Referenced**: {', '.join(sp_context['instructions'])}  \n\n")
                    
                    if sp_context.get('discussion_context'):
                        f.write("**Discussion Context**:  \n")
                        for ctx in sp_context['discussion_context'][:2]:
                            f.write(f"- {ctx.get('text', '')[:150]}...  \n")
                        f.write("\n")
                    
                    # Caption if meaningful
                    if img.get('caption') and len(img['caption']) > 10:
                        f.write(f"**Caption**: {img['caption'][:200]}  \n\n")
                f.write("\n")
            
            # Then include images WITH modes
            for mode in sorted(mode_groups.keys()):
                images = mode_groups[mode]
                mode_name = self.mode_descriptions.get(mode, self.SMART_PIN_MODES.get(mode, ""))
                
                f.write(f"## {mode}: {mode_name}\n\n")
                
                for idx, img in enumerate(images, 1):
                    f.write("---\n\n")
                    f.write(f"### {img['global_id']}: Image {idx} for {mode}\n\n")
                    
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
                    if img.get('search_keywords'):
                        f.write(f"**Search**: `{' | '.join(img['search_keywords'][:15])}`  \n\n")
            
            # Footer with summary
            f.write("---\n\n")
            f.write("## 📊 Extraction Summary\n\n")
            f.write(f"- **Total Images**: {len(self.image_catalog)}\n")
            f.write(f"- **Images with modes**: {sum(len(g) for g in mode_groups.values())}\n")
            f.write(f"- **Images without modes**: {len(no_mode_images)}\n")
            f.write(f"- **Unique Modes**: {len(mode_groups)}\n")
            if mode_groups:
                f.write(f"- **Modes with Images**: {', '.join(sorted(mode_groups.keys()))}\n")
    
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
                    "extractor_version": "3.1-smartpins-inclusive"
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
    
    # ... (include all other methods from original extractor like extract_images, etc.)
    # For brevity, I'm focusing on the key changes in the markdown generation

def main():
    print("Smart Pins Image Extractor V2 - Now includes ALL images!")
    print("Images without modes will be marked as 'Mode Not Known'")
    # Implementation would follow...

if __name__ == "__main__":
    main()