-- P2KB PASM2 - Entry Format Filter
-- Purpose: Format instruction entry elements properly:
--   1. Convert Markdown --- to tight LaTeX horizontal rules (minimal spacing)
--   2. Process multiple instruction syntax forms with proper line breaks
--
-- Version: 1.2
-- Date: 2025-12-02

-- Convert HorizontalRule to a tight LaTeX rule
-- Markdown --- becomes a full-width rule with minimal spacing
function HorizontalRule(elem)
  -- Create a very tight horizontal rule with negative vspace to counter paragraph spacing:
  -- \vspace{-\parskip} - remove paragraph skip above
  -- \vspace{-2pt} - additional tightening
  -- \noindent\rule{\linewidth}{0.4pt} - full-width thin rule
  -- \vspace{-2pt} - minimal space below
  -- \vspace{-\parskip} - remove paragraph skip below
  local tight_rule = pandoc.RawBlock('latex',
    '\\vspace{-\\parskip}\\vspace{-2pt}\\noindent\\rule{\\linewidth}{0.4pt}\\vspace{-2pt}\\vspace{-\\parskip}'
  )
  return tight_rule
end

-- Check if a paragraph is a syntax definition block
-- Syntax blocks have a VERY specific structure:
--   **MNEMONIC** *operands* **{effects}**
--   **MNEMONIC** *operands* **{effects}**
-- They contain ONLY: Strong, Emph, Space, SoftBreak elements
-- NO Str elements with actual words (prose)
local function is_syntax_paragraph(content)
  if #content < 1 then
    return false
  end

  -- Must start with Strong (bold mnemonic)
  if content[1].t ~= "Strong" then
    return false
  end

  -- First element must be an uppercase mnemonic
  local first_text = pandoc.utils.stringify(content[1])
  if not (first_text:match("^[A-Z][A-Z0-9_]*$") or
          first_text:match("^[A-Z][A-Z0-9_]*/[A-Z0-9_]+$")) then
    return false
  end

  -- Check all elements - syntax paragraphs should NOT have prose words
  -- They only have: Strong (mnemonic/effects), Emph (operands), Space, SoftBreak
  for i, item in ipairs(content) do
    if item.t == "Str" then
      local text = item.text
      -- Allow only whitespace, commas, and empty strings
      -- Any actual word content means this is prose
      if text:match("%a%a") then
        -- Two or more consecutive letters = prose word
        return false
      end
    end
  end

  return true
end

-- Process Para elements to add line breaks between multiple syntax forms
-- Pattern: Multiple **MNEMONIC** *operands* **{effects}** on separate lines
-- ONLY operates on syntax definition paragraphs, NOT prose paragraphs
function Para(elem)
  local content = elem.content

  -- Check if this is a syntax definition paragraph (not prose)
  if not is_syntax_paragraph(content) then
    return elem
  end

  -- Count Strong elements that look like instruction mnemonics
  local mnemonic_count = 0
  for i, item in ipairs(content) do
    if item.t == "Strong" then
      local text = pandoc.utils.stringify(item)
      -- Check if it looks like an instruction mnemonic (starts with caps)
      -- Mnemonics are like ABS, ADDCT1, CALL/RET, etc.
      -- NOT effect flags like {WC|WZ|WCZ}
      if (text:match("^[A-Z][A-Z0-9_]*$") or
          text:match("^[A-Z][A-Z0-9_]*/[A-Z0-9_]+$") or
          text:match("^[A-Z][A-Z0-9_]+ /")) and
         not text:match("^{") then
        mnemonic_count = mnemonic_count + 1
      end
    end
  end

  -- If we don't have multiple mnemonics, just return as-is
  if mnemonic_count < 2 then
    return elem
  end

  -- Insert line breaks before each mnemonic (except the first)
  local new_content = {}
  local first_mnemonic_seen = false

  for i, item in ipairs(content) do
    if item.t == "Strong" then
      local text = pandoc.utils.stringify(item)
      -- Check if it looks like an instruction mnemonic (not effect flags)
      if (text:match("^[A-Z][A-Z0-9_]*$") or
          text:match("^[A-Z][A-Z0-9_]*/[A-Z0-9_]+$") or
          text:match("^[A-Z][A-Z0-9_]+ /")) and
         not text:match("^{") then
        if first_mnemonic_seen then
          -- Insert a LaTeX line break before this mnemonic
          table.insert(new_content, pandoc.RawInline('latex', '\\\\'))
        end
        first_mnemonic_seen = true
      end
    end

    table.insert(new_content, item)
  end

  elem.content = new_content
  return elem
end
