-- P2KB Smart Pins - Index Letter TOC Suppression
-- Purpose: Prevent index letter sections (A, B, C...) from appearing in TOC
-- These are single uppercase letter headings used to organize index entries
--
-- Version: 1.3
-- Date: 2025-12-03

function Header(header)
  local title = pandoc.utils.stringify(header)

  -- Check for single uppercase letter headings (A, B, C, etc.)
  -- These are index letter dividers - keep them in document but exclude from TOC
  if title:match("^%u$") then
    -- Convert to unnumbered section (section* doesn't appear in TOC)
    return pandoc.RawBlock('latex', '\\section*{' .. title .. '}')
  end

  return header
end