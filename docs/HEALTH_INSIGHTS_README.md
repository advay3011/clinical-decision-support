# Health Insights Agent

An educational health analysis tool that reads medical reports, extracts lab values, analyzes patterns, and generates structured health insights. **This tool provides educational information only and is NOT a medical diagnosis tool.**

## ⚠️ MEDICAL DISCLAIMER

**CRITICAL:** This agent provides educational information only and should NEVER be used for medical diagnosis, treatment, or clinical decision-making. Always consult with qualified healthcare professionals for medical advice. This tool is designed to help users understand their lab results in plain language, not to replace professional medical judgment.

## Features

### Core Capabilities

1. **PDF Ingestion** - Extract text from medical reports and lab documents
2. **Metric Parsing** - Identify and extract lab values from unstructured text
3. **Unit Normalization** - Convert units to standard forms for comparison
4. **Reference Lookup** - Check values against clinical reference ranges
5. **Abnormal Detection** - Flag values outside normal ranges with severity levels
6. **Pattern Analysis** - Identify multi-marker patterns indicating potential health concerns
7. **Risk Scoring** - Assign risk severity based on abnormal findings and patterns
8. **Insight Generation** - Generate plain language explanations of findings
9. **Report Building** - Produce structured, comprehensive health insight reports

### Supported Lab Metrics

- **Metabolic Panel**: Glucose, Total Cholesterol, LDL, HDL, Triglycerides
- **Blood Count**: Hemoglobin, Hematocrit
- **Liver Function**: ALT, AST, Bilirubin
- **Kidney Function**: Creatinine, BUN
- **Thyroid**: TSH, T3, T4
- **Electrolytes**: Sodium, Potassium, Chloride

### Multi-Marker Patterns Detected

- **Metabolic Concern**: Elevated glucose + elevated triglycerides
- **Lipid Concern**: High cholesterol + low HDL
- **Liver Concern**: Elevated ALT + elevated AST
- **Kidney Concern**: Elevated creatinine + elevated BUN

## Architecture

### Tool Pipeline

```
PDF Report
    ↓
[PDF Processor] → Extract text
    ↓
[Text Cleaner] → Normalize and clean
    ↓
[Lab Metric Extractor] → Parse values
    ↓
[Unit Normalizer] → Standardize units
    ↓
[Clinical Reference Lookup] → Get normal ranges
    ↓
[Abnormal Flag Detector] → Identify abnormalities
    ↓
[Pattern Detector] → Find multi-marker patterns
    ↓
[Risk Scorer] → Calculate risk level
    ↓
[Plain Language Explainer] → Generate explanations
    ↓
[Report Builder] → Create structured report
```

### Tools Included

1. **pdf_processor** - Extracts text from PDF content
2. **text_cleaner** - Cleans and normalizes extracted text
3. **lab_metric_extractor** - Parses lab values and units
4. **unit_normalizer** - Converts units to standard forms
5. **clinical_reference_lookup** - Retrieves reference ranges
6. **abnormal_flag_detector** - Identifies abnormal values
7. **pattern_detector** - Detects multi-marker patterns
8. **risk_scorer** - Calculates overall risk level
9. **plain_language_explainer** - Generates readable explanations
10. **report_builder** - Creates comprehensive reports

## Installation

```bash
pip install -r health_insights_requirements.txt
```

### Requirements

- Python 3.8+
- anthropic >= 0.28.0
- bedrock-agents >= 0.1.0
- pydantic >= 2.0.0
- python-dotenv >= 1.0.0
- PyPDF2 >= 3.0.0

## Usage

### Basic Usage

```python
from health_insights_agent import create_health_insights_agent

# Create agent
agent = create_health_insights_agent()

# Analyze medical report
report_text = """
LABORATORY TEST RESULTS
Glucose: 125 mg/dL
Total Cholesterol: 220 mg/dL
HDL Cholesterol: 35 mg/dL
Triglycerides: 180 mg/dL
"""

# Run analysis
response = agent.run(f"Analyze this medical report: {report_text}")
```

### Running the Demo

```bash
python health_insights_demo.py
```

This runs a complete workflow demonstrating:
- PDF processing
- Text cleaning
- Metric extraction
- Unit normalization
- Reference range lookup
- Abnormal detection
- Pattern detection
- Risk scoring
- Plain language explanations
- Report generation

## Report Structure

The generated report includes:

```json
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
  "risk_assessment": {
    "risk_score": 5,
    "risk_level": "moderate"
  },
  "recommendations": [...]
}
```

## Risk Levels

- **Low**: 0-1 abnormal metrics, no patterns
- **Moderate**: 2-4 abnormal metrics or 1-2 patterns
- **High**: 5+ abnormal metrics or 3+ patterns

## Clinical Reference Ranges

### Glucose (Fasting)
- Normal: 70-100 mg/dL
- Elevated: > 100 mg/dL

### Hemoglobin
- Male: 13.5-17.5 g/dL
- Female: 12.0-15.5 g/dL

### Total Cholesterol
- Optimal: < 200 mg/dL
- Borderline: 200-239 mg/dL
- High: ≥ 240 mg/dL

### HDL Cholesterol
- Low: < 40 mg/dL
- Optimal: ≥ 60 mg/dL

### Triglycerides
- Normal: < 150 mg/dL
- Borderline: 150-199 mg/dL
- High: ≥ 200 mg/dL

### Liver Enzymes (ALT/AST)
- Normal: 7-56 U/L (ALT), 10-40 U/L (AST)

### Kidney Function
- Creatinine: 0.6-1.3 mg/dL
- BUN: 7-20 mg/dL

## Plain Language Explanations

The agent generates user-friendly explanations for each metric:

```
Glucose: 125 mg/dL
"Your glucose level (125 mg/dL) is above the normal range (70-100 mg/dL). 
This may indicate your body is having difficulty regulating blood sugar."
```

## Pattern Detection Examples

### Metabolic Concern Pattern
- Triggered by: Elevated glucose + elevated triglycerides
- Significance: May indicate metabolic dysfunction
- Recommendation: Consult healthcare provider

### Lipid Concern Pattern
- Triggered by: High cholesterol + low HDL
- Significance: May increase cardiovascular risk
- Recommendation: Discuss with healthcare provider

## Important Guidelines

### What This Tool Does
✓ Extracts lab values from reports
✓ Compares values to reference ranges
✓ Identifies abnormal findings
✓ Detects multi-marker patterns
✓ Generates educational explanations
✓ Produces structured reports

### What This Tool Does NOT Do
✗ Provide medical diagnosis
✗ Recommend treatments
✗ Replace healthcare professionals
✗ Provide clinical decision support
✗ Diagnose diseases or conditions

## Integration with Strands

This agent is designed to work with the Strands Agent SDK:

```python
from strands_sdk import Agent, Tool

# Tools are pre-configured for Strands integration
agent = create_health_insights_agent()

# Run with Strands framework
result = agent.execute(user_query)
```

## Error Handling

The agent handles:
- Missing or incomplete lab data
- Unknown metric names
- Invalid unit formats
- Missing reference ranges
- Malformed PDF content

## Limitations

1. **Reference Ranges**: Based on general population standards; individual ranges may vary
2. **Unit Support**: Currently supports common units; custom units may need mapping
3. **Metric Coverage**: Supports common lab metrics; specialized tests may not be recognized
4. **Gender-Specific Ranges**: Limited to male/female; other variations not supported
5. **Age-Specific Ranges**: Uses adult reference ranges; pediatric ranges not included

## Future Enhancements

- [ ] Support for pediatric reference ranges
- [ ] Age-specific reference ranges
- [ ] Pregnancy-specific ranges
- [ ] Medication interaction analysis
- [ ] Trend analysis across multiple reports
- [ ] Integration with EHR systems
- [ ] Multi-language support
- [ ] Advanced pattern recognition with ML

## Contributing

To add new metrics or patterns:

1. Add reference ranges to `clinical_reference_lookup()`
2. Add pattern detection logic to `pattern_detector()`
3. Add explanations to `plain_language_explainer()`
4. Update documentation

## Support

For issues or questions:
1. Check the demo script for usage examples
2. Review the tool documentation
3. Consult the Strands SDK documentation
4. Contact healthcare professionals for medical questions

## License

This tool is provided for educational purposes only.

## Disclaimer

**This tool is NOT a medical device and should NOT be used for clinical decision-making. Always consult with qualified healthcare professionals for medical advice, diagnosis, or treatment. The creators and maintainers of this tool are not responsible for any medical decisions made based on its output.**
