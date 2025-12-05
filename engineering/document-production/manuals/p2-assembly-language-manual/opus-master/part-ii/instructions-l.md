# Instructions: L

This section contains all PASM2 instructions beginning with the letter L.



::: instrheader
## LOC {#loc}
Load Address

[Hub Memory Access](#hub-memory-access) - Loads an address into a pointer register (PA, PB, PTRA, or PTRB).
:::

**LOC**  *PA/PB/PTRA/PTRB, #A*\
**LOC**  *PA/PB/PTRA/PTRB, #\A*

---

**Result:** Address is loaded into the specified pointer register.

- PA, PB, PTRA, or PTRB is the destination pointer register.
- A is a 20-bit address value.
- The optional backslash (\) prefix forces absolute addressing (R=0). Without it, relative addressing is used (R=1).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 11101WW | RAA | AAAAAAAAA | AAAAAAAAA | Per W | --- | --- | 2 |


**Related:** [PA](#pa), [PB](#pb), [PTRA](#ptra), [PTRB](#ptrb), [CALLD](#calld), [CALLPA](#callpa), [CALLPB](#callpb)

**Explanation:**

LOC loads an address into one of the four pointer registers: PA, PB, PTRA, or PTRB. These pointer registers are used by various memory operations and call instructions.

The instruction supports two addressing modes, controlled by the R bit in the encoding. By default, LOC uses relative addressing (R=1), where the address is calculated as PC + A. This allows position-independent code, as the address is computed relative to the current program counter. To force absolute addressing (R=0), prefix the address with a backslash (\), making the address equal to A directly.

The WW field in the encoding selects which pointer register to load: 00 for PA, 01 for PB, 10 for PTRA, and 11 for PTRB. The address field A is 20 bits wide, providing access to the full Hub memory space.

LOC is commonly used to set up pointer registers before memory operations, call sequences, or when establishing base addresses for data structures. The relative addressing mode is particularly useful for creating position-independent code blocks that can execute correctly regardless of where they are loaded in Hub memory.



::: instrheader
## LOCKNEW {#locknew}
Allocate New Lock

[COG Control and Locks](#cog-control-and-locks) - Requests an available lock from the hardware pool.
:::

**LOCKNEW**  *D*  **{WC}**

---

**Result:** D is written with an available lock number (0-15), or remains unchanged if no lock is available.

- D is a register where the allocated lock number is written.
- WC is an optional effect to update the C flag.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | C00 | DDDDDDDDD | 000000100 | D | 1 if no LOCK available | --- | 4...11 |


**Related:** [LOCKTRY](#locktry), [LOCKREL](#lockrel), [LOCKRET](#lockret)

**Explanation:**

LOCKNEW requests a lock from the P2's hardware lock pool. The P2 provides 16 hardware locks (numbered 0-15) for inter-COG synchronization and resource protection. LOCKNEW searches the lock pool for an available lock and, if one is found, returns its number in the D register.

If the WC effect is specified, the C flag is set (1) if no lock is available, or cleared (0) if a lock was successfully allocated. This allows the calling code to detect allocation failure and take appropriate action.

Once a lock is allocated with LOCKNEW, it remains assigned until explicitly returned to the pool with LOCKRET. The allocated lock can then be used with LOCKTRY to acquire exclusive access and LOCKREL to release it. This allocation-try-release-return pattern ensures proper resource management in multi-COG systems.

LOCKNEW is essential for dynamic lock allocation in systems where the number of required locks is not known at compile time, or where locks are allocated and deallocated as resources are created and destroyed. The instruction completes in 4 to 11 clock cycles depending on lock availability and contention.



::: instrheader
## LOCKREL {#lockrel}
Release Lock

[COG Control and Locks](#cog-control-and-locks) - Releases a lock for other COGs to acquire.
:::

**LOCKREL**  *{#}D*  **{WC}**

---

**Result:** The lock specified by D[3:0] is released for other COGs to acquire.

- D is a register or 4-bit literal (0-15) specifying the lock number to release.
- When D is a register and WC is specified, D is written with the previous owner's COG ID and the C flag indicates lock status.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | C0L | DDDDDDDDD | 000000111 | --- | --- | --- | 2...9, +2 if result |


**Related:** [LOCKTRY](#locktry), [LOCKNEW](#locknew), [LOCKRET](#lockret), [COGID](#cogid)

**Explanation:**

LOCKREL releases a lock that was previously acquired with LOCKTRY, making it available for other COGs to acquire. The lock to release is specified by the lower 4 bits of D (D[3:0]), allowing lock numbers 0 through 15.

When D is a register (not an immediate) and the WC effect is specified, LOCKREL performs an additional operation: it writes the COG ID of the previous lock owner into D and sets the C flag based on whether the lock was held. This diagnostic feature allows verification of lock ownership and debugging of synchronization issues.

LOCKREL is safe to call even if the lock was not held by the current COG. Releasing an unheld lock simply has no effect. This property simplifies error recovery code, as locks can be released without checking ownership first.

Proper lock management requires that every LOCKTRY that successfully acquires a lock is balanced with a corresponding LOCKREL. Failure to release locks leads to deadlocks and resource starvation. The instruction completes in 2 to 9 clock cycles, with an additional 2 cycles if the result is written back to D.



::: instrheader
## LOCKRET {#lockret}
Return Lock To Pool

[COG Control and Locks](#cog-control-and-locks) - Returns a lock to the pool for reallocation by LOCKNEW.
:::

**LOCKRET**  *{#}D*

---

**Result:** The lock specified by D[3:0] is returned to the pool and becomes available for LOCKNEW.

- D is a register or 4-bit literal (0-15) specifying the lock number to return.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000000101 | --- | --- | --- | 2...9 |


**Related:** [LOCKNEW](#locknew), [LOCKTRY](#locktry), [LOCKREL](#lockrel)

**Explanation:**

LOCKRET returns a lock to the hardware lock pool, making it available for future allocation by LOCKNEW. This instruction completes the lifecycle of a dynamically allocated lock: first allocated with LOCKNEW, then used with LOCKTRY and LOCKREL for synchronization, and finally returned with LOCKRET when no longer needed.

The lock to return is specified by the lower 4 bits of D (D[3:0]), allowing lock numbers 0 through 15. Unlike LOCKREL, which only releases ownership of a lock while keeping it allocated, LOCKRET deallocates the lock entirely, allowing LOCKNEW to assign it to a different purpose.

LOCKRET should only be called on locks that are not currently held by any COG. Before returning a lock, ensure it has been released with LOCKREL. Returning a lock that is still held can cause synchronization failures in other COGs that may be waiting for or using that lock.

The proper pattern for dynamic lock usage is: LOCKNEW to allocate, LOCKTRY/LOCKREL for each critical section, and LOCKRET when the lock is no longer needed for any purpose. This ensures efficient use of the limited pool of 16 hardware locks. The instruction completes in 2 to 9 clock cycles depending on Hub access contention.



::: instrheader
## LOCKTRY {#locktry}
Try To Acquire Lock

[COG Control and Locks](#cog-control-and-locks) - Attempts to acquire a lock using atomic test-and-set.
:::

**LOCKTRY**  *{#}D*  **{WC}**

---

**Result:** Attempts to acquire the lock specified by D[3:0]. The C flag indicates success.

- D is a register or 4-bit literal (0-15) specifying the lock number to acquire.
- WC is an optional effect to update the C flag.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | C0L | DDDDDDDDD | 000000110 | --- | 1 if got LOCK | --- | 2...9, +2 if result |


**Related:** [LOCKREL](#lockrel), [LOCKNEW](#locknew), [LOCKRET](#lockret), [COGID](#cogid)

**Explanation:**

LOCKTRY attempts to acquire a lock using an atomic test-and-set operation. The lock to acquire is specified by the lower 4 bits of D (D[3:0]), allowing lock numbers 0 through 15. The P2 provides 16 hardware locks for inter-COG synchronization and resource protection.

If the WC effect is specified, the C flag is set (1) if the lock was successfully acquired, or cleared (0) if the lock is already held by another COG. This non-blocking behavior allows the calling code to make immediate decisions: proceed with the protected operation if the lock was acquired, or take alternative action if it was not.

LOCKTRY implements the critical section entry point in the standard lock pattern: try to acquire the lock, and only proceed if successful. The lock must be released with LOCKREL when the critical section completes. This ensures mutual exclusion, preventing multiple COGs from simultaneously accessing shared resources.

The instruction is non-blocking and returns immediately regardless of lock availability. For spin-lock behavior (waiting until the lock is acquired), LOCKTRY must be called repeatedly in a loop. Lock 15 is traditionally reserved for debug monitor use. The instruction completes in 2 to 9 clock cycles, with an additional 2 cycles if a result is returned.



