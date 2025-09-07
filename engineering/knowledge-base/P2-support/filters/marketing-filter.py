#!/usr/bin/env python3
"""
P2 Knowledge Base Marketing Filter System
Identifies and removes marketing content, subjective claims, and non-technical material
Version: 1.0.0
"""

import re
import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

class MarketingFilter:
    """Filters marketing content from technical documentation"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.filter_log = []
        self.review_queue = []
        self.filtered_content = []
        
        # Initialize sentiment analyzer for subjective claim detection
        try:
            self.sia = SentimentIntensityAnalyzer()
        except:
            print("Warning: NLTK sentiment analyzer not available")
            self.sia = None
            
        # Marketing phrase patterns
        self.marketing_phrases = [
            # Superlatives
            r'\b(revolutionary|game.?changing|breakthrough|cutting.?edge)\b',
            r'\b(industry.?leading|world.?class|best.?in.?class)\b',
            r'\b(unprecedented|unmatched|unparalleled|unique)\b',
            
            # Comparison marketing
            r'\b(better than|superior to|outperforms|beats)\b',
            r'\b(unlike other|compared to other|versus other)\b',
            r'\b(competitive advantage|market leader)\b',
            
            # Subjective claims
            r'\b(amazing|incredible|fantastic|excellent)\b',
            r'\b(powerful|robust|comprehensive|advanced)\b',
            r'\b(easy|simple|intuitive|user.?friendly)\b',
            
            # Sales language
            r'\b(perfect for|ideal for|designed for)\b',
            r'\b(customers|users|developers) will (love|appreciate)\b',
            r'\b(save time|save money|increase productivity)\b'
        ]
        
        # Technical comparison whitelist (legitimate comparisons)
        self.technical_whitelist = [
            r'\d+\s*(times|x)\s*(faster|slower|larger|smaller)',  # "2x faster"
            r'\d+\s*(cycles|clocks|ticks)\s*(vs|versus|compared)',  # "8 cycles vs 16"
            r'\d+\s*(KB|MB|GB|bytes)\s*(vs|versus|compared)',  # "512KB vs 256KB"
            r'\d+\s*(MHz|GHz|Hz)\s*(vs|versus|compared)',  # "200MHz vs 100MHz"
            r'\d+\s*(bits?|bytes?)\s*(wide|width)',  # "32-bit wide"
            r'(higher|lower|more|less|fewer)\s*(latency|throughput|bandwidth)',
            r'(pin|port|register|instruction)\s*compatible'
        ]
        
        # Educational comparison whitelist
        self.educational_whitelist = [
            r'similar to|like|resembles|equivalent',  # Educational analogies
            r'differs from|different from|unlike',  # Educational contrasts
            r'compared to|in contrast to|whereas',  # Educational comparisons
            r'traditionally|historically|previously',  # Historical context
            r'for example|such as|including'  # Examples
        ]
        
    def is_marketing_phrase(self, text: str) -> List[Dict]:
        """Detect marketing phrases in text"""
        detected = []
        text_lower = text.lower()
        
        for pattern in self.marketing_phrases:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                # Check if it's whitelisted
                if not self.is_whitelisted(text, match.start(), match.end()):
                    detected.append({
                        'type': 'marketing_phrase',
                        'pattern': pattern,
                        'match': match.group(),
                        'position': (match.start(), match.end()),
                        'context': text[max(0, match.start()-20):min(len(text), match.end()+20)]
                    })
                    
        return detected
        
    def is_whitelisted(self, text: str, start: int, end: int) -> bool:
        """Check if a match is whitelisted as technical or educational"""
        # Get surrounding context
        context_start = max(0, start - 50)
        context_end = min(len(text), end + 50)
        context = text[context_start:context_end]
        
        # Check technical whitelist
        for pattern in self.technical_whitelist:
            if re.search(pattern, context, re.IGNORECASE):
                return True
                
        # Check educational whitelist
        for pattern in self.educational_whitelist:
            if re.search(pattern, context, re.IGNORECASE):
                return True
                
        return False
        
    def detect_subjective_claims(self, text: str) -> List[Dict]:
        """Detect subjective claims without technical backing"""
        detected = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            # Check for subjective indicators
            subjective_score = self.calculate_subjectivity(sentence)
            
            if subjective_score > 0.6:  # High subjectivity threshold
                # Check if it has technical backing
                if not self.has_technical_backing(sentence):
                    detected.append({
                        'type': 'subjective_claim',
                        'text': sentence.strip(),
                        'subjectivity_score': subjective_score,
                        'needs_review': subjective_score < 0.8  # Borderline cases
                    })
                    
        return detected
        
    def calculate_subjectivity(self, text: str) -> float:
        """Calculate subjectivity score for text"""
        if self.sia:
            scores = self.sia.polarity_scores(text)
            # Higher compound score indicates more subjective/emotional content
            return abs(scores['compound'])
        else:
            # Fallback: count subjective words
            subjective_words = [
                'amazing', 'excellent', 'powerful', 'robust', 'advanced',
                'easy', 'simple', 'intuitive', 'best', 'superior'
            ]
            word_count = len(text.split())
            subjective_count = sum(1 for word in subjective_words if word in text.lower())
            return subjective_count / max(word_count, 1)
            
    def has_technical_backing(self, text: str) -> bool:
        """Check if a claim has technical backing"""
        technical_indicators = [
            r'\d+\s*(cycles|clocks|MHz|GHz|KB|MB|bits?|bytes?)',  # Numbers with units
            r'0x[0-9A-Fa-f]+',  # Hex values
            r'\$[0-9A-Fa-f]+',  # Hex with $ prefix
            r'%[01]+',  # Binary values
            r'\b(register|instruction|opcode|encoding|timing)\b',  # Technical terms
            r'\b(latency|throughput|bandwidth|frequency)\b',  # Performance terms
            r'\b(specification|requirement|constraint)\b'  # Formal terms
        ]
        
        for pattern in technical_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                return True
                
        return False
        
    def detect_competitor_comparisons(self, text: str) -> List[Dict]:
        """Detect competitor comparisons and product mentions"""
        detected = []
        
        # Known competitor patterns
        competitor_patterns = [
            r'\b(ARM|Intel|AMD|RISC-?V|Arduino|Raspberry)\b',
            r'\b(Cortex|x86|AVR|PIC|ESP32|STM32)\b',
            r'\b(competing|competitor|alternative|other)\s+(processor|chip|solution)',
            r'\b(versus|vs\.?|compared to)\s+\w+\s+(processor|chip|MCU|CPU)'
        ]
        
        for pattern in competitor_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Check if it's educational context
                if not self.is_educational_comparison(text, match):
                    detected.append({
                        'type': 'competitor_comparison',
                        'pattern': pattern,
                        'match': match.group(),
                        'context': text[max(0, match.start()-30):min(len(text), match.end()+30)]
                    })
                    
        return detected
        
    def is_educational_comparison(self, text: str, match) -> bool:
        """Check if a comparison is educational rather than marketing"""
        context_start = max(0, match.start() - 100)
        context_end = min(len(text), match.end() + 100)
        context = text[context_start:context_end]
        
        educational_indicators = [
            'architecture', 'design', 'approach', 'method',
            'technique', 'implementation', 'concept', 'principle',
            'example', 'illustration', 'demonstration'
        ]
        
        return any(indicator in context.lower() for indicator in educational_indicators)
        
    def detect_historical_narratives(self, text: str) -> List[Dict]:
        """Detect historical narratives not relevant to technical implementation"""
        detected = []
        
        historical_patterns = [
            r'(in|since|back in)\s+\d{4}',  # Year references
            r'(originally|initially|first)\s+(developed|designed|created)',
            r'(history|evolution|development)\s+of',
            r'(founder|inventor|creator|company)\s+(story|journey)',
            r'(started|began|founded)\s+(in|when|after)'
        ]
        
        for pattern in historical_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Check if it's relevant technical history
                if not self.is_technical_history(text, match):
                    detected.append({
                        'type': 'historical_narrative',
                        'pattern': pattern,
                        'match': match.group(),
                        'relevance': 'low'
                    })
                    
        return detected
        
    def is_technical_history(self, text: str, match) -> bool:
        """Check if historical content is technically relevant"""
        context = text[max(0, match.start()-50):min(len(text), match.end()+50)]
        
        technical_relevance = [
            'version', 'revision', 'update', 'release',
            'specification', 'standard', 'protocol',
            'backward compatible', 'legacy', 'deprecated'
        ]
        
        return any(term in context.lower() for term in technical_relevance)
        
    def filter_entry(self, entry_path: Path) -> Dict:
        """Filter marketing content from a single entry"""
        results = {
            'path': str(entry_path),
            'filtered': False,
            'detections': [],
            'review_items': []
        }
        
        try:
            with open(entry_path, 'r') as f:
                data = yaml.safe_load(f)
                
            if not data:
                return results
                
            # Check main text fields
            text_fields = ['description', 'usage_notes', 'operation']
            
            for field in text_fields:
                if field in data and isinstance(data[field], str):
                    text = data[field]
                    
                    # Run all detectors
                    detections = []
                    detections.extend(self.is_marketing_phrase(text))
                    detections.extend(self.detect_subjective_claims(text))
                    detections.extend(self.detect_competitor_comparisons(text))
                    detections.extend(self.detect_historical_narratives(text))
                    
                    if detections:
                        results['filtered'] = True
                        results['detections'].extend([
                            {**d, 'field': field} for d in detections
                        ])
                        
                        # Clean the text
                        cleaned_text = self.clean_text(text, detections)
                        if cleaned_text != text:
                            # Store original for rollback
                            self.filtered_content.append({
                                'entry': str(entry_path),
                                'field': field,
                                'original': text,
                                'cleaned': cleaned_text,
                                'timestamp': datetime.now().isoformat()
                            })
                            
                            # Update the entry
                            data[field] = cleaned_text
                            
            # Check examples
            if 'examples' in data and isinstance(data['examples'], list):
                for i, example in enumerate(data['examples']):
                    if 'explanation' in example:
                        text = example['explanation']
                        detections = self.is_marketing_phrase(text)
                        
                        if detections:
                            results['filtered'] = True
                            results['detections'].extend([
                                {**d, 'field': f'examples[{i}].explanation'} 
                                for d in detections
                            ])
                            
            # Add borderline cases to review queue
            for detection in results['detections']:
                if detection.get('needs_review'):
                    results['review_items'].append(detection)
                    self.review_queue.append({
                        'entry': str(entry_path),
                        'detection': detection,
                        'timestamp': datetime.now().isoformat()
                    })
                    
            # Save filtered entry if modified
            if results['filtered']:
                with open(entry_path, 'w') as f:
                    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
                    
        except Exception as e:
            results['error'] = str(e)
            
        return results
        
    def clean_text(self, text: str, detections: List[Dict]) -> str:
        """Remove detected marketing content from text"""
        # Sort detections by position (reverse order to maintain positions)
        position_detections = [d for d in detections if 'position' in d]
        position_detections.sort(key=lambda x: x['position'][0], reverse=True)
        
        cleaned = text
        for detection in position_detections:
            start, end = detection['position']
            # Replace with ellipsis or remove entirely
            if end - start > 20:
                cleaned = cleaned[:start] + '[removed]' + cleaned[end:]
            else:
                cleaned = cleaned[:start] + cleaned[end:]
                
        # Clean up multiple spaces and empty sentences
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = re.sub(r'\.\s*\.', '.', cleaned)
        cleaned = cleaned.strip()
        
        return cleaned
        
    def filter_repository(self) -> Dict:
        """Filter entire repository"""
        results = {
            'total_entries': 0,
            'filtered_entries': 0,
            'total_detections': 0,
            'review_queue_size': 0,
            'by_type': defaultdict(int)
        }
        
        patterns = [
            "instructions/**/*.yaml",
            "components/**/*.yaml",
            "architecture/*.yaml"
        ]
        
        for pattern in patterns:
            for entry_path in self.repo_path.glob(pattern):
                results['total_entries'] += 1
                
                entry_results = self.filter_entry(entry_path)
                
                if entry_results['filtered']:
                    results['filtered_entries'] += 1
                    
                for detection in entry_results.get('detections', []):
                    results['total_detections'] += 1
                    results['by_type'][detection['type']] += 1
                    
                # Log the filtering
                if entry_results['filtered']:
                    self.filter_log.append({
                        'entry': str(entry_path),
                        'detections': len(entry_results['detections']),
                        'types': list(set(d['type'] for d in entry_results['detections'])),
                        'timestamp': datetime.now().isoformat()
                    })
                    
        results['review_queue_size'] = len(self.review_queue)
        
        return results
        
    def generate_filter_report(self, results: Dict) -> str:
        """Generate filtering report"""
        report = f"""# Marketing Filter Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total Entries Processed**: {results['total_entries']}
- **Entries Filtered**: {results['filtered_entries']}
- **Total Detections**: {results['total_detections']}
- **Items for Review**: {results['review_queue_size']}

## Detections by Type
"""
        
        for detection_type, count in results['by_type'].items():
            report += f"- **{detection_type.replace('_', ' ').title()}**: {count}\n"
            
        # Add filtered content log
        if self.filter_log:
            report += "\n## Filtered Entries (First 20)\n"
            for log_entry in self.filter_log[:20]:
                report += f"- `{Path(log_entry['entry']).name}`: "
                report += f"{log_entry['detections']} detections "
                report += f"({', '.join(log_entry['types'])})\n"
                
        # Add review queue
        if self.review_queue:
            report += f"\n## Review Queue ({len(self.review_queue)} items)\n"
            report += "Items requiring human judgment:\n\n"
            
            for item in self.review_queue[:10]:
                report += f"### {Path(item['entry']).name}\n"
                detection = item['detection']
                report += f"- Type: {detection['type']}\n"
                report += f"- Text: {detection.get('text', detection.get('match', ''))[:100]}...\n"
                if 'subjectivity_score' in detection:
                    report += f"- Score: {detection['subjectivity_score']:.2f}\n"
                report += "\n"
                
        # Add filtering guidelines
        report += """
## Filtering Guidelines

### Removed Content Types
1. **Marketing Phrases**: Superlatives, competitive claims, sales language
2. **Subjective Claims**: Opinions without technical backing
3. **Competitor Comparisons**: Non-educational product comparisons
4. **Historical Narratives**: Non-technical company/product history

### Preserved Content Types
1. **Technical Comparisons**: Specific metrics (cycles, memory, speed)
2. **Educational Comparisons**: Explanatory analogies and contrasts
3. **Technical History**: Version history, deprecation notes
4. **Objective Descriptions**: Fact-based technical content

## Actions Required
"""
        
        if results['review_queue_size'] > 0:
            report += f"1. Review {results['review_queue_size']} borderline cases in review queue\n"
            
        if results['filtered_entries'] > 0:
            report += f"2. Verify {results['filtered_entries']} filtered entries for accuracy\n"
            
        report += "3. Update extraction pipeline to prevent marketing content\n"
        
        return report
        
    def save_filter_logs(self) -> None:
        """Save all filter logs and queues"""
        log_dir = self.repo_path / "update-tracking" / "filter-logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save filter log
        if self.filter_log:
            log_file = log_dir / f"filter-log-{timestamp}.yaml"
            with open(log_file, 'w') as f:
                yaml.dump(self.filter_log, f, default_flow_style=False)
                
        # Save review queue
        if self.review_queue:
            queue_file = log_dir / f"review-queue-{timestamp}.yaml"
            with open(queue_file, 'w') as f:
                yaml.dump(self.review_queue, f, default_flow_style=False)
                
        # Save filtered content for rollback
        if self.filtered_content:
            content_file = log_dir / f"filtered-content-{timestamp}.yaml"
            with open(content_file, 'w') as f:
                yaml.dump(self.filtered_content, f, default_flow_style=False)
                

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="P2 Knowledge Base Marketing Filter")
    parser.add_argument('--repo-path', default='.', help='Repository root path')
    parser.add_argument('--dry-run', action='store_true', help='Analyze without modifying files')
    parser.add_argument('--entry', help='Filter single entry')
    
    args = parser.parse_args()
    
    filter_system = MarketingFilter(args.repo_path)
    
    if args.entry:
        # Filter single entry
        results = filter_system.filter_entry(Path(args.entry))
        print(f"Filtered: {results['filtered']}")
        print(f"Detections: {len(results['detections'])}")
    else:
        # Filter entire repository
        print("🔍 Running marketing content filter...")
        results = filter_system.filter_repository()
        
        # Generate report
        report = filter_system.generate_filter_report(results)
        
        # Save report
        report_file = Path(args.repo_path) / "update-tracking" / "reports" / \
                     f"filter-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            f.write(report)
            
        print(f"\n📄 Report saved: {report_file.name}")
        
        # Save logs
        filter_system.save_filter_logs()
        
        # Print summary
        print("\n📊 Filter Summary:")
        print(f"  Entries processed: {results['total_entries']}")
        print(f"  Entries filtered: {results['filtered_entries']}")
        print(f"  Total detections: {results['total_detections']}")
        print(f"  Review queue: {results['review_queue_size']} items")