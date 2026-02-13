# Health Insights Agent - Architecture & Design

## System Overview

The Health Insights Agent is a multi-stage pipeline that processes medical reports and generates educational health insights. It follows a strand-based architecture with specialized tools for each processing stage.

```
┌─────────────────────────────────────────────────────────────────┐
│                    HEALTH INSIGHTS AGENT                        │
│                  (Strands Agent Framework)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │      INPUT: Medical Report (PDF/Text)   │
        └─────────────────────────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
    ┌────────────────┐                    ┌──────────────────┐
    │ PDF Processor  │                    │  Text Cleaner    │
    │ (Extract Text) │                    │ (Normalize Text) │
    └────────────────┘                    └──────────────────┘
        │                                           │
        └─────────────────────┬─────────────────────┘
                              │
                              ▼
                ┌──────────────────────────────┐
                │  Lab Metric Extractor        │
                │  (Parse Values & Units)      │
                └──────────────────────────────┘
                              │
                              ▼
                ┌──────────────────────────────┐
                │  Unit Normalizer             │
                │  (Standardize Units)         │
                └──────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │  Clinical Reference Lookup              │
        │  (Get Normal Ranges for Each Metric)    │
        └─────────────────────────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
    ┌────────────────────┐            ┌──────────────────────┐
    │ Abnormal Flag      │            │ Pattern Detector     │
    │ Detector           │            │ (Multi-Marker        │
    │ (Check Ranges)     │            │  Pattern Analysis)   │
    └────────────────────┘            └──────────────────────┘
        │                                           │
        └─────────────────────┬─────────────────────┘
                              │
                              ▼
                ┌──────────────────────────────┐
                │  Risk Scorer                 │
                │  (Calculate Risk Level)      │
                └──────────────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
    ┌────────────────────┐            ┌──────────────────────┐
    │ Plain Language     │            │ Report Builder       │
    │ Explainer          │            │ (Structured Report)  │
    │ (Generate Text)    │            │                      │
    └────────────────────┘            └──────────────────────┘
        │                                           │
        └─────────────────────┬─────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │  OUTPUT: Health Insights Report (JSON)  │
        │  - Summary                              │
        │  - Abnormal Metrics                     │
        │  - Patterns Detected                    │
        │  - Risk Assessment                      │
        │  - Plain Language Explanations          │
        │  - Medical Disclaimer                   │
        └─────────────────────────────────────────┘
```

## Tool Architecture

### Stage 1: Input Processing

#### pdf_processor
- **Input**: Raw PDF content or text
- **Output**: Extracted text with metadata
- **Purpose**: Convert PDF to processable text
- **Error Handling**: Handles malformed PDFs gracefully

#### text_cleaner
- **Input**: Raw extracted text
- **Output**: Cleaned, normalized text
- **Purpose**: Remove noise and standardize formatting
- **Processing**: Regex-based cleaning, whitespace normalization

### Stage 2: Data Extraction

#### lab_metric_extractor
- **Input**: Cleaned text
- **Output**: Dictionary of metrics with values and units
- **Purpose**: Parse lab values from unstructured text
- **Pattern**: Regex matching for "metric: value unit"
- **Robustness**: Handles variations in formatting

### Stage 3: Normalization

#### unit_normalizer
- **Input**: Extracted metrics with units
- **Output**: Normalized metrics with standard units
- **Purpose**: Convert different unit formats to standards
- **Conversions**: mg/dL ↔ mmol/L, g/dL ↔ g/L, etc.
- **Extensibility**: Easy to add new conversions

### Stage 4: Reference & Validation

#### clinical_reference_lookup
- **Input**: Metric name, optional gender
- **Output**: Reference range with min/max values
- **Purpose**: Retrieve clinical normal ranges
- **Data Source**: Evidence-based clinical standards
- **Gender-Specific**: Supports male/female variations
- **Extensibility**: Easy to add new metrics

#### abnormal_flag_detector
- **Input**: Metric name, value, reference range
- **Output**: Abnormality flag with severity
- **Purpose**: Identify out-of-range values
- **Severity Levels**: normal, low, high
- **Direction**: Tracks if value is above or below range

### Stage 5: Pattern Analysis

#### pattern_detector
- **Input**: All extracted metrics
- **Output**: List of detected multi-marker patterns
- **Purpose**: Identify concerning combinations
- **Patterns**:
  - Metabolic concern (glucose + triglycerides)
  - Lipid concern (cholesterol + HDL)
  - Liver concern (ALT + AST)
  - Kidney concern (creatinine + BUN)
- **Extensibility**: Easy to add new patterns

### Stage 6: Risk Assessment

#### risk_scorer
- **Input**: Abnormal metrics, detected patterns
- **Output**: Risk score and risk level
- **Purpose**: Quantify overall health risk
- **Scoring**:
  - 1 point per abnormal metric
  - 2 points per detected pattern
- **Risk Levels**:
  - Low: 0-1 points
  - Moderate: 2-4 points
  - High: 5+ points

### Stage 7: Explanation Generation

#### plain_language_explainer
- **Input**: Metric name, value, range, severity
- **Output**: Human-readable explanation
- **Purpose**: Make findings understandable
- **Language**: Non-technical, accessible
- **Tone**: Educational, non-alarming
- **Extensibility**: Easy to add new explanations

### Stage 8: Report Generation

#### report_builder
- **Input**: All analysis results
- **Output**: Structured JSON report
- **Purpose**: Consolidate findings into report
- **Components**:
  - Report metadata
  - Medical disclaimer
  - Summary statistics
  - Detailed findings
  - Risk assessment
  - Recommendations
  - Structured data for integration

## Data Flow

### Input Data Structure

```python
{
    "report_text": "LABORATORY TEST RESULTS...",
    "patient_info": {
        "gender": "female",
        "age": 45  # optional
    }
}
```

### Metric Data Structure

```python
{
    "glucose": {
        "value": 125,
        "unit": "mg/dL",
        "raw": "125 mg/dL"
    },
    "cholesterol": {
        "value": 220,
        "unit": "mg/dL",
        "raw": "220 mg/dL"
    }
}
```

### Abnormal Flag Structure

```python
{
    "metric": "glucose",
    "value": 125,
    "is_abnormal": True,
    "severity": "high",
    "direction": "above",
    "reference_range": {
        "min": 70,
        "max": 100,
        "unit": "mg/dL"
    }
}
```

### Pattern Structure

```python
{
    "pattern": "metabolic_concern",
    "markers": ["glucose", "triglycerides"],
    "description": "Elevated glucose and triglycerides may indicate metabolic concerns"
}
```

### Risk Score Structure

```python
{
    "risk_score": 4,
    "risk_level": "moderate",
    "abnormal_count": 3,
    "pattern_count": 1
}
```

### Final Report Structure

```python
{
    "report_type": "Health Insights Report",
    "generated_at": "2024-02-05T10:30:00",
    "disclaimer": "MEDICAL DISCLAIMER: ...",
    "summary": {
        "total_metrics_analyzed": 10,
        "abnormal_metrics": 3,
        "patterns_detected": 2,
        "overall_risk_level": "moderate"
    },
    "metrics_analysis": {
        "normal": [...],
        "abnormal": [...]
    },
    "patterns": [...],
    "risk_assessment": {...},
    "recommendations": [...]
}
```

## Reference Data

### Clinical Reference Ranges

```python
reference_ranges = {
    "glucose": {
        "normal": {"min": 70, "max": 100, "unit": "mg/dL"}
    },
    "hemoglobin": {
        "male": {"min": 13.5, "max": 17.5, "unit": "g/dL"},
        "female": {"min": 12.0, "max": 15.5, "unit": "g/dL"}
    },
    "cholesterol": {
        "total": {"min": 0, "max": 200, "unit": "mg/dL"}
    },
    # ... more metrics
}
```

### Unit Conversions

```python
unit_conversions = {
    "mg/dL": {"glucose": 1, "cholesterol": 1},
    "mmol/L": {"glucose": 0.0555, "cholesterol": 0.0259},
    "g/dL": {"hemoglobin": 1},
    "g/L": {"hemoglobin": 10},
    # ... more conversions
}
```

## Error Handling Strategy

### Input Validation
- Check for empty/null inputs
- Validate metric names
- Verify unit formats
- Handle missing reference ranges

### Processing Errors
- Graceful degradation for unknown metrics
- Skip unparseable values
- Continue processing with available data
- Log warnings for missing data

### Output Validation
- Ensure all required fields present
- Validate data types
- Include error messages in report
- Always include disclaimer

## Extensibility Points

### Adding New Metrics

1. Add to `clinical_reference_lookup()`:
```python
"new_metric": {
    "normal": {"min": X, "max": Y, "unit": "Z"}
}
```

2. Add explanation to `plain_language_explainer()`:
```python
"new_metric": {
    "high": "Explanation for high value",
    "low": "Explanation for low value",
    "normal": "Explanation for normal value"
}
```

### Adding New Patterns

1. Add detection logic to `pattern_detector()`:
```python
if ("metric1" in metrics and metrics["metric1"]["value"] > threshold and
    "metric2" in metrics and metrics["metric2"]["value"] > threshold):
    patterns.append({
        "pattern": "new_pattern",
        "markers": ["metric1", "metric2"],
        "description": "Description of concern"
    })
```

### Adding New Unit Conversions

1. Add to `unit_normalizer()`:
```python
unit_conversions = {
    "new_unit": {"metric": conversion_factor}
}
```

## Performance Considerations

### Optimization Strategies
- Cache reference ranges
- Pre-compile regex patterns
- Batch metric lookups
- Lazy load reference data

### Scalability
- Process large reports in chunks
- Stream processing for very large files
- Parallel pattern detection
- Async tool execution

## Security Considerations

### Data Privacy
- No data persistence by default
- No external API calls
- Local processing only
- No logging of sensitive data

### Input Validation
- Sanitize text input
- Validate metric values
- Check unit formats
- Prevent injection attacks

## Integration Points

### With Strands Framework
```python
agent = Agent(
    name="Health Insights Agent",
    tools=tools,
    system_prompt=system_prompt,
    model="anthropic.claude-3-5-sonnet-20241022"
)
```

### With External Systems
- JSON output for API integration
- Structured data for database storage
- Plain text for email/messaging
- HTML for web display

## Testing Strategy

### Unit Tests
- Test each tool independently
- Verify reference ranges
- Test pattern detection
- Validate risk scoring

### Integration Tests
- Test full pipeline
- Verify data flow
- Check output structure
- Validate disclaimers

### Edge Cases
- Missing metrics
- Invalid units
- Extreme values
- Malformed input

## Deployment Considerations

### Requirements
- Python 3.8+
- Anthropic SDK
- Bedrock Agents SDK
- Standard libraries only

### Configuration
- Environment variables for API keys
- Configurable reference ranges
- Customizable patterns
- Adjustable risk thresholds

### Monitoring
- Log processing steps
- Track errors
- Monitor performance
- Audit report generation
