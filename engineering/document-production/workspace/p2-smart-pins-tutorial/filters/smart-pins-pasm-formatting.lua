-- Smart Pins PASM Instruction Formatting
-- Makes PASM instruction mnemonics uppercase and bold
-- Handles complex syntax: labels, conditionals, instructions
--
-- P2 PASM Syntax Components:
-- 1. Optional label (starts line): label or .label or :label (NO COLON at end)
-- 2. Optional conditional: if_c, if_nc, if_z, if_nz, if_a, if_b, etc.
-- 3. Optional instruction: mov, add, wrpin, etc.
-- 4. Operands follow instruction
--
-- Labels:
-- - Start with letter, period, or colon
-- - Followed by alphanumeric/underscore
-- - NO trailing colon (not part of P2 syntax)
-- - Can appear on their own line or before instructions
--
-- Examples:
-- gen_burst     if_c    MOV     x, y     -> gen_burst     if_c    **MOV**     x, y
-- gen_burst                              -> gen_burst (label alone on line)
--               if_c    MOV     x, y     ->               if_c    **MOV**     x, y
-- .wait         rdpin   x, #pin          -> .wait         **RDPIN**   x, #pin
--               if_z    jmp     #.wait   ->               if_z    **JMP**     #.wait
--               mov     x, y             ->               **MOV**     x, y

-- Complete list of P2 conditionals
local conditionals = {
  -- Basic conditionals
  "if_c", "if_nc", "if_z", "if_nz",
  -- Combined conditionals 
  "if_c_and_z", "if_c_and_nz", "if_nc_and_z", "if_nc_and_nz",
  -- Comparison conditionals
  "if_a", "if_ae", "if_b", "if_be", "if_e", "if_ne",
  -- Return variants (special suffix)
  "_ret_"
}

-- Build conditional pattern for matching
local conditional_pattern = ""
for i, cond in ipairs(conditionals) do
  if i > 1 then conditional_pattern = conditional_pattern .. "|" end
  conditional_pattern = conditional_pattern .. cond:gsub("_", "_")
end

-- Complete list of PASM instructions (comprehensive set)
local pasm_instructions = {
  -- Data movement
  "mov", "movbyts", "sets", "setd", "alts", "altd", "altr", "alti",
  
  -- Arithmetic
  "add", "addx", "adds", "addsx", "sub", "subx", "subs", "subsx",
  "mul", "muls", "sca", "scas", "qmul", "qdiv", "qfrac", "qsqrt",
  
  -- Logic
  "and", "andn", "or", "xor", "not", "test", "testn", "testb", "testbn",
  
  -- Bit operations
  "shl", "shr", "sal", "sar", "rol", "ror", "rcl", "rcr",
  "rev", "zerox", "signx", "encod", "decod", "ones",
  
  -- Hub memory
  "rdlong", "wrlong", "rdword", "wrword", "rdbyte", "wrbyte",
  "rdfast", "wrfast", "fblock", "rflong", "rfword", "rfbyte",
  "wflong", "wfword", "wfbyte",
  
  -- Pin control
  "dirl", "dirh", "dirnot", "dirc", "dirnc", "dirz", "dirnz",
  "drvl", "drvh", "drvnot", "drvc", "drvnc", "drvz", "drvnz",
  "outl", "outh", "outnot", "outc", "outnc", "outz", "outnz",
  "fltl", "flth", "fltnot", "fltc", "fltnc", "fltz", "fltnz",
  "wrpin", "wxpin", "wypin", "rdpin", "rqpin", "akpin",
  
  -- Flow control
  "jmp", "call", "ret", "reta", "retb", "calla", "callb", "callpa", "callpb",
  "djnz", "djz", "ijnz", "ijz", "tjnz", "tjz", "tjf", "tjs",
  "jmprel", "skip", "skipf", "execf",
  
  -- COG control
  "coginit", "cogstop", "cogid", "locknew", "lockret", "locktry", "lockrel",
  
  -- Timing
  "waitx", "waitct1", "waitct2", "waitct3", "waitse1", "waitse2", "waitse3", "waitse4",
  "waitpat", "waitfbw", "waitxmt", "waitxfi", "waitxro", "waitatn",
  "addct1", "addct2", "addct3", "getct",
  
  -- Events/Interrupts
  "pollct1", "pollct2", "pollct3", "pollse1", "pollse2", "pollse3", "pollse4",
  "pollpat", "pollfbw", "pollxmt", "pollxfi", "pollxro", "pollatn",
  "pollqmt", "setint1", "setint2", "setint3", "seti", "clri", "stalli", "allowi",
  
  -- Stack operations
  "push", "pop", "pusha", "pushb", "popa", "popb",
  
  -- Special
  "nop", "getqx", "getqy", "getxacc", "clkset", "hubset", "cogspin",
  "setq", "setq2", "augd", "augs", "rep", "modc", "modz", "modcz",
  "seti", "setd", "sets", "setb", "clrb", "notb", "setbc", "setbnc",
  "setbz", "setbnz", "bitl", "bith", "bitnot", "bitc", "bitnc", "bitz", "bitnz",
  
  -- CORDIC
  "cordic", "qrotate", "qvector",
  
  -- Comparison
  "cmp", "cmps", "cmpx", "cmpsx", "cmpr", "cmpm", "cmpsub",
  
  -- Other
  "min", "max", "mins", "maxs", "sumc", "sumnc", "sumz", "sumnz",
  "abs", "neg", "negc", "negnc", "negz", "negnz", "incmod", "decmod",
  "muxc", "muxnc", "muxz", "muxnz", "muxq", "muxnits", "muxnibs", "muxbyts",
  "wrc", "wrnc", "wrz", "wrnz", "splitb", "mergeb", "splitw", "mergew", "seussf", "seussr"
}

-- Build instruction lookup table for faster matching
local instruction_set = {}
for _, inst in ipairs(pasm_instructions) do
  instruction_set[inst:lower()] = inst:upper()
end

function CodeBlock(block)
  -- Only process PASM2 blocks
  if not (block.attr and block.attr.classes and block.attr.classes:includes("pasm2")) then
    return block
  end
  
  local lines = {}
  for line in block.text:gmatch("[^\r\n]+") do
    local formatted_line = process_pasm_line(line)
    table.insert(lines, formatted_line)
  end
  
  -- Return as LaTeX block with colored environment
  local latex_block = '\\begin{PASM2Block}\n' ..
                     '\\begin{Verbatim}[numbers=left,numbersep=10pt,xleftmargin=10pt]\n' ..
                     table.concat(lines, '\n') .. '\n' ..
                     '\\end{Verbatim}\n' ..
                     '\\end{PASM2Block}'
  return pandoc.RawBlock('latex', latex_block)
end

function process_pasm_line(line)
  -- Skip empty lines and pure comment lines
  if line:match("^%s*$") or line:match("^%s*'") then
    return line
  end
  
  -- Handle lines with comments - process the code part, keep comment as-is
  local code_part, comment_part = line:match("^([^']*)(.*)")
  if not code_part then
    code_part = line
    comment_part = ""
  end
  
  -- Parse the code part
  local result = parse_and_format_code(code_part)
  
  -- Recombine with comment
  return result .. comment_part
end

function parse_and_format_code(code)
  -- Preserve leading whitespace
  local indent, content = code:match("^(%s*)(.*)")
  if not indent then
    indent = ""
    content = code
  end
  
  -- Trim trailing whitespace from content
  content = content:gsub("%s+$", "")
  
  -- If empty after trimming, return as is
  if content == "" then
    return indent
  end
  
  -- Try to parse label if present
  local label, after_label = parse_label(content)
  local working_text = after_label or content
  
  -- Try to parse conditional if present
  local conditional, after_conditional = parse_conditional(working_text)
  local instruction_part = after_conditional or working_text
  
  -- Try to parse instruction
  local formatted_instruction = parse_instruction(instruction_part)
  
  -- Reconstruct the line
  local result = indent
  if label then
    result = result .. label
    -- Add spacing after label if there's more content
    if conditional or formatted_instruction ~= instruction_part then
      result = result .. reconstruct_spacing(content, label)
    end
  end
  if conditional then
    result = result .. conditional
    -- Add spacing after conditional if there's an instruction
    if formatted_instruction ~= instruction_part then
      result = result .. reconstruct_spacing(working_text, conditional)
    end
  end
  result = result .. formatted_instruction
  
  return result
end

function parse_label(text)
  -- P2 Label patterns (NO trailing colons in P2!): 
  -- 1. starts with letter, then alphanumeric/underscore
  -- 2. starts with period, then MUST be letter, then alphanumeric/underscore  
  -- 3. starts with colon, then MUST be letter, then alphanumeric/underscore
  
  local label, rest
  
  -- First try labels starting with . or : (must be followed by alpha)
  label_pattern = "^([%.:][%a][%w_]*)%s*(.*)"
  label, rest = text:match(label_pattern)
  
  -- If no match, try labels starting with alpha directly
  if not label then
    label_pattern = "^([%a][%w_]*)%s*(.*)"
    label, rest = text:match(label_pattern)
  end
  
  if label then
    -- Check if this might actually be an instruction (not a label)
    local label_lower = label:lower():gsub("^[%.:]?", "")
    if instruction_set[label_lower] then
      return nil, text  -- It's an instruction, not a label
    end
    
    -- Check if this looks like a conditional (not a label)
    for _, cond in ipairs(conditionals) do
      if label:lower() == cond then
        return nil, text  -- It's a conditional, not a label
      end
    end
    
    -- It's a valid label if:
    -- 1. Nothing follows (label on its own line)
    -- 2. What follows is a conditional or instruction
    
    if rest == "" then
      return label, rest  -- Label alone on line
    end
    
    -- Check if rest starts with a conditional or instruction
    local rest_lower = rest:lower()
    
    -- Check for conditional
    for _, cond in ipairs(conditionals) do
      if rest_lower:match("^" .. cond:gsub("_", "_") .. "([%s%p].*)?$") then
        return label, rest  -- Valid label before conditional
      end
    end
    
    -- Check for instruction
    local first_word = rest:match("^(%S+)")
    if first_word then
      local fw_lower = first_word:lower():gsub("_ret_$", "")
      if instruction_set[fw_lower] then
        return label, rest  -- Valid label before instruction
      end
    end
    
    -- If we get here, first word might be a label too (shouldn't happen usually)
    -- but we'll treat this as NOT a label to be safe
  end
  
  return nil, text
end

function parse_conditional(text)
  -- Check for conditional at start of remaining text
  local text_lower = text:lower()
  
  for _, cond in ipairs(conditionals) do
    -- Match conditional as whole word
    local pattern = "^(" .. cond .. ")%s+(.*)"
    local found, rest = text_lower:match(pattern)
    if found then
      -- Extract the actual conditional preserving case
      local actual_cond = text:sub(1, #cond)
      local actual_rest = text:sub(#cond + 1):match("^%s*(.*)")
      return actual_cond, actual_rest
    end
  end
  
  -- Check for _ret_ suffix (special case - appears after instruction)
  -- This is handled in instruction parsing
  
  return nil, text
end

function parse_instruction(text)
  -- Split into words
  local first_word, rest = text:match("^(%S+)(.*)")
  if not first_word then
    return text
  end
  
  -- Check if first word is an instruction (case-insensitive)
  local word_lower = first_word:lower()
  
  -- Handle _ret_ suffix specially
  local base_word = word_lower:gsub("_ret_$", "")
  local has_ret = word_lower:match("_ret_$")
  
  if instruction_set[base_word] then
    -- Just uppercase the instruction (can't use LaTeX commands in Verbatim)
    local formatted = instruction_set[base_word]
    if has_ret then
      formatted = formatted .. "_ret_"
    end
    return formatted .. rest
  end
  
  return text
end

function reconstruct_spacing(original, parsed_part)
  -- Try to preserve original spacing between components
  -- Look for spacing after the parsed part in the original
  local _, _, spacing = original:find(parsed_part:gsub("([%^%$%(%)%%%.%[%]%*%+%-%?])", "%%%1") .. "(%s*)")
  if spacing then
    return spacing
  end
  -- Default to reasonable spacing
  return "    "
end

return {
  {CodeBlock = CodeBlock}
}