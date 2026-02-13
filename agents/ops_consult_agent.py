#!/usr/bin/env python3
"""
Operations Consulting Agent
Analyzes business problems and provides data-driven improvement recommendations.

Flow: UNDERSTAND → SELECT TOOLS → ANALYZE → FIND DRIVERS → RECOMMEND → EXPLAIN
"""

import json
from strands import Agent, tool
from typing import List, Dict, Optional


# ============================================================================
# TOOL 1: PROBLEM CLASSIFIER
# ============================================================================

@tool
def problem_classifier_tool(problem_description: str) -> str:
    """Classify the business problem into a type.
    
    Types:
    - cost_problem: Reduce expenses, improve margins
    - process_bottleneck: Speed up operations, reduce delays
    - demand_sales_issue: Increase revenue, improve conversion
    - supply_chain_issue: Improve sourcing, reduce lead times
    - marketing_efficiency: Improve ROI, reach, engagement
    
    Args:
        problem_description: Text description of the problem
    
    Returns:
        JSON with problem type and confidence
    """
    try:
        desc_lower = problem_description.lower()
        
        # Classify based on keywords
        if any(word in desc_lower for word in ["cost", "expensive", "margin", "profit", "reduce spend", "budget"]):
            problem_type = "cost_problem"
            confidence = 0.9
        elif any(word in desc_lower for word in ["slow", "delay", "bottleneck", "speed", "throughput", "process", "time"]):
            problem_type = "process_bottleneck"
            confidence = 0.9
        elif any(word in desc_lower for word in ["sales", "revenue", "conversion", "demand", "customer", "growth"]):
            problem_type = "demand_sales_issue"
            confidence = 0.9
        elif any(word in desc_lower for word in ["supplier", "supply", "sourcing", "delivery", "lead time"]):
            problem_type = "supply_chain_issue"
            confidence = 0.9
        elif any(word in desc_lower for word in ["marketing", "campaign", "roi", "engagement", "reach", "ads"]):
            problem_type = "marketing_efficiency"
            confidence = 0.9
        else:
            problem_type = "general_operations"
            confidence = 0.5
        
        return json.dumps({
            "status": "success",
            "problem_type": problem_type,
            "confidence": confidence,
            "description": problem_description[:100] + "..." if len(problem_description) > 100 else problem_description
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# TOOL 2: DATA SUMMARY
# ============================================================================

@tool
def data_summary_tool(data_json: str) -> str:
    """Generate basic statistics and key metrics from dataset.
    
    Args:
        data_json: JSON array of data points with numeric values
    
    Returns:
        JSON with summary statistics
    """
    try:
        data = json.loads(data_json)
        
        if not data or not isinstance(data, list):
            return json.dumps({"status": "error", "message": "Invalid data format"})
        
        # Extract numeric values
        values = []
        for item in data:
            if isinstance(item, dict):
                for v in item.values():
                    if isinstance(v, (int, float)):
                        values.append(v)
            elif isinstance(item, (int, float)):
                values.append(item)
        
        if not values:
            return json.dumps({"status": "error", "message": "No numeric data found"})
        
        # Calculate statistics
        values.sort()
        n = len(values)
        mean = sum(values) / n
        median = values[n // 2]
        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val
        
        # Standard deviation
        variance = sum((x - mean) ** 2 for x in values) / n
        std_dev = variance ** 0.5
        
        return json.dumps({
            "status": "success",
            "count": n,
            "mean": round(mean, 2),
            "median": round(median, 2),
            "min": round(min_val, 2),
            "max": round(max_val, 2),
            "range": round(range_val, 2),
            "std_dev": round(std_dev, 2),
            "key_insight": f"Data ranges from {round(min_val, 2)} to {round(max_val, 2)} with average of {round(mean, 2)}"
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# TOOL 3: TREND DETECTION
# ============================================================================

@tool
def trend_tool(time_series_json: str) -> str:
    """Detect trends (increasing, decreasing, stable) in time series data.
    
    Args:
        time_series_json: JSON array of {period, value} objects
    
    Returns:
        JSON with trend analysis
    """
    try:
        data = json.loads(time_series_json)
        
        if not data or len(data) < 2:
            return json.dumps({"status": "error", "message": "Need at least 2 data points"})
        
        # Extract values
        values = [item.get("value", 0) for item in data]
        periods = [item.get("period", i) for i, item in enumerate(data)]
        
        # Calculate trend
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)
        
        change_pct = ((avg_second - avg_first) / avg_first * 100) if avg_first != 0 else 0
        
        if change_pct > 5:
            trend = "INCREASING"
        elif change_pct < -5:
            trend = "DECREASING"
        else:
            trend = "STABLE"
        
        return json.dumps({
            "status": "success",
            "trend": trend,
            "change_percent": round(change_pct, 1),
            "first_period_avg": round(avg_first, 2),
            "second_period_avg": round(avg_second, 2),
            "insight": f"Trend is {trend} with {abs(round(change_pct, 1))}% change"
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# TOOL 4: BOTTLENECK DETECTION
# ============================================================================

@tool
def bottleneck_tool(process_data_json: str) -> str:
    """Find the slowest step or biggest constraint in a process.
    
    Args:
        process_data_json: JSON array of {step, time, capacity} objects
    
    Returns:
        JSON with bottleneck identification
    """
    try:
        data = json.loads(process_data_json)
        
        if not data:
            return json.dumps({"status": "error", "message": "No process data"})
        
        # Find slowest step
        slowest = max(data, key=lambda x: x.get("time", 0))
        
        # Find most constrained (lowest capacity)
        most_constrained = min(data, key=lambda x: x.get("capacity", float('inf')))
        
        # Calculate impact
        total_time = sum(item.get("time", 0) for item in data)
        bottleneck_impact = (slowest.get("time", 0) / total_time * 100) if total_time > 0 else 0
        
        return json.dumps({
            "status": "success",
            "slowest_step": slowest.get("step", "Unknown"),
            "slowest_time": slowest.get("time", 0),
            "most_constrained": most_constrained.get("step", "Unknown"),
            "constraint_capacity": most_constrained.get("capacity", 0),
            "bottleneck_impact_percent": round(bottleneck_impact, 1),
            "total_process_time": total_time,
            "insight": f"Bottleneck: {slowest.get('step')} takes {slowest.get('time')} units ({round(bottleneck_impact, 1)}% of total time)"
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# TOOL 5: COST DRIVER ANALYSIS
# ============================================================================

@tool
def cost_driver_tool(cost_data_json: str) -> str:
    """Identify the biggest cost contributors.
    
    Args:
        cost_data_json: JSON array of {category, cost} objects
    
    Returns:
        JSON with cost breakdown and drivers
    """
    try:
        data = json.loads(cost_data_json)
        
        if not data:
            return json.dumps({"status": "error", "message": "No cost data"})
        
        # Sort by cost
        sorted_data = sorted(data, key=lambda x: x.get("cost", 0), reverse=True)
        
        total_cost = sum(item.get("cost", 0) for item in data)
        
        # Calculate percentages
        breakdown = []
        for item in sorted_data:
            cost = item.get("cost", 0)
            pct = (cost / total_cost * 100) if total_cost > 0 else 0
            breakdown.append({
                "category": item.get("category", "Unknown"),
                "cost": round(cost, 2),
                "percent": round(pct, 1)
            })
        
        # Top 3 drivers
        top_drivers = breakdown[:3]
        top_driver_pct = sum(item["percent"] for item in top_drivers)
        
        return json.dumps({
            "status": "success",
            "total_cost": round(total_cost, 2),
            "breakdown": breakdown,
            "top_drivers": top_drivers,
            "top_drivers_percent": round(top_driver_pct, 1),
            "insight": f"Top 3 cost drivers account for {round(top_driver_pct, 1)}% of total costs"
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# TOOL 6: SCENARIO SIMULATION
# ============================================================================

@tool
def scenario_tool(original_data_json: str, scenario_change: str) -> str:
    """Apply a what-if change and show the impact.
    
    Scenarios:
    - "reduce:category:percent" - reduce a cost by percent
    - "improve:metric:percent" - improve a metric by percent
    - "remove:step" - remove a process step
    
    Args:
        original_data_json: Original data
        scenario_change: Scenario description
    
    Returns:
        JSON with before/after comparison
    """
    try:
        data = json.loads(original_data_json)
        parts = scenario_change.split(":")
        scenario_type = parts[0]
        target = parts[1] if len(parts) > 1 else None
        value = int(parts[2]) if len(parts) > 2 else 0
        
        # Apply scenario
        if scenario_type == "reduce":
            for item in data:
                if item.get("category") == target or item.get("step") == target:
                    item["cost"] = item.get("cost", 0) * (1 - value/100)
        
        elif scenario_type == "improve":
            for item in data:
                if item.get("metric") == target or item.get("step") == target:
                    item["value"] = item.get("value", 0) * (1 + value/100)
        
        # Calculate impact
        original_total = sum(item.get("cost", item.get("value", 0)) for item in json.loads(original_data_json))
        new_total = sum(item.get("cost", item.get("value", 0)) for item in data)
        impact = ((new_total - original_total) / original_total * 100) if original_total > 0 else 0
        
        return json.dumps({
            "status": "success",
            "scenario": scenario_change,
            "original_total": round(original_total, 2),
            "new_total": round(new_total, 2),
            "impact_percent": round(impact, 1),
            "savings_or_gain": round(abs(new_total - original_total), 2),
            "insight": f"Scenario '{scenario_change}' would result in {round(impact, 1)}% change"
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# TOOL 7: RECOMMENDATION GENERATION
# ============================================================================

@tool
def recommendation_tool(findings_json: str, problem_type: str) -> str:
    """Convert findings into actionable recommendations.
    
    Args:
        findings_json: JSON with analysis findings
        problem_type: Type of problem (cost, bottleneck, etc.)
    
    Returns:
        JSON with 2-4 recommended actions
    """
    try:
        findings = json.loads(findings_json)
        recommendations = []
        
        if problem_type == "cost_problem":
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
        
        elif problem_type == "process_bottleneck":
            recommendations.append({
                "action": "Optimize bottleneck step",
                "description": "Invest in automation or process redesign for slowest step",
                "priority": "HIGH",
                "estimated_impact": "20-30% throughput increase"
            })
            recommendations.append({
                "action": "Add parallel processing",
                "description": "Run non-dependent steps in parallel",
                "priority": "MEDIUM",
                "estimated_impact": "15-25% time reduction"
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
        
        elif problem_type == "supply_chain_issue":
            recommendations.append({
                "action": "Diversify suppliers",
                "description": "Reduce dependency on single suppliers",
                "priority": "HIGH",
                "estimated_impact": "Reduce risk, improve reliability"
            })
            recommendations.append({
                "action": "Optimize inventory levels",
                "description": "Balance safety stock with carrying costs",
                "priority": "MEDIUM",
                "estimated_impact": "15-20% inventory reduction"
            })
        
        else:
            recommendations.append({
                "action": "Conduct detailed analysis",
                "description": "Gather more specific data on the problem area",
                "priority": "HIGH",
                "estimated_impact": "Better understanding for next steps"
            })
        
        return json.dumps({
            "status": "success",
            "recommendations": recommendations,
            "total_recommendations": len(recommendations)
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# TOOL 8: EXPLANATION
# ============================================================================

@tool
def explanation_tool(problem_type: str, findings_json: str, recommendations_json: str) -> str:
    """Convert analysis into consultant-style report summary.
    
    Args:
        problem_type: Type of problem
        findings_json: Analysis findings
        recommendations_json: Recommendations
    
    Returns:
        Plain-language consultant report
    """
    try:
        findings = json.loads(findings_json)
        recommendations = json.loads(recommendations_json)
        
        report = []
        
        report.append("=" * 70)
        report.append("OPERATIONS CONSULTING REPORT")
        report.append("=" * 70)
        
        report.append(f"\n📋 PROBLEM TYPE: {problem_type.replace('_', ' ').upper()}")
        
        report.append(f"\n🔍 KEY FINDINGS:")
        report.append(f"  • Analysis completed on {len(findings)} data points")
        
        if "insight" in findings:
            report.append(f"  • {findings['insight']}")
        
        report.append(f"\n💡 RECOMMENDED ACTIONS:")
        for i, rec in enumerate(recommendations.get("recommendations", []), 1):
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
        
        return json.dumps({
            "status": "success",
            "report": "\n".join(report)
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# AGENT SETUP
# ============================================================================

agent = Agent(
    system_prompt="""You are an Operations Consulting Agent.

Your job is to analyze business problems and provide data-driven recommendations.

WORKFLOW:
1. UNDERSTAND: Read the problem and classify it
2. SELECT TOOLS: Choose the right analysis tools
3. ANALYZE: Run analytics on the data
4. FIND DRIVERS: Identify root causes
5. RECOMMEND: Generate actionable recommendations
6. EXPLAIN: Present findings in consultant-style report
7. SIMULATE (optional): Test what-if scenarios

PROBLEM TYPES:
- cost_problem: Reduce expenses, improve margins
- process_bottleneck: Speed up operations, reduce delays
- demand_sales_issue: Increase revenue, improve conversion
- supply_chain_issue: Improve sourcing, reduce lead times
- marketing_efficiency: Improve ROI, reach, engagement

TOOLS YOU HAVE:
- problem_classifier_tool: Classify the problem type
- data_summary_tool: Get basic statistics
- trend_tool: Find increasing/decreasing trends
- bottleneck_tool: Find slowest steps or constraints
- cost_driver_tool: Identify biggest cost contributors
- scenario_tool: Test what-if changes
- recommendation_tool: Generate actionable recommendations
- explanation_tool: Create consultant-style report

IMPORTANT:
- Always explain in plain language (no jargon)
- Focus on actionable insights
- Provide estimated impact for each recommendation
- Support what-if analysis
- Be specific and data-driven

When user provides problem + data:
1. Classify the problem
2. Summarize the data
3. Run appropriate analysis tools
4. Generate recommendations
5. Explain findings in report format
6. Offer to simulate scenarios""",
    tools=[
        problem_classifier_tool,
        data_summary_tool,
        trend_tool,
        bottleneck_tool,
        cost_driver_tool,
        scenario_tool,
        recommendation_tool,
        explanation_tool,
    ],
)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the ops consult agent in interactive mode."""
    print("=" * 70)
    print("OPERATIONS CONSULTING AGENT")
    print("=" * 70)
    print("\nCapabilities:")
    print("  • Classify business problems")
    print("  • Analyze data and find trends")
    print("  • Identify bottlenecks and cost drivers")
    print("  • Generate actionable recommendations")
    print("  • Simulate what-if scenarios")
    print("  • Provide consultant-style reports")
    print("\nExample queries:")
    print("  'Our manufacturing process is slow. Here's the data: ...'")
    print("  'We need to reduce costs. What are our biggest expenses?'")
    print("  'What if we automate step 3?'")
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
