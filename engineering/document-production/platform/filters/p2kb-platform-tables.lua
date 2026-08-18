-- P2KB IOSP Table Formatting Filter
-- Auto-shrink tables to content width, full-width only when needed
-- Author: Iron Sheep Productions, LLC
-- Version: 6.10 - Numbered table captions (layout standard). When a markdown table
--                 carries a "Table: ..." caption, emit a NUMBERED \caption that
--                 registers it in the List of Tables and keeps caption welded to
--                 the table: non-breaking tblr is wrapped in a table[H] float;
--                 breakable longtblr uses the [caption=,label=] outer key;
--                 longtable encoding tables use a leading \caption row. Uncaptioned
--                 tables are unchanged (bare, unnumbered).
-- Version: 6.9 - Fix #5: many-col tables (<=12) routed to token-fit wide branch + \tiny tier (6.1);
--                is_instr_desc col-1 width is token-aware so long symbols never overflow (6.2)
-- Version: 6.8 - Fix #3: wide+many-row auto-shrink tables use breakable longtblr (case 5.1)
--
-- Strategy:
-- - 9-column encoding tables: Fixed widths with colored headers (tabularray)
-- - Tables with long content patterns: Full page width with proportional columns
--   * Constant | Value | Description (36-char binary patterns)
--   * Condition Code tables (long alias lists)
--   * Instruction | Description (Appendix B style)
-- - All other tables: Auto-shrink to content width (no wrapping)
-- - This produces cleaner output for short explanatory tables

-- Helper: escape LaTeX specials in plain text bound for a raw LaTeX position.
--
-- THE INVARIANT: any stringify()'d text this filter emits into a raw position (a
-- tblr cell, a caption={} key) MUST pass through here. stringify() flattens an
-- element to plain text, so nothing in the result is intentional LaTeX. Inside a
-- tblr cell an unescaped & IS an alignment tab: it ends the cell early and shifts
-- every later column right (F-284 -- "Parity of (D & S)" shipped for two releases
-- as "Parity of (D" | "S)"). An unescaped % is worse, silently commenting out the
-- rest of the row with a clean compile log.
--
-- SCOPE IS DELIBERATELY & % # _ -- the same four the cell renderers already
-- escape inline. It does NOT escape { } \, because instruction tables legitimately
-- carry P2 syntax like {#}, and escaping those braces would change pages that
-- render correctly today. Closing the hole must not move correct output.
local function cell_escape(s)
  s = s:gsub("&", "\\&")
  s = s:gsub("%%", "\\%%")
  s = s:gsub("#", "\\#")
  s = s:gsub("_", "\\_")
  return s
end

-- ==================== NUMBERED CAPTIONS (layout standard) ====================
-- A markdown table caption ("Table: ...", or ": ..." below the table) lands in
-- el.caption.long. Render it to LaTeX and pair it with the table's identifier
-- (e.g. {#tbl:foo}) as a \label. Returns ("","") when the table has no caption
-- so uncaptioned tables stay bare and unnumbered.
local function table_caption_and_label(el)
  local cap = ""
  if el.caption and el.caption.long and #el.caption.long > 0 then
    local ok, res = pcall(function()
      local s = pandoc.write(pandoc.Pandoc(el.caption.long), "latex")
      return (s or ""):gsub("%s+$", "")
    end)
    if ok and res and res ~= "" then
      cap = res
    else
      -- pandoc.write escapes; the stringify fallback does not, and cap is emitted
      -- into a raw caption={} key.
      cap = cell_escape(pandoc.utils.stringify(el.caption.long))
    end
  end
  local label = el.identifier or ""
  return cap, label
end

-- Opening line for a breaking table (longtblr), adding the numbered-caption outer
-- key when present. longtblr ALWAYS emits (and counts) a caption of its own, so the
-- caption MUST go through this native key -- emitting a separate \captionof would
-- double the caption and skew the table counter. The caption's VISUAL style (period
-- separator, small font, bold "Table N.M" label) is matched to the caption-package
-- look used by figures and short tables via the tabularray caption-template
-- overrides in p2kb-platform-content.sty, so both table paths read identically.
local function longtblr_begin(cap, label)
  if cap == "" then
    return "\\begin{longtblr}{"
  end
  local opt = "caption={" .. cap .. "}"
  if label ~= "" then
    opt = opt .. ",label={" .. label .. "}"
  end
  return "\\begin{longtblr}[" .. opt .. "]{"
end

-- Caption row for a classic longtable (the encoding/master tables). longtable
-- takes its caption as a leading row before \endfirsthead; it numbers the table
-- and registers it in the List of Tables. Returns nil when there is no caption.
local function longtable_caption_row(cap, label)
  if cap == "" then
    return nil
  end
  local s = "\\caption{" .. cap .. "}"
  if label ~= "" then
    s = s .. "\\label{" .. label .. "}"
  end
  return s .. " \\\\"
end

-- Wrap a NON-breaking table environment (tblr / short tblr) in a table[H] float so
-- a numbered \caption sits welded above it (both move together to the next page if
-- they do not fit -- the H float is an unbreakable unit). No caption => unchanged.
local function wrap_float(inner, cap, label)
  if cap == "" then
    return inner
  end
  local pre = "\\begin{table}[H]\n\\centering\n\\caption{" .. cap .. "}"
  if label ~= "" then
    pre = pre .. "\\label{" .. label .. "}"
  end
  return pre .. "\n" .. inner .. "\n\\end{table}"
end

-- Count total data rows in a table (excluding header)
local function count_data_rows(el)
  local count = 0
  for _, body in ipairs(el.bodies) do
    if body.body then
      count = count + #body.body
    end
  end
  return count
end

-- Get maximum text length in a column across all rows (used for encoding tables)
local function get_max_column_length(el, col_index)
  local max_len = 0

  -- Check header rows
  if el.head and el.head.rows then
    for _, row in ipairs(el.head.rows) do
      if row.cells and row.cells[col_index] then
        local text = pandoc.utils.stringify(row.cells[col_index].contents)
        if #text > max_len then
          max_len = #text
        end
      end
    end
  end

  -- Check body rows
  for _, body in ipairs(el.bodies) do
    if body.body then
      for _, row in ipairs(body.body) do
        if row.cells and row.cells[col_index] then
          local text = pandoc.utils.stringify(row.cells[col_index].contents)
          if #text > max_len then
            max_len = #text
          end
        end
      end
    end
  end

  return max_len
end

-- Get the longest UNBREAKABLE token (whitespace-delimited run) in a column.
-- This is the minimum width that column must have: identifiers like
-- P_OE_FLOAT_LOW_1K5_PULLUP_FILTER cannot be hyphenated or wrapped, so the
-- column has to be at least this wide or the token spills into the next column.
local function get_max_token_length(el, col_index)
  local max_tok = 1
  local function scan(rows)
    if not rows then return end
    for _, row in ipairs(rows) do
      if row.cells and row.cells[col_index] then
        local s = pandoc.utils.stringify(row.cells[col_index].contents)
        for tok in s:gmatch("%S+") do
          if #tok > max_tok then max_tok = #tok end
        end
      end
    end
  end
  if el.head then scan(el.head.rows) end
  for _, body in ipairs(el.bodies) do
    if body.body then scan(body.body) end
  end
  return max_tok
end

-- Handle 9-column encoding tables specially
-- Columns 1-5 are fixed-width bit fields (EEEE, Opcode, CZI, D, S)
-- Columns 6-9 are variable content (C, Z, Result, Clks)
-- Uses standard longtable for reliable multi-page support
local function handle_encoding_table(el)
  -- Count rows to decide between tabular and longtable
  local row_count = count_data_rows(el)
  local use_longtable = row_count > 20  -- Use longtable for tables with 20+ rows
  local cap, label = table_caption_and_label(el)

  -- Helper to render cell contents as LaTeX
  local function cell_to_latex(cell)
    if not cell or not cell.contents then
      return ""
    end
    if #cell.contents == 0 then
      return ""
    end
    local text = pandoc.utils.stringify(cell.contents)
    -- Escape special LaTeX characters in cell content.
    -- stringify() flattens the cell to plain text, so nothing here is
    -- intentional LaTeX. An unescaped & ends the cell early and shifts every
    -- later column right; % silently comments out the rest of the row.
    text = text:gsub("&", "\\&")
    text = text:gsub("%%", "\\%%")
    text = text:gsub("#", "\\#")
    text = text:gsub("_", "\\_")
    return text
  end

  -- Extract header row
  local headers = {"EEEE", "Opcode", "CZI", "Dest", "Src", "C", "Z", "Result", "Clks"}
  if el.head and el.head.rows and #el.head.rows > 0 then
    local header_row = el.head.rows[1]
    if header_row.cells then
      for i, cell in ipairs(header_row.cells) do
        if i <= 9 then
          headers[i] = cell_to_latex(cell)
        end
      end
    end
  end

  local latex = {}

  if use_longtable then
    -- Use standard longtable for reliable page breaks
    -- Column spec: p{width} for fixed columns, centered
    table.insert(latex, "\\begin{longtable}{|>{\\centering\\arraybackslash\\ttfamily\\small}p{0.055\\linewidth}|>{\\centering\\arraybackslash\\ttfamily\\small}p{0.075\\linewidth}|>{\\centering\\arraybackslash\\ttfamily\\small}p{0.04\\linewidth}|>{\\centering\\arraybackslash\\ttfamily\\small}p{0.095\\linewidth}|>{\\centering\\arraybackslash\\ttfamily\\small}p{0.095\\linewidth}|>{\\centering\\arraybackslash\\small}p{0.12\\linewidth}|>{\\centering\\arraybackslash\\small}p{0.12\\linewidth}|>{\\centering\\arraybackslash\\small}p{0.17\\linewidth}|>{\\centering\\arraybackslash\\small}p{0.05\\linewidth}|}")

    -- Numbered caption (registers in List of Tables), if the table carries one
    local cap_row = longtable_caption_row(cap, label)
    if cap_row then table.insert(latex, cap_row) end

    -- Build colored header row (cell colors for each zone)
    local header_row = "\\cellcolor{iosp-enc-instruction}\\textbf{" .. headers[1] .. "} & " ..
                       "\\cellcolor{iosp-enc-instruction}\\textbf{" .. headers[2] .. "} & " ..
                       "\\cellcolor{iosp-enc-instruction}\\textbf{" .. headers[3] .. "} & " ..
                       "\\cellcolor{iosp-enc-operand}\\textbf{" .. headers[4] .. "} & " ..
                       "\\cellcolor{iosp-enc-operand}\\textbf{" .. headers[5] .. "} & " ..
                       "\\cellcolor{iosp-enc-flags}\\textbf{" .. headers[6] .. "} & " ..
                       "\\cellcolor{iosp-enc-flags}\\textbf{" .. headers[7] .. "} & " ..
                       "\\cellcolor{iosp-enc-result}\\textbf{" .. headers[8] .. "} & " ..
                       "\\cellcolor{iosp-enc-result}\\textbf{" .. headers[9] .. "} \\\\"

    -- First head (first page only)
    table.insert(latex, "\\hline")
    table.insert(latex, header_row)
    table.insert(latex, "\\hline")
    table.insert(latex, "\\endfirsthead")

    -- Continuation head (subsequent pages)
    table.insert(latex, "\\hline")
    table.insert(latex, "\\multicolumn{9}{|c|}{\\textit{(continued from previous page)}} \\\\")
    table.insert(latex, "\\hline")
    table.insert(latex, header_row)
    table.insert(latex, "\\hline")
    table.insert(latex, "\\endhead")

    -- Footer (bottom of each page except last)
    table.insert(latex, "\\hline")
    table.insert(latex, "\\multicolumn{9}{|r|}{\\textit{(continued on next page)}} \\\\")
    table.insert(latex, "\\hline")
    table.insert(latex, "\\endfoot")

    -- Last footer
    table.insert(latex, "\\hline")
    table.insert(latex, "\\endlastfoot")

  else
    -- Use tblr for short tables (preserves nice formatting)
    table.insert(latex, "\\begin{tblr}{")
    table.insert(latex, "  width=\\linewidth,")
    table.insert(latex, "  rowsep=2pt,")
    table.insert(latex, "  colsep=4pt,")
    table.insert(latex, "  column{1}={wd=0.070\\linewidth, halign=c, font=\\ttfamily\\small},")
    table.insert(latex, "  column{2}={wd=0.090\\linewidth, halign=c, font=\\ttfamily\\small},")
    table.insert(latex, "  column{3}={wd=0.050\\linewidth, halign=c, font=\\ttfamily\\small},")
    table.insert(latex, "  column{4}={wd=0.110\\linewidth, halign=c, font=\\ttfamily\\small},")
    table.insert(latex, "  column{5}={wd=0.110\\linewidth, halign=c, font=\\ttfamily\\small},")
    table.insert(latex, "  column{6}={wd=0.100\\linewidth, halign=c, font=\\small},")
    table.insert(latex, "  column{7}={wd=0.100\\linewidth, halign=c, font=\\small},")
    table.insert(latex, "  column{8}={wd=0.170\\linewidth, halign=c, font=\\small},")
    table.insert(latex, "  column{9}={wd=0.080\\linewidth, halign=c, font=\\small},")
    table.insert(latex, "  row{1}={font=\\bfseries\\footnotesize},")
    table.insert(latex, "  cell{1}{1}={bg=iosp-enc-instruction},")
    table.insert(latex, "  cell{1}{2}={bg=iosp-enc-instruction},")
    table.insert(latex, "  cell{1}{3}={bg=iosp-enc-instruction},")
    table.insert(latex, "  cell{1}{4-5}={bg=iosp-enc-operand},")
    table.insert(latex, "  cell{1}{6-7}={bg=iosp-enc-flags},")
    table.insert(latex, "  cell{1}{8-9}={bg=iosp-enc-result},")
    table.insert(latex, "  hlines,")
    table.insert(latex, "  vlines,")
    table.insert(latex, "}")
    table.insert(latex, "  " .. table.concat(headers, " & ") .. " \\\\")
  end

  -- Add data rows
  for _, body in ipairs(el.bodies) do
    if body.body then
      for _, row in ipairs(body.body) do
        local cells = {}
        for i, cell in ipairs(row.cells) do
          if i <= 9 then
            table.insert(cells, cell_to_latex(cell))
          end
        end
        if #cells == 9 then
          table.insert(latex, "  " .. table.concat(cells, " & ") .. " \\\\")
        end
      end
    end
  end

  if use_longtable then
    table.insert(latex, "\\end{longtable}")
    -- Return as RawBlock (longtable carries its own caption row above)
    return pandoc.RawBlock("latex", table.concat(latex, "\n"))
  else
    table.insert(latex, "\\end{tblr}")
    -- Short encoding tables are non-breaking tblr -> weld caption via table[H] float
    return pandoc.RawBlock("latex", wrap_float(table.concat(latex, "\n"), cap, label))
  end
end

-- Detect if this is a 6-column encoding master table (Appendix A pattern)
-- Headers: Instruction | Opcode | CZI | Cycles | C Effect | Z Effect
local function is_encoding_master_table(el)
  if #el.colspecs ~= 6 then
    return false
  end

  -- Check header row for encoding table pattern
  if el.head and el.head.rows and #el.head.rows > 0 then
    local header_row = el.head.rows[1]
    if header_row.cells and #header_row.cells >= 6 then
      local h1 = pandoc.utils.stringify(header_row.cells[1].contents):lower()
      local h2 = pandoc.utils.stringify(header_row.cells[2].contents):lower()
      local h3 = pandoc.utils.stringify(header_row.cells[3].contents):lower()

      -- Match "Instruction | Opcode | CZI | ..." pattern
      if h1:match("instruction") and h2:match("opcode") and h3:match("czi") then
        return true
      end
    end
  end

  return false
end

-- Handle 6-column encoding master table (Appendix A)
-- Uses standard longtable for reliable multi-page support
local function handle_encoding_master_table(el)
  local row_count = count_data_rows(el)
  local cap, label = table_caption_and_label(el)

  -- Helper to render cell contents as LaTeX (with escaping)
  local function cell_to_latex(cell)
    if not cell or not cell.contents then
      return ""
    end
    if #cell.contents == 0 then
      return ""
    end
    local text = pandoc.utils.stringify(cell.contents)
    -- Escape special LaTeX characters in cell content
    text = text:gsub("&", "\\&")
    text = text:gsub("%%", "\\%%")
    text = text:gsub("#", "\\#")
    text = text:gsub("_", "\\_")
    return text
  end

  -- Extract header row
  local headers = {"Instruction", "Opcode", "CZI", "Cycles", "C Effect", "Z Effect"}
  if el.head and el.head.rows and #el.head.rows > 0 then
    local header_row = el.head.rows[1]
    if header_row.cells then
      for i, cell in ipairs(header_row.cells) do
        if i <= 6 then
          headers[i] = cell_to_latex(cell)
        end
      end
    end
  end

  local latex = {}

  -- Always use longtable for this table (it has 300+ rows)
  -- Column spec: fixed widths for all columns
  table.insert(latex, "\\begin{longtable}{|>{\\raggedright\\arraybackslash}p{0.14\\linewidth}|>{\\centering\\arraybackslash\\ttfamily\\small}p{0.10\\linewidth}|>{\\centering\\arraybackslash}p{0.05\\linewidth}|>{\\centering\\arraybackslash}p{0.07\\linewidth}|>{\\raggedright\\arraybackslash\\small}p{0.26\\linewidth}|>{\\raggedright\\arraybackslash\\small}p{0.26\\linewidth}|}")

  -- Numbered caption (registers in List of Tables), if the table carries one
  local cap_row = longtable_caption_row(cap, label)
  if cap_row then table.insert(latex, cap_row) end

  -- Build header row
  local header_row_tex = "\\textbf{" .. headers[1] .. "} & " ..
                         "\\textbf{" .. headers[2] .. "} & " ..
                         "\\textbf{" .. headers[3] .. "} & " ..
                         "\\textbf{" .. headers[4] .. "} & " ..
                         "\\textbf{" .. headers[5] .. "} & " ..
                         "\\textbf{" .. headers[6] .. "} \\\\"

  -- First head (first page only)
  table.insert(latex, "\\hline")
  table.insert(latex, header_row_tex)
  table.insert(latex, "\\hline")
  table.insert(latex, "\\endfirsthead")

  -- Continuation head (subsequent pages)
  table.insert(latex, "\\hline")
  table.insert(latex, "\\multicolumn{6}{|c|}{\\textit{Instruction Encodings (continued)}} \\\\")
  table.insert(latex, "\\hline")
  table.insert(latex, header_row_tex)
  table.insert(latex, "\\hline")
  table.insert(latex, "\\endhead")

  -- Footer (bottom of each page except last)
  table.insert(latex, "\\hline")
  table.insert(latex, "\\multicolumn{6}{|r|}{\\textit{(continued on next page)}} \\\\")
  table.insert(latex, "\\hline")
  table.insert(latex, "\\endfoot")

  -- Last footer
  table.insert(latex, "\\hline")
  table.insert(latex, "\\endlastfoot")

  -- Add data rows
  for _, body in ipairs(el.bodies) do
    if body.body then
      for _, row in ipairs(body.body) do
        local cells = {}
        for i, cell in ipairs(row.cells) do
          if i <= 6 then
            table.insert(cells, cell_to_latex(cell))
          end
        end
        if #cells == 6 then
          table.insert(latex, "  " .. table.concat(cells, " & ") .. " \\\\")
        end
      end
    end
  end

  table.insert(latex, "\\end{longtable}")

  return pandoc.RawBlock("latex", table.concat(latex, "\n"))
end

-- Detect if this is a "Constant | Value | Description" table (Appendix E, F patterns)
-- These tables have long binary/hex values in column 2 that need special handling
local function is_constant_value_description_table(el)
  if #el.colspecs ~= 3 then
    return false
  end

  -- Check header row for "Constant", "Value", "Description" pattern
  if el.head and el.head.rows and #el.head.rows > 0 then
    local header_row = el.head.rows[1]
    if header_row.cells and #header_row.cells >= 3 then
      local h1 = pandoc.utils.stringify(header_row.cells[1].contents):lower()
      local h2 = pandoc.utils.stringify(header_row.cells[2].contents):lower()
      local h3 = pandoc.utils.stringify(header_row.cells[3].contents):lower()

      -- Match "Constant | Value | Description" or similar patterns
      if (h1:match("constant") or h1:match("name") or h1:match("symbol")) and
         (h2:match("value") or h2:match("hex") or h2:match("binary")) and
         (h3:match("description") or h3:match("meaning") or h3:match("purpose")) then
        return true
      end
    end
  end

  return false
end

-- Detect if this is a 2-column table with long descriptions (Appendix B, Chapter 4 patterns)
-- These tables need full width: ~20% identifier, ~80% description/behavior
-- Patterns: "Instruction | Description", "X | Behavior", "X | Description", etc.
local function is_instruction_description_table(el)
  if #el.colspecs ~= 2 then
    return false
  end

  -- Check header row for patterns where column 2 contains long text
  if el.head and el.head.rows and #el.head.rows > 0 then
    local header_row = el.head.rows[1]
    if header_row.cells and #header_row.cells >= 2 then
      local h2 = pandoc.utils.stringify(header_row.cells[2].contents):lower()

      -- Match tables where column 2 typically has long paragraph-style content
      -- Note: "meaning" and "purpose" often have short entries, so exclude them
      if h2:match("description") or h2:match("behavior") or h2:match("explanation") then
        return true
      end
    end
  end

  return false
end

-- Detect if this is an "Operator | Description | Example" table (Chapter 2 pattern)
-- These 3-column tables need consistent widths to prevent column 1 cramping column 2
local function is_operator_description_example_table(el)
  if #el.colspecs ~= 3 then
    return false
  end

  -- Check header row for "Operator", "Description", "Example" pattern
  if el.head and el.head.rows and #el.head.rows > 0 then
    local header_row = el.head.rows[1]
    if header_row.cells and #header_row.cells >= 3 then
      local h1 = pandoc.utils.stringify(header_row.cells[1].contents):lower()
      local h2 = pandoc.utils.stringify(header_row.cells[2].contents):lower()
      local h3 = pandoc.utils.stringify(header_row.cells[3].contents):lower()

      -- Match "Operator | Description | Example" pattern
      if h1:match("operator") and h2:match("description") and h3:match("example") then
        return true
      end
    end
  end

  return false
end

-- Detect if this is a Condition Code Table (Chapter 2.2.1 pattern)
-- 5 columns: EEEE | Primary Mnemonic | Aliases | Condition | Description
-- Needs specific widths because Aliases column has long comma-separated lists
local function is_condition_code_table(el)
  if #el.colspecs ~= 5 then
    return false
  end

  -- Check header row for "EEEE" in first column (unique identifier)
  if el.head and el.head.rows and #el.head.rows > 0 then
    local header_row = el.head.rows[1]
    if header_row.cells and #header_row.cells >= 5 then
      local h1 = pandoc.utils.stringify(header_row.cells[1].contents):upper()
      local h3 = pandoc.utils.stringify(header_row.cells[3].contents):lower()
      local h4 = pandoc.utils.stringify(header_row.cells[4].contents):lower()

      -- Match "EEEE | ... | Aliases | Condition | ..." pattern
      if h1 == "EEEE" and h3:match("alias") and h4:match("condition") then
        return true
      end
    end
  end

  return false
end

-- Detect if this is a table with long comma-separated instruction lists (Chapter 3 pattern)
-- 3 columns where column 2 or 3 has "Instructions" header
local function is_category_instructions_table(el)
  if #el.colspecs ~= 3 then
    return false
  end

  -- Check header row for pattern with "Instructions" in column 2 or 3
  if el.head and el.head.rows and #el.head.rows > 0 then
    local header_row = el.head.rows[1]
    if header_row.cells and #header_row.cells >= 3 then
      local h1 = pandoc.utils.stringify(header_row.cells[1].contents):lower()
      local h2 = pandoc.utils.stringify(header_row.cells[2].contents):lower()
      local h3 = pandoc.utils.stringify(header_row.cells[3].contents):lower()

      -- Match "Category | Count | Instructions" pattern (column 3 has long lists)
      if (h1:match("category") or h1:match("type")) and h3:match("instruction") then
        return true
      end

      -- Match "Family | Instructions | Operation" pattern (column 2 has long lists)
      if h1:match("family") and h2:match("instruction") then
        return true
      end

      -- Match "Category | Example Modes | Typical Applications" pattern (Chapter 5)
      if h1:match("category") and (h2:match("mode") or h2:match("example")) and h3:match("application") then
        return true
      end

      -- Match "Category | Allowed Effects | Reason" pattern (Appendix C)
      if h1:match("category") and h2:match("effect") and h3:match("reason") then
        return true
      end
    end
  end

  return false
end

-- Detect tables that NEED full page width due to long content
-- These are tables where auto-shrink would cause overflow or look bad
local function needs_full_width(el)
  -- Check each detection function for long-content patterns
  if is_constant_value_description_table(el) then
    return true  -- 36-char binary patterns in Value column
  end

  if is_condition_code_table(el) then
    return true  -- Long comma-separated alias lists
  end

  if is_instruction_description_table(el) then
    return true  -- Descriptions may be long paragraphs
  end

  if is_operator_description_example_table(el) then
    return true  -- Examples with code need controlled widths
  end

  if is_category_instructions_table(el) then
    return true  -- Long comma-separated instruction lists
  end

  return false
end

-- Handle auto-shrink tables: no width constraint, columns size to content
local function handle_auto_shrink_table(el)
  local num_cols = #el.colspecs
  local cap, label = table_caption_and_label(el)

  -- Helper to render cell contents as LaTeX
  local function cell_to_latex(cell)
    if not cell or not cell.contents then
      return ""
    end
    if #cell.contents == 0 then
      return ""
    end
    local ok, result = pcall(function()
      local doc = pandoc.Pandoc(cell.contents)
      local latex_str = pandoc.write(doc, "latex")
      if latex_str then
        return latex_str:gsub("\n$", "")
      else
        -- stringify does NOT escape; this lands raw in a tblr cell
        return cell_escape(pandoc.utils.stringify(cell.contents))
      end
    end)
    if ok then
      return result or ""
    else
      return cell_escape(pandoc.utils.stringify(cell.contents)) or ""
    end
  end

  -- Estimate content width (in characters) per column to decide wrap vs shrink.
  -- Wide tables would overflow the right margin with plain "l" columns, so they
  -- switch to width=\linewidth with proportional wrapping X columns + smaller font.
  local maxlen = {}   -- longest full cell (chars) per column
  local maxtok = {}   -- longest UNBREAKABLE unit (chars) per column
  for i = 1, num_cols do maxlen[i] = 1; maxtok[i] = 1 end
  local function measure(cells)
    if not cells then return end
    for i, cell in ipairs(cells) do
      if i <= num_cols then
        local s = pandoc.utils.stringify(cell.contents)
        local n = #s
        if n > maxlen[i] then maxlen[i] = n end
        -- A column's minimum width is its longest UNBREAKABLE unit. Identifiers
        -- like P_COUNTER_PERIODS cannot be hyphenated and must fit whole, but
        -- ordinary words DO hyphenate -- so counting every word as unbreakable
        -- over-reserves width on prose-heavy tables and forces an unreadably
        -- small font (which then can't even fit the real identifiers; that was
        -- the 6.1 overlap). Split on spaces, hyphens and en/em dashes (all real
        -- break points), then let only "hard" units -- anything that is NOT a
        -- plain Capitalized/lowercase word (i.e. has underscores, digits,
        -- acronym caps, slashes...) -- set the floor. Plain words wrap freely.
        -- Hard units (identifiers) must fit whole; soft words only need room for
        -- a hyphenation fragment, so they are capped at SOFT_FLOOR characters. A
        -- column's floor is the larger of the two, which keeps prose columns wide
        -- enough to hyphenate cleanly without over-reserving for whole words.
        local SOFT_FLOOR = 6
        -- Identifier glyphs (caps, digits, underscores) are noticeably wider than
        -- the mixed-case average the cpl constants are calibrated for, so a hard
        -- unit needs ~25% more width than its raw character count or it overruns
        -- its column into the next one.
        local HARD_FACTOR = 1.25
        local t = s:gsub("\226\128\147", " "):gsub("\226\128\148", " ")  -- en/em dash -> space
        for unit in t:gmatch("[^%s%-]+") do
          local hard = not unit:match("^%u?%l+$")
          local need = hard and math.ceil(#unit * HARD_FACTOR) or math.min(#unit, SOFT_FLOOR)
          if need > maxtok[i] then maxtok[i] = need end
        end
      end
    end
  end
  if el.head and el.head.rows then
    for _, r in ipairs(el.head.rows) do measure(r.cells) end
  end
  for _, body in ipairs(el.bodies) do
    if body.body then for _, r in ipairs(body.body) do measure(r.cells) end end
  end
  local total = 0
  for i = 1, num_cols do total = total + maxlen[i] end
  -- The narrow branch renders unconstrained "l" columns at \normalsize, which
  -- fits only ~60 chars across \linewidth. If natural content approaches that,
  -- the table overflows the right margin (or, with long unbreakable identifiers,
  -- collides into the next column) -- so route it to the width-managed wide
  -- branch instead. (Previous 72 threshold was calibrated for \small and let
  -- ~60-72-char tables like Ch12.11 / Appendix D overflow at \normalsize.)
  local wide = (total > 60) or (num_cols >= 4 and total > 44)

  -- Tall narrow tables (e.g. the 34-row instruction quick-reference, Table 1.10)
  -- render as a single non-breaking tblr. At default size they overrun the page
  -- bottom and orphan the following legend. Compress row spacing + font so the
  -- whole table (and its legend paragraph) fits on one page.
  local tall = count_data_rows(el) > 24

  -- A WIDE table with many rows cannot fit on one page: a non-breaking tblr runs
  -- straight off the page bottom and silently loses its tail (platform case 5.1).
  -- Route such tables to longtblr instead -- breakable, with a repeating header
  -- row (rowhead=1). The narrow "tall" branch is deliberately NOT converted: it
  -- compresses onto a SINGLE page by design (Table 1.10 + its legend stay
  -- together), which is a different, already-verified goal.
  local use_longtblr = wide and count_data_rows(el) > 20

  local latex = {}
  if use_longtblr then
    table.insert(latex, longtblr_begin(cap, label))
  else
    table.insert(latex, "\\begin{tblr}{")
  end
  if wide then
    -- Width allocation that never overflows AND never splits a name.
    -- Every column is given a FIXED width (Q[wd=...]) of at least its longest
    -- unbreakable token, so identifiers like P_COUNTER_PERIODS always fit inside
    -- their cell (no spill into the next column, no hyphenation at underscores).
    -- Any leftover width is then handed to the columns that have wrappable prose
    -- (cell length beyond their longest token), which wrap at spaces. Font is
    -- shrunk only if the minimum (token-fit) widths don't fit at the larger size.
    -- chars_per_line = how many characters span \linewidth at a given font
    -- (calibrated: ~72 at \small, scaling roughly with font size).
    local fonts = {
      {name="\\small",      cpl=72, cs="5pt"},
      {name="\\footnotesize", cpl=84, cs="4pt"},
      {name="\\scriptsize", cpl=100, cs="3pt"},
      -- Smallest tier: lets very wide many-column tables (e.g. the 10-column
      -- platform 6.1) fit their token-minimum widths across \linewidth. Only
      -- selected when the larger tiers cannot fit the per-column tokens.
      {name="\\tiny",       cpl=115, cs="2pt"},
    }
    local pad = 1.0          -- breathing room (chars) added to each token width
    -- Leave headroom below 1.0 for the inter-column colsep: tblr forces the table
    -- to width=\linewidth, so if the Q widths + colseps exceed it the columns get
    -- silently compressed below their computed widths and identifiers overrun.
    local usable = 0.93      -- fraction of \linewidth available to column bodies
    local chosen, minfrac
    for _, f in ipairs(fonts) do
      local frac = {}
      local summ = 0
      for i = 1, num_cols do
        frac[i] = (maxtok[i] + pad) / f.cpl
        summ = summ + frac[i]
      end
      if summ <= usable then chosen = f; minfrac = frac; break end
      chosen = f; minfrac = frac   -- keep smallest font as fallback
    end
    -- Distribute leftover width to columns with wrappable excess (prose).
    local summ = 0
    for i = 1, num_cols do summ = summ + minfrac[i] end
    local leftover = usable - summ
    local excess_total = 0
    local excess = {}
    for i = 1, num_cols do
      excess[i] = math.max(0, (maxlen[i] - maxtok[i]))
      excess_total = excess_total + excess[i]
    end
    local width = {}
    for i = 1, num_cols do
      if leftover > 0 and excess_total > 0 then
        width[i] = minfrac[i] + leftover * (excess[i] / excess_total)
      else
        width[i] = minfrac[i]
      end
    end
    table.insert(latex, "  width=\\linewidth,")
    table.insert(latex, "  rowsep=2pt,")
    table.insert(latex, "  colsep=" .. chosen.cs .. ",")
    local colspec_parts = {}
    for i = 1, num_cols do
      colspec_parts[i] = string.format("Q[wd=%.3f\\linewidth,l]", width[i])
    end
    table.insert(latex, "  colspec={" .. table.concat(colspec_parts, " ") .. "},")
    table.insert(latex, "  cells={font=" .. chosen.name .. "},")
    table.insert(latex, "  row{1}={font=" .. chosen.name .. "\\bfseries},")
  elseif tall then
    -- Tall narrow table: compress so all rows + legend fit on one page.
    -- (Companion fix in p2kb-iosp-figures.lua reserves vertical space before the
    -- heading so the whole heading+table+legend unit stays together on one page.)
    table.insert(latex, "  rowsep=0.5pt,")
    table.insert(latex, "  colsep=6pt,")
    local colspec_parts = {}
    for i = 1, num_cols do
      table.insert(colspec_parts, "l")
    end
    table.insert(latex, "  colspec={" .. table.concat(colspec_parts, " ") .. "},")
    table.insert(latex, "  cells={font=\\footnotesize},")
    table.insert(latex, "  row{1}={font=\\footnotesize\\bfseries},")
  else
    -- Narrow table: auto-shrink to content (no width constraint)
    table.insert(latex, "  rowsep=3pt,")
    table.insert(latex, "  colsep=6pt,")
    local colspec_parts = {}
    for i = 1, num_cols do
      table.insert(colspec_parts, "l")
    end
    table.insert(latex, "  colspec={" .. table.concat(colspec_parts, " ") .. "},")
    table.insert(latex, "  row{1}={font=\\bfseries},")
  end
  -- Repeat the header row at the top of each continuation page.
  if use_longtblr then
    table.insert(latex, "  rowhead=1,")
  end
  table.insert(latex, "  hline{1,2}={solid},")
  table.insert(latex, "  hline{Z}={solid},")
  table.insert(latex, "}")

  -- Extract and add header row
  if el.head and el.head.rows and #el.head.rows > 0 then
    local header_row = el.head.rows[1]
    if header_row.cells then
      local headers = {}
      for i, cell in ipairs(header_row.cells) do
        if i <= num_cols then
          table.insert(headers, cell_to_latex(cell))
        end
      end
      if #headers > 0 then
        table.insert(latex, "  " .. table.concat(headers, " & ") .. " \\\\")
      end
    end
  end

  -- Add data rows
  for _, body in ipairs(el.bodies) do
    if body.body then
      for _, row in ipairs(body.body) do
        local cells = {}
        for i, cell in ipairs(row.cells) do
          if i <= num_cols then
            table.insert(cells, cell_to_latex(cell))
          end
        end
        if #cells > 0 then
          table.insert(latex, "  " .. table.concat(cells, " & ") .. " \\\\")
        end
      end
    end
  end

  if use_longtblr then
    table.insert(latex, "\\end{longtblr}")
    -- Breaking longtblr carries its caption via the native [caption=] key above.
    -- Add vertical space after table to separate from following content
    table.insert(latex, "\\vspace{12pt}")
    return pandoc.RawBlock("latex", table.concat(latex, "\n"))
  else
    table.insert(latex, "\\end{tblr}")
    -- Non-breaking tblr -> weld a numbered caption above it via a table[H] float
    local body = wrap_float(table.concat(latex, "\n"), cap, label)
    return pandoc.RawBlock("latex", body .. "\n\\vspace{12pt}")
  end
end

-- Handle content tables (2-8 columns) with page-width constraint
-- CONSERVATIVE: Uses Pandoc's column width hints from markdown, just adds width=\linewidth
-- If no widths specified in markdown, uses equal distribution with last column flexible
local function handle_content_table(el)
  local num_cols = #el.colspecs
  local cap, label = table_caption_and_label(el)

  -- Special handling for "Constant | Value | Description" tables (Appendix E, F)
  -- These need specific widths because Value column has long binary patterns
  local is_const_val_desc = is_constant_value_description_table(el)

  -- Special handling for "Instruction | Description" tables (Appendix B)
  -- These need consistent widths to avoid 50/50 split on shorter tables
  local is_instr_desc = is_instruction_description_table(el)

  -- Special handling for "Operator | Description | Example" tables (Chapter 2)
  -- These need consistent widths to prevent Operator column cramping Description
  local is_op_desc_ex = is_operator_description_example_table(el)

  -- Special handling for Condition Code Table (Chapter 2.2.1)
  -- Needs optimized widths: EEEE is narrow, Aliases needs room for comma-separated lists
  local is_cond_code = is_condition_code_table(el)

  -- Special handling for "Category | Count | Instructions" tables (Chapter 3)
  -- Column 3 has long comma-separated instruction lists that need wrapping
  local is_cat_instr = is_category_instructions_table(el)

  -- Extract column widths from Pandoc's colspecs
  -- colspecs is a list of {alignment, width} pairs
  -- width is nil if not specified, or a fraction (0.0-1.0) of line width
  local widths = {}
  local has_widths = false
  local total_specified = 0

  for i = 1, num_cols do
    local spec = el.colspecs[i]
    if spec and spec[2] then
      widths[i] = spec[2]
      has_widths = true
      total_specified = total_specified + spec[2]
    else
      widths[i] = nil
    end
  end

  -- Special case: Constant | Value | Description tables
  -- Override Pandoc's widths with optimized values for binary/hex content
  -- Appendix E has very long values: %0000_0000_000_0000000000000_00_00000_0 (36 chars)
  -- Appendix F has shorter values: %0000_0000_0000_0000 << 16 (26 chars)
  -- Measure actual content to determine which width profile to use
  if is_const_val_desc then
    -- Measure max length in column 2 (Value column)
    local max_value_len = get_max_column_length(el, 2)

    if max_value_len >= 32 then
      -- Appendix E style: long 36-char binary values
      -- Column 1 (Constant): 17% - max 16 chars like P_DAC_DITHER_RND
      -- Column 2 (Value): 43% - 36-char binary patterns
      -- Column 3 (Description): 35% - more room for descriptions
      widths[1] = 0.17
      widths[2] = 0.43
      widths[3] = 0.35
    else
      -- Appendix F style: shorter 26-char shifted values
      -- Column 1 (Constant): 22% - Column 2 (Value): 32% - Column 3: 41%
      --
      -- The 22% default does NOT fit the 24 chars its old comment claimed.
      -- Measured on the shipped PDF: X_2ADC8_16P_4DAC8_WFLONG renders 129.1pt
      -- wide in IBMPlexMono 9pt, against a 103.0pt column (22% of the 468pt
      -- block). Column 2 starts at x=186.6 while the symbol runs to x=204.8, so
      -- the constant printed ON TOP OF its own value and the bit pattern was
      -- unreadable - in a bit-level constant reference, the one thing the table
      -- exists to convey. It shipped that way for at least two releases.
      --
      -- So size the symbol columns to their content when, and ONLY when, the
      -- default is too narrow. 468pt / 5.38pt-per-char = 87 chars span the
      -- block at this size; 103pt holds 19. Tables at or under 19 keep the
      -- exact fixed widths they render correctly with today.
      --
      -- Blast radius measured, not assumed: of 45 Constant|Value|Description
      -- tables across every master, exactly FOUR exceed 19 chars - two in the
      -- Assembly manual (Appendix G) and two in the Streamer guide. The other
      -- 41 take the unchanged branch and are byte-identical.
      local tok1 = get_max_token_length(el, 1)
      if tok1 > 19 then
        local tok2 = get_max_token_length(el, 2)
        widths[1] = math.min(0.45, (tok1 + 1.5) / 87)
        widths[2] = math.min(0.40, (tok2 + 1.5) / 87)
        widths[3] = math.max(0.25, 0.95 - widths[1] - widths[2])
      else
        widths[1] = 0.22
        widths[2] = 0.32
        widths[3] = 0.41
      end
    end
    has_widths = true
  elseif is_instr_desc then
    -- Symbol/Instruction | Description tables (Appendix B, platform 6.2).
    -- Column 1 is a fixed Q[wd] column, so a long unbreakable symbol like
    -- P_OE_FLOAT_LOW_1K5_PULLUP_FILTER (32 chars) overflows into the description
    -- unless the column is at least as wide as that token. Size column 1 to its
    -- longest token (never split the symbol) instead of a fixed 18%: ~60 chars
    -- span \linewidth at the body \normalsize, +1 char breathing room. Floor at
    -- 0.18 (keep short-name tables compact) and cap at 0.55 (always leave the
    -- description a readable half). Column 2 takes the rest.
    local tok1 = get_max_token_length(el, 1)
    local need1 = (tok1 + 1) / 60
    widths[1] = math.max(0.18, math.min(0.55, need1))
    widths[2] = 0.95 - widths[1]
    has_widths = true
  elseif is_op_desc_ex then
    -- Operator | Description | Example tables (Chapter 2)
    -- Column 1 (Operator): 12% - short symbols like `+`, `>>`, `#>`
    -- Column 2 (Description): 43% - medium text like "Bitwise NOT (invert all bits)"
    -- Column 3 (Example): 40% - code examples like `$80 >> 4` → `$08`
    widths[1] = 0.12
    widths[2] = 0.43
    widths[3] = 0.40
    has_widths = true
  elseif is_cond_code then
    -- Condition Code Table (Chapter 2.2.1)
    -- Column 1 (EEEE): 6% - just 4 chars like "0000"
    -- Column 2 (Primary Mnemonic): 16% - like "IF_NC_AND_NZ"
    -- Column 3 (Aliases): 30% - comma-separated lists like "IF_NZ_AND_NC, IF_GT, IF_A, IF_00"
    -- Column 4 (Condition): 13% - like "C=0 AND Z=0"
    -- Column 5 (Description): 30% - explanatory text
    widths[1] = 0.06
    widths[2] = 0.16
    widths[3] = 0.30
    widths[4] = 0.13
    widths[5] = 0.30
    has_widths = true
  elseif is_cat_instr then
    -- Tables with long instruction lists in column 2 or 3
    -- Check which pattern we have by looking at headers
    local h2 = ""
    if el.head and el.head.rows and #el.head.rows > 0 then
      local header_row = el.head.rows[1]
      if header_row.cells and header_row.cells[2] then
        h2 = pandoc.utils.stringify(header_row.cells[2].contents):lower()
      end
    end

    if h2:match("instruction") then
      -- "Family | Instructions | Operation" pattern
      -- Column 1 (Family): 10% - like "BIT*", "DIR*"
      -- Column 2 (Instructions): 55% - comma-separated lists
      -- Column 3 (Operation): 30% - short descriptions
      widths[1] = 0.10
      widths[2] = 0.55
      widths[3] = 0.30
    elseif h2:match("mode") or h2:match("example") then
      -- "Category | Example Modes | Typical Applications" pattern (Chapter 5)
      -- Column 1 (Category): 12% - like "Digital I/O", "Serial"
      -- Column 2 (Example Modes): 40% - comma-separated mode names
      -- Column 3 (Typical Applications): 43% - comma-separated application descriptions
      widths[1] = 0.12
      widths[2] = 0.40
      widths[3] = 0.43
    elseif h2:match("effect") then
      -- "Category | Allowed Effects | Reason" pattern (Appendix C)
      -- Column 1 (Category): 12% - like "Full", "Extended"
      -- Column 2 (Allowed Effects): 45% - lists like "WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, XORZ"
      -- Column 3 (Reason): 38% - explanatory text
      widths[1] = 0.12
      widths[2] = 0.45
      widths[3] = 0.38
    else
      -- "Category | Count | Instructions" pattern
      -- Column 1 (Category): 18% - like "Full (WC/WZ/WCZ)"
      -- Column 2 (Count): 8% - just numbers like "~300"
      -- Column 3 (Instructions): 69% - long comma-separated instruction lists
      widths[1] = 0.18
      widths[2] = 0.08
      widths[3] = 0.69
    end
    has_widths = true
  elseif has_widths and total_specified > 0 then
    -- Scale widths to sum to ~0.95 (leave room for padding)
    local scale = 0.95 / total_specified
    for i = 1, num_cols do
      if widths[i] then
        widths[i] = widths[i] * scale
      end
    end
  else
    -- No widths specified: give equal space to first N-1 cols, last col gets remainder
    -- This ensures last column (usually description) can wrap
    local per_col = 0.15  -- ~15% each for narrow columns
    local max_for_narrow = 0.60  -- max 60% for narrow columns combined

    if (num_cols - 1) * per_col > max_for_narrow then
      per_col = max_for_narrow / (num_cols - 1)
    end

    for i = 1, num_cols - 1 do
      widths[i] = per_col
    end
    -- Last column is flexible (X type in tabularray)
    widths[num_cols] = nil  -- will use X
  end

  -- Helper to render cell contents as LaTeX
  local function cell_to_latex(cell)
    if not cell or not cell.contents then
      return ""
    end
    if #cell.contents == 0 then
      return ""
    end
    -- cell.contents is a list of Blocks, use pandoc.write directly
    local ok, result = pcall(function()
      local doc = pandoc.Pandoc(cell.contents)
      local latex_str = pandoc.write(doc, "latex")
      if latex_str then
        return latex_str:gsub("\n$", "")
      else
        -- stringify does NOT escape; this lands raw in a tblr cell
        return cell_escape(pandoc.utils.stringify(cell.contents))
      end
    end)
    if ok then
      return result or ""
    else
      -- Fallback to stringify if pandoc.write fails (escaped -- raw tblr cell)
      return cell_escape(pandoc.utils.stringify(cell.contents)) or ""
    end
  end

  -- Count rows to decide between tblr and longtblr
  -- Threshold lowered to 12 because tables with wrapped content (like Condition Code Table
  -- with 16 rows) can exceed one page height even with fewer rows
  local row_count = count_data_rows(el)
  local use_longtblr = row_count > 12  -- Use longtblr for tables with 12+ rows

  -- Build tabularray LaTeX
  local latex = {}
  if use_longtblr then
    table.insert(latex, longtblr_begin(cap, label))
  else
    table.insert(latex, "\\begin{tblr}{")
  end
  table.insert(latex, "  width=\\linewidth,")

  -- Use tighter spacing for Constant|Value|Description tables
  if is_const_val_desc then
    table.insert(latex, "  rowsep=2pt,")
    table.insert(latex, "  colsep=4pt,")
  else
    table.insert(latex, "  rowsep=3pt,")
    table.insert(latex, "  colsep=6pt,")
  end

  -- Column specifications
  -- Build colspec string for tabularray
  local colspec_parts = {}
  for i = 1, num_cols do
    if widths[i] then
      table.insert(colspec_parts, string.format("Q[wd=%.3f\\linewidth, l]", widths[i]))
    else
      -- Flexible column (X type) - takes remaining space and wraps
      table.insert(colspec_parts, "X[l]")
    end
  end
  table.insert(latex, "  colspec={" .. table.concat(colspec_parts, " ") .. "},")

  -- Styling for Constant|Value|Description tables: smaller monospace font
  if is_const_val_desc then
    table.insert(latex, "  row{1}={font=\\bfseries\\footnotesize},")
    table.insert(latex, "  row{2-Z}={font=\\ttfamily\\footnotesize},")
  else
    -- Styling: bold header row
    table.insert(latex, "  row{1}={font=\\bfseries},")
  end

  -- For longtblr, repeat header row on each page (inner key for older tabularray)
  if use_longtblr then
    table.insert(latex, "  rowhead=1,")
  end

  table.insert(latex, "  hline{1,2}={solid},")
  table.insert(latex, "  hline{Z}={solid},")
  table.insert(latex, "}")

  -- Extract and add header row
  if el.head and el.head.rows and #el.head.rows > 0 then
    local header_row = el.head.rows[1]
    if header_row.cells then
      local headers = {}
      for i, cell in ipairs(header_row.cells) do
        if i <= num_cols then
          table.insert(headers, cell_to_latex(cell))
        end
      end
      if #headers > 0 then
        table.insert(latex, "  " .. table.concat(headers, " & ") .. " \\\\")
      end
    end
  end

  -- Add data rows
  for _, body in ipairs(el.bodies) do
    if body.body then
      for _, row in ipairs(body.body) do
        local cells = {}
        for i, cell in ipairs(row.cells) do
          if i <= num_cols then
            table.insert(cells, cell_to_latex(cell))
          end
        end
        if #cells > 0 then
          table.insert(latex, "  " .. table.concat(cells, " & ") .. " \\\\")
        end
      end
    end
  end

  if use_longtblr then
    table.insert(latex, "\\end{longtblr}")
    -- Breaking longtblr carries its caption via the native [caption=] key above.
    return pandoc.RawBlock("latex", table.concat(latex, "\n"))
  else
    table.insert(latex, "\\end{tblr}")
    -- Non-breaking tblr -> weld a numbered caption above it via a table[H] float
    return pandoc.RawBlock("latex", wrap_float(table.concat(latex, "\n"), cap, label))
  end
end

function Table(el)
  -- Get number of columns
  local num_cols = #el.colspecs

  -- Handle 9-column encoding tables specially (fixed widths with colored headers)
  if num_cols == 9 then
    return handle_encoding_table(el)
  end

  -- Handle 6-column encoding master table (Appendix A) - uses longtable for page breaks
  if num_cols == 6 and is_encoding_master_table(el) then
    return handle_encoding_master_table(el)
  end

  -- Handle tables that NEED full page width (long content patterns)
  -- These would overflow if auto-shrunk
  if num_cols >= 2 and num_cols <= 8 and needs_full_width(el) then
    return handle_content_table(el)
  end

  -- Default: auto-shrink tables to content width. The wide branch allocates a
  -- token-fit fixed width per column and shrinks the font as needed, so this also
  -- covers many-column tables (up to 12) that would otherwise fall to pandoc's
  -- narrow defaults and overlap (platform 6.1, a 10-column table). 9-column
  -- encoding tables are already handled above and never reach here.
  if num_cols >= 2 and num_cols <= 12 then
    return handle_auto_shrink_table(el)
  end

  -- For tables outside our handling (1 column or 13+ columns), pass through
  return el
end
