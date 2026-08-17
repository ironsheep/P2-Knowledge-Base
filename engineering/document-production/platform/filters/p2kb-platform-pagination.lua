-- P2KB IOSP Reference Manual - Pagination Filter
-- Purpose: Handles Part/Chapter structure and page breaks
--
-- Behavior:
-- - "# Part X" → \manualpart{} (own page, adds to TOC)
-- - First chapter after Part → NO page break (stays on Part page)
-- - Subsequent chapters → page break before
-- - "# Instructions: X" treated as chapters
-- - "# Assembler Directives", "# Special Registers" treated as chapters
--
-- Version: 2.0 - Proper Part/Chapter/TOC handling
-- Date: 2025-12-04

-- Track if this is the first chapter (to avoid clearpage right after TOC)
local first_chapter = true

-- Track if we just emitted a Part (next chapter stays on same page)
local just_emitted_part = false

-- Helper: escape LaTeX specials in a plain-text string.
--
-- THE INVARIANT: any stringify()'d text this filter emits inside a RawBlock
-- MUST pass through here. stringify() flattens an element to plain text, so
-- nothing in the result is intentional LaTeX — but a raw argument bypasses
-- pandoc's escaping entirely, and an unescaped &, %, $, #, or _ then reaches
-- xelatex raw. & aborts with "Misplaced alignment tab character &"; % is worse,
-- silently commenting out the rest of the line with a clean log.
--
-- Both raw sites are covered: \chaptersubtitle{} (e.g. "Periods, Duty &
-- Reciprocal Counting") and \manualpart{}. The Part title went unescaped until
-- 2026-08-17, which is why authors were told to spell "and" in Part titles —
-- a workaround for this bug, no longer needed.
local function latex_escape(s)
  return (s:gsub('([&%%$#_])', '\\%1'))
end

-- Helper: Check if title represents a chapter-level heading
local function is_chapter_heading(title)
  return title:match("^Chapter") or
         title:match("^Appendix") or
         title:match("^Instructions:") or
         title:match("^Assembler Directives") or
         title:match("^Special Registers") or
         title:match("^Preface") or
         title:match("^Copyright") or
         title:match("^Dedication") or
         title:match("^Acknowledgments") or
         title:match("Quick Reference") or
         title:match("^Index")
end

-- Handle Header elements for page breaks and Part conversion
function Header(header)
  local title = pandoc.utils.stringify(header.content)

  -- Level 1 headers need special handling
  if header.level == 1 then

    -- Part headings → \manualpart{} (adds to TOC, own page, no break after)
    if title:match("^Part ") then
      local manualpart = pandoc.RawBlock('latex', '\\manualpart{' .. latex_escape(title) .. '}')
      just_emitted_part = true
      return manualpart
    end

    -- Chapter-level headings
    if is_chapter_heading(title) then
      local blocks = {}

      -- Page break before the chapter (except the very first, and the first
      -- chapter right after a Part divider)
      if first_chapter then
        first_chapter = false
      elseif just_emitted_part then
        just_emitted_part = false
      else
        table.insert(blocks, pandoc.RawBlock('latex', '\\clearpage'))
      end

      -- Set the chapter counter from the heading's REAL number/letter so per-chapter
      -- figure numbering is correct (Figure 7.1, 11.2, D.1, ...). Pandoc emits
      -- \chapter* (unnumbered), which does not step the counter, so figures would
      -- otherwise all read 0.x. Also reset the figure counter at each chapter.
      local cnum = title:match("^Chapter%s+(%d+)")
      local anum = title:match("^Appendix%s+([A-Z])")
      if cnum then
        table.insert(blocks, pandoc.RawBlock('latex',
          '\\setcounter{chapter}{' .. cnum .. '}\\setcounter{figure}{0}'))
      elseif anum then
        local idx = string.byte(anum) - string.byte('A') + 1
        table.insert(blocks, pandoc.RawBlock('latex',
          '\\renewcommand{\\thechapter}{\\Alph{chapter}}\\setcounter{chapter}{' .. idx .. '}\\setcounter{figure}{0}'))
      end

      -- Split a "Title — Subtitle" chapter heading: the Title stays on the
      -- \chapter (so the TOC + running head carry the window name only); the
      -- Subtitle renders just under it via \chaptersubtitle (foundation macro).
      -- Numbered chapters only; " — " is space + em-dash (U+2014, bytes
      -- \226\128\148) + space = 5 bytes.
      local subtitle = nil
      if cnum then
        local sep = title:find(" \226\128\148 ", 1, true)
        if sep then
          header.content = { pandoc.Str(title:sub(1, sep - 1)) }
          subtitle = title:sub(sep + 5)
        end
      end

      table.insert(blocks, header)
      if subtitle then
        table.insert(blocks, pandoc.RawBlock('latex', '\\chaptersubtitle{' .. latex_escape(subtitle) .. '}'))
      end
      return blocks
    end
  end

  -- Any non-Part header clears the just_emitted_part flag
  just_emitted_part = false

  -- Level 2 and below: no automatic page breaks
  return header
end
