--[[
  p2kb-platform-crossref.lua  —  P2KB platform cross-reference auto-linker

  Turns in-prose references to document structure into clickable internal links:
    "Chapter 8"   -> the Chapter 8 header
    "Appendix C"  -> the Appendix C header
    "Section 8.2" -> the 8.2 header
    "§8.2"        -> the 8.2 header

  Two passes over the document:
    Pass 1  harvests every header's auto-generated identifier, keyed by chapter
            number / appendix letter / leading section number.
    Pass 2  rewrites matching inline runs inside Para/Plain blocks into Links
            whose target is the harvested anchor.

  SAFE BY DESIGN:
    * Only links a reference whose target header actually EXISTS in this document;
      an unmatched "Chapter 99" / "§99.9" stays plain text.
    * Headers are never rewritten (no self-links inside titles).
    * Rewrites prose inside Para/Plain and descends into inline containers
      (Emph/Strong/Span/Quoted/...), so refs inside *italic* "see also" lines link
      too. It does NOT recurse into a Link (no double-wrapping an existing markdown
      link) or into Code/Math.
    * Pandoc strips leading numbers from section identifiers, so we map the section
      NUMBER -> the real identifier pandoc assigned (never guess the anchor text).

  ADOPTION (platform note): opt-in per manual via request.json `lua_filters`.
  Auto-linking can mis-fire (e.g. a manual using "Chapter N" to mean another
  document, or a stray "Section 1.2" in code prose), so each manual must be
  VISUALLY AUDITED for cross-ref behavior the next time it is released. See
  engineering/document-production/CROSSREF-FILTER-ADOPTION.md.
]]

local chapters   = {}   -- ["8"]  = "chapter-8-frequency-generation-nco"
local appendices = {}   -- ["C"]  = "appendix-c-..."
local sections   = {}   -- ["8.2"]= the identifier pandoc assigned to that header

-- ---------- Pass 1: harvest header identifiers ----------
local function harvest(h)
  local id = h.identifier
  if not id or id == "" then return nil end
  local txt = pandoc.utils.stringify(h.content)
  local c = txt:match("^Chapter%s+(%d+)")
  if c then chapters[c] = id end
  local a = txt:match("^Appendix%s+([A-Za-z])")
  if a then appendices[a:upper()] = id end
  local s = txt:match("^(%d+%.%d[%d%.]*)")
  if s then sections[s] = id end
  return nil
end

-- ---------- Pass 2 helpers ----------
local function mklink(inls, id)
  return pandoc.Link(inls, "#" .. id)
end

-- keyword + following token text -> (id, core, trailing) or nil
local function resolve(keyword, tok)
  if keyword == "Chapter" or keyword == "Ch" then
    local num, rest = tok:match("^(%d+)(.*)$")
    if num and chapters[num] then return chapters[num], num, rest end
  elseif keyword == "Appendix" then
    local let, rest = tok:match("^([A-Za-z])(.*)$")
    if let and appendices[let:upper()] then return appendices[let:upper()], let, rest end
  elseif keyword == "Section" then
    local num, rest = tok:match("^(%d+%.%d[%d%.]*)(.*)$")
    if num and sections[num] then return sections[num], num, rest end
  end
  return nil
end

-- inline containers we descend INTO (refs are often inside *italic* summary lines,
-- **bold**, spans, etc.). We deliberately do NOT recurse into Link (avoid double-
-- wrapping an existing link) or Code/Math (no linkable prose there).
local CONTAINER = {
  Emph = true, Strong = true, Underline = true, Strikeout = true,
  Superscript = true, Subscript = true, SmallCaps = true, Span = true, Quoted = true,
}

local function rewrite(inlines)
  local out, i, n = {}, 1, #inlines
  while i <= n do
    local el = inlines[i]
    local handled = false

    if el.t == "Str" then
      -- Form A: keyword + Space + token  (Chapter 8 / Appendix C / Section 8.2)
      -- allow a leading-punct prefix on the keyword token, e.g. "(Chapter"
      local pfx, kw = el.text:match("^(.-)(%a+)$")
      if kw and (kw == "Chapter" or kw == "Ch" or kw == "Appendix" or kw == "Section")
         and inlines[i+1] and inlines[i+1].t == "Space"
         and inlines[i+2] and inlines[i+2].t == "Str" then
        local id, core, rest = resolve(kw, inlines[i+2].text)
        if id then
          if pfx ~= "" then out[#out+1] = pandoc.Str(pfx) end
          out[#out+1] = mklink({ pandoc.Str(kw), pandoc.Space(), pandoc.Str(core) }, id)
          if rest and rest ~= "" then out[#out+1] = pandoc.Str(rest) end
          i, handled = i + 3, true
        end
      end

      -- Form B: "§8.2" as one token, possibly with surrounding punctuation
      if not handled then
        local pre, snum, post = el.text:match("^(.-)§(%d+%.%d[%d%.]*)(.*)$")
        if snum and sections[snum] then
          if pre ~= "" then out[#out+1] = pandoc.Str(pre) end
          out[#out+1] = mklink({ pandoc.Str("§" .. snum) }, sections[snum])
          if post ~= "" then out[#out+1] = pandoc.Str(post) end
          i, handled = i + 1, true
        end
      end
    elseif CONTAINER[el.t] and el.content then
      el.content = rewrite(el.content)   -- descend into italics/bold/spans
    end

    if not handled then out[#out+1] = el; i = i + 1 end
  end
  return out
end

local function do_block(el)
  el.content = rewrite(el.content)
  return el
end

return {
  { Header = harvest },                    -- pass 1: build the anchor maps
  { Para = do_block, Plain = do_block },   -- pass 2: link prose references
}
