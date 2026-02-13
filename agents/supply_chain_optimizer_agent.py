#!/usr/bin/env python3
"""
Supply Chain Optimizer Agent
Uses Strands framework to optimize supplier selection and reorder planning.

Flow: PLAN → SCORE → ALLOCATE → CHECK CONSTRAINTS → DECIDE → EXPLAIN
"""

import json
from strands import Agent, tool
from typing import List, Dict, Optional


# ============================================================================
# TOOL 1: SUPPLIER SCORING
# ============================================================================

@tool
def supplier_score_tool(suppliers_json: str, deadline_days: int) -> str:
    """Score each supplier based on cost, delivery time, and reliability.
    
    Weighted scoring:
    - Reliability: 40% (most important - on-time delivery)
    - Deadline fit: 35% (can we meet the deadline?)
    - Cost: 25% (lower is better)
    
    Args:
        suppliers_json: JSON array of suppliers with cost, delivery_days, reliability
        deadline_days: Days until we need the order
    
    Returns:
        JSON with scored suppliers ranked best to worst
    """
    try:
        suppliers = json.loads(suppliers_json)
        scored = []
        
        for supplier in suppliers:
            name = supplier.get("name", "Unknown")
            cost = supplier.get("cost_per_unit", 0)
            delivery = supplier.get("delivery_days", 999)
            reliability = supplier.get("reliability_score", 0)  # 0-100
            
            # Normalize scores to 0-100
            cost_score = max(0, 100 - (cost * 2))  # Lower cost = higher score
            delivery_score = 100 if delivery <= deadline_days else max(0, 100 - (delivery - deadline_days) * 5)
            reliability_score = reliability  # Already 0-100
            
            # Weighted score (reliability + deadline fit favored)
            weighted_score = (
                reliability_score * 0.40 +
                delivery_score * 0.35 +
                cost_score * 0.25
            )
            
            scored.append({
                "name": name,
                "cost_per_unit": cost,
                "delivery_days": delivery,
                "reliability_score": reliability,
                "cost_score": round(cost_score, 1),
                "delivery_score": round(delivery_score, 1),
                "reliability_score_normalized": reliability_score,
                "weighted_score": round(weighted_score, 1),
                "capacity": supplier.get("max_capacity", 0)
            })
        
        # Sort by weighted score (best first)
        scored.sort(key=lambda x: x["weighted_score"], reverse=True)
        
        return json.dumps({
            "status": "success",
            "scored_suppliers": scored,
            "best_supplier": scored[0]["name"] if scored else "None"
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# TOOL 2: DEMAND ALLOCATION
# ============================================================================

@tool
def allocation_tool(suppliers_json: str, total_demand: int) -> str:
    """Allocate demand across suppliers respecting capacity limits.
    
    Strategy: Use best suppliers first until capacity hit, then move to next.
    
    Args:
        suppliers_json: JSON array of scored suppliers (from supplier_score_tool)
        total_demand: Total units needed
    
    Returns:
        JSON with allocation plan and total cost
    """
    try:
        suppliers = json.loads(suppliers_json)
        allocation = []
        remaining_demand = total_demand
        total_cost = 0
        
        for supplier in suppliers:
            if remaining_demand <= 0:
                break
            
            name = supplier.get("name", "Unknown")
            capacity = supplier.get("capacity", 0)
            cost_per_unit = supplier.get("cost_per_unit", 0)
            
            # Allocate as much as possible from this supplier
            allocated = min(remaining_demand, capacity)
            cost = allocated * cost_per_unit
            
            allocation.append({
                "supplier": name,
                "quantity": allocated,
                "cost_per_unit": cost_per_unit,
                "total_cost": round(cost, 2),
                "capacity_used": f"{allocated}/{capacity}",
                "reliability": supplier.get("reliability_score", 0),
                "delivery_days": supplier.get("delivery_days", 0)
            })
            
            remaining_demand -= allocated
            total_cost += cost
        
        # Check if demand is fully met
        demand_met = remaining_demand <= 0
        
        return json.dumps({
            "status": "success",
            "allocation": allocation,
            "total_cost": round(total_cost, 2),
            "demand_met": demand_met,
            "unmet_demand": max(0, remaining_demand),
            "suppliers_used": len(allocation)
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# TOOL 3: RISK ASSESSMENT
# ============================================================================

@tool
def risk_tool(allocation_json: str, deadline_days: int) -> str:
    """Estimate delay and stockout risk from supplier reliability and delivery times.
    
    Risk factors:
    - Low reliability = high risk
    - Long delivery time close to deadline = high risk
    - Multiple suppliers = lower risk (diversification)
    
    Args:
        allocation_json: JSON allocation plan from allocation_tool
        deadline_days: Days until deadline
    
    Returns:
        JSON with risk scores and recommendations
    """
    try:
        data = json.loads(allocation_json)
        allocation = data.get("allocation", [])
        
        if not allocation:
            return json.dumps({"status": "error", "message": "No allocation data"})
        
        # Calculate risk metrics
        avg_reliability = sum(s.get("reliability", 0) for s in allocation) / len(allocation)
        max_delivery = max(s.get("delivery_days", 0) for s in allocation)
        num_suppliers = len(allocation)
        
        # Risk score (0-100, higher = more risk)
        reliability_risk = (100 - avg_reliability) * 0.5  # Low reliability = high risk
        deadline_risk = max(0, (max_delivery - deadline_days) * 5) * 0.3  # Late delivery = risk
        concentration_risk = (100 - (num_suppliers * 20)) * 0.2  # Single supplier = risk
        
        total_risk = min(100, reliability_risk + deadline_risk + concentration_risk)
        
        # Risk level classification
        if total_risk < 20:
            risk_level = "LOW"
        elif total_risk < 50:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"
        
        # Recommendations
        recommendations = []
        if avg_reliability < 85:
            recommendations.append("⚠️ Consider suppliers with higher reliability scores")
        if max_delivery > deadline_days:
            recommendations.append("⚠️ Some suppliers may miss deadline - consider expedited shipping")
        if num_suppliers == 1:
            recommendations.append("⚠️ Single supplier - high concentration risk. Diversify if possible")
        if total_risk > 50:
            recommendations.append("⚠️ Consider increasing safety stock buffer")
        
        return json.dumps({
            "status": "success",
            "risk_score": round(total_risk, 1),
            "risk_level": risk_level,
            "avg_reliability": round(avg_reliability, 1),
            "max_delivery_days": max_delivery,
            "num_suppliers": num_suppliers,
            "recommendations": recommendations
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# TOOL 4: REORDER PLANNING
# ============================================================================

@tool
def reorder_tool(allocation_json: str, daily_demand: float, lead_time_days: int) -> str:
    """Compute reorder point and safety stock buffer.
    
    Formulas:
    - Reorder Point = (Daily Demand × Lead Time) + Safety Stock
    - Safety Stock = Z-score × Std Dev × sqrt(Lead Time)
    
    Args:
        allocation_json: JSON allocation plan
        daily_demand: Average daily demand (units/day)
        lead_time_days: Average lead time from suppliers
    
    Returns:
        JSON with reorder point and safety stock recommendations
    """
    try:
        data = json.loads(allocation_json)
        allocation = data.get("allocation", [])
        
        if not allocation:
            return json.dumps({"status": "error", "message": "No allocation data"})
        
        # Calculate average lead time from allocation
        avg_lead_time = sum(s.get("delivery_days", 0) for s in allocation) / len(allocation)
        
        # Safety stock calculation (simplified)
        # Z-score for 95% service level = 1.65
        # Assume 20% demand variability
        z_score = 1.65
        demand_std_dev = daily_demand * 0.20
        safety_stock = z_score * demand_std_dev * (avg_lead_time ** 0.5)
        
        # Reorder point
        reorder_point = (daily_demand * avg_lead_time) + safety_stock
        
        # Economic order quantity (simplified)
        # EOQ = sqrt(2 * D * S / H) where D=annual demand, S=order cost, H=holding cost
        # Simplified: use total allocation as reference
        total_allocated = sum(s.get("quantity", 0) for s in allocation)
        eoq = (total_allocated * 0.3) ** 0.5  # Simplified
        
        return json.dumps({
            "status": "success",
            "reorder_point": round(reorder_point, 1),
            "safety_stock": round(safety_stock, 1),
            "avg_lead_time_days": round(avg_lead_time, 1),
            "daily_demand": daily_demand,
            "economic_order_qty": round(eoq, 1),
            "recommendation": f"Reorder when inventory drops to {round(reorder_point, 0)} units"
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# TOOL 5: DISRUPTION SIMULATION
# ============================================================================

@tool
def disruption_simulation_tool(suppliers_json: str, disruption_scenario: str, total_demand: int, deadline_days: int) -> str:
    """Simulate supplier disruption and recompute allocation.
    
    Scenarios:
    - "supplier_delay:name:days" - delay a supplier by N days
    - "capacity_drop:name:percent" - reduce capacity by percent
    - "reliability_drop:name:percent" - reduce reliability by percent
    
    Args:
        suppliers_json: Original supplier data
        disruption_scenario: Disruption description
        total_demand: Total demand
        deadline_days: Deadline
    
    Returns:
        JSON with new allocation plan after disruption
    """
    try:
        suppliers = json.loads(suppliers_json)
        
        # Parse disruption scenario
        parts = disruption_scenario.split(":")
        scenario_type = parts[0]
        supplier_name = parts[1] if len(parts) > 1 else None
        value = int(parts[2]) if len(parts) > 2 else 0
        
        # Apply disruption
        for supplier in suppliers:
            if supplier.get("name") == supplier_name:
                if scenario_type == "supplier_delay":
                    supplier["delivery_days"] += value
                elif scenario_type == "capacity_drop":
                    supplier["max_capacity"] = int(supplier["max_capacity"] * (1 - value/100))
                elif scenario_type == "reliability_drop":
                    supplier["reliability_score"] = max(0, supplier["reliability_score"] - value)
        
        # Rescore and reallocate
        score_result = supplier_score_tool(json.dumps(suppliers), deadline_days)
        score_data = json.loads(score_result)
        
        if score_data.get("status") != "success":
            return json.dumps({"status": "error", "message": "Scoring failed"})
        
        allocation_result = allocation_tool(json.dumps(score_data["scored_suppliers"]), total_demand)
        allocation_data = json.loads(allocation_result)
        
        return json.dumps({
            "status": "success",
            "disruption": disruption_scenario,
            "new_allocation": allocation_data.get("allocation", []),
            "new_total_cost": allocation_data.get("total_cost", 0),
            "demand_met": allocation_data.get("demand_met", False),
            "unmet_demand": allocation_data.get("unmet_demand", 0),
            "impact": "Reallocation successful" if allocation_data.get("demand_met") else "⚠️ Cannot meet demand with disruption!"
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# TOOL 6: EXPLANATION
# ============================================================================

@tool
def explanation_tool(allocation_json: str, risk_json: str, reorder_json: str) -> str:
    """Convert numbers into plain-language reasoning.
    
    Args:
        allocation_json: Allocation plan
        risk_json: Risk assessment
        reorder_json: Reorder plan
    
    Returns:
        Plain-language explanation of the supply chain plan
    """
    try:
        alloc = json.loads(allocation_json)
        risk = json.loads(risk_json)
        reorder = json.loads(reorder_json)
        
        allocation = alloc.get("allocation", [])
        
        # Build explanation
        explanation = []
        
        # Supplier selection
        explanation.append("📦 SUPPLIER SELECTION:")
        for i, supplier in enumerate(allocation, 1):
            explanation.append(f"  {i}. {supplier['supplier']}: {supplier['quantity']} units @ ${supplier['cost_per_unit']}/unit")
            explanation.append(f"     Reliability: {supplier['reliability']}% | Delivery: {supplier['delivery_days']} days")
        
        # Cost summary
        explanation.append(f"\n💰 COST SUMMARY:")
        explanation.append(f"  Total Cost: ${alloc.get('total_cost', 0)}")
        explanation.append(f"  Suppliers Used: {alloc.get('suppliers_used', 0)}")
        
        # Risk assessment
        explanation.append(f"\n⚠️ RISK ASSESSMENT:")
        explanation.append(f"  Risk Level: {risk.get('risk_level', 'UNKNOWN')}")
        explanation.append(f"  Risk Score: {risk.get('risk_score', 0)}/100")
        explanation.append(f"  Avg Reliability: {risk.get('avg_reliability', 0)}%")
        
        if risk.get("recommendations"):
            explanation.append(f"  Recommendations:")
            for rec in risk.get("recommendations", []):
                explanation.append(f"    {rec}")
        
        # Reorder planning
        explanation.append(f"\n📊 REORDER PLANNING:")
        explanation.append(f"  Reorder Point: {reorder.get('reorder_point', 0)} units")
        explanation.append(f"  Safety Stock: {reorder.get('safety_stock', 0)} units")
        explanation.append(f"  Avg Lead Time: {reorder.get('avg_lead_time_days', 0)} days")
        explanation.append(f"  {reorder.get('recommendation', '')}")
        
        # Final recommendation
        explanation.append(f"\n✅ RECOMMENDATION:")
        if alloc.get("demand_met"):
            explanation.append(f"  ✓ Demand can be fully met with this supplier mix")
        else:
            explanation.append(f"  ✗ WARNING: {alloc.get('unmet_demand', 0)} units cannot be sourced!")
        
        if risk.get("risk_level") == "LOW":
            explanation.append(f"  ✓ Low supply chain risk - plan is solid")
        elif risk.get("risk_level") == "MEDIUM":
            explanation.append(f"  ⚠️ Medium risk - monitor suppliers closely")
        else:
            explanation.append(f"  ✗ High risk - consider contingency plans")
        
        return json.dumps({
            "status": "success",
            "explanation": "\n".join(explanation)
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# AGENT SETUP
# ============================================================================

agent = Agent(
    system_prompt="""You are a Supply Chain Helper Agent.

Your job is to help people choose the best suppliers and plan orders in SIMPLE terms.

WHAT YOU DO:
1. Look at each supplier (cost, speed, reliability)
2. Pick the best ones for the job
3. Split the order across them
4. Check if there are any problems
5. Explain everything in plain English

SIMPLE SCORING:
- Reliability (most important): Does the supplier deliver on time? (0-100%)
- Speed (important): How fast can they deliver? (fewer days = better)
- Cost (less important): How much do they charge? (lower = better)

PLAIN LANGUAGE RULES:
- NO jargon. Use simple words.
- Explain WHY you chose each supplier
- Use emojis and simple formatting
- Give clear recommendations
- Support "what-if" questions

EXAMPLE EXPLANATION:
"We need 1000 items by day 15.
✓ Supplier A is BEST - super reliable (95%), fast (5 days), good price ($10)
✓ Supplier C is FAST - fastest delivery (3 days), very reliable (98%)
✓ Supplier D is CHEAP - lowest price ($9), decent reliability (85%)

We'll order from all 3 to spread the risk.
Total cost: $10,150
Risk level: LOW (all suppliers are reliable)
Reorder when you have 287 items left"

WHEN USER ASKS "WHAT IF":
- Recalculate everything
- Show what changes
- Explain if it's still OK or if there's a problem""",
    tools=[
        supplier_score_tool,
        allocation_tool,
        risk_tool,
        reorder_tool,
        disruption_simulation_tool,
        explanation_tool,
    ],
)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the supply chain optimizer agent in interactive mode."""
    print("=" * 70)
    print("SUPPLY CHAIN OPTIMIZER AGENT")
    print("=" * 70)
    print("\nCapabilities:")
    print("  • Score suppliers by cost, delivery time, and reliability")
    print("  • Allocate demand across best suppliers")
    print("  • Assess supply chain risk")
    print("  • Calculate reorder points and safety stock")
    print("  • Simulate disruptions (delays, capacity drops, etc.)")
    print("  • Explain recommendations in plain language")
    print("\nExample queries:")
    print("  'I need 1000 units by day 30. Here are my suppliers: ...'")
    print("  'What if Supplier A is delayed by 5 days?'")
    print("  'Show me the reorder plan'")
    print("\nType 'exit' to quit\n")
    
    while True:
        try:
            user_input = input("You > ").strip()
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\n[Agent analyzing...]\n")
            response = agent(user_input)
            print(f"Agent > {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
