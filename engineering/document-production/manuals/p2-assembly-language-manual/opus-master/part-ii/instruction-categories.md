# Instruction Categories {#instruction-categories}

This chapter defines the instruction categories used throughout Part II. Each category groups instructions by their primary function. Click any category name in the instruction entries to return here.

## Branch {#branch}

Branch instructions control program flow by modifying the program counter. This category includes conditional and unconditional jumps, subroutine calls, and returns. Branch instructions interact with the hardware call stack and pointer registers (PTRA, PTRB).

## CORDIC Solver {#cordic-solver}

CORDIC (Coordinate Rotation Digital Computer) instructions provide hardware-accelerated mathematical operations including trigonometric functions, vector rotation, and polar/rectangular coordinate conversion. These instructions use the dedicated CORDIC coprocessor and typically require multiple clock cycles.

## Color Space Converter {#color-space-converter}

Color space converter instructions perform colorspace transformations used in video and graphics applications. They convert between different color representations such as RGB and YUV formats.

## Event {#event}

Event instructions monitor and respond to system events including counter triggers, smart pin signals, and inter-cog communication (attention signals). They provide polling and waiting mechanisms for synchronization.

## Hub Control {#hub-control}

Hub control instructions manage cog operations and hub-level system functions. This includes starting and stopping cogs, setting clock configuration, and controlling the lock system for inter-cog synchronization.

## Hub FIFO {#hub-fifo}

Hub FIFO instructions perform fast sequential access to hub memory through the dedicated FIFO buffer. They enable efficient streaming data transfers between hub memory and cog registers.

## Hub RAM {#hub-ram}

Hub RAM instructions transfer data between cog registers and the shared hub memory. They support byte, word, and long access with various addressing modes including pointer-based addressing.

## Interrupt {#interrupt}

Interrupt instructions control the cog's interrupt system including enabling/disabling interrupts, returning from interrupt handlers, and managing interrupt state.

## Lookup Table {#lookup-table}

Lookup table (LUT) instructions access the 512-long LUT memory that each cog has in addition to its main COG RAM. The LUT can be used for fast table lookups or as additional register storage.

## Math and Logic {#math-and-logic}

Math and logic instructions perform arithmetic operations (add, subtract, multiply), logical operations (AND, OR, XOR), comparisons, bit manipulation, shifts, and rotates. This is the largest instruction category.

## Miscellaneous {#miscellaneous}

Miscellaneous instructions provide utility functions that don't fit neatly into other categories, including debugging support, immediate value extension (AUGS/AUGD), and specialized operations.

## Pin {#pin}

Pin instructions directly control the P2's 64 I/O pins, setting their direction (input/output) and output level (high/low). These work with the basic I/O system separate from smart pin functionality.

## Pixel Mixer {#pixel-mixer}

Pixel mixer instructions perform hardware-accelerated pixel blending and color manipulation operations used in graphics applications. They support alpha blending, color addition, and format conversion.

## Register Indirection {#register-indirection}

Register indirection instructions modify subsequent instructions by altering their source, destination, or bit index fields. They enable dynamic register addressing and are essential for implementing arrays and pointers in assembly.

## Smart Pin {#smart-pin}

Smart pin instructions configure and communicate with the P2's 64 smart pins. Each smart pin contains an autonomous state machine that can perform complex I/O functions independent of cog processing.

## Streamer {#streamer-category}

Streamer instructions control the cog's dedicated DMA engine (streamer) that can autonomously transfer data between hub memory, LUT, and I/O pins. The streamer is essential for high-bandwidth applications like video output.

## System Control {#system-control}

System control instructions manage system-wide settings and operations including clock configuration and low-level hardware control.
