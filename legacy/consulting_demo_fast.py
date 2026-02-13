#!/usr/bin/env python3
"""
Fast Consulting Demo - Tests tools directly without full agent
"""

from ops_consult_agent import (
    problem_classifier_tool,
    data_summary_tool,
    cost_driver_tool,
    bottleneck_tool,
    recommendation_tool,
    explanation_tool,
)
import json

print("=" * 70)
print("OPERATIONS CONSULTING DEMO - FAST VERSION")
print("=" * 70)

# ============================================================================
# SCENARIO 1: COST PROBLEM
# ============================================================================

print("\n" + "=" * 70)
print("SCENARIO 1: MANUFACTURING COMPANY - HIGH COSTS")
print("=" * 70)

problem_desc = "Our manufacturing costs are too high and profit margins are shrinking"

print(f"\n📞 CLIENT: '{problem_desc}'")

# Step 1: Classify
print("\n[Step 1: Classifying problem...]")
classify_result = problem_classifier_tool(problem_desc)
classify_data = json.loads(classify_result)
print(f"Problem Type: {classify_data['problem_type']}")

# Step 2: Analyze costs
print("\n[Step 2: Analyzing cost breakdown...]")
cost_data = [
    {"category": "Raw Materials", "cost": 800000},
    {"category": "Labor", "cost": 600000},
    {"category": "Equipment", "cost": 200000},
    {"category": "Overhead", "cost": 150000},
    {"category": "Logistics", "cost": 100000},
    {"category": "Marketing", "cost": 50000},
    {"category": "Other", "cost": 100000},
]

cost_result = cost_driver_tool(json.dumps(cost_data))
cost_analysis = json.loads(cost_result)

print(f"Total Cost: ${cost_analysis['total_cost']:,.0f}")
print(f"\nTop 3 Cost Drivers ({cost_analysis['top_drivers_percent']}% of total):")
for driver in cost_analysis['top_drivers']:
    print(f"  • {driver['category']}: ${driver['cost']:,.0f} ({driver['percent']}%)")

# Step 3: Generate recommendations
print("\n[Step 3: Generating recommendations...]")
rec_result = recommendation_tool(cost_result, classify_data['problem_type'])
rec_data = json.loads(rec_result)

print(f"\nRecommendations:")
for i, rec in enumerate(rec_data['recommendations'], 1):
    print(f"\n  {i}. {rec['action']} [{rec['priority']}]")
    print(f"     {rec['description']}")
    print(f"     Impact: {rec['estimated_impact']}")

# Step 4: Explain
print("\n[Step 4: Creating consultant report...]")
explain_result = explanation_tool(classify_data['problem_type'], cost_result, rec_result)
explain_data = json.loads(explain_result)
print(explain_data['report'])

# ============================================================================
# SCENARIO 2: BOTTLENECK PROBLEM
# ============================================================================

print("\n\n" + "=" * 70)
print("SCENARIO 2: LOGISTICS COMPANY - SLOW DELIVERY")
print("=" * 70)

problem_desc2 = "Our delivery times are too slow compared to competitors"

print(f"\n📞 CLIENT: '{problem_desc2}'")

# Step 1: Classify
print("\n[Step 1: Classifying problem...]")
classify_result2 = problem_classifier_tool(problem_desc2)
classify_data2 = json.loads(classify_result2)
print(f"Problem Type: {classify_data2['problem_type']}")

# Step 2: Find bottleneck
print("\n[Step 2: Analyzing delivery process...]")
process_data = [
    {"step": "Order Processing", "time": 1, "capacity": 100},
    {"step": "Warehouse Picking", "time": 2, "capacity": 50},
    {"step": "Quality Check", "time": 1, "capacity": 75},
    {"step": "Packing", "time": 0.5, "capacity": 100},
    {"step": "Loading & Dispatch", "time": 0.5, "capacity": 80},
    {"step": "Transit", "time": 2, "capacity": 100},
]

bottleneck_result = bottleneck_tool(json.dumps(process_data))
bottleneck_data = json.loads(bottleneck_result)

print(f"Slowest Step: {bottleneck_data['slowest_step']} ({bottleneck_data['slowest_time']} days)")
print(f"Bottleneck Impact: {bottleneck_data['bottleneck_impact_percent']}% of total time")
print(f"Total Process Time: {bottleneck_data['total_process_time']} days")

# Step 3: Generate recommendations
print("\n[Step 3: Generating recommendations...]")
rec_result2 = recommendation_tool(bottleneck_result, classify_data2['problem_type'])
rec_data2 = json.loads(rec_result2)

print(f"\nRecommendations:")
for i, rec in enumerate(rec_data2['recommendations'], 1):
    print(f"\n  {i}. {rec['action']} [{rec['priority']}]")
    print(f"     {rec['description']}")
    print(f"     Impact: {rec['estimated_impact']}")

# Step 4: Explain
print("\n[Step 4: Creating consultant report...]")
explain_result2 = explanation_tool(classify_data2['problem_type'], bottleneck_result, rec_result2)
explain_data2 = json.loads(explain_result2)
print(explain_data2['report'])

print("\n" + "=" * 70)
print("DEMO COMPLETE")
print("=" * 70)
