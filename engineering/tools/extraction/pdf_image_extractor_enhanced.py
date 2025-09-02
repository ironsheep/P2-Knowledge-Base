#!/usr/bin/env python3
"""
Enhanced PDF Image Extractor for P2 Knowledge Base
Extracts images with rich metadata for cross-document consumption.
Generates both JSON and Markdown catalogs with clear image separation.
"""

import fitz  # PyMuPDF
import os
import sys
import json
import re
import hashlib
from pathlib import Path
import argparse
from pdf2image import convert_from_path
from PIL import Image
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class EnhancedPDFImageExtractor:
    """Enhanced extractor with rich metadata capture for document consumption."""
    
    # Document ID mapping (expand as needed)
    DOCUMENT_IDS = {
        "SmartPins": "SP",
        "P2 SmartPins": "SP",
        "PASM2": "PASM",
        "Spin2": "SPIN",
        "P2 Documentation": "P2DOC",
        "P2 Edge": "EDGE",
        "Silicon": "SIL"
    }
    
    # Semantic type patterns
    DIAGRAM_PATTERNS = {
        "timing_diagram": ["timing", "clock", "cycle", "delay", "waveform", "signal"],
        "block_diagram": ["block", "module", "component", "architecture", "system"],
        "pin_diagram": ["pin", "pinout", "connector", "physical", "layout"],
        "schematic": ["schematic", "circuit", "electrical", "voltage", "current"],
        "flow_diagram": ["flow", "process", "sequence", "step", "procedure"],
        "state_diagram": ["state", "machine", "transition", "fsm"],
        "register_diagram": ["register", "bit", "field", "configuration"],
        "waveform": ["waveform", "oscilloscope", "trace", "signal"],
        "example": ["example", "sample", "demo", "illustration"],
        "comparison": ["comparison", "versus", "vs", "difference", "contrast"]
    }
    
    def __init__(self, pdf_path: str, output_dir: str = "extracted_images_enhanced"):
        """Initialize the enhanced extractor."""
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.pdf_name = Path(pdf_path).stem
        self.doc_id = self._determine_document_id()
        self.global_id_counter = 1
        self.image_catalog = []
        self.document_structure = {}
        
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
    def _determine_document_id(self) -> str:
        """Determine document ID from filename."""
        for key, doc_id in self.DOCUMENT_IDS.items():
            if key.lower() in self.pdf_name.lower():
                return doc_id
        return "DOC"  # Default if no match
        
    def _generate_global_id(self) -> str:
        """Generate globally unique image ID."""
        global_id = f"{self.doc_id}-IMG-{self.global_id_counter:03d}"
        self.global_id_counter += 1
        return global_id
        
    def extract_document_structure(self) -> Dict:
        """Extract PDF structure including bookmarks and headings."""
        structure = {
            "outline": [],
            "total_pages": 0,
            "sections": {}
        }
        
        try:
            doc = fitz.open(self.pdf_path)
            structure["total_pages"] = len(doc)
            
            # Extract PDF outline (bookmarks)
            toc = doc.get_toc()
            if toc:
                for level, title, page in toc:
                    structure["outline"].append({
                        "level": level,
                        "title": title,
                        "page": page
                    })
                    
                    # Map pages to sections
                    if page not in structure["sections"]:
                        structure["sections"][page] = []
                    structure["sections"][page].append({
                        "level": level,
                        "title": title
                    })
            
            # Extract heading-like text from each page
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                blocks = page.get_text("dict")
                
                page_headings = self._extract_headings_from_page(blocks)
                if page_headings:
                    if page_num + 1 not in structure["sections"]:
                        structure["sections"][page_num + 1] = []
                    structure["sections"][page_num + 1].extend(page_headings)
            
            doc.close()
            
        except Exception as e:
            print(f"⚠️ Error extracting document structure: {e}")
            
        self.document_structure = structure
        return structure
    
    def _extract_headings_from_page(self, blocks: Dict) -> List[Dict]:
        """Extract heading-like text from page blocks."""
        headings = []
        
        for block in blocks.get("blocks", []):
            if "lines" not in block:
                continue
                
            for line in block["lines"]:
                if not line.get("spans"):
                    continue
                    
                # Check first span for heading characteristics
                span = line["spans"][0]
                text = span.get("text", "").strip()
                
                if not text:
                    continue
                
                # Heading detection heuristics
                font_size = span.get("size", 0)
                flags = span.get("flags", 0)
                
                # Check for heading patterns
                is_heading = False
                level = 3  # Default level
                
                # Pattern 1: Numbered sections (1., 1.1, 1.1.1)
                if re.match(r'^\d+(\.\d+)*\.?\s+\w', text):
                    is_heading = True
                    level = text.count('.') + 1
                    
                # Pattern 2: All caps (more than 3 words)
                elif text.isupper() and len(text.split()) > 2:
                    is_heading = True
                    level = 1
                    
                # Pattern 3: Large font or bold
                elif font_size > 12 or (flags & 2**4):  # Bold flag
                    is_heading = True
                    level = 2 if font_size > 14 else 3
                
                if is_heading:
                    headings.append({
                        "level": level,
                        "title": text,
                        "font_size": font_size,
                        "position": line["bbox"]
                    })
        
        return headings
    
    def _determine_section_hierarchy(self, page_num: int) -> Dict:
        """Determine section hierarchy for a given page."""
        hierarchy = {
            "chapter": "",
            "section": "",
            "subsection": ""
        }
        
        # Look for sections mapped to this page
        page_sections = self.document_structure.get("sections", {}).get(page_num, [])
        
        if page_sections:
            for section in page_sections:
                level = section.get("level", 3)
                title = section.get("title", "")
                
                if level == 1:
                    hierarchy["chapter"] = title
                elif level == 2:
                    hierarchy["section"] = title
                elif level == 3:
                    hierarchy["subsection"] = title
        
        # Also check previous pages for inherited chapter/section
        if not hierarchy["chapter"]:
            for p in range(page_num, 0, -1):
                prev_sections = self.document_structure.get("sections", {}).get(p, [])
                for section in prev_sections:
                    if section.get("level") == 1 and not hierarchy["chapter"]:
                        hierarchy["chapter"] = section.get("title", "")
                        break
        
        return hierarchy
    
    def _classify_semantic_type(self, context: Dict, page_text: str) -> str:
        """Classify image semantic type based on context."""
        combined_text = (
            context.get("caption", "") + " " +
            " ".join([t.get("text", "") for t in context.get("nearby_text", [])])
        ).lower()
        
        # Add page text for broader context
        combined_text += " " + page_text.lower()
        
        # Score each type based on keyword matches
        type_scores = {}
        for diagram_type, keywords in self.DIAGRAM_PATTERNS.items():
            score = sum(1 for keyword in keywords if keyword in combined_text)
            if score > 0:
                type_scores[diagram_type] = score
        
        # Return highest scoring type, or "diagram" as default
        if type_scores:
            return max(type_scores.items(), key=lambda x: x[1])[0]
        return "diagram"
    
    def _extract_technical_subjects(self, context: Dict, page_text: str) -> List[str]:
        """Extract technical subjects and terms from context."""
        subjects = []
        
        combined_text = (
            context.get("caption", "") + " " +
            " ".join([t.get("text", "") for t in context.get("nearby_text", [])])
        )
        
        # Common P2 technical terms to look for
        technical_patterns = [
            r'\b[A-Z]{3,}\b',  # Instructions like DRVH, WRPIN
            r'\bP\d+\b',  # Pin references like P0, P15
            r'\b\d+\s*MHz\b',  # Frequencies
            r'\b\d+\s*ns\b',  # Nanoseconds
            r'\b\d+\s*cycle[s]?\b',  # Clock cycles
            r'\bsmart\s*pin[s]?\b',  # Smart pins
            r'\bmode\s*\d+\b',  # Mode numbers
            r'\b(?:input|output|high|low|clock|data|signal)\b'  # Common signals
        ]
        
        for pattern in technical_patterns:
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            subjects.extend([m.strip() for m in matches])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_subjects = []
        for subj in subjects:
            if subj.lower() not in seen:
                seen.add(subj.lower())
                unique_subjects.append(subj)
        
        return unique_subjects[:10]  # Limit to top 10
    
    def _extract_enhanced_context(self, page, img, page_num: int) -> Dict:
        """Extract enhanced context with wider search and better classification."""
        try:
            # Get image position on page
            image_rects = page.get_image_rects(img[0])
            if not image_rects:
                return {"error": "No image position found"}
            
            img_rect = image_rects[0]
            
            # Get all text from page
            page_text = page.get_text()
            text_blocks = page.get_text("dict")
            
            # Find text near the image with expanded radius
            nearby_text = []
            potential_captions = []
            figure_references = []
            code_blocks = []
            
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
                
                # Collect text within 150 points (expanded from 100)
                if distance < 150:
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
                    
                    # Check for figure references
                    fig_match = re.search(r'(Figure|Fig\.?)\s*(\d+[\.\-]?\d*)', block_text)
                    if fig_match:
                        figure_references.append(fig_match.group(0))
                    
                    # Check for code blocks (monospace font or code patterns)
                    if re.search(r'^\s*(\/\/|#|PUB|PRI|DAT|CON|VAR|WRPIN|WXPIN|RDPIN|DRVH|DRVL)', block_text):
                        code_blocks.append(block_text[:200])  # First 200 chars
                    
                    # Potential captions (close and short)
                    if distance < 50 and len(block_text) < 200:
                        potential_captions.append(block_text)
            
            # Sort by distance
            nearby_text.sort(key=lambda x: x["distance"])
            
            # Determine section hierarchy
            hierarchy = self._determine_section_hierarchy(page_num)
            
            # Classify semantic type
            semantic_type = self._classify_semantic_type(
                {"caption": potential_captions[0] if potential_captions else "",
                 "nearby_text": nearby_text},
                page_text
            )
            
            # Extract technical subjects
            technical_subjects = self._extract_technical_subjects(
                {"caption": potential_captions[0] if potential_captions else "",
                 "nearby_text": nearby_text},
                page_text
            )
            
            return {
                "caption": potential_captions[0] if potential_captions else "",
                "nearby_text": nearby_text[:10],  # Top 10 closest
                "potential_captions": potential_captions[:3],
                "figure_references": figure_references,
                "code_context": code_blocks[:2],  # Up to 2 code blocks
                "section_hierarchy": hierarchy,
                "semantic_type": semantic_type,
                "technical_subjects": technical_subjects,
                "page_text_sample": page_text[:500]  # First 500 chars of page
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def extract_images(self) -> List[Dict]:
        """Extract all images with enhanced metadata."""
        print(f"🚀 Enhanced Extraction Starting: {self.pdf_name}")
        print(f"📋 Document ID: {self.doc_id}")
        
        # First extract document structure
        print("📚 Extracting document structure...")
        self.extract_document_structure()
        
        try:
            doc = fitz.open(self.pdf_path)
            print(f"✅ Opened PDF: {self.pdf_path}")
            print(f"📄 Total pages: {len(doc)}")
        except Exception as e:
            print(f"❌ Error opening PDF: {e}")
            return []
        
        total_images = 0
        
        # Extract images from each page
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)
            
            if not image_list:
                continue
                
            print(f"\n📄 Page {page_num + 1}: Found {len(image_list)} images")
            
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
                
                # Generate filenames
                global_id = self._generate_global_id()
                local_ref = f"page{page_num+1:02d}_img{img_index+1:02d}"
                img_filename = f"{self.pdf_name}_{local_ref}.png"
                img_path = os.path.join(self.output_dir, img_filename)
                
                # Save image
                if pix.n - pix.alpha < 4:  # GRAY or RGB
                    pix.save(img_path)
                else:  # CMYK: convert to RGB
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.save(img_path)
                    pix1 = None
                
                # Check for placeholder
                file_size = os.path.getsize(img_path)
                is_placeholder = self._detect_placeholder(img_path, file_size)
                
                if is_placeholder:
                    print(f"  ⚠️ Placeholder detected: {global_id}")
                    # Could attempt rescue here
                
                # Extract enhanced context
                context = self._extract_enhanced_context(page, img, page_num + 1)
                
                # Build enhanced metadata
                metadata = {
                    "global_id": global_id,
                    "document_id": self.doc_id,
                    "local_ref": local_ref,
                    "filename": img_filename,
                    "source_pdf": os.path.basename(self.pdf_path),
                    "page_number": page_num + 1,
                    "image_index": img_index + 1,
                    "dimensions": {
                        "width": pix.width,
                        "height": pix.height,
                        "display": f"{pix.width}×{pix.height}"
                    },
                    "technical_data": {
                        "xref": xref,
                        "colorspace": pix.colorspace.name if pix.colorspace else "Unknown",
                        "alpha": bool(pix.alpha),
                        "file_size_bytes": file_size,
                        "extraction_status": "failed" if is_placeholder else "success"
                    },
                    "section_hierarchy": context.get("section_hierarchy", {}),
                    "semantic_type": context.get("semantic_type", "diagram"),
                    "technical_subjects": context.get("technical_subjects", []),
                    "figure_reference": context.get("figure_references", [])[0] if context.get("figure_references") else None,
                    "caption": context.get("caption", ""),
                    "nearby_text": context.get("nearby_text", [])[:5],
                    "code_context": context.get("code_context", []),
                    "pedagogical_purpose": self._determine_pedagogical_purpose(context),
                    "search_keywords": self._generate_search_keywords(context),
                    "consumption_hints": self._generate_consumption_hints(pix, context)
                }
                
                self.image_catalog.append(metadata)
                total_images += 1
                
                print(f"  ✅ {global_id}: {context.get('semantic_type', 'diagram')} ({pix.width}×{pix.height})")
                
                pix = None  # Free memory
        
        doc.close()
        
        print(f"\n🎯 Extraction Complete: {total_images} images")
        return self.image_catalog
    
    def _detect_placeholder(self, img_path: str, file_size: int) -> bool:
        """Detect placeholder images."""
        KNOWN_PLACEHOLDER_SIZES = [16232, 16240, 16250]
        return file_size in KNOWN_PLACEHOLDER_SIZES
    
    def _determine_pedagogical_purpose(self, context: Dict) -> str:
        """Determine pedagogical purpose from context."""
        combined_text = (
            context.get("caption", "") + " " +
            " ".join([t.get("text", "") for t in context.get("nearby_text", [])])
        ).lower()
        
        if "example" in combined_text or "sample" in combined_text:
            return "example"
        elif "introduction" in combined_text or "overview" in combined_text:
            return "introduction"
        elif "reference" in combined_text or "table" in combined_text:
            return "reference"
        elif "compar" in combined_text or "versus" in combined_text:
            return "comparison"
        else:
            return "explanation"
    
    def _generate_search_keywords(self, context: Dict) -> List[str]:
        """Generate search keywords from all context."""
        keywords = set()
        
        # Add technical subjects
        keywords.update([s.lower() for s in context.get("technical_subjects", [])])
        
        # Add semantic type
        keywords.add(context.get("semantic_type", "diagram"))
        
        # Extract key terms from caption
        caption = context.get("caption", "")
        if caption:
            # Extract significant words (not common words)
            words = re.findall(r'\b[a-zA-Z]{3,}\b', caption)
            keywords.update([w.lower() for w in words 
                           if w.lower() not in {'the', 'and', 'for', 'with', 'this', 'that'}])
        
        return list(keywords)[:20]  # Limit to 20 keywords
    
    def _generate_consumption_hints(self, pix, context: Dict) -> Dict:
        """Generate hints for how to best consume this image."""
        hints = {
            "ideal_size": "full_width" if pix.width > 1500 else "half_page" if pix.width > 800 else "inline",
            "requires_caption": bool(context.get("caption")),
            "color_important": pix.colorspace.name != "DeviceGray" if pix.colorspace else False,
            "high_detail": pix.width > 2000 or pix.height > 1500,
            "aspect_ratio": round(pix.width / pix.height, 2) if pix.height > 0 else 1
        }
        return hints
    
    def save_catalogs(self):
        """Save both JSON and Markdown catalogs."""
        # Save JSON catalog
        json_path = os.path.join(self.output_dir, f"{self.pdf_name}_catalog.json")
        with open(json_path, 'w') as f:
            json.dump({
                "metadata": {
                    "source_pdf": self.pdf_path,
                    "document_id": self.doc_id,
                    "extraction_date": datetime.now().isoformat(),
                    "total_images": len(self.image_catalog),
                    "extractor_version": "2.0-enhanced"
                },
                "document_structure": self.document_structure,
                "images": self.image_catalog
            }, f, indent=2)
        print(f"📋 JSON catalog saved: {json_path}")
        
        # Save Markdown catalog
        md_path = os.path.join(self.output_dir, f"{self.pdf_name}_catalog.md")
        self._save_markdown_catalog(md_path)
        print(f"📖 Markdown catalog saved: {md_path}")
    
    def _save_markdown_catalog(self, md_path: str):
        """Save human-readable Markdown catalog with clear separation."""
        with open(md_path, 'w') as f:
            # Header
            f.write(f"# {self.pdf_name} - Enhanced Image Catalog\n\n")
            f.write(f"**Document ID**: {self.doc_id}  \n")
            f.write(f"**Extraction Date**: {datetime.now().strftime('%Y-%m-%d')}  \n")
            f.write(f"**Total Images**: {len(self.image_catalog)}  \n")
            f.write(f"**Purpose**: Rich metadata for cross-document image consumption  \n\n")
            
            # Quick Reference Section
            f.write("## 📚 Quick Reference\n\n")
            
            # Group by semantic type
            type_groups = {}
            for img in self.image_catalog:
                sem_type = img["semantic_type"]
                if sem_type not in type_groups:
                    type_groups[sem_type] = []
                type_groups[sem_type].append(img["global_id"])
            
            f.write("### Images by Type\n")
            for sem_type, ids in sorted(type_groups.items()):
                f.write(f"- **{sem_type}**: {', '.join(ids)}\n")
            f.write("\n")
            
            # Group by section
            section_groups = {}
            for img in self.image_catalog:
                chapter = img["section_hierarchy"].get("chapter", "Unknown")
                if chapter not in section_groups:
                    section_groups[chapter] = []
                section_groups[chapter].append(img["global_id"])
            
            if len(section_groups) > 1:  # Only show if we have sections
                f.write("### Images by Section\n")
                for section, ids in sorted(section_groups.items()):
                    if section:  # Skip empty sections
                        f.write(f"- **{section}**: {', '.join(ids)}\n")
                f.write("\n")
            
            f.write("---\n\n")
            
            # Individual image entries with clear separation
            f.write("## 🖼️ Complete Image Inventory\n\n")
            
            for img in self.image_catalog:
                f.write("---\n\n")
                f.write(f"## {img['global_id']}: {img.get('caption', 'Image on Page ' + str(img['page_number']))}\n\n")
                
                # Display the image
                f.write(f"![{img['global_id']}](./{img['filename']})\n\n")
                
                # Metadata in structured format
                f.write(f"**Page**: {img['page_number']} | ")
                f.write(f"**Type**: {img['semantic_type']} | ")
                f.write(f"**Purpose**: {img['pedagogical_purpose']}  \n")
                f.write(f"**Dimensions**: {img['dimensions']['display']} | ")
                f.write(f"**Size**: {img['consumption_hints']['ideal_size']}  \n\n")
                
                # Section hierarchy if available
                hierarchy = img['section_hierarchy']
                if any(hierarchy.values()):
                    f.write("**Section Hierarchy**:  \n")
                    if hierarchy.get('chapter'):
                        f.write(f"📁 {hierarchy['chapter']}  \n")
                    if hierarchy.get('section'):
                        f.write(f"  📂 {hierarchy['section']}  \n")
                    if hierarchy.get('subsection'):
                        f.write(f"    📄 {hierarchy['subsection']}  \n")
                    f.write("\n")
                
                # Technical subjects if present
                if img['technical_subjects']:
                    f.write(f"**Technical Content**: {', '.join(img['technical_subjects'])}  \n\n")
                
                # Figure reference if present
                if img.get('figure_reference'):
                    f.write(f"**Reference**: {img['figure_reference']}  \n\n")
                
                # Code context if present
                if img.get('code_context'):
                    f.write("**Associated Code**:  \n")
                    f.write("```\n")
                    f.write(img['code_context'][0][:200])  # First 200 chars
                    f.write("\n```\n\n")
                
                # Search keywords
                if img['search_keywords']:
                    f.write(f"**Keywords**: `{' | '.join(img['search_keywords'][:10])}`  \n\n")
                
                # Consumption hints
                hints = img['consumption_hints']
                f.write("**Consumption Hints**:  \n")
                f.write(f"- Ideal size: {hints['ideal_size']}  \n")
                if hints.get('high_detail'):
                    f.write(f"- ⚠️ High detail image - preserve resolution  \n")
                if hints.get('color_important'):
                    f.write(f"- 🎨 Color is important  \n")
                f.write("\n")
            
            # Footer
            f.write("---\n\n")
            f.write("## 📊 Extraction Summary\n\n")
            f.write(f"- **Total Images**: {len(self.image_catalog)}\n")
            f.write(f"- **Successful Extractions**: {sum(1 for img in self.image_catalog if img['technical_data']['extraction_status'] == 'success')}\n")
            f.write(f"- **Failed Extractions**: {sum(1 for img in self.image_catalog if img['technical_data']['extraction_status'] == 'failed')}\n")
            f.write(f"- **Document Structure Extracted**: {'Yes' if self.document_structure.get('outline') else 'Partial'}\n")
            f.write(f"- **Unique Sections**: {len(set(img['section_hierarchy'].get('chapter', '') for img in self.image_catalog))}\n")

def main():
    parser = argparse.ArgumentParser(description='Enhanced PDF Image Extractor with Rich Metadata')
    parser.add_argument('pdf_path', nargs='?', help='Path to PDF file')
    parser.add_argument('-o', '--output', default=None, 
                      help='Output directory (default: extracted_images_enhanced_YYYYMMDD)')
    parser.add_argument('--smartpins', action='store_true',
                      help='Extract Smart Pins document with enhanced metadata')
    
    args = parser.parse_args()
    
    # Generate output directory with date if not specified
    if not args.output:
        date_str = datetime.now().strftime('%Y%m%d')
        args.output = f"extracted_images_enhanced_{date_str}"
    
    if args.smartpins or not args.pdf_path:
        # Extract Smart Pins document
        smartpins_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/smart-pins/P2 SmartPins-220809.pdf"
        
        if not os.path.exists(smartpins_path):
            print(f"❌ Smart Pins PDF not found at: {smartpins_path}")
            sys.exit(1)
        
        print("🎯 Extracting Smart Pins document with enhanced metadata...")
        
        # Use smart-pins specific output directory
        output_dir = os.path.join(
            "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/smart-pins/assets",
            f"images-enhanced-{datetime.now().strftime('%Y%m%d')}"
        )
        
        extractor = EnhancedPDFImageExtractor(smartpins_path, output_dir)
        extractor.extract_images()
        extractor.save_catalogs()
        
    else:
        if not os.path.exists(args.pdf_path):
            print(f"❌ PDF file not found: {args.pdf_path}")
            sys.exit(1)
        
        extractor = EnhancedPDFImageExtractor(args.pdf_path, args.output)
        extractor.extract_images()
        extractor.save_catalogs()

if __name__ == "__main__":
    main()