-- P2KB Smart Pins - No Float Images
-- Purpose: Convert Pandoc's figure environment to non-floating
-- This intercepts at the Para level where Pandoc wraps images
--
-- Version: 2.0 - Different approach
-- Date: 2025-09-07

-- Debug helper
local function debug_element(elem, label)
  -- Uncomment for debugging
  -- io.stderr:write(label .. ": " .. pandoc.utils.type(elem) .. "\n")
end

-- Process Para elements that contain images
function Para(para)
  -- Check if this paragraph contains an image
  if #para.content == 1 and para.content[1].t == "Image" then
    local img = para.content[1]
    
    -- Get image source
    local src = img.src
    -- Decode URL encoding
    src = src:gsub("%%20", " ")
    
    -- Get caption
    local caption = pandoc.utils.stringify(img.caption or "")
    
    -- Generate raw LaTeX for non-floating image
    local latex_code
    
    if caption ~= "" then
      -- With caption - use figure with [H]
      latex_code = string.format([[\begin{figure}[H]
\centering
\includegraphics[width=0.85\textwidth]{%s}
\caption{%s}
\end{figure}]], src, caption)
    else
      -- Without caption - just center it
      latex_code = string.format([[\begin{center}
\includegraphics[width=0.85\textwidth]{%s}
\end{center}]], src)
    end
    
    -- Return as RawBlock to replace the Para
    return pandoc.RawBlock('latex', latex_code)
  end
  
  -- Not an image paragraph, return unchanged
  return para
end

-- Also handle plain Image elements (in case they're not wrapped in Para)
function Image(img)
  local src = img.src
  src = src:gsub("%%20", " ")
  
  local caption = pandoc.utils.stringify(img.caption or "")
  
  -- For inline images, return inline LaTeX
  local latex_code = string.format([[\includegraphics[width=0.85\textwidth]{%s}]], src)
  
  return pandoc.RawInline('latex', latex_code)
end