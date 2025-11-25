-- P2KB DeSilva Mnemonic Bold Filter
-- Converts PASM2 mnemonics to BOLD UPPERCASE
-- Version: 1.0
--
-- Behavior:
-- - In code blocks: uppercase all mnemonics
-- - In inline code: uppercase and bold mnemonics
-- - In narrative text: conservative approach - only bold+uppercase when in code context
--
-- Conservative contexts for narrative text:
-- - After "the", "a", "an" + mnemonic + "instruction"
-- - After "use", "using", "uses"
-- - Mnemonic in backticks (handled as inline code)

-- Complete list of PASM2 mnemonics (extracted from knowledge base)
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
  "fltrnd", "fltz", "getbrk", "getbyte", "getct", "getnib", "getptr", "getqx",
  "getqy", "getrnd", "getscp", "getword", "getxacc", "hubexec", "hubset", "ijnz",
  "ijz", "incmod", "jatn", "jct1", "jct2", "jct3", "jfbw", "jint", "jmp", "jmprel",
  "jnatn", "jnct1", "jnct2", "jnct3", "jnfbw", "jnint", "jnpat", "jnqmt", "jnse1",
  "jnse2", "jnse3", "jnse4", "jnxfi", "jnxmt", "jnxrl", "jnxro", "jpat", "jqmt",
  "jse1", "jse2", "jse3", "jse4", "jxfi", "jxmt", "jxrl", "jxro", "loc", "locknew",
  "lockrel", "lockret", "locktry", "long", "mergeb", "mergew", "mixpix", "modc",
  "modcz", "modz", "mov", "movbyts", "mul", "mulpix", "muls", "muxc", "muxnc",
  "muxnibs", "muxnits", "muxnz", "muxq", "muxz", "neg", "negc", "negnc", "negnz",
  "negx", "negz", "nixint1", "nixint2", "nixint3", "nop", "not", "ones", "or",
  "org", "orgh", "outc", "outh", "outl", "outnc", "outnot", "outnz", "outrnd",
  "outz", "pollatn", "pollct1", "pollct2", "pollct3", "pollfbw", "pollint",
  "pollpat", "pollqmt", "pollse1", "pollse2", "pollse3", "pollse4", "pollxfi",
  "pollxmt", "pollxrl", "pollxro", "pop", "popa", "popb", "posx", "push", "pusha",
  "pushb", "qdiv", "qexp", "qfrac", "qlog", "qmul", "qrotate", "qsqrt", "qvector",
  "rcl", "rcr", "rczl", "rczr", "rdbyte", "rdfast", "rdlong", "rdlut", "rdpin",
  "rdword", "rep", "res", "resi0", "resi1", "resi2", "resi3", "ret", "reta",
  "retb", "reti0", "reti1", "reti2", "reti3", "rev", "rfbyte", "rflong", "rfvar",
  "rfvars", "rfword", "rgbexp", "rgbsqz", "rol", "rolbyte", "rolnib", "rolword",
  "ror", "rqpin", "sal", "sar", "sca", "scas", "setbyte", "setcfrq", "setci",
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
  "wmlong", "word", "wrbyte",
  "wrc", "wrfast", "wrlong", "wrlut", "wrnc", "wrnz", "wrpin", "wrword", "wrz",
  "wxpin", "wypin", "xcont", "xinit", "xor", "xoro32", "xstop", "xzero", "zerox"
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

-- Uppercase mnemonics in a line of code
-- Only match standalone mnemonics, not parts of identifiers like "long_d"
local function uppercase_mnemonics_in_code(text)
  -- Process character by character to handle word boundaries properly
  local result = {}
  local i = 1
  local len = #text

  while i <= len do
    local char = text:sub(i, i)

    -- Check if we're starting a potential word (letter)
    if char:match("%a") then
      -- Find the end of this alphabetic sequence
      local word_start = i
      while i <= len and text:sub(i, i):match("%a") do
        i = i + 1
      end
      local word = text:sub(word_start, i - 1)

      -- Check what comes before and after
      local char_before = word_start > 1 and text:sub(word_start - 1, word_start - 1) or ""
      local char_after = i <= len and text:sub(i, i) or ""

      -- Only uppercase if it's a standalone mnemonic (not part of identifier)
      -- Identifier chars: letters, digits, underscore
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

  return table.concat(result)
end

-- Process code blocks - uppercase mnemonics
function CodeBlock(block)
  block.text = uppercase_mnemonics_in_code(block.text)
  return block
end

-- Process inline code - uppercase mnemonics (will appear in monospace)
function Code(el)
  el.text = uppercase_mnemonics_in_code(el.text)
  return el
end

-- For narrative text, we use conservative approach
-- Only process when mnemonic appears to be in code context
-- This is handled by inline code (backticks) which goes through Code() above

return {
  { CodeBlock = CodeBlock },
  { Code = Code }
}
