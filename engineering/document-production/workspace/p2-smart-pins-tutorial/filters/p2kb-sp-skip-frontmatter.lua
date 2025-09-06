-- P2KB Smart Pins - Skip Frontmatter Filter
-- Purpose: Skip processing headers until we reach "Part I"
-- This prevents title/subtitle from being treated as Parts/Chapters
--
-- Version: 1.0
-- Date: 2025-09-04

local found_part_one = false

function Header(header)
  local title = pandoc.utils.stringify(header.content)
  
  -- Check if this is "Part I" - the start of real content
  if title:match("^Part I:") or title:match("^Part I ") then
    found_part_one = true
    -- Let this header through normally
    return header
  end
  
  -- If we haven't found Part I yet, demote these headers to prevent processing
  if not found_part_one then
    -- Demote the header by increasing its level (max level is 6)
    if header.level < 6 then
      header.level = header.level + 3  -- Demote by 3 levels
    end
    return header
  end
  
  -- After Part I, process normally
  return header
end