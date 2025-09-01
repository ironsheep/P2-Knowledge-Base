; Bytecode Dispatch Table Structure
; Source: spin-interpreter-v51-complete-analysis.md
; Category: Bytecode Operations
; Description: Vector table for bytecode dispatch

; Vector table structure (lines 66-139)
bc_hubset    word    @hubset_     ; Implementation function pointer
bc_clkset    word    @clkset_     ; Each bytecode maps to PASM function
bc_cogspin   word    @cogspin_    ; Direct function call architecture