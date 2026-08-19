```{=latex}
% ISP cover standard (p2kb-platform-isp-cover): maroon 5:1 band inset to the
% text block, trace field at the right, Iron Sheep mark alone bottom-right.
% This is an Iron Sheep Productions-only document — NO P2 Knowledge Base
% banner, no Parallax mark, no affiliation line.
\ispcoverband{PNut-Term-TS}{Downloader · Terminal · Debug Display}

\begin{center}
\vspace{1.4cm}
{\fontsize{34}{40}\selectfont\bfseries \DocTitle\par}
% 0.69cm not 0.35cm: the minipage below sets its own first baseline, which
% consumed 9.5pt of this gap (measured v1 vs v2 on the daemon, 20.8pt -> 11.3pt).
\vspace{0.69cm}
% Subtitle measure is PRESENTATION and stays here; the TEXT is single-sourced
% (\DocSubtitle from request.json). Narrowing the measure balances the two-line
% break — at full width it breaks after "for the" and orphans "Propeller 2".
{\Large\itshape\begin{minipage}{0.66\linewidth}\centering \DocSubtitle\end{minipage}\par}
\vspace{0.9cm}
{\large \DocDate\par}
\vspace{0.15cm}
{\large\color{iosp-review-border}\bfseries Version \DocVersion{} — Tool Developer Review Draft\par}
\vspace{0.15cm}
{\normalsize\color{iosp-review-border}Circulated to named tool authors for review. Not for public distribution.\par}

\vfill
\begin{tcolorbox}[
  colback=gray!5,
  colframe=gray!40,
  boxrule=1pt,
  width=0.85\textwidth,
  center,
  title={\bfseries\color{black} Guide Organization},
  colbacktitle=gray!15,
  coltitle=black
]
\textbf{A practical guide to operating PNut-Term-TS}

\vspace{0.3cm}
\begin{minipage}[t]{0.46\linewidth}
\textbf{Getting Oriented \& Using the GUI}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Where It Fits, and the Fork
\item The Main Window
\item Downloading \& Running
\item The Serial Terminal
\item Debug Windows \& Placement
\item The Single-Step Debugger
\item Menus, Settings, Devices
\item Further Features
\end{itemize}
\end{minipage}\hfill
\begin{minipage}[t]{0.46\linewidth}
\textbf{Headless \& Reference}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Running Headless
\item Ending a Run Cleanly
\item The Log as Feedback Loop
\item A Complete Automated Run
\item Command-Line Reference
\item Keyboard Shortcuts
\item Troubleshooting
\item Support \& Resources
\end{itemize}
\end{minipage}

\end{tcolorbox}
\end{center}

% The Iron Sheep mark stands alone bottom-right — it replaces the old
% publisher/affiliation text lines (ISP-only document, no KB affiliation).
\vfill
\ispcovermark

\clearpage
\pagestyle{fancy}

% ---- REVIEW-DRAFT ROADMAP -------------------------------------------------
% Draft scaffolding. Deleted when the reviewers' answers are written in; the
% release gate fails on any surviving ToolReviewBlock, this one included.
\begin{ToolReviewBlock}{Marco Maccaferri and Eric Smith}
Thank you for reading this. PNut-Term-TS downloads and runs binaries from any P2
compiler, and this guide now says so — which means it makes claims about
\emph{your} tools. We would rather print your words than our assumptions, so this
draft goes to you before it goes to anyone else.

\vspace{4pt}
Violet boxes like this one are questions for you, and each carries the name of the
person it is meant for. There are four, and they are all short:

\vspace{4pt}
\begin{itemize}[leftmargin=*, itemsep=2pt, topsep=0pt]
\item \textbf{Chapter 2} --- \emph{Marco}: we describe Spin Tools IDE as fully
      supported (debug windows and the debugger). Confirm or correct.
\item \textbf{Chapter 2} --- \emph{Eric}: what does FlexSpin's \texttt{debug()}
      output actually reach --- the display windows, or debug text only?
\item \textbf{Chapter 6} --- \emph{Eric}: we say a FlexSpin binary carries no
      readable debug baud rate. Is that right?
\item \textbf{Chapter 9} --- \emph{Eric}: can FlexSpin compile in the debugger
      kernel the single-step debugger needs?
\end{itemize}

\vspace{4pt}
Anything you would like said about your own tool, we will print as you write it.
Corrections anywhere else in the guide are welcome too.
\end{ToolReviewBlock}

\clearpage

\tableofcontents
\clearpage
\listoffigures
\clearpage
```

```{=latex}
% ISP copyright page — the mark carries the page that makes the ownership claim.
% Deliberately NOT a \chapter: \chapter forces a page break, which would strand
% the mark alone on the preceding page. The TOC entry is added by hand so the
% page still lists as "Copyright and License".
\ispcopyrightmark
% \phantomsection is REQUIRED before a hand-added TOC line: without an anchor of
% its own, hyperref points the entry at the last anchor it saw -- the document
% start -- so the bookmark and the TOC link both jumped to the cover instead of
% this page. (Verified in the 2026-08-08 pre-release check: entry targeted p1,
% section lives on p5.)
\phantomsection
\addcontentsline{toc}{chapter}{Copyright and License}
\markboth{Copyright and License}{}
\vspace{0.5cm}
{\Large\bfseries Copyright and License\par}
\vspace{0.4cm}
```

Copyright © 2026 Iron Sheep Productions, LLC.

PNut-Term-TS is © 2024–2026 Iron Sheep Productions, LLC and is licensed under the MIT License.

This user guide is licensed under the Creative Commons Attribution–ShareAlike 4.0 International License (CC BY-SA 4.0).

You are free to:

- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

To view the full license, visit: https://creativecommons.org/licenses/by-sa/4.0/

### Trademarks

Parallax, Propeller, Spin, and the Parallax logo are trademarks of Parallax Inc. This license grants permissions under copyright only; it does not grant rights to use these trademarks, and adapted or redistributed copies must not imply endorsement by, or official status with, Iron Sheep Productions, LLC.

```{=latex}
\clearpage
```
