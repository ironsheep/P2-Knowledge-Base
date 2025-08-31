-- Part-Chapter Page Break Control Lua Filter
-- Manages page breaks between Parts (level 1 headers) and Chapters (level 2 headers)
-- 
-- Logic: 
-- - Front matter sections: each gets own page
-- - Part I: new page, Chapter 1: same page, Chapter 2: new page
-- - Part II: new page, Chapter 3: same page, Chapter 4: new page
--   Special: First mode flows with chapter, subsequent modes new page
-- - Appendices: each gets own page

local after_part = false
local in_part_two = false
local after_chapter_in_part_two = false
local in_front_matter = true

function Header(elem)
  local header_text = pandoc.utils.stringify(elem)
  -- DEBUG: Always insert a comment showing we processed this header
  local debug_comment = pandoc.RawInline('latex', '% LUA FILTER: Processing header level ' .. elem.level .. ' - ' .. header_text)
  
  if elem.level == 1 then
    -- Level 1 = Part or front matter sections (Pandoc converts to \chapter{})
    
    -- Check for front matter sections
    if header_text:match("Executive Summary") or header_text:match("Quick Start") then
      if in_front_matter then
        local fm_comment = pandoc.RawInline('latex', '% LUA FILTER: Front matter section - inserting \\clearpage')
        local pagebreak = pandoc.RawInline('latex', '\\clearpage')
        return {debug_comment, fm_comment, pagebreak, elem}
      end
    end
    
    -- Check for Parts
    if header_text:match("Part I[^I]") or header_text:match("Part 1") then
      in_front_matter = false
      in_part_two = false
      after_part = true
      local part_comment = pandoc.RawInline('latex', '% LUA FILTER: Part I detected - inserting \\clearpage')
      local pagebreak = pandoc.RawInline('latex', '\\clearpage')
      return {debug_comment, part_comment, pagebreak, elem}
      
    elseif header_text:match("Part II") or header_text:match("Part 2") then
      in_front_matter = false
      in_part_two = true
      after_part = true
      local part_comment = pandoc.RawInline('latex', '% LUA FILTER: Part II detected - inserting \\clearpage')
      local pagebreak = pandoc.RawInline('latex', '\\clearpage')
      return {debug_comment, part_comment, pagebreak, elem}
      
    elseif header_text:match("Part III") or header_text:match("Part 3") then
      in_front_matter = false
      in_part_two = false
      after_part = true
      local part_comment = pandoc.RawInline('latex', '% LUA FILTER: Part III detected - inserting \\clearpage')
      local pagebreak = pandoc.RawInline('latex', '\\clearpage')
      return {debug_comment, part_comment, pagebreak, elem}
    end
    
    -- Check for Appendices
    if header_text:match("Appendix") then
      in_front_matter = false
      in_part_two = false
      local app_comment = pandoc.RawInline('latex', '% LUA FILTER: Appendix detected - inserting \\clearpage')
      local pagebreak = pandoc.RawInline('latex', '\\clearpage')
      return {debug_comment, app_comment, pagebreak, elem}
    end
    
  elseif elem.level == 2 then
    -- Level 2 = Chapter (Pandoc converts to \section{})
    -- Conditional page break: first chapter after part stays on same page
    
    if after_part then
      -- First chapter after part: no page break, reset flag
      after_part = false
      if in_part_two then
        after_chapter_in_part_two = true  -- Mark that we're in first chapter of Part II
      end
      local chapter_comment = pandoc.RawInline('latex', '% LUA FILTER: First chapter after part - NO pagebreak')
      return {debug_comment, chapter_comment, elem}
    else
      -- Subsequent chapters: force page break
      if in_part_two then
        after_chapter_in_part_two = true  -- Reset for new chapter in Part II
      end
      local chapter_comment = pandoc.RawInline('latex', '% LUA FILTER: Subsequent chapter - inserting \\clearpage')
      local pagebreak = pandoc.RawInline('latex', '\\clearpage')
      return {debug_comment, chapter_comment, pagebreak, elem}
    end
    
  elseif elem.level == 3 and in_part_two then
    -- Level 3 in Part II = Mode sections (Pandoc converts to \subsection{})
    
    if header_text:match("Mode") then
      if after_chapter_in_part_two then
        -- First mode after chapter in Part II: no page break
        after_chapter_in_part_two = false
        local mode_comment = pandoc.RawInline('latex', '% LUA FILTER: First mode in Part II chapter - NO pagebreak')
        return {debug_comment, mode_comment, elem}
      else
        -- Subsequent modes: page break
        local mode_comment = pandoc.RawInline('latex', '% LUA FILTER: Subsequent mode in Part II - inserting \\clearpage')
        local pagebreak = pandoc.RawInline('latex', '\\clearpage')
        return {debug_comment, mode_comment, pagebreak, elem}
      end
    end
  end
  
  -- Other header levels unchanged
  return elem
end