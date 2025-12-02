-- P2KB PASM2 Table Formatting Filter
-- Makes content tables full width and adjusts column ratios based on content
-- EXCLUDES encoding tables (9-column instruction encoding tables)
-- Author: Iron Sheep Productions, LLC
-- Version: 2.0 - Content-aware column width selection
--
-- This filter analyzes table content to choose appropriate column widths:
-- - Short columns (codes, labels) get minimal width
-- - Description columns (typically last) get maximum width
-- - Prevents unnecessary text wrapping in description columns

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

function Table(el)
  -- Get number of columns
  local num_cols = #el.colspecs

  -- Skip encoding tables (9 columns with specific header patterns)
  if num_cols == 9 then
    return el
  end

  -- Also skip tables with 8+ columns (encoding table variants)
  if num_cols >= 8 then
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
    -- 2-column tables: adjust based on first column size
    -- Total must be <= 0.95 to leave room for column separators
    local c1 = col_classes[1]

    if c1 == "tiny" then
      -- Very short first column (codes, single words): 15/75
      el.colspecs[1] = {pandoc.AlignLeft, 0.15}
      el.colspecs[2] = {pandoc.AlignLeft, 0.75}
    elseif c1 == "small" then
      -- Short first column: 20/70
      el.colspecs[1] = {pandoc.AlignLeft, 0.20}
      el.colspecs[2] = {pandoc.AlignLeft, 0.70}
    elseif c1 == "medium" then
      -- Medium first column: 30/60
      el.colspecs[1] = {pandoc.AlignLeft, 0.30}
      el.colspecs[2] = {pandoc.AlignLeft, 0.60}
    else
      -- Large first column: 40/50
      el.colspecs[1] = {pandoc.AlignLeft, 0.40}
      el.colspecs[2] = {pandoc.AlignLeft, 0.50}
    end

  elseif num_cols == 3 then
    -- 3-column tables: adjust based on first two columns
    local c1 = col_classes[1]
    local c2 = col_classes[2]

    if c1 == "tiny" and c2 == "tiny" then
      -- Both tiny: 10/10/75
      el.colspecs[1] = {pandoc.AlignLeft, 0.10}
      el.colspecs[2] = {pandoc.AlignLeft, 0.10}
      el.colspecs[3] = {pandoc.AlignLeft, 0.75}
    elseif c1 == "tiny" and c2 == "small" then
      -- Tiny + small: 10/18/67
      el.colspecs[1] = {pandoc.AlignLeft, 0.10}
      el.colspecs[2] = {pandoc.AlignLeft, 0.18}
      el.colspecs[3] = {pandoc.AlignLeft, 0.67}
    elseif c1 == "small" and c2 == "tiny" then
      -- Small + tiny: 18/10/67
      el.colspecs[1] = {pandoc.AlignLeft, 0.18}
      el.colspecs[2] = {pandoc.AlignLeft, 0.10}
      el.colspecs[3] = {pandoc.AlignLeft, 0.67}
    elseif c1 == "small" and c2 == "small" then
      -- Both small: 15/15/65
      el.colspecs[1] = {pandoc.AlignLeft, 0.15}
      el.colspecs[2] = {pandoc.AlignLeft, 0.15}
      el.colspecs[3] = {pandoc.AlignLeft, 0.65}
    elseif c1 == "tiny" then
      -- Tiny first, medium+ second: 10/30/55
      el.colspecs[1] = {pandoc.AlignLeft, 0.10}
      el.colspecs[2] = {pandoc.AlignLeft, 0.30}
      el.colspecs[3] = {pandoc.AlignLeft, 0.55}
    elseif c2 == "tiny" then
      -- Medium+ first, tiny second: 30/10/55
      el.colspecs[1] = {pandoc.AlignLeft, 0.30}
      el.colspecs[2] = {pandoc.AlignLeft, 0.10}
      el.colspecs[3] = {pandoc.AlignLeft, 0.55}
    else
      -- Default balanced: 20/25/50
      el.colspecs[1] = {pandoc.AlignLeft, 0.20}
      el.colspecs[2] = {pandoc.AlignLeft, 0.25}
      el.colspecs[3] = {pandoc.AlignLeft, 0.50}
    end

  elseif num_cols == 4 then
    -- 4-column tables: check if first columns are tiny
    local c1 = col_classes[1]
    local c2 = col_classes[2]
    local c3 = col_classes[3]

    if c1 == "tiny" and c2 == "tiny" and c3 == "tiny" then
      -- Three tiny columns: 10/10/10/65
      el.colspecs[1] = {pandoc.AlignLeft, 0.10}
      el.colspecs[2] = {pandoc.AlignLeft, 0.10}
      el.colspecs[3] = {pandoc.AlignLeft, 0.10}
      el.colspecs[4] = {pandoc.AlignLeft, 0.65}
    elseif c1 == "tiny" and c2 == "tiny" then
      -- Two tiny columns: 10/10/25/50
      el.colspecs[1] = {pandoc.AlignLeft, 0.10}
      el.colspecs[2] = {pandoc.AlignLeft, 0.10}
      el.colspecs[3] = {pandoc.AlignLeft, 0.25}
      el.colspecs[4] = {pandoc.AlignLeft, 0.50}
    elseif c1 == "tiny" then
      -- One tiny column: 10/22/22/41
      el.colspecs[1] = {pandoc.AlignLeft, 0.10}
      el.colspecs[2] = {pandoc.AlignLeft, 0.22}
      el.colspecs[3] = {pandoc.AlignLeft, 0.22}
      el.colspecs[4] = {pandoc.AlignLeft, 0.41}
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
