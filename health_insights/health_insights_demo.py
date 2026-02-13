"""
Health Insights Agent - Interactive Demo
Demonstrates the full workflow of analyzing medical reports
"""

import json
from health_insights_agent import (
    pdf_processor, text_cleaner, lab_metric_extractor,
    unit_normalizer, clinical_reference_lookup, abnormal_flag_detector,
    pattern_detector, risk_scorer, plain_language_explainer, report_builder
)


def demo_full_workflow():
    """Run complete health analysis workflow"""
    
    print("\n" + "=" * 80)
    print("HEALTH INSIGHTS AGENT - COMPLETE WORKFLOW DEMO")
    print("=" * 80)
    
    # Step 1: Sample medical report
    print("\n[STEP 1] SAMPLE MEDICAL REPORT")
    print("-" * 80)
    
    sample_report = """
    LABORATORY TEST RESULTS
    Patient: Jane Smith
    Date: 2024-02-05
    Gender: Female
    
    METABOLIC PANEL:
    Fasting Glucose: 128 mg/dL
    Total Cholesterol: 245 mg/dL
    LDL Cholesterol: 165 mg/dL
    HDL Cholesterol: 32 mg/dL
    Triglycerides: 195 mg/dL
    
    COMPLETE BLOOD COUNT:
    Hemoglobin: 11.8 g/dL
    
    LIVER FUNCTION TESTS:
    ALT: 72 U/L
    AST: 55 U/L
    
    KIDNEY FUNCTION TESTS:
    Creatinine: 1.5 mg/dL
    BUN: 24 mg/dL
    """
    
    print(sample_report)
    
    # Step 2: Process PDF
    print("\n[STEP 2] PDF PROCESSING")
    print("-" * 80)
    pdf_result = pdf_processor(sample_report)
    print(f"Status: {pdf_result['status']}")
    print(f"Extraction timestamp: {pdf_result['extraction_timestamp']}")
    
    # Step 3: Clean text
    print("\n[STEP 3] TEXT CLEANING")
    print("-" * 80)
    clean_result = text_cleaner(sample_report)
    print(f"Status: {clean_result['status']}")
    print(f"Lines extracted: {len(clean_result['lines'])}")
    
    # Step 4: Extract metrics
    print("\n[STEP 4] LAB METRIC EXTRACTION")
    print("-" * 80)
    extract_result = lab_metric_extractor(sample_report)
    print(f"Status: {extract_result['status']}")
    print(f"Metrics found: {extract_result['metrics_found']}")
    print("\nExtracted Metrics:")
    for metric, data in extract_result['metrics'].items():
        print(f"  {metric}: {data['value']} {data['unit']}")
    
    metrics = extract_result['metrics']
    
    # Step 5: Normalize units
    print("\n[STEP 5] UNIT NORMALIZATION")
    print("-" * 80)
    normalize_result = unit_normalizer(metrics)
    print(f"Status: {normalize_result['status']}")
    print("Normalized metrics:")
    for metric, data in normalize_result['normalized_metrics'].items():
        print(f"  {metric}: {data['normalized_value']} {data['normalized_unit']}")
    
    # Step 6: Check reference ranges and flag abnormals
    print("\n[STEP 6] REFERENCE RANGE LOOKUP & ABNORMAL DETECTION")
    print("-" * 80)
    
    abnormal_flags = []
    for metric_name, metric_data in metrics.items():
        ref_result = clinical_reference_lookup(metric_name, gender="female")
        
        if ref_result['status'] == 'success' and ref_result['reference_range']:
            ref_range = ref_result['reference_range']
            flag_result = abnormal_flag_detector(
                metric_name,
                metric_data['value'],
                ref_range
            )
            abnormal_flags.append(flag_result)
            
            status = "✓ NORMAL" if not flag_result['is_abnormal'] else f"⚠ {flag_result['severity'].upper()}"
            print(f"  {metric_name}: {metric_data['value']} {metric_data['unit']} {status}")
            print(f"    Reference: {ref_range['min']}-{ref_range['max']} {ref_range['unit']}")
    
    # Step 7: Detect patterns
    print("\n[STEP 7] MULTI-MARKER PATTERN DETECTION")
    print("-" * 80)
    pattern_result = pattern_detector(metrics)
    print(f"Patterns detected: {pattern_result['patterns_detected']}")
    for pattern in pattern_result['patterns']:
        print(f"  • {pattern['pattern'].upper()}")
        print(f"    Markers: {', '.join(pattern['markers'])}")
        print(f"    Description: {pattern['description']}")
    
    # Step 8: Risk scoring
    print("\n[STEP 8] RISK SCORING")
    print("-" * 80)
    risk_result = risk_scorer(abnormal_flags, pattern_result['patterns'])
    print(f"Risk Score: {risk_result['risk_score']}")
    print(f"Risk Level: {risk_result['risk_level'].upper()}")
    print(f"Abnormal Metrics: {risk_result['abnormal_count']}")
    print(f"Patterns Detected: {risk_result['pattern_count']}")
    
    # Step 9: Plain language explanations
    print("\n[STEP 9] PLAIN LANGUAGE EXPLANATIONS")
    print("-" * 80)
    for flag in abnormal_flags:
        if flag['is_abnormal']:
            explain_result = plain_language_explainer(
                flag['metric'],
                flag['value'],
                flag['reference_range'],
                flag['severity']
            )
            print(f"\n{flag['metric']}:")
            print(f"  {explain_result['explanation']}")
    
    # Step 10: Build report
    print("\n[STEP 10] REPORT BUILDING")
    print("-" * 80)
    report_result = report_builder(
        metrics,
        abnormal_flags,
        pattern_result['patterns'],
        risk_result
    )
    
    report = report_result['report']
    print(f"\nReport Type: {report['report_type']}")
    print(f"Generated: {report['generated_at']}")
    print(f"\nDISCLAIMER:")
    print(f"  {report['disclaimer']}")
    
    print(f"\nSUMMARY:")
    print(f"  Total Metrics Analyzed: {report['summary']['total_metrics_analyzed']}")
    print(f"  Abnormal Metrics: {report['summary']['abnormal_metrics']}")
    print(f"  Patterns Detected: {report['summary']['patterns_detected']}")
    print(f"  Overall Risk Level: {report['summary']['overall_risk_level']}")
    
    print(f"\nRECOMMENDATIONS:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    # Step 11: Full report JSON
    print("\n[STEP 11] FULL STRUCTURED REPORT (JSON)")
    print("-" * 80)
    print(json.dumps(report, indent=2))
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)


def demo_single_metric_analysis():
    """Demo analyzing a single metric"""
    
    print("\n" + "=" * 80)
    print("SINGLE METRIC ANALYSIS DEMO")
    print("=" * 80)
    
    # Analyze glucose
    metric_name = "glucose"
    value = 145
    gender = "female"
    
    print(f"\nAnalyzing: {metric_name} = {value} mg/dL")
    
    # Get reference range
    ref_result = clinical_reference_lookup(metric_name, gender)
    ref_range = ref_result['reference_range']
    print(f"Reference Range: {ref_range['min']}-{ref_range['max']} {ref_range['unit']}")
    
    # Flag abnormal
    flag_result = abnormal_flag_detector(metric_name, value, ref_range)
    print(f"Is Abnormal: {flag_result['is_abnormal']}")
    print(f"Severity: {flag_result['severity']}")
    print(f"Direction: {flag_result['direction']}")
    
    # Explain
    explain_result = plain_language_explainer(
        metric_name, value, ref_range, flag_result['severity']
    )
    print(f"\nExplanation:")
    print(f"  {explain_result['explanation']}")


if __name__ == "__main__":
    demo_full_workflow()
    demo_single_metric_analysis()
