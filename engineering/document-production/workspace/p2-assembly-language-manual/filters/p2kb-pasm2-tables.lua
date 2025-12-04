-- P2KB PASM2 Table Formatting Filter
-- Makes content tables full width and adjusts column ratios based on content
-- INCLUDES special handling for 9-column encoding tables
-- Author: Iron Sheep Productions, LLC
-- Version: 3.0 - Content-aware column width selection including encoding tables
--
-- This filter analyzes table content to choose appropriate column widths:
-- - Short columns (codes, labels) get minimal width
-- - Description columns (typically last) get maximum width
-- - Prevents unnecessary text wrapping in description columns
-- - 9-column encoding tables: fixed widths for cols 1-5, proportional for 6-9

-- Get maximum text length in a column across all rows
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

-- Classify column width needs based on max content length
-- Returns: "tiny" (<= 12 chars), "small" (<= 25 chars), "medium" (<= 50 chars), "large" (> 50 chars)
local function classify_column(max_len)
  if max_len <= 12 then
    return "tiny"
  elseif max_len <= 25 then
    return "small"
  elseif max_len <= 50 then
    return "medium"
  else
    return "large"
  end
end

-- Handle 9-column encoding tables specially
-- Columns 1-5 are fixed-width bit fields (EEEE, Opcode, CZI, D, S)
-- Columns 6-9 are variable content (C, Z, Result, Clks)
-- Strategy: Set minimums for C, Z, Clks based on max content; give remainder to Result
-- Emits raw LaTeX tabularray with colored header zones
local function handle_encoding_table(el)
  -- Fixed widths for bit field columns (total: ~0.41)
  local fixed_widths = {
    0.055,  -- Col 1: EEEE (4 chars)
    0.100,  -- Col 2: Opcode (7 chars)
    0.035,  -- Col 3: CZI (3 chars)
    0.110,  -- Col 4: D (9 chars)
    0.110,  -- Col 5: S (9 chars)
  }

  -- Total available for columns 6-9 (leave margin for borders/padding)
  local remaining = 0.54

  -- Measure content length in columns 6-9
  local content_lens = {}
  for i = 6, 9 do
    content_lens[i] = get_max_column_length(el, i)
  end

  -- Calculate widths based on content with minimum constraints
  -- C (col 6): min 0.06, scale up for long content like "correct sign of..."
  -- Z (col 7): min 0.06, scale up for long content like "Z AND (D == S + C)"
  -- Clks (col 9): min 0.08, scale up for long content like "2 or WRFAST finish..."
  -- Result (col 8): gets whatever remains (at least 0.20)

  local flex_widths = {}

  -- Width per character (approximate) - about 0.007 per char for small font
  local char_width = 0.007

  -- Column 6 (C): minimum 0.06, or content-based
  local c_content_width = content_lens[6] * char_width
  flex_widths[6] = math.max(0.06, math.min(c_content_width + 0.02, 0.18))

  -- Column 7 (Z): minimum 0.06, or content-based
  local z_content_width = content_lens[7] * char_width
  flex_widths[7] = math.max(0.06, math.min(z_content_width + 0.02, 0.14))

  -- Column 9 (Clks): minimum 0.08, or content-based
  local clks_content_width = content_lens[9] * char_width
  flex_widths[9] = math.max(0.08, math.min(clks_content_width + 0.02, 0.22))

  -- Column 8 (Result): gets the remainder, minimum 0.20
  local used = flex_widths[6] + flex_widths[7] + flex_widths[9]
  flex_widths[8] = math.max(0.20, remaining - used)

  -- Build tabularray LaTeX with colored headers
  -- Header color zones:
  --   Cols 1-3 (EEEE, Opcode, CZI): pasm2-enc-instruction (light blue)
  --   Cols 4-5 (D, S): pasm2-enc-operand (light green)
  --   Cols 6-7 (C, Z): pasm2-enc-flags (light orange)
  --   Cols 8-9 (Result, Clks): pasm2-enc-result (light gray)

  local latex = {}
  table.insert(latex, "\\begin{tblr}{")
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
  table.insert(latex, "  row{1}={font=\\bfseries\\small},")
  table.insert(latex, "  cell{1}{1}={bg=pasm2-enc-instruction, preto={\\hspace{4pt}}, appto={\\hspace{4pt}}},")
  table.insert(latex, "  cell{1}{2}={bg=pasm2-enc-instruction},")
  table.insert(latex, "  cell{1}{3}={bg=pasm2-enc-instruction, preto={\\hspace{4pt}}, appto={\\hspace{4pt}}},")
  table.insert(latex, "  cell{1}{4-5}={bg=pasm2-enc-operand},")
  table.insert(latex, "  cell{1}{6-7}={bg=pasm2-enc-flags},")
  table.insert(latex, "  cell{1}{8-9}={bg=pasm2-enc-result},")
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
  local headers = {"EEEE", "Opcode", "CZI", "D", "S", "C", "Z", "Result", "Clks"}

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

  table.insert(latex, "\\end{tblr}")

  -- Return as RawBlock
  return pandoc.RawBlock("latex", table.concat(latex, "\n"))
end

function Table(el)
  -- Get number of columns
  local num_cols = #el.colspecs

  -- Handle 9-column encoding tables specially
  if num_cols == 9 then
    return handle_encoding_table(el)
  end

  -- Skip tables with 8 columns (rare, might be encoding variants)
  if num_cols == 8 then
    return el
  end

  -- Only modify tables that don't already have explicit widths
  if el.colspecs[1] and el.colspecs[1][2] and el.colspecs[1][2] > 0 then
    return el
  end

  -- Analyze each column's content
  local col_classes = {}
  for i = 1, num_cols do
    local max_len = get_max_column_length(el, i)
    col_classes[i] = classify_column(max_len)
  end

  if num_cols == 2 then
    -- 2-column tables: proportional based on actual content lengths
    -- Give more space to the column that needs it
    local len1 = get_max_column_length(el, 1)
    local len2 = get_max_column_length(el, 2)
    local total = len1 + len2

    -- Calculate proportional widths with constraints
    -- Min width 0.10 for any column, max 0.85 for description column
    local w1 = math.max(0.10, math.min(0.35, (len1 / total) * 0.95))
    local w2 = 0.95 - w1

    -- If col1 data is very short (like 3-char codes), shrink further
    -- Check data rows only (not header) for this
    local data_len1 = 0
    for _, body in ipairs(el.bodies) do
      if body.body then
        for _, row in ipairs(body.body) do
          if row.cells and row.cells[1] then
            local text = pandoc.utils.stringify(row.cells[1].contents)
            if #text > data_len1 then data_len1 = #text end
          end
        end
      end
    end

    -- If data is much shorter than header, use data length for sizing
    if data_len1 < len1 * 0.5 and data_len1 <= 10 then
      w1 = math.max(0.10, (data_len1 + 2) * 0.01)  -- ~1% per char + padding
      w2 = 0.95 - w1
    end

    el.colspecs[1] = {pandoc.AlignLeft, w1}
    el.colspecs[2] = {pandoc.AlignLeft, w2}

  elseif num_cols == 3 then
    -- 3-column tables: proportional based on DATA content (not headers)
    -- Headers can wrap, but data determines visual "right size"

    -- Get header lengths
    local hdr1, hdr2, hdr3 = 0, 0, 0
    if el.head and el.head.rows and #el.head.rows > 0 then
      local hrow = el.head.rows[1]
      if hrow.cells then
        if hrow.cells[1] then hdr1 = #pandoc.utils.stringify(hrow.cells[1].contents) end
        if hrow.cells[2] then hdr2 = #pandoc.utils.stringify(hrow.cells[2].contents) end
        if hrow.cells[3] then hdr3 = #pandoc.utils.stringify(hrow.cells[3].contents) end
      end
    end

    -- Get max data lengths (body rows only)
    local data1, data2, data3 = 0, 0, 0
    for _, body in ipairs(el.bodies) do
      if body.body then
        for _, row in ipairs(body.body) do
          if row.cells then
            if row.cells[1] then
              local len = #pandoc.utils.stringify(row.cells[1].contents)
              if len > data1 then data1 = len end
            end
            if row.cells[2] then
              local len = #pandoc.utils.stringify(row.cells[2].contents)
              if len > data2 then data2 = len end
            end
            if row.cells[3] then
              local len = #pandoc.utils.stringify(row.cells[3].contents)
              if len > data3 then data3 = len end
            end
          end
        end
      end
    end

    -- Use data length for sizing, but ensure header fits (with some wrapping allowed)
    -- If header is much longer than data, use data length + small buffer
    local len1 = data1
    local len2 = data2
    local len3 = data3

    -- If header is > 1.5x data, header can wrap - use data length + buffer
    if hdr1 > data1 * 1.5 and data1 > 0 then len1 = data1 + 3 else len1 = math.max(data1, hdr1) end
    if hdr2 > data2 * 1.5 and data2 > 0 then len2 = data2 + 3 else len2 = math.max(data2, hdr2) end
    if hdr3 > data3 * 1.5 and data3 > 0 then len3 = data3 + 3 else len3 = math.max(data3, hdr3) end

    -- Ensure minimums
    len1 = math.max(len1, 5)
    len2 = math.max(len2, 5)
    len3 = math.max(len3, 5)

    local total = len1 + len2 + len3

    -- Check for "long description" pattern: one column much longer than others
    -- Example: CORDIC table has col3 = 53 chars, col1 = 17, col2 = 8
    -- In this case, short columns should get tight widths, long column gets rest
    local max_len = math.max(len1, len2, len3)
    local short_threshold = 20  -- Columns under this are "short"
    local long_threshold = 40   -- Columns over this are "long descriptions"

    local w1, w2, w3

    -- If one column is very long (>40) and others are relatively short (<20)
    -- give the long column maximum space
    if len3 > long_threshold and len1 < short_threshold and len2 < short_threshold then
      -- Col 3 is long description, cols 1+2 are short
      -- Calculate tight widths for short columns based on content
      w1 = math.max(0.10, len1 * 0.008)  -- ~0.8% per char
      w2 = math.max(0.08, len2 * 0.008)
      w3 = 0.95 - w1 - w2
    elseif len1 > long_threshold and len2 < short_threshold and len3 < short_threshold then
      -- Col 1 is long description
      w2 = math.max(0.08, len2 * 0.008)
      w3 = math.max(0.08, len3 * 0.008)
      w1 = 0.95 - w2 - w3
    elseif len2 > long_threshold and len1 < short_threshold and len3 < short_threshold then
      -- Col 2 is long description
      w1 = math.max(0.10, len1 * 0.008)
      w3 = math.max(0.08, len3 * 0.008)
      w2 = 0.95 - w1 - w3
    else
      -- Normal proportional calculation
      local total = len1 + len2 + len3
      w1 = (len1 / total) * 0.95
      w2 = (len2 / total) * 0.95
      w3 = (len3 / total) * 0.95

      -- Apply minimums - use smaller minimum (0.06) for short columns
      local min1 = (len1 <= 12) and 0.06 or 0.08
      local min2 = (len2 <= 12) and 0.06 or 0.08
      local min3 = (len3 <= 12) and 0.06 or 0.08

      w1 = math.max(min1, w1)
      w2 = math.max(min2, w2)
      w3 = math.max(min3, w3)

      -- Normalize to 0.95 total
      local sum = w1 + w2 + w3
      local scale = 0.95 / sum
      w1 = w1 * scale
      w2 = w2 * scale
      w3 = w3 * scale
    end

    el.colspecs[1] = {pandoc.AlignLeft, w1}
    el.colspecs[2] = {pandoc.AlignLeft, w2}
    el.colspecs[3] = {pandoc.AlignLeft, w3}

  elseif num_cols == 4 then
    -- 4-column tables: content-aware widths to avoid overlap
    local c1 = col_classes[1]
    local c2 = col_classes[2]
    local c3 = col_classes[3]

    -- Get actual content lengths for more precise sizing
    local len1 = get_max_column_length(el, 1)
    local len2 = get_max_column_length(el, 2)
    local len3 = get_max_column_length(el, 3)
    local len4 = get_max_column_length(el, 4)

    if c1 == "tiny" and c2 == "tiny" and c3 == "tiny" then
      -- All three leading columns are short
      -- But check if col2 is at the upper edge of "tiny" (10-12 chars)
      -- Example: Condition Code Table has IF_NC_AND_NZ (12 chars)
      if len2 >= 10 then
        -- Col2 needs more room: 10/18/12/55
        el.colspecs[1] = {pandoc.AlignLeft, 0.10}
        el.colspecs[2] = {pandoc.AlignLeft, 0.18}
        el.colspecs[3] = {pandoc.AlignLeft, 0.12}
        el.colspecs[4] = {pandoc.AlignLeft, 0.55}
      else
        -- Truly short columns: 12/12/12/59
        el.colspecs[1] = {pandoc.AlignLeft, 0.12}
        el.colspecs[2] = {pandoc.AlignLeft, 0.12}
        el.colspecs[3] = {pandoc.AlignLeft, 0.12}
        el.colspecs[4] = {pandoc.AlignLeft, 0.59}
      end
    elseif c1 == "tiny" and c2 == "tiny" then
      -- Two short columns, third is longer: 12/12/20/51
      el.colspecs[1] = {pandoc.AlignLeft, 0.12}
      el.colspecs[2] = {pandoc.AlignLeft, 0.12}
      el.colspecs[3] = {pandoc.AlignLeft, 0.20}
      el.colspecs[4] = {pandoc.AlignLeft, 0.51}
    elseif c1 == "tiny" then
      -- One short column: 12/20/20/43
      el.colspecs[1] = {pandoc.AlignLeft, 0.12}
      el.colspecs[2] = {pandoc.AlignLeft, 0.20}
      el.colspecs[3] = {pandoc.AlignLeft, 0.20}
      el.colspecs[4] = {pandoc.AlignLeft, 0.43}
    else
      -- Default: roughly equal
      el.colspecs[1] = {pandoc.AlignLeft, 0.20}
      el.colspecs[2] = {pandoc.AlignLeft, 0.20}
      el.colspecs[3] = {pandoc.AlignLeft, 0.20}
      el.colspecs[4] = {pandoc.AlignLeft, 0.35}
    end

  elseif num_cols == 5 then
    -- 5-column tables: give more to last column
    local c1 = col_classes[1]
    local c2 = col_classes[2]

    if c1 == "tiny" and c2 == "tiny" then
      el.colspecs[1] = {pandoc.AlignLeft, 0.08}
      el.colspecs[2] = {pandoc.AlignLeft, 0.08}
      el.colspecs[3] = {pandoc.AlignLeft, 0.15}
      el.colspecs[4] = {pandoc.AlignLeft, 0.15}
      el.colspecs[5] = {pandoc.AlignLeft, 0.49}
    else
      el.colspecs[1] = {pandoc.AlignLeft, 0.12}
      el.colspecs[2] = {pandoc.AlignLeft, 0.12}
      el.colspecs[3] = {pandoc.AlignLeft, 0.15}
      el.colspecs[4] = {pandoc.AlignLeft, 0.15}
      el.colspecs[5] = {pandoc.AlignLeft, 0.41}
    end

  elseif num_cols == 6 then
    -- 6-column tables
    el.colspecs[1] = {pandoc.AlignLeft, 0.10}
    el.colspecs[2] = {pandoc.AlignLeft, 0.10}
    el.colspecs[3] = {pandoc.AlignLeft, 0.12}
    el.colspecs[4] = {pandoc.AlignLeft, 0.12}
    el.colspecs[5] = {pandoc.AlignLeft, 0.15}
    el.colspecs[6] = {pandoc.AlignLeft, 0.36}

  elseif num_cols == 7 then
    -- 7-column tables
    el.colspecs[1] = {pandoc.AlignLeft, 0.08}
    el.colspecs[2] = {pandoc.AlignLeft, 0.08}
    el.colspecs[3] = {pandoc.AlignLeft, 0.10}
    el.colspecs[4] = {pandoc.AlignLeft, 0.10}
    el.colspecs[5] = {pandoc.AlignLeft, 0.12}
    el.colspecs[6] = {pandoc.AlignLeft, 0.14}
    el.colspecs[7] = {pandoc.AlignLeft, 0.33}
  end

  return el
end
