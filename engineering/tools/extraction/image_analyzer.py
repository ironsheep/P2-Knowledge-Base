#!/usr/bin/env python3
"""
Image content analyzer for Smart Pins images.
Uses PIL to analyze image characteristics and improve classification.
"""

import os
import json
from PIL import Image
import numpy as np
from pathlib import Path
import re

class ImageContentAnalyzer:
    """Analyze image content to improve semantic classification."""
    
    def __init__(self, image_dir: str):
        """Initialize analyzer with image directory."""
        self.image_dir = image_dir
        self.images = {}
        
    def analyze_image(self, image_path: str) -> dict:
        """Analyze image characteristics without OCR."""
        img = Image.open(image_path)
        img_array = np.array(img)
        
        analysis = {
            "path": image_path,
            "filename": os.path.basename(image_path),
            "dimensions": img.size,
            "mode": img.mode,
            "characteristics": {}
        }
        
        # Analyze color distribution
        if len(img_array.shape) == 3:  # Color image
            # Check for specific colors that indicate diagram types
            unique_colors = len(np.unique(img_array.reshape(-1, img_array.shape[2]), axis=0))
            analysis["characteristics"]["unique_colors"] = unique_colors
            analysis["characteristics"]["is_monochrome"] = unique_colors < 10
            
            # Check for waveform patterns (repeating horizontal patterns)
            analysis["characteristics"]["has_grid"] = self._detect_grid_pattern(img_array)
            analysis["characteristics"]["has_waveform"] = self._detect_waveform_pattern(img_array)
        
        # Analyze aspect ratio
        width, height = img.size
        aspect_ratio = width / height if height > 0 else 1
        analysis["characteristics"]["aspect_ratio"] = aspect_ratio
        analysis["characteristics"]["is_wide"] = aspect_ratio > 2.5  # Timing diagrams are often wide
        analysis["characteristics"]["is_tall"] = aspect_ratio < 0.7  # State machines might be tall
        
        # Detect text regions (areas with high frequency changes)
        analysis["characteristics"]["text_density"] = self._estimate_text_density(img_array)
        
        # Classify based on characteristics
        analysis["improved_classification"] = self._classify_from_characteristics(analysis["characteristics"])
        
        return analysis
    
    def _detect_grid_pattern(self, img_array):
        """Detect if image has a grid pattern (common in timing diagrams)."""
        # Simple check: look for regular vertical/horizontal lines
        if len(img_array.shape) == 2:  # Grayscale
            gray = img_array
        else:
            # Convert to grayscale
            gray = np.mean(img_array, axis=2).astype(np.uint8)
        
        # Check for horizontal lines (common in timing diagrams)
        horizontal_variance = np.var(gray, axis=1)
        regular_horizontals = np.sum(horizontal_variance < 100) > gray.shape[0] * 0.1
        
        # Check for vertical lines (timing grid)
        vertical_variance = np.var(gray, axis=0)
        regular_verticals = np.sum(vertical_variance < 100) > gray.shape[1] * 0.1
        
        return regular_horizontals and regular_verticals
    
    def _detect_waveform_pattern(self, img_array):
        """Detect waveform-like patterns."""
        if len(img_array.shape) == 2:
            gray = img_array
        else:
            gray = np.mean(img_array, axis=2).astype(np.uint8)
        
        # Look for sharp transitions (edges) that indicate signal changes
        # Simple edge detection using differences
        horizontal_diffs = np.abs(np.diff(gray, axis=1))
        
        # Waveforms have regular vertical transitions
        edge_columns = np.sum(horizontal_diffs > 50, axis=0)
        
        # Check if we have periodic vertical edges
        has_regular_edges = np.sum(edge_columns > gray.shape[0] * 0.2) > 10
        
        return has_regular_edges
    
    def _estimate_text_density(self, img_array):
        """Estimate how much of the image is likely text."""
        if len(img_array.shape) == 2:
            gray = img_array
        else:
            gray = np.mean(img_array, axis=2).astype(np.uint8)
        
        # Text areas have high local variance
        # Calculate local variance using a sliding window
        window_size = 10
        local_vars = []
        
        for i in range(0, gray.shape[0] - window_size, window_size):
            for j in range(0, gray.shape[1] - window_size, window_size):
                window = gray[i:i+window_size, j:j+window_size]
                local_vars.append(np.var(window))
        
        # High variance regions likely contain text or detailed patterns
        high_var_ratio = np.sum(np.array(local_vars) > 500) / len(local_vars) if local_vars else 0
        
        return high_var_ratio
    
    def _classify_from_characteristics(self, chars):
        """Improved classification based on image characteristics."""
        # Scoring system for each type
        scores = {
            "timing_diagram": 0,
            "waveform": 0,
            "block_diagram": 0,
            "register_diagram": 0,
            "code_example": 0,
            "pin_diagram": 0,
            "schematic": 0
        }
        
        # Timing diagram indicators
        if chars.get("is_wide") and chars.get("has_grid"):
            scores["timing_diagram"] += 3
        if chars.get("has_waveform"):
            scores["timing_diagram"] += 2
            scores["waveform"] += 3
        
        # Code example indicators
        if chars.get("is_monochrome") and chars.get("text_density", 0) > 0.3:
            scores["code_example"] += 3
        if chars.get("aspect_ratio", 1) > 3 and chars.get("text_density", 0) > 0.2:
            scores["code_example"] += 2
        
        # Block diagram indicators
        if not chars.get("is_wide") and not chars.get("is_tall"):
            scores["block_diagram"] += 1
        if chars.get("unique_colors", 1000) < 50:  # Limited color palette
            scores["block_diagram"] += 1
        
        # Register diagram indicators
        if chars.get("has_grid") and not chars.get("has_waveform"):
            scores["register_diagram"] += 2
        
        # Return highest scoring type
        if max(scores.values()) == 0:
            return "diagram"  # Default
        
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def analyze_all_images(self):
        """Analyze all images in directory."""
        results = {}
        
        for img_file in Path(self.image_dir).glob("*.png"):
            print(f"Analyzing {img_file.name}...")
            results[img_file.name] = self.analyze_image(str(img_file))
        
        return results
    
    def create_correction_map(self, catalog_path: str):
        """Create a correction map for the existing catalog."""
        # Load existing catalog
        with open(catalog_path, 'r') as f:
            catalog = json.load(f)
        
        # Analyze all images
        analysis_results = self.analyze_all_images()
        
        # Create correction map
        corrections = []
        for img_meta in catalog.get("images", []):
            filename = img_meta["filename"]
            if filename in analysis_results:
                analysis = analysis_results[filename]
                
                old_type = img_meta["semantic_type"]
                new_type = analysis["improved_classification"]
                
                if old_type != new_type:
                    corrections.append({
                        "global_id": img_meta["global_id"],
                        "filename": filename,
                        "page": img_meta["page_number"],
                        "old_classification": old_type,
                        "new_classification": new_type,
                        "confidence_indicators": analysis["characteristics"]
                    })
        
        return corrections

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze Smart Pins images for better classification')
    parser.add_argument('--dir', default='engineering/ingestion/sources/smart-pins/assets/images-enhanced-20250901',
                      help='Image directory')
    parser.add_argument('--catalog', default='engineering/ingestion/sources/smart-pins/assets/images-enhanced-20250901/P2 SmartPins-220809_catalog.json',
                      help='Catalog JSON path')
    parser.add_argument('--show-chars', action='store_true',
                      help='Show detailed characteristics for each image')
    
    args = parser.parse_args()
    
    # Make paths absolute if needed
    if not args.dir.startswith('/'):
        base = '/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base'
        args.dir = os.path.join(base, args.dir)
        args.catalog = os.path.join(base, args.catalog)
    
    analyzer = ImageContentAnalyzer(args.dir)
    
    if args.show_chars:
        # Show detailed analysis
        results = analyzer.analyze_all_images()
        for filename, analysis in results.items():
            print(f"\n{'='*60}")
            print(f"Image: {filename}")
            print(f"Dimensions: {analysis['dimensions']}")
            print(f"Characteristics:")
            for key, value in analysis['characteristics'].items():
                print(f"  - {key}: {value}")
            print(f"Classification: {analysis['improved_classification']}")
    else:
        # Show corrections needed
        corrections = analyzer.create_correction_map(args.catalog)
        
        if corrections:
            print("\n🔧 Classification Corrections Needed:\n")
            for correction in corrections:
                print(f"Page {correction['page']} - {correction['global_id']}:")
                print(f"  Current: {correction['old_classification']}")
                print(f"  Better:  {correction['new_classification']}")
                
                # Show key indicators
                chars = correction['confidence_indicators']
                indicators = []
                if chars.get('is_wide'):
                    indicators.append("wide aspect")
                if chars.get('has_waveform'):
                    indicators.append("waveform pattern")
                if chars.get('text_density', 0) > 0.3:
                    indicators.append(f"high text ({chars['text_density']:.1%})")
                if chars.get('is_monochrome'):
                    indicators.append("monochrome")
                if chars.get('has_grid'):
                    indicators.append("grid pattern")
                
                if indicators:
                    print(f"  Because: {', '.join(indicators)}")
                print()
        else:
            print("✅ No corrections needed - classifications look good!")

if __name__ == "__main__":
    main()