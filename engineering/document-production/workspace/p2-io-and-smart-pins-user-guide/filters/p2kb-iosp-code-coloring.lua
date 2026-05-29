-- P2KB IOSP - Code Coloring Filter (ADAPTED FROM PROVEN SMART PINS)
-- Purpose: ONLY handles code block coloring for div-wrapped blocks
-- No pagination - single responsibility
--
-- Supported div block types (5-color code system):
--   Spin2 blocks (green):         ::: spin2 (includes configuration)
--   IOSP blocks (yellow):        ::: iosp
--   CORDIC blocks (purple):       ::: cordic (hardware math operations)
--   Multi-COG blocks (blue):      ::: multicog (parallel processing)
--   Antipattern blocks (red):     ::: antipattern
--
-- Also handles pedagogical elements (legacy; unused in this reference guide):
--   Medicine Cabinet, Your Turn, Sidetrack, etc.
--
-- Version: 1.1 - Integrated mnemonic uppercasing (was separate filter)
-- Date: 2025-11-26
-- Source: Proven Smart Pins workspace filter (3-color -> 5-color expansion)

-- ===== MNEMONIC UPPERCASING (integrated from p2kb-desilva-mnemonic-bold.lua) =====

-- Complete list of IOSP mnemonics
local mnemonics = {
  "abs", "add", "addct1", "addct2", "addct3", "addpix", "adds", "addsx", "addx",
  "akpin", "alignl", "alignw", "allowi", "altb", "altd", "altgb", "altgn", "altgw",
  "alti", "altr", "alts", "altsb", "altsn", "altsw", "and", "andn", "asmclk",
  "augd", "augs", "bitc", "bith", "bitl", "bitnc", "bitnot", "bitnz", "bitrnd",
  "bitz", "blnpix", "bmask", "brk", "byte", "call", "calla", "callb", "calld",
  "callpa", "callpb", "cmp", "cmpm", "cmpr", "cmps", "cmpsub", "cmpsx", "cmpx",
  "cogatn", "cogbrk", "cogexec", "cogid", "coginit", "cogstop", "crcbit", "crcnib",
  "debug", "decmod", "decod", "dirc", "dirh", "dirl", "dirnc", "dirnot", "dirnz",
  "dirrnd", "dirz", "djf", "djnf", "djnz", "djz", "drvc", "drvh", "drvl", "drvnc",
  "drvnot", "drvnz", "drvrnd", "drvz", "encod", "execf", "fblock", "fge", "fges",
  "fit", "fle", "fles", "fltc", "flth", "fltl", "fltnc", "fltnot", "fltnz",
  "fltrnd", "fltz", "getbrk", "getbyte", "getct", "getnib", "getmull", "getmulh",
  "getptr", "getqx", "getqy", "getrnd", "getscp", "getword", "getxacc", "hubexec",
  "hubset", "ijnz", "ijz", "incmod", "jatn", "jct1", "jct2", "jct3", "jfbw",
  "jint", "jmp", "jmprel", "jnatn", "jnct1", "jnct2", "jnct3", "jnfbw", "jnint",
  "jnpat", "jnqmt", "jnse1", "jnse2", "jnse3", "jnse4", "jnxfi", "jnxmt", "jnxrl",
  "jnxro", "jpat", "jqmt", "jse1", "jse2", "jse3", "jse4", "jxfi", "jxmt", "jxrl",
  "jxro", "loc", "locknew", "lockrel", "lockret", "locktry", "long", "mergeb",
  "mergew", "mixpix", "modc", "modcz", "modz", "mov", "movbyts", "mul", "mulpix",
  "muls", "muxc", "muxnc", "muxnibs", "muxnits", "muxnz", "muxq", "muxz", "neg",
  "negc", "negnc", "negnz", "negx", "negz", "nixint1", "nixint2", "nixint3", "nop",
  "not", "ones", "or", "org", "orgh", "outc", "outh", "outl", "outnc", "outnot",
  "outnz", "outrnd", "outz", "pollatn", "pollct1", "pollct2", "pollct3", "pollfbw",
  "pollint", "pollpat", "pollqmt", "pollse1", "pollse2", "pollse3", "pollse4",
  "pollxfi", "pollxmt", "pollxrl", "pollxro", "pop", "popa", "popb", "posx", "push",
  "pusha", "pushb", "qdiv", "qexp", "qfrac", "qlog", "qmul", "qrotate", "qsqrt",
  "qvector", "rcl", "rcr", "rczl", "rczr", "rdbyte", "rdfast", "rdlong", "rdlut",
  "rdluts", "rdpin", "rdword", "rep", "res", "resi0", "resi1", "resi2", "resi3", "ret", "reta",
  "retb", "reti0", "reti1", "reti2", "reti3", "rev", "rfbyte", "rflong", "rfvar",
  "rfvars", "rfword", "rgbexp", "rgbsqz", "rol", "rolbyte", "rolnib", "rolword",
  "ror", "rqpin", "sal", "sar", "sca", "scas", "scl", "setbyte", "setcfrq", "setci",
  "setcmod", "setcq", "setcy", "setd", "setdacs", "setint1", "setint2", "setint3",
  "setluts", "setnib", "setpat", "setpiv", "setpix", "setq", "setq2", "setr",
  "sets", "setscp", "setse1", "setse2", "setse3", "setse4", "setword", "setxfrq",
  "seussf", "seussr", "shl", "shr", "signx", "skip", "skipf", "splitb", "splitw",
  "stalli", "sub", "subr", "subs", "subsx", "subx", "sumc", "sumnc", "sumnz",
  "sumz", "test", "testb", "testbn", "testn", "testp", "testpn", "tjf", "tjnf",
  "tjns", "tjnz", "tjs", "tjv", "tjz", "trgint1", "trgint2", "trgint3",
  "waitatn", "waitcnt", "waitct1", "waitct2", "waitct3", "waitfbw", "waitint",
  "waitpat", "waitpeq", "waitpne", "waitse1", "waitse2", "waitse3", "waitse4", "waitx",
  "waitxfi", "waitxmt", "waitxrl", "waitxro", "wfbyte", "wflong", "wfword",
  "wmlong", "word", "wrbyte", "wrc", "wrfast", "wrlong", "wrlut", "wrnc", "wrnz",
  "wrpin", "wrword", "wrz", "wxpin", "wypin", "xcont", "xinit", "xor", "xoro32",
  "xstop", "xzero", "zerox"
}

-- Build lookup table for fast matching
local mnemonic_set = {}
for _, m in ipairs(mnemonics) do
  mnemonic_set[m:lower()] = true
end

-- Check if a word is a mnemonic
local function is_mnemonic(word)
  return mnemonic_set[word:lower()] ~= nil
end

-- Uppercase mnemonics in a single line of code (stops at comment)
local function uppercase_mnemonics_in_line(line)
  -- Find comment start (single quote in IOSP)
  local comment_start = line:find("'")
  local code_part = comment_start and line:sub(1, comment_start - 1) or line
  local comment_part = comment_start and line:sub(comment_start) or ""

  -- Process only the code part
  local result = {}
  local i = 1
  local len = #code_part

  while i <= len do
    local char = code_part:sub(i, i)

    -- Match words starting with letter, can contain digits (for addct1, waitct2, setse1, etc.)
    if char:match("%a") then
      local word_start = i
      while i <= len and code_part:sub(i, i):match("[%a%d]") do
        i = i + 1
      end
      local word = code_part:sub(word_start, i - 1)

      local char_before = word_start > 1 and code_part:sub(word_start - 1, word_start - 1) or ""
      local char_after = i <= len and code_part:sub(i, i) or ""

      local is_part_of_identifier = char_before:match("[%w_]") or char_after:match("[%w_]")

      if is_mnemonic(word) and not is_part_of_identifier then
        table.insert(result, word:upper())
      else
        table.insert(result, word)
      end
    else
      table.insert(result, char)
      i = i + 1
    end
  end

  return table.concat(result) .. comment_part
end

-- Uppercase mnemonics in code text (process line by line)
local function uppercase_mnemonics(text)
  local lines = {}
  for line in text:gmatch("([^\n]*)\n?") do
    table.insert(lines, uppercase_mnemonics_in_line(line))
  end
  -- Remove trailing empty line if original didn't have one
  if #lines > 0 and lines[#lines] == "" and not text:match("\n$") then
    table.remove(lines)
  end
  return table.concat(lines, "\n")
end

-- ===== DIV HANDLER =====

-- Handle Div elements for code blocks and pedagogical elements
function Div(div)
  local classes = div.classes
  
  -- ===== CODE BLOCK DIVS (5-color code system) =====
  
  -- Antipattern blocks: ::: antipattern -> AntipatternBlock environment (RED)
  if classes:includes("antipattern") then
    -- Find the CodeBlock inside this div
    local code_block = nil
    pandoc.walk_block(div, {
      CodeBlock = function(cb)
        code_block = cb
        return cb
      end
    })

    if code_block then
      -- Uppercase mnemonics in the code text
      local processed_text = uppercase_mnemonics(code_block.text)
      -- Return complete LaTeX block for antipattern styling
      local latex_block = '\\begin{AntipatternBlock}\n' ..
                         '\\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]\n' ..
                         processed_text .. '\n' ..
                         '\\end{Verbatim}\n' ..
                         '\\end{AntipatternBlock}'
      return pandoc.RawBlock('latex', latex_block)
    end
  
  -- Spin2 blocks: ::: spin2 -> Spin2Block environment (GREEN)
  -- Note: This includes configuration blocks (WRPIN:/WXPIN:/WYPIN:) per pedagogical decision
  elseif classes:includes("spin2") then
    -- Find the CodeBlock inside this div
    local code_block = nil
    pandoc.walk_block(div, {
      CodeBlock = function(cb)
        code_block = cb
        return cb
      end
    })
    
    if code_block then
      -- Return complete LaTeX block for Spin2 styling
      local latex_block = '\\begin{Spin2Block}\n' ..
                         '\\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]\n' ..
                         code_block.text .. '\n' ..
                         '\\end{Verbatim}\n' ..
                         '\\end{Spin2Block}'
      return pandoc.RawBlock('latex', latex_block)
    end
    
  -- IOSP blocks: ::: iosp -> IOSPBlock environment (YELLOW)
  elseif classes:includes("iosp") then
    -- Find the CodeBlock inside this div
    local code_block = nil
    pandoc.walk_block(div, {
      CodeBlock = function(cb)
        code_block = cb
        return cb
      end
    })

    if code_block then
      -- Uppercase mnemonics in the code text
      local processed_text = uppercase_mnemonics(code_block.text)
      -- Return complete LaTeX block using Verbatim
      local latex_block = '\\begin{IOSPBlock}\n' ..
                         '\\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]\n' ..
                         processed_text .. '\n' ..
                         '\\end{Verbatim}\n' ..
                         '\\end{IOSPBlock}'
      return pandoc.RawBlock('latex', latex_block)
    end
    
  -- CORDIC blocks: ::: cordic -> CORDICBlock environment (PURPLE)
  elseif classes:includes("cordic") then
    -- Find the CodeBlock inside this div
    local code_block = nil
    pandoc.walk_block(div, {
      CodeBlock = function(cb)
        code_block = cb
        return cb
      end
    })

    if code_block then
      -- Uppercase mnemonics in the code text
      local processed_text = uppercase_mnemonics(code_block.text)
      -- Return complete LaTeX block for CORDIC styling
      local latex_block = '\\begin{CORDICBlock}\n' ..
                         '\\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]\n' ..
                         processed_text .. '\n' ..
                         '\\end{Verbatim}\n' ..
                         '\\end{CORDICBlock}'
      return pandoc.RawBlock('latex', latex_block)
    end

  -- Multi-COG blocks: ::: multicog -> MultiCOGBlock environment (BLUE)
  elseif classes:includes("multicog") then
    -- Find the CodeBlock inside this div
    local code_block = nil
    pandoc.walk_block(div, {
      CodeBlock = function(cb)
        code_block = cb
        return cb
      end
    })

    if code_block then
      -- Uppercase mnemonics in the code text
      local processed_text = uppercase_mnemonics(code_block.text)
      -- Return complete LaTeX block for Multi-COG styling
      local latex_block = '\\begin{MultiCOGBlock}\n' ..
                         '\\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]\n' ..
                         processed_text .. '\n' ..
                         '\\end{Verbatim}\n' ..
                         '\\end{MultiCOGBlock}'
      return pandoc.RawBlock('latex', latex_block)
    end
  
  -- ===== DESILVA PEDAGOGICAL ELEMENTS =====
  
  elseif classes:includes("medicine-cabinet") then
    local result = {pandoc.RawBlock('latex', '\\begin{dsmedicinecabinet}')}
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{dsmedicinecabinet}'))
    return result

  elseif classes:includes("your-turn") then
    local result = {pandoc.RawBlock('latex', '\\begin{dsyourturn}')}
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{dsyourturn}'))
    return result

  elseif classes:includes("sidetrack") then
    -- Extract title from first heading in sidetrack for TOC entry
    local sidetrack_title = nil
    for _, block in ipairs(div.content) do
      if block.t == "Header" then
        sidetrack_title = pandoc.utils.stringify(block.content)
        break
      end
    end

    local result = {pandoc.RawBlock('latex', '\\begin{dssidetrack}')}
    -- Add TOC entry if we found a title
    if sidetrack_title then
      table.insert(result, pandoc.RawBlock('latex',
        '\\addcontentsline{toc}{section}{Sidetrack: ' .. sidetrack_title .. '}'))
    end
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{dssidetrack}'))
    return result

  elseif classes:includes("uff") then
    local result = {pandoc.RawBlock('latex', '\\begin{dsuff}')}
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{dsuff}'))
    return result

  elseif classes:includes("well") then
    local result = {pandoc.RawBlock('latex', '\\begin{dswell}')}
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{dswell}'))
    return result

  elseif classes:includes("have-fun") then
    local result = {pandoc.RawBlock('latex', '\\begin{dshavefun}')}
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{dshavefun}'))
    return result

  elseif classes:includes("interlude") then
    local result = {pandoc.RawBlock('latex', '\\begin{InterludeBlock}')}
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{InterludeBlock}'))
    return result
  end

  -- Return div unchanged if not a recognized type
  return div
end

-- NO Header function - pagination is handled by separate filter

-- CodeBlock function - handles code blocks with language classes that appear
-- inside other elements (like sidetracks) where they aren't in a div wrapper
function CodeBlock(cb)
  local classes = cb.classes

  -- Check for iosp or pasm language tag
  if classes:includes("iosp") or classes:includes("pasm") or classes:includes("pasm2") then
    local processed_text = uppercase_mnemonics(cb.text)
    local latex_block = '\\begin{IOSPBlock}\n' ..
                       '\\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]\n' ..
                       processed_text .. '\n' ..
                       '\\end{Verbatim}\n' ..
                       '\\end{IOSPBlock}'
    return pandoc.RawBlock('latex', latex_block)

  -- Check for spin2 language tag
  elseif classes:includes("spin2") then
    local latex_block = '\\begin{Spin2Block}\n' ..
                       '\\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]\n' ..
                       cb.text .. '\n' ..
                       '\\end{Verbatim}\n' ..
                       '\\end{Spin2Block}'
    return pandoc.RawBlock('latex', latex_block)

  -- Check for cordic language tag
  elseif classes:includes("cordic") then
    local processed_text = uppercase_mnemonics(cb.text)
    local latex_block = '\\begin{CORDICBlock}\n' ..
                       '\\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]\n' ..
                       processed_text .. '\n' ..
                       '\\end{Verbatim}\n' ..
                       '\\end{CORDICBlock}'
    return pandoc.RawBlock('latex', latex_block)

  -- Check for multicog language tag
  elseif classes:includes("multicog") then
    local processed_text = uppercase_mnemonics(cb.text)
    local latex_block = '\\begin{MultiCOGBlock}\n' ..
                       '\\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]\n' ..
                       processed_text .. '\n' ..
                       '\\end{Verbatim}\n' ..
                       '\\end{MultiCOGBlock}'
    return pandoc.RawBlock('latex', latex_block)

  -- Instruction syntax forms: ```syntax -> SyntaxBlock (slate, reference tier).
  -- Line numbers ONLY when multi-line (single-line forms read cleaner without
  -- a "1" gutter). Content is shown verbatim (KB-sourced, already uppercased).
  elseif classes:includes("spin-syntax") or classes:includes("syntax")
         or classes:includes("pasm-syntax") then
    local txt = cb.text:gsub("%s+$", "")
    -- Bar color + enclosed title encode language: Spin2 = blue, PASM2 = green.
    -- The title is a small bold label inside the bar (relocates the section
    -- heading into the block), making the bar self-documenting.
    local is_spin = classes:includes("spin-syntax")
    local barcolor = is_spin and 'iosp-spin2-border' or 'iosp-pasm2-border'
    local title = is_spin and 'Spin2 Syntax' or 'PASM2 Syntax'
    local multiline = txt:find("\n") ~= nil
    local verb = multiline
      and '\\begin{Verbatim}[numbers=left,numbersep=6pt]\n'
      or  '\\begin{Verbatim}\n'
    local latex_block = '\\begin{SyntaxBlock}{' .. barcolor .. '}\n' ..
                       '{\\small\\bfseries\\color{' .. barcolor .. '}' .. title .. '}\\par\\vspace{2pt}\n' ..
                       verb ..
                       txt .. '\n' ..
                       '\\end{Verbatim}\n' ..
                       '\\end{SyntaxBlock}'
    return pandoc.RawBlock('latex', latex_block)

  -- Bit-field / register-layout diagrams: ```layout -> LayoutBlock (bronze). No numbers.
  elseif classes:includes("layout") then
    local txt = cb.text:gsub("%s+$", "")
    local latex_block = '\\begin{LayoutBlock}\n' ..
                       '\\begin{Verbatim}[xleftmargin=0pt]\n' ..
                       txt .. '\n' ..
                       '\\end{Verbatim}\n' ..
                       '\\end{LayoutBlock}'
    return pandoc.RawBlock('latex', latex_block)

  -- Formulas / worked calculations: ```formula -> FormulaBlock (indigo). No numbers.
  elseif classes:includes("formula") then
    local txt = cb.text:gsub("%s+$", "")
    local latex_block = '\\begin{FormulaBlock}\n' ..
                       '\\begin{Verbatim}[xleftmargin=0pt]\n' ..
                       txt .. '\n' ..
                       '\\end{Verbatim}\n' ..
                       '\\end{FormulaBlock}'
    return pandoc.RawBlock('latex', latex_block)
  end

  -- Return unchanged if not a recognized language
  return cb
end