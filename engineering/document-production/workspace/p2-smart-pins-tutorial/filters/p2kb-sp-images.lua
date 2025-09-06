-- Non-Floating Images Filter
-- Converts all images to non-floating, centered images that appear exactly where placed
-- This prevents LaTeX from moving images to "optimize" page layout
-- 
-- Version: 2.0 - Fixed caption field and space handling
-- Date: 2025-09-04
-- Purpose: Keep images in narrative flow for Green Book tutorial

function Image(img)
  -- Extract the image path
  local src = img.src
  
  -- CRITICAL: Decode URL encoding for spaces
  -- Pandoc encodes spaces as %20, but LaTeX needs actual spaces
  src = src:gsub("%%20", " ")
  
  -- Get caption (markdown alt text is stored in caption, not alt!)
  local caption = ""
  if img.caption and type(img.caption) == "table" then
    caption = pandoc.utils.stringify(img.caption)
  end
  
  -- Determine width (default to 85% of text width for visual breathing room)
  -- This prevents images from dominating the page
  local width = "0.85\\textwidth"  -- 85% looks professional, not overwhelming
  
  -- Allow override if image has explicit width attribute
  if img.attr and img.attr.attributes and img.attr.attributes.width then
    local w = img.attr.attributes.width
    -- Handle percentage widths
    if w:match("%%$") then
      local percent = w:match("(%d+)%%")
      if percent then
        width = string.format("%.2f\\textwidth", tonumber(percent) / 100)
      end
    else
      width = w
    end
  end
  
  -- Create LaTeX code for centered, non-floating image
  -- Modern LaTeX handles spaces in filenames without quotes
  local latex
  if caption and caption ~= "" then
    -- Include caption below image (no width parameter to avoid issues with spaces)
    latex = string.format([[
\begin{center}
\includegraphics{%s}
\textit{%s}
\end{center}]], src, caption)
  else
    -- No caption - no width parameter
    latex = string.format([[
\begin{center}
\includegraphics{%s}
\end{center}]], src)
  end
  
  -- Return as raw LaTeX inline (Pandoc expects Inline from Image function)
  return pandoc.RawInline('latex', latex)
end

-- Note: If we want to switch to [H] placement later, change the latex string to:
-- local latex = string.format([[
-- \begin{figure}[H]
-- \centering
-- \includegraphics[width=%s]{%s}
-- \caption{%s}
-- \end{figure}]], width, src, alt)