#!/usr/bin/env python3
"""
Simplest possible test - just run the agent
"""

from health_insights_agent import create_health_insights_agent
import json

print("\n" + "="*80)
print("HEALTH INSIGHTS AGENT - SIMPLE TEST")
print("="*80 + "\n")

# Create agent
agent = create_health_insights_agent()

# Simple test report
report = """
Glucose: 125 mg/dL
Cholesterol: 220 mg/dL
HDL: 35 mg/dL
Triglycerides: 180 mg/dL
ALT: 65 U/L
AST: 48 U/L
Creatinine: 1.4 mg/dL
BUN: 22 mg/dL
"""

print("Input Report:")
print(report)

print("\nAnalyzing...")
result = agent.run(report)

print("\n" + "="*80)
print("RESULTS")
print("="*80)

print(f"\nRisk Level: {result['summary']['overall_risk_level'].upper()}")
print(f"Metrics Analyzed: {result['summary']['total_metrics_analyzed']}")
print(f"Abnormal Metrics: {result['summary']['abnormal_metrics']}")
print(f"Patterns Detected: {result['summary']['patterns_detected']}")

if result['metrics_analysis']['abnormal']:
    print("\n📊 Abnormal Findings:")
    for m in result['metrics_analysis']['abnormal']:
        print(f"  • {m['metric']}: {m['value']} {m['reference_range']['unit']} ({m['severity'].upper()})")

if result['patterns']:
    print("\n⚠️  Detected Patterns:")
    for p in result['patterns']:
        print(f"  • {p['pattern'].upper()}")
        print(f"    {p['description']}")

print("\n" + "="*80)
print("✅ Test Complete!")
print("="*80)
