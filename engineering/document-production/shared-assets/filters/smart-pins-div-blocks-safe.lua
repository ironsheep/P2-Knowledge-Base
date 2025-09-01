-- Smart Pins Div-Based Colored Blocks System (SAFE VERSION)
-- Simplified to avoid potential recursion issues
-- 
-- Supported div block types (4-color system):
--   Spin2 blocks (green):         :::: spin2
--   Configuration (blue):         :::: configuration  
--   PASM2 blocks (yellow):        :::: pasm2  
--   Antipattern blocks (red):     :::: antipattern
--
-- Version: 2.1 - Safer implementation without walk_block
-- Date: 2025-08-31

-- Handle Div elements for code blocks
function Div(div)
  local classes = div.classes
  
  -- Only process our specific div types
  if not (classes:includes("antipattern") or 
          classes:includes("spin2") or 
          classes:includes("configuration") or
          classes:includes("pasm2")) then
    return div  -- Pass through unchanged
  end
  
  -- Look for CodeBlock in immediate children only (no recursion)
  local code_text = nil
  for _, block in ipairs(div.content) do
    if block.t == "CodeBlock" then
      code_text = block.text
      break  -- Take first code block only
    end
  end
  
  -- If no code block found, return unchanged
  if not code_text then
    return div
  end
  
  -- Generate appropriate LaTeX based on div type
  local latex_block = nil
  
  if classes:includes("configuration") then
    -- Blue configuration blocks
    latex_block = '\\begin{ConfigurationBlock}\n' ..
                  '\\begin{Verbatim}[numbers=left,numbersep=5pt,xleftmargin=15pt]\n' ..
                  code_text .. '\n' ..
                  '\\end{Verbatim}\n' ..
                  '\\end{ConfigurationBlock}'
                  
  elseif classes:includes("antipattern") then
    -- Red antipattern blocks
    latex_block = '\\begin{AntipatternBlock}\n' ..
                  '\\begin{Verbatim}[numbers=left,numbersep=5pt,xleftmargin=15pt]\n' ..
                  code_text .. '\n' ..
                  '\\end{Verbatim}\n' ..
                  '\\end{AntipatternBlock}'
                  
  elseif classes:includes("spin2") then
    -- Green Spin2 blocks
    latex_block = '\\begin{Spin2Block}\n' ..
                  '\\begin{Verbatim}[numbers=left,numbersep=5pt,xleftmargin=15pt]\n' ..
                  code_text .. '\n' ..
                  '\\end{Verbatim}\n' ..
                  '\\end{Spin2Block}'
                  
  elseif classes:includes("pasm2") then
    -- Yellow PASM2 blocks
    latex_block = '\\begin{PASM2Block}\n' ..
                  '\\lstset{language=pasm2,basicstyle=\\ttfamily,keywordstyle=\\bfseries\\uppercase,' ..
                  'numbers=left,numberstyle=\\tiny,xleftmargin=15pt,frame=none,backgroundcolor=\\color{white}}\n' ..
                  '\\begin{lstlisting}\n' ..
                  code_text .. '\n' ..
                  '\\end{lstlisting}\n' ..
                  '\\end{PASM2Block}'
  end
  
  if latex_block then
    return pandoc.RawBlock('latex', latex_block)
  else
    return div
  end
end