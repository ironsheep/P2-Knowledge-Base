# P2 Knowledge Base MCP Server - Architecture Evaluation

**Status:** Future Enhancement - Evaluation Phase
**Created:** 2025-10-02
**Purpose:** Evaluate MCP server approaches to solve remote Claude Code instance access limitations

---

## Problem Statement

Remote Claude Code instances (without local filesystem access to the knowledge base) face critical limitations when accessing P2 Knowledge Base content from GitHub:

### Current Limitations
1. **WebFetch tool has ~5KB output limit** due to AI processing layer
2. **214 YAML files (8%) exceed this limit**, including:
   - 11 critical manifest files (26.8% of manifests)
   - 119 knowledge base files (12.4% of content)
3. **Per-project downloads are inefficient** - same files downloaded repeatedly
4. **No cache invalidation** - stale content risk without update mechanism
5. **Complex navigation** - Claude must manually manage manifest traversal

### Core Requirements
- ✅ Bypass WebFetch size limits
- ✅ Shared cache across project instances
- ✅ Staleness detection (hash-based validation)
- ✅ Minimal transformation risk
- ✅ Cross-platform compatibility

---

## Approach 1: Minimal MCP - Smart File Fetcher

**Philosophy:** MCP provides caching infrastructure, Claude handles all parsing/navigation

### Tool Interface

```python
# Core file access
p2kb__fetch_file(path: str) -> str
    """
    Fetch file from cache or GitHub, return raw content.

    Args:
        path: Relative path from repository root
              e.g., "manifests/P2/language/pasm2-manifest.yaml"

    Returns:
        Raw file content (YAML string)

    Behavior:
        1. Check cache for path
        2. If missing/stale, download from GitHub using curl
        3. Save to cache
        4. Return raw content (no parsing, no transformation)
    """

# Cache management
p2kb__check_updates() -> dict
    """
    Check if cached content is stale.

    Returns:
        {
            "current_version": "v1.4.0",
            "latest_version": "v1.4.1",
            "needs_update": true,
            "content_hash_match": false
        }

    Behavior:
        1. Fetch propeller-knowledge-root.yaml (small file)
        2. Extract ai_instructions.content_hash
        3. Compare with cached metadata
    """

p2kb__clear_cache() -> bool
    """Force cache refresh on next fetch."""

# Optional convenience
p2kb__list_files(pattern: str = "*") -> list[str]
    """List files in cache matching glob pattern."""
```

### Claude's Workflow

```python
# Session start
updates = p2kb__check_updates()
if updates["needs_update"]:
    p2kb__clear_cache()

# Navigate knowledge base (Claude does this)
root_yaml = p2kb__fetch_file("manifests/propeller-knowledge-root.yaml")
root = yaml.parse(root_yaml)  # Claude parses

pasm2_manifest_yaml = p2kb__fetch_file("manifests/P2/language/pasm2-manifest.yaml")
pasm2 = yaml.parse(pasm2_manifest_yaml)  # Claude parses

# Get specific instruction
add_yaml = p2kb__fetch_file("engineering/knowledge-base/P2/language/pasm2/add.yaml")
add_instruction = yaml.parse(add_yaml)  # Claude parses and uses
```

### Internal Implementation

```python
class P2KBMinimalMCP:
    def __init__(self):
        self.cache_root = Path.home() / ".p2kb-mcp-cache"
        self.metadata_file = self.cache_root / ".metadata"
        self.github_base = "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main"

    def fetch_file(self, path: str) -> str:
        cache_path = self.cache_root / self._get_current_version() / path

        # Check cache
        if cache_path.exists() and not self._is_stale():
            return cache_path.read_text()

        # Download from GitHub (no size limits!)
        url = f"{self.github_base}/{path}"
        response = requests.get(url)
        content = response.text

        # Save to cache
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(content)

        return content  # Raw YAML, no transformation

    def check_updates(self) -> dict:
        # Fetch root manifest hash
        root = self.fetch_file("manifests/propeller-knowledge-root.yaml")
        root_data = yaml.safe_load(root)
        remote_hash = root_data["ai_instructions"]["content_hash"]

        # Compare with cached metadata
        metadata = self._load_metadata()
        local_hash = metadata.get("content_hash")

        return {
            "current_version": metadata.get("version"),
            "remote_hash": remote_hash,
            "needs_update": remote_hash != local_hash
        }
```

### Pros
- ✅ **Zero transformation risk** - Returns exact GitHub content
- ✅ **Minimal code** - ~200 lines total implementation
- ✅ **Easy maintenance** - No logic updates when KB structure changes
- ✅ **Claude expertise preserved** - Still uses existing YAML parsing skills
- ✅ **Maximum flexibility** - Claude can navigate any way it wants

### Cons
- ❌ **Claude does more work** - Manual manifest navigation
- ❌ **No optimizations** - Each fetch is independent
- ❌ **No search indexes** - Claude searches by reading files
- ❌ **Verbose tool calls** - Multiple fetches for complex queries

### Effort Estimate
- **Implementation:** 1-2 days
- **Testing:** 1 day
- **Documentation:** 0.5 days
- **Total:** ~3 days

---

## Approach 2: Smart MCP - Knowledge Base Navigator

**Philosophy:** MCP provides high-level semantic interface, handles all navigation/parsing internally

### Tool Interface

```python
# PASM2 Instructions
p2kb__get_instruction(mnemonic: str) -> dict
    """Get complete instruction data, parsed and ready to use."""

p2kb__list_instructions(category: str = None) -> list[dict]
    """List all instructions or filter by category."""

p2kb__search_instructions(keyword: str) -> list[dict]
    """Search instruction mnemonics, descriptions, examples."""

# OBEX Objects
p2kb__search_obex(keyword: str) -> list[dict]
    """Search unified OBEX index with natural groups and aliases."""

p2kb__get_obex_object(object_id: str) -> dict
    """Get specific OBEX object metadata."""

# Smart Pins
p2kb__get_smart_pin_mode(mode: int) -> dict
    """Get Smart Pin mode configuration (0-31)."""

p2kb__list_smart_pin_modes(filter_type: str = None) -> list[dict]
    """List all modes, optionally filtered by type."""

# Spin2 Elements
p2kb__get_spin2_element(name: str, type: str = None) -> dict
    """Get Spin2 method, operator, keyword, etc."""

p2kb__search_spin2(keyword: str) -> list[dict]
    """Search all Spin2 elements."""

# Patterns & Idioms
p2kb__get_pattern(pattern_id: str) -> dict
    """Get code pattern with examples."""

p2kb__search_patterns(keyword: str) -> list[dict]
    """Search patterns by keyword."""

# Manifests
p2kb__get_manifest(path: str) -> dict
    """Get parsed manifest structure."""

# System
p2kb__check_updates() -> dict
    """Check for KB updates."""

p2kb__get_version() -> str
    """Get cached KB version."""

p2kb__clear_cache() -> bool
    """Force cache refresh."""
```

### Claude's Workflow

```python
# Session start - automatic
updates = p2kb__check_updates()

# Get instruction - single call
add_instruction = p2kb__get_instruction("ADD")
# Returns: {mnemonic, syntax, encoding, description, timing, flags, examples, ...}

# Search OBEX - single call
i2c_objects = p2kb__search_obex("i2c")
# Returns: [{name, description, category, download_url, ...}, ...]

# Get Smart Pin mode - single call
pwm_mode = p2kb__get_smart_pin_mode(10)
# Returns: {mode, name, description, configuration, examples, ...}
```

### Internal Implementation

```python
class P2KBSmartMCP:
    def __init__(self):
        self.cache = P2KBCache()  # Same caching as Approach 1
        self.manifest_nav = ManifestNavigator(self.cache)
        self.search_index = SearchIndex(self.cache)

    def get_instruction(self, mnemonic: str) -> dict:
        # 1. Navigate to instruction via manifests
        manifest = self._fetch_and_parse("manifests/P2/language/pasm2-manifest.yaml")

        # 2. Find instruction entry
        inst_entry = manifest.find_instruction(mnemonic)

        # 3. Fetch instruction YAML
        inst_yaml = self._fetch_and_parse(inst_entry["content_path"])

        # 4. Return parsed data
        return inst_yaml

    def search_obex(self, keyword: str) -> list[dict]:
        # Load unified index once, cache in memory
        if not self.obex_index:
            index_yaml = self._fetch_and_parse("manifests/P2/community/obex-unified-index.yaml")
            self.obex_index = index_yaml

        # Search with alias resolution
        results = self.obex_index.search_with_aliases(keyword)
        return results

    def _fetch_and_parse(self, path: str) -> dict:
        # Same fetch logic as Approach 1
        yaml_content = self.cache.fetch_file(path)
        # But parse internally
        return yaml.safe_load(yaml_content)
```

### Advanced Features Possible

```python
# Smart search across all sources
p2kb__search_all(query: str) -> dict
    """
    Returns:
        {
            "instructions": [...],
            "obex_objects": [...],
            "smart_pins": [...],
            "patterns": [...],
            "spin2_elements": [...]
        }
    """

# Relationship mapping
p2kb__get_related(item_id: str) -> dict
    """
    Returns related content:
    - Similar instructions
    - Patterns using this instruction
    - OBEX objects implementing this
    """

# Code validation
p2kb__validate_instruction_syntax(syntax: str) -> dict
    """Validate instruction syntax against encoding."""
```

### Pros
- ✅ **Simpler for Claude** - Single tool call vs. multi-step navigation
- ✅ **Optimizable** - Can build search indexes, cache parsed objects
- ✅ **Powerful features** - Cross-cutting search, relationship mapping
- ✅ **Consistent interface** - Tools don't change when KB structure changes
- ✅ **Better UX** - Fewer round-trips, less token usage

### Cons
- ❌ **Transformation risk** - Parsing/reformatting could introduce errors
- ❌ **More code** - ~1000-1500 lines implementation
- ❌ **Maintenance burden** - Must update when KB structure changes
- ❌ **Less flexible** - Tools constrain how Claude navigates
- ❌ **Duplication** - Parsing logic exists in both MCP and Claude

### Effort Estimate
- **Implementation:** 1-2 weeks
- **Testing:** 3-5 days
- **Documentation:** 2 days
- **Maintenance:** Ongoing when KB schema changes
- **Total:** ~3 weeks initial + ongoing

---

## Approach 3: Existing Local-Only MCP (Node.js)

**Status:** Already Implemented (engineering/enhancements/mcp-server/)
**Philosophy:** Semantic tools for local instances, assumes KB already cloned

### Tool Interface

```javascript
// PASM2 Instructions
p2_instruction(mnemonic: string, category?: string) -> object
    """Look up a P2 PASM2 instruction by mnemonic."""

p2_instruction_list(category: string) -> object
    """List all P2 instructions in a category."""

// Smart Pins
smart_pin_mode(mode: string) -> object
    """Get Smart Pin mode configuration.
    Accepts: binary (00010), decimal (2), or name (sync_tx)"""

smart_pin_list() -> array
    """List all available Smart Pin modes."""

// Spin2
spin2_method(method: string) -> object
    """Look up a Spin2 method."""

// Patterns
search_patterns(pattern: string) -> array
    """Search for code patterns."""
```

### Implementation Details

**Language:** Node.js with MCP SDK
**Location:** `engineering/enhancements/mcp-server/`
**Dependencies:**
- `@modelcontextprotocol/sdk` - MCP framework
- `yaml` - YAML parsing
- `glob` - File pattern matching

**File Structure:**
```
mcp-server/
├── index.js          # Main server implementation (~400 lines)
├── package.json      # Dependencies
├── README.md         # Usage documentation
└── MCP-SERVER-SETUP.md  # Detailed setup guide
```

### How It Works

```javascript
// From index.js - assumes local filesystem
const KB_ROOT = process.env.P2KB_PATH || path.resolve(process.cwd());
const PASM2_PATH = path.join(KB_ROOT, 'engineering/knowledge-base/P2/language/pasm2');
const SPIN2_PATH = path.join(KB_ROOT, 'engineering/knowledge-base/P2/language/spin2');
const SMARTPINS_PATH = path.join(KB_ROOT, 'engineering/knowledge-base/P2/hardware/smart-pins/modes');

// Direct file access
async loadYamlFile(filePath) {
    const content = await fs.promises.readFile(filePath, 'utf8');
    return yaml.parse(content);
}

// Example: Lookup instruction
async lookupInstruction(mnemonic, category) {
    const files = await glob(`${PASM2_PATH}/**/${mnemonic.toLowerCase()}.yaml`);
    if (files.length > 0) {
        return await this.loadYamlFile(files[0]);
    }
}
```

### Claude's Workflow

```javascript
// Single call to get instruction
const add = await p2_instruction("ADD");
// Returns parsed YAML as JSON object

// List Smart Pin modes
const modes = await smart_pin_list();
// Returns array of all 32 modes with metadata

// Search patterns
const pwm_patterns = await search_patterns("pwm");
// Returns matching pattern files
```

### Pros
- ✅ **Already implemented** - Working code, tested
- ✅ **Simple for Claude** - Single-call semantic interface
- ✅ **Fast** - Direct filesystem access, no network latency
- ✅ **Node.js ecosystem** - Easy to extend with npm packages
- ✅ **Good for local instances** - Perfect when KB is cloned

### Cons
- ❌ **No remote support** - Cannot download from GitHub
- ❌ **No caching** - Assumes files always present
- ❌ **No staleness checking** - No update mechanism
- ❌ **Limited scope** - Doesn't cover all KB content (no OBEX, limited patterns)
- ❌ **Assumes local clone** - Fails if KB not in expected location
- ❌ **Does NOT solve the original problem** - Remote instances still broken

### Critical Limitation

**This MCP does NOT address the core problem:**
- Remote Claude Code instances without local KB clone → ❌ **Won't work**
- Shared cache across projects → ❌ **Not implemented**
- Download from GitHub → ❌ **Not implemented**
- Staleness detection → ❌ **Not implemented**

**Only works when:**
- KB repository is cloned locally
- MCP can access via `P2KB_PATH` or `process.cwd()`
- User is working within their local KB directory structure

### Use Case

**Perfect for:**
- Local development with KB repo cloned
- Users who always work from same machine
- Enhancement to existing local workflow

**Not suitable for:**
- Remote Claude Code instances
- Users without local KB clone
- Cross-project cache sharing

### Effort Estimate
- **Already complete** - 0 days
- **Extend to remote support** - Would need Approach 1's download/cache layer added

---

## Comparison Matrix

| Dimension | Approach 1: Minimal | Approach 2: Smart | Approach 3: Local-Only |
|-----------|-------------------|------------------|----------------------|
| **Implementation Status** | Not started | Not started | ✅ Complete |
| **Implementation Complexity** | Low (~200 lines) | High (~1500 lines) | Medium (~400 lines) |
| **Solves Remote Problem** | ✅ Yes | ✅ Yes | ❌ **No** |
| **Download from GitHub** | ✅ Yes | ✅ Yes | ❌ No |
| **Caching Strategy** | ✅ Yes | ✅ Yes | ❌ No |
| **Staleness Detection** | ✅ Yes | ✅ Yes | ❌ No |
| **Transformation Risk** | None (returns raw) | Moderate (parses internally) | Moderate (parses internally) |
| **Claude Workload** | Higher (manual nav) | Lower (single calls) | Lower (single calls) |
| **Token Efficiency** | Lower (multiple calls) | Higher (single calls) | Higher (single calls) |
| **Flexibility** | Maximum | Constrained by tools | Constrained by tools |
| **Optimization Potential** | None | High (indexing, caching) | Medium (local only) |
| **Maintenance Burden** | Minimal | Moderate-High | Low-Medium |
| **Feature Richness** | Basic | Advanced possible | Moderate |
| **Language** | Python (proposed) | Python (proposed) | Node.js (existing) |
| **Time to Production** | ~3 days | ~3 weeks | ✅ Already done (for local) |

---

## Hybrid Approaches (Combining Best of Each)

### Option A: Extend Approach 3 with Download/Cache Layer

**Add to existing Node.js MCP:**
```javascript
// New tools added to existing server
p2kb__download_cache() -> status
    """Download KB from GitHub to local cache."""

p2kb__set_kb_path(path: string) -> status
    """Point to cached KB instead of local clone."""

p2kb__check_updates() -> status
    """Check GitHub for updates, refresh cache if needed."""
```

**Benefits:**
- ✅ Leverage existing working code
- ✅ Maintain familiar tool interface
- ✅ Add remote support without rewrite
- ✅ Can use Node.js ecosystem for downloads

**Effort:** ~2-3 days to add download/cache layer

### Option B: Approach 1 Base + Approach 3 Convenience Layer

**Two-tier system:**
```python
# Tier 1: Minimal fetcher (Approach 1 - for all instances)
p2kb__fetch_file(path: str) -> str

# Tier 2: Semantic tools (Approach 3 - optional enhancement)
p2_instruction(mnemonic: str) -> dict
smart_pin_mode(mode: int) -> dict
```

**Benefits:**
- Start with Approach 1 (minimal risk, fast delivery)
- Use Approach 3 as optional enhancement layer
- Two independent MCPs, can use together or separately
- No commitment to full semantic layer

**Effort:** ~3 days (Approach 1) + Approach 3 already done

### Option C: Unified Python MCP with Progressive Features

```python
# Core (always available)
p2kb__fetch_file(path: str) -> str

# Convenience (optional, low risk)
p2kb__get_manifest_parsed(path: str) -> dict
    """Parse manifest YAML, but no navigation logic."""

p2kb__get_instruction_parsed(path: str) -> dict
    """Parse instruction YAML, but no path lookup."""

# Semantic (optional, higher level)
p2kb__search_obex_index(keyword: str) -> list[dict]
    """Search pre-built OBEX index only."""
```

**Benefits:**
- Single MCP server, progressive enhancement
- Can evaluate usage patterns before building more
- Python ecosystem (matches KB tooling)
- Start minimal, grow as needed

---

## Recommendation: Evaluation Criteria

### Choose Approach 1 (Minimal) If:
- **Primary goal:** Solve remote instance problem
- Speed to production is critical (3 days)
- Want to minimize transformation risk
- KB structure changes frequently
- Prefer Claude to retain full navigation control
- Want simplest possible solution

### Choose Approach 2 (Smart) If:
- Token efficiency is paramount
- Want to enable advanced features (cross-search, relationships)
- KB structure is stable
- Willing to invest in maintenance (3 weeks + ongoing)
- Premium user experience over simplicity

### Choose Approach 3 (Existing) If:
- **Only need local enhancement** (already works!)
- Users always work with KB cloned locally
- Remote access is NOT a requirement
- Want zero additional implementation effort

### Choose Hybrid Option A (Extend Approach 3) If:
- Want to leverage existing Node.js code
- Prefer incremental enhancement (2-3 days)
- Like the semantic tool interface
- Comfortable maintaining Node.js

### Choose Hybrid Option B (Two-Tier) If:
- Want both minimal and semantic options
- Users can choose their preference
- Two independent servers acceptable
- Maximum flexibility desired

### Choose Hybrid Option C (Progressive Python) If:
- Want single unified MCP
- Python ecosystem preferred (matches KB tools)
- Start minimal, evaluate, then enhance
- Single codebase easier to maintain

---

## Critical Assessment: Untested Code Changes Everything

**IMPORTANT DISCOVERY:** Approach 3 (existing Node.js MCP) has **never been tested in production**.

### What This Means

**Assumptions we made:**
- ❌ Semantic tools are helpful
- ❌ Tool interface is well-designed
- ❌ Parsing approach works reliably
- ❌ Integration with Claude works smoothly
- ❌ Performance is acceptable

**Reality:**
- ✅ Code exists (~400 lines)
- ❌ **Zero real-world validation**
- ❌ **Unknown if approach is correct**

### Risk of Building Full-Featured First

**Classic mistake:** Build features before validating assumptions

**Risks:**
- Build wrong abstractions
- Waste time on unused features
- Lock into bad design patterns
- Harder to pivot if fundamentally wrong

### Recommended Approach: Incremental with Learning

#### Phase 1: Minimal Viable Product (1-2 days)
**Goal:** Solve remote instance problem ONLY

```javascript
// Three tools:
p2kb__fetch_file(path: string) -> string
    // Download from GitHub OR cache, return raw YAML

p2kb__check_updates() -> object
    // Hash-based staleness detection

p2kb__clear_cache() -> boolean
    // Force refresh
```

**Test:** Can Claude navigate KB with just raw file access?

#### Phase 2: Real-World Usage (1 week)
**Goal:** Learn actual patterns

**Questions to answer:**
- How often same file fetched multiple times?
- Is manual manifest navigation painful?
- What queries are most common?
- Where does Claude struggle?

#### Phase 3: Evidence-Based Enhancement
**Goal:** Add features based on observed pain points

**Only add if evidence shows need:**
- Manifest parsing helper (if navigation is tedious)
- Instruction lookup (if frequently used)
- OBEX search (if common pattern)
- Smart Pin queries (if repeated)

**Don't build speculatively.**

### Why This Matters

**Node.js environment available ≠ should build everything**
- ✅ No external dependencies needed (built-in `https`)
- ✅ Can build full-featured MCP
- ❌ **But should we?** Unknown without testing

**Start minimal, learn fast, expand based on evidence.**

---

## Technology Choice Consideration

**Discovery:** Todo MCP (reference implementation) is written in **Go**, delivered as compiled binaries.

### Node.js vs. Go for MCP Server

**Node.js (Current Approach 3):**
- Interpreted/JIT compiled
- Slower startup time (~50-200ms)
- Higher memory usage (~30-50MB baseline)
- Good for I/O-bound operations
- Easy to modify/iterate

**Go (Todo MCP approach):**
- Compiled to native binary
- Fast startup (~5-10ms)
- Low memory footprint (~5-10MB)
- Excellent performance for parsing/processing
- Requires compilation step

### Performance Implications

**For MCP Server Workload:**

| Operation | Node.js | Go | Winner |
|-----------|---------|-----|--------|
| **Startup time** | 50-200ms | 5-10ms | Go (20x faster) |
| **Memory baseline** | 30-50MB | 5-10MB | Go (5x better) |
| **File downloads (https)** | Fast | Fast | Tie |
| **YAML parsing** | Moderate | Fast | Go (2-3x faster) |
| **JSON serialization** | Fast | Very fast | Go (slightly) |
| **In-memory caching** | Higher memory cost | Lower memory cost | Go |
| **Repeated parsing** | Slower | Much faster | Go (significant) |

### When Performance Matters

**Minimal MCP (Approach 1):**
- Mostly I/O bound (downloads, file reads)
- Performance difference: **Small**
- Node.js acceptable

**Full-Featured MCP (Approach 2):**
- Parsing-intensive (YAML → objects repeatedly)
- Search operations (indexing, filtering)
- In-memory caching (manifests, indexes)
- Performance difference: **Significant**
- Go strongly preferred

### Development Speed vs. Runtime Performance

**Node.js advantages:**
- Faster iteration (no compilation)
- Easier debugging
- Good for prototyping/learning phase
- Existing code in Approach 3

**Go advantages:**
- Better runtime performance
- Lower resource usage
- Cross-platform binaries (like Todo MCP)
- Professional deployment
- Matches Todo MCP architecture

### Strategic Recommendation

**Phase 1 (MVP):** Node.js acceptable
- Performance not critical for file fetching
- Fast iteration during learning phase
- Leverage existing Approach 3 code

**Phase 2+ (Production):** Consider Go rewrite if:
- Full-featured MCP justified by usage data
- Performance becomes issue (parsing overhead)
- Want cross-platform binaries
- Match Todo MCP deployment model

**OR:** Keep Node.js if:
- Minimal interface proves sufficient
- Performance is acceptable in practice
- Maintenance simplicity preferred
- Don't need binary distribution

---

## RECOMMENDED APPROACHES: Multiple Paths Forward

### Path A: Interim curl/wget (Immediate Hours)

**Strategy:** Enable remote instances TODAY, optimize later

**What to do:**
- Update CLAUDE.md instructions to allow curl/wget
- Claude downloads files to `.p2kb-cache/` in project root
- Per-project cache (not shared yet)
- No code to write

**Timeline:** 2-3 hours (documentation update)

**Pros:**
- ✅ Users working IMMEDIATELY (today)
- ✅ Zero development effort
- ✅ Uses existing tools
- ✅ Buys time to build proper MCP

**Cons:**
- ❌ Cache not shared across projects (inefficient)
- ❌ No automatic staleness detection
- ❌ Manual cache management
- ❌ Not optimal long-term solution

**Use case:** "Get users unblocked RIGHT NOW while we build the real solution"

---

### Path B: Node.js Minimal → Go Full-Featured

**Decision:** Node.js Minimal → Go Full-Featured

### Phase 1: Node.js Minimal MCP (Immediate - Week 1-2)

**Goal:** Unblock users NOW, validate approach

**What to build:**
- Three core tools (fetch, check_updates, clear_cache)
- Shared cache at `~/.p2kb-cache/`
- Uses Node.js built-in `https` module (zero external dependencies)
- ~200 lines of code
- **Time to users: 2-3 days**

**Why Node.js first:**
- ✅ **Immediate value** - Users unblocked this week
- ✅ **Fast iteration** - No compilation, easy debugging
- ✅ **Low risk** - Small codebase, simple functionality
- ✅ **Learning phase** - Real usage informs Go design
- ✅ **Node.js already required** - Claude Code dependency

**Deliverable:**
```bash
npm install -g @p2kb/mcp-server
# Users can immediately access KB from remote instances
```

### Phase 2: Go Full-Featured MCP (Production - Week 5-8)

**Goal:** Optimize performance, add advanced features

**What to build:**
- All Phase 1 functionality (backward compatible)
- Rich semantic tools (instruction lookup, OBEX search, etc.)
- Advanced features (cross-search, validation, relationships)
- In-memory caching and indexing
- Cross-platform binaries (matches Todo MCP model)
- **Time to production: 2-3 weeks** (informed by Phase 1 usage)

**Why Go for production:**
- ✅ **20x faster startup** (5ms vs 100ms)
- ✅ **5x lower memory** (5-10MB vs 30-50MB)
- ✅ **2-3x faster parsing** (critical for full-featured)
- ✅ **Cross-platform binaries** (consistent with Todo MCP)
- ✅ **Professional deployment** - No npm/Node.js runtime needed

**Deliverable:**
```bash
brew install p2kb-mcp  # macOS
# Or download binary for Linux/Windows
# Drop-in replacement, uses same cache
```

### Seamless Upgrade Path

**Critical design: Language-agnostic cache**

```
~/.p2kb-cache/
├── .metadata.json          # JSON (both Node.js and Go can read)
├── .lock                   # Prevent concurrent writes
└── v1.4.0/
    ├── manifests/          # Raw YAML files
    │   └── propeller-knowledge-root.yaml
    └── engineering/        # Raw YAML files
        └── knowledge-base/...
```

**Cache format rules:**
- ✅ Store raw YAML/JSON files only
- ✅ Metadata in standard JSON
- ✅ No language-specific serialization
- ✅ Each MCP builds own in-memory indexes
- ✅ Both can coexist, share cache

**User upgrade experience:**
```bash
# User starts with Node.js
npm install -g @p2kb/mcp-server

# Later, upgrade to Go (when ready)
npm uninstall -g @p2kb/mcp-server
brew install p2kb-mcp

# Cache intact, just faster!
# Same tools, same cache, 10x performance
```

### Why This Strategy Works

**1. Immediate Value**
- Users unblocked in days, not weeks
- Remote Claude instances work immediately
- Shared cache solves multi-project inefficiency

**2. Risk Mitigation**
- Real usage validates approach before major investment
- Learn which features actually matter
- Discover performance bottlenecks empirically
- Cache strategy proven before Go implementation

**3. Informed Design**
- Phase 1 usage data shows:
  - Most common queries
  - Performance bottlenecks
  - Feature priorities
  - Cache hit rates
- Phase 2 builds exactly what's needed

**4. Classic Lean/Agile**
- MVP first (solve core problem)
- Learn from real usage
- Invest in optimization when value proven
- Users get value at every stage

**5. No Breaking Changes**
- Same cache location
- Same tool names
- Go adds MORE tools, doesn't change existing
- Seamless migration

### Timeline

**Week 1-2: Build Node.js Minimal**
- Implement three core tools
- Test with real projects
- Document and release

**Week 3-4: Learn & Measure**
- Monitor usage patterns
- Profile performance
- Collect user feedback
- Identify feature priorities

**Week 5-8: Build Go Full-Featured**
- Core tools (compatible with Node.js)
- Advanced features (based on usage data)
- Performance optimization
- Cross-platform binaries

**Week 9: Production Release**
- Deprecate Node.js version (with migration guide)
- Release Go binaries
- Users upgrade seamlessly

### Communication to Users

**Phase 1 Announcement:**
> **P2 Knowledge Base MCP Now Available**
>
> Remote Claude Code instances can now access the P2 Knowledge Base!
>
> `npm install -g @p2kb/mcp-server`
>
> Features:
> - Download KB files from GitHub (no size limits)
> - Shared cache across all projects (~/.p2kb-cache/)
> - Automatic staleness detection
>
> Note: This is v1.0 focused on core functionality. Advanced features coming in v2.0.

**Phase 2 Announcement:**
> **P2KB MCP v2.0 - Production Release**
>
> Major performance upgrade + advanced features:
> - 10x faster startup, 5x lower memory
> - Rich semantic tools (instruction lookup, OBEX search)
> - Advanced features (cross-search, validation)
> - Cross-platform binaries (no Node.js needed)
>
> **Drop-in replacement** - uses your existing cache
>
> Migration: See docs/UPGRADE.md

### Potential Concerns & Solutions

**Concern: Two codebases temporarily?**
- ✅ Node.js deprecated after Go ships (~3 months overlap)
- ✅ Node.js is simple (~200 lines), minimal maintenance
- ✅ Clear transition plan

**Concern: User confusion about which to use?**
- ✅ Clear docs: "Node.js = quick start, Go = production"
- ✅ Deprecation notice in Node.js version after Go releases
- ✅ Migration guide with examples

**Concern: Wasted effort on Node.js?**
- ✅ Validates approach (not wasted)
- ✅ Unblocks users immediately (real value)
- ✅ Informs Go design (makes it better)
- ✅ Only ~3 days of work

**Concern: Breaking changes between versions?**
- ✅ Shared cache prevents this
- ✅ Same tool names (`p2kb__fetch_file`)
- ✅ Go is superset (adds tools, doesn't change existing)
- ✅ Tested migration path

---

### Path C: Go Minimal → Go Full-Featured (Skip Node.js)

**Strategy:** Build proper solution from the start, skip interim Node.js step

**Timeline:**
- Week 1-2: Go minimal (3 tools)
- Week 5-8: Go full-featured (expand tools)

#### Phase 1: Go Minimal MCP (Week 1-2)

**Goal:** Production-quality minimal MCP from day one

**What to build:**
- Same 3 tools as Node.js approach:
  - `p2kb__fetch_file`
  - `p2kb__check_updates`
  - `p2kb__clear_cache`
- Go implementation (~300-400 lines)
- Cross-platform binaries (macOS, Linux, Windows)
- Shared cache at `~/.p2kb-cache/`

**Why Go from the start:**
- ✅ **No throwaway code** - Node.js version becomes obsolete
- ✅ **Matches Todo MCP model** immediately
- ✅ **Better performance** from day one (5ms startup vs 100ms)
- ✅ **Smaller binaries** (2-5MB vs 50MB)
- ✅ **Single codebase** to maintain
- ✅ **You know Go** (built Todo MCP)

**Why skip Node.js:**
- ❌ Node.js Phase 1 becomes technical debt
- ❌ Two codebases to maintain (briefly)
- ❌ Users might not upgrade from Node.js to Go
- ❌ Extra migration work

**Implementation sketch:**
```go
// engineering/mcp-server/main.go
package main

import (
    "github.com/modelcontextprotocol/go-sdk/mcp"
)

func main() {
    server := mcp.NewServer("p2kb", "1.0.0")

    // Register 3 core tools
    server.AddTool("p2kb__fetch_file", fetchFileTool)
    server.AddTool("p2kb__check_updates", checkUpdatesTool)
    server.AddTool("p2kb__clear_cache", clearCacheTool)

    server.Run()
}

func fetchFileTool(args map[string]interface{}) (interface{}, error) {
    path := args["path"].(string)

    // Check cache
    if content, ok := getCachedFile(path); ok {
        return textContent(content), nil
    }

    // Download from GitHub
    content, err := downloadFile(path)
    if err != nil {
        return nil, err
    }

    // Cache and return
    cacheFile(path, content)
    return textContent(content), nil
}
```

**Build process:**
```bash
# Cross-compile for all platforms
GOOS=darwin GOARCH=amd64 go build -o p2kb-mcp-macos
GOOS=linux GOARCH=amd64 go build -o p2kb-mcp-linux
GOOS=windows GOARCH=amd64 go build -o p2kb-mcp-win.exe

# Upload to GitHub releases
gh release upload v1.0.0 p2kb-mcp-*
```

**Deliverable (Week 2):**
- Production-ready binaries (2-5MB each)
- Same 3 tools as Node.js approach
- Better performance
- Matches Todo MCP architecture

#### Phase 2: Go Full-Featured (Week 5-8)

**Goal:** Expand with semantic tools based on Phase 1 usage

**Add tools based on evidence:**
- `p2kb__get_instruction(mnemonic)` - If instruction lookup is common
- `p2kb__search_obex(keyword)` - If OBEX search is frequent
- `p2kb__get_smart_pin_mode(mode)` - If Smart Pin queries are repeated
- Advanced features only if validated by usage

**Benefits:**
- Same codebase, just more tools
- No migration needed (same binary name)
- Incremental improvement
- Evidence-based feature development

---

## Path Comparison

| Aspect | Path A: curl/wget | Path B: Node.js → Go | Path C: Go → Go |
|--------|------------------|---------------------|-----------------|
| **Time to users** | Hours | Days | 1-2 weeks |
| **Initial quality** | Basic | Good | Excellent |
| **Long-term solution** | No (interim only) | Yes | Yes |
| **Code to maintain** | None | 2 codebases briefly | 1 codebase |
| **Performance** | N/A | Node: OK, Go: Great | Great from start |
| **Binary size** | N/A | Node: 50MB, Go: 2-5MB | 2-5MB |
| **User migration** | curl → MCP | Node MCP → Go MCP | None needed |
| **Matches Todo MCP** | No | Eventually | Immediately |
| **Development effort** | None | Low + Medium | Medium |
| **Technical debt** | High (throwaway) | Low (Node deprecated) | None |

---

## Strategic Decision Matrix

**Choose Path A (curl/wget) if:**
- ✅ Need users working TODAY (hours not days)
- ✅ Want to validate approach before building
- ✅ Willing to accept inefficiency temporarily
- ✅ Want zero development effort now

**Choose Path B (Node.js → Go) if:**
- ✅ Want fastest MCP delivery (days not weeks)
- ✅ Comfortable with brief dual-codebase period
- ✅ Want to validate MCP approach quickly
- ✅ Prefer iterative development

**Choose Path C (Go → Go) if:**
- ✅ Can wait 1-2 weeks for proper solution
- ✅ Want production quality from day one
- ✅ Prefer single codebase to maintain
- ✅ Know Go well (like you do with Todo MCP)
- ✅ Want to match Todo MCP architecture immediately
- ✅ Avoid technical debt

**Hybrid Strategy: Path A + Path C**

**Recommended combination:**

**This Week (Path A):**
- Update CLAUDE.md to enable curl/wget (2 hours)
- Users unblocked immediately
- Zero development effort

**Week 1-2 (Path C Phase 1):**
- Build Go minimal MCP (3 tools)
- Ship production binaries
- Users upgrade when ready

**Week 5-8 (Path C Phase 2):**
- Expand Go MCP based on usage data
- Add semantic tools
- Advanced features

**Benefits:**
- ✅ Users working TODAY (curl/wget)
- ✅ No Node.js throwaway code
- ✅ Production quality when MCP ships
- ✅ Single migration (curl → Go MCP)
- ✅ Matches Todo MCP architecture

**Tradeoffs:**
- Users live with per-project cache for 1-2 weeks
- Then upgrade to shared cache with Go MCP
- No intermediate Node.js step

---

## Next Steps - APPROVED PLAN (Path B)

### Immediate (This Week)
1. **Design Node.js minimal API** - Three tools, simple interface
2. **Implement Node.js MCP** - ~200 lines, 2-3 days
3. **Test with real project** - Validate cache strategy
4. **Document and release** - npm package, setup guide

### Week 3-4 (Learning Phase)
1. **Monitor usage** - What queries are common?
2. **Profile performance** - Where are bottlenecks?
3. **Collect feedback** - What features do users need?
4. **Plan Go features** - Based on evidence, not speculation

### Week 5-8 (Go Implementation)
1. **Port core functionality** - Fetch, cache, updates
2. **Add semantic tools** - Only proven features
3. **Performance optimization** - Parsing, caching, indexing
4. **Cross-platform builds** - macOS, Linux, Windows binaries

### Week 9+ (Production Transition)
1. **Release Go v2.0** - With migration guide
2. **Deprecate Node.js** - Clear sunset timeline
3. **Support migration** - Help users upgrade
4. **Retire Node.js version** - Archive, redirect to Go

---

## Open Questions (To Be Answered in Phase 1)

- What is actual WebFetch size limit? (empirical testing needed)
- What are most common access patterns? (monitor real usage)
- Is Node.js performance acceptable? (profile in production)
- Which semantic tools add most value? (user feedback)
- What cache hit rate do we achieve? (measure effectiveness)
- Should we support version pinning? (e.g., lock to v1.4.0)

---

## Node.js Minimal MCP - API Specification

**Version:** 1.0.0 (Phase 1)
**Package:** `@p2kb/mcp-server`

### Core Tools (Three Functions)

#### 1. `p2kb__fetch_file`

**Purpose:** Download file from GitHub or return from cache

**Signature:**
```typescript
p2kb__fetch_file(path: string) -> string
```

**Parameters:**
- `path` (required): Relative path from repository root
  - Example: `"manifests/propeller-knowledge-root.yaml"`
  - Example: `"engineering/knowledge-base/P2/language/pasm2/add.yaml"`

**Returns:**
- Raw file content as string (YAML, JSON, or text)
- No parsing, no transformation

**Behavior:**
1. Check if file exists in cache: `~/.p2kb-cache/v{version}/{path}`
2. Check if cache is stale (compare metadata timestamp)
3. **If cached and fresh:** Return cached content
4. **If missing or stale:**
   - Download from: `https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/{path}`
   - Save to cache
   - Update metadata
   - Return content

**Error Handling:**
- 404 Not Found → Return error: `"File not found: {path}"`
- Network error → Return error: `"Network error: {details}"`
- Cache write error → Return error but include downloaded content

**Example Usage:**
```javascript
// Claude's workflow
const root_yaml = await p2kb__fetch_file("manifests/propeller-knowledge-root.yaml");
// Returns: "---\nmanifest_version: \"2.0\"\n..."

// Claude parses it
const root = YAML.parse(root_yaml);

// Navigate to next file
const pasm2_path = root.manifests.find(m => m.name === "pasm2").manifest;
const pasm2_yaml = await p2kb__fetch_file(pasm2_path);
```

---

#### 2. `p2kb__check_updates`

**Purpose:** Check if cached content is stale, prompt update if needed

**Signature:**
```typescript
p2kb__check_updates() -> object
```

**Parameters:** None

**Returns:**
```typescript
{
  "cache_version": "v1.4.0",           // Current cached version
  "cache_hash": "sha256:abc123...",    // Current cached hash
  "remote_hash": "sha256:def456...",   // Latest GitHub hash
  "needs_update": false,                // true if hashes differ
  "last_check": "2025-10-02T14:30:00Z", // ISO timestamp
  "cache_size_mb": 12.5,                // Total cache size
  "file_count": 2687                    // Files in cache
}
```

**Behavior:**
1. Fetch root manifest (small file, always fresh): `manifests/propeller-knowledge-root.yaml`
2. Extract `ai_instructions.content_hash` from root
3. Load local cache metadata: `~/.p2kb-cache/.metadata.json`
4. Compare hashes
5. Return status object

**Error Handling:**
- Network error → Return last known status with warning
- No cache → Return `needs_update: true`
- Corrupted metadata → Rebuild from cache directory scan

**Example Usage:**
```javascript
// Session start (automatic)
const status = await p2kb__check_updates();

if (status.needs_update) {
  console.log("KB updates available. Use p2kb__clear_cache() to refresh.");
}
```

---

#### 3. `p2kb__clear_cache`

**Purpose:** Force cache refresh on next fetch

**Signature:**
```typescript
p2kb__clear_cache(selective?: string) -> object
```

**Parameters:**
- `selective` (optional): Pattern to clear selectively
  - If omitted: Clear entire cache
  - If provided: Clear matching files only
  - Examples: `"manifests/*"`, `"*.yaml"`, `"pasm2/*"`

**Returns:**
```typescript
{
  "cleared": true,
  "files_removed": 2687,      // Count of files deleted
  "space_freed_mb": 12.5,     // MB freed
  "cache_path": "~/.p2kb-cache/v1.4.0"
}
```

**Behavior:**
1. **Full clear (no pattern):**
   - Delete `~/.p2kb-cache/v{version}/` directory
   - Preserve `~/.p2kb-cache/.metadata.json` (for version tracking)
   - Next fetch will re-download

2. **Selective clear (with pattern):**
   - Match files with glob pattern
   - Delete matching files only
   - Update metadata to mark as stale

**Error Handling:**
- Permission denied → Return error with details
- Cache doesn't exist → Return success (already clear)
- Partial failure → Return list of files that couldn't be deleted

**Example Usage:**
```javascript
// Full cache refresh
const result = await p2kb__clear_cache();
// Next p2kb__fetch_file will download fresh

// Selective refresh (just manifests)
const result = await p2kb__clear_cache("manifests/*");
// Only manifest files will re-download
```

---

### Cache Structure

```
~/.p2kb-cache/
├── .metadata.json          # Cache metadata
├── .lock                   # Prevent concurrent writes
└── v1.4.0/                 # Version-specific cache
    ├── manifests/
    │   ├── propeller-knowledge-root.yaml
    │   └── P2/
    │       └── language/
    │           └── pasm2-manifest.yaml
    └── engineering/
        └── knowledge-base/
            └── P2/
                └── language/
                    └── pasm2/
                        └── add.yaml
```

**`.metadata.json` format:**
```json
{
  "version": "v1.4.0",
  "content_hash": "sha256:56b39b658f0a2188b5f9dd2b19abc39c613c4fa5e9f94a7261b37cb1896297d1",
  "last_update": "2025-10-02T14:30:00Z",
  "last_check": "2025-10-02T18:45:00Z",
  "github_base": "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main",
  "file_count": 2687,
  "total_size_bytes": 13107200
}
```

**`.lock` file:**
- Simple lock file (touch to create, delete to release)
- Prevents concurrent cache writes from multiple Claude instances
- Max lock age: 60 seconds (auto-release if stale)

---

### Internal Implementation Notes

#### Download with Built-in HTTPS

```javascript
const https = require('https');
const fs = require('fs').promises;
const path = require('path');

async function downloadFile(url, destPath) {
  return new Promise((resolve, reject) => {
    https.get(url, (response) => {
      if (response.statusCode === 404) {
        reject(new Error('File not found'));
        return;
      }

      let data = '';
      response.on('data', chunk => data += chunk);
      response.on('end', async () => {
        try {
          await fs.mkdir(path.dirname(destPath), { recursive: true });
          await fs.writeFile(destPath, data, 'utf8');
          resolve(data);
        } catch (err) {
          reject(err);
        }
      });
    }).on('error', reject);
  });
}
```

#### Cache Staleness Check

```javascript
async function isCacheStale() {
  const metadata = await loadMetadata();

  // Fetch root manifest hash
  const rootUrl = 'https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/manifests/propeller-knowledge-root.yaml';
  const rootContent = await downloadFile(rootUrl, '/tmp/root-check.yaml');
  const root = YAML.parse(rootContent);
  const remoteHash = root.ai_instructions.content_hash;

  return metadata.content_hash !== remoteHash;
}
```

#### Lock Management

```javascript
const LOCK_FILE = path.join(CACHE_ROOT, '.lock');
const LOCK_TIMEOUT = 60000; // 60 seconds

async function acquireLock() {
  const lockExists = await fs.access(LOCK_FILE).then(() => true).catch(() => false);

  if (lockExists) {
    const stats = await fs.stat(LOCK_FILE);
    const age = Date.now() - stats.mtimeMs;

    if (age > LOCK_TIMEOUT) {
      // Stale lock, remove it
      await fs.unlink(LOCK_FILE);
    } else {
      throw new Error('Cache is locked by another process');
    }
  }

  await fs.writeFile(LOCK_FILE, String(process.pid));
}

async function releaseLock() {
  await fs.unlink(LOCK_FILE).catch(() => {});
}
```

---

### Configuration (Optional)

**Environment Variables:**
```bash
# Override cache location
P2KB_CACHE_DIR=~/my-custom-cache

# Override GitHub repository
P2KB_GITHUB_REPO=ironsheep/P2-Knowledge-Base

# Override branch (default: main)
P2KB_GITHUB_BRANCH=main

# Disable staleness checks (always use cache)
P2KB_OFFLINE_MODE=true
```

**Config file:** `~/.p2kb-config.json` (optional)
```json
{
  "cache_dir": "~/.p2kb-cache",
  "github_repo": "ironsheep/P2-Knowledge-Base",
  "github_branch": "main",
  "offline_mode": false,
  "auto_update_check": true
}
```

---

### Error Handling Philosophy

**Fail gracefully, prefer stale data over failure:**

1. **Network unavailable:** Use cached data (even if stale)
2. **Cache corrupted:** Re-download affected files
3. **Partial download failure:** Retry 3 times, then error
4. **Lock timeout:** Wait 60s, then force-acquire

**Error response format:**
```json
{
  "error": true,
  "message": "Network error: ECONNREFUSED",
  "fallback": "Using cached content (may be stale)",
  "details": "...",
  "timestamp": "2025-10-02T14:30:00Z"
}
```

---
