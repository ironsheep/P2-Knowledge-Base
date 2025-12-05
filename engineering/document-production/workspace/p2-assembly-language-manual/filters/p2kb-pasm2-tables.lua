-- P2KB PASM2 Table Formatting Filter
-- Auto-sized content tables with no wrapping; fixed-width encoding tables
-- Author: Iron Sheep Productions, LLC
-- Version: 4.0 - Auto-sized columns for content tables (no fixed widths)
--
-- Strategy:
-- - 9-column encoding tables: Use fixed widths with colored headers (tabularray)
-- - All other tables: Let LaTeX auto-size columns to fit content (no wrapping)
--   This means NOT setting explicit colspecs widths, allowing natural sizing

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

function Table(el)
  -- Get number of columns
  local num_cols = #el.colspecs

  -- Handle 9-column encoding tables specially (fixed widths with colored headers)
  if num_cols == 9 then
    return handle_encoding_table(el)
  end

  -- For other tables: don't set explicit widths, let LaTeX auto-size
  -- Just preserve alignment from markdown, use nil for width (auto)
  for i = 1, num_cols do
    local align = el.colspecs[i] and el.colspecs[i][1] or pandoc.AlignDefault
    el.colspecs[i] = {align, nil}
  end

  return el
end
