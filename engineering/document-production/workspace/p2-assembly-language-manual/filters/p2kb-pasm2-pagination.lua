-- P2KB DeSilva - Pagination Filter (Chapter-based document)
-- Purpose: ONLY handles page breaks between Chapters and special sections
-- No code block processing - single responsibility
--
-- Version: 1.3 - Part and first chapter stay on same page
-- Date: 2025-12-02

-- Track if this is the first chapter (to avoid clearpage right after TOC)
local first_chapter = true

-- Track if we just emitted a Part divider (next chapter stays on same page)
local just_emitted_part = false

-- Handle Header elements for page breaks
function Header(header)
  local title = pandoc.utils.stringify(header.content)

  -- Level 1 headers are Chapters with --top-level-division=chapter
  if header.level == 1 then

    -- Part headings get special treatment: use \partdivider command
    -- This prevents the page break AFTER the part heading
    if title:match("^Part ") then
      -- Convert Part heading to custom LaTeX command
      local partdivider = pandoc.RawBlock('latex', '\\partdivider{' .. title .. '}')
      just_emitted_part = true
      return partdivider
    end

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

      -- Skip clearpage for chapter immediately after a Part divider
      if just_emitted_part then
        just_emitted_part = false
        return header  -- No page break - stay on same page as Part
      end

      -- All other chapters/appendices get page breaks
      local pagebreak = pandoc.RawBlock('latex', '\\clearpage')
      return {pagebreak, header}
    end
  end

  -- Any other header clears the just_emitted_part flag
  just_emitted_part = false

  -- Level 2 and below: no automatic page breaks (sections flow within chapters)
  return header
end
