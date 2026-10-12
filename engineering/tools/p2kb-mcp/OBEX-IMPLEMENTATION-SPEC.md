# OBEX Implementation Specification for P2KB MCP

This document provides implementation details for adding OBEX (Parallax Object Exchange) support to the P2KB MCP server.

## Overview

OBEX is Parallax's community repository of P2 code objects. The P2 Knowledge Base mirrors the catalog entry of every P2 object on OBEX (130 on 2026-10-12), one YAML file per object.

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

Each OBEX object is a **pure mirror** of its catalog page (KB v1.24.4): the catalog's fields and
nothing of ours. Every object has exactly this shape, keys in this order:

```yaml
object_metadata:
  object_id: "2811"                    # OBEX Object ID (string); also the file name
  title: "Park transformation"         # page title
  author: "ManAtWork"                  # OBEX "Author"
  functionality:
    category: ["Math", "Motor Control", "Protocol", "Snippet"]  # OBEX "Category"/"Categories":
                                       # a string when one, a list when several, "" when none
    tags: ["Servo"]                    # OBEX "Tag(s)" ([] when none)
    description_short: "..."           # authored one-liner, ≤120 chars (served as `description`)
    description_full: "..."            # the catalog description as text; a link's URL follows its words
  technical_details:
    content_type: ["Code"]             # OBEX "Content": Code, Hardware or Tip
    microcontroller: ["P2"]            # OBEX "Microcontroller(s)"
    languages: ["PASM2"]               # OBEX "Language(s)"
    licence: "Other"                   # OBEX "Licence": MIT or Other
  metadata:
    created_date: "2020-05-09"         # OBEX upload date (the Object ID line's date)
  urls:
    obex_page: "https://obex.parallax.com/obex/park-transformation/"
    download_direct: "https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB2811"
                                       # ABSENT when OBEX offers no download (5 objects)
```

`description_short` is the one field that is not catalog text: an authored one-sentence summary
(F-573), checked by the release gate "OBEX One-Line Descriptions". Every other field is written only
by `engineering/tools/obex-integration/obex-catalog-mirror.py`, from the object's page.

**Not in any object (removed in KB v1.24.4):**
- `author_username`, `version`, `file_size` and `file_format`;
- `github_repo`, `documentation` and `forum_discussion`;
- `subcategory`, `hardware_support` and `peripherals`;
- the `compatibility`, `version_tracking`, `capability` and `scrape_tracking` blocks.

The KB rates no object and records no compatibility or version of its own. The `capability`
classification is the KB's own; it moved to an engineering-side file that is not served. A link
OBEX shows in the description (a GitHub repository, a store page) is in `description_full` with its
URL.

## Download URL Pattern

Use `urls.download_direct`; never build the URL from the id. OBEX's ZIP link has this form:
```
https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB{object_id}
```
The URL uses the `OB` prefix (e.g., `OB2811`), but the object_id in YAML is just the number (`2811`).

**Some objects have no download.** For five objects (4442, 4571, 4581, 4616, 4617 on 2026-10-12)
the OBEX page says "There are no downloads available for this object", and the ZIP link answers
`invalid!`. Their YAML has no `download_direct`. A tool reports "no download; see the page"
for them and fetches nothing. Their descriptions say where the code is, usually a GitHub repository.

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
  download_url?: string;   // urls.download_direct; omitted when the object has no download
  languages: string[];
  tags: string[];
  obex_page: string;
  metadata?: {             // omitted when created_date is absent or empty
    created_date: string;  // object_metadata.metadata.created_date
  };                       // no quality, version or size: the KB rates nothing, OBEX publishes neither
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
- Download URLs come from each object's `urls.download_direct` (absent when OBEX offers no download)

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
