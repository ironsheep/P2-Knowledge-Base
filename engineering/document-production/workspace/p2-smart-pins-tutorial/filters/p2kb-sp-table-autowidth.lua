-- p2kb-sp-table-autowidth.lua
-- Converts tables with fixed-width columns to auto-width columns
-- This prevents simple 2-3 column tables from stretching to full page width

-- Only process for LaTeX output
if FORMAT:match 'latex' then
  function Table(tbl)
    -- Check if this is a simple table (few columns, short content)
    local num_cols = #tbl.colspecs

    -- For tables with 4 or fewer columns, convert to auto-width
    if num_cols <= 4 then
      -- Reset all column widths to nil (auto) and alignment to left
      for i, colspec in ipairs(tbl.colspecs) do
        -- Keep alignment but remove width
        tbl.colspecs[i] = {colspec[1], nil}
      end
    end

    return tbl
  end
end
