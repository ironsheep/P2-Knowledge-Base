-- P2KB Smart Pins Mnemonic Bold Filter
-- Converts PASM2 mnemonics to BOLD UPPERCASE in prose and code
-- Version: 1.0 - Adapted from p2kb-pasm2-mnemonic-bold.lua v2.0
--
-- Behavior:
-- - In code blocks: uppercase all mnemonics
-- - In inline code: uppercase all mnemonics
-- - In narrative prose: bold+uppercase mnemonics with grammar-aware filtering
--   to avoid false positives on common English words (and, or, not, etc.)

-- Complete list of PASM2 mnemonics
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
  "pollxfi", "pollxmt", "pollxrl", "pollxro", "pop", "popa", "popb", "posx",
  "push", "pusha", "pushb", "qdiv", "qexp", "qfrac", "qlog", "qmul", "qrotate",
  "qsqrt", "qvector", "rcl", "rcr", "rczl", "rczr", "rdbyte", "rdfast", "rdlong",
  "rdlut", "rdluts", "rdpin", "rdword", "rep", "res", "resi0", "resi1", "resi2",
  "resi3", "ret", "reta", "retb", "reti0", "reti1", "reti2", "reti3", "rev",
  "rfbyte", "rflong", "rfvar", "rfvars", "rfword", "rgbexp", "rgbsqz", "rol",
  "rolbyte", "rolnib", "rolword", "ror", "rqpin", "sal", "sar", "sca", "scas",
  "scl", "setbyte", "setcfrq", "setci", "setcmod", "setcq", "setcy", "setd",
  "setdacs", "setint1", "setint2", "setint3", "setluts", "setnib", "setpat",
  "setpiv", "setpix", "setq", "setq2", "setr", "sets", "setscp", "setse1",
  "setse2", "setse3", "setse4", "setword", "setxfrq", "seussf", "seussr", "shl",
  "shr", "signx", "skip", "skipf", "splitb", "splitw", "stalli", "sub", "subr",
  "subs", "subsx", "subx", "sumc", "sumnc", "sumnz", "sumz", "test", "testb",
  "testbn", "testn", "testp", "testpn", "tjf", "tjnf", "tjns", "tjnz", "tjs",
  "tjv", "tjz", "trgint1", "trgint2", "trgint3", "waitatn", "waitcnt", "waitct1",
  "waitct2", "waitct3", "waitfbw", "waitint", "waitpat", "waitpeq", "waitpne",
  "waitse1", "waitse2", "waitse3", "waitse4", "waitx", "waitxfi", "waitxmt",
  "waitxrl", "waitxro", "wfbyte", "wflong", "wfword", "wmlong", "word", "wrbyte",
  "wrc", "wrfast", "wrlong", "wrlut", "wrnc", "wrnz", "wrpin", "wrword", "wrz",
  "wxpin", "wypin", "xcont", "xinit", "xor", "xoro32", "xstop", "xzero", "zerox"
}

-- Build lookup table for fast matching
local mnemonic_set = {}
for _, m in ipairs(mnemonics) do
  mnemonic_set[m:lower()] = true
end

-- Words that are commonly used as English and need grammar checking
-- These require context analysis to determine if they're instructions
local ambiguous_words = {
  ["and"] = true,
  ["or"] = true,
  ["not"] = true,
  ["long"] = true,
  ["word"] = true,
  ["byte"] = true,
  ["add"] = true,
  ["adds"] = true,
  ["test"] = true,
  ["call"] = true,
  ["fit"] = true,
  ["push"] = true,
  ["pop"] = true,
  ["ret"] = true,
  ["rep"] = true,
  ["sub"] = true,
  ["neg"] = true,
  ["abs"] = true,
  ["rev"] = true,
  ["ones"] = true,
  ["skip"] = true,
  ["debug"] = true,
  ["sets"] = true,  -- "sets direction" vs SETS instruction
}

-- Check if a word is a mnemonic
local function is_mnemonic(word)
  return mnemonic_set[word:lower()] ~= nil
end

-- Check if word is ambiguous (common English word)
local function is_ambiguous(word)
  return ambiguous_words[word:lower()] ~= nil
end

-- Grammar patterns that indicate English usage (NOT an instruction)
-- prev_word is the word before, next_word is the word after
-- suffix is any trailing characters after the word (like "-level" in "BYTE-level")
local function is_english_context(word, prev_word, next_word, suffix)
  local w = word:lower()
  local prev = prev_word and prev_word:lower() or ""
  local next = next_word and next_word:lower() or ""
  local suf = suffix and suffix:lower() or ""

  -- Check for hyphenated compounds - if suffix starts with hyphen, check what follows
  -- e.g., "BYTE-level" has suffix "-level"
  if suf:match("^%-") then
    local hyphen_word = suf:match("^%-(%a+)")
    if hyphen_word then
      -- Treat hyphenated compound as English usage
      -- "BYTE-level", "WORD-aligned", etc.
      return true
    end
  end

  -- "and" as conjunction: "X and Y", "and the", "and then", "and also"
  if w == "and" then
    -- If followed by instruction/directive keywords, it's the instruction
    if next == "instruction" or next == "performs" then
      return false
    end
    -- If preceded by instruction-like context, it's the instruction
    if prev == "the" and next == "instruction" then
      return false
    end
    -- "configuration AND operation" - AND as conjunction
    if next == "operation" or next == "operations" then
      return true
    end
    -- Otherwise, "and" in prose is almost always a conjunction
    -- The instruction AND is typically written as `AND` in code or "the AND instruction"
    return true
  end

  -- "or" as conjunction: "X or Y", "either...or", "or the"
  if w == "or" then
    -- If followed by instruction/directive keywords, it's the instruction
    if next == "instruction" or next == "performs" or next == "operation" then
      return false
    end
    -- Otherwise, "or" in prose is almost always a conjunction
    -- The instruction OR is typically written as `OR` in code or "the OR instruction"
    return true
  end

  -- "not" as negation: "not the", "does not", "is not", "will not", "do not", "can not"
  if w == "not" then
    -- If followed by instruction/directive keywords, it's the instruction
    if next == "instruction" or next == "performs" or next == "operation" then
      return false
    end
    -- Otherwise, "not" in prose is almost always negation
    -- The instruction NOT is typically written as `NOT` in code or "the NOT instruction"
    return true
  end

  -- "long" as adjective: "long time", "long value", "how long", "too long"
  if w == "long" then
    if prev == "how" or prev == "too" or prev == "very" or prev == "a" or
       prev == "the" then
      return true
    end
    if next == "time" or next == "value" or next == "values" or next == "enough" or
       next == "way" or next == "period" or next == "run" then
      return true
    end
    if next == "instruction" or next == "directive" or next == "data" then
      return false
    end
    -- Default: "long" in prose is the adjective/noun (long time, a long, etc.)
    return true
  end

  -- "word" as noun: "the word", "a word", "word value"
  if w == "word" then
    if prev == "the" or prev == "a" or prev == "each" or prev == "every" or
       prev == "this" or prev == "that" then
      return true
    end
    if next == "value" or next == "values" or next == "size" or next == "aligned" then
      return true
    end
    if next == "instruction" or next == "directive" then
      return false
    end
    -- Default: "word" in prose is the noun (a word, the word, word value)
    return true
  end

  -- "byte" as noun/adjective: "the byte", "a byte", "byte value", "BYTE-level"
  if w == "byte" then
    if prev == "the" or prev == "a" or prev == "each" or prev == "every" or
       prev == "per" or prev == "one" then
      return true
    end
    if next == "value" or next == "values" or next == "size" or next == "aligned" or
       next == "boundary" or next == "order" or next == "level" then
      return true
    end
    -- Hyphenated compounds: "BYTE-level", "BYTE-sized" etc.
    -- The next "word" after hyphen stripping might be "level"
    if next and next:match("^level") then
      return true
    end
    if next == "instruction" or next == "directive" then
      return false
    end
    -- Default: "byte" in prose is the noun/adjective (a byte, byte order, style byte)
    return true
  end

  -- "add" as verb: "add to", "add the", "to add", "will add"
  if w == "add" then
    -- If followed by instruction/directive keywords, it's the instruction
    if next == "instruction" or next == "performs" or next == "operation" then
      return false
    end
    -- Otherwise, "add" in prose is almost always the verb
    -- The instruction ADD is typically written as `ADD` in code or "the ADD instruction"
    return true
  end

  -- "adds" as verb: "adds two", "adds the", "X adds Y" (mirrors "add")
  if w == "adds" then
    if next == "instruction" or next == "performs" or next == "operation" then
      return false
    end
    return true
  end

  -- "sub" as prefix/noun: rarely used alone in English, usually instruction
  if w == "sub" then
    -- Almost always the instruction in this context
    return false
  end

  -- "test" as verb: "test the", "to test", "will test"
  if w == "test" then
    if prev == "to" or prev == "will" or prev == "can" or prev == "could" or
       prev == "would" or prev == "should" or prev == "must" or prev == "the" or
       prev == "a" then
      return true
    end
    if next == "the" or next == "a" or next == "an" or next == "this" or
       next == "that" or next == "it" or next == "whether" or next == "if" or
       next == "for" then
      return true
    end
    if next == "instruction" or next == "performs" or next == "bits" then
      return false
    end
    return false
  end

  -- "call" as verb: "call the", "to call", "will call"
  if w == "call" then
    if prev == "to" or prev == "will" or prev == "can" or prev == "could" or
       prev == "would" or prev == "should" or prev == "must" or prev == "a" or
       prev == "the" or prev == "function" or prev == "subroutine" then
      return true
    end
    if next == "the" or next == "a" or next == "an" or next == "this" or
       next == "that" or next == "it" or next == "to" then
      return true
    end
    if next == "instruction" or next == "performs" then
      return false
    end
    return false
  end

  -- "fit" as verb: "fit in", "to fit", "will fit", "does fit"
  if w == "fit" then
    if prev == "to" or prev == "will" or prev == "can" or prev == "could" or
       prev == "would" or prev == "should" or prev == "must" or prev == "does" or
       prev == "do" or prev == "did" or prev == "doesn" then
      return true
    end
    if next == "in" or next == "into" or next == "within" or next == "the" then
      return true
    end
    if next == "directive" or next == "statement" then
      return false
    end
    return false
  end

  -- "push" as verb: "push the", "to push"
  if w == "push" then
    if prev == "to" or prev == "will" or prev == "can" then
      return true
    end
    if next == "the" or next == "a" or next == "it" or next == "them" then
      return true
    end
    if next == "instruction" or next == "performs" then
      return false
    end
    return false
  end

  -- "pop" as verb/noun: "pop the", "to pop"
  if w == "pop" then
    if prev == "to" or prev == "will" or prev == "can" then
      return true
    end
    if next == "the" or next == "a" or next == "it" or next == "them" or
       next == "off" then
      return true
    end
    if next == "instruction" or next == "performs" then
      return false
    end
    return false
  end

  -- "ret" - rarely English, almost always instruction
  if w == "ret" then
    return false
  end

  -- "rep" - rarely English alone, usually instruction
  if w == "rep" then
    return false
  end

  -- "neg" - rarely English alone, usually instruction
  if w == "neg" then
    return false
  end

  -- "abs" - could be "abs" (abbreviation) but usually instruction in this context
  if w == "abs" then
    if prev == "the" then
      return true
    end
    return false
  end

  -- "rev" - could be abbreviation, but usually instruction
  if w == "rev" then
    if next == "." then  -- abbreviation like "Rev."
      return true
    end
    return false
  end

  -- "ones" as noun: "the ones", "which ones"
  if w == "ones" then
    if prev == "the" or prev == "which" or prev == "these" or prev == "those" then
      return true
    end
    if next == "instruction" or next == "count" then
      return false
    end
    return false
  end

  -- "skip" as verb: "skip the", "to skip"
  if w == "skip" then
    if prev == "to" or prev == "will" or prev == "can" then
      return true
    end
    if next == "the" or next == "a" or next == "over" or next == "to" then
      return true
    end
    if next == "instruction" or next == "performs" then
      return false
    end
    return false
  end

  -- "debug" as verb/noun: "debug the", "to debug"
  if w == "debug" then
    if prev == "to" or prev == "will" or prev == "can" or prev == "the" or
       prev == "a" then
      return true
    end
    if next == "the" or next == "a" or next == "this" or next == "mode" or
       next == "output" or next == "message" then
      return true
    end
    if next == "instruction" or next == "performs" then
      return false
    end
    return false
  end

  -- "sets" as verb: "sets direction", "sets the", "DIRZ sets"
  -- The SETS instruction is rare in prose; "sets" is almost always the verb
  if w == "sets" then
    -- If followed by instruction keyword, it's the instruction
    if next == "instruction" or next == "performs" then
      return false
    end
    -- "sets direction", "sets the", "sets a" - all verb usage
    if next == "direction" or next == "the" or next == "a" or next == "an" or
       next == "it" or next == "this" or next == "that" then
      return true
    end
    -- Previous word is an instruction (like DIRZ) - this "sets" is the verb
    -- describing what that instruction does
    if is_mnemonic(prev) then
      return true
    end
    -- Default for "sets" - treat as English verb (very common)
    return true
  end

  -- Default: not English context (treat as instruction)
  return false
end

-- Check if paragraph content is in instruction header area (before Explanation)
-- These areas already have proper formatting and shouldn't be double-processed
local function is_instruction_header_area(elements)
  local full_text = ""
  for _, elem in ipairs(elements) do
    if elem.t == "Str" then
      full_text = full_text .. elem.text
    elseif elem.t == "Strong" then
      full_text = full_text .. pandoc.utils.stringify(elem)
    end
  end

  -- Patterns indicating instruction header area:
  -- Syntax lines with operand placeholders
  if full_text:match("{#}") or full_text:match("Dest,") or full_text:match(", Src") or
     full_text:match("{WC") or full_text:match("{WZ") or full_text:match("WCZ}") then
    return true
  end

  -- Result line
  if full_text:match("^Result:") then
    return true
  end

  -- Related line
  if full_text:match("^Related:") then
    return true
  end

  -- Category/one-liner (contains instruction category links)
  if full_text:match("Instruction%]") or full_text:match("Directive%]") or
     full_text:match("Constant%]") then
    return true
  end

  return false
end

-- Check if a Plain block (bullet item) is an operand description
local function is_operand_description(elements)
  local full_text = ""
  for _, elem in ipairs(elements) do
    if elem.t == "Str" then
      full_text = full_text .. elem.text
    end
  end

  -- Operand description patterns: starts with operand name
  if full_text:match("^Dest ") or full_text:match("^Src ") or
     full_text:match("^D ") or full_text:match("^S ") or
     full_text:match("^WC,") or full_text:match("^WZ,") or
     full_text:match("^The ") then
    return true
  end

  return false
end

-- Uppercase mnemonics in a single line of code (stops at comment)
local function uppercase_mnemonics_in_line(line)
  local comment_start = line:find("'")
  local code_part = comment_start and line:sub(1, comment_start - 1) or line
  local comment_part = comment_start and line:sub(comment_start) or ""

  local result = {}
  local i = 1
  local len = #code_part

  while i <= len do
    local char = code_part:sub(i, i)

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

-- Uppercase mnemonics in a code block
local function uppercase_mnemonics_in_code(text)
  local lines = {}
  for line in text:gmatch("([^\n]*)\n?") do
    if line ~= "" or text:sub(-1) == "\n" then
      table.insert(lines, uppercase_mnemonics_in_line(line))
    end
  end
  return table.concat(lines, "\n")
end

-- Process code blocks
function CodeBlock(block)
  block.text = uppercase_mnemonics_in_code(block.text)
  return block
end

-- Process inline code
function Code(el)
  el.text = uppercase_mnemonics_in_code(el.text)
  return el
end

-- Process paragraph text - bold mnemonics with grammar awareness
function Para(para)
  local elements = para.content

  -- Skip instruction header areas (syntax lines, Result, Related, etc.)
  if is_instruction_header_area(elements) then
    return para
  end

  local new_content = {}

  for i, elem in ipairs(elements) do
    if elem.t == "Str" then
      local word = elem.text
      local word_lower = word:lower()

      -- Strip trailing punctuation for matching
      local core_word = word:match("^(%a+)")
      local suffix = core_word and word:sub(#core_word + 1) or ""

      if core_word and is_mnemonic(core_word) then
        -- Get previous and next words for context
        local prev_word = nil
        local next_word = nil

        -- Look backward for previous word
        for j = i - 1, 1, -1 do
          if elements[j].t == "Str" then
            prev_word = elements[j].text:match("(%a+)")
            break
          elseif elements[j].t == "Space" or elements[j].t == "SoftBreak" then
            -- continue looking
          else
            break
          end
        end

        -- Look forward for next word
        for j = i + 1, #elements do
          if elements[j].t == "Str" then
            next_word = elements[j].text:match("(%a+)")
            break
          elseif elements[j].t == "Space" or elements[j].t == "SoftBreak" then
            -- continue looking
          else
            break
          end
        end

        -- Check if this is an ambiguous word needing grammar analysis
        local should_bold = true
        if is_ambiguous(core_word) then
          if is_english_context(core_word, prev_word, next_word, suffix) then
            should_bold = false
          end
        end

        if should_bold then
          -- Bold and uppercase the mnemonic
          local bold_elem = pandoc.Strong(pandoc.Str(core_word:upper()))
          table.insert(new_content, bold_elem)
          if suffix ~= "" then
            table.insert(new_content, pandoc.Str(suffix))
          end
        else
          -- Keep as-is
          table.insert(new_content, elem)
        end
      else
        table.insert(new_content, elem)
      end
    else
      table.insert(new_content, elem)
    end
  end

  para.content = new_content
  return para
end

-- Also process plain blocks (like in list items)
function Plain(plain)
  local elements = plain.content

  -- Skip operand description bullets (Dest is..., Src is..., etc.)
  if is_operand_description(elements) then
    return plain
  end

  local new_content = {}

  for i, elem in ipairs(elements) do
    if elem.t == "Str" then
      local word = elem.text
      local core_word = word:match("^(%a+)")
      local suffix = core_word and word:sub(#core_word + 1) or ""

      if core_word and is_mnemonic(core_word) then
        local prev_word = nil
        local next_word = nil

        for j = i - 1, 1, -1 do
          if elements[j].t == "Str" then
            prev_word = elements[j].text:match("(%a+)")
            break
          elseif elements[j].t == "Space" or elements[j].t == "SoftBreak" then
            -- continue
          else
            break
          end
        end

        for j = i + 1, #elements do
          if elements[j].t == "Str" then
            next_word = elements[j].text:match("(%a+)")
            break
          elseif elements[j].t == "Space" or elements[j].t == "SoftBreak" then
            -- continue
          else
            break
          end
        end

        local should_bold = true
        if is_ambiguous(core_word) then
          if is_english_context(core_word, prev_word, next_word, suffix) then
            should_bold = false
          end
        end

        if should_bold then
          local bold_elem = pandoc.Strong(pandoc.Str(core_word:upper()))
          table.insert(new_content, bold_elem)
          if suffix ~= "" then
            table.insert(new_content, pandoc.Str(suffix))
          end
        else
          table.insert(new_content, elem)
        end
      else
        table.insert(new_content, elem)
      end
    else
      table.insert(new_content, elem)
    end
  end

  plain.content = new_content
  return plain
end

return {
  { CodeBlock = CodeBlock },
  { Code = Code },
  { Para = Para },
  { Plain = Plain }
}
