#!/bin/bash
# ============================================================================
#  PDF Forge — FONT discovery
#
#  Companion to pdfforge-discovery.sh, which captured a font list once (Aug
#  2025, see pdfforge-capabilities.txt "SYSTEM FONTS"). That capture is not
#  enough, for one specific reason: it lists what FONTCONFIG knows by NAME,
#  and IBM Plex — the family the Donna manuscript is actually being set in
#  right now — does not appear in it. So the old list is either stale or is
#  describing a different surface than the one that matters.
#
#  What matters is the TeX tree, because our templates load fonts BY FILENAME
#  through kpathsea, not by family name through fontconfig:
#
#      \setmainfont{IBMPlexSerif}[Extension=.otf,
#        UprightFont=*-Regular, BoldFont=*-Bold,
#        ItalicFont=*-Italic,   BoldItalicFont=*-BoldItalic]
#
#  So this script answers three questions the old capture cannot:
#    1. which font FILES are in the TeX tree (loadable by filename)
#    2. which families have all FOUR styles under one consistent stem
#       (without that, the \setmainfont pattern above cannot work)
#    3. which carry the two features a book actually needs — real SMALL CAPS
#       (smcp) and OLDSTYLE FIGURES (onum). Our foundation currently FAKES
#       small caps by letterspacing uppercase, because IBM Plex Serif has
#       none; and this book is saturated with dates and numbers, which is
#       exactly where oldstyle figures earn their keep.
#
#  Safe to run: read-only, no root, installs nothing, writes one report file
#  into the current directory.
#
#  Usage:   ./pdfforge-font-discovery.sh
#  Output:  pdfforge-font-report.txt   <- send this back
#
#  Runtime: a few minutes on a full TeX Live (it probes one face per family,
#  not every file).
# ============================================================================

OUT="pdfforge-font-report.txt"
: > "$OUT"

say()   { printf '%s\n' "$*" >> "$OUT"; }
head1() { say ""; say "============================================================"; say "$*"; say "============================================================"; }
head2() { say ""; say "--- $* ---"; }
progress() { printf '[font-discovery] %s\n' "$*" >&2; }
have()  { command -v "$1" >/dev/null 2>&1; }

say "PDF Forge — Font Discovery Report"
say "Generated: $(date)"
say "Host:      $(hostname 2>/dev/null)"
say ""
say "Read-only probe. Send this whole file back."

# ---------------------------------------------------------------------------
head1 "1. ENVIRONMENT"
# ---------------------------------------------------------------------------
say "uname: $(uname -a 2>&1)"
[ -r /etc/os-release ] && say "os:    $(. /etc/os-release 2>/dev/null; printf '%s' "$PRETTY_NAME")"

head2 "tool versions"
for t in xelatex lualatex pdflatex pandoc kpsewhich otfinfo fc-list tlmgr; do
  if have "$t"; then
    say "$(printf '%-10s' "$t") PRESENT   $("$t" --version 2>&1 | head -1)"
  else
    say "$(printf '%-10s' "$t") -- NOT FOUND --"
  fi
done

head2 "TeX Live roots"
if have kpsewhich; then
  for v in TEXMFDIST TEXMFLOCAL TEXMFHOME TEXMFVAR OPENTYPEFONTS TTFONTS; do
    say "$(printf '%-14s' "$v") $(kpsewhich --var-value=$v 2>&1)"
  done
else
  say "kpsewhich not available — cannot resolve TeX roots."
fi

# ---------------------------------------------------------------------------
head1 "2. FONT FILES IN THE TeX TREE (loadable by filename — what we need)"
# ---------------------------------------------------------------------------
progress "scanning the TeX tree for .otf/.ttf files..."

SEARCH_DIRS=""
for d in \
  "$(kpsewhich --var-value=TEXMFDIST 2>/dev/null)" \
  "$(kpsewhich --var-value=TEXMFLOCAL 2>/dev/null)" \
  "$(kpsewhich --var-value=TEXMFHOME 2>/dev/null)" \
  /usr/share/texlive /usr/local/texlive /opt/texlive /usr/share/texmf ; do
  [ -n "$d" ] && [ -d "$d" ] && SEARCH_DIRS="$SEARCH_DIRS
$d"
done
SEARCH_DIRS=$(printf '%s\n' "$SEARCH_DIRS" | grep -v '^$' | sort -u)

say "Scanned roots:"
if [ -n "$SEARCH_DIRS" ]; then
  printf '%s\n' "$SEARCH_DIRS" | sed 's/^/    /' >> "$OUT"
else
  say "    (none — no TeX tree found at any of the usual locations)"
fi

FONTLIST=$(mktemp); REGLIST=$(mktemp); FAMFILE=$(mktemp)
trap 'rm -f "$FONTLIST" "$REGLIST" "$FAMFILE"' EXIT

printf '%s\n' "$SEARCH_DIRS" | while IFS= read -r d; do
  [ -n "$d" ] && find "$d" -type f \( -iname '*.otf' -o -iname '*.ttf' \) 2>/dev/null
done | sort -u > "$FONTLIST"

TOTAL=$(wc -l < "$FONTLIST" | tr -d ' ')
say ""
say "Total font files found in the TeX tree: $TOTAL"

if [ "$TOTAL" -eq 0 ]; then
  say ""
  say "NOTHING FOUND. Either the roots above are wrong, or fonts live"
  say "elsewhere on this machine. Section 5 (fontconfig) and section 6"
  say "(packages) will still be informative."
fi

# family = containing directory
awk -F/ 'NF>1 { d=$1; for(i=2;i<NF;i++) d=d"/"$i; print d }' "$FONTLIST" | sort -u > "$FAMFILE"

head2 "font files grouped by directory"
say "A family is USABLE BY OUR TEMPLATES only if it shows all four of"
say "Regular / Bold / Italic / BoldItalic under one consistent stem."

while IFS= read -r dir; do
  [ -z "$dir" ] && continue
  n=$(grep -c "^${dir}/[^/]*$" "$FONTLIST")
  [ "$n" -eq 0 ] && continue
  say ""
  say "[$n files] $dir"
  grep "^${dir}/[^/]*$" "$FONTLIST" | sed "s|^${dir}/|      |" | sort >> "$OUT"
done < "$FAMFILE"

# ---------------------------------------------------------------------------
head1 "3. BOOK-READINESS PROBE (real small caps + oldstyle figures)"
# ---------------------------------------------------------------------------
if ! have otfinfo; then
  say "otfinfo NOT AVAILABLE — cannot read OpenType feature tags."
  say "It ships with TeX Live as part of lcdf-typetools. If this section is"
  say "empty that is why; the rest of the report is still good."
elif [ "$TOTAL" -eq 0 ]; then
  say "Skipped — no font files found in section 2."
else
  say "One upright face probed per family (probing every file would take far"
  say "longer and say the same thing)."
  say ""
  say "  smcp = real small capitals      onum = oldstyle (text) figures"
  say ""
  say "Both matter here. The book is full of datelines and numbers, and our"
  say "foundation currently fakes small caps by letterspacing uppercase."
  say ""
  say "STATUS  SMCP  ONUM  FILE"
  say "------  ----  ----  ------------------------------------------------"

  progress "probing OpenType features (the slow part)..."

  grep -iE '[-_]?(Regular|Roman|Book)\.(otf|ttf)$' "$FONTLIST" > "$REGLIST"
  # families with no *-Regular: take the first file in that directory
  while IFS= read -r dir; do
    [ -z "$dir" ] && continue
    grep -q "^${dir}/[^/]*$" "$REGLIST" || grep -m1 "^${dir}/[^/]*$" "$FONTLIST" >> "$REGLIST"
  done < "$FAMFILE"
  sort -u "$REGLIST" -o "$REGLIST"

  BOOKFAM=$(mktemp)
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    feats=$(otfinfo -f "$f" 2>/dev/null) || continue
    [ -z "$feats" ] && continue
    sc="  . "; on="  . "
    printf '%s\n' "$feats" | grep -q '^smcp' && sc=" YES"
    printf '%s\n' "$feats" | grep -q '^onum' && on=" YES"
    if [ "$sc" = " YES" ] && [ "$on" = " YES" ]; then
      status="BOOK  "; printf '%s\n' "$f" >> "$BOOKFAM"
    elif [ "$sc" = " YES" ] || [ "$on" = " YES" ]; then
      status="part  "
    else
      status="      "
    fi
    say "$status  $sc  $on  $f"
  done < "$REGLIST"

  say ""
  say "Rows marked BOOK have BOTH real small caps and oldstyle figures."
  say "BOOK-grade families found: $(wc -l < "$BOOKFAM" 2>/dev/null | tr -d ' ')"
  head2 "the BOOK-grade shortlist"
  sort "$BOOKFAM" 2>/dev/null >> "$OUT"
  rm -f "$BOOKFAM"
fi

# ---------------------------------------------------------------------------
head1 "4. TARGETED CHECK — the families actually under consideration"
# ---------------------------------------------------------------------------
say "For each: is it in the TeX tree, and does it have the four styles our"
say "\\setmainfont pattern needs? A READY block can be pasted straight into"
say "donna-book-foundation.sty."
say ""
say "The first group is what the Aug-2025 fontconfig capture said this"
say "machine has; the second is worth checking even though that capture"
say "did not list it, since the capture also missed IBM Plex."

report_stem() {
  # $1 = an upright font file; report whether the four-style set exists.
  #
  # The upright face is NOT always called "-Regular". Several of the best
  # book families in TeX Live name it "-Roman" (Cochineal, XCharter,
  # Domitian, Crimson) and a few use "-Book". An earlier version of this
  # script only knew "-Regular" and therefore reported "no complete set"
  # for exactly the families we most wanted — so try each upright spelling.
  f="$1"
  base=$(basename "$f"); ext="${base##*.}"
  dir=$(dirname "$f")

  upright=""
  for u in Regular Roman Book; do
    case "$base" in
      *-$u.*) upright="$u"; break ;;
    esac
  done
  [ -z "$upright" ] && return 0

  stem=$(printf '%s' "$base" | sed -E "s/-${upright}\.(otf|ttf)$//")
  ok=1
  for s in "$upright" Bold Italic BoldItalic; do
    [ -f "$dir/$stem-$s.$ext" ] || ok=0
  done
  if [ "$ok" -eq 1 ]; then
    say ""
    say "    READY — all four styles present:"
    say "      \\setmainfont{$stem}[Extension=.$ext,"
    say "        UprightFont=*-$upright, BoldFont=*-Bold,"
    say "        ItalicFont=*-Italic,   BoldItalicFont=*-BoldItalic]"
    if have otfinfo; then
      fe=$(otfinfo -f "$dir/$stem-$upright.$ext" 2>/dev/null)
      s=no; o=no
      printf '%s\n' "$fe" | grep -q '^smcp' && s=YES
      printf '%s\n' "$fe" | grep -q '^onum' && o=YES
      say "      real small caps: $s     oldstyle figures: $o"
    fi
  else
    say "      (no complete $upright/Bold/Italic/BoldItalic set under stem '$stem')"
  fi
}

check_family() {
  label="$1"; shift
  say ""
  say "### $label"
  found=0
  for pat in "$@"; do
    hits=$(grep -i "/[^/]*${pat}[^/]*\.\(otf\|ttf\)$" "$FONTLIST" 2>/dev/null)
    [ -z "$hits" ] && continue
    found=1
    printf '%s\n' "$hits" | sed 's/^/    /' >> "$OUT"
    printf '%s\n' "$hits" | while IFS= read -r h; do report_stem "$h"; done
  done
  [ "$found" -eq 0 ] && say "    NOT FOUND in the TeX tree."
  return 0
}

say ""
say "======== group A: listed in the Aug-2025 capture ========"
check_family "EB Garamond — first choice. The capture shows dedicated SC (small-caps) faces, which is exactly what our faux-small-caps workaround exists to replace." "EBGaramond" "ebgaramond"
check_family "Linux Libertine / Libertinus — modern, even colour, very complete" "LinLibertine" "Libertinus" "libertine"
check_family "TeX Gyre Pagella (Palatino) — broad, highly legible" "texgyrepagella"
check_family "TeX Gyre Schola (Century Schoolbook) — maximum legibility" "texgyreschola"
check_family "TeX Gyre Termes / Bonum / Heros" "texgyretermes" "texgyrebonum" "texgyreheros"
check_family "Berenis ADF Pro — Baskerville-ish text family, genuinely a book face" "Berenis" "berenis"
check_family "Accanthis ADF — warm oldstyle, often used for literary work" "Accanthis" "accanthis"
check_family "Bitstream Charter / Charis SIL — sturdy, excellent on cheap stock" "Charter" "CharisSIL" "Charis"
check_family "Junicode — oldstyle with an enormous feature set" "Junicode"
check_family "Utopia / Heuristica / Erewhon — the Utopia lineage" "Utopia" "Heuristica" "Erewhon"
check_family "Gentium — humanist, very readable" "Gentium"
check_family "GFS Baskerville / GFS Didot" "GFSBaskerville" "GFSDidot" "Baskerv" "Didot"

say ""
say "======== group B: not in the capture, check anyway ========"
check_family "Cochineal — Crimson derivative, sturdier on cream stock" "Cochineal" "cochineal"
check_family "Crimson Pro" "CrimsonPro" "Crimson"
check_family "Alegreya — literary-contemporary, strong small caps" "Alegreya"
check_family "Source Serif" "SourceSerif"
check_family "IBM Plex — WHAT THE BOOK USES NOW, for comparison" "IBMPlex"

# ---------------------------------------------------------------------------
head1 "5. FONTCONFIG VIEW (system fonts, by NAME)"
# ---------------------------------------------------------------------------
say "Our foundation file records that fontconfig here could not resolve most"
say "fonts by name, which is why we load by filename. This section says"
say "whether that is still true, and lets us diff against the Aug-2025 list."
say ""
if have fc-list; then
  say "families known to fontconfig: $(fc-list : family 2>/dev/null | tr ',' '\n' | sed 's/^ *//' | sort -u | grep -c .)"
  head2 "full family list"
  fc-list : family 2>/dev/null | tr ',' '\n' | sed 's/^ *//' | sort -u >> "$OUT"
else
  say "fc-list not available (fontconfig not installed)."
fi

# ---------------------------------------------------------------------------
head1 "6. INSTALLED PACKAGES (font + TeX related)"
# ---------------------------------------------------------------------------
if have dpkg-query; then
  head2 "matching packages and versions"
  dpkg-query -W -f='${Package}\t${Version}\n' 2>/dev/null \
    | grep -iE 'font|texlive|tex-|otf|ttf|xetex|luatex|pandoc' | sort >> "$OUT"

  head2 "font files shipped by each font package"
  progress "listing font package contents..."
  dpkg-query -W -f='${Package}\n' 2>/dev/null \
    | grep -iE '^(fonts-|ttf-|otf-|xfonts-|texlive-fonts)' | sort \
    | while IFS= read -r p; do
        say ""
        say "### $p"
        dpkg -L "$p" 2>/dev/null | grep -iE '\.(otf|ttf|pfb)$' | sort >> "$OUT"
      done
else
  say "dpkg-query not available — not a Debian/Ubuntu image?"
  have rpm && { head2 "rpm font/tex packages"; rpm -qa 2>/dev/null | grep -iE 'font|texlive' | sort >> "$OUT"; }
fi

# ---------------------------------------------------------------------------
head1 "7. TeX Live PACKAGE MANAGER (what could be added)"
# ---------------------------------------------------------------------------
if have tlmgr; then
  say "tlmgr present — fonts could be added without apt."
  head2 "installed font-ish tlmgr packages"
  { tlmgr list --only-installed 2>/dev/null || tlmgr list 2>/dev/null; } \
    | grep -iE 'font|garamond|libertin|cochineal|crimson|alegreya|gyre|plex|junicode|accanthis|berenis' \
    | sort >> "$OUT"
else
  say "tlmgr not present — this is a distro-packaged TeX Live, so adding a"
  say "family means an apt package, or dropping .otf files into TEXMFLOCAL"
  say "and running mktexlsr."
fi

head1 "END OF REPORT"
say "Send $OUT back."

progress "done — wrote $OUT ($(wc -l < "$OUT" | tr -d ' ') lines)"
printf '\nReport written to: %s\nSend that file back.\n' "$OUT"
