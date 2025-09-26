#!/usr/bin/env python3
"""
Correlate YouTube playlist videos with actual Quick Bytes.
Filters out non-Quick Byte content and matches videos to website entries.
"""

import re
from datetime import datetime
from typing import Dict, List, Tuple

class YouTubeQuickBytesCorrelator:
    def __init__(self):
        self.quick_byte_patterns = [
            r'P2\s+Quick\s+Byte[s]?[\s:-]',
            r'Quick\s+Byte[s]?[\s:-]',
            r'QB[\s:-]',
            r'QuickByte[\s:-]'
        ]
        
        self.non_quick_byte_indicators = [
            'Live Forum',
            'Early Adopter',
            'Webinar',
            'Tutorial Series',
            'Full Course',
            'Introduction to Propeller',
            'Getting Started Guide',
            'Overview',
            'Announcement'
        ]
        
        self.stats = {
            'total_playlist_videos': 0,
            'identified_quick_bytes': 0,
            'non_quick_bytes': 0,
            'uncertain': 0
        }
    
    def is_quick_byte(self, video_title: str, video_description: str = '') -> Tuple[bool, float, str]:
        """
        Determine if a video is a Quick Byte.
        Returns: (is_quick_byte, confidence, reason)
        """
        title_lower = video_title.lower()
        
        # Check for explicit Quick Byte patterns
        for pattern in self.quick_byte_patterns:
            if re.search(pattern, video_title, re.IGNORECASE):
                return True, 0.95, "Title contains Quick Byte pattern"
        
        # Check for non-Quick Byte indicators
        for indicator in self.non_quick_byte_indicators:
            if indicator.lower() in title_lower:
                return False, 0.90, f"Title contains non-QB indicator: {indicator}"
        
        # Heuristic checks for Quick Byte characteristics
        confidence = 0.5  # Start neutral
        reasons = []
        
        # Quick Bytes tend to be focused on single topics
        if any(word in title_lower for word in ['demo', 'example', 'how to', 'using', 'with']):
            confidence += 0.2
            reasons.append("Contains demo/tutorial keywords")
        
        # Check for hardware/module mentions (common in Quick Bytes)
        hardware_keywords = ['sensor', 'module', 'board', 'display', 'motor', 'led', 
                           'gps', 'rtc', 'i2c', 'spi', 'uart', 'adc', 'dac']
        if any(hw in title_lower for hw in hardware_keywords):
            confidence += 0.15
            reasons.append("Contains hardware keywords")
        
        # Check for P2/Propeller 2 mention
        if 'p2' in title_lower or 'propeller 2' in title_lower:
            confidence += 0.1
            reasons.append("Mentions P2/Propeller 2")
        
        # Length check - Quick Bytes titles tend to be concise
        if len(video_title) < 60:
            confidence += 0.05
            reasons.append("Concise title")
        elif len(video_title) > 100:
            confidence -= 0.1
            reasons.append("Very long title")
        
        # Determine based on confidence
        is_qb = confidence >= 0.65
        reason = "; ".join(reasons) if reasons else "No specific indicators"
        
        return is_qb, confidence, reason
    
    def extract_quick_byte_topic(self, video_title: str) -> str:
        """
        Extract the main topic from a Quick Byte video title.
        Removes prefixes like "P2 Quick Byte:" or "Quick Byte -"
        """
        # Remove common prefixes
        cleaned = video_title
        patterns_to_remove = [
            r'^P2\s+Quick\s+Byte[s]?\s*[-:]\s*',
            r'^Quick\s+Byte[s]?\s*[-:]\s*',
            r'^QB\s*[-:]\s*',
            r'^QuickByte\s*[-:]\s*'
        ]
        
        for pattern in patterns_to_remove:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        return cleaned.strip()
    
    def correlate_with_website(self, youtube_videos: List[Dict], website_entries: List[Dict]) -> Dict:
        """
        Correlate YouTube videos with website Quick Bytes entries.
        
        Args:
            youtube_videos: List of dicts with 'title', 'video_id', 'description'
            website_entries: List of dicts with 'title', 'url', 'date'
        
        Returns:
            Correlation results with matches, unmatched, and statistics
        """
        correlations = {
            'matched': [],
            'youtube_only': [],
            'website_only': list(website_entries),  # Start with all, remove matches
            'non_quick_bytes': []
        }
        
        for video in youtube_videos:
            self.stats['total_playlist_videos'] += 1
            
            # Check if it's a Quick Byte
            is_qb, confidence, reason = self.is_quick_byte(video['title'])
            
            if not is_qb:
                self.stats['non_quick_bytes'] += 1
                correlations['non_quick_bytes'].append({
                    'video': video,
                    'confidence': confidence,
                    'reason': reason
                })
                continue
            
            self.stats['identified_quick_bytes'] += 1
            
            # Extract topic for matching
            video_topic = self.extract_quick_byte_topic(video['title'])
            
            # Try to match with website entries
            best_match = None
            best_score = 0
            
            for web_entry in website_entries:
                score = self.calculate_match_score(video_topic, web_entry.get('title', ''))
                if score > best_score:
                    best_score = score
                    best_match = web_entry
            
            if best_match and best_score > 0.7:
                correlations['matched'].append({
                    'youtube': video,
                    'website': best_match,
                    'match_score': best_score,
                    'topic': video_topic
                })
                # Remove from website_only list
                if best_match in correlations['website_only']:
                    correlations['website_only'].remove(best_match)
            else:
                correlations['youtube_only'].append({
                    'video': video,
                    'topic': video_topic,
                    'confidence': confidence
                })
        
        return correlations
    
    def calculate_match_score(self, title1: str, title2: str) -> float:
        """
        Calculate similarity score between two titles.
        """
        # Simple word-based matching
        words1 = set(title1.lower().split())
        words2 = set(title2.lower().split())
        
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                      'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was'}
        words1 -= stop_words
        words2 -= stop_words
        
        if not words1 or not words2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = words1 & words2
        union = words1 | words2
        
        if not union:
            return 0.0
            
        return len(intersection) / len(union)
    
    def generate_correlation_report(self, correlations: Dict) -> str:
        """
        Generate a human-readable correlation report.
        """
        report = []
        report.append("=" * 60)
        report.append("YOUTUBE PLAYLIST - QUICK BYTES CORRELATION REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Statistics
        report.append("STATISTICS:")
        report.append(f"Total playlist videos: {self.stats['total_playlist_videos']}")
        report.append(f"Identified Quick Bytes: {self.stats['identified_quick_bytes']}")
        report.append(f"Non-Quick Byte videos: {self.stats['non_quick_bytes']}")
        report.append("")
        
        # Matched entries
        report.append(f"MATCHED ENTRIES: {len(correlations['matched'])}")
        report.append("-" * 40)
        for match in correlations['matched'][:5]:  # Show first 5
            report.append(f"YouTube: {match['youtube']['title']}")
            report.append(f"Website: {match['website']['title']}")
            report.append(f"Match Score: {match['match_score']:.2f}")
            report.append("")
        
        if len(correlations['matched']) > 5:
            report.append(f"... and {len(correlations['matched']) - 5} more matches")
            report.append("")
        
        # YouTube-only Quick Bytes
        report.append(f"YOUTUBE-ONLY QUICK BYTES: {len(correlations['youtube_only'])}")
        report.append("-" * 40)
        for item in correlations['youtube_only'][:5]:
            report.append(f"Title: {item['video']['title']}")
            report.append(f"Topic: {item['topic']}")
            report.append(f"Confidence: {item['confidence']:.2f}")
            report.append("")
        
        # Website-only entries
        report.append(f"WEBSITE-ONLY ENTRIES: {len(correlations['website_only'])}")
        report.append("-" * 40)
        for item in correlations['website_only'][:5]:
            report.append(f"Title: {item.get('title', 'Unknown')}")
            report.append("")
        
        # Non-Quick Byte videos filtered out
        report.append(f"FILTERED OUT (NON-QUICK BYTES): {len(correlations['non_quick_bytes'])}")
        report.append("-" * 40)
        for item in correlations['non_quick_bytes'][:5]:
            report.append(f"Title: {item['video']['title']}")
            report.append(f"Reason: {item['reason']}")
            report.append("")
        
        return "\n".join(report)


def main():
    """
    Example usage of the correlator.
    """
    correlator = YouTubeQuickBytesCorrelator()
    
    # Example YouTube videos (would come from playlist)
    youtube_videos = [
        {"title": "P2 Quick Byte: RTC Module Demo", "video_id": "abc123"},
        {"title": "Quick Byte - Using GPS with P2", "video_id": "def456"},
        {"title": "Propeller 2 Live Forum #123", "video_id": "ghi789"},  # Not a QB
        {"title": "P2 Early Adopter Series", "video_id": "jkl012"},  # Not a QB
        {"title": "1-Wire Temperature Sensor Demo", "video_id": "mno345"},  # Might be QB
    ]
    
    # Example website entries (would come from scraper)
    website_entries = [
        {"title": "P2 RTC Add-on Board Demo", "url": "/p2-rtc-add-on-board-demo/"},
        {"title": "NMEA GPS String Parsing", "url": "/nmea-gps-string-parsing/"},
        {"title": "1-Wire Driver with DS18B20 Temperature Sensor Demo", "url": "/1-wire-driver/"},
    ]
    
    # Test individual classification
    print("CLASSIFICATION TESTS:")
    print("-" * 40)
    for video in youtube_videos:
        is_qb, confidence, reason = correlator.is_quick_byte(video['title'])
        status = "✅ Quick Byte" if is_qb else "❌ Not QB"
        print(f"{status} ({confidence:.2f}): {video['title']}")
        print(f"  Reason: {reason}")
        print()
    
    # Run correlation
    print("\nRUNNING CORRELATION...")
    correlations = correlator.correlate_with_website(youtube_videos, website_entries)
    
    # Generate report
    report = correlator.generate_correlation_report(correlations)
    print(report)


if __name__ == "__main__":
    main()