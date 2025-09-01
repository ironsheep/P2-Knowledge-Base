\begin{sidetrack}
\textbf{Why 512 Longs?}

The magic number 512 comes from addressing. With 9 bits, you can address 2\^{}9 = 512 locations. This fits perfectly in P2 instruction encoding. It's enough for surprisingly complex programs, but small enough that all 8 cogs get their own private RAM without breaking the bank on silicon area.
\end{sidetrack}