-- Smart Pins Complete Page Break and Numbering Control
-- This filter manages ALL page breaks and numbering changes
-- 
-- Page Break Rules:
-- 1. Parts always start on new page
-- 2. First chapter after part: same page as part
-- 3. All other chapters: new page
-- 4. Executive Summary: new page
-- 5. Quick Start Guide: new page
-- 6. Each Mode (%xxxxx): new page (but first mode after chapter: same page)
-- 7. Each Appendix: new page
-- 8. Index: new page
--
-- Numbering Control:
-- - Start with secnumdepth=-1 (no numbering)
-- - Chapter 1: set to 1 (number chapters and sections)
-- - Part II: set to 0 (only chapters numbered, not modes)
-- - Part III+: back to 1

local after_part = false
local after_mode_chapter = false
local in_frontmatter = true
local in_mode_reference = false
local current_part = 0

function Header(elem)
  local title = pandoc.utils.stringify(elem)
  local needs_pagebreak = false
  local reason = ""
  local blocks_to_add = {}
  
  -- DEBUG: Always show what we're processing
  table.insert(blocks_to_add, pandoc.RawInline('latex', 
    string.format('%% LUA: Level %d - "%s"', elem.level, title)))
  
  -- PART HANDLING (Level 1)
  if elem.level == 1 then
    current_part = current_part + 1
    needs_pagebreak = true
    reason = "Part detected"
    after_part = true
    
    -- Check which part this is
    if title:match("Part II") or title:match("Mode Reference") then
      in_mode_reference = true
      in_frontmatter = false
      -- Part II: Only chapters numbered, not sections
      table.insert(blocks_to_add, pandoc.RawInline('latex', 
        '\\setcounter{secnumdepth}{0}% Part II: Only chapters numbered'))
    elseif title:match("Part III") or title:match("Part IV") then
      in_mode_reference = false
      in_frontmatter = false
      -- Parts III, IV: Back to normal numbering
      table.insert(blocks_to_add, pandoc.RawInline('latex', 
        '\\setcounter{secnumdepth}{1}% Parts III/IV: Sections numbered'))
    end
    
  -- CHAPTER HANDLING (Level 2)
  elseif elem.level == 2 then
    
    -- Special front matter sections (always new page)
    if title:match("^Executive Summary") then
      needs_pagebreak = true
      reason = "Executive Summary"
      after_part = false
      in_frontmatter = true
      -- Keep numbering off (already -1)
      
    elseif title:match("^Quick Start") then
      needs_pagebreak = true
      reason = "Quick Start Guide"
      after_part = false
      in_frontmatter = true
      -- Keep numbering off (already -1)
      
    -- Chapter 1: Turn numbering ON
    elseif title:match("^Chapter 1:") then
      in_frontmatter = false
      table.insert(blocks_to_add, pandoc.RawInline('latex', 
        '\\setcounter{secnumdepth}{1}% Chapter 1: Start numbering sections'))
      
      if after_part then
        needs_pagebreak = false
        reason = "First chapter after part - same page"
        after_part = false
      else
        needs_pagebreak = true
        reason = "Regular chapter"
      end
      
    -- Mode chapters in Part II
    elseif in_mode_reference and title:match("Modes") then
      after_mode_chapter = true  -- Set flag for first mode
      needs_pagebreak = true
      reason = "Mode chapter"
      
    -- Appendices (always new page)
    elseif title:match("^Appendix") then
      needs_pagebreak = true
      reason = "Appendix section"
      after_part = false
      -- Force into TOC
      table.insert(blocks_to_add, pandoc.RawInline('latex', 
        string.format('\\addcontentsline{toc}{chapter}{%s}', title)))
      
    -- Index (always new page)
    elseif title:match("^Index") or title:match("^About") then
      needs_pagebreak = true
      reason = "Index/About section"
      after_part = false
      -- Force into TOC
      table.insert(blocks_to_add, pandoc.RawInline('latex', 
        string.format('\\addcontentsline{toc}{chapter}{%s}', title)))
      
    -- Regular chapters
    else
      if after_part then
        -- First chapter after part: no page break
        needs_pagebreak = false
        reason = "First chapter after part - same page"
        after_part = false
      else
        -- All other chapters: new page
        needs_pagebreak = true
        reason = "Regular chapter"
      end
    end
    
  -- SECTION HANDLING (Level 3)
  elseif elem.level == 3 then
    
    -- Sections in frontmatter - force into TOC
    if in_frontmatter then
      table.insert(blocks_to_add, pandoc.RawInline('latex', 
        string.format('\\addcontentsline{toc}{section}{%s}', title)))
      reason = "Frontmatter section - forced to TOC"
    
    -- Smart Pin Modes in Part II
    elseif in_mode_reference and (title:match("^Mode `?%%") or title:match("^Mode %%")) then
      if after_mode_chapter then
        needs_pagebreak = false
        reason = "First mode after chapter - same page"
        after_mode_chapter = false
      else
        needs_pagebreak = true
        reason = "Smart Pin Mode section"
      end
      -- Force mode into TOC (unnumbered)
      table.insert(blocks_to_add, pandoc.RawInline('latex', 
        string.format('\\addcontentsline{toc}{section}{%s}', title)))
      
    -- Other special level 3 sections that might need breaks
    elseif title:match("^Appendix") then
      needs_pagebreak = true
      reason = "Appendix subsection"
      after_part = false
      table.insert(blocks_to_add, pandoc.RawInline('latex', 
        string.format('\\addcontentsline{toc}{section}{%s}', title)))
    end
    
  end
  
  -- Apply page break if needed
  if needs_pagebreak then
    table.insert(blocks_to_add, pandoc.RawInline('latex', 
      string.format('%% LUA: Adding \\clearpage (%s)', reason)))
    table.insert(blocks_to_add, pandoc.RawInline('latex', '\\clearpage'))
  else
    table.insert(blocks_to_add, pandoc.RawInline('latex', 
      string.format('%% LUA: No break (%s)', reason)))
  end
  
  -- Add all blocks before the header
  for _, block in ipairs(blocks_to_add) do
    table.insert(blocks_to_add, block)
  end
  table.insert(blocks_to_add, elem)
  
  return blocks_to_add
end

-- Also handle any raw LaTeX \chapter commands that might slip through
function RawBlock(elem)
  if elem.format == "latex" then
    -- Remove any \clearpage commands that aren't ours
    if elem.text:match("^\\clearpage") and not elem.text:match("LUA:") then
      local warning = pandoc.RawBlock('latex', 
        '% LUA: Removed unwanted \\clearpage from LaTeX')
      return warning
    end
  end
  return elem
end

return {
  {Header = Header},
  {RawBlock = RawBlock}
}