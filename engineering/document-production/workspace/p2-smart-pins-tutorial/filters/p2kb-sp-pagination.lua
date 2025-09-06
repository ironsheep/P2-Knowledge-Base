-- P2KB Smart Pins - Pagination Filter
-- Purpose: ONLY handles page breaks between Parts, Chapters, and Appendices
-- No code block processing - single responsibility
--
-- Version: 1.1 - Fixed double clearpage after TOC
-- Date: 2025-09-04

-- Track if we just saw a Part header to avoid double page breaks
local just_saw_part = false
-- Track if this is the first header (to avoid clearpage right after TOC)
local first_header = true

-- Handle Header elements for page breaks
function Header(header)
  local title = pandoc.utils.stringify(header.content)
  
  -- Level 1 headers (Parts, Quick Reference, Index) always get page breaks
  if header.level == 1 then
    -- Skip clearpage for the very first header (right after TOC)
    if first_header then
      first_header = false
      -- Mark that we just saw a Part if applicable
      if title:match("^Part") then
        just_saw_part = true
      else
        just_saw_part = false
      end
      return header  -- No page break for first header
    end
    
    local pagebreak = pandoc.RawBlock('latex', '\\clearpage')
    -- Mark that we just saw a Part
    if title:match("^Part") then
      just_saw_part = true
    else
      just_saw_part = false
    end
    return {pagebreak, header}
  
  -- Level 2 headers - check for specific patterns
  elseif header.level == 2 then
    -- Check if it's Preface (always gets page break)
    if title:match("^Preface") then
      just_saw_part = false
      local pagebreak = pandoc.RawBlock('latex', '\\clearpage')
      return {pagebreak, header}
    -- Check if it's a chapter or appendix
    elseif title:match("^Chapter") or title:match("^Appendix") then
      -- Skip page break if this is the first chapter/appendix after a Part
      if just_saw_part then
        just_saw_part = false  -- Reset flag
        return header  -- No page break
      else
        -- Normal chapter/appendix - gets page break
        local pagebreak = pandoc.RawBlock('latex', '\\clearpage')
        return {pagebreak, header}
      end
    -- Other level 2 headers that need page breaks
    elseif title:match("^Part") or
           title:match("Quick Reference") or
           title:match("^Index") then
      just_saw_part = false  -- Reset flag
      local pagebreak = pandoc.RawBlock('latex', '\\clearpage')
      return {pagebreak, header}
    end
  end
  
  -- Any other header type resets the flag
  just_saw_part = false
  return header
end