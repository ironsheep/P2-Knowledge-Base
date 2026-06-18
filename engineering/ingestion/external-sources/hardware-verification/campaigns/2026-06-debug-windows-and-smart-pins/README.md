# Campaign — DEBUG windows & smart pins (2026-06)

**Scope.** Re-audit of the DEBUG display-window YAMLs + the smart-pin YAMLs and the
Titus↔IOSP cross-audit, settled by building tests, running on real P2 silicon, and
analyzing the captures. Drove corrections F-135…F-139 and the IOSP RA-* verdicts.

**Tooling.** `pnut-ts` v1.55.0 (compile, **`-d` mandatory** for DEBUG programs).
Run on a real P2 (Eval/Edge, `_clkfreq = 200 MHz` unless noted) via PNut-Term-TS; Stephen
flashed each `.bin` and returned the DEBUG log. (GUI/hardware runs are external — the
container only compiles + views returned images.)

**Rig.** Wiring-free where possible (own IN flag, or internal relative-pin routing
`P_PLUS1_A`/`P_MINUS1_A`). Two tests use a **real jumper loopback**: `P0→P2` and `P1→P3`
(test3/test4), and `P0→P2` (test51b). Each rig test has a Phase-0 bidirectional check that
HALTs on a bad jumper so a wiring fault can't be misread as a result.

**Evidence kept.** The `.spin2` stimulus programs are here under `tests/`. `.bin` files are
regenerable (`pnut-ts -d`) and not tracked. Raw `usb-traffic*.log` captures (28–82 MB) are
not tracked; the salient DEBUG output is quoted below. Durable facts → the
[ledger](../../P2-EMPIRICAL-FINDINGS.md).

## DEBUG-window tests

| Test | Question | Verdict | Ledger |
|------|----------|---------|--------|
| `test1-term-string-quoting` | single vs double quotes; formatted value in named TERM | single required; value→raw byte | EF-001, EF-002 |
| `test2-createline-vs-config` | does a channel-def on the create line break creation? | YES for SCOPE; LOGIC/SCOPE_XY OK | EF-003 |
| `test2b-fft-createline` | FFT create-line label + 2-window render | FFT not rendering (→ pursued in 2c/2d) | EF-004 |
| `test2c-fft-baseline` | manual's verbatim FFT snippet (no channel) | **blank on Term-TS AND real PNut** | EF-004 |
| `test2d-fft-with-channel` | snippet + one channel-decl + phase accumulator | **single clean peak** | EF-004 |
| `test3-smartpin-00101-y0-continuous` | is %00101 Y=0 continuous or idle? | **IDLE** (YAML claim false) | EF-010 |
| `test4-init-order-compare` | WYPIN before vs after enable (%00101) | after-enable required | EF-011 |

## Smart-pin tests

| Test | Question | Verdict | Ledger |
|------|----------|---------|--------|
| `iosp-titus-verification-batch1` | RA-06 / RA-12 / RA-17 | all PASS | EF-012/013/014 |
| `test50-eventtiming-rdpin-restart` | does RDPIN ack auto-restart event timing? | CONFIRMED | EF-015 |
| `test51-asynctx-firstbyte-glitch` | first-byte glitch (internal loopback) | NOT-OBSERVED (inconclusive — see 51b) | EF-016 |
| `test51b-asynctx-firstbyte-glitch-wired` | first-byte glitch (REAL wire P0→P2) | **NOT-OBSERVED (strong)** | EF-016 |
| `test60-pulse-universal-order` | %00100 old vs universal order | PASS-REQUIRED | EF-011 |
| `test61-nco-universal-order` | %00110 old vs universal order | PASS-SAFE | EF-011 |
| `test62-asynctx-universal-order` | %11110 old vs universal order | PASS-REQUIRED | EF-011 |
| `test63-dacnoise-universal-order` | %00001 old vs universal order | PASS-SAFE | EF-011 |

## Key result excerpts (verbatim from the DEBUG logs)

```
batch1   RA-06 PASS: WRPIN #0 reset a RUNNING pin with NO DIR cycle.  running=200 after=0
batch1   RA-12 PASS: NCO Y=0 produces NO output (static).  Y=0 events=0  control(Y>0)=200
batch1   RA-17 PASS: DAC-noise X=0 sample period = 65_534 clocks (~65536 expected)
test50   RA-24: CONFIRMED  RDPIN acknowledge AUTO-RESTARTS the measurement (2nd arrived).
test51b  sent $A5/$01: settled=$A500_0000 immediate=$A569_4000(byte $A5) preclear=$A57F_DA56 immediate$01=$0169_5FF6(byte $01)
test51b  RA-19: NOT-OBSERVED  every cold first byte arrived clean on the real wire.
test60   pulse:   PASS-REQUIRED  universal order NEEDED (old produced nothing).  old=0 new=1
test61   NCO:     PASS-SAFE  both orders work; universal order is safe.  old=200 new=200
test62   asyncTX: PASS-REQUIRED  universal order NEEDED (old produced nothing).  old=0 new=1
test63   DACnoise:PASS-SAFE  both orders work; universal order is safe.  old=305 new=305
test2c   FFT baseline: NO WINDOW rendered (P2 emitted FFT-create x1 + Spectrum feed x46754)
test2d   FFT + channel decl: single clean peak rendered
```

(test1/test2/test3/test4 verdicts were read from the rendered windows + DEBUG text on
Stephen's screen; see the ledger entries for the per-window detail.)

## Not built (routed elsewhere)
- **RA-33** (scope `SCP_ADDR D[7:6]` group-size encoding) — a streamer/`SETSCP` feature,
  not a clean smart-pin observable → routed to Chip Gracie, not a test.
