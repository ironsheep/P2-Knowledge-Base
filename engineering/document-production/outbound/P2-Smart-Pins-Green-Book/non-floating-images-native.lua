-- Non-Floating Images Filter
-- Converts all images to non-floating, centered images that appear exactly where placed
-- This prevents LaTeX from moving images to "optimize" page layout
-- 
-- Version: 1.0
-- Date: 2025-08-31
-- Purpose: Keep images in narrative flow for Green Book tutorial

function Image(img)
  -- Extract the image path and attributes
  local src = img.src
  local alt = pandoc.utils.stringify(img.alt)
  
  -- Determine width (default to 85% of text width for visual breathing room)
  -- This prevents images from dominating the page
  local width = "0.85\\textwidth"  -- 85% looks professional, not overwhelming
  
  -- Allow override if image has explicit width attribute
  if img.attributes and img.attributes.width then
    width = img.attributes.width
  end
  
  -- Create LaTeX code for centered, non-floating image
  local latex = string.format([[
\begin{center}
\includegraphics[width=%s]{%s}
\end{center}]], width, src)
  
  -- Return as raw LaTeX block
  return pandoc.RawInline('latex', latex)
end

-- Note: If we want to switch to [H] placement later, change the latex string to:
-- local latex = string.format([[
-- \begin{figure}[H]
-- \centering
-- \includegraphics[width=%s]{%s}
-- \caption{%s}
-- \end{figure}]], width, src, alt)