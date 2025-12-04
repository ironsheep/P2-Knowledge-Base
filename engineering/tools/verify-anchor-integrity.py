#!/usr/bin/env python3
"""
Verify anchor integrity in PASM2 manual files.

Extracts all anchor definitions and link targets, then cross-references
to identify broken links (links pointing to non-existent anchors).
"""

import re
import os
import sys
from pathlib import Path
from collections import defaultdict

def extract_anchors(content, filename):
    """Extract all anchor definitions from markdown content."""
    anchors = set()

    # Pattern 1: Explicit anchors {#anchor-name}
    explicit = re.findall(r'\{#([^}]+)\}', content)
    anchors.update(explicit)

    # Pattern 2: ATX headings (## Heading) - generate anchors from text
    # Markdown auto-generates anchors from heading text
    headings = re.findall(r'^#{1,6}\s+(.+?)(?:\s*\{#[^}]+\})?\s*$', content, re.MULTILINE)
    for heading in headings:
        # Generate anchor from heading text (lowercase, spaces to hyphens, remove special chars)
        anchor = heading.lower()
        anchor = re.sub(r'[^\w\s-]', '', anchor)
        anchor = re.sub(r'\s+', '-', anchor)
        anchor = anchor.strip('-')
        if anchor:
            anchors.add(anchor)

    return anchors

def extract_links(content, filename):
    """Extract all in-document link targets from markdown content."""
    links = []

    # Pattern: [text](#anchor)
    matches = re.finditer(r'\[([^\]]+)\]\(#([^)]+)\)', content)
    for match in matches:
        links.append({
            'text': match.group(1),
            'anchor': match.group(2),
            'file': filename,
            'position': match.start()
        })

    return links

def extract_cross_file_links(content, filename):
    """Extract any remaining cross-file links (should be none after fix)."""
    links = []

    # Pattern: [text](filename.md#anchor)
    matches = re.finditer(r'\[([^\]]+)\]\(([^)#]+\.md)#([^)]+)\)', content)
    for match in matches:
        links.append({
            'text': match.group(1),
            'target_file': match.group(2),
            'anchor': match.group(3),
            'source_file': filename,
            'position': match.start()
        })

    return links

def main():
    # Directory containing the files
    opus_master = Path('/workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master')

    all_anchors = set()
    all_links = []
    all_cross_file_links = []
    anchors_by_file = defaultdict(set)

    # Process all markdown files
    print("=" * 70)
    print("ANCHOR INTEGRITY VERIFICATION")
    print("=" * 70)

    md_files = list(opus_master.rglob('*.md'))
    print(f"\nProcessing {len(md_files)} markdown files...\n")

    for md_file in sorted(md_files):
        if md_file.name == 'README.md':
            continue  # Skip README

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        rel_path = md_file.relative_to(opus_master)

        # Extract anchors
        anchors = extract_anchors(content, str(rel_path))
        all_anchors.update(anchors)
        anchors_by_file[str(rel_path)] = anchors

        # Extract in-document links
        links = extract_links(content, str(rel_path))
        all_links.extend(links)

        # Extract cross-file links (should be none)
        cross_links = extract_cross_file_links(content, str(rel_path))
        all_cross_file_links.extend(cross_links)

    # Report statistics
    print("STATISTICS")
    print("-" * 40)
    print(f"Total anchor definitions: {len(all_anchors)}")
    print(f"Total in-document links: {len(all_links)}")
    print(f"Total cross-file links: {len(all_cross_file_links)}")

    # Check for broken links
    print("\n" + "=" * 70)
    print("BROKEN LINK CHECK")
    print("=" * 70)

    broken_links = []
    for link in all_links:
        if link['anchor'] not in all_anchors:
            broken_links.append(link)

    if broken_links:
        print(f"\n❌ FOUND {len(broken_links)} BROKEN LINKS:")
        print("-" * 40)
        for link in broken_links:
            print(f"  File: {link['file']}")
            print(f"  Link: [{link['text']}](#{link['anchor']})")
            print()
    else:
        print("\n✅ All in-document links are valid!")

    # Check for remaining cross-file links
    if all_cross_file_links:
        print("\n" + "=" * 70)
        print("⚠️  REMAINING CROSS-FILE LINKS (should be converted)")
        print("=" * 70)
        for link in all_cross_file_links:
            print(f"  Source: {link['source_file']}")
            print(f"  Link: [{link['text']}]({link['target_file']}#{link['anchor']})")
            print()
    else:
        print("\n✅ No cross-file links remaining!")

    # Report anchor counts by file
    print("\n" + "=" * 70)
    print("ANCHORS BY FILE")
    print("=" * 70)
    for filepath in sorted(anchors_by_file.keys()):
        count = len(anchors_by_file[filepath])
        print(f"  {filepath}: {count} anchors")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    if broken_links or all_cross_file_links:
        print(f"❌ Issues found: {len(broken_links)} broken links, {len(all_cross_file_links)} cross-file links")
        return 1
    else:
        print("✅ All links verified successfully!")
        return 0

if __name__ == '__main__':
    sys.exit(main())
