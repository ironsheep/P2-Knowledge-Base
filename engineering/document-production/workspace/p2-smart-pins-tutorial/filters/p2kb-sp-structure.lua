-- P2KB Smart Pins - Document Structure (Main Matter)
-- Purpose: Handle document structure AFTER Part I begins
-- Works WITH style sheet page break handling
-- Responsibilities:
--   - Track when we're after Parts (for first chapter handling)
--   - Let style sheet handle ALL page breaks (Parts/Chapters/Modes)
--   - Takes over AFTER frontmatter filter is done
--
-- Version: 3.2  
-- Date: 2025-09-05
-- Changes: Removed mode logic - stylesheet already handles level 3 sections

local seen_part_one = false
local just_saw_part = false  -- Track if we just saw a Part header

function Header(header)
  local title = pandoc.utils.stringify(header)
  
  -- Check if we've reached Part I - that's when we start processing
  if header.level == 1 and title:match("^Part I") then
    seen_part_one = true
    just_saw_part = true  -- Mark that we just saw a Part
    -- Don't add page break - style sheet handles Parts
    return header
  end
  
  -- Don't process anything until after Part I
  if not seen_part_one then
    return header
  end
  
  -- Level 1: Handle subsequent Parts (Part II, Part III, etc.)
  if header.level == 1 and title:match("^Part ") then
    just_saw_part = true  -- Mark that we just saw a Part
    -- Don't add page break - style sheet handles Parts
    return header
  end
  
  -- Level 2: Handle Chapters
  if header.level == 2 and title:match("^Chapter") then
    if just_saw_part then
      -- First chapter after a Part - style sheet won't add page break
      just_saw_part = false  -- Reset flag
    end
    -- Let style sheet handle chapters
    return header
  end
  
  -- Level 2: Handle Appendices  
  if header.level == 2 and title:match("^Appendix") then
    if just_saw_part then
      -- First appendix after "Appendices" part
      just_saw_part = false  -- Reset flag
    end
    -- Let style sheet handle appendices
    return header
  end
  
  -- Any other level 2 header resets the just_saw_part flag
  if header.level == 2 then
    just_saw_part = false
  end
  
  -- Level 3 headers (including Modes) are handled by stylesheet
  -- With --top-level-division=part:
  -- Level 3 becomes \section{} which gets \clearpage from stylesheet
  -- unless it's right after a \chapter{}
  
  return header
end