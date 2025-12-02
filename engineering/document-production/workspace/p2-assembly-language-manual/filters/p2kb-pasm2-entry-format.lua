-- P2KB PASM2 - Entry Format Filter
-- Purpose: Format instruction entry elements properly:
--   1. Convert Markdown --- to tight LaTeX horizontal rules (minimal spacing)
--   2. Process multiple instruction syntax forms with proper line breaks
--
-- Version: 1.1
-- Date: 2025-12-02

-- Convert HorizontalRule to a tight LaTeX rule
-- Markdown --- becomes a full-width rule with minimal spacing
function HorizontalRule(elem)
  -- Create a very tight horizontal rule:
  -- \vspace{0pt} - no extra space above (just natural paragraph spacing)
  -- \noindent\rule{\linewidth}{0.4pt} - full-width thin rule
  -- \vspace{0pt} - no extra space below
  local tight_rule = pandoc.RawBlock('latex',
    '\\vspace{0pt}\\noindent\\rule{\\linewidth}{0.4pt}\\vspace{0pt}'
  )
  return tight_rule
end

-- Process Para elements to add line breaks between multiple syntax forms
-- Pattern: Multiple **MNEMONIC** elements in one paragraph need \\ between them
function Para(elem)
  local content = elem.content
  local new_content = {}
  local found_multiple = false

  -- First pass: count Strong elements that look like instruction mnemonics
  local mnemonic_count = 0
  local i = 1
  while i <= #content do
    local item = content[i]
    if item.t == "Strong" then
      local text = pandoc.utils.stringify(item)
      -- Check if it looks like an instruction mnemonic (starts with caps)
      -- Mnemonics are like ABS, ADDCT1, CALL/RET, etc.
      if text:match("^[A-Z][A-Z0-9_]*$") or text:match("^[A-Z][A-Z0-9_]*/[A-Z0-9_]+$") or
         text:match("^[A-Z][A-Z0-9_]+ /") then
        mnemonic_count = mnemonic_count + 1
      end
    end
    i = i + 1
  end

  -- If we don't have multiple mnemonics, just return as-is
  if mnemonic_count < 2 then
    return elem
  end

  -- Second pass: insert line breaks before each mnemonic (except the first)
  local first_mnemonic_seen = false
  i = 1
  while i <= #content do
    local item = content[i]

    if item.t == "Strong" then
      local text = pandoc.utils.stringify(item)
      -- Check if it looks like an instruction mnemonic
      if text:match("^[A-Z][A-Z0-9_]*$") or text:match("^[A-Z][A-Z0-9_]*/[A-Z0-9_]+$") or
         text:match("^[A-Z][A-Z0-9_]+ /") then
        if first_mnemonic_seen then
          -- Insert a LaTeX line break before this mnemonic
          table.insert(new_content, pandoc.RawInline('latex', '\\\\'))
          found_multiple = true
        end
        first_mnemonic_seen = true
      end
    end

    table.insert(new_content, item)
    i = i + 1
  end

  if found_multiple then
    elem.content = new_content
  end

  return elem
end
