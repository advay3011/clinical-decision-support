# Health Insights Agent - Quick Start Guide

## Installation

```bash
pip install -r health_insights_requirements.txt
```

## Run the Demo

```bash
python health_insights_demo.py
```

## Basic Usage

### 1. Create the Agent

```python
from health_insights_agent import create_health_insights_agent

agent = create_health_insights_agent()
```

### 2. Analyze a Medical Report

```python
report = """
LABORATORY TEST RESULTS
Glucose: 125 mg/dL
Total Cholesterol: 220 mg/dL
HDL Cholesterol: 35 mg/dL
Triglycerides: 180 mg/dL
"""

response = agent.run(f"Analyze this report: {report}")
```

### 3. Get Structured Report

The agent returns a comprehensive report with:
- Summary of findings
- Abnormal metrics flagged
- Multi-marker patterns detected
- Risk assessment
- Plain language explanations
- Medical disclaimer

## Tool Pipeline

```
Medical Report
    ↓
Extract Text (pdf_processor)
    ↓
Clean Text (text_cleaner)
    ↓
Parse Metrics (lab_metric_extractor)
    ↓
Normalize Units (unit_normalizer)
    ↓
Check References (clinical_reference_lookup)
    ↓
Flag Abnormals (abnormal_flag_detector)
    ↓
Detect Patterns (pattern_detector)
    ↓
Score Risk (risk_scorer)
    ↓
Explain Results (plain_language_explainer)
    ↓
Build Report (report_builder)
```

## Supported Metrics

| Metric | Normal Range | Unit |
|--------|--------------|------|
| Glucose (Fasting) | 70-100 | mg/dL |
| Total Cholesterol | <200 | mg/dL |
| LDL Cholesterol | <100 | mg/dL |
| HDL Cholesterol | >40 | mg/dL |
| Triglycerides | <150 | mg/dL |
| Hemoglobin (M) | 13.5-17.5 | g/dL |
| Hemoglobin (F) | 12.0-15.5 | g/dL |
| ALT | 7-56 | U/L |
| AST | 10-40 | U/L |
| Creatinine (M) | 0.7-1.3 | mg/dL |
| Creatinine (F) | 0.6-1.1 | mg/dL |
| BUN | 7-20 | mg/dL |

## Detected Patterns

### Metabolic Concern
- **Triggers**: Glucose > 100 + Triglycerides > 150
- **Significance**: May indicate metabolic dysfunction

### Lipid Concern
- **Triggers**: Cholesterol > 200 + HDL < 40
- **Significance**: May increase cardiovascular risk

### Liver Concern
- **Triggers**: ALT > 56 + AST > 40
- **Significance**: May indicate liver stress

### Kidney Concern
- **Triggers**: Creatinine > 1.3 + BUN > 20
- **Significance**: May indicate kidney function concerns

## Risk Levels

| Level | Score | Meaning |
|-------|-------|---------|
| Low | 0-1 | Few or no abnormal findings |
| Moderate | 2-4 | Several abnormal findings or patterns |
| High | 5+ | Multiple abnormal findings and patterns |

## Example Output

```json
{
  "report_type": "Health Insights Report",
  "summary": {
    "total_metrics_analyzed": 8,
    "abnormal_metrics": 4,
    "patterns_detected": 2,
    "overall_risk_level": "moderate"
  },
  "patterns": [
    {
      "pattern": "metabolic_concern",
      "markers": ["glucose", "triglycerides"],
      "description": "Elevated glucose and triglycerides may indicate metabolic concerns"
    }
  ],
  "risk_assessment": {
    "risk_score": 4,
    "risk_level": "moderate"
  },
  "disclaimer": "MEDICAL DISCLAIMER: This report provides educational information only..."
}
```

## Plain Language Explanations

The agent generates readable explanations:

```
Glucose: 125 mg/dL
"Your glucose level (125 mg/dL) is above the normal range (70-100 mg/dL). 
This may indicate your body is having difficulty regulating blood sugar."

HDL Cholesterol: 35 mg/dL
"Your HDL cholesterol is low. HDL is often called 'good cholesterol' 
and helps remove other forms of cholesterol from your arteries."
```

## Key Features

✓ **Educational Focus** - Explains findings in plain language
✓ **No Diagnosis** - Never provides medical diagnosis
✓ **Pattern Detection** - Identifies multi-marker concerns
✓ **Risk Assessment** - Scores overall health risk
✓ **Structured Output** - JSON reports for integration
✓ **Medical Disclaimer** - Always included in reports
✓ **Reference Ranges** - Based on clinical standards
✓ **Unit Normalization** - Handles different unit formats

## Important Reminders

⚠️ **This is NOT a medical diagnosis tool**
⚠️ **Always consult healthcare professionals**
⚠️ **For medical advice, see your doctor**
⚠️ **This provides educational information only**

## Workflow Example

```python
from health_insights_agent import (
    lab_metric_extractor,
    clinical_reference_lookup,
    abnormal_flag_detector,
    pattern_detector,
    risk_scorer,
    report_builder
)

# 1. Extract metrics
metrics = lab_metric_extractor(report_text)['metrics']

# 2. Check each metric
abnormal_flags = []
for metric_name, data in metrics.items():
    ref = clinical_reference_lookup(metric_name)['reference_range']
    flag = abnormal_flag_detector(metric_name, data['value'], ref)
    abnormal_flags.append(flag)

# 3. Detect patterns
patterns = pattern_detector(metrics)['patterns']

# 4. Score risk
risk = risk_scorer(abnormal_flags, patterns)

# 5. Build report
report = report_builder(metrics, abnormal_flags, patterns, risk)['report']
```

## Troubleshooting

### Metric Not Recognized
- Check spelling and capitalization
- Verify metric is in supported list
- Add custom metric to reference ranges

### Unit Not Normalized
- Check unit format
- Add conversion to unit_normalizer
- Use standard units (mg/dL, g/dL, U/L)

### Reference Range Not Found
- Metric may not be in database
- Add to clinical_reference_lookup
- Provide gender for gender-specific ranges

## Next Steps

1. Run the demo: `python health_insights_demo.py`
2. Review the full documentation: `HEALTH_INSIGHTS_README.md`
3. Integrate with your application
4. Customize reference ranges as needed
5. Add additional metrics or patterns

## Support

For questions or issues:
- Check the demo script for examples
- Review the main agent file for tool details
- Consult healthcare professionals for medical questions
- See Strands SDK documentation for integration help
