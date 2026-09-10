# PNut-Term-TS User Guide Changelog

## v1.0.0 (2026-09-10): Initial public release

**Initial release.** The operating guide for **PNut-Term-TS** — the downloader, serial
terminal, and debug display for the Propeller 2, in one program that runs the same way on
every platform. It replaces Parallax Serial Terminal, hosts the `debug()` display windows
and the single-step debugger, and does all three without a specific operating system.

The guide forks by intent after a shared orientation: one opening places the tool in your
workflow, then the reading splits into the GUI path and the headless command-line path so
you follow only the half you work in. It states the tool's compiler independence outright
— downloading is the P2's own boot protocol, so a binary from any toolchain downloads and
runs — and is plain about the one place toolchains differ: PNut and `pnut-ts` images are
auto-detected and carry their own serial rate, and a build from anything else needs `-b`.

**The opening teaches the loop you can actually see.** Chapter 1 places the tool in the
workflow as *you* operate it: you compile, PNut-Term-TS downloads and runs, and what the
P2 sends comes back to your terminal and debug windows, with a log written alongside as a
record. The automated form of that loop — where an agent stands in for the person, P2KB
MCP supplies what it knows about the P2, and the log becomes the only return path because
there is no longer a screen — is taught in Chapter 15, once the headless run, its exit
codes, and its log are in hand. The two chapters carry matching diagrams of one spine, and
the difference between them is the lesson: **who is watching decides what the return path
is.**

**Three subjects get more room than a tour would give them**, because each one costs a
reader real time when it is guessed at:

- **The exit codes are a contract, not a courtesy.** Chapter 13 states what each one
  asserts — `0` that the captured log is complete, `125` that it may not be, `4` that a
  `debug()` directive named a display the tool cannot address — because the automated run
  in Chapter 15 branches on them.
- **The Debug Logger is a window onto the log, not the log.** Closing it stops the drawing
  and nothing else; the file is ended by the run, never by a window. Under a fast stream
  the display sheds lines and says so on screen, and the file still holds every one.
- **A display's name is its only address on the wire**, so the guide gives the rule
  outright: `trace` is illegal, `spin2` is fine, names are case-insensitive and stop at 30
  characters. PNut discards an unusable name silently; this tool reports it and stops.

Current as of PNut-Term-TS v1.0.7.

Ships with four TikZ diagrams and six screenshots. Released alongside the *P2 Single-Step
Debugger Manual*, which covers driving the debugger itself.
