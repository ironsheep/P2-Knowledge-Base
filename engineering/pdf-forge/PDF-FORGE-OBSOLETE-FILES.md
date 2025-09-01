# PDF Forge - Obsolete Files to Remove

**Purpose**: Track files that have been renamed/replaced and can be deleted from PDF Forge

## 2025-08-29 Cleanup Required

### Obsolete Lua Filters (replaced by smart-pins-colored-blocks.lua)
These can be deleted from PDF Forge `/workspace/filters/`:
- [ ] `smart-pins-block-coloring.lua` → REPLACED BY `smart-pins-colored-blocks.lua`
- [ ] `smart-pins-four-color-final.lua` → REPLACED BY `smart-pins-colored-blocks.lua`
- [ ] `smart-pins-config-blue-v2.lua` → Old iteration, no longer needed

### Reason for Changes
- **smart-pins-colored-blocks.lua** is the new consolidated filter that handles:
  - Configuration blocks (blue)
  - Spin2 blocks (green)
  - PASM2 blocks (yellow)
  - Antipattern blocks (red)
  - Decision tree boxes
  - Page break logic

## Cleanup Protocol
1. Deploy new files first
2. Test that new files work
3. Delete obsolete files from Forge
4. Check this document and mark items as deleted
5. Clear completed items from this list monthly

## History
- 2025-08-29: Renamed `smart-pins-block-coloring.lua` to `smart-pins-colored-blocks.lua` for clarity