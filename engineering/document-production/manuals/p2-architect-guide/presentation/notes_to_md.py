#!/usr/bin/env python3
"""Extract the deck's presenter notes into a scannable Markdown file: one
section per slide (number + title), the timing label in bold, and the talk
track broken from a dense paragraph into a bulleted list of sentences. Also
lists the on-screen bullets for context. Reads the generated .pptx so the doc
always matches the deck."""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

SRC, OUT = sys.argv[1], sys.argv[2]
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"


def sp_text_by_para(sp):
    out = []
    for para in sp.iter(A + "p"):
        runs = [t.text or "" for t in para.iter(A + "t")]
        txt = "".join(runs).strip()
        if txt:
            out.append(txt)
    return out


def ph_type(sp):
    ph = sp.find(f".//{P}nvSpPr/{P}nvPr/{P}ph")
    if ph is None:
        return None, None
    return ph.get("type"), ph.get("idx")


def split_sentences(text):
    # protect a few abbreviations, then split on sentence-final punct + space
    prot = text
    for ab in ("e.g.", "i.e.", "vs.", "Dr.", "Mr.", "Ms.", "St."):
        prot = prot.replace(ab, ab.replace(".", "\0"))
    parts = re.split(r'(?<=[.?!])\s+(?=[A-Z0-9"“‘\'])', prot)
    return [p.replace("\0", ".").strip() for p in parts if p.strip()]


z = zipfile.ZipFile(SRC)
n = len(z.namelist())
lines = ["# Thinking in P2: Functional Decomposition — Presenter Notes", "",
         "*Talk track for each slide, listified for quick scanning. "
         "Generated from the deck.*", ""]

idx = 1
while f"ppt/slides/slide{idx}.xml" in z.namelist():
    slide = ET.fromstring(z.read(f"ppt/slides/slide{idx}.xml"))
    title, bullets = f"Slide {idx}", []
    for sp in slide.iter(P + "sp"):
        t, i = ph_type(sp)
        txt = sp_text_by_para(sp)
        if t in ("title", "ctrTitle"):
            title = " ".join(txt) if txt else title
        elif t == "body" or i == "1":
            bullets = txt
    # notes
    note_txt = ""
    nf = f"ppt/notesSlides/notesSlide{idx}.xml"
    if nf in z.namelist():
        ns = ET.fromstring(z.read(nf))
        for sp in ns.iter(P + "sp"):
            t, i = ph_type(sp)
            if t == "body" or i == "3":
                note_txt = " ".join(sp_text_by_para(sp)).strip()

    lines.append(f"## Slide {idx} — {title}")
    lines.append("")
    if bullets:
        lines.append("*On screen:* " + " · ".join(bullets))
        lines.append("")
    if note_txt:
        sents = split_sentences(note_txt)
        # first sentence is the LABEL (e.g. "FORCE 1 (≈90s).") -> bold lead
        if sents and re.match(r"^[A-Z0-9].{0,100}\)$", sents[0].rstrip(".")):
            lines.append(f"**{sents[0].rstrip('.')}**")
            lines.append("")
            sents = sents[1:]
        for s in sents:
            lines.append(f"- {s}")
    lines.append("")
    idx += 1

open(OUT, "w").write("\n".join(lines) + "\n")
print(f"wrote {OUT} ({idx-1} slides)")
