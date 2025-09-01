#!/usr/bin/env python3
"""
Generate Smart Pin architecture diagrams using Graphviz
Author: Claude with guidance from Stephen (former Graphviz Debian packager!)
Purpose: Create both detailed and simplified views of P2 Smart Pin architecture

This version generates DOT files directly and uses the command-line dot tool
"""

import os
import subprocess
from pathlib import Path

def create_simple_dot():
    """
    Create simplified block diagram showing basic signal flow
    """
    return """digraph SmartPinSimple {
    rankdir=LR;
    compound=true;
    fontname="Arial";
    bgcolor="white";
    pad=0.5;
    
    label="P2 Smart Pin - Simplified Architecture";
    fontsize=16;
    labelloc=t;
    
    // Node defaults
    node [shape=box, style="filled,rounded", fontsize=11];
    
    // Physical pins cluster
    subgraph cluster_pins {
        label="Physical I/O";
        bgcolor="#fff4e6";
        pin_even [label="Even Pin\\n(0,2,4...62)", fillcolor="#8b7355", fontcolor="white"];
        pin_odd [label="Odd Pin\\n(1,3,5...63)", fillcolor="#8b7355", fontcolor="white"];
    }
    
    // Signal conditioning cluster
    subgraph cluster_analog {
        label="Signal Conditioning";
        bgcolor="#e6f3ff";
        adc [label="ADC\\nSigma-Delta", fillcolor="#d4a76a"];
        dac [label="DAC\\n8-bit Flash", fillcolor="#4682b4", fontcolor="white"];
        comp [label="Comparator\\n& Schmitt", fillcolor="#5f9ea0"];
    }
    
    // Smart Pin cores cluster
    subgraph cluster_smart {
        label="Smart Pin Cores";
        bgcolor="#ffe6e6";
        sp_even [label="Smart Pin\\nEven #", fillcolor="#dc143c", fontcolor="white"];
        sp_odd [label="Smart Pin\\nOdd #", fillcolor="#dc143c", fontcolor="white"];
        modes [label="32 Operating\\nModes Each", fillcolor="#ff69b4"];
    }
    
    // COG interface cluster
    subgraph cluster_cogs {
        label="COG Interface";
        bgcolor="#e6ffe6";
        cog_bus [label="COG 0-7\\nDAC Bus", fillcolor="#90ee90"];
        commands [label="WXPIN/WYPIN\\nRDPIN/AKPIN", fillcolor="#98fb98"];
    }
    
    // Connections
    pin_even -> adc [label="analog in"];
    pin_even -> comp [label="digital in"];
    dac -> pin_even [label="analog out"];
    
    pin_odd -> adc [label="analog in"];
    pin_odd -> comp [label="digital in"];
    dac -> pin_odd [label="analog out"];
    
    adc -> sp_even;
    comp -> sp_even;
    sp_even -> dac;
    sp_even -> modes [style=dashed];
    
    adc -> sp_odd;
    comp -> sp_odd;
    sp_odd -> dac;
    sp_odd -> modes [style=dashed];
    
    cog_bus -> dac [label="streamer"];
    commands -> sp_even [label="control"];
    commands -> sp_odd [label="control"];
    sp_even -> commands [label="data", style=dotted];
    sp_odd -> commands [label="data", style=dotted];
}"""

def create_detailed_dot():
    """
    Create detailed diagram matching the original architecture
    """
    return """digraph SmartPinDetailed {
    rankdir=LR;
    compound=true;
    fontname="Arial";
    bgcolor="white";
    pad=0.5;
    
    label="P2 Smart Pin - Detailed Architecture";
    fontsize=16;
    labelloc=t;
    
    // Node defaults for record shapes
    node [shape=record, style=filled, fontsize=10];
    
    // Even pin architecture
    subgraph cluster_even {
        label="Even Pin Architecture (0,2,4...62)";
        bgcolor="#fffacd";
        style=filled;
        
        even_pin [label="Physical\\nEven #\\nPin", shape=box, fillcolor="#8b7355", fontcolor="white"];
        even_dac [label="{Flash DAC\\nNetwork|{%M...M|8-bit}}", fillcolor="#4682b4", fontcolor="white"];
        even_drive [label="{Logic Drive|{%M...M|%TT}}", fillcolor="#4682b4", fontcolor="white"];
        even_comp [label="Comparator\\nLogic\\nSchmitt\\n%M...M", shape=box, fillcolor="#5f9ea0"];
        even_adc [label="{Sigma-Delta\\nADC|%M...M}", fillcolor="#d4a76a"];
        even_smart [label="{Even #\\nSmart Pin|{%SSSSS_0|{WXPIN|WYPIN|RDPIN}|32 modes}}", 
                   fillcolor="#dc143c", fontcolor="white"];
        even_logic_out [label="{Logic Output|{%TT|Enable|Output|SmartOut}}", fillcolor="#ff8c00"];
        even_logic_in [label="{Logic Input|{%A_B_F|{-1|-2|-3|OUT}|{+1|+2|+3}}}", 
                      fillcolor="#808080", fontcolor="white"];
    }
    
    // Odd pin architecture
    subgraph cluster_odd {
        label="Odd Pin Architecture (1,3,5...63)";
        bgcolor="#fffacd";
        style=filled;
        
        odd_pin [label="Physical\\nOdd #\\nPin", shape=box, fillcolor="#8b7355", fontcolor="white"];
        odd_dac [label="{Flash DAC\\nNetwork|{%M...M|8-bit}}", fillcolor="#4682b4", fontcolor="white"];
        odd_drive [label="{Logic Drive|{%M...M|%TT}}", fillcolor="#4682b4", fontcolor="white"];
        odd_comp [label="Comparator\\nLogic\\nSchmitt\\n%M...M", shape=box, fillcolor="#5f9ea0"];
        odd_adc [label="{Sigma-Delta\\nADC|%M...M}", fillcolor="#d4a76a"];
        odd_smart [label="{Odd #\\nSmart Pin|{%SSSSS_0|{WXPIN|WYPIN|RDPIN}|32 modes}}", 
                  fillcolor="#dc143c", fontcolor="white"];
        odd_logic_out [label="{Logic Output|{%TT|Enable|Output|SmartOut}}", fillcolor="#ff8c00"];
        odd_logic_in [label="{Logic Input|{%A_B_F|{-1|-2|-3|OUT}|{+1|+2|+3}}}", 
                     fillcolor="#808080", fontcolor="white"];
    }
    
    // COG interface
    subgraph cluster_cog {
        label="COG Interface";
        bgcolor="#e0ffe0";
        style=filled;
        cog_dac [label="{DAC Bus\\nSelect|{COG 0-7|Streamers}}", fillcolor="#90ee90"];
        cog_cmds [label="COG\\nCommands", shape=box, fillcolor="#98fb98"];
    }
    
    // Even pin connections
    even_pin -> even_comp [dir=both];
    even_pin -> even_adc;
    even_dac -> even_pin;
    even_drive -> even_pin;
    
    even_comp -> even_logic_in [label="Input"];
    even_adc -> even_logic_in;
    even_logic_in -> even_smart [label="SmartA\\nSmartB"];
    even_smart -> even_logic_out [label="SmartOut"];
    even_logic_out -> even_drive [label="OUT"];
    even_logic_out -> even_dac [label="BitDAC"];
    
    // Odd pin connections
    odd_pin -> odd_comp [dir=both];
    odd_pin -> odd_adc;
    odd_dac -> odd_pin;
    odd_drive -> odd_pin;
    
    odd_comp -> odd_logic_in [label="Input"];
    odd_adc -> odd_logic_in;
    odd_logic_in -> odd_smart [label="SmartA\\nSmartB"];
    odd_smart -> odd_logic_out [label="SmartOut"];
    odd_logic_out -> odd_drive [label="OUT"];
    odd_logic_out -> odd_dac [label="BitDAC"];
    
    // COG connections
    cog_dac -> even_dac [label="DACBUS", style=bold, color="green"];
    cog_dac -> odd_dac [label="DACBUS", style=bold, color="green"];
    cog_cmds -> even_smart [label="32-bit\\ndata", dir=both];
    cog_cmds -> odd_smart [label="32-bit\\ndata", dir=both];
    
    // Cross-connections (pin routing)
    even_logic_in -> odd_logic_in [label="±3 pins", style=dotted, dir=both, color="blue"];
}"""

def create_pwm_path_dot():
    """
    PWM generation signal path highlighting
    """
    return """digraph PWMPath {
    rankdir=LR;
    fontname="Arial";
    bgcolor="white";
    pad=0.5;
    
    label="Smart Pin PWM Generation Path";
    fontsize=16;
    labelloc=t;
    
    node [shape=box, style="filled,rounded", fontsize=11];
    
    // Nodes in the PWM path
    cog [label="COG\\nWXPIN: period\\nWYPIN: duty", fillcolor="#98fb98"];
    smart [label="Smart Pin\\nPWM Mode\\n(%01001)", fillcolor="#dc143c", fontcolor="white"];
    counter [label="Period\\nCounter", fillcolor="#ffb6c1"];
    compare [label="Duty\\nComparator", fillcolor="#ffb6c1"];
    output [label="Logic\\nOutput", fillcolor="#ff8c00"];
    pin [label="Physical\\nPin", fillcolor="#8b7355", fontcolor="white"];
    
    // Signal flow
    cog -> smart [label="configure"];
    smart -> counter [label="period"];
    smart -> compare [label="duty"];
    counter -> compare [label="count"];
    compare -> output [label="PWM signal"];
    output -> pin [label="drive pin", style=bold, color="red"];
    
    // Annotation
    note [label="Runs autonomously\\nNo COG cycles needed\\nafter configuration", 
          shape=note, fillcolor="#ffffcc"];
    note -> smart [style=dotted, arrowhead=none];
}"""

def create_uart_path_dot():
    """
    UART communication path
    """
    return """digraph UARTPath {
    rankdir=LR;
    fontname="Arial";
    bgcolor="white";
    pad=0.5;
    
    label="Smart Pin UART Communication Path";
    fontsize=16;
    labelloc=t;
    
    node [shape=box, style="filled,rounded", fontsize=11];
    
    // TX path
    subgraph cluster_tx {
        label="Transmit Path";
        bgcolor="#ffe6e6";
        cog_tx [label="COG\\nWYPIN: byte", fillcolor="#98fb98"];
        smart_tx [label="Smart Pin\\nAsync TX\\n(%11110)", fillcolor="#dc143c", fontcolor="white"];
        shift_tx [label="Shift\\nRegister", fillcolor="#ffb6c1"];
        pin_tx [label="TX Pin", fillcolor="#8b7355", fontcolor="white"];
    }
    
    // RX path
    subgraph cluster_rx {
        label="Receive Path";
        bgcolor="#e6e6ff";
        pin_rx [label="RX Pin", fillcolor="#8b7355", fontcolor="white"];
        smart_rx [label="Smart Pin\\nAsync RX\\n(%11111)", fillcolor="#dc143c", fontcolor="white"];
        shift_rx [label="Shift\\nRegister", fillcolor="#b6c1ff"];
        cog_rx [label="COG\\nRDPIN: byte", fillcolor="#98fb98"];
    }
    
    // Connections
    cog_tx -> smart_tx [label="send"];
    smart_tx -> shift_tx [label="serialize"];
    shift_tx -> pin_tx [label="bits", style=bold];
    
    pin_rx -> smart_rx [label="bits", style=bold];
    smart_rx -> shift_rx [label="deserialize"];
    shift_rx -> cog_rx [label="byte ready"];
    
    // Timing note
    timing [label="Automatic baud rate\\ntiming generation", shape=note, fillcolor="#ffffcc"];
    timing -> smart_tx [style=dotted, arrowhead=none];
    timing -> smart_rx [style=dotted, arrowhead=none];
}"""

def create_adc_path_dot():
    """
    ADC sampling path
    """
    return """digraph ADCPath {
    rankdir=LR;
    fontname="Arial";
    bgcolor="white";
    pad=0.5;
    
    label="Smart Pin ADC Sampling Path";
    fontsize=16;
    labelloc=t;
    
    node [shape=box, style="filled,rounded", fontsize=11];
    
    // ADC signal path
    analog [label="Analog\\nSignal", shape=circle, fillcolor="#ffd700"];
    pin [label="Physical\\nPin", fillcolor="#8b7355", fontcolor="white"];
    adc [label="Sigma-Delta\\nADC", fillcolor="#d4a76a"];
    filter [label="SINC3\\nFilter", fillcolor="#daa520"];
    smart [label="Smart Pin\\nADC Mode\\n(%11000)", fillcolor="#dc143c", fontcolor="white"];
    accumulator [label="Sample\\nAccumulator", fillcolor="#ff69b4"];
    cog [label="COG\\nRDPIN: sample", fillcolor="#98fb98"];
    
    // Connections
    analog -> pin [label="voltage"];
    pin -> adc [label="analog", style=bold, color="blue"];
    adc -> filter [label="bitstream"];
    filter -> smart [label="filtered"];
    smart -> accumulator [label="accumulate"];
    accumulator -> cog [label="ready flag"];
    
    // Configuration
    config [label="WXPIN: mode\\nWYPIN: period", shape=note, fillcolor="#e6ffe6"];
    config -> smart [style=dotted];
    
    // Continuous operation note
    continuous [label="Continuous\\nsampling\\nno COG wait", shape=note, fillcolor="#ffffcc"];
    continuous -> accumulator [style=dotted, arrowhead=none];
}"""

def create_quadrature_path_dot():
    """
    Quadrature encoder path showing A/B input routing
    """
    return """digraph QuadraturePath {
    rankdir=LR;
    fontname="Arial";
    bgcolor="white";
    pad=0.5;
    
    label="Smart Pin Quadrature Decoder Path";
    fontsize=16;
    labelloc=t;
    
    node [shape=box, style="filled,rounded", fontsize=11];
    
    // Input pins
    subgraph cluster_inputs {
        label="Encoder Inputs";
        bgcolor="#fff4e6";
        pin_a [label="Pin A\\n(Phase A)", fillcolor="#8b7355", fontcolor="white"];
        pin_b [label="Pin B\\n(Phase B)", fillcolor="#8b7355", fontcolor="white"];
    }
    
    // Smart Pin processing
    subgraph cluster_decoder {
        label="Quadrature Decoder";
        bgcolor="#ffe6e6";
        router [label="Pin Router\\n(A/B select)", fillcolor="#808080", fontcolor="white"];
        smart [label="Smart Pin\\nQuad Mode\\n(%10110)", fillcolor="#dc143c", fontcolor="white"];
        counter [label="Position\\nCounter\\n32-bit", fillcolor="#ff69b4"];
        detector [label="Direction\\nDetector", fillcolor="#ffb6c1"];
    }
    
    // Output
    cog [label="COG\\nRDPIN: position", fillcolor="#98fb98"];
    
    // Connections
    pin_a -> router [label="A signal", color="blue"];
    pin_b -> router [label="B signal", color="green"];
    router -> smart [label="A & B"];
    smart -> detector [label="phase decode"];
    detector -> counter [label="up/down"];
    counter -> cog [label="position"];
    
    // State diagram
    state [label="A B\\n0 0 → 0 1\\n↓     ↑\\n1 0 ← 1 1", shape=note, fillcolor="#ffffcc"];
    state -> detector [style=dotted, arrowhead=none];
    
    // Note about neighbor pins
    neighbor [label="Can use pins\\n±3 positions\\nfor A/B inputs", shape=note, fillcolor="#e6ffe6"];
    neighbor -> router [style=dotted, arrowhead=none];
}"""

def generate_diagram(dot_content, output_path, formats=['png', 'svg']):
    """
    Generate diagram from DOT content using command-line tool
    """
    # Write DOT file
    dot_path = output_path + '.dot'
    with open(dot_path, 'w') as f:
        f.write(dot_content)
    
    # Generate each format
    for fmt in formats:
        output_file = f"{output_path}.{fmt}"
        cmd = ['/opt/local/bin/dot', '-T', fmt, dot_path, '-o', output_file]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ Generated: {os.path.basename(output_file)}")
            else:
                print(f"✗ Error generating {output_file}: {result.stderr}")
        except Exception as e:
            print(f"✗ Failed to run dot command: {e}")
    
    # Clean up DOT file
    os.remove(dot_path)

def main():
    """
    Generate all diagram variants
    """
    output_dir = '/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/exports/pdf-generation/outbound/P2-Smart-Pins-Reference/assets'
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    diagrams = [
        ('smart-pins-simple', create_simple_dot(), ['png', 'svg']),
        ('smart-pins-detailed', create_detailed_dot(), ['png', 'svg']),
        ('smart-pins-pwm-path', create_pwm_path_dot(), ['png']),
        ('smart-pins-uart-path', create_uart_path_dot(), ['png']),
        ('smart-pins-adc-path', create_adc_path_dot(), ['png']),
        ('smart-pins-quadrature-path', create_quadrature_path_dot(), ['png'])
    ]
    
    print("Generating Smart Pin architecture diagrams...")
    print(f"Output directory: {output_dir}\n")
    
    for name, dot_content, formats in diagrams:
        output_path = os.path.join(output_dir, name)
        generate_diagram(dot_content, output_path, formats)
    
    print(f"\n✅ All diagrams generated successfully!")
    print(f"Location: {output_dir}")

if __name__ == '__main__':
    main()