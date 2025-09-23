# Enriched YAML Analysis for PASM2 Instructions

## Analysis Date: 2025-09-22

## Summary

Based on the current heat map, we have identified instructions that need narrative enrichment and matched them against available enriched YAMLs in `/engineering/operations/backups/pasm2-instruction-backups/`.

## Instructions Needing Enrichment (Score < 60)

### Critical Priority - Poor Score (20-39)
| Instruction | Heat Map Score | Enriched YAML Available |
|-------------|----------------|------------------------|
| PUSHA | 🟧 35 | ✅ YES - pusha.yaml |
| PUSHB | 🟧 35 | ✅ YES - pushb.yaml |

### High Priority - Fair Score (40-59) 
Instructions with enriched YAMLs available:

| Instruction | Heat Map Score | Enriched YAML Available |
|-------------|----------------|------------------------|
| POPB | 🟨 40 | ✅ YES - popb.yaml |
| POPA | 🟨 40 | ✅ YES - popa.yaml |
| NIXINT1 | 🟨 40 | ✅ YES - nixint1.yaml |
| NIXINT2 | 🟨 40 | ✅ YES - nixint2.yaml |
| NIXINT3 | 🟨 40 | ✅ YES - nixint3.yaml |
| CRCNIB | 🟨 40 | ✅ YES - crcnib.yaml |
| CRCBIT | 🟨 40 | ✅ YES - crcbit.yaml |
| SETCY | 🟨 40 | ✅ YES - setcy.yaml |
| XSTOP | 🟨 50 | ✅ YES - xstop.yaml |
| SETDACS | 🟨 40 | ✅ YES - setdacs.yaml |
| WRLUT | 🟨 50 | ✅ YES - wrlut.yaml |
| RGBEXP | 🟨 40 | ✅ YES - rgbexp.yaml |
| TRGINT1 | 🟨 40 | ✅ YES - trgint1.yaml |
| TRGINT2 | 🟨 40 | ✅ YES - trgint2.yaml |
| TRGINT3 | 🟨 40 | ✅ YES - trgint3.yaml |
| MULPIX | 🟨 40 | ✅ YES - mulpix.yaml |
| SETINT1 | 🟨 40 | ✅ YES - setint1.yaml |
| SETINT2 | 🟨 40 | ✅ YES - setint2.yaml |
| SETINT3 | 🟨 40 | ✅ YES - setint3.yaml |
| SETPIX | 🟨 40 | ✅ YES - setpix.yaml |
| SETCFRQ | 🟨 40 | ✅ YES - setcfrq.yaml |
| SETSE1 | 🟨 40 | ✅ YES - setse1.yaml |
| SETSE2 | 🟨 40 | ✅ YES - setse2.yaml |
| SETSE3 | 🟨 40 | ✅ YES - setse3.yaml |
| SETSE4 | 🟨 40 | ✅ YES - setse4.yaml |
| WRC | 🟨 40 | ✅ YES - wrc.yaml |
| WRBYTE | 🟨 40 | ✅ YES - wrbyte.yaml |
| WRZ | 🟨 40 | ✅ YES - wrz.yaml |
| SETPIV | 🟨 40 | ✅ YES - setpiv.yaml |
| SETCQ | 🟨 40 | ✅ YES - setcq.yaml |
| SETCI | 🟨 40 | ✅ YES - setci.yaml |
| SETCMOD | 🟨 40 | ✅ YES - setcmod.yaml |
| SETXFRQ | 🟨 40 | ✅ YES - setxfrq.yaml |
| RGBSQZ | 🟨 40 | ✅ YES - rgbsqz.yaml |
| LOC | 🟨 50 | ✅ YES - loc.yaml |
| BLNPIX | 🟨 40 | ✅ YES - blnpix.yaml |
| MIXPIX | 🟨 40 | ✅ YES - mixpix.yaml |
| RQPIN | 🟨 40 | ✅ YES - rqpin.yaml |
| GETCT | 🟨 50 | ✅ YES - getct.yaml |
| JINT | 🟨 50 | ✅ YES - jint.yaml |
| TJF | 🟨 50 | ✅ YES - tjf.yaml |
| TJS | 🟨 50 | ✅ YES - tjs.yaml |
| REP | 🟨 50 | ✅ YES - rep.yaml |
| JPAT | 🟨 50 | ✅ YES - jpat.yaml |
| WFBYTE | 🟨 50 | ✅ YES - wfbyte.yaml |
| WRLONG | 🟨 50 | ✅ YES - wrlong.yaml |
| JXRO | 🟨 50 | ✅ YES - jxro.yaml |
| WRWORD | 🟨 50 | ✅ YES - wrword.yaml |
| WFWORD | 🟨 50 | ✅ YES - wfword.yaml |
| HUBSET | 🟨 50 | ✅ YES - hubset.yaml |
| WFLONG | 🟨 50 | ✅ YES - wflong.yaml |
| LOCKRET | 🟨 50 | ✅ YES - lockret.yaml |
| MERGEW | 🟨 50 | ✅ YES - mergew.yaml |
| GETPTR | 🟨 50 | ✅ YES - getptr.yaml |
| MERGEB | 🟨 50 | ✅ YES - mergeb.yaml |
| MOVBYTS | 🟨 50 | ✅ YES - movbyts.yaml |
| XCONT | 🟨 50 | ✅ YES - xcont.yaml |
| TESTB | 🟨 50 | ✅ YES - testb.yaml |
| TJZ | 🟨 50 | ✅ YES - tjz.yaml |
| XZERO | 🟨 50 | ✅ YES - xzero.yaml |
| SETSCP | 🟨 50 | ✅ YES - setscp.yaml |
| JXFI | 🟨 50 | ✅ YES - jxfi.yaml |
| RET | 🟨 50 | ✅ YES - ret.yaml |
| GETSCP | 🟨 50 | ✅ YES - getscp.yaml |
| XORO32 | 🟨 50 | ✅ YES - xoro32.yaml |
| GETRND | 🟨 50 | ✅ YES - getrnd.yaml |
| SPLITW | 🟨 50 | ✅ YES - splitw.yaml |
| SPLITB | 🟨 50 | ✅ YES - splitb.yaml |
| JMP | 🟨 50 | ✅ YES - jmp.yaml |
| SUMZ | 🟨 50 | ✅ YES - sumz.yaml |
| RDBYTE | 🟨 50 | ✅ YES - rdbyte.yaml |
| SUMC | 🟨 50 | ✅ YES - sumc.yaml |
| RFVAR | 🟨 50 | ✅ YES - rfvar.yaml |
| EXECF | 🟨 50 | ✅ YES - execf.yaml |
| RFVARS | 🟨 50 | ✅ YES - rfvars.yaml |
| RDPIN | 🟨 50 | ✅ YES - rdpin.yaml |
| WRNC | 🟨 50 | ✅ YES - wrnc.yaml |
| RETB | 🟨 50 | ✅ YES - retb.yaml |
| MUXC | 🟨 50 | ✅ YES - muxc.yaml |
| RFWORD | 🟨 50 | ✅ YES - rfword.yaml |
| RFLONG | 🟨 50 | ✅ YES - rflong.yaml |
| RETA | 🟨 50 | ✅ YES - reta.yaml |
| GETQX | 🟨 50 | ✅ YES - getqx.yaml |
| RFBYTE | 🟨 50 | ✅ YES - rfbyte.yaml |
| GETQY | 🟨 50 | ✅ YES - getqy.yaml |
| RDLUT | 🟨 50 | ✅ YES - rdlut.yaml |
| LOCKNEW | 🟨 50 | ✅ YES - locknew.yaml |
| JATN | 🟨 50 | ✅ YES - jatn.yaml |

### Fair Score Instructions WITHOUT Enriched YAMLs
These instructions need YAMLs created from scratch:

| Instruction | Heat Map Score | Notes |
|-------------|----------------|-------|
| WMLONG | 🟨 50 | Missing enriched YAML |
| SETQ | 🟨 50 | Missing enriched YAML |
| TJNZ | 🟨 50 | Missing enriched YAML |
| JNXRO | 🟨 50 | Missing enriched YAML |
| SKIP | 🟨 50 | Missing enriched YAML |
| JNINT | 🟨 50 | Missing enriched YAML |
| WRFAST | 🟨 50 | Missing enriched YAML |
| JNPAT | 🟨 50 | Missing enriched YAML |
| SETPAT | 🟨 50 | Missing enriched YAML |
| NOP | 🟨 50 | Missing enriched YAML |
| WXPIN | 🟨 50 | Missing enriched YAML |
| JNATN | 🟨 50 | Missing enriched YAML |
| JMPREL | 🟨 50 | Missing enriched YAML |
| FBLOCK | 🟨 50 | Missing enriched YAML |
| SETLUTS | 🟨 50 | Missing enriched YAML |
| SEUSSR | 🟨 50 | Missing enriched YAML |
| SEUSSF | 🟨 50 | Missing enriched YAML |
| SKIPF | 🟨 50 | Missing enriched YAML |
| JNXFI | 🟨 50 | Missing enriched YAML |
| ASMCLK | 🟨 50 | Missing enriched YAML |
| WRNZ | 🟨 50 | Missing enriched YAML |
| MUXNC | 🟨 50 | Missing enriched YAML |
| DEBUG | 🟨 50 | Missing enriched YAML |

## Good Score Instructions WITH Enriched YAMLs (Not Needed)
These have good scores (60+) and don't need the enriched versions:

| Instruction | Heat Map Score | Enriched YAML Available | Status |
|-------------|----------------|------------------------|--------|
| XINIT | 🟦 60 | ❌ NO | Already good |
| RESI0-3 | 🟦 60 | ✅ YES - resi[0-3].yaml | Not needed |
| RETI0-3 | 🟦 60 | ✅ YES - reti[0-3].yaml | Not needed |
| RDWORD | 🟦 60 | ✅ YES - rdword.yaml | Not needed |
| RDLONG | 🟦 60 | ✅ YES - rdlong.yaml | Not needed |
| AND | 🟦 60 | ✅ YES - and.yaml | Not needed |
| BITC | 🟦 60 | ✅ YES - bitc.yaml | Not needed |
| BITH | 🟦 60 | ✅ YES - bith.yaml | Not needed |
| BITZ | 🟦 60 | ✅ YES - bitz.yaml | Not needed |
| OUTC | 🟦 60 | ✅ YES - outc.yaml | Not needed |
| OUTH | 🟦 60 | ✅ YES - outh.yaml | Not needed |
| OUTZ | 🟦 60 | ✅ YES - outz.yaml | Not needed |
| DIRC | 🟦 60 | ✅ YES - dirc.yaml | Not needed |
| DIRH | 🟦 60 | ✅ YES - dirh.yaml | Not needed |
| DIRZ | 🟦 60 | ✅ YES - dirz.yaml | Not needed |
| DRVC | 🟦 60 | ✅ YES - drvc.yaml | Not needed |
| DRVH | 🟦 60 | ✅ YES - drvh.yaml | Not needed |
| DRVZ | 🟦 60 | ✅ YES - drvz.yaml | Not needed |
| MODC | 🟦 60 | ✅ YES - modc.yaml | Not needed |
| MODZ | 🟦 60 | ✅ YES - modz.yaml | Not needed |
| MUXZ | 🟦 60 | ✅ YES - muxz.yaml | Not needed |
| NOT | 🟦 60 | ✅ YES - not.yaml | Not needed |
| REV | 🟦 60 | ✅ YES - rev.yaml | Not needed |
| DJF | 🟦 60 | ✅ YES - djf.yaml | Not needed |
| DJZ | 🟦 60 | ✅ YES - djz.yaml | Not needed |
| IJZ | 🟦 60 | ✅ YES - ijz.yaml | Not needed |
| FLTC | 🟦 60 | ✅ YES - fltc.yaml | Not needed |
| FLTH | 🟦 60 | ✅ YES - flth.yaml | Not needed |
| FLTZ | 🟦 60 | ✅ YES - fltz.yaml | Not needed |
| CALLA | 🟦 60 | ✅ YES - calla.yaml | Not needed |
| CALLPA | 🟦 60 | ✅ YES - callpa.yaml | Not needed |
| JFBW | 🟦 70 | ✅ YES - jfbw.yaml | Not needed |
| JXMT | 🟦 70 | ✅ YES - jxmt.yaml | Not needed |
| JXRL | 🟦 70 | ✅ YES - jxrl.yaml | Not needed |
| JQMT | 🟦 70 | ✅ YES - jqmt.yaml | Not needed |
| POLLCT1-3 | 🟩 80 | ✅ YES - pollct[1-3].yaml | Not needed |
| POLLSE1-4 | 🟦 70 | ✅ YES - pollse[1-4].yaml | Not needed |
| POLLXFI | 🟦 70 | ✅ YES - pollxfi.yaml | Not needed |
| POLLXRL | 🟦 70 | ✅ YES - pollxrl.yaml | Not needed |
| JCT1-3 | 🟩 80 | ✅ YES - jct[1-3].yaml | Not needed |
| JNCT1-3 | 🟩 80 | ✅ YES - jnct[1-3].yaml | Not needed |
| JSE1-4 | 🟩 80 | ✅ YES - jse[1-4].yaml | Not needed |
| JNSE1-4 | 🟩 80 | ✅ YES - jnse[1-4].yaml | Not needed |
| WAITCT1-3 | 🟩 80 | ✅ YES - waitct[1-3].yaml | Not needed |
| WAITSE1-4 | 🟩 80 | ✅ YES - waitse[1-4].yaml | Not needed |

## Summary Statistics

- **Total weak instructions (score < 60)**: 114
- **Enriched YAMLs available for weak instructions**: 91
- **Weak instructions missing enriched YAMLs**: 23
- **Enriched YAMLs not needed (good scores)**: 56

## Recommendations

### Immediate Actions
1. **Apply the 91 enriched YAMLs** for weak instructions
2. **Focus on the 2 POOR instructions** (PUSHA, PUSHB) first
3. **Create new YAMLs** for the 23 missing instructions

### Priority Order
1. **Critical**: PUSHA, PUSHB (score 35)
2. **High**: All score 40 instructions with YAMLs available
3. **Medium**: All score 50 instructions with YAMLs available
4. **Low**: Create YAMLs for missing instructions

## Files to Use Today

Based on the heat map, here are the enriched YAMLs we should use:

### Must Use (91 files)
All files in `/engineering/operations/backups/pasm2-instruction-backups/` EXCEPT:
- resi[0-3].yaml
- reti[0-3].yaml
- rdword.yaml, rdlong.yaml
- and.yaml
- bitc.yaml, bith.yaml, bitz.yaml
- outc.yaml, outh.yaml, outz.yaml
- dirc.yaml, dirh.yaml, dirz.yaml
- drvc.yaml, drvh.yaml, drvz.yaml
- modc.yaml, modz.yaml, muxz.yaml
- not.yaml, rev.yaml
- djf.yaml, djz.yaml, ijz.yaml
- fltc.yaml, flth.yaml, fltz.yaml
- calla.yaml, callpa.yaml
- jfbw.yaml, jxmt.yaml, jxrl.yaml, jqmt.yaml
- pollct[1-3].yaml, pollse[1-4].yaml
- pollxfi.yaml, pollxrl.yaml
- jct[1-3].yaml, jnct[1-3].yaml
- jse[1-4].yaml, jnse[1-4].yaml
- waitct[1-3].yaml, waitse[1-4].yaml