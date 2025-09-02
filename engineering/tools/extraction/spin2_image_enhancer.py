#!/usr/bin/env python3
"""
Spin2 v51 Image Enhancer
Enriches extracted images with .docx narrative context and global IDs
"""

import json
import re
from pathlib import Path
from datetime import datetime

class Spin2ImageEnhancer:
    def __init__(self):
        self.doc_id = "SPIN"
        self.base_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/spin2-v51")
        self.assets_path = self.base_path / "assets" / "images-20250824"
        self.narrative_path = self.base_path / "spin2-v51-narrative.txt"
        
        # Debug-specific patterns
        self.debug_patterns = {
            'debug_commands': r'DEBUG\s*\([^)]+\)',
            'display_types': r'(PLOT|SCOPE|SCOPE_XY|TERM|LOGIC|BITMAP|FFT)',
            'window_types': r'(Output|Input|Status|Watch)',
            'debug_modes': r'(ubin|udec|uhex|sbin|sdec|shex)',
            'pc_commands': r'PC_(KEY|MOUSE)',
            'trigger_modes': r'TRIGGER\s+\w+\s+AUTO'
        }
        
        # Enhanced context for each image based on page numbers
        self.page_contexts = {
            25: {
                "section": "DEBUG Command Introduction",
                "topic": "Bitfield Display Examples",
                "description": "Shows DEBUG output for bitfield indexing examples"
            },
            31: {
                "section": "DEBUG Displays",
                "topic": "TERM Display Mode",
                "description": "Terminal window display for text output"
            },
            33: {
                "section": "DEBUG Displays",
                "topic": "PLOT Display Mode",
                "description": "XY plotting display with traces and sprites"
            },
            34: {
                "section": "DEBUG Displays",
                "topic": "PLOT Configuration",
                "description": "PLOT display configuration and scaling"
            },
            35: {
                "section": "DEBUG Displays",
                "topic": "SCOPE Display Mode",
                "description": "Oscilloscope-style waveform display"
            },
            36: {
                "section": "DEBUG Displays",
                "topic": "SCOPE Configuration",
                "description": "SCOPE display settings and triggers"
            },
            37: {
                "section": "DEBUG Displays",
                "topic": "SCOPE_XY Display Mode",
                "description": "XY oscilloscope display for phase patterns"
            },
            38: {
                "section": "DEBUG Displays",
                "topic": "FFT Display Mode",
                "description": "Fast Fourier Transform spectrum analyzer"
            },
            39: {
                "section": "DEBUG Displays",
                "topic": "FFT Configuration",
                "description": "FFT display settings and windows"
            },
            40: {
                "section": "DEBUG Displays",
                "topic": "LOGIC Display Mode",
                "description": "Logic analyzer display for digital signals"
            },
            41: {
                "section": "DEBUG Displays",
                "topic": "LOGIC Configuration",
                "description": "Logic analyzer timing and triggers"
            },
            42: {
                "section": "DEBUG Displays",
                "topic": "BITMAP Display Mode",
                "description": "Bitmap graphics display for pixel data"
            },
            43: {
                "section": "DEBUG Displays",
                "topic": "BITMAP Configuration",
                "description": "Bitmap display formats and colors"
            },
            44: {
                "section": "DEBUG Commands",
                "topic": "PC_KEY Input",
                "description": "Keyboard input from host computer"
            },
            45: {
                "section": "DEBUG Commands",
                "topic": "PC_MOUSE Input",
                "description": "Mouse input and pixel color reading"
            },
            47: {
                "section": "DEBUG Features",
                "topic": "Anti-aliasing",
                "description": "Gamma-corrected alpha blending for smooth displays"
            },
            48: {
                "section": "DEBUG Features",
                "topic": "Clock Adaptation",
                "description": "Runtime clock frequency adaptation for DEBUG"
            }
        }
        
    def load_existing_catalog(self):
        """Load the existing JSON catalog"""
        catalog_path = self.assets_path / "P2 Spin2 Documentation v51-250425_image_catalog.json"
        with open(catalog_path, 'r') as f:
            return json.load(f)
    
    def load_narrative(self):
        """Load the .docx narrative text"""
        with open(self.narrative_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_debug_context(self, narrative, page_num):
        """Extract DEBUG-related context for a specific page"""
        context = {}
        
        # Find DEBUG commands near this page reference
        page_marker = f"page {page_num}"
        lines = narrative.split('\n')
        
        # Search for DEBUG patterns
        debug_commands = []
        display_types = []
        
        for pattern_name, pattern in self.debug_patterns.items():
            matches = re.findall(pattern, narrative, re.IGNORECASE)
            if matches:
                if pattern_name == 'debug_commands':
                    debug_commands.extend(matches[:5])  # First 5 matches
                elif pattern_name == 'display_types':
                    display_types.extend(set(matches))
        
        context['debug_commands'] = debug_commands
        context['display_types'] = display_types
        
        return context
    
    def enhance_image(self, image_data, narrative, image_counter):
        """Enhance a single image with context"""
        page_num = image_data['page_number']
        
        # Generate global ID
        global_id = f"{self.doc_id}-IMG-{image_counter:03d}"
        
        # Get page-specific context
        page_context = self.page_contexts.get(page_num, {})
        
        # Extract DEBUG context from narrative
        debug_context = self.extract_debug_context(narrative, page_num)
        
        # Build enhanced metadata
        enhanced = {
            "global_id": global_id,
            "document_id": self.doc_id,
            "original_data": image_data,
            "enhanced_context": {
                "section": page_context.get("section", "DEBUG Documentation"),
                "topic": page_context.get("topic", "DEBUG Display"),
                "description": page_context.get("description", ""),
                "narrative_context": self.get_narrative_snippet(narrative, page_num),
                "debug_info": {
                    "commands": debug_context.get('debug_commands', []),
                    "display_types": debug_context.get('display_types', [])
                },
                "extraction_source": "Parallax Spin2 Documentation v51.docx",
                "enhancement_date": datetime.now().isoformat()
            },
            "semantic_type": self.classify_image_type(page_context.get("topic", "")),
            "search_keywords": self.generate_keywords(page_context, debug_context)
        }
        
        return enhanced
    
    def get_narrative_snippet(self, narrative, page_num):
        """Get relevant narrative snippet for the page"""
        lines = narrative.split('\n')
        
        # Find lines mentioning DEBUG or display types
        relevant_lines = []
        for i, line in enumerate(lines):
            if 'DEBUG' in line.upper() or any(display in line for display in ['PLOT', 'SCOPE', 'TERM', 'LOGIC', 'BITMAP', 'FFT']):
                # Get context around the match
                start = max(0, i - 1)
                end = min(len(lines), i + 2)
                snippet = ' '.join(lines[start:end]).strip()
                if snippet and len(snippet) > 20:
                    relevant_lines.append(snippet)
                    if len(relevant_lines) >= 3:
                        break
        
        return ' | '.join(relevant_lines[:3]) if relevant_lines else ""
    
    def classify_image_type(self, topic):
        """Classify the semantic type of the image"""
        topic_lower = topic.lower()
        
        if 'term' in topic_lower:
            return "terminal_output"
        elif 'plot' in topic_lower:
            return "xy_plot_display"
        elif 'scope_xy' in topic_lower:
            return "xy_oscilloscope"
        elif 'scope' in topic_lower:
            return "oscilloscope_display"
        elif 'fft' in topic_lower:
            return "spectrum_analyzer"
        elif 'logic' in topic_lower:
            return "logic_analyzer"
        elif 'bitmap' in topic_lower:
            return "bitmap_graphics"
        elif 'pc_key' in topic_lower:
            return "keyboard_input"
        elif 'pc_mouse' in topic_lower:
            return "mouse_input"
        else:
            return "debug_display"
    
    def generate_keywords(self, page_context, debug_context):
        """Generate search keywords for the image"""
        keywords = []
        
        # Add topic words
        if page_context.get("topic"):
            keywords.extend(page_context["topic"].lower().split())
        
        # Add display types
        keywords.extend([dt.lower() for dt in debug_context.get('display_types', [])])
        
        # Add DEBUG-specific terms
        keywords.extend(['debug', 'display', 'window', 'spin2'])
        
        # Remove duplicates and common words
        keywords = list(set(keywords))
        common_words = {'the', 'and', 'or', 'for', 'mode', 'display'}
        keywords = [k for k in keywords if k not in common_words]
        
        return keywords[:10]  # Top 10 keywords
    
    def enhance_all_images(self):
        """Enhance all images in the catalog"""
        print("Loading existing catalog...")
        catalog = self.load_existing_catalog()
        
        print("Loading narrative text...")
        narrative = self.load_narrative()
        
        print(f"Enhancing {len(catalog['images'])} images...")
        
        enhanced_images = []
        for i, image in enumerate(catalog['images'], 1):
            enhanced = self.enhance_image(image, narrative, i)
            enhanced_images.append(enhanced)
            print(f"  ✅ Enhanced {enhanced['global_id']} - {enhanced['enhanced_context']['topic']}")
        
        # Create enhanced catalog
        enhanced_catalog = {
            "metadata": {
                "source_pdf": catalog['source_pdf'],
                "document_id": self.doc_id,
                "extraction_date": catalog.get('extraction_summary', {}).get('extraction_date', '2025-08-24'),
                "enhancement_date": datetime.now().isoformat(),
                "total_images": len(enhanced_images),
                "extractor_version": "1.0-spin2",
                "enhancement_version": "2.0-docx-enriched"
            },
            "images": enhanced_images
        }
        
        # Save enhanced catalog
        output_path = self.assets_path / "spin2_v51_enhanced_catalog.json"
        with open(output_path, 'w') as f:
            json.dump(enhanced_catalog, f, indent=2)
        
        print(f"\n✅ Enhanced catalog saved to: {output_path}")
        print(f"📊 Total images enhanced: {len(enhanced_images)}")
        
        return enhanced_catalog

if __name__ == "__main__":
    enhancer = Spin2ImageEnhancer()
    enhanced_catalog = enhancer.enhance_all_images()
    
    # Show summary
    print("\n📋 Enhancement Summary:")
    print(f"  - Document ID: SPIN")
    print(f"  - Images Enhanced: {len(enhanced_catalog['images'])}")
    print(f"  - Context Source: Parallax Spin2 Documentation v51.docx")
    print(f"  - Global IDs: SPIN-IMG-001 through SPIN-IMG-{len(enhanced_catalog['images']):03d}")