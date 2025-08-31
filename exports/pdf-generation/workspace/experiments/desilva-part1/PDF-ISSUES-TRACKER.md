# PDF Generation Issues Tracker
## Last Updated: 2025-08-23 01:45

## ✅ FIXED (Don't report these again)
- [x] Font changed from Charter to Palatino
- [x] Code blocks have yellow background (pastel FFFACD)
- [x] Technical Review cover page added
- [x] Table of Contents included
- [x] Footer says "Draft for Technical Review"
- [x] Chapter numbering enabled (was disabled)
- [x] Monospace font for code blocks
- [x] Correct pastel colors per style guide
- [x] Lists properly formatted with blank lines
- [x] Excessive horizontal separators removed from markdown
- [x] Günter deSilva's full name used throughout

## 🔧 ATTEMPTED FIXES (Need verification in next PDF)
- [ ] TOC red boxes - added linkcolor=black
- [ ] Chapters starting on new pages - changed method
- [ ] Page headers showing chapter names - fixed chaptermark
- [ ] Bold titles/headings - added \bfseries
- [ ] Green chapter-end boxes - added border
- [ ] Code alignment - set columns=fixed

## ❌ STILL BROKEN (Known issues)
- [ ] Double asterisks ** showing instead of bold (Pandoc issue)
- [ ] Backslashes showing in narrative text (escaping issue)
- [ ] Famous quotes left-aligned (should be centered)
- [ ] Section end markers not inside green blocks
- [ ] Chapter 2 appears at end of Part 1 (but needs to stay for concatenation)

## 📝 NEW ISSUES (Not yet reported)
_Add new issues here after each PDF test_

## 🎯 NEXT STEPS
1. Test PDF with current fixes
2. Update this tracker with results
3. Only report NEW issues not listed above
4. Work through STILL BROKEN items systematically

## 💡 WORKFLOW IMPROVEMENT
Instead of reporting all issues each time:
1. Check this tracker first
2. Only report NEW issues
3. Confirm which "attempted fixes" worked
4. Update tracker after each iteration