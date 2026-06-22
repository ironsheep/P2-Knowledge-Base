# A/V Breakout Add-on Board (#64006H)

**Part:** #64006H · **Series:** P2 Eval Add-on Boards (#64006) · **Source:** Product Guide v2.0 (1/12/2021)
**Cross-edition:** present in the 2020 #64006-ES set edition (largest module).

**Images:** `../assets/images-p2-eval-add-on-boards-2026-06-22/img-012.png` (board photo), `img-013.png` (mic-socket wiring), `img-014.png` (headphone-socket wiring), `img-015.png` (**PCB dimensions + pad layout**, 3.2×1.3 in). See `image-catalog.md`.

## Function
Combined audio + video breakout:
- Amplified Audio Out (80 mW) / headphone socket (3.5 mm stereo jack)
- Audio Input / microphone socket (3.5 mm mono jack)
- Audio-to-RCA 4-band
- Component Video-to-RCA 4-band (Composite Sync, RGBS)
- Digital component video (RCA socket)
- Composite Video (RCA socket)
- VGA (15-pin VGA socket)

Some features share I/O pins and sockets. A **dip switch** selects whether the 4× RCA sockets are in
**Audio** or **Video** mode.

## Pin map (I/O 0–7) — function depends on dip-switch setting
| I/O | Common (any setting) | Dip = VIDEO | Dip = AUDIO |
|-----|----------------------|-------------|-------------|
| 0 | VGA 15-pin — HSync | RCA Socket 0 (H – HSync) | RCA Socket 0 via 22 µF cap |
| 1 | VGA 15-pin — Blue | RCA Socket 1 (B – Blue) | RCA Socket 1 via 22 µF cap |
| 2 | VGA 15-pin — Green | RCA Socket 2 (G – Green) | RCA Socket 2 via 22 µF cap |
| 3 | VGA 15-pin — Red | RCA Socket 3 (R – Red) | RCA Socket 3 via 22 µF cap |
| 4 | VGA 15-pin — VSync | — | — |
| 5 | Microphone socket via 1 µF cap | — | — |
| 6 | Output to Audio amp (Left) | — | — |
| 7 | Output to Audio amp (Right) | — | — |

## Notes
- Microphone socket wiring: **Tip = signal, Sleeve = ground**.
- Headphone (audio out) socket wiring: **Tip = left, Ring = right, Sleeve = ground**.
- **Tip:** always use the P2-EVAL **3.3 V LDO** power selection when working with audio.
- Both audio jacks accept 3.5 mm jack plugs.
