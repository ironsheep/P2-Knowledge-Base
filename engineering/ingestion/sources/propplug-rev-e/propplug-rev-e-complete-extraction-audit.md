# Prop Plug Rev E (#32201) — Complete Extraction Audit (Audit of Record)

**Document:** `32201-PropPlugRev-Guide-RevE.pdf`
**Document version:** v3.0 (2/03/2021) — hardware Rev E
**Pages:** 4
**Trust tier:** 🏆 / GREEN — official Parallax hardware product guide
**Re-extraction date:** 2026-06-29 (supersedes the 2025-08-29 PDF-era capture — now in `archive/`)
**Ingestion mode:** re-extraction (§0.6) — modern tooling replacing the lossy prior capture
**Curated reference:** `complete-propplug-rev-e-reference.md`

---

## Passes completed (PDF-only ladder)

| Pass | Status | Tooling | Notes |
|------|--------|---------|-------|
| 1 Content | ✅ | `pdftotext -layout` (clean text layer) + `pdf2md` (docling) | 4 pp.; all body text + Specifications + Reset Option + driver notes + revision history captured. Text layer clean (no OCR/corruption). |
| 2 Code | ✅ (n/a) | — | **No code in document** (hardware adapter guide). 0 examples to extract/validate. |
| 3 Images | ✅ | `pdftoppm -r 200` + visual read | 2 fact-bearing figures rendered + cataloged (`assets/images-propplug-rev-e-2026-06-29/image-catalog.md`). The pinout is figure-only (page 3); read directly. |
| 4 Post-processing | ✅ (n/a) | — | No timing/relationship matrices warranted for a single programming adapter. |
| 5 Validation | ✅ | section-by-section | All page sections accounted for (see below). |
| 6 Cross-source Q&A | ✅ | corroboration | See below — 0 conflicts; P2-programming role corroborated by #64010 / #64007 guides. |
| 7 Registration | ✅ | dashboards | README + AUTHORITATIVE-SOURCES + DOCUMENT-LINEAGE updated; this audit promoted to audit-of-record. |

## Section completeness (pass 5)

- ✅ Overview / Rev E improvements (pin labelling both sides, 2-sided LEDs, buffered I/O, customer reset option)
- ✅ Specifications (power, current, USB 2.0 FS, UART 3.3 V CMOS / TTL, 5.5 V-tolerant RX, 300 baud–3 Mbps, ~20 µs reset pulse, USB micro-B + 4-pin SIP, temp, PCB dims)
- ✅ 4-pin header pinout (RX/TX/RES/VSS) + Interface-to-Propeller wiring (P30/P31/RESn/GND) — from page-3 figure
- ✅ Customer Reset Option (DTR default / RTS / none)
- ✅ PC Drivers Installation (FTDI, parallax.com/usbdrivers, macOS 10.15+ built-in)
- ✅ Related parts (#805-00016 cable required; #32200 Prop Clip; Rev D and earlier)
- ✅ Resources/Downloads + Revision History

**Completeness: 100%** of the 4-page guide. No gates open.

## Key facts (for the board-suite YAML consumer)

- **Part #32201**, Prop Plug Rev E; **FTDI FT231X** USB bridge.
- USB-powered (5 VDC), ~15 mA typ.; USB **micro-B** connector + **4-pin 0.1″ female SIP socket**.
- Serial: **300 baud – 3 Mbps**, true 3.3 V CMOS out / TTL in, buffered RX tolerant to **5.5 V** (works with 3.3 V and 5 V targets).
- **DTR-toggle reset pulse** ~20 µs (15–25 µs); Rev E option pad selects **DTR (default) / RTS / none**.
- 4-pin header: **RX ← Propeller TX (P30); TX → Propeller RX (P31); RES → RESn; VSS → GND**.
- Requires **#805-00016** USB A→micro-B cable (not included). Predecessor: **Prop Clip #32200**.
- PCB 23.5 × 12.1 mm; ~33 mm long with connectors. Temp −40 to +85 °C.

## Cross-source Q&A (pass 6)

- **Answered prior holes:** none open against this source.
- **New questions raised:** none. The guide is complete for its scope (it defers schematic to the product page, which is expected).
- **Reviewer notes:** none embedded (PDF, no comments).
- **Conflicts:** **0.** The guide's P1-illustrated figure does not conflict with P2 usage; P2-programming role is **corroborated** (not contradicted) by the #64010 Universal Motor Driver guide and #64007 WX-Adapter guide, which both name "Prop Plug (#32201)" as the typical P2 Edge programmer.
- **Trust:** HIGH — single authoritative Parallax source, internally consistent, figure-confirmed.

## Obsolescence handling (§0.6)

- **Mode:** re-extraction. Prior 2025-08-29 PDF-era artifacts (`*-complete-extraction-audit.md` + `32201-…-RevE.txt`) **archived** to `archive/` (gitignored; git history is the deeper record) with a pointer README. No downstream path references to the specific stale files (only the source-folder name is referenced by dashboards, which is unchanged).
- The bloated docling intermediate (`32201-…-RevE.md`, 1.7 MB base64) was discarded; kept artifacts = raw `propplug-rev-e-text.txt` + curated `complete-propplug-rev-e-reference.md` + page renders.

## Next step

Feeds the YAML head: author `deliverables/ai/P2/hardware/` entry (board-suite findability F-116)
as the 7th board of the addon-wave-2026-06 YAML wave.
