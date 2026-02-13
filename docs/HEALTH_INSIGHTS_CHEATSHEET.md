# Health Insights Agent - Quick Reference Card

## 🚀 Get Started in 30 Seconds

```bash
# 1. Install
pip install -r health_insights_requirements.txt

# 2. Run demo
python health_insights_demo.py

# 3. Use agent
python -c "
from health_insights_agent import create_health_insights_agent
agent = create_health_insights_agent()
result = agent.run('Analyze: Glucose 125 mg/dL, Cholesterol 220 mg/dL')
print(result)
"
```

---

## 📊 Supported Metrics

| Metric | Normal | Unit |
|--------|--------|------|
| Glucose | 70-100 | mg/dL |
| Total Cholesterol | <200 | mg/dL |
| LDL | <100 | mg/dL |
| HDL | >40 | mg/dL |
| Triglycerides | <150 | mg/dL |
| Hemoglobin (M) | 13.5-17.5 | g/dL |
| Hemoglobin (F) | 12.0-15.5 | g/dL |
| ALT | 7-56 | U/L |
| AST | 10-40 | U/L |
| Creatinine (M) | 0.7-1.3 | mg/dL |
| Creatinine (F) | 0.6-1.1 | mg/dL |
| BUN | 7-20 | mg/dL |

---

## 🔍 Detected Patterns

| Pattern | Triggers | Risk |
|---------|----------|------|
| Metabolic | Glucose ↑ + Triglycerides ↑ | Moderate |
| Lipid | Cholesterol ↑ + HDL ↓ | Moderate |
| Liver | ALT ↑ + AST ↑ | Moderate |
| Kidney | Creatinine ↑ + BUN ↑ | Moderate |

---

## 📈 Risk Scoring

| Score | Level | Meaning |
|-------|-------|---------|
| 0-1 | Low | Few abnormalities |
| 2-4 | Moderate | Several abnormalities |
| 5+ | High | Multiple abnormalities |

---

## 🛠️ 10 Tools

```
1. pdf_processor           - Extract text
2. text_cleaner            - Clean text
3. lab_metric_extractor    - Parse values
4. unit_normalizer         - Standardize units
5. clinical_reference_lookup - Get ranges
6. abnormal_flag_detector  - Flag abnormalities
7. pattern_detector        - Find patterns
8. risk_scorer             - Score risk
9. plain_language_explainer - Explain findings
10. report_builder         - Build report
```

---

## 💻 Code Examples

### Basic Usage
```python
from health_insights_agent import create_health_insights_agent

agent = create_health_insights_agent()
result = agent.run("Analyze this report: ...")
```

### Extract Metrics
```python
from health_insights_agent import lab_metric_extractor

metrics = lab_metric_extractor("Glucose: 125 mg/dL")
print(metrics['metrics'])
```

### Check Reference Range
```python
from health_insights_agent import clinical_reference_lookup

ref = clinical_reference_lookup("glucose", gender="male")
print(ref['reference_range'])
```

### Flag Abnormal
```python
from health_insights_agent import abnormal_flag_detector

flag = abnormal_flag_detector("glucose", 125, {"min": 70, "max": 100})
print(flag['is_abnormal'])  # True
print(flag['severity'])     # high
```

### Detect Patterns
```python
from health_insights_agent import pattern_detector

metrics = {"glucose": {"value": 125}, "triglycerides": {"value": 180}}
patterns = pattern_detector(metrics)
print(patterns['patterns'])
```

### Score Risk
```python
from health_insights_agent import risk_scorer

risk = risk_scorer(abnormal_flags, patterns)
print(risk['risk_level'])  # moderate
```

### Build Report
```python
from health_insights_agent import report_builder

report = report_builder(metrics, abnormal_flags, patterns, risk)
print(report['report'])
```

---

## 📋 Report Output

```json
{
  "report_type": "Health Insights Report",
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

---

## 🔧 Customize

### Add Metric
```python
# In clinical_reference_lookup()
"new_metric": {
    "normal": {"min": X, "max": Y, "unit": "Z"}
}

# In plain_language_explainer()
"new_metric": {
    "high": "Explanation...",
    "low": "Explanation...",
    "normal": "Explanation..."
}
```

### Add Pattern
```python
# In pattern_detector()
if ("metric1" in metrics and metrics["metric1"]["value"] > threshold and
    "metric2" in metrics and metrics["metric2"]["value"] > threshold):
    patterns.append({
        "pattern": "new_pattern",
        "markers": ["metric1", "metric2"],
        "description": "Description..."
    })
```

---

## 🌐 Integration

### Flask API
```python
@app.route('/analyze', methods=['POST'])
def analyze():
    report = request.json['report']
    result = agent.run(f"Analyze: {report}")
    return jsonify(result)
```

### Streamlit
```python
import streamlit as st
report = st.text_area("Paste report:")
if st.button("Analyze"):
    result = agent.run(f"Analyze: {report}")
    st.json(result)
```

### Batch Processing
```python
for report in reports:
    result = agent.run(f"Analyze: {report}")
    save_result(result)
```

---

## ⚠️ Important

- ✅ Educational information only
- ✅ Not a medical diagnosis tool
- ✅ Always consult healthcare professionals
- ✅ Medical disclaimer in every report
- ✅ No treatment recommendations

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| HEALTH_INSIGHTS_INDEX.md | Navigation guide |
| HEALTH_INSIGHTS_QUICK_START.md | 5-minute start |
| HEALTH_INSIGHTS_README.md | Full documentation |
| HEALTH_INSIGHTS_ARCHITECTURE.md | System design |
| HEALTH_INSIGHTS_EXAMPLES.md | Usage examples |
| HEALTH_INSIGHTS_SUMMARY.md | Project overview |

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Metric not recognized | Add to `clinical_reference_lookup()` |
| Unit not normalized | Add to `unit_normalizer()` |
| Reference range missing | Add to `clinical_reference_lookup()` |
| Pattern not detected | Add to `pattern_detector()` |

---

## 📞 Quick Links

- **Start**: `HEALTH_INSIGHTS_QUICK_START.md`
- **Docs**: `HEALTH_INSIGHTS_README.md`
- **Design**: `HEALTH_INSIGHTS_ARCHITECTURE.md`
- **Examples**: `HEALTH_INSIGHTS_EXAMPLES.md`
- **Demo**: `python health_insights_demo.py`

---

## 🎯 Common Tasks

```bash
# Run demo
python health_insights_demo.py

# Install dependencies
pip install -r health_insights_requirements.txt

# View agent code
cat health_insights_agent.py

# Read documentation
cat HEALTH_INSIGHTS_README.md
```

---

## 📊 Metrics at a Glance

```
Glucose:        70-100 mg/dL
Cholesterol:    <200 mg/dL
LDL:            <100 mg/dL
HDL:            >40 mg/dL
Triglycerides:  <150 mg/dL
Hemoglobin:     13.5-17.5 g/dL (M), 12.0-15.5 g/dL (F)
ALT:            7-56 U/L
AST:            10-40 U/L
Creatinine:     0.7-1.3 mg/dL (M), 0.6-1.1 mg/dL (F)
BUN:            7-20 mg/dL
```

---

## 🚀 Next Steps

1. Run: `python health_insights_demo.py`
2. Read: `HEALTH_INSIGHTS_QUICK_START.md`
3. Explore: `HEALTH_INSIGHTS_EXAMPLES.md`
4. Integrate: Build your app
5. Customize: Add metrics/patterns

---

**Version**: 1.0 | **Status**: Production Ready | **Created**: Feb 5, 2024
