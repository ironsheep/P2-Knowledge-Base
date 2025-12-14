# OBEX Download Helper - Theory of Operations

This document describes the operational flow of the OBEX download helper, intended for reimplementation in the P2KB MCP server.

## Purpose

The download helper automates the process of:
1. Looking up OBEX object metadata from the P2 Knowledge Base
2. Downloading the ZIP file from Parallax's OBEX server
3. Extracting the contents (including nested ZIPs)
4. Organizing files in a named directory

## Project Directory Structure

OBEX objects are downloaded into an `OBEX/` folder at the root of the user's project. Each object gets its own subdirectory named by a slug derived from the object's title.

### Location

```
{project_root}/
├── OBEX/                           # Container for all OBEX downloads
│   ├── park-transformation/        # Object 2811
│   │   ├── OB2811.zip             # Original download (kept for reference)
│   │   ├── park_transform.spin2   # Extracted files
│   │   └── ...
│   ├── ws2812b-led-driver/         # Object 4047
│   │   ├── OB4047.zip
│   │   ├── ws2812b.spin2
│   │   └── ...
│   └── i2c-oled-display/           # Object 2853
│       ├── OB2853.zip
│       └── ...
├── src/                            # User's project source
└── ...
```

### Why This Structure Works

1. **Isolation**: Each OBEX object lives in its own directory - no file conflicts
2. **Identification**: Directory names are human-readable (slug from title)
3. **Traceability**: Original ZIP files are preserved with object ID
4. **Coexistence**: Multiple objects can be downloaded without collision
5. **Portability**: The entire `OBEX/` folder can be moved or shared

### Slug-Based Naming

The slug ensures:
- **No collisions**: Different objects get different directory names
- **Filesystem safety**: Only alphanumeric characters and hyphens
- **Readability**: Users can identify objects by directory name

**Same-title handling**: If two objects had identical titles (rare), they would get the same slug. The second download would overwrite the first. In practice, OBEX titles are unique.

### Working Directory

The download helper operates from the project root and:
1. Creates `OBEX/` if it doesn't exist
2. Creates `OBEX/{slug}/` for the specific object
3. Changes into that directory for download/extraction
4. Returns to project root when complete

## Input

- **Object ID**: A numeric string (e.g., `"2811"`, `"4047"`)
- NOT prefixed with "OB" - that prefix is only used in download URLs

## Important: OBEX Not in P2KB Index

**OBEX objects are NOT included in the main p2kb-index.json**. This means:
- You cannot use `p2kb_get` or key-based lookup for OBEX
- OBEX YAML files must be fetched directly via HTTP
- The MCP needs separate OBEX-specific tools

This is by design - OBEX is a separate subsystem with its own metadata structure.

## Operational Flow

### Step 1: Fetch Object Metadata

**Goal**: Retrieve the YAML metadata for the object directly from GitHub.

**Important**: Must fetch via HTTP, not through p2kb key lookup.

**Path Construction**:
```
deliverables/ai/P2/community/obex/objects/{object_id}.yaml
```

**Full URL (GitHub API)**:
```
https://api.github.com/repos/ironsheep/P2-Knowledge-Base/contents/deliverables/ai/P2/community/obex/objects/{object_id}.yaml
```
With header: `Accept: application/vnd.github.raw`

**Example**:
```
Object ID: 2811
Path: deliverables/ai/P2/community/obex/objects/2811.yaml
```

**Validation**:
- File must exist
- Content must not be empty
- Must be valid YAML

**Error Case**: If metadata not found, abort with error suggesting user verify the object ID.

### Step 2: Parse Title from Metadata

**Goal**: Extract the human-readable title for directory naming.

**YAML Field**: `object_metadata.title` (appears as `title:` at root level after `object_metadata:`)

**Example**:
```yaml
object_metadata:
  title: "Park transformation"
```

**Result**: `"Park transformation"`

**Error Case**: If title cannot be parsed, abort - metadata may be malformed.

### Step 3: Generate Directory Slug

**Goal**: Create a filesystem-safe directory name from the title.

**Algorithm**:
```
1. Convert to lowercase
2. Replace all non-alphanumeric characters with hyphens
3. Collapse multiple consecutive hyphens to single hyphen
4. Remove leading/trailing hyphens
```

**Examples**:
| Title | Slug |
|-------|------|
| `Park transformation` | `park-transformation` |
| `WS2812B LED Driver` | `ws2812b-led-driver` |
| `I2C OLED Display (128x64)` | `i2c-oled-display-128x64` |
| `  Spaces & Symbols! @#$  ` | `spaces-symbols` |

**Pseudocode**:
```javascript
function generateSlug(title) {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9]/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}
```

### Step 4: Determine Download URL

**Goal**: Get the direct download URL for the ZIP file.

**Primary Source**: `object_metadata.urls.download_direct` from YAML

**Fallback Construction** (if field empty or missing):
```
https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB{object_id}
```

**Important**: The URL uses `OB` prefix (e.g., `OB2811`), unlike the object_id which is just numeric.

**Example**:
```
Object ID: 2811
Download URL: https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB2811
```

### Step 5: Create Target Directory

**Goal**: Create a directory to hold the downloaded and extracted files.

**Path Pattern**:
```
OBEX/{slug}/
```

**Example**:
```
OBEX/park-transformation/
```

**Behavior**: Create directory if it doesn't exist. If it exists, contents will be overwritten on extraction.

### Step 6: Download ZIP File

**Goal**: Fetch the ZIP archive from Parallax's server.

**Filename Pattern**:
```
OB{object_id}.zip
```

**Example**:
```
OB2811.zip
```

**Validation**:
- HTTP request must succeed
- File must not be empty (0 bytes)
- Should report file size for user feedback

**Error Cases**:
- Network failure: Report connection error
- Empty file: OBEX server may have returned error page instead of ZIP
- HTTP error: Report status code

### Step 7: Extract Primary ZIP

**Goal**: Unpack the downloaded ZIP archive.

**Destination**: Current directory (the slug-named directory created in Step 5)

**Behavior**: Overwrite existing files if present (`-Force` equivalent)

### Step 8: Handle Nested ZIPs

**Goal**: OBEX packages often contain nested ZIP files that should also be extracted.

**Detection**:
```
Find all *.zip files recursively EXCEPT the original download (OB{id}.zip)
```

**Extraction**:
For each nested ZIP:
1. Get filename without extension (e.g., `nested.zip` → `nested`)
2. Create subdirectory with that name
3. Extract contents into subdirectory

**Example**:
```
OBEX/my-object/
├── OB2811.zip (original - skip)
├── source-code.zip → extract to source-code/
└── documentation.zip → extract to documentation/
```

### Step 9: Report Results

**Goal**: Provide user with summary of what was downloaded and where.

**Information to Report**:
- Object ID
- Title
- Final directory path
- List of extracted files (optional, can be verbose)
- Total size

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│ Input: Object ID (e.g., "2811")                         │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 1: Fetch YAML metadata                             │
│   GET deliverables/ai/P2/community/obex/objects/2811.yaml│
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 2: Parse title                                     │
│   title: "Park transformation"                          │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 3: Generate slug                                   │
│   "park-transformation"                                 │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 4: Get download URL                                │
│   From YAML or construct:                               │
│   https://obex.parallax.com/...&obuid=OB2811            │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 5: Create directory                                │
│   OBEX/park-transformation/                             │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 6: Download ZIP                                    │
│   → OB2811.zip (validate non-empty)                     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 7: Extract primary ZIP                             │
│   Unzip OB2811.zip to current directory                 │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 8: Find and extract nested ZIPs                    │
│   For each *.zip (except OB2811.zip):                   │
│     Create subdir, extract into it                      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 9: Report results                                  │
│   - Location: OBEX/park-transformation/                 │
│   - Files: [list]                                       │
│   - Size: X KB                                          │
└─────────────────────────────────────────────────────────┘
```

## MCP Implementation Considerations

### What the MCP Should Provide

The MCP cannot directly write files to the user's filesystem. Instead, it should provide:

1. **`p2kb_obex_get`**: Returns metadata including download URL
2. **`p2kb_obex_download_info`**: Returns all information needed to download:
   - Download URL
   - Suggested filename (`OB{id}.zip`)
   - Suggested directory name (slug)
   - Title for display

### What the Client (Claude) Should Do

The AI client using the MCP should:
1. Call `p2kb_obex_get` to fetch metadata
2. Use the returned download URL with appropriate tools (Bash `curl`, etc.)
3. Handle extraction using available tools
4. Report results to user

### Alternative: MCP Download Tool

If the MCP has filesystem access (depends on deployment), it could provide:

```typescript
interface ObexDownloadParams {
  object_id: string;
  target_dir?: string;  // Default: "./OBEX"
  extract?: boolean;    // Default: true
}

interface ObexDownloadResult {
  success: boolean;
  object_id: string;
  title: string;
  path: string;           // Full path to extracted files
  files: string[];        // List of extracted files
  size_bytes: number;
  nested_zips_extracted: number;
}
```

## Error Handling Summary

| Step | Error | Response |
|------|-------|----------|
| 1 | Metadata not found | "Object ID {id} not found. Verify the ID is correct." |
| 2 | Title parse fail | "Metadata malformed - missing title field." |
| 4 | No download URL | Use fallback URL construction |
| 6 | Download fails | "Download failed: {HTTP error or network message}" |
| 6 | Empty file | "Download returned empty file - OBEX may be unavailable." |
| 7 | Extract fails | "ZIP extraction failed - file may be corrupted." |

## Additional Output Behaviors

### File Listing

After extraction, the helper lists all extracted files recursively. This helps users see what they got:
```
[INFO] Extracted contents:
Mode         LastWriteTime     Length Name
----         -------------     ------ ----
-a----       5/9/2020 12:00     1234  park_transform.spin2
-a----       5/9/2020 12:00      567  README.txt
```

### Programmatic Output

The final line of stdout contains ONLY the path to the extracted files:
```
C:\Users\...\OBEX\park-transformation
```

This allows calling scripts/tools to capture the path for further processing:
```powershell
$extractPath = & ".p2kb-cache\obex\download-helper.ps1" -ObjectId 2811 | Select-Object -Last 1
```

### User Inspection Pause

The helper ends with `[STOP] Ready for user inspection` to indicate:
1. Download and extraction completed successfully
2. User should review the files before proceeding
3. No further automatic actions will be taken

### Preserved Original ZIP

The original `OB{id}.zip` file is kept in the directory for:
- Re-extraction if needed
- Verification of original contents
- Sharing with others

## Testing Checklist

- [ ] Valid object ID returns correct metadata
- [ ] Invalid object ID returns helpful error
- [ ] Slug generation handles special characters
- [ ] Download URL fallback works when YAML field empty
- [ ] Nested ZIPs are detected and extracted
- [ ] Empty downloads are rejected
- [ ] Directory already exists - handled gracefully
- [ ] Stdout last line contains only the path
- [ ] Original ZIP is preserved after extraction
