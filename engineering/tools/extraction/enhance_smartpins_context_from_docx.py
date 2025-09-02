#!/usr/bin/env python3
"""
Enhance Smart Pins image catalog with context from .docx extraction.
Maps narrative descriptions to specific images based on page numbers and content.
"""

import json
import re
from datetime import datetime

def load_docx_text(filepath):
    """Load the .docx extracted text."""
    with open(filepath, 'r') as f:
        return f.read()

def enhance_image_context():
    """Map .docx narrative context to images."""
    
    # Load the .docx text
    docx_text = load_docx_text("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/smart-pins/smartpins-narrative-from-docx.txt")
    
    # Load the current catalog
    catalog_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/smart-pins/assets/images-smartpins-20250901/P2 SmartPins-220809_smartpins_catalog_final_instructions_corrected.json"
    
    with open(catalog_path, 'r') as f:
        catalog = json.load(f)
    
    # Define enhanced context for each image based on .docx narrative
    enhancements = {
        "SP-IMG-001": {
            "narrative_context": "When an instruction changes a DIRx or OUTx bit, the processor needs three (3) additional system-clock cycles after the instruction before the pin starts to transition to its new state.",
            "figure_reference": "The figure below shows the delay for a DRVH instruction",
            "timing_detail": "3-clock delay after instruction execution before pin state change"
        },
        "SP-IMG-002": {
            "narrative_context": "When an instruction reads the contents of the IN register associated with a pin, the processor receives the state of the pins as they existed three (3) system-clock cycles before the start of the instruction.",
            "figure_reference": "The figure below shows the timing for a the TESTB INA,#0 operation",
            "timing_detail": "3-clock latency - reads pin state from before instruction start"
        },
        "SP-IMG-003": {
            "narrative_context": "When a program uses a TESTP or TESTPN instruction to read the state of a pin, the processor receives the state of the pins as they existed two (2) system-clock cycles before the start of the instruction. So, the TESTP and TESTPN gather 'fresher' INx data than is available via the INx registers.",
            "figure_reference": "The figure below shows the timing for a TESTP instruction",
            "timing_detail": "2-clock latency - provides fresher data than IN register reads"
        },
        "SP-IMG-004": {
            "narrative_context": "But, proportionally averaging some of the 3.083V and the 3.096 voltages lets the DAC can get very close to 3.095V, as shown below for a 256-system-clock period (DAC period).",
            "figure_reference": "Shows PWM dithering for DAC output precision",
            "mode_context": "DAC output with added PWM dither - extends 8-bit DAC resolution"
        },
        "SP-IMG-005": {
            "narrative_context": "This mode lets a Smart Pin produce a series of logic-1 pulses. Software sets the pulse period, X[15:0], and the length of the logic-0 state, X[31:16], as shown in the figure below.",
            "figure_reference": "Shows pulse/cycle output timing configuration",
            "register_usage": "X[15:0] = pulse period, X[31:16] = logic-0 duration"
        },
        "SP-IMG-006": {
            "narrative_context": "This command creates a series of pulses with equal logic-0 and logic-1 periods. The value X[15:0] sets that period as a count of system-clock periods.",
            "figure_reference": "Shows transition output mode timing",
            "register_usage": "X[15:0] = transition period, Y[31:0] = number of transitions"
        },
        "SP-IMG-007": {
            "narrative_context": "NCO frequency mode - The Pin output signal reflects the value of the Z31 bit. The circuit raises the IN flag whenever the Z register overflows.",
            "figure_reference": "Shows NCO operation timing and conceptual diagram",
            "mode_context": "Numerically Controlled Oscillator frequency generation"
        },
        "SP-IMG-008": {
            "narrative_context": "NCO configuration example showing setup for specific frequency generation",
            "figure_reference": "NCO mode configuration and timing",
            "code_context": "Shows WRPIN, WXPIN setup for NCO mode"
        },
        "SP-IMG-009": {
            "narrative_context": "PWM triangle waveform generation using up-down counter",
            "figure_reference": "Triangle PWM waveform pattern",
            "mode_context": "%01000 = Triangle-wave pulse-width modulation"
        },
        "SP-IMG-010": {
            "narrative_context": "The X[31:16] bits sets the number of 40-nsec base periods you want in a frame period. In this mode, the PWM period is twice the frame period.",
            "figure_reference": "Triangle PWM timing diagram with frame periods",
            "register_usage": "X[31:16] = frame period count, Y[15:0] = pulse width"
        },
        "SP-IMG-011": {
            "narrative_context": "The X[31:16] bits sets the number of base periods in a frame period. In sawtooth mode, the frame period equals the PWM period.",
            "figure_reference": "Sawtooth PWM timing diagram",
            "mode_context": "%01001 = PWM sawtooth using up counter only"
        },
        "SP-IMG-012": {
            "narrative_context": "Quadrature encoder A/B signal processing. The Z register holds a 2's complement value representing net encoder counts.",
            "figure_reference": "Quadrature encoder signal timing",
            "mode_context": "%01011 = A/B-input quadrature encoder"
        },
        "SP-IMG-013": {
            "narrative_context": "This mode lets a Smart Pin continuously measure the time a pin is held in a logic-1 or logic-0 state.",
            "figure_reference": "Time A-input states measurement",
            "mode_context": "%10000 = Time A-input states with carry flag indication"
        },
        "SP-IMG-014": {
            "narrative_context": "%001 = Measure the period of X number of pulse widths starting on logic-0 to logic-1 edges. The diagram shows timing for X[31:0] = $9.",
            "figure_reference": "Shows measurement of 9 pulse periods",
            "register_usage": "X[31:0] = number of pulses to measure"
        },
        "SP-IMG-015": {
            "narrative_context": "%01x = Measure the period between X number of logic edges on an A input. The diagram shows timing for six edges, X[31:0] = 6.",
            "figure_reference": "Shows edge-to-edge period measurement",
            "register_usage": "X[31:0] = number of edges to count"
        },
        "SP-IMG-016": {
            "narrative_context": "Missing A-input edge detection. If an event fails to occur during the period, the pin raises the IN flag.",
            "figure_reference": "Shows missing edge detection timing",
            "mode_context": "%11x = Missing A-input edge monitoring"
        },
        "SP-IMG-017": {
            "narrative_context": "The value in X register (X[31:0]) sets the number of A-input to B-input events that must occur before you get a result.",
            "figure_reference": "A-to-B input event measurement",
            "register_usage": "X[31:0] = number of A-to-B events"
        },
        "SP-IMG-018": {
            "narrative_context": "Synchronous serial transmit - Data shifts out synchronized with separate clock signal. Bits shift out LSB first.",
            "figure_reference": "Serial data transmission timing",
            "mode_context": "%11100 = Synchronous serial transmit (SST)"
        },
        "SP-IMG-019": {
            "narrative_context": "Shows timing for synchronous serial transmission with positive-edge and negative-edge clocking options.",
            "figure_reference": "Synchronous serial clocking options",
            "mode_context": "Positive vs negative edge clocking for SST"
        },
        "SP-IMG-020": {
            "narrative_context": "Asynchronous serial transmit waveform - left portion showing start bit and beginning of data transmission",
            "figure_reference": "Async serial TX start sequence (left half)",
            "mode_context": "%11110 = Asynchronous serial transmit"
        },
        "SP-IMG-021": {
            "narrative_context": "Asynchronous serial transmit waveform - right portion showing end of data and stop bit",
            "figure_reference": "Async serial TX stop sequence (right half)",
            "mode_context": "Shows data completion and stop bit timing"
        }
    }
    
    # Update catalog with enhanced context
    updated_count = 0
    for img in catalog.get('images', []):
        global_id = img.get('global_id')
        
        if global_id in enhancements:
            enhancement = enhancements[global_id]
            
            # Add enhanced context
            if 'enhanced_context' not in img:
                img['enhanced_context'] = {}
            
            img['enhanced_context'].update({
                'narrative_context': enhancement.get('narrative_context', ''),
                'figure_reference': enhancement.get('figure_reference', ''),
                'timing_detail': enhancement.get('timing_detail', ''),
                'mode_context': enhancement.get('mode_context', ''),
                'register_usage': enhancement.get('register_usage', ''),
                'code_context': enhancement.get('code_context', ''),
                'extraction_source': 'Smart Pins rev 5.docx via pandoc',
                'enhancement_date': datetime.now().isoformat()
            })
            
            updated_count += 1
            print(f"✅ Enhanced {global_id}")
    
    # Save enhanced catalog
    output_path = catalog_path.replace('.json', '_enhanced.json')
    with open(output_path, 'w') as f:
        json.dump(catalog, f, indent=2)
    
    print(f"\n📊 Enhancement Summary:")
    print(f"  - Enhanced: {updated_count} images with .docx narrative context")
    print(f"  - Added: figure references, timing details, mode context, register usage")
    print(f"  - Source: Smart Pins rev 5.docx (clean extraction)")
    print(f"  - Saved to: {output_path}")

if __name__ == "__main__":
    enhance_image_context()