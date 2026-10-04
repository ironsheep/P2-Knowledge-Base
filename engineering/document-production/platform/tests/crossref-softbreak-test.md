# Chapter 1: References Under Test

Each paragraph below is one case. The marker token at the start of each is unique so a
text search can locate the page, and every case targets a heading that either exists in
this document or deliberately does not.

CASE-CONTROL-SPACE — the terminal configures 8N1 exclusively (Chapter 2), and this is the
control: a reference separated from its number by an ordinary space. It linked before the
change and must still link after it.

CASE-FIX-WRAP — the terminal configures 8N1 exclusively (Chapter
3), and this is the case the change is for. The source wraps between the keyword and the
number, so pandoc emits a SoftBreak where a Space would normally sit.

CASE-NEG-PLAIN — there is no Chapter 99 in this document, so this reference must stay
plain text. If it links, the filter is matching things that do not exist.

CASE-NEG-WRAP — there is likewise no Chapter
98 in this document. This is the negative control for the new path specifically: the
SoftBreak branch must still honour the target-must-exist rule.

CASE-APPX-SPACE — see Appendix A for the appendix control.

CASE-APPX-WRAP — see Appendix
A for the appendix wrapped case.

CASE-SECT-SPACE — see Section 2.1 for the section control.

CASE-SECT-WRAP — see Section
2.1 for the section wrapped case.

# Chapter 2: Control Target

This chapter exists so the control reference has somewhere to land.

## 2.1 Section Target

This section exists so the Section references have somewhere to land.

# Chapter 3: Wrapped Target

This chapter exists so the wrapped reference has somewhere to land.

# Appendix A: Appendix Target

This appendix exists so the Appendix references have somewhere to land.
