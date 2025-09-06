-- P2KB Smart Pins - Fix Hypertarget Issues
-- Purpose: Selectively fix hypertarget issues while preserving TOC links
-- Only removes problematic identifiers that cause bracket duplication
--
-- Version: 1.3
-- Date: 2025-09-05
-- Changes: Clear ALL attributes on Parts to prevent bracket issues

function Header(header)
  local title = pandoc.utils.stringify(header)
  
  -- Only remove identifiers for Part headers (level 1)
  -- These are causing the [Part I:]Part I: duplication
  if header.level == 1 and title:match("^Part ") then
    header.identifier = ""
    -- Also clear ALL attributes to prevent any bracket issues
    header.attributes = {}
    header.classes = {}
  end
  
  -- Leave all other headers alone so TOC links work
  return header
end