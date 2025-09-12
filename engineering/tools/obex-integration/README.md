# OBEX Integration Tools

Tools for discovering, cataloging, and analyzing P2 objects from the Parallax Object Exchange (OBEX).

## Quick Start

```bash
# Run complete discovery (recommended)
./discover_obex.sh

# Custom discovery options
./discover_obex.sh --categories spin2 --delay 2.0
```

## Files

### Core Tools
- **`obex_discovery.py`** - Main discovery engine (Python)
- **`discover_obex.sh`** - Shell wrapper script
- **`README.md`** - This documentation

### Output Structure
Generated files will be created in `engineering/knowledge-base/external-resources/obex/`:
- **`master-index.yaml`** - Complete catalog of all P2 objects
- **`objects/XXXX.yaml`** - Individual object metadata files
- **`authors/username.yaml`** - Author profile aggregations

## Dependencies

Required Python packages:
```bash
pip3 install requests beautifulsoup4 pyyaml
```

## Usage Examples

### Basic Discovery
```bash
# Discover all P2 objects from SPIN2 and PASM categories
./discover_obex.sh
```

### Category-Specific Discovery
```bash
# Only SPIN2 objects
./discover_obex.sh --categories spin2

# Only PASM objects  
./discover_obex.sh --categories pasm
```

### Respectful Crawling
```bash
# Slower crawling (2 second delays)
./discover_obex.sh --delay 2.0
```

### Advanced Python Usage
```python
from obex_discovery import OBEXDiscovery

# Initialize discovery engine
discovery = OBEXDiscovery()
discovery.request_delay = 1.5  # Custom delay

# Run discovery
result = discovery.run_discovery(['spin2'])
print(f"Found {result['objects_found']} objects")

# Access individual object data
objects = discovery.discover_category_objects('spin2')
for obj in objects:
    detailed = discovery.extract_detailed_metadata(obj)
    print(f"Object: {detailed['title']} by {detailed['author']}")
```

## Output Format

### Master Index Structure
```yaml
metadata:
  generated_date: "2025-09-11"
  total_objects: 42
  schema_version: "1.0"

objects:
  - object_id: "2842"
    title: "Full Duplex Serial Driver"
    author: "Jon McPhalen (jonnymac)"
    url: "https://obex.parallax.com/obex/full-duplex-serial-2/"
    download_url: "https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB2842"
    languages: ["SPIN2", "PASM2"]
    category: "drivers"
    tags: ["serial", "driver", "communication"]

indices:
  by_author:
    "Jon McPhalen (jonnymac)": ["2842", "2850"]
  by_category:
    "drivers": ["2842", "2850"]
```

### Individual Object Format
```yaml
object_metadata:
  object_id: "2842"
  title: "Full Duplex Serial Driver"
  author: "Jon McPhalen (jonnymac)"
  
  urls:
    obex_page: "https://obex.parallax.com/obex/full-duplex-serial-2/"
    download_direct: "https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB2842"
    
  technical_details:
    languages: ["SPIN2", "PASM2"]
    microcontroller: ["P2"]
    
  functionality:
    category: "drivers"
    description_full: "High-performance serial communication driver"
    tags: ["serial", "driver", "communication"]
```

## Features

### Discovery Capabilities
- **Category Crawling**: Process all pages in SPIN2/PASM categories
- **Pagination Handling**: Automatically process multi-page results  
- **Metadata Extraction**: Extract titles, authors, descriptions, Object IDs
- **Download URL Generation**: Construct direct download URLs using Object IDs
- **Rate Limiting**: Respectful crawling with configurable delays

### Data Processing  
- **Automatic Categorization**: Classify objects by functionality
- **Tag Generation**: Generate relevant tags from titles/descriptions
- **Language Detection**: Identify SPIN2/PASM2 usage
- **Author Aggregation**: Group objects by author

### Quality Features
- **Error Handling**: Graceful failure with detailed error reporting
- **Progress Tracking**: Real-time status updates during discovery
- **Validation**: Check for required fields and data quality
- **Incremental Updates**: Add new objects without losing existing data

## Technical Details

### Discovery Process
1. **Category Pages**: Process `/code-language/spin2/page/N/` URLs
2. **Object Links**: Extract object page URLs from listings
3. **Individual Pages**: Visit each object page for detailed metadata
4. **Object ID Extraction**: Find "Object ID : XXXX" patterns
5. **Download URL Construction**: Build download URLs from Object IDs
6. **YAML Generation**: Convert to structured metadata format

### Rate Limiting
- Default 1.0 second delay between requests
- Configurable via `--delay` parameter
- Respects robots.txt and reasonable crawling practices

### Error Recovery
- Continue processing on individual failures
- Collect and report all errors at completion
- Graceful handling of network timeouts
- Validation of required fields before saving

## Integration Workflow

### Phase 1: Discovery
```bash
# Run discovery to build initial catalog
./discover_obex.sh
```

### Phase 2: Download & Analysis
```bash
# Use generated download URLs to fetch ZIP files
# Extract to external-projects directory
# Analyze code patterns with AI assistance
```

### Phase 3: Knowledge Base Integration
```bash
# Cross-reference OBEX objects with existing KB content
# Add "Community Examples" sections to relevant YAML files
# Link proven community patterns to official documentation
```

## Maintenance

### Regular Updates
```bash
# Monthly discovery runs to find new objects
./discover_obex.sh

# Check for updated versions of existing objects
# Validate download URLs still work
```

### Quality Assurance
- Verify P2 compatibility of discovered objects
- Check author attribution accuracy
- Validate download URL construction
- Monitor for OBEX website structure changes

## Troubleshooting

### Common Issues

**"Missing required Python packages"**
```bash
pip3 install requests beautifulsoup4 pyyaml
```

**"No objects found"**
- Check internet connectivity
- Verify OBEX website accessibility
- Try increasing `--delay` parameter

**"Download URLs not working"**
- Object IDs may have changed
- Run fresh discovery to update IDs
- Check OBEX website for structural changes

### Debug Mode
```python
# Enable verbose logging
discovery = OBEXDiscovery()
discovery.session.headers.update({'User-Agent': 'Debug/1.0'})
result = discovery.run_discovery(['spin2'])
print(discovery.stats['errors'])  # View all errors
```

## Contributing

### Adding New Categories
Modify `obex_discovery.py` to add new OBEX categories beyond SPIN2/PASM.

### Improving Metadata Extraction
Update extraction methods in `_extract_*` functions to capture additional metadata fields.

### Custom Categorization
Modify `_categorize_object()` and `_generate_tags()` methods to improve automatic classification.

---

**Status**: Production ready  
**Last Updated**: 2025-09-11  
**Maintainer**: P2 Knowledge Base Team