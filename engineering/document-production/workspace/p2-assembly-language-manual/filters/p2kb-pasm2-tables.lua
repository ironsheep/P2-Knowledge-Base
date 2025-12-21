-- P2KB PASM2 Table Formatting Filter
-- Auto-shrink tables to content width, full-width only when needed
-- Author: Iron Sheep Productions, LLC
-- Version: 6.2 - Extended 2-column full-width detection (Description, Behavior, Explanation)
--
-- Strategy:
-- - 9-column encoding tables: Fixed widths with colored headers (tabularray)
-- - Tables with long content patterns: Full page width with proportional columns
--   * Constant | Value | Description (36-char binary patterns)
--   * Condition Code tables (long alias lists)
--   * Instruction | Description (Appendix B style)
-- - All other tables: Auto-shrink to content width (no wrapping)
-- - This produces cleaner output for short explanatory tables

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

-- Handle 9-column encoding tables specially
-- Columns 1-5 are fixed-width bit fields (EEEE, Opcode, CZI, D, S)
-- Columns 6-9 are variable content (C, Z, Result, Clks)
-- Strategy: Set minimums for C, Z, Clks based on max content; give remainder to Result
-- Emits raw LaTeX tabularray with colored header zones
local function handle_encoding_table(el)
  -- Fixed widths for bit field columns (total: ~0.43)
  -- NOTE: Cols 1 & 3 have preto/appto padding (8pt total each)
  -- Redistributed: took 0.010 from Opcode, 0.005 from CZI, gave to EEEE
  local fixed_widths = {
    0.070,  -- Col 1: EEEE (4 chars + 8pt padding) - was 0.055, increased to prevent line-wrap
    0.090,  -- Col 2: Opcode (7 chars) - was 0.100, reduced slightly
    0.050,  -- Col 3: CZI (3 chars + 8pt padding) - was 0.055, reduced to balance whitespace
    0.110,  -- Col 4: D (9 chars)
    0.110,  -- Col 5: S (9 chars)
  }

  -- Total available for columns 6-9 (leave margin for borders/padding)
  -- Fixed cols total ~0.43, so remaining is ~0.52 for flexible cols + margins
  local remaining = 0.52

  -- Measure content length in columns 6-9
  local content_lens = {}
  for i = 6, 9 do
    content_lens[i] = get_max_column_length(el, i)
  end

  -- Calculate widths based on content with minimum constraints
  -- Strategy: Calculate what each column NEEDS, then distribute remaining space proportionally
  -- C (col 6): min 0.06, content like "DIRx + OUTx" needs more
  -- Z (col 7): min 0.06, content like "Z AND (D == S + C)" needs more
  -- Result (col 8): min 0.15, typically short content like "OUT bit"
  -- Clks (col 9): min 0.06, typically "2" or similar

  local flex_widths = {}

  -- Width per character (approximate) - about 0.008 per char for small font
  local char_width = 0.008

  -- Calculate content-based width for each column
  local c_need = math.max(0.06, content_lens[6] * char_width + 0.02)
  local z_need = math.max(0.06, content_lens[7] * char_width + 0.02)
  local result_need = math.max(0.15, content_lens[8] * char_width + 0.02)
  local clks_need = math.max(0.06, content_lens[9] * char_width + 0.02)

  local total_need = c_need + z_need + result_need + clks_need

  -- If total need fits in remaining, use proportional distribution
  -- Otherwise, cap the largest columns and give priority to C and Z (flag columns)
  if total_need <= remaining then
    -- Everything fits - distribute extra space proportionally
    local extra = remaining - total_need
    local scale = 1 + (extra / total_need)
    flex_widths[6] = c_need * scale
    flex_widths[7] = z_need * scale
    flex_widths[8] = result_need * scale
    flex_widths[9] = clks_need * scale
  else
    -- Need to fit into remaining - prioritize C and Z, cap Result
    flex_widths[6] = math.min(c_need, 0.14)
    flex_widths[7] = math.min(z_need, 0.12)
    flex_widths[9] = math.min(clks_need, 0.10)
    local used = flex_widths[6] + flex_widths[7] + flex_widths[9]
    flex_widths[8] = math.max(0.15, remaining - used)
  end

  -- Build tabularray LaTeX with colored headers
  -- Header color zones:
  --   Cols 1-3 (EEEE, Opcode, CZI): pasm2-enc-instruction (light blue)
  --   Cols 4-5 (D, S): pasm2-enc-operand (light green)
  --   Cols 6-7 (C, Z): pasm2-enc-flags (light orange)
  --   Cols 8-9 (Result, Clks): pasm2-enc-result (light gray)

  -- Count rows to decide between tblr and longtblr
  -- Encoding tables like Appendix A can have 300+ rows
  local row_count = count_data_rows(el)
  local use_longtblr = row_count > 20  -- Use longtblr for tables with 20+ rows

  local latex = {}
  if use_longtblr then
    table.insert(latex, "\\begin{longtblr}{")
  else
    table.insert(latex, "\\begin{tblr}{")
  end
  table.insert(latex, "  width=\\linewidth,")
  table.insert(latex, "  rowsep=2pt,")
  table.insert(latex, "  colsep=4pt,")
  -- Column widths (all centered, Result too since user wants centered)
  table.insert(latex, string.format("  column{1}={wd=%.3f\\linewidth, halign=c, font=\\ttfamily\\small},", fixed_widths[1]))
  table.insert(latex, string.format("  column{2}={wd=%.3f\\linewidth, halign=c, font=\\ttfamily\\small},", fixed_widths[2]))
  table.insert(latex, string.format("  column{3}={wd=%.3f\\linewidth, halign=c, font=\\ttfamily\\small},", fixed_widths[3]))
  table.insert(latex, string.format("  column{4}={wd=%.3f\\linewidth, halign=c, font=\\ttfamily\\small},", fixed_widths[4]))
  table.insert(latex, string.format("  column{5}={wd=%.3f\\linewidth, halign=c, font=\\ttfamily\\small},", fixed_widths[5]))
  table.insert(latex, string.format("  column{6}={wd=%.3f\\linewidth, halign=c, font=\\small},", flex_widths[6]))
  table.insert(latex, string.format("  column{7}={wd=%.3f\\linewidth, halign=c, font=\\small},", flex_widths[7]))
  table.insert(latex, string.format("  column{8}={wd=%.3f\\linewidth, halign=c, font=\\small},", flex_widths[8]))
  table.insert(latex, string.format("  column{9}={wd=%.3f\\linewidth, halign=c, font=\\small},", flex_widths[9]))
  -- Header row styling with color zones and inner padding
  -- Add padding to narrow columns (EEEE, CZI) so text doesn't butt against borders
  table.insert(latex, "  row{1}={font=\\bfseries\\footnotesize},")
  table.insert(latex, "  cell{1}{1}={bg=pasm2-enc-instruction, preto={\\hspace{4pt}}, appto={\\hspace{4pt}}},")
  table.insert(latex, "  cell{1}{2}={bg=pasm2-enc-instruction},")
  table.insert(latex, "  cell{1}{3}={bg=pasm2-enc-instruction, preto={\\hspace{4pt}}, appto={\\hspace{4pt}}},")
  table.insert(latex, "  cell{1}{4-5}={bg=pasm2-enc-operand},")
  table.insert(latex, "  cell{1}{6-7}={bg=pasm2-enc-flags},")
  table.insert(latex, "  cell{1}{8-9}={bg=pasm2-enc-result},")
  -- For longtblr, repeat header row on each page
  if use_longtblr then
    table.insert(latex, "  rowhead=1,")
  end
  table.insert(latex, "  hlines,")
  table.insert(latex, "  vlines,")
  table.insert(latex, "}")

  -- Helper to render cell contents as LaTeX
  -- Also handles \textsuperscript{N} patterns that come from markdown as literal text
  local function cell_to_latex(cell)
    if not cell or not cell.contents then
      return ""
    end
    local content = cell.contents
    if #content == 0 then
      return ""
    end
    -- Get plain text first
    local text = pandoc.utils.stringify(content)
    -- The \textsuperscript pattern is stored as literal text in markdown
    -- We need to ensure the backslash is preserved for LaTeX
    -- In the markdown, it's written as \textsuperscript{1} but pandoc reads
    -- the backslash as literal, so stringify gives us "\\textsuperscript{1}"
    -- which when output to LaTeX becomes the correct command
    -- Actually, let's check what we get and ensure it works:
    -- If text contains the pattern, it should work as-is since we're emitting raw LaTeX
    return text
  end

  -- Extract header row (should be first row from markdown table)
  local headers = {"EEEE", "Opcode", "CZI", "Dest", "Src", "C", "Z", "Result", "Clks"}

  -- Check if table has header
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

  table.insert(latex, "  " .. table.concat(headers, " & ") .. " \\\\")

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

  if use_longtblr then
    table.insert(latex, "\\end{longtblr}")
  else
    table.insert(latex, "\\end{tblr}")
  end

  -- Return as RawBlock
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

  return false
end

-- Handle auto-shrink tables: no width constraint, columns size to content
local function handle_auto_shrink_table(el)
  local num_cols = #el.colspecs

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
        return pandoc.utils.stringify(cell.contents)
      end
    end)
    if ok then
      return result or ""
    else
      return pandoc.utils.stringify(cell.contents) or ""
    end
  end

  -- Build tabularray LaTeX WITHOUT width=\linewidth (auto-shrink)
  local latex = {}
  table.insert(latex, "\\begin{tblr}{")
  -- No width specification - table shrinks to content
  table.insert(latex, "  rowsep=3pt,")
  table.insert(latex, "  colsep=6pt,")

  -- All columns use auto-width left-aligned
  local colspec_parts = {}
  for i = 1, num_cols do
    table.insert(colspec_parts, "l")
  end
  table.insert(latex, "  colspec={" .. table.concat(colspec_parts, " ") .. "},")

  -- Styling: bold header row
  table.insert(latex, "  row{1}={font=\\bfseries},")
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

  table.insert(latex, "\\end{tblr}")
  -- Add vertical space after table to separate from following content
  table.insert(latex, "\\vspace{12pt}")

  return pandoc.RawBlock("latex", table.concat(latex, "\n"))
end

-- Handle content tables (2-8 columns) with page-width constraint
-- CONSERVATIVE: Uses Pandoc's column width hints from markdown, just adds width=\linewidth
-- If no widths specified in markdown, uses equal distribution with last column flexible
local function handle_content_table(el)
  local num_cols = #el.colspecs

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
      -- Column 1 (Constant): 22% - max 24 chars like X_2ADC8_16P_4DAC8_WFLONG
      -- Column 2 (Value): 32% - 26-char shifted patterns
      -- Column 3 (Description): 41% - much more room for descriptions
      widths[1] = 0.22
      widths[2] = 0.32
      widths[3] = 0.41
    end
    has_widths = true
  elseif is_instr_desc then
    -- Instruction | Description tables (Appendix B)
    -- Force consistent widths: 18% instruction name, 77% description
    -- This prevents Pandoc from inferring 50/50 on shorter tables
    widths[1] = 0.18
    widths[2] = 0.77
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
        return pandoc.utils.stringify(cell.contents)
      end
    end)
    if ok then
      return result or ""
    else
      -- Fallback to stringify if pandoc.write fails
      return pandoc.utils.stringify(cell.contents) or ""
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
    -- longtblr allows page breaks within table; no caption/label needed
    table.insert(latex, "\\begin{longtblr}{")
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

  -- For longtblr, specify header row to repeat on each page
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
  else
    table.insert(latex, "\\end{tblr}")
  end

  return pandoc.RawBlock("latex", table.concat(latex, "\n"))
end

function Table(el)
  -- Get number of columns
  local num_cols = #el.colspecs

  -- Handle 9-column encoding tables specially (fixed widths with colored headers)
  if num_cols == 9 then
    return handle_encoding_table(el)
  end

  -- Handle tables that NEED full page width (long content patterns)
  -- These would overflow if auto-shrunk
  if num_cols >= 2 and num_cols <= 8 and needs_full_width(el) then
    return handle_content_table(el)
  end

  -- Default: auto-shrink tables to content width (no wrapping)
  -- This produces cleaner output for short explanatory tables
  if num_cols >= 2 and num_cols <= 8 then
    return handle_auto_shrink_table(el)
  end

  -- For tables outside our handling (1 column or 10+ columns), pass through
  return el
end
