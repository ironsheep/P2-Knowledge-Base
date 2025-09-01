-- Part-Chapter Page Break Control Lua Filter
-- Manages page breaks between Parts (level 1 headers) and Chapters (level 2 headers)
-- 
-- Logic: 
-- - Part I: new page, Chapter 1: same page 
-- - Chapter 2: new page
-- - Part II: new page, Chapter 3: same page
-- - Chapter 4: new page

local after_part = false

function Header(elem)
  -- DEBUG: Always insert a comment showing we processed this header
  local debug_comment = pandoc.RawInline('latex', '% LUA FILTER: Processing header level ' .. elem.level .. ' - ' .. pandoc.utils.stringify(elem))
  
  if elem.level == 1 then
    -- Level 1 = Part (Pandoc converts to \chapter{})
    -- Always start parts on new page and set flag
    after_part = true
    
    local part_comment = pandoc.RawInline('latex', '% LUA FILTER: Part detected - inserting \\clearpage and setting after_part=true')
    local pagebreak = pandoc.RawInline('latex', '\\clearpage')
    return {debug_comment, part_comment, pagebreak, elem}
    
  elseif elem.level == 2 then
    -- Level 2 = Potential Chapter (Pandoc converts to \section{})
    -- Only treat as chapter if header text starts with "Chapter"
    local header_text = pandoc.utils.stringify(elem)
    
    if string.match(header_text, "^Chapter") then
      -- This is an actual chapter - apply conditional page break logic
      if after_part then
        -- First chapter after part: no page break, reset flag
        after_part = false
        local chapter_comment = pandoc.RawInline('latex', '% LUA FILTER: First chapter after part - NO pagebreak, resetting after_part=false')
        return {debug_comment, chapter_comment, elem}
      else
        -- Subsequent chapters: force page break
        local chapter_comment = pandoc.RawInline('latex', '% LUA FILTER: Subsequent chapter - inserting \\clearpage')
        local pagebreak = pandoc.RawInline('latex', '\\clearpage')
        return {debug_comment, chapter_comment, pagebreak, elem}
      end
    else
      -- This is a Level 2 header but not a chapter (like Executive Summary)
      local non_chapter_comment = pandoc.RawInline('latex', '% LUA FILTER: Level 2 non-chapter header - unchanged')
      return {debug_comment, non_chapter_comment, elem}
    end
  end
  
  -- Other header levels unchanged
  local other_comment = pandoc.RawInline('latex', '% LUA FILTER: Non-part/chapter header - unchanged')
  return {debug_comment, other_comment, elem}
end