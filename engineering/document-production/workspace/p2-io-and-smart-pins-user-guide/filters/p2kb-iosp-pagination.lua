-- P2KB IOSP Reference Manual - Pagination Filter
-- Purpose: Handles Part/Chapter structure and page breaks
--
-- Behavior:
-- - "# Part X" → \manualpart{} (own page, adds to TOC)
-- - First chapter after Part → NO page break (stays on Part page)
-- - Subsequent chapters → page break before
-- - "# Instructions: X" treated as chapters
-- - "# Assembler Directives", "# Special Registers" treated as chapters
--
-- Version: 2.0 - Proper Part/Chapter/TOC handling
-- Date: 2025-12-04

-- Track if this is the first chapter (to avoid clearpage right after TOC)
local first_chapter = true

-- Track if we just emitted a Part (next chapter stays on same page)
local just_emitted_part = false

-- Helper: Check if title represents a chapter-level heading
local function is_chapter_heading(title)
  return title:match("^Chapter") or
         title:match("^Appendix") or
         title:match("^Instructions:") or
         title:match("^Assembler Directives") or
         title:match("^Special Registers") or
         title:match("^Preface") or
         title:match("^Copyright") or
         title:match("^Dedication") or
         title:match("^Acknowledgments") or
         title:match("Quick Reference") or
         title:match("^Index")
end

-- Handle Header elements for page breaks and Part conversion
function Header(header)
  local title = pandoc.utils.stringify(header.content)

  -- Level 1 headers need special handling
  if header.level == 1 then

    -- Part headings → \manualpart{} (adds to TOC, own page, no break after)
    if title:match("^Part ") then
      local manualpart = pandoc.RawBlock('latex', '\\manualpart{' .. title .. '}')
      just_emitted_part = true
      return manualpart
    end

    -- Chapter-level headings
    if is_chapter_heading(title) then
      -- Skip clearpage for the very first chapter (right after TOC)
      if first_chapter then
        first_chapter = false
        return header
      end

      -- Skip clearpage for chapter immediately after a Part
      if just_emitted_part then
        just_emitted_part = false
        return header
      end

      -- All other chapters get page breaks before
      local pagebreak = pandoc.RawBlock('latex', '\\clearpage')
      return {pagebreak, header}
    end
  end

  -- Any non-Part header clears the just_emitted_part flag
  just_emitted_part = false

  -- Level 2 and below: no automatic page breaks
  return header
end
