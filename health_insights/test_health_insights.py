#!/usr/bin/env python3
"""
Interactive Health Insights Agent Tester
Test the agent with your own medical reports
"""

import json
from health_insights_agent import create_health_insights_agent

def print_header(title):
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80 + "\n")

def print_section(title):
    print(f"\n{title}")
    print("-" * 80)

def format_report(report):
    """Pretty print the report"""
    print_section("ANALYSIS RESULTS")
    
    print(f"\n📋 Report Type: {report['report_type']}")
    print(f"⏰ Generated: {report['generated_at']}")
    
    print_section("SUMMARY")
    summary = report['summary']
    print(f"  Total Metrics Analyzed: {summary['total_metrics_analyzed']}")
    print(f"  Abnormal Metrics: {summary['abnormal_metrics']}")
    print(f"  Patterns Detected: {summary['patterns_detected']}")
    print(f"  Overall Risk Level: {summary['overall_risk_level'].upper()}")
    
    if report['metrics_analysis']['abnormal']:
        print_section("ABNORMAL FINDINGS")
        for metric in report['metrics_analysis']['abnormal']:
            print(f"\n  {metric['metric']}: {metric['value']} {metric['reference_range']['unit']}")
            print(f"    Status: {metric['severity'].upper()}")
            print(f"    Normal Range: {metric['reference_range']['min']}-{metric['reference_range']['max']}")
    
    if report['patterns']:
        print_section("DETECTED PATTERNS")
        for pattern in report['patterns']:
            print(f"\n  • {pattern['pattern'].upper()}")
            print(f"    Markers: {', '.join(pattern['markers'])}")
            print(f"    Description: {pattern['description']}")
    
    print_section("RISK ASSESSMENT")
    risk = report['risk_assessment']
    print(f"  Risk Score: {risk['risk_score']}")
    print(f"  Risk Level: {risk['risk_level'].upper()}")
    
    print_section("RECOMMENDATIONS")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    print_section("MEDICAL DISCLAIMER")
    print(f"  {report['disclaimer']}")

def test_sample_reports():
    """Test with predefined sample reports"""
    
    samples = {
        "1": {
            "name": "Healthy Results",
            "report": """
            LABORATORY TEST RESULTS
            Date: 2024-02-05
            
            Glucose: 92 mg/dL
            Total Cholesterol: 180 mg/dL
            LDL Cholesterol: 110 mg/dL
            HDL Cholesterol: 55 mg/dL
            Triglycerides: 100 mg/dL
            Hemoglobin: 13.5 g/dL
            ALT: 25 U/L
            AST: 22 U/L
            Creatinine: 0.8 mg/dL
            BUN: 15 mg/dL
            """
        },
        "2": {
            "name": "Metabolic Concern",
            "report": """
            LABORATORY TEST RESULTS
            Date: 2024-02-05
            
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
        },
        "3": {
            "name": "Liver Concern",
            "report": """
            LABORATORY TEST RESULTS
            Date: 2024-02-05
            
            ALT: 95 U/L
            AST: 78 U/L
            Bilirubin: 1.8 mg/dL
            Albumin: 3.2 g/dL
            """
        },
        "4": {
            "name": "Kidney Concern",
            "report": """
            LABORATORY TEST RESULTS
            Date: 2024-02-05
            
            Creatinine: 1.6 mg/dL
            BUN: 28 mg/dL
            eGFR: 42 mL/min/1.73m2
            """
        }
    }
    
    print_header("HEALTH INSIGHTS AGENT - INTERACTIVE TESTER")
    print("Sample Reports Available:\n")
    
    for key, sample in samples.items():
        print(f"  {key}. {sample['name']}")
    
    print("\n  0. Enter custom report")
    print("  Q. Quit")
    
    choice = input("\nSelect option (0-4, Q): ").strip().upper()
    
    if choice == "Q":
        print("\nGoodbye!")
        return
    
    if choice == "0":
        print("\nEnter your medical report (type 'END' on a new line when done):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        report_text = "\n".join(lines)
    elif choice in samples:
        report_text = samples[choice]['report']
        print(f"\nAnalyzing: {samples[choice]['name']}")
    else:
        print("Invalid choice!")
        return
    
    # Create agent and analyze
    print("\n⏳ Analyzing report...")
    agent = create_health_insights_agent()
    result = agent.run(report_text)
    
    # Display results
    format_report(result)
    
    # Option to see full JSON
    print_section("FULL JSON REPORT")
    print(json.dumps(result, indent=2))

def test_single_metric():
    """Test analyzing a single metric"""
    from health_insights_agent import (
        clinical_reference_lookup,
        abnormal_flag_detector,
        plain_language_explainer
    )
    
    print_header("SINGLE METRIC ANALYZER")
    
    print("Available metrics:")
    metrics = ["glucose", "cholesterol", "hemoglobin", "alt", "ast", "creatinine", "bun"]
    for i, m in enumerate(metrics, 1):
        print(f"  {i}. {m}")
    
    choice = input("\nSelect metric (1-7): ").strip()
    
    try:
        metric_name = metrics[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid choice!")
        return
    
    try:
        value = float(input(f"Enter {metric_name} value: "))
    except ValueError:
        print("Invalid value!")
        return
    
    # Get reference range
    ref_result = clinical_reference_lookup(metric_name)
    if ref_result['status'] != 'success':
        print(f"Reference range not found for {metric_name}")
        return
    
    ref_range = ref_result['reference_range']
    
    # Flag abnormal
    flag_result = abnormal_flag_detector(metric_name, value, ref_range)
    
    # Explain
    explain_result = plain_language_explainer(
        metric_name, value, ref_range, flag_result['severity']
    )
    
    print_section(f"ANALYSIS: {metric_name.upper()}")
    print(f"Value: {value} {ref_range['unit']}")
    print(f"Normal Range: {ref_range['min']}-{ref_range['max']} {ref_range['unit']}")
    print(f"Status: {flag_result['severity'].upper()}")
    print(f"\nExplanation:")
    print(f"  {explain_result['explanation']}")

def main():
    """Main menu"""
    while True:
        print_header("HEALTH INSIGHTS AGENT - TEST MENU")
        print("1. Test with sample reports")
        print("2. Analyze single metric")
        print("3. Run full demo")
        print("Q. Quit")
        
        choice = input("\nSelect option (1-3, Q): ").strip().upper()
        
        if choice == "1":
            test_sample_reports()
        elif choice == "2":
            test_single_metric()
        elif choice == "3":
            import subprocess
            subprocess.run(["python", "health_insights_demo.py"])
        elif choice == "Q":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
