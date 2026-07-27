```{=latex}
% Banner image at top (full width) with drop shadow for visual balance
\begin{tcolorbox}[
  enhanced,
  boxrule=1.5pt,
  colframe=gray!60,
  colback=white,
  drop shadow southeast,
  shadow={3pt}{-3pt}{1mm}{black!15},
  left=0pt, right=0pt, top=0pt, bottom=0pt,
  width=\textwidth,
  arc=0pt,
  outer arc=0pt
]
\includegraphics[width=\linewidth]{inbox/assets/book-artwork.png}
\end{tcolorbox}

\begin{center}
\vspace{0.4cm}
{\fontsize{36}{42}\selectfont\bfseries P2 Debug Window Manual\par}
\vspace{0.3cm}
{\Large\itshape See What Your Program Is Doing\par}
\vspace{0.35cm}
{\large July 2026\par}
\vspace{0.15cm}
{\large\color{blue}Version 1.1.1\par}

\vspace{0.5cm}
\begin{tcolorbox}[
  colback=gray!5,
  colframe=gray!40,
  boxrule=1pt,
  width=0.85\textwidth,
  center,
  title={\bfseries\color{black} Manual Organization},
  colbacktitle=gray!15,
  coltitle=black
]
{\footnotesize
\textbf{The nine DEBUG display windows of the Propeller 2}

\vspace{0.2cm}
\begin{minipage}[t]{0.45\textwidth}
\textbf{Part I --- Foundation}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item The DEBUG Display Windows
\item Getting Started
\end{itemize}
\vspace{0.15cm}
\textbf{Part II --- The Windows}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item TERM --- Text Output
\item BITMAP --- Pixel Raster
\item PLOT --- Vector Drawing
\item LOGIC --- Digital Waveforms
\item SCOPE --- Oscilloscope
\item SCOPE\_XY --- XY \& Phase
\item FFT --- Frequency Spectrum
\item SPECTRO --- Spectrogram
\item MIDI --- Keyboard Display
\end{itemize}
\end{minipage}%
\begin{minipage}[t]{0.45\textwidth}
\textbf{Part III --- Integration}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Bidirectional Control
\item Packed Data
\item Multiple Windows \& PASM
\end{itemize}
\vspace{0.15cm}
\textbf{Appendices}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Command Reference
\item Packed-Data Formats
\item Color \& Coordinate
\end{itemize}
\end{minipage}
} % end \footnotesize

\end{tcolorbox}
\vspace{0.3cm}

{\small Iron Sheep Productions, LLC\par}
{\small P2 Knowledge Base Project\par}
\end{center}

\clearpage
\pagestyle{fancy}

\tableofcontents
\clearpage
```

# Copyright and License

Copyright © 2026 Iron Sheep Productions, LLC and Parallax Inc.

This work is licensed under the Creative Commons Attribution–NonCommercial–NoDerivatives 4.0 International License (CC BY-NC-ND 4.0).

You are free to:

- **Share** — copy and redistribute the material in any medium or format

Under the following terms:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made (for example, formatting or excerpting).
- **NonCommercial** — You may not use the material for commercial purposes.
- **NoDerivatives** — If you remix, transform, translate, or build upon the material, you may not distribute the modified material.

**Commercial use:** For uses that may be commercial (including paid courses, kits, or redistribution with products), please contact Iron Sheep Productions, LLC and Parallax Inc. (info@ironsheep.biz) for separate permission.

To view the full license, visit: https://creativecommons.org/licenses/by-nc-nd/4.0/

### Trademarks

Parallax, Propeller, Spin, and the Parallax logo are trademarks of Parallax Inc.

### Acknowledgments

**Parallax Inc.** and **Chip Gracey** for the Propeller 2 and its DEBUG display system. The reverse-engineered per-window theory-of-operations references that ground this manual were verified against the PNut v55 implementation.

```{=latex}
\clearpage
```
