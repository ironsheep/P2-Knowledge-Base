# PASM2 Instruction Narrative Enrichment

## Purpose
This directory contains PASM2 instruction YAMLs that need narrative enrichment for the Advanced PASM2 Manual. These are copies from the P2 Knowledge Base that will be enhanced with:
- Rich multi-paragraph descriptions
- Practical code examples
- Usage notes and best practices
- Related instruction references

## Structure
- `/pasm2-narratives/` - Instruction YAMLs for enrichment
- `/README.md` - This file
- `/enrichment-status.md` - Tracking document for progress

## Important Notes
- DO NOT modify `/engineering/knowledge-base/P2/` - that's released content
- Work only in this ingestion directory
- Once enriched, these will be integrated in a future release

## Instructions by Priority

### Critical Priority (Score 35) - Need Complete Narratives
- pusha.yaml - Push using PTRA
- pushb.yaml - Push using PTRB

### High Priority (Score 40) - Need Full Documentation
Stack Operations:
- popa.yaml - Pop using PTRA
- popb.yaml - Pop using PTRB

Interrupt Instructions:
- nixint1.yaml, nixint2.yaml, nixint3.yaml
- trgint1.yaml, trgint2.yaml, trgint3.yaml
- setint1.yaml, setint2.yaml, setint3.yaml

CRC Instructions:
- crcbit.yaml - CRC bit operation
- crcnib.yaml - CRC nibble operation

Color Space:
- setcy.yaml, setcfrq.yaml, setcq.yaml, setci.yaml, setcmod.yaml

Pixel Operations:
- mulpix.yaml, setpix.yaml, setpiv.yaml, blnpix.yaml
- mixpix.yaml, rgbexp.yaml, rgbsqz.yaml

Event Instructions:
- setse1.yaml, setse2.yaml, setse3.yaml, setse4.yaml

DAC/Streamer:
- setdacs.yaml - DAC setup
- setxfrq.yaml - Streamer frequency

Hub Write:
- wrc.yaml, wrbyte.yaml, wrz.yaml

### Medium Priority (Score 50) - Need Examples & Notes
(70+ instructions that have basic docs but need practical examples)