-- P2KB PASM2 Table Formatting Filter
-- Conservative fix: constrain tables to page width, last column wraps
-- Author: Iron Sheep Productions, LLC
-- Version: 5.1 - Conservative fix for table overflow (uses Pandoc widths when available)
--
-- Strategy:
-- - 9-column encoding tables: Fixed widths with colored headers (tabularray)
-- - 2-8 column tables: Use tabularray with width=\linewidth
--   * If markdown specifies column widths (via grid table syntax), use those proportions
--   * If no widths specified, give ~15% each to first N-1 columns, last column flexible (X)
-- - This preserves existing table appearance while preventing overflow
-- - Last column uses X type (flexible width with word-wrap) when no width specified

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
  -- NOTE: Col 3 (CZI) needs extra width for preto/appto padding (8pt total)
  local fixed_widths = {
    0.055,  -- Col 1: EEEE (4 chars + 8pt padding)
    0.100,  -- Col 2: Opcode (7 chars)
    0.055,  -- Col 3: CZI (3 chars + 8pt padding) - was 0.035, too narrow
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

  table.insert(latex, "\\end{tblr}")

  -- Return as RawBlock
  return pandoc.RawBlock("latex", table.concat(latex, "\n"))
end

-- Handle content tables (2-8 columns) with page-width constraint
-- CONSERVATIVE: Uses Pandoc's column width hints from markdown, just adds width=\linewidth
-- If no widths specified in markdown, uses equal distribution with last column flexible
local function handle_content_table(el)
  local num_cols = #el.colspecs

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

  -- If markdown specified widths, use them (scaled to fit)
  -- If not, calculate reasonable defaults
  if has_widths and total_specified > 0 then
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

  -- Build tabularray LaTeX
  local latex = {}
  table.insert(latex, "\\begin{tblr}{")
  table.insert(latex, "  width=\\linewidth,")
  table.insert(latex, "  rowsep=3pt,")
  table.insert(latex, "  colsep=6pt,")

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


  -- Styling: bold header row, horizontal rules
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

  return pandoc.RawBlock("latex", table.concat(latex, "\n"))
end

function Table(el)
  -- Get number of columns
  local num_cols = #el.colspecs

  -- Handle 9-column encoding tables specially (fixed widths with colored headers)
  if num_cols == 9 then
    return handle_encoding_table(el)
  end

  -- Handle 2-8 column content tables with page-width constraint
  if num_cols >= 2 and num_cols <= 8 then
    return handle_content_table(el)
  end

  -- For tables outside our handling (1 column or 10+ columns), pass through
  return el
end
