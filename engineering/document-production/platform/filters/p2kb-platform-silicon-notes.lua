--[[
  p2kb-platform-silicon-notes.lua  —  P2KB platform silicon-note tag + index

  A silicon note is a one-sentence rule about how the current silicon behaves
  that a reader rarely meets but must not miss when they do (a silicon erratum,
  stated in the manual's own voice, at the point of use). It is marked with a
  small inline tag, never a box: a box signals "this matters to everyone here",
  which is wrong for a rare case and would compete with the manual's real trap
  callouts.

  AUTHORING (the sentence leads with the tag; the tag replaces "On Rev C silicon,"):

      [Rev C]{.silicon-note topic="DEBUG_TIMESTAMP stamp order"} A message from ...

    * The span's CONTENT is the visible tag text (normally "Rev C"). Without this
      filter the span still reads sensibly as plain "Rev C".
    * `topic` names the rule in a few words. It is what the index lists, so it
      must say what the rule is about, not where it is. Plain text only — no
      backticks (the escape pass cannot protect inline code inside an attribute).

  INDEX (optional, per manual — use it where a manual carries three or more notes):

      # Appendix X: Silicon Notes

      One intro sentence in the manual's voice.

      ::: silicon-note-index
      :::

    The empty div is replaced by one line per note, in document order:
        <topic, linked to the note> — <chapter>; <section> — page N
    The index only points; it never restates a rule, so nothing lives in two
    places. When the amended Parallax documentation is published, its citation
    goes in the appendix intro, once.

  LaTeX macros (p2kb-platform-content.sty): \SiliconNoteAnchor{id} (link target +
  page label), \SiliconNoteTag{text} (the chip). Both live in the shared content
  layer, so every platform manual can use them; a manual that never writes a
  silicon-note span is unaffected.

  FILTER ORDER: run BEFORE p2kb-platform-tables. The tables filter flattens each
  cell's inlines, so a table-cell note must already be raw LaTeX when it arrives;
  in that order a note in a cell keeps its tag and its index entry (proven by
  platform/tests/silicon-notes-test.md).

  The latex escape pass protects the `]{.class attr="..."}` block (it is markdown
  syntax, not content) — see latex_escape_processor.py.
]]

if FORMAT ~= "latex" then return {} end

local notes = {}          -- { id, topic (inlines), chapter (inlines), section (inlines|nil) }
local chapter, section    -- the header inlines in force at the current point

local function warn(msg)
  io.stderr:write("[p2kb-platform-silicon-notes] WARNING: " .. msg .. "\n")
end

local function topic_inlines(span, fallback)
  local t = span.attributes["topic"]
  if not t or t:match("^%s*$") then
    warn("silicon-note without a topic; the index will show its section title")
    return fallback
  end
  local doc = pandoc.read(t, "markdown")
  local blk = doc.blocks[1]
  if blk and blk.content then return blk.content end
  return { pandoc.Str(t) }
end

local function tag_note(span)
  local id = "silicon-note-" .. (#notes + 1)
  local label = span.content
  if #label == 0 then label = { pandoc.Str("Rev"), pandoc.Space(), pandoc.Str("C") } end
  notes[#notes + 1] = {
    id      = id,
    topic   = topic_inlines(span, section or chapter or label),
    chapter = chapter,
    section = section,
  }
  local out = {
    pandoc.RawInline("latex", "\\SiliconNoteAnchor{" .. id .. "}\\SiliconNoteTag{"),
  }
  for _, el in ipairs(label) do out[#out + 1] = el end
  out[#out + 1] = pandoc.RawInline("latex", "}")
  return out
end

local span_filter = {
  Span = function(span)
    if span.classes:includes("silicon-note") then return tag_note(span) end
  end,
}

-- Walk blocks in document order so each note knows the chapter/section it sits in.
local function visit(blocks)
  for i, blk in ipairs(blocks) do
    if blk.t == "Header" then
      if blk.level == 1 then chapter, section = blk.content, nil
      else section = blk.content end
    elseif blk.t == "Div" and blk.classes:includes("silicon-note-index") then
      -- filled in after the whole document has been read
    elseif blk.t == "Div" or blk.t == "BlockQuote" then
      -- reassign: element lists may be marshalled copies, not live references
      local c = blk.content
      visit(c)
      blk.content = c
      blocks[i] = blk
    else
      blocks[i] = pandoc.walk_block(blk, span_filter)
    end
  end
end

local function index_line(n)
  local line = { pandoc.Link(n.topic, "#" .. n.id), pandoc.Space(),
                 pandoc.Str("—"), pandoc.Space() }
  if n.chapter then
    for _, el in ipairs(n.chapter) do line[#line + 1] = el end
  end
  if n.section then
    line[#line + 1] = pandoc.Str(";")
    line[#line + 1] = pandoc.Space()
    for _, el in ipairs(n.section) do line[#line + 1] = el end
  end
  line[#line + 1] = pandoc.Space()
  line[#line + 1] = pandoc.Str("—")
  line[#line + 1] = pandoc.Space()
  line[#line + 1] = pandoc.RawInline("latex", "page~\\pageref{" .. n.id .. "}")
  return { pandoc.Plain(line) }
end

local function fill_index(blocks)
  for i, blk in ipairs(blocks) do
    if blk.t == "Div" and blk.classes:includes("silicon-note-index") then
      if #notes == 0 then
        warn("silicon-note-index placed but the document has no silicon notes")
        blocks[i] = pandoc.Null()
      else
        local items = {}
        for _, n in ipairs(notes) do items[#items + 1] = index_line(n) end
        blocks[i] = pandoc.BulletList(items)
      end
    elseif blk.t == "Div" or blk.t == "BlockQuote" then
      local c = blk.content
      fill_index(c)
      blk.content = c
      blocks[i] = blk
    end
  end
end

return {
  {
    Pandoc = function(doc)
      local b = doc.blocks
      visit(b)
      fill_index(b)
      doc.blocks = b
      return doc
    end,
  },
}
