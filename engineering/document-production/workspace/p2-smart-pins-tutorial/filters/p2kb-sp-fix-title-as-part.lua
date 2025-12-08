-- P2KB Smart Pins - Fix Title Being Treated as Part
-- Purpose: The first level 1 header is the document title, not a part
-- Demote it so it doesn't become \part{} in LaTeX
--
-- Version: 1.0
-- Date: 2025-09-04

local is_first_h1 = true
local is_first_h2 = true

function Header(header)
  -- The first level 1 header is the document title
  -- BUT: Skip if it's a "Part" header - those are real parts, not titles
  if header.level == 1 and is_first_h1 then
    local title = pandoc.utils.stringify(header)

    -- Don't treat Part headers as document title - let them be real \part{}
    if title:match("^Part ") then
      -- This is a Part header, not a title - pass through unchanged
      -- Part-structured documents don't have title/subtitle, so disable both
      is_first_h1 = false
      is_first_h2 = false  -- Prevent next H2 from being treated as subtitle
      return header
    end

    is_first_h1 = false
    -- Escape LaTeX special characters
    local escaped_title = title:gsub('&', '\\&')
    -- Don't change the level, but replace with custom formatting
    -- that doesn't trigger \part but adds a TOC entry like a chapter
    return {
      pandoc.RawBlock('latex', '\\addcontentsline{toc}{chapter}{' .. escaped_title .. '}'),
      pandoc.RawBlock('latex', '\\begin{center}'),
      pandoc.RawBlock('latex', '{\\Huge\\bfseries ' .. escaped_title .. '}'),
      pandoc.RawBlock('latex', '\\end{center}'),
      pandoc.RawBlock('latex', '\\vspace{1em}')
    }
  end
  
  -- The first level 2 header after the title is the subtitle
  if header.level == 2 and is_first_h2 and not is_first_h1 then
    is_first_h2 = false
    -- Demote to level 4 so it doesn't become a \chapter
    header.level = 4
    -- Add some formatting to make it look like a subtitle
    return {
      pandoc.RawBlock('latex', '\\begin{center}'),
      pandoc.RawBlock('latex', '{\\Large\\itshape'),
      header,
      pandoc.RawBlock('latex', '}'),
      pandoc.RawBlock('latex', '\\end{center}'),
      pandoc.RawBlock('latex', '\\vspace{2em}')
    }
  end
  
  return header
end