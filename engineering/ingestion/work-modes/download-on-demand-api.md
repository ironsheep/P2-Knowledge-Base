# Mini-Guide: Download-on-Demand API Build

## Purpose
Build efficient API to serve P2 knowledge from central repository to AI agents for demo in 1 week.

## Context Required
- Read: `/engineering/planning/SNAPSHOT-AND-DEMO-STRATEGY.md` (demo timeline)
- Read: `/engineering/ingestion/work-modes/central-repository-build.md` (prerequisite)
- Complete: Central repository must exist first

## Data Flow
```
[SOURCE] → [PROCESSING] → [OUTPUT]
/central-repository/    api_server.py    https://api.p2knowledge.com/
```

## Source Location (INPUT)
```bash
/central-repository/                    # Created by central-repository-build
├── instructions/                       # 491 instruction YAML files
│   ├── ADD.yaml
│   ├── ADDX.yaml
│   └── ...
├── smart-pins/                        # 32 mode YAML files
│   ├── async-serial-tx.yaml
│   └── ...
├── architecture/                      # Core P2 structure
│   └── core.yaml
└── manifest.yaml                      # Complete index
```

## Output API Structure
```
https://api.p2knowledge.com/v1/
├── /query                             # Natural language queries
├── /instruction/{name}                # Get specific instruction
├── /smart-pin/{mode}                  # Get specific smart pin mode
├── /search                            # Structured search
├── /context/{task}                    # Task-specific bundles
└── /manifest                          # Available knowledge index
```

## Immediate Actions

### Step 1: Design Query Interface
```python
# Natural language → Relevant knowledge chunks
POST /query
{
    "prompt": "Help me write UART code",
    "context": "beginner",
    "max_tokens": 4000
}

Response:
{
    "instructions": ["WRPIN", "WXPIN", "WYPIN", "RDPIN"],
    "smart_pins": ["async-serial-tx", "async-serial-rx"],
    "examples": [...],
    "confidence": 0.95
}
```

### Step 2: Build API Server
```python
# api_server.py
from flask import Flask, jsonify
import yaml
import os

app = Flask(__name__)

# Load central repository
def load_knowledge():
    knowledge = {}
    # Load from /central-repository/
    return knowledge

@app.route('/v1/instruction/<name>')
def get_instruction(name):
    # Return specific instruction
    with open(f'/central-repository/instructions/{name}.yaml') as f:
        return jsonify(yaml.safe_load(f))

@app.route('/v1/query', methods=['POST'])
def query():
    # Process natural language query
    # Return relevant knowledge chunks
    pass
```

### Step 3: Create Context Bundles
```python
# Pre-computed bundles for common tasks
contexts = {
    "uart_setup": {
        "instructions": ["WRPIN", "WXPIN", "WYPIN", "RDPIN"],
        "smart_pins": ["async-serial-tx", "async-serial-rx"],
        "examples": load_uart_examples(),
        "pattern": "smart-pin-serial-pattern.md"
    },
    "led_blink": {
        "instructions": ["DIRH", "OUTH", "OUTL", "WAITMS"],
        "pins": ["digital-output"],
        "examples": load_led_examples()
    },
    "extended_math": {
        "instructions": ["ADD", "ADDX", "ADDSX", "SUB", "SUBX", "SUBSX"],
        "patterns": load_from_chip_gracey(),
        "confidence": 1.0  # From Chip himself
    }
}
```

### Step 4: Optimize for AI Context Windows
```python
def optimize_response(knowledge, max_tokens=4000):
    """
    Trim response to fit context window
    Priority: examples > description > technical > metadata
    """
    essential = extract_essential(knowledge)
    if token_count(essential) < max_tokens:
        return essential
    else:
        return prioritize_content(essential, max_tokens)
```

## Local Test Setup
```bash
# Directory structure for local testing
/engineering/api/
├── api_server.py              # Flask API server
├── query_engine.py            # Natural language processing
├── test_queries.py            # Demo scenarios
└── requirements.txt           # Python dependencies
```

## Demo Scenarios to Implement

### Scenario 1: "Help me blink an LED"
```json
Request: {"prompt": "Help me blink an LED on pin 56"}
Response: {
    "instructions": ["DIRH", "OUTH", "OUTL", "WAITMS"],
    "example": "' Blink LED on P56\nloop:\n    OUTH #56\n    WAITMS #500\n    OUTL #56\n    WAITMS #500\n    JMP #loop",
    "explanation": "Use DIRH to set pin as output, then toggle with OUTH/OUTL"
}
```

### Scenario 2: "Create UART at 115200"
```json
Request: {"prompt": "Setup UART at 115200 baud on pins 0-1"}
Response: {
    "smart_pin_mode": "async_serial",
    "setup_code": "...",
    "baud_calculation": "sysclock / 115200"
}
```

### Scenario 3: "Debug SETQ issue"
```json
Request: {"prompt": "Why isn't my SETQ block transfer working with PTRA++?"}
Response: {
    "known_bug": true,
    "issue": "SETQ/PTRx silicon bug",
    "workaround": "Don't use ALTx/AUGS/AUGD between SETQ and transfer",
    "source": "KNOWN-BUGS-CRITICAL.md"
}
```

## Success Criteria
- [ ] API responds in <100ms locally
- [ ] Natural language queries return relevant knowledge
- [ ] Context fits in 4K-8K token windows
- [ ] All demo scenarios work perfectly
- [ ] Confidence scores included
- [ ] Source attribution preserved

## Time Budget
- API design: 2 hours
- Server implementation: 4 hours
- Query engine: 3 hours
- Demo scenarios: 2 hours
- Testing & polish: 2 hours
- **Total: 13 hours over 2-3 days**

## Key Decisions Already Made
1. **REST API** - Simple, standard, debuggable
2. **Local first** - Deploy to cloud later if needed
3. **Pre-computed contexts** - Fast demo responses
4. **YAML source** - Already structured from central repo
5. **Python/Flask** - Quick to build and deploy

## Files to Create
```bash
# Implementation files
/engineering/api/
├── api_server.py              # Main API server
├── query_engine.py            # NLP to knowledge mapper
├── context_builder.py         # Bundle related knowledge
├── test_client.py             # Test the API
└── demo_scenarios.json        # Pre-built demo queries
```

## Deployment Options (Post-Demo)

### Option 1: Local Server
```bash
python api_server.py  # Runs on localhost:5000
```

### Option 2: Cloud Function
- AWS Lambda + API Gateway
- Google Cloud Functions
- Vercel/Netlify Functions

### Option 3: Static CDN
- Pre-generate all possible responses
- Serve from CDN as static JSON
- No server needed

## Remember
- Demo in 1 week - working demo beats perfect API
- Central repository is the source
- Optimize for AI agent consumption
- Focus on the three demo scenarios
- Polish after successful demo

## Integration with Claude Code
```python
# How Claude Code will use our API
import requests

def get_p2_knowledge(prompt):
    response = requests.post(
        "http://localhost:5000/v1/query",
        json={"prompt": prompt, "max_tokens": 4000}
    )
    return response.json()

# In Claude Code:
knowledge = get_p2_knowledge("How do I setup UART?")
# Use knowledge to generate P2 code...
```

## Next Steps
1. Central repository must be complete
2. Build basic API server
3. Implement demo scenarios
4. Test with mock Claude Code queries
5. Polish for live demo