#!/usr/bin/env python3
"""
Operations Consulting Agent - Standalone Demo
Analyzes business problems and provides recommendations
"""

import json
from typing import List, Dict

# ============================================================================
# TOOLS (Simplified for standalone use)
# ============================================================================

def problem_classifier(problem_description: str) -> dict:
    """Classify the business problem"""
    desc_lower = problem_description.lower()
    
    if any(word in desc_lower for word in ["cost", "expensive", "margin", "profit", "reduce spend"]):
        return {"type": "cost_problem", "confidence": 0.9}
    elif any(word in desc_lower for word in ["slow", "delay", "bottleneck", "speed", "throughput"]):
        return {"type": "process_bottleneck", "confidence": 0.9}
    elif any(word in desc_lower for word in ["sales", "revenue", "conversion", "demand", "growth"]):
        return {"type": "demand_sales_issue", "confidence": 0.9}
    else:
        return {"type": "general_operations", "confidence": 0.5}


def analyze_bottleneck(process_data: List[Dict]) -> dict:
    """Find the slowest step in a process"""
    if not process_data:
        return {"error": "No data"}
    
    slowest = max(process_data, key=lambda x: x.get("time", 0))
    most_constrained = min(process_data, key=lambda x: x.get("capacity", float('inf')))
    
    total_time = sum(item.get("time", 0) for item in process_data)
    bottleneck_impact = (slowest.get("time", 0) / total_time * 100) if total_time > 0 else 0
    
    return {
        "slowest_step": slowest.get("step", "Unknown"),
        "slowest_time": slowest.get("time", 0),
        "most_constrained": most_constrained.get("step", "Unknown"),
        "constraint_capacity": most_constrained.get("capacity", 0),
        "bottleneck_impact_percent": round(bottleneck_impact, 1),
        "total_process_time": total_time
    }


def generate_recommendations(problem_type: str, findings: dict) -> List[Dict]:
    """Generate actionable recommendations"""
    recommendations = []
    
    if problem_type == "process_bottleneck":
        recommendations.append({
            "action": "Optimize bottleneck step",
            "description": f"Focus on {findings.get('slowest_step')} which takes {findings.get('slowest_time')} hours",
            "priority": "HIGH",
            "estimated_impact": "20-30% throughput increase"
        })
        recommendations.append({
            "action": "Add parallel processing",
            "description": "Run non-dependent steps in parallel to reduce total time",
            "priority": "MEDIUM",
            "estimated_impact": "15-25% time reduction"
        })
        recommendations.append({
            "action": "Invest in automation",
            "description": f"Automate {findings.get('slowest_step')} to increase capacity",
            "priority": "HIGH",
            "estimated_impact": "30-40% capacity increase"
        })
    
    elif problem_type == "cost_problem":
        recommendations.append({
            "action": "Focus on top cost drivers",
            "description": "Target the 3 categories that account for 80% of costs",
            "priority": "HIGH",
            "estimated_impact": "10-20% cost reduction"
        })
        recommendations.append({
            "action": "Negotiate with suppliers",
            "description": "Use volume leverage to reduce unit costs",
            "priority": "MEDIUM",
            "estimated_impact": "5-10% cost reduction"
        })
    
    elif problem_type == "demand_sales_issue":
        recommendations.append({
            "action": "Improve conversion funnel",
            "description": "Focus on highest-drop stages in sales process",
            "priority": "HIGH",
            "estimated_impact": "10-15% conversion improvement"
        })
        recommendations.append({
            "action": "Increase marketing reach",
            "description": "Expand to underserved customer segments",
            "priority": "MEDIUM",
            "estimated_impact": "20-30% demand increase"
        })
    
    return recommendations


def generate_report(problem_type: str, findings: dict, recommendations: List[Dict]) -> str:
    """Generate consultant-style report"""
    report = []
    
    report.append("=" * 70)
    report.append("OPERATIONS CONSULTING REPORT")
    report.append("=" * 70)
    
    report.append(f"\n📋 PROBLEM TYPE: {problem_type.replace('_', ' ').upper()}")
    
    report.append(f"\n🔍 KEY FINDINGS:")
    if "slowest_step" in findings:
        report.append(f"  • Bottleneck: {findings['slowest_step']} ({findings['slowest_time']} hours)")
        report.append(f"  • Impact: {findings['bottleneck_impact_percent']}% of total process time")
        report.append(f"  • Total Process Time: {findings['total_process_time']} hours")
    
    report.append(f"\n💡 RECOMMENDED ACTIONS:")
    for i, rec in enumerate(recommendations, 1):
        report.append(f"\n  {i}. {rec['action']} [{rec['priority']}]")
        report.append(f"     {rec['description']}")
        report.append(f"     Expected Impact: {rec['estimated_impact']}")
    
    report.append(f"\n⚠️ RISKS & TRADEOFFS:")
    report.append(f"  • Implementation may require upfront investment")
    report.append(f"  • Changes should be monitored closely")
    report.append(f"  • Phased approach recommended")
    
    report.append(f"\n✅ NEXT STEPS:")
    report.append(f"  1. Prioritize recommendations by impact and effort")
    report.append(f"  2. Develop detailed implementation plan")
    report.append(f"  3. Set KPIs to measure success")
    report.append(f"  4. Monitor and adjust as needed")
    
    report.append("\n" + "=" * 70)
    
    return "\n".join(report)


# ============================================================================
# DEMO
# ============================================================================

def run_demo():
    """Run a consulting analysis demo"""
    
    print("\n" + "=" * 70)
    print("OPERATIONS CONSULTING AGENT - DEMO")
    print("=" * 70)
    
    # Example 1: Manufacturing bottleneck
    print("\n📊 SCENARIO 1: Manufacturing Process Optimization")
    print("-" * 70)
    
    problem = "Our manufacturing process is too slow. We need to speed things up."
    
    process_data = [
        {"step": "Assembly", "time": 10, "capacity": 100},
        {"step": "Quality Check", "time": 8, "capacity": 150},
        {"step": "Packaging", "time": 5, "capacity": 200},
        {"step": "Shipping", "time": 12, "capacity": 80}
    ]
    
    print(f"\nProblem: {problem}")
    print(f"\nProcess Data:")
    for step in process_data:
        print(f"  • {step['step']}: {step['time']} hours, capacity {step['capacity']} units")
    
    # Analyze
    problem_type = problem_classifier(problem)["type"]
    findings = analyze_bottleneck(process_data)
    recommendations = generate_recommendations(problem_type, findings)
    report = generate_report(problem_type, findings, recommendations)
    
    print(f"\n{report}")
    
    # Example 2: Cost reduction
    print("\n\n📊 SCENARIO 2: Cost Reduction Analysis")
    print("-" * 70)
    
    problem2 = "We need to reduce our operating costs significantly."
    
    cost_data = [
        {"category": "Labor", "cost": 500000},
        {"category": "Materials", "cost": 300000},
        {"category": "Utilities", "cost": 150000},
        {"category": "Equipment", "cost": 100000},
        {"category": "Other", "cost": 50000}
    ]
    
    print(f"\nProblem: {problem2}")
    print(f"\nCost Breakdown:")
    total = sum(c["cost"] for c in cost_data)
    for item in cost_data:
        pct = (item["cost"] / total * 100)
        print(f"  • {item['category']}: ${item['cost']:,} ({pct:.1f}%)")
    
    # Analyze
    problem_type2 = problem_classifier(problem2)["type"]
    recommendations2 = generate_recommendations(problem_type2, {})
    
    print(f"\n💡 RECOMMENDATIONS:")
    for i, rec in enumerate(recommendations2, 1):
        print(f"\n  {i}. {rec['action']} [{rec['priority']}]")
        print(f"     {rec['description']}")
        print(f"     Expected Impact: {rec['estimated_impact']}")
    
    # Example 3: Sales growth
    print("\n\n📊 SCENARIO 3: Sales Growth Strategy")
    print("-" * 70)
    
    problem3 = "Our sales are flat and we need to grow revenue."
    
    sales_data = [
        {"stage": "Awareness", "conversion": 0.30},
        {"stage": "Interest", "conversion": 0.50},
        {"stage": "Consideration", "conversion": 0.40},
        {"stage": "Purchase", "conversion": 0.25}
    ]
    
    print(f"\nProblem: {problem3}")
    print(f"\nSales Funnel:")
    for stage in sales_data:
        print(f"  • {stage['stage']}: {stage['conversion']*100:.0f}% conversion")
    
    # Analyze
    problem_type3 = problem_classifier(problem3)["type"]
    recommendations3 = generate_recommendations(problem_type3, {})
    
    print(f"\n💡 RECOMMENDATIONS:")
    for i, rec in enumerate(recommendations3, 1):
        print(f"\n  {i}. {rec['action']} [{rec['priority']}]")
        print(f"     {rec['description']}")
        print(f"     Expected Impact: {rec['estimated_impact']}")
    
    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
