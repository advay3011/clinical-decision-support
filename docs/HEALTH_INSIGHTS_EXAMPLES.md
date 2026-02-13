# Health Insights Agent - Usage Examples

## Example 1: Basic Lab Report Analysis

### Input Report
```
LABORATORY TEST RESULTS
Date: 2024-02-05
Patient: John Doe, Male, 45 years old

METABOLIC PANEL:
Fasting Glucose: 110 mg/dL
Total Cholesterol: 210 mg/dL
LDL Cholesterol: 140 mg/dL
HDL Cholesterol: 38 mg/dL
Triglycerides: 160 mg/dL

COMPLETE BLOOD COUNT:
Hemoglobin: 14.5 g/dL

LIVER FUNCTION:
ALT: 32 U/L
AST: 28 U/L

KIDNEY FUNCTION:
Creatinine: 0.9 mg/dL
BUN: 16 mg/dL
```

### Processing Steps

```python
from health_insights_agent import (
    lab_metric_extractor,
    clinical_reference_lookup,
    abnormal_flag_detector,
    pattern_detector,
    risk_scorer,
    report_builder
)

# Step 1: Extract metrics
metrics = {
    "glucose": {"value": 110, "unit": "mg/dL"},
    "cholesterol": {"value": 210, "unit": "mg/dL"},
    "ldl": {"value": 140, "unit": "mg/dL"},
    "hdl": {"value": 38, "unit": "mg/dL"},
    "triglycerides": {"value": 160, "unit": "mg/dL"},
    "hemoglobin": {"value": 14.5, "unit": "g/dL"},
    "alt": {"value": 32, "unit": "U/L"},
    "ast": {"value": 28, "unit": "U/L"},
    "creatinine": {"value": 0.9, "unit": "mg/dL"},
    "bun": {"value": 16, "unit": "mg/dL"}
}

# Step 2: Check each metric
abnormal_flags = []
for metric_name, data in metrics.items():
    ref = clinical_reference_lookup(metric_name, gender="male")
    if ref['status'] == 'success':
        flag = abnormal_flag_detector(
            metric_name,
            data['value'],
            ref['reference_range']
        )
        abnormal_flags.append(flag)

# Step 3: Detect patterns
patterns = pattern_detector(metrics)['patterns']

# Step 4: Score risk
risk = risk_scorer(abnormal_flags, patterns)

# Step 5: Build report
report = report_builder(metrics, abnormal_flags, patterns, risk)
```

### Output Report

```json
{
  "report_type": "Health Insights Report",
  "generated_at": "2024-02-05T10:30:00",
  "disclaimer": "MEDICAL DISCLAIMER: This report provides educational information only...",
  "summary": {
    "total_metrics_analyzed": 10,
    "abnormal_metrics": 4,
    "patterns_detected": 1,
    "overall_risk_level": "moderate"
  },
  "metrics_analysis": {
    "normal": [
      {
        "metric": "hemoglobin",
        "value": 14.5,
        "severity": "normal",
        "reference_range": {"min": 13.5, "max": 17.5, "unit": "g/dL"}
      },
      {
        "metric": "alt",
        "value": 32,
        "severity": "normal",
        "reference_range": {"min": 7, "max": 56, "unit": "U/L"}
      }
    ],
    "abnormal": [
      {
        "metric": "glucose",
        "value": 110,
        "severity": "high",
        "direction": "above",
        "reference_range": {"min": 70, "max": 100, "unit": "mg/dL"}
      },
      {
        "metric": "cholesterol",
        "value": 210,
        "severity": "high",
        "direction": "above",
        "reference_range": {"min": 0, "max": 200, "unit": "mg/dL"}
      },
      {
        "metric": "hdl",
        "value": 38,
        "severity": "low",
        "direction": "below",
        "reference_range": {"min": 40, "max": 999, "unit": "mg/dL"}
      },
      {
        "metric": "triglycerides",
        "value": 160,
        "severity": "high",
        "direction": "above",
        "reference_range": {"min": 0, "max": 150, "unit": "mg/dL"}
      }
    ]
  },
  "patterns": [
    {
      "pattern": "metabolic_concern",
      "markers": ["glucose", "triglycerides"],
      "description": "Elevated glucose and triglycerides may indicate metabolic concerns"
    },
    {
      "pattern": "lipid_concern",
      "markers": ["cholesterol", "hdl"],
      "description": "Lipid profile shows potential cardiovascular risk markers"
    }
  ],
  "risk_assessment": {
    "risk_score": 6,
    "risk_level": "high",
    "abnormal_count": 4,
    "pattern_count": 2
  },
  "recommendations": [
    "Consult with your healthcare provider to discuss these results",
    "Consider lifestyle modifications if recommended by your doctor",
    "Schedule follow-up testing as advised by your healthcare team",
    "Maintain a healthy diet and regular exercise routine"
  ]
}
```

### Plain Language Explanations

```
GLUCOSE: 110 mg/dL
"Your glucose level (110 mg/dL) is above the normal range (70-100 mg/dL). 
This may indicate your body is having difficulty regulating blood sugar."

CHOLESTEROL: 210 mg/dL
"Your total cholesterol (210 mg/dL) is above 200 mg/dL. Higher levels may 
increase cardiovascular risk."

HDL CHOLESTEROL: 38 mg/dL
"Your HDL cholesterol is low. HDL is often called 'good cholesterol' and 
helps remove other forms of cholesterol from your arteries."

TRIGLYCERIDES: 160 mg/dL
"Your triglycerides (160 mg/dL) are elevated. High triglycerides combined 
with other lipid abnormalities may increase cardiovascular risk."

METABOLIC CONCERN PATTERN:
"Your glucose and triglycerides are both elevated. This combination may 
indicate metabolic dysfunction. Discuss with your healthcare provider."
```

---

## Example 2: Healthy Lab Results

### Input Report
```
LABORATORY TEST RESULTS
Date: 2024-02-05
Patient: Jane Smith, Female, 35 years old

Fasting Glucose: 92 mg/dL
Total Cholesterol: 180 mg/dL
LDL Cholesterol: 110 mg/dL
HDL Cholesterol: 55 mg/dL
Triglycerides: 100 mg/dL
Hemoglobin: 13.5 g/dL
ALT: 25 U/L
AST: 22 U/L
Creatinine: 0.8 mg/dL
BUN: 15 mg/dL
```

### Output Summary

```json
{
  "summary": {
    "total_metrics_analyzed": 10,
    "abnormal_metrics": 0,
    "patterns_detected": 0,
    "overall_risk_level": "low"
  },
  "risk_assessment": {
    "risk_score": 0,
    "risk_level": "low"
  },
  "recommendations": [
    "Maintain current healthy lifestyle",
    "Continue regular health check-ups",
    "Follow recommended screening guidelines",
    "Maintain balanced diet and exercise routine"
  ]
}
```

---

## Example 3: Liver Function Concern

### Input Report
```
LABORATORY TEST RESULTS
Date: 2024-02-05

ALT: 95 U/L
AST: 78 U/L
Bilirubin: 1.8 mg/dL
Albumin: 3.2 g/dL
```

### Analysis

```
ABNORMAL FINDINGS:
- ALT: 95 U/L (Normal: 7-56 U/L) - HIGH
- AST: 78 U/L (Normal: 10-40 U/L) - HIGH

PATTERN DETECTED: LIVER CONCERN
"Elevated liver enzymes (ALT and AST) may indicate liver stress or damage. 
This pattern requires medical evaluation."

RISK LEVEL: MODERATE
"Multiple liver function markers are abnormal. Consult your healthcare 
provider for further evaluation."
```

---

## Example 4: Kidney Function Concern

### Input Report
```
LABORATORY TEST RESULTS
Date: 2024-02-05
Patient: Male, 60 years old

Creatinine: 1.6 mg/dL
BUN: 28 mg/dL
eGFR: 42 mL/min/1.73m2
```

### Analysis

```
ABNORMAL FINDINGS:
- Creatinine: 1.6 mg/dL (Normal: 0.7-1.3 mg/dL) - HIGH
- BUN: 28 mg/dL (Normal: 7-20 mg/dL) - HIGH

PATTERN DETECTED: KIDNEY CONCERN
"Elevated kidney markers (creatinine and BUN) may indicate reduced kidney 
function. This requires medical evaluation."

RISK LEVEL: MODERATE
"Your kidney function markers are elevated. Discuss with your healthcare 
provider about next steps."
```

---

## Example 5: Anemia Detection

### Input Report
```
LABORATORY TEST RESULTS
Date: 2024-02-05
Patient: Female, 28 years old

Hemoglobin: 10.2 g/dL
Hematocrit: 31%
Red Blood Cell Count: 3.8 million/μL
Mean Corpuscular Volume: 78 fL
```

### Analysis

```
ABNORMAL FINDINGS:
- Hemoglobin: 10.2 g/dL (Normal: 12.0-15.5 g/dL) - LOW

EXPLANATION:
"Your hemoglobin (10.2 g/dL) is below the normal range. This may indicate 
anemia or reduced oxygen-carrying capacity in your blood."

RISK LEVEL: MODERATE
"Low hemoglobin may cause fatigue and reduced oxygen delivery to tissues. 
Consult your healthcare provider for evaluation."
```

---

## Example 6: Multiple Abnormalities

### Input Report
```
LABORATORY TEST RESULTS
Date: 2024-02-05
Patient: Male, 55 years old

Glucose: 185 mg/dL
Total Cholesterol: 280 mg/dL
LDL: 200 mg/dL
HDL: 28 mg/dL
Triglycerides: 320 mg/dL
Hemoglobin: 10.5 g/dL
ALT: 120 U/L
AST: 95 U/L
Creatinine: 2.1 mg/dL
BUN: 35 mg/dL
```

### Output Summary

```json
{
  "summary": {
    "total_metrics_analyzed": 10,
    "abnormal_metrics": 10,
    "patterns_detected": 4,
    "overall_risk_level": "high"
  },
  "patterns": [
    {
      "pattern": "metabolic_concern",
      "markers": ["glucose", "triglycerides"]
    },
    {
      "pattern": "lipid_concern",
      "markers": ["cholesterol", "hdl"]
    },
    {
      "pattern": "liver_concern",
      "markers": ["alt", "ast"]
    },
    {
      "pattern": "kidney_concern",
      "markers": ["creatinine", "bun"]
    }
  ],
  "risk_assessment": {
    "risk_score": 12,
    "risk_level": "high"
  }
}
```

### Critical Recommendations

```
⚠️ IMPORTANT: Multiple abnormal findings detected

This report shows multiple concerning patterns across different organ systems:
- Metabolic dysfunction (glucose and triglycerides)
- Lipid abnormalities (cholesterol and HDL)
- Liver function concerns (ALT and AST)
- Kidney function concerns (creatinine and BUN)

IMMEDIATE ACTION REQUIRED:
1. Schedule urgent appointment with healthcare provider
2. Bring this report to your doctor
3. Do not delay medical evaluation
4. Follow all medical recommendations

This is NOT a diagnosis. Only your healthcare provider can diagnose 
and recommend treatment.
```

---

## Example 7: Thyroid Function Analysis

### Input Report
```
LABORATORY TEST RESULTS
Date: 2024-02-05
Patient: Female, 42 years old

TSH: 8.5 mIU/L
Free T4: 0.8 ng/dL
Free T3: 2.1 pg/mL
```

### Analysis

```
ABNORMAL FINDINGS:
- TSH: 8.5 mIU/L (Normal: 0.4-4.0 mIU/L) - HIGH
- Free T4: 0.8 ng/dL (Normal: 0.8-1.8 ng/dL) - LOW

PATTERN: HYPOTHYROIDISM INDICATORS
"Elevated TSH with low Free T4 may indicate hypothyroidism (underactive 
thyroid). This pattern requires medical evaluation."

SYMPTOMS TO DISCUSS WITH DOCTOR:
- Fatigue
- Weight gain
- Cold sensitivity
- Dry skin
- Hair loss

NEXT STEPS:
"Consult your healthcare provider for thyroid evaluation and possible 
treatment options."
```

---

## Example 8: Lipid Panel Optimization

### Input Report
```
LABORATORY TEST RESULTS
Date: 2024-02-05
Patient: Male, 50 years old

Total Cholesterol: 195 mg/dL
LDL Cholesterol: 115 mg/dL
HDL Cholesterol: 45 mg/dL
Triglycerides: 140 mg/dL
```

### Analysis

```
FINDINGS:
- Total Cholesterol: 195 mg/dL (Optimal: <200) - NORMAL
- LDL Cholesterol: 115 mg/dL (Optimal: <100) - BORDERLINE
- HDL Cholesterol: 45 mg/dL (Optimal: >40) - ACCEPTABLE
- Triglycerides: 140 mg/dL (Normal: <150) - NORMAL

OVERALL ASSESSMENT:
"Your lipid profile is generally acceptable but could be optimized. 
LDL cholesterol is slightly elevated and HDL could be higher."

RECOMMENDATIONS:
1. Increase physical activity
2. Reduce saturated fat intake
3. Increase fiber consumption
4. Consider heart-healthy diet (Mediterranean, DASH)
5. Recheck in 3-6 months

RISK LEVEL: LOW
"Your lipid profile shows low cardiovascular risk, but optimization 
could further reduce risk."
```

---

## Integration Example: Web API

```python
from flask import Flask, request, jsonify
from health_insights_agent import create_health_insights_agent

app = Flask(__name__)
agent = create_health_insights_agent()

@app.route('/analyze', methods=['POST'])
def analyze_report():
    """API endpoint for health report analysis"""
    
    data = request.json
    report_text = data.get('report')
    gender = data.get('gender', 'general')
    
    if not report_text:
        return jsonify({"error": "No report provided"}), 400
    
    try:
        # Run analysis
        result = agent.run(f"""
        Analyze this medical report (patient gender: {gender}):
        
        {report_text}
        
        Provide a comprehensive health insights report.
        """)
        
        return jsonify({
            "status": "success",
            "report": result
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Integration Example: Streamlit App

```python
import streamlit as st
from health_insights_agent import create_health_insights_agent

st.set_page_config(page_title="Health Insights", layout="wide")

st.title("Health Insights Agent")
st.markdown("📋 Educational health analysis tool")

# Medical disclaimer
st.warning("""
⚠️ **MEDICAL DISCLAIMER**: This tool provides educational information only 
and is NOT a medical diagnosis tool. Always consult with healthcare professionals.
""")

# Input section
col1, col2 = st.columns([2, 1])

with col1:
    report_text = st.text_area(
        "Paste your lab report:",
        height=300,
        placeholder="LABORATORY TEST RESULTS\nGlucose: 125 mg/dL\n..."
    )

with col2:
    gender = st.selectbox("Gender (for reference ranges):", 
                         ["General", "Male", "Female"])

# Analysis button
if st.button("Analyze Report", type="primary"):
    if report_text:
        with st.spinner("Analyzing..."):
            agent = create_health_insights_agent()
            result = agent.run(f"Analyze this report: {report_text}")
            
            # Display results
            st.success("Analysis complete!")
            st.json(result)
    else:
        st.error("Please paste a lab report")
```

---

## Batch Processing Example

```python
import json
from health_insights_agent import create_health_insights_agent

def batch_analyze_reports(reports_file):
    """Analyze multiple reports from a JSON file"""
    
    agent = create_health_insights_agent()
    
    with open(reports_file, 'r') as f:
        reports = json.load(f)
    
    results = []
    
    for i, report in enumerate(reports, 1):
        print(f"Processing report {i}/{len(reports)}...")
        
        result = agent.run(f"Analyze: {report['text']}")
        
        results.append({
            "patient_id": report.get('id'),
            "analysis": result
        })
    
    # Save results
    with open('analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Processed {len(results)} reports")

# Usage
batch_analyze_reports('reports.json')
```

These examples demonstrate the agent's versatility across different scenarios and integration patterns.
