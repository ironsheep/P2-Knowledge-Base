-- P2KB DeSilva - Pagination Filter (Chapter-based document)
-- Purpose: ONLY handles page breaks between Chapters and special sections
-- No code block processing - single responsibility
--
-- Version: 1.1 - Updated for chapter-based document (no Parts)
-- Date: 2025-11-24

-- Track if this is the first chapter (to avoid clearpage right after TOC)
local first_chapter = true

-- Handle Header elements for page breaks
function Header(header)
  local title = pandoc.utils.stringify(header.content)

  -- Level 1 headers are Chapters with --top-level-division=chapter
  if header.level == 1 then
    -- Check for chapter, appendix, or special sections
    if title:match("^Chapter") or title:match("^Appendix") or
       title:match("^Preface") or title:match("^Copyright") or
       title:match("^Dedication") or title:match("^Acknowledgments") or
       title:match("Quick Reference") or title:match("^Index") then

      -- Skip clearpage for the very first chapter (right after TOC)
      if first_chapter then
        first_chapter = false
        return header  -- No page break for first header
      end

      -- All other chapters/appendices get page breaks
      local pagebreak = pandoc.RawBlock('latex', '\\clearpage')
      return {pagebreak, header}
    end
  end

  -- Level 2 and below: no automatic page breaks (sections flow within chapters)
  return header
end
