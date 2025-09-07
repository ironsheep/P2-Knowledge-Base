# P2 Knowledge Base Content Filters

## Overview
Content filtering system to ensure technical accuracy and remove non-technical material from the P2 Knowledge Base. The primary focus is removing marketing content, subjective claims, and non-technical narratives while preserving educational and technical comparisons.

## Marketing Filter System

### Purpose
The marketing filter (`marketing-filter.py`) identifies and removes:
- Marketing language and superlatives
- Competitor comparisons (non-educational)
- Subjective claims without technical backing
- Historical narratives not relevant to implementation

### Detection Categories

#### 1. Marketing Phrases
**Detected:**
- Superlatives: "revolutionary", "game-changing", "breakthrough"
- Comparisons: "better than", "superior to", "outperforms"
- Sales language: "perfect for", "save time", "increase productivity"

**Preserved:**
- Technical metrics: "2x faster", "8 cycles vs 16"
- Educational comparisons: "similar to", "differs from"

#### 2. Subjective Claims
**Detected:**
- Opinions without data: "amazing performance"
- Unsubstantiated claims: "easy to use"
- Marketing adjectives: "powerful", "robust", "comprehensive"

**Preserved:**
- Claims with metrics: "powerful 32-bit processing"
- Technical descriptions: "comprehensive instruction set of 500+ opcodes"

#### 3. Competitor Comparisons
**Detected:**
- Product comparisons: "unlike Arduino", "beats Intel"
- Marketing positioning: "market leader", "competitive advantage"

**Preserved:**
- Architecture education: "ARM-like pipeline structure"
- Technical contrasts: "unlike RISC-V, P2 includes..."

#### 4. Historical Narratives
**Detected:**
- Company history: "founded in 2006"
- Development stories: "the journey began"
- Non-technical evolution: "started as a hobby project"

**Preserved:**
- Version history: "introduced in v2.0"
- Technical evolution: "deprecated since revision 3"

## Usage

### Basic Filtering
```bash
# Filter entire repository
python3 filters/marketing-filter.py

# Filter single entry
python3 filters/marketing-filter.py --entry instructions/pasm2/add-instruction.yaml

# Dry run (analyze without modifying)
python3 filters/marketing-filter.py --dry-run
```

### Review Process
```bash
# Check review queue
cat update-tracking/filter-logs/review-queue-*.yaml

# Manual review of borderline cases
python3 filters/review-manager.py
```

## Filter Configuration

### Whitelist Patterns
Technical comparisons are preserved when they include:
- Specific metrics (cycles, bytes, MHz)
- Technical units (bits, registers, pins)
- Educational context (example, demonstration)
- Architecture terms (latency, throughput, bandwidth)

### Subjectivity Scoring
- **0.0-0.3**: Objective, technical content
- **0.3-0.6**: Mixed content, review recommended
- **0.6-0.8**: Subjective, flagged for review
- **0.8-1.0**: Marketing content, auto-removed

### Edge Case Handling

#### Legitimate Technical Comparisons
```yaml
# Preserved:
timing:
  cycles: "2-9"  # 2x faster than previous version
  
# Removed:
description: "Blazingly fast execution"  # No metrics
```

#### Educational Comparisons
```yaml
# Preserved:
usage_notes: "Similar to MOV but affects flags"

# Removed:  
description: "Better than competing processors"
```

#### Embedded Marketing
```yaml
# Before:
description: "This revolutionary instruction provides amazing 32-bit multiply"

# After:
description: "This instruction provides 32-bit multiply"
```

## Output Files

### Filter Logs
Location: `update-tracking/filter-logs/`
- `filter-log-{timestamp}.yaml` - All filtering actions
- `review-queue-{timestamp}.yaml` - Items needing human review
- `filtered-content-{timestamp}.yaml` - Original content for rollback

### Reports
Location: `update-tracking/reports/`
- `filter-report-{timestamp}.md` - Comprehensive filtering report

## Review Queue Management

### Borderline Cases
Items with subjectivity scores between 0.6-0.8 are queued for review:

```yaml
- entry: instructions/pasm2/mul-instruction.yaml
  detection:
    type: subjective_claim
    text: "Provides efficient multiplication"
    subjectivity_score: 0.65
    needs_review: true
```

### Review Actions
1. **Accept**: Keep the filtered version
2. **Reject**: Restore original content
3. **Modify**: Custom edit the content
4. **Whitelist**: Add pattern to whitelist

## Integration with Extraction Pipeline

### Pre-Extraction Filtering
Apply filters during extraction to prevent marketing content from entering:

```python
from filters.marketing_filter import MarketingFilter

filter = MarketingFilter(repo_path)
# During extraction
cleaned_text = filter.clean_text(extracted_text, 
                                filter.is_marketing_phrase(extracted_text))
```

### Post-Extraction Cleanup
Regular filtering passes to maintain quality:

```bash
# Weekly cleanup
0 0 * * 0 cd /path/to/repo && python3 filters/marketing-filter.py
```

## Rollback Capability

### Restore Original Content
All filtered content is preserved for rollback:

```bash
# Restore from filtered-content backup
python3 filters/restore-original.py --backup filtered-content-20250106_120000.yaml
```

### Selective Restoration
Restore specific entries or fields:

```bash
# Restore single entry
python3 filters/restore-original.py --entry add-instruction --field description
```

## Best Practices

### 1. Regular Filtering
- Run after each major extraction
- Weekly maintenance filtering
- Review queue processing within 48 hours

### 2. Whitelist Maintenance
- Add legitimate technical phrases
- Document whitelist additions
- Review whitelist quarterly

### 3. Human Review
- Prioritize high-score items
- Document review decisions
- Create review guidelines

### 4. Quality Metrics
Track filtering effectiveness:
- False positive rate
- Review queue resolution time
- Content quality improvement

## Troubleshooting

### Common Issues

#### "NLTK not available"
Install sentiment analyzer:
```bash
pip install nltk
python -c "import nltk; nltk.download('vader_lexicon')"
```

#### "Too many items in review queue"
Adjust sensitivity:
```python
# In marketing-filter.py
if subjective_score > 0.7:  # Increase threshold
```

#### "Legitimate content removed"
Add to whitelist:
```python
self.technical_whitelist.append(r'your_pattern_here')
```

## Future Enhancements

### Planned Features
- Machine learning-based detection
- Context-aware filtering
- Multi-language support
- Real-time filtering API
- Automated whitelist learning

### Proposed Improvements
- Sentiment analysis refinement
- Domain-specific dictionaries
- Collaborative review interface
- Filtering effectiveness metrics
- Integration with CI/CD pipeline