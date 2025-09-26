# Quick Bytes Ingestion Plan
*Strategy for ingesting Parallax P2 Quick Bytes into knowledge base*

## Executive Summary

Quick Bytes are short tutorial videos with accompanying code that demonstrate P2 features and applications. Currently ~36 Quick Bytes exist across the Parallax website with potential discrepancies between main page and index.

## Discovery Findings

### Website Structure
- **Main Page**: https://www.parallax.com/propeller-2/quick-bytes/
  - Shows 12 initial entries with "Load More" pagination
  - JavaScript-based lazy loading
  
- **Index Page**: https://www.parallax.com/propeller-2/quick-bytes/p2-quick-bytes-index/
  - Page 1: 24 entries
  - Page 2: 12 entries  
  - Page 3: Empty (no results)
  - **Total from index**: ~36 Quick Bytes

- **YouTube Playlist**: https://youtube.com/playlist?list=PLt_MJJ1F_EXamgxASnod1rf2mpqT7z8f7
  - Centralized collection of Quick Bytes videos
  - Additional validation source for completeness
  - May contain videos not listed on website

### URL Patterns
- Individual Quick Byte: `https://www.parallax.com/[slug]/`
- Index pagination: `.../p2-quick-bytes-index/page/[N]/`
- Code downloads: `https://www.parallax.com/package/[slug]-example-code/`

### Content Structure
Each Quick Byte contains:
- Title and description
- YouTube video embed
- Source code downloads (ZIP) - **Can be multiple, or none for procedural guides**
- Bill of Materials (hardware list)
- Author and date
- **Tags** - Master taxonomy from index pages
- Programming languages used (Spin2, PASM2)
- Development tools referenced

### Master Tag Taxonomy
The index pages contain clickable tag links representing the complete categorization system:
- ADC / DAC
- Audio
- Development Tools
- Environmental
- Gaming
- Human Input
- IoT
- LCD
- LED
- Memory
- Motor Control
- Protocols
- Raspberry Pi
- Robotics
- RTC
- Sensors
- Smart Pins
- Utility
- VGA / HDMI
- Visual
- Wireless

## Data Schema Design

### YAML Structure
```yaml
quick_byte_metadata:
  quick_byte_id: "QB####"  # Sequential ID
  title: "P2 RTC Add-on Board Demo"
  slug: "p2-rtc-add-on-board-demo"
  author: "Mason Portell"
  date: "2023-01-26"
  
  urls:
    parallax_page: "https://www.parallax.com/p2-rtc-add-on-board-demo/"
    youtube_video: "https://youtube.com/watch?v=..."  # From individual video
    youtube_playlist: "https://youtube.com/playlist?list=PLt_MJJ1F_EXamgxASnod1rf2mpqT7z8f7"
    source_code_downloads:  # Can be multiple
      - url: "https://www.parallax.com/package/p2-rtc-demo-code/"
        description: "RTC Demo Code"
      - url: "https://www.parallax.com/package/p2-rtc-calibration-code/"
        description: "RTC Calibration Tool"
    
  tags:  # From master taxonomy
    - RTC
    - Sensors
    - Smart Pins
    
  quick_byte_type: "tutorial"  # or "procedural" for setup guides
  
  code_availability:
    has_code: true  # false for procedural guides
    download_count: 2  # Number of separate downloads
    code_type: "downloadable"  # or "none", "inline_only"
    note: "Multiple code downloads available (2 files)"  # Descriptive note
    
  hardware:
    - part: "P2 RTC Add-on Board"
      parallax_id: "64025"
    - part: "P2 Edge Module"
      parallax_id: "P2-EC"
      
  programming:
    languages:
      - Spin2
      - PASM2
    tools:
      - "Propeller Tool"
      - "FlexProp"
      
  content:
    description: "This Quick Byte shows how to use..."
    duration: "8m 3s"
    key_concepts:
      - "RTC calibration"
      - "Battery backup"
      - "Date/time setting"
      
  relationships:
    obex_objects: []  # Cross-reference to OBEX if applicable
    related_quickbytes: []
    documentation_refs: []
    
  metadata:
    ingestion_date: "2025-09-26"
    last_verified: "2025-09-26"
    status: "complete"
```

## Directory Structure
```
engineering/knowledge-base/P2/community/quick-bytes/
├── objects/
│   ├── QB0001.yaml  # Individual Quick Byte files
│   ├── QB0002.yaml
│   └── ...
├── manifests/
│   ├── quick-bytes-root.yaml      # Main index
│   ├── tags/                      # Tag-based indexes
│   │   ├── sensors.yaml           
│   │   ├── smart-pins.yaml
│   │   ├── protocols.yaml
│   │   └── ...                    # One per master tag
│   └── authors/
│       ├── mason-portell.yaml     # Author indexes
│       └── ...
├── source-code/
│   ├── QB0001/                     # Extracted source code
│   │   ├── main.spin2
│   │   └── README.md
│   └── ...
└── tags-taxonomy.yaml              # Master tag definitions
```

## Ingestion Process

### Phase 1: Discovery & Validation
1. **Extract master tag taxonomy** from index page links
2. **Scrape index pages** (page 1 & 2)
3. **Scrape main page** with Load More iterations (if needed)
4. **Extract YouTube playlist** video titles and IDs
5. **Cross-validate** all three sources to identify:
   - Items only in index
   - Items only in main page  
   - Complete canonical list
4. **Generate discrepancy report**

### Phase 2: Content Extraction
1. **For each Quick Byte URL**:
   - Fetch page content
   - Extract all metadata fields
   - Download source code ZIP
   - Extract YouTube video ID
   - Capture hardware BOM
   
2. **Process source code downloads**:
   - Handle multiple downloads per Quick Byte
   - Unzip each to temporary location
   - Analyze file structure
   - Extract main Spin2/PASM2 files
   - Preserve in source-code/QB####/ subdirectories

### Phase 3: Enrichment
1. **Cross-reference with OBEX**:
   - Match hardware components
   - Link related drivers
   - Identify duplicate functionality
   
2. **Category mapping**:
   - Normalize category names
   - Create category hierarchies
   - Build reverse indexes

### Phase 4: Integration
1. **Create manifests**:
   - Root manifest with all Quick Bytes
   - Category manifests
   - Author manifests
   
2. **Update main P2 knowledge base**:
   - Add to p2-knowledge-root.yaml
   - Create quick-bytes-manifest.yaml
   - Update auxiliary guides

## Implementation Tools

### Scraper Script
```python
# engineering/tools/quick-bytes-integration/scrape-quick-bytes.py

import requests
from bs4 import BeautifulSoup
import yaml
import time
from pathlib import Path

class QuickBytesScraper:
    def scrape_index_page(self, page_num):
        """Scrape index page for Quick Bytes list"""
        
    def scrape_individual_page(self, url):
        """Extract all data from a Quick Byte page"""
        
    def download_source_code(self, download_url, output_dir):
        """Download and extract source code ZIP"""
        
    def generate_yaml(self, data, output_path):
        """Create YAML file for Quick Byte"""
```

## Quality Assurance

### Validation Checks
- [ ] All Quick Bytes discovered (no orphans)
- [ ] YouTube URLs valid
- [ ] Source code downloads successful
- [ ] Hardware parts cross-referenced
- [ ] No duplicate IDs
- [ ] Categories normalized
- [ ] Dates properly formatted

### Metrics to Track
- Total Quick Bytes ingested
- Source code packages downloaded
- YouTube videos cataloged  
- Hardware components referenced
- OBEX cross-references created
- Categories utilized

## Timeline

### Week 1
- Day 1-2: Build and test scraper
- Day 3-4: Complete discovery phase
- Day 5: Validation and discrepancy resolution

### Week 2  
- Day 1-3: Content extraction
- Day 4: Source code processing
- Day 5: Enrichment and cross-referencing

### Week 3
- Day 1-2: Manifest generation
- Day 3: Integration testing
- Day 4-5: Documentation and cleanup

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Website structure changes | Version scraper, maintain fallbacks |
| Missing source code | Flag and track, manual recovery |
| Video unavailability | Store video IDs, note removal |
| Pagination inconsistencies | Cross-validate multiple sources |
| YouTube playlist access | Use API or manual extraction if needed |

## Success Criteria

1. **Complete coverage**: All Quick Bytes cataloged
2. **Rich metadata**: All fields populated
3. **Source code preserved**: Local copies available
4. **Cross-referenced**: OBEX and hardware linked
5. **AI-discoverable**: Integrated into manifest system

## Next Steps

1. Review and approve plan
2. Create scraper script
3. Run discovery phase
4. Begin ingestion

---

*This plan ensures comprehensive capture of Quick Bytes content while maintaining consistency with existing P2 Knowledge Base structure.*