-- Smart Pins Complete Page Break and Numbering Control
-- This filter manages page breaks AND section numbering
-- 
-- Page Break Rules:
-- 1. Parts always start on new page
-- 2. First chapter after part: same page as part
-- 3. All other chapters: new page
-- 4. Executive Summary: new page
-- 5. Quick Start Guide: new page
-- 6. NO page breaks for sections (modes, etc) - let them flow
-- 7. Each Appendix: new page
-- 8. Index: new page
--
-- Numbering Rules:
-- - Chapters 1-4: Section numbering ON (1.1, 1.2, etc.)
-- - Chapters 5-12 (Modes): Section numbering OFF
-- - Chapters 13-15: Section numbering ON
-- - Appendices, Index, About: Section numbering OFF

local after_part = false
local after_mode_chapter = false
local in_frontmatter = true
local in_mode_reference = false
local in_appendix = false
local current_part = 0
local chapter_number = 0
local numbering_on = false

-- Helper function to escape LaTeX special characters
local function escape_latex(str)
  -- Escape special LaTeX characters
  str = str:gsub("%%", "\\%%")
  str = str:gsub("#", "\\#")
  str = str:gsub("%$", "\\$")
  str = str:gsub("&", "\\&")
  str = str:gsub("_", "\\_")
  str = str:gsub("%^", "\\^{}")
  str = str:gsub("~", "\\~{}")
  str = str:gsub("{", "\\{")
  str = str:gsub("}", "\\}")
  return str
end

function Header(elem)
  local title = pandoc.utils.stringify(elem)
  local escaped_title = escape_latex(title)
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
    
    -- Check which part this is for tracking purposes
    if title:match("Part II") or title:match("Mode Reference") then
      in_mode_reference = true
      in_frontmatter = false
    elseif title:match("Part III") or title:match("Part IV") then
      in_mode_reference = false
      in_frontmatter = false
    end
    -- NO numbering changes - keep at -1
    
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
      
    -- Chapter 1 (and all numbered chapters)
    elseif title:match("^Chapter (%d+):") then
      in_frontmatter = false
      
      -- Extract chapter number
      local ch_num = tonumber(title:match("^Chapter (%d+):"))
      chapter_number = ch_num
      
      -- Control section numbering based on chapter
      if ch_num >= 1 and ch_num <= 3 then
        -- Chapters 1-3: Turn ON section numbering
        if not numbering_on then
          table.insert(blocks_to_add, pandoc.RawInline('latex', 
            '\\setcounter{secnumdepth}{3}% Turn on section numbering for Chapters 1-3'))
          numbering_on = true
        end
      elseif ch_num >= 4 and ch_num <= 12 then
        -- Chapters 4-12 (Mode chapters): Turn OFF section numbering
        if numbering_on then
          table.insert(blocks_to_add, pandoc.RawInline('latex', 
            '\\setcounter{secnumdepth}{-1}% Turn off section numbering for Mode chapters'))
          numbering_on = false
        end
      elseif ch_num >= 13 and ch_num <= 15 then
        -- Chapters 13-15: Turn ON section numbering
        if not numbering_on then
          table.insert(blocks_to_add, pandoc.RawInline('latex', 
            '\\setcounter{secnumdepth}{3}% Turn on section numbering for Chapters 13-15'))
          numbering_on = true
        end
      end
      
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
      
    -- Appendices at chapter level only (always new page)
    -- Match "Appendix A:" but not subsections like "A.1" 
    elseif title:match("^Appendix [A-Z]:") then
      needs_pagebreak = true
      reason = "Appendix chapter"
      after_part = false
      in_appendix = true  -- Mark that we're in an appendix
      
      -- Turn OFF section numbering for appendices
      if numbering_on then
        table.insert(blocks_to_add, pandoc.RawInline('latex', 
          '\\setcounter{secnumdepth}{-1}% Turn off section numbering for Appendices'))
        numbering_on = false
      end
      
    -- Index (always new page)
    elseif title:match("^Index") or title:match("^About") then
      needs_pagebreak = true
      reason = "Index/About section"
      after_part = false
      in_appendix = false  -- No longer in appendix
      
      -- Turn OFF section numbering for Index/About
      if numbering_on then
        table.insert(blocks_to_add, pandoc.RawInline('latex', 
          '\\setcounter{secnumdepth}{-1}% Turn off section numbering for Index/About'))
        numbering_on = false
      end
      
    -- Regular chapters
    else
      in_appendix = false  -- Regular chapters are not appendices
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
    
  -- SECTION HANDLING (Level 3 and below)
  elseif elem.level >= 3 then
    
    -- ABSOLUTELY NO PAGE BREAKS FOR SECTIONS - let them flow naturally
    needs_pagebreak = false
    reason = "Section/subsection - no page break"
    
    -- Extra confirmation for appendix sections
    if in_appendix then
      reason = "Appendix section - definitely no page break, let flow with tables"  
    end
    
    -- Sections in frontmatter - force into TOC
    if in_frontmatter and elem.level == 3 then
      -- Don't add to TOC - Pandoc handles this
      -- table.insert(blocks_to_add, pandoc.RawInline('latex', 
      --   string.format('\\addcontentsline{toc}{section}{%s}', escaped_title)))
      reason = "Frontmatter section - forced to TOC, no page break"
    
    -- Smart Pin Modes in Part II - force into TOC but no page breaks
    elseif in_mode_reference and elem.level == 3 and (title:match("^Mode `?%%") or title:match("^Mode %%")) then
      reason = "Smart Pin Mode - no page break, flows naturally"
      -- Don't add to TOC - Pandoc handles this
      -- table.insert(blocks_to_add, pandoc.RawInline('latex', 
      --   string.format('\\addcontentsline{toc}{section}{%s}', escaped_title)))
    end
    -- NO SPECIAL CASES - NO PAGE BREAKS FOR ANY SECTIONS
    
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
  
  -- Return all blocks including the header
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