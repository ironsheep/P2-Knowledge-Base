-- P2KB Smart Pins - Front Matter Handler
-- Purpose: Handle EVERYTHING until Part I begins
-- Responsibilities:
--   - Demote headers strategically to work WITH style sheet page breaks
--   - Preserve visual weight of demoted headers
--   - Suppress metadata headers
--   - Transition to main matter at Part I
--   - Then STOPS processing (structure filter takes over)
--
-- Version: 2.1
-- Date: 2025-09-05
-- Changes: Demote Copyright/Version History to level 4 (subsection) instead of 3

local in_frontmatter = true
local seen_part_one = false
local in_preface = false
local metadata_headers_count = 0

function Header(header)
  -- Once we've seen Part I, this filter is done - let structure filter handle everything
  if seen_part_one then
    return header
  end
  
  local title = pandoc.utils.stringify(header)
  
  -- Suppress metadata headers (Version, Created date)
  if header.level == 3 then
    if title:match("^Version %d+%.%d+") or 
       title:match("^Created:") or
       title:match("Green Book Edition") or
       title:match("Image refresh") then
      metadata_headers_count = metadata_headers_count + 1
      -- Return empty to suppress these headers
      return {}
    end
  end
  
  -- Check for Part I - this ends front matter and this filter's job
  if header.level == 1 and title:match("^Part I") then
    seen_part_one = true  -- Mark that we're done
    in_frontmatter = false
    in_preface = false
    -- Insert command to switch from Roman to Arabic page numbering
    -- Let style sheet handle the clearpage for parts
    return {
      pandoc.RawBlock('latex', '\\mainmatter'),
      pandoc.RawBlock('latex', '\\setcounter{page}{1}'),
      header
    }
  end
  
  -- Special handling for "Chapter 1:" if it appears before Part I
  if header.level == 2 and title:match("^Chapter 1:") then
    in_frontmatter = false
    -- Insert command to switch to Arabic page numbering
    return {
      pandoc.RawBlock('latex', '\\mainmatter'),
      pandoc.RawBlock('latex', '\\setcounter{page}{1}'),
      header
    }
  end
  
  -- Handle front matter sections
  if in_frontmatter then
    -- Level 3 headers in frontmatter
    if header.level == 3 then
      if in_preface then
        -- Subsections within Preface - demote to level 4 to avoid section page breaks
        -- But preserve visual weight with formatting
        header.level = 4
        return {
          pandoc.RawBlock('latex', '{\\large\\bfseries'),  -- Make it look like a section
          header,
          pandoc.RawBlock('latex', '}')
        }
      end
      -- Other level 3 headers in frontmatter stay as-is
      return header
    end
    
    if header.level == 2 then
      -- Preface should remain a chapter to get its page break from style
      if title:match("^Preface:") or title:match("^Preface$") then
        in_preface = true  -- Mark that we're in Preface
        -- Keep as level 2 (chapter) - style sheet will handle page break
        return header
      end
      
      -- Executive Summary and Quick Start also stay as chapters
      if title:match("^Executive Summary") or title:match("^Quick Start") then
        in_preface = false  -- These end Preface
        -- Keep as level 2 (chapter) - style sheet will handle page break
        return header
      end
      
      -- All other level 2 headers in frontmatter (Copyright, Version History, etc.)
      -- Demote to level 4 (subsection) to avoid ALL page breaks
      -- But preserve visual weight
      header.level = 4
      return {
        pandoc.RawBlock('latex', '{\\Large\\bfseries'),  -- Make it look like a chapter
        header,
        pandoc.RawBlock('latex', '}\\vspace{0.5em}')  -- Add some space after
      }
    end
  end
  
  return header
end

-- Process horizontal rules (---)
function HorizontalRule()
  -- Suppress ALL horizontal rules in front matter
  if in_frontmatter then
    return {}  -- Suppress all HRs before Part I
  end
  return nil  -- Keep HRs in main matter
end

-- Don't insert frontmatter here - let the template handle it
-- The template should have \frontmatter before \tableofcontents