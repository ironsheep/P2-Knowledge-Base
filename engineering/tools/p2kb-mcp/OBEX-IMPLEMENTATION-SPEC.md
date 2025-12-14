# OBEX Implementation Specification for P2KB MCP

This document provides implementation details for adding OBEX (Parallax Object Exchange) support to the P2KB MCP server.

## Overview

OBEX is Parallax's community repository of P2 code objects. The P2 Knowledge Base contains metadata for ~113 OBEX objects, stored as individual YAML files.

**Important**: OBEX objects are NOT in the main `p2kb-index.json`. They require separate tools and direct HTTP fetching. The MCP must implement OBEX-specific tools (`p2kb_obex_*`) that fetch YAML directly from GitHub, not through the key-based lookup system.

## Data Location

```
GitHub Raw Base: https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main
GitHub API Base: https://api.github.com/repos/ironsheep/P2-Knowledge-Base/contents

OBEX Objects Path: deliverables/ai/P2/community/obex/objects/
Example: deliverables/ai/P2/community/obex/objects/2811.yaml
```

**Important**: Object IDs are numeric (e.g., `2811`, `4047`, `5274`), NOT prefixed with "OB".

## YAML Schema

Each OBEX object has this structure:

```yaml
object_metadata:
  object_id: "2811"                    # Unique numeric ID (string)
  title: "Park transformation"         # Human-readable name
  author: "ManAtWork"                  # Author display name
  author_username: ""                  # Forum username if different

  urls:
    obex_page: "https://obex.parallax.com/obex/park-transformation/"
    download_direct: "https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB2811"
    forum_discussion: ""               # Related forum thread
    github_repo: ""                    # GitHub mirror if exists
    documentation: ""                  # External docs

  technical_details:
    languages: ["SPIN2", "PASM2"]      # Code languages used
    microcontroller: ["P2"]            # Always P2 for this KB
    version: ""                        # Version string
    file_format: "ZIP"                 # Usually ZIP
    file_size: "16 B"                  # Size string

  functionality:
    category: "motors"                 # Primary category
    subcategory: ""                    # Optional subcategory
    description_short: "..."           # Brief description
    description_full: "..."            # Full description
    tags: ["servo", "motor", "adc"]    # Searchable tags
    hardware_support: []               # Hardware platforms
    peripherals: []                    # Connected peripherals

  metadata:
    discovery_date: "2025-09-12..."    # When indexed
    last_verified: "2025-09-12..."     # Last verification
    extraction_status: "author_extracted"  # Status
    quality_score: 5                   # 1-10 rating
    created_date: "2020-05-09 12:00:00"    # Original upload date
```

## Download URL Pattern

All OBEX downloads follow this pattern:
```
https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB{object_id}
```

Note: The URL uses `OB` prefix (e.g., `OB2811`), but the object_id in YAML is just the number (`2811`).

## Categories

Current OBEX categories and counts:
- `drivers`: 49 objects
- `misc`: 34 objects
- `display`: 7 objects
- `demos`: 5 objects
- `audio`: 5 objects
- `motors`: 5 objects
- `communication`: 4 objects
- `sensors`: 3 objects
- `tools`: 1 object

**Important**: Many objects are miscategorized. Always search across ALL objects, not just by category.

## Suggested MCP Tools

### p2kb_obex_get

Retrieves OBEX object metadata by ID.

```typescript
interface ObexGetParams {
  object_id: string;  // e.g., "2811" (NOT "OB2811")
}

interface ObexGetResult {
  object_id: string;
  title: string;
  author: string;
  category: string;
  description: string;
  download_url: string;
  languages: string[];
  tags: string[];
  obex_page: string;
  full_metadata: object;  // Complete YAML content
}
```

### p2kb_obex_search

Searches OBEX objects by keyword in title, description, tags.

```typescript
interface ObexSearchParams {
  term: string;           // Search term
  category?: string;      // Optional category filter
  language?: string;      // Optional language filter ("SPIN2", "PASM2")
  limit?: number;         // Default: 20
}

interface ObexSearchResult {
  term: string;
  results: Array<{
    object_id: string;
    title: string;
    author: string;
    category: string;
    description_short: string;
    match_type: string;  // "title", "tag", "description"
  }>;
  count: number;
  total_objects: number;
}
```

### p2kb_obex_browse

Lists OBEX objects by category.

```typescript
interface ObexBrowseParams {
  category?: string;      // Optional - if omitted, list all categories
  author?: string;        // Optional - filter by author
}

interface ObexBrowseResult {
  category: string | null;
  objects: Array<{
    object_id: string;
    title: string;
    author: string;
  }>;
  count: number;
}

// When no category specified:
interface ObexCategoriesResult {
  categories: Record<string, number>;  // category -> count
  total_objects: number;
}
```

### p2kb_obex_authors

Lists prolific OBEX authors (useful for finding quality code).

```typescript
interface ObexAuthorsResult {
  authors: Array<{
    name: string;
    object_count: number;
  }>;
  total_authors: number;
}
```

Top authors:
- Jon McPhalen (jonnymac): ~44 objects
- Stephen M Moraco: ~15 objects
- Wuerfel_21: ~11 objects

## Search Strategy Guidance

The MCP should implement intelligent search expansion. When searching for hardware terms, expand to related terms:

```yaml
keyword_expansions:
  i2c: [i2c, iic, twi, two-wire]
  spi: [spi, serial peripheral, shift]
  uart: [uart, serial, rs232, rs485]
  led: [led, pixel, ws2812, rgb, neopixel, strip]
  motor: [motor, servo, stepper, pwm, drive]
  sensor: [sensor, detector, measure, monitor]
  display: [display, lcd, oled, screen, graphics]
```

## Implementation Notes

### Listing All Objects

To get all OBEX object IDs, the MCP can:
1. Fetch the directory listing from GitHub API
2. Parse filenames (exclude `_template.yaml`)
3. Cache the list with the main index

```
GET https://api.github.com/repos/ironsheep/P2-Knowledge-Base/contents/deliverables/ai/P2/community/obex/objects
```

### Caching Strategy

- Cache individual object YAML files (they rarely change)
- Cache the object ID list (refresh with main index)
- No need to cache download URLs (they're constructed from object_id)

### Error Handling

When object not found:
1. Check if ID looks valid (numeric)
2. Suggest similar object IDs if close match exists
3. Suggest searching by term instead

## Example Usage Flow

1. User asks: "Find OBEX objects for I2C sensors"
2. MCP expands search: ["i2c", "iic", "twi", "sensor", "detector"]
3. MCP searches all objects' titles, descriptions, tags
4. Return matches sorted by relevance
5. User picks object ID 4047
6. MCP fetches full metadata via `p2kb_obex_get`
7. User gets download_url to fetch the actual code

## Files to Reference

In P2-Knowledge-Base repo:
- `deliverables/ai/P2/community/obex/objects/*.yaml` - All object metadata
- `deliverables/ai-reference/auxiliary-guides/search-strategies/obex-search-optimization.md` - Search guide
- `engineering/tools/p2kb/obex/download-helper.ps1` - Reference implementation (PowerShell)

## Testing

Test with these object IDs:
- `2811` - Park transformation (motors, CORDIC example)
- `4047` - Should exist
- `9999` - Should NOT exist (test error handling)
