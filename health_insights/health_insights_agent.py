"""
Health Insights Agent - Educational Health Analysis Tool
Reads medical reports, extracts lab values, analyzes patterns, and generates insights.
DISCLAIMER: This tool provides educational information only and is NOT a medical diagnosis.
Always consult with healthcare professionals for medical advice.
"""

import json
import re
from typing import Any
from datetime import datetime

# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

def pdf_processor(pdf_content: str) -> dict:
    """Extract text from PDF content"""
    return {
        "status": "success",
        "extracted_text": pdf_content,
        "extraction_timestamp": datetime.now().isoformat()
    }


def text_cleaner(raw_text: str) -> dict:
    """Clean and normalize extracted text"""
    cleaned = re.sub(r'\s+', ' ', raw_text).strip()
    # Keep colons, they're important for parsing
    cleaned = re.sub(r'[^\w\s\.\,\:\-\(\)\/]', '', cleaned)
    return {
        "status": "success",
        "cleaned_text": cleaned,
        "lines": cleaned.split('.')
    }


def lab_metric_extractor(text: str) -> dict:
    """Extract lab metrics and values from text"""
    metrics = {}
    
    # Pattern: metric_name: value unit
    pattern = r'([A-Za-z\s]+?):\s*([\d\.]+)\s*([A-Za-z/%]*)'
    matches = re.findall(pattern, text)
    
    # Keywords to skip (not actual metrics)
    skip_keywords = ['date', 'patient', 'age', 'gender', 'time', 'result', 'test', 'laboratory']
    
    for metric_name, value, unit in matches:
        metric_name = metric_name.strip()
        metric_lower = metric_name.lower()
        
        # Skip non-metric entries
        if any(skip in metric_lower for skip in skip_keywords):
            continue
        
        try:
            metrics[metric_name] = {
                "value": float(value),
                "unit": unit.strip() if unit else "unknown",
                "raw": f"{value} {unit}"
            }
        except ValueError:
            continue
    
    return {
        "status": "success",
        "metrics_found": len(metrics),
        "metrics": metrics
    }


def unit_normalizer(metrics: dict) -> dict:
    """Normalize units to standard forms"""
    unit_conversions = {
        "mg/dL": {"glucose": 1, "cholesterol": 1},
        "mmol/L": {"glucose": 0.0555, "cholesterol": 0.0259},
        "g/dL": {"hemoglobin": 1},
        "g/L": {"hemoglobin": 10},
        "IU/L": {"alt": 1, "ast": 1},
        "U/L": {"alt": 1, "ast": 1},
    }
    
    normalized = {}
    for metric_name, data in metrics.items():
        normalized[metric_name] = {
            "original_value": data["value"],
            "original_unit": data["unit"],
            "normalized_value": data["value"],
            "normalized_unit": data["unit"],
            "conversion_applied": False
        }
    
    return {
        "status": "success",
        "normalized_metrics": normalized
    }


def clinical_reference_lookup(metric_name: str, gender: str = "general") -> dict:
    """Look up clinical reference ranges"""
    reference_ranges = {
        "glucose": {
            "normal": {"min": 70, "max": 100, "unit": "mg/dL"},
            "fasting": {"min": 70, "max": 100, "unit": "mg/dL"},
            "postprandial": {"min": 70, "max": 140, "unit": "mg/dL"}
        },
        "hemoglobin": {
            "male": {"min": 13.5, "max": 17.5, "unit": "g/dL"},
            "female": {"min": 12.0, "max": 15.5, "unit": "g/dL"}
        },
        "cholesterol": {
            "total": {"min": 0, "max": 200, "unit": "mg/dL", "optimal": True},
            "ldl": {"min": 0, "max": 100, "unit": "mg/dL", "optimal": True},
            "hdl": {"min": 40, "max": 999, "unit": "mg/dL", "optimal": True}
        },
        "triglycerides": {
            "normal": {"min": 0, "max": 150, "unit": "mg/dL"}
        },
        "alt": {
            "normal": {"min": 7, "max": 56, "unit": "U/L"}
        },
        "ast": {
            "normal": {"min": 10, "max": 40, "unit": "U/L"}
        },
        "creatinine": {
            "male": {"min": 0.7, "max": 1.3, "unit": "mg/dL"},
            "female": {"min": 0.6, "max": 1.1, "unit": "mg/dL"}
        },
        "bun": {
            "normal": {"min": 7, "max": 20, "unit": "mg/dL"}
        }
    }
    
    metric_lower = metric_name.lower()
    
    # Handle variations in metric names
    metric_map = {
        "fasting glucose": "glucose",
        "total cholesterol": "cholesterol",
        "ldl cholesterol": "ldl",
        "hdl cholesterol": "hdl",
        "ldl": "cholesterol",
        "hdl": "cholesterol",
        "total": "cholesterol"
    }
    
    # Check if it's a mapped metric
    if metric_lower in metric_map:
        metric_lower = metric_map[metric_lower]
    
    if metric_lower in reference_ranges:
        ranges = reference_ranges[metric_lower]
        if gender in ranges:
            return {"status": "success", "reference_range": ranges[gender]}
        elif "normal" in ranges:
            return {"status": "success", "reference_range": ranges["normal"]}
    
    return {"status": "not_found", "reference_range": None}


def abnormal_flag_detector(metric_name: str, value: float, reference_range: dict) -> dict:
    """Detect abnormal values"""
    is_abnormal = False
    severity = "normal"
    direction = None
    
    if value < reference_range["min"]:
        is_abnormal = True
        severity = "low"
        direction = "below"
    elif value > reference_range["max"]:
        is_abnormal = True
        severity = "high"
        direction = "above"
    
    return {
        "status": "success",
        "metric": metric_name,
        "value": value,
        "is_abnormal": is_abnormal,
        "severity": severity,
        "direction": direction,
        "reference_range": reference_range
    }


def pattern_detector(metrics: dict) -> dict:
    """Detect multi-marker risk patterns"""
    patterns = []
    
    # Metabolic syndrome pattern
    if ("glucose" in metrics and metrics["glucose"]["value"] > 100 and
        "triglycerides" in metrics and metrics["triglycerides"]["value"] > 150):
        patterns.append({
            "pattern": "metabolic_concern",
            "markers": ["glucose", "triglycerides"],
            "description": "Elevated glucose and triglycerides may indicate metabolic concerns"
        })
    
    # Lipid profile concern
    if ("cholesterol" in metrics and metrics["cholesterol"]["value"] > 200 and
        "hdl" in metrics and metrics["hdl"]["value"] < 40):
        patterns.append({
            "pattern": "lipid_concern",
            "markers": ["cholesterol", "hdl"],
            "description": "Lipid profile shows potential cardiovascular risk markers"
        })
    
    # Liver function concern
    if ("alt" in metrics and metrics["alt"]["value"] > 56 and
        "ast" in metrics and metrics["ast"]["value"] > 40):
        patterns.append({
            "pattern": "liver_concern",
            "markers": ["alt", "ast"],
            "description": "Elevated liver enzymes may indicate liver stress"
        })
    
    # Kidney function concern
    if ("creatinine" in metrics and metrics["creatinine"]["value"] > 1.3 and
        "bun" in metrics and metrics["bun"]["value"] > 20):
        patterns.append({
            "pattern": "kidney_concern",
            "markers": ["creatinine", "bun"],
            "description": "Elevated kidney markers may indicate kidney function concerns"
        })
    
    return {
        "status": "success",
        "patterns_detected": len(patterns),
        "patterns": patterns
    }


def risk_scorer(abnormal_metrics: list, patterns: list) -> dict:
    """Assign risk severity score"""
    score = 0
    risk_level = "low"
    
    # Score abnormal metrics
    for metric in abnormal_metrics:
        if metric["severity"] == "high" or metric["severity"] == "low":
            score += 1
    
    # Score patterns
    score += len(patterns) * 2
    
    if score >= 5:
        risk_level = "high"
    elif score >= 2:
        risk_level = "moderate"
    else:
        risk_level = "low"
    
    return {
        "status": "success",
        "risk_score": score,
        "risk_level": risk_level,
        "abnormal_count": len(abnormal_metrics),
        "pattern_count": len(patterns)
    }


def plain_language_explainer(metric_name: str, value: float, 
                            reference_range: dict, severity: str) -> dict:
    """Generate plain language explanations"""
    explanations = {
        "glucose": {
            "high": f"Your glucose level ({value} mg/dL) is above the normal range (70-100 mg/dL). This may indicate your body is having difficulty regulating blood sugar.",
            "low": f"Your glucose level ({value} mg/dL) is below the normal range. This may indicate low blood sugar.",
            "normal": f"Your glucose level ({value} mg/dL) is within normal range."
        },
        "hemoglobin": {
            "high": f"Your hemoglobin ({value} g/dL) is elevated, which may indicate dehydration or other conditions.",
            "low": f"Your hemoglobin ({value} g/dL) is low, which may indicate anemia or reduced oxygen-carrying capacity.",
            "normal": f"Your hemoglobin ({value} g/dL) is normal."
        },
        "cholesterol": {
            "high": f"Your total cholesterol ({value} mg/dL) is above 200 mg/dL. Higher levels may increase cardiovascular risk.",
            "low": f"Your cholesterol is low.",
            "normal": f"Your cholesterol ({value} mg/dL) is at a healthy level."
        }
    }
    
    metric_lower = metric_name.lower()
    if metric_lower in explanations and severity in explanations[metric_lower]:
        return {
            "status": "success",
            "metric": metric_name,
            "explanation": explanations[metric_lower][severity]
        }
    
    return {
        "status": "success",
        "metric": metric_name,
        "explanation": f"{metric_name} value is {severity}."
    }


def report_builder(metrics: dict, abnormal_flags: list, patterns: list, 
                  risk_score: dict) -> dict:
    """Build structured health insight report"""
    report = {
        "report_type": "Health Insights Report",
        "generated_at": datetime.now().isoformat(),
        "disclaimer": "MEDICAL DISCLAIMER: This report provides educational information only and is NOT a medical diagnosis. Always consult with qualified healthcare professionals for medical advice, diagnosis, or treatment.",
        "summary": {
            "total_metrics_analyzed": len(metrics),
            "abnormal_metrics": len(abnormal_flags),
            "patterns_detected": len(patterns),
            "overall_risk_level": risk_score.get("risk_level", "unknown")
        },
        "metrics_analysis": {
            "normal": [m for m in abnormal_flags if m["severity"] == "normal"],
            "abnormal": [m for m in abnormal_flags if m["severity"] != "normal"]
        },
        "patterns": patterns,
        "risk_assessment": risk_score,
        "recommendations": [
            "Consult with your healthcare provider to discuss these results",
            "Consider lifestyle modifications if recommended by your doctor",
            "Schedule follow-up testing as advised by your healthcare team",
            "Maintain a healthy diet and regular exercise routine"
        ]
    }
    
    return {
        "status": "success",
        "report": report
    }


# ============================================================================
# AGENT DEFINITION (Simplified for standalone use)
# ============================================================================

class HealthInsightsAgent:
    """Simplified Health Insights Agent for standalone use"""
    
    def __init__(self):
        self.name = "Health Insights Agent"
        self.description = "Analyzes medical reports and lab tests to provide educational health insights"
    
    def run(self, report_text: str, gender: str = "general") -> dict:
        """Run complete analysis on a medical report"""
        
        # Step 1: Process text
        clean_result = text_cleaner(report_text)
        cleaned_text = clean_result['cleaned_text']
        
        # Step 2: Extract metrics
        extract_result = lab_metric_extractor(cleaned_text)
        metrics = extract_result['metrics']
        
        # Step 3: Normalize units
        normalize_result = unit_normalizer(metrics)
        normalized_metrics = normalize_result['normalized_metrics']
        
        # Step 4: Check references and flag abnormals
        abnormal_flags = []
        for metric_name, data in metrics.items():
            ref_result = clinical_reference_lookup(metric_name, gender=gender)
            
            if ref_result['status'] == 'success' and ref_result['reference_range']:
                ref_range = ref_result['reference_range']
                flag_result = abnormal_flag_detector(
                    metric_name,
                    data['value'],
                    ref_range
                )
                abnormal_flags.append(flag_result)
        
        # Step 5: Detect patterns
        pattern_result = pattern_detector(metrics)
        patterns = pattern_result['patterns']
        
        # Step 6: Score risk
        risk_result = risk_scorer(abnormal_flags, patterns)
        
        # Step 7: Build report
        report_result = report_builder(metrics, abnormal_flags, patterns, risk_result)
        
        return report_result['report']


def create_health_insights_agent():
    """Create and configure the Health Insights Agent"""
    return HealthInsightsAgent()


# ============================================================================
# DEMO USAGE
# ============================================================================

def demo_health_analysis():
    """Demo the Health Insights Agent"""
    
    # Sample medical report data
    sample_report = """
    LABORATORY TEST RESULTS
    Patient: John Doe
    Date: 2024-02-05
    
    METABOLIC PANEL:
    Glucose: 125 mg/dL
    Total Cholesterol: 220 mg/dL
    LDL Cholesterol: 150 mg/dL
    HDL Cholesterol: 35 mg/dL
    Triglycerides: 180 mg/dL
    
    COMPLETE BLOOD COUNT:
    Hemoglobin: 14.2 g/dL
    
    LIVER FUNCTION:
    ALT: 65 U/L
    AST: 48 U/L
    
    KIDNEY FUNCTION:
    Creatinine: 1.4 mg/dL
    BUN: 22 mg/dL
    """
    
    print("=" * 80)
    print("HEALTH INSIGHTS AGENT - DEMO")
    print("=" * 80)
    print("\nSample Medical Report:")
    print(sample_report)
    print("\n" + "=" * 80)
    print("Processing report with Health Insights Agent...")
    print("=" * 80)
    
    # Create agent
    agent = create_health_insights_agent()
    
    # Prepare analysis request
    analysis_request = f"""
    Please analyze the following medical report and provide a comprehensive health insights report:
    
    {sample_report}
    
    Please:
    1. Extract all lab metrics and values
    2. Normalize units to standard forms
    3. Check each value against clinical reference ranges
    4. Flag any abnormal values
    5. Identify multi-marker patterns
    6. Assess overall risk level
    7. Generate plain language explanations
    8. Build a structured health insight report
    
    Remember to include the medical disclaimer and emphasize this is educational only.
    """
    
    # Run agent (in real implementation, would use actual Strands SDK)
    print("\nAgent Analysis Request:")
    print(analysis_request)
    print("\n" + "=" * 80)
    print("Note: In production, this would run through the Strands Agent framework")
    print("=" * 80)


if __name__ == "__main__":
    demo_health_analysis()
