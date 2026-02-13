#!/usr/bin/env python3
"""Test the Supply Chain Optimizer Agent with sample data."""

from supply_chain_optimizer_agent import (
    supplier_score_tool,
    allocation_tool,
    risk_tool,
    reorder_tool,
    disruption_simulation_tool,
    explanation_tool,
)
import json

print("=" * 70)
print("SUPPLY CHAIN OPTIMIZER AGENT - TEST")
print("=" * 70)

# Sample supplier data
suppliers = [
    {
        "name": "Supplier A",
        "cost_per_unit": 10,
        "delivery_days": 5,
        "reliability_score": 95,
        "max_capacity": 400
    },
    {
        "name": "Supplier B",
        "cost_per_unit": 8,
        "delivery_days": 10,
        "reliability_score": 80,
        "max_capacity": 300
    },
    {
        "name": "Supplier C",
        "cost_per_unit": 12,
        "delivery_days": 3,
        "reliability_score": 98,
        "max_capacity": 250
    },
    {
        "name": "Supplier D",
        "cost_per_unit": 9,
        "delivery_days": 7,
        "reliability_score": 85,
        "max_capacity": 350
    }
]

total_demand = 1000
deadline_days = 15
daily_demand = 50
lead_time_days = 7

print("\n📋 INPUT DATA:")
print(f"  Total Demand: {total_demand} units")
print(f"  Deadline: {deadline_days} days")
print(f"  Daily Demand: {daily_demand} units/day")
print(f"  Suppliers: {len(suppliers)}")

# Step 1: Score suppliers
print("\n" + "=" * 70)
print("STEP 1: SCORE SUPPLIERS")
print("=" * 70)
score_result = supplier_score_tool(json.dumps(suppliers), deadline_days)
score_data = json.loads(score_result)
print(json.dumps(score_data, indent=2))

# Step 2: Allocate demand
print("\n" + "=" * 70)
print("STEP 2: ALLOCATE DEMAND")
print("=" * 70)
allocation_result = allocation_tool(json.dumps(score_data["scored_suppliers"]), total_demand)
allocation_data = json.loads(allocation_result)
print(json.dumps(allocation_data, indent=2))

# Step 3: Assess risk
print("\n" + "=" * 70)
print("STEP 3: ASSESS RISK")
print("=" * 70)
risk_result = risk_tool(allocation_result, deadline_days)
risk_data = json.loads(risk_result)
print(json.dumps(risk_data, indent=2))

# Step 4: Calculate reorder plan
print("\n" + "=" * 70)
print("STEP 4: REORDER PLANNING")
print("=" * 70)
reorder_result = reorder_tool(allocation_result, daily_demand, lead_time_days)
reorder_data = json.loads(reorder_result)
print(json.dumps(reorder_data, indent=2))

# Step 5: Generate explanation
print("\n" + "=" * 70)
print("STEP 5: PLAIN-LANGUAGE EXPLANATION")
print("=" * 70)
explanation_result = explanation_tool(allocation_result, risk_result, reorder_result)
explanation_data = json.loads(explanation_result)
print(explanation_data["explanation"])

# Step 6: Simulate disruption
print("\n" + "=" * 70)
print("STEP 6: DISRUPTION SIMULATION")
print("=" * 70)
print("\n🔴 SCENARIO: Supplier A delayed by 5 days")
disruption_result = disruption_simulation_tool(
    json.dumps(suppliers),
    "supplier_delay:Supplier A:5",
    total_demand,
    deadline_days
)
disruption_data = json.loads(disruption_result)
print(json.dumps(disruption_data, indent=2))

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
