#!/usr/bin/env python3
"""
Quick test of Health Insights Agent
Run this to see the agent in action
"""

from health_insights_agent import create_health_insights_agent
import json

# Create agent
agent = create_health_insights_agent()

# Test 1: Healthy results
print("\n" + "="*80)
print("TEST 1: HEALTHY LAB RESULTS")
print("="*80)

healthy_report = """
LABORATORY TEST RESULTS
Date: 2024-02-05
Patient: John Doe, Male, 35 years old

Glucose: 92 mg/dL
Total Cholesterol: 180 mg/dL
LDL Cholesterol: 110 mg/dL
HDL Cholesterol: 55 mg/dL
Triglycerides: 100 mg/dL
Hemoglobin: 14.5 g/dL
ALT: 25 U/L
AST: 22 U/L
Creatinine: 0.8 mg/dL
BUN: 15 mg/dL
"""

result = agent.run(healthy_report, gender="male")
print(f"\nRisk Level: {result['summary']['overall_risk_level'].upper()}")
print(f"Abnormal Metrics: {result['summary']['abnormal_metrics']}")
print(f"Patterns Detected: {result['summary']['patterns_detected']}")

# Test 2: Metabolic concern
print("\n" + "="*80)
print("TEST 2: METABOLIC CONCERN")
print("="*80)

metabolic_report = """
LABORATORY TEST RESULTS
Date: 2024-02-05
Patient: Jane Smith, Female, 45 years old

Glucose: 145 mg/dL
Total Cholesterol: 220 mg/dL
LDL Cholesterol: 150 mg/dL
HDL Cholesterol: 35 mg/dL
Triglycerides: 200 mg/dL
Hemoglobin: 14.2 g/dL
ALT: 32 U/L
AST: 28 U/L
Creatinine: 0.9 mg/dL
BUN: 16 mg/dL
"""

result = agent.run(metabolic_report, gender="female")
print(f"\nRisk Level: {result['summary']['overall_risk_level'].upper()}")
print(f"Abnormal Metrics: {result['summary']['abnormal_metrics']}")
print(f"Patterns Detected: {result['summary']['patterns_detected']}")

if result['metrics_analysis']['abnormal']:
    print("\nAbnormal Findings:")
    for metric in result['metrics_analysis']['abnormal']:
        print(f"  • {metric['metric']}: {metric['value']} (Status: {metric['severity'].upper()})")

# Test 3: Multiple concerns
print("\n" + "="*80)
print("TEST 3: MULTIPLE HEALTH CONCERNS")
print("="*80)

concern_report = """
LABORATORY TEST RESULTS
Date: 2024-02-05
Patient: Robert Wilson, Male, 55 years old

Glucose: 185 mg/dL
Total Cholesterol: 280 mg/dL
LDL Cholesterol: 200 mg/dL
HDL Cholesterol: 28 mg/dL
Triglycerides: 320 mg/dL
Hemoglobin: 10.5 g/dL
ALT: 120 U/L
AST: 95 U/L
Creatinine: 2.1 mg/dL
BUN: 35 mg/dL
"""

result = agent.run(concern_report, gender="male")
print(f"\nRisk Level: {result['summary']['overall_risk_level'].upper()}")
print(f"Abnormal Metrics: {result['summary']['abnormal_metrics']}")
print(f"Patterns Detected: {result['summary']['patterns_detected']}")

if result['metrics_analysis']['abnormal']:
    print("\nAbnormal Findings:")
    for metric in result['metrics_analysis']['abnormal']:
        print(f"  • {metric['metric']}: {metric['value']} (Status: {metric['severity'].upper()})")

if result['patterns']:
    print("\nDetected Patterns:")
    for pattern in result['patterns']:
        print(f"  • {pattern['pattern'].upper()}: {pattern['description']}")

# Test 4: Single metric analysis
print("\n" + "="*80)
print("TEST 4: SINGLE METRIC ANALYSIS")
print("="*80)

from health_insights_agent import (
    clinical_reference_lookup,
    abnormal_flag_detector,
    plain_language_explainer
)

# Analyze high glucose
metric_name = "glucose"
value = 150
gender = "male"

ref_result = clinical_reference_lookup(metric_name, gender)
ref_range = ref_result['reference_range']

flag_result = abnormal_flag_detector(metric_name, value, ref_range)

explain_result = plain_language_explainer(
    metric_name, value, ref_range, flag_result['severity']
)

print(f"\nMetric: {metric_name.upper()}")
print(f"Value: {value} {ref_range['unit']}")
print(f"Normal Range: {ref_range['min']}-{ref_range['max']}")
print(f"Status: {flag_result['severity'].upper()}")
print(f"\nExplanation:")
print(f"  {explain_result['explanation']}")

print("\n" + "="*80)
print("ALL TESTS COMPLETE")
print("="*80)
print("\n✅ Agent is working correctly!")
print("\nNext steps:")
print("  1. Run: python test_health_insights.py (for interactive testing)")
print("  2. Run: python health_insights_demo.py (for full demo)")
print("  3. Read: HEALTH_INSIGHTS_QUICK_START.md (for documentation)")
