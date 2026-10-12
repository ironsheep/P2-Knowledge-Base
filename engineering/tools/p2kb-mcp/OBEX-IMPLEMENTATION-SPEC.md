# OBEX Implementation Specification for P2KB MCP

This document provides implementation details for adding OBEX (Parallax Object Exchange) support to the P2KB MCP server.

## Overview

OBEX is Parallax's community repository of P2 code objects. The P2 Knowledge Base contains metadata for ~113 OBEX objects, stored as individual YAML files.

**Important**: OBEX objects are served through OBEX-specific tools (`p2kb_obex_*`), separate from the key-based `p2kb_get`. *(Corrected 2026-10-07: this line used to say the objects are NOT in the main `p2kb-index.json`. They are — all 131 files under `community/obex/objects/`, including `_template.yaml`, are listed there as `p2kbCommunity<id>` keys. Like every KB file, they are subject to the delivery filter — `MCP-DELIVERY-FILTER-HANDOFF.md` §5.1.)*

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
    languages: ["PASM2"]               # OBEX "Language(s)"
    microcontroller: ["P2"]            # OBEX "Microcontroller(s)"
    content_type: ["Code"]             # OBEX "Content": Code, Hardware or Tip
    licence: "Other"                   # OBEX "Licence": MIT or Other
    version: ""                        # Version string (the only version field)
    file_format: "ZIP"                 # Usually ZIP
    file_size: "16 B"                  # Size string

  functionality:
    category: ["Math", "Motor Control", "Protocol", "Snippet"]  # OBEX "Category"/"Categories":
                                       # a string when one, a list when several
    subcategory: ""                    # Optional subcategory
    description_short: "..."           # authored one-liner, ≤120 chars (served as `description`)
    description_full: "..."            # the catalog description, as text
    tags: ["Servo"]                    # OBEX "Tag(s)" ([] when none)
    hardware_support: []               # Hardware platforms
    peripherals: []                    # Connected peripherals

  metadata:                            # served; holds only the upload date
    created_date: "2020-05-09"         # OBEX upload date; absent when OBEX shows none

  version_tracking:
    has_github_repo: false

  scrape_tracking:                     # scraper bookkeeping; removed by the delivery filter
    discovery_date: "2025-09-12..."    # When indexed
    created_date: "2022-01-04 12:00:00"  # the scraper's own record; never served
```

`metadata.created_date` is the object's OBEX upload date — the field `p2kb_obex_get` reports as
`metadata.created_date` (moved there from `version_tracking.obex_upload_date` in KB v1.24.1, F-571).
`metadata` carries nothing else: the KB does not rate objects, so there is no quality score.

`scrape_tracking:` is the scrape bookkeeping (discovery and extraction dates, import source, and
similar). It stays in the YAML for our own scraper and gates, and the delivery filter removes it
(`scrape_tracking` is in the index's `remove_fields`; see `MCP-DELIVERY-FILTER-HANDOFF.md`, §3 and the
2026-10-10 amendment). A `p2kb_obex_*` tool therefore never receives any field under it.

## Download URL Pattern

All OBEX downloads follow this pattern:
```
https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB{object_id}
```

Note: The URL uses `OB` prefix (e.g., `OB2811`), but the object_id in YAML is just the number (`2811`).

## Categories

From KB v1.24.2 every object carries **OBEX's own categories**, mirrored from its catalog page by
`engineering/tools/obex-integration/obex-catalog-mirror.py` (F-573); 32 of the 130 objects list
several, so `category` is a string or a list. Objects per category on 2026-10-12 (an object counts
once in each category it lists):

| Category | Objects | Category | Objects |
|---|---|---|---|
| Protocol | 32 | Data Storage | 9 |
| Sensor | 30 | Math | 7 |
| Display | 26 | Fun | 5 |
| Human Input | 13 | Snippet | 5 |
| Signals | 13 | 3D Model | 3 |
| Motor Control | 11 | PCB Design | 3 |
| Speech and Sound | 9 | Tool | 3 |
| | | Other | 2 |

The list changes when OBEX changes; a tool reads it from the objects, never from a fixed list
(`MCP-OBEX-SUMMARY-CHANGE-REQUEST.md` §3.5). The earlier nine values (`drivers`, `misc`, …) were
our scraper's own buckets and are gone.

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
  metadata?: {             // each key omitted when empty; the whole block omitted when all are
    created_date?: string; // object_metadata.metadata.created_date
    file_size?: string;    // technical_details.file_size
    version?: string;      // technical_details.version
  };                       // no quality field: the KB does not rate objects
  full_metadata: object;   // the object's object_metadata AFTER the delivery filter (from 1.5.1)
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
