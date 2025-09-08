-- P2KB Smart Pins - Index TOC Management
-- Purpose: Handle Index section in TOC properly
-- 1. Convert "# Index" to chapter level so it appears in TOC
-- 2. Prevent index letter sections (A, B, C...) from appearing in TOC
--
-- Version: 1.0
-- Date: 2025-09-07

local in_index = false
local index_found = false

function Header(header)
  local title = pandoc.utils.stringify(header)
  
  -- Check if this is the Index heading
  if header.level == 1 and title == "Index" then
    in_index = true
    index_found = true
    -- Convert to level 2 (chapter) so it appears in TOC
    header.level = 2
    return header
  end
  
  -- If we're in the Index section
  if in_index then
    -- Check for single letter headings (A, B, C, etc.)
    if header.level == 3 and title:match("^%u$") then
      -- Keep as section but prevent from appearing in TOC
      -- We do this by wrapping in raw LaTeX that suppresses TOC entry
      return {
        pandoc.RawBlock('latex', '\\addtocontents{toc}{\\protect\\setcounter{tocdepth}{1}}'),
        header,
        pandoc.RawBlock('latex', '\\addtocontents{toc}{\\protect\\setcounter{tocdepth}{2}}')
      }
    end
  end
  
  return header
end