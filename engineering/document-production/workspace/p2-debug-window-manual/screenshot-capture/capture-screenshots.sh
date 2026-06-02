#!/bin/bash
# capture-screenshots.sh — resumable screenshot capture for the P2 Debug Window Manual.
#
# Run on a host with a P2 attached. AUTO-ITERATES every example in examples/: compiles
# it with pnut-ts, runs it with PNut Term-ts (-r downloads to RAM and runs), and the
# example SAVEs its own DEBUG window to a .bmp in captures/screenshots/.
#
# This script does NOT convert images (the capture host has no image tools). The .bmp
# files are converted to .png back in the doc container with bmp2png.py.
#
# RESUMABLE: skips any example that already has a NON-EMPTY .bmp, so re-running picks up
# the next missing/failed capture. (A 0-byte or bad capture: just delete its .bmp and
# re-run — only the missing ones are attempted.)
#
# Each example ends after it SAVEs (with a flush delay first), so PNut Term-ts may
# self-quit on program end and the loop advances unattended; if it doesn't self-quit,
# just quit PNut Term-ts after the save and the loop continues.

set -u
cd "$(dirname "$0")" || exit 1

# ================ SET THESE ONCE — applied to EVERY example automatically ================
CC='pnut-ts -d'                  # compiler: .spin2 -> .bin
RUN='pnut-term-ts -r {BIN}'      # PNut Term-ts: -r = download .bin to RAM and run ({BIN} auto-filled)
# ========================================================================================

EXAMPLES_DIR="examples"          # instrumented self-saving .spin2 files (one per figure)
CAPTURE_DIR="captures"           # PNut Term-ts working dir
SAVE_DIR="$CAPTURE_DIR/screenshots"   # PNut Term-ts writes SAVE images into this subdir

mkdir -p "$CAPTURE_DIR"
shopt -s nullglob
ran=0; skipped=0; total=0

for spin in "$EXAMPLES_DIR"/*.spin2; do
  total=$((total + 1))
  base="$(basename "$spin" .spin2)"          # e.g. fig-05-plot-gauge
  bmp="$SAVE_DIR/$base.bmp"

  if [ -s "$bmp" ]; then                      # -s : exists AND non-empty
    echo "skip    $base  (already captured)"
    skipped=$((skipped + 1)); continue
  fi
  rm -f "$bmp"                                 # clear any 0-byte leftover

  echo "build   $base"
  if ! $CC "$spin" >/dev/null 2>&1; then
    echo "  !! compile failed — skipping"; continue
  fi
  bin="${spin%.spin2}.bin"

  echo "run     $base  (window opens, SAVEs itself, program ends; quit PNut Term-ts if it doesn't)"
  ( cd "$CAPTURE_DIR" && eval "${RUN/\{BIN\}/../$bin}" )       # blocks until PNut Term-ts exits

  if [ -s "$bmp" ]; then
    echo "  -> captured  $bmp"; ran=$((ran + 1))
  else
    echo "  !! no (or empty) ${base}.bmp produced — will retry on the next run"
  fi
done

echo ""
echo "captured this run: $ran    already had: $skipped    total: $total"
echo "BMPs are in $SAVE_DIR/ — convert them to PNG in the doc container with:  python3 bmp2png.py"
