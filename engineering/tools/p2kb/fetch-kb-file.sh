#!/bin/bash
# P2 Knowledge Base Fetcher v2.1 - Pre-approvable with progress
# Usage: fetch-kb-file.sh <path> [--verbose]

path=$1
verbose=${2:-""}
cache=".p2kb-cache/${path}"
url="https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/${path}"

# Progress reporting to stderr (doesn't interfere with stdout)
report() { echo "P2KB: $1" >&2; }

if [ "$verbose" = "--verbose" ]; then
  report "Fetching: $path"
fi

if [ -f "$cache" ]; then
  [ "$verbose" = "--verbose" ] && report "Using cached: $cache"
  cat "$cache"
  result=$?
else
  [ "$verbose" = "--verbose" ] && report "Downloading: $url"
  mkdir -p "$(dirname "$cache")"
  
  # Download with progress reporting
  if command -v curl &>/dev/null; then
    curl -sS -o "$cache" "$url" 2>/dev/null
    result=$?
  elif command -v wget &>/dev/null; then
    wget -q -O "$cache" "$url"
    result=$?
  else
    report "ERROR: Neither curl nor wget found"
    exit 1
  fi
  
  if [ $result -eq 0 ]; then
    [ "$verbose" = "--verbose" ] && report "Downloaded successfully: $path"
    cat "$cache"
  else
    report "ERROR: Download failed for $path"
    rm -f "$cache"  # Remove partial download
    exit $result
  fi
fi

# Report completion for tracking
[ "$verbose" = "--verbose" ] && report "Complete: $path (exit: $result)"
exit $result
