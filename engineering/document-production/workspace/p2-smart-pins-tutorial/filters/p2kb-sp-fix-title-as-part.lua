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
  if header.level == 1 and is_first_h1 then
    is_first_h1 = false
    -- Demote to level 3 so it doesn't become a \part
    header.level = 3
    -- Add some formatting to make it look like a title
    return {
      pandoc.RawBlock('latex', '\\begin{center}'),
      pandoc.RawBlock('latex', '{\\Huge\\bfseries'),
      header,
      pandoc.RawBlock('latex', '}'),
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