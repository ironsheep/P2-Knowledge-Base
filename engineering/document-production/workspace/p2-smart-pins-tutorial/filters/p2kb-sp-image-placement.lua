-- P2KB Smart Pins - Image Placement Control
-- Purpose: Keep images at their reference location, not floating
-- Features:
--   1. Images stay where referenced (using [H] placement)
--   2. 85% width for visual breathing room
--   3. Centered presentation
--   4. Handles spaces in filenames properly
--
-- Version: 1.0
-- Date: 2025-09-07

function Image(img)
  -- Extract the image path
  local src = img.src
  
  -- Decode URL encoding for spaces
  src = src:gsub("%%20", " ")
  
  -- Get caption from the caption field (not alt)
  local caption = ""
  if img.caption and type(img.caption) == "table" then
    caption = pandoc.utils.stringify(img.caption)
  end
  
  -- Create LaTeX for non-floating image with [H] placement
  -- [H] from float package forces "HERE" placement
  local latex
  
  if caption and caption ~= "" then
    -- With caption - use figure environment with [H]
    latex = string.format([[
\begin{figure}[H]
\centering
\includegraphics[width=0.85\textwidth]{%s}
\caption{%s}
\end{figure}]], src, caption)
  else
    -- Without caption - simple centered image
    latex = string.format([[
\begin{center}
\includegraphics[width=0.85\textwidth]{%s}
\end{center}]], src)
  end
  
  -- Return as raw LaTeX block (better for block-level content)
  return pandoc.RawBlock('latex', latex)
end