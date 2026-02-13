#!/usr/bin/env python3
"""
Multi-Agent Orchestrator
Coordinates Supply Chain Optimizer Agent and Operations Consulting Agent

The orchestrator:
1. Understands the user's request
2. Routes to the appropriate agent
3. Combines results if needed
4. Provides unified response
"""

import json
from supply_chain_optimizer_agent import agent as supply_chain_agent
from ops_consult_agent import agent as ops_consult_agent
from strands import Agent, tool


# ============================================================================
# ROUTING TOOL
# ============================================================================

@tool
def route_request_tool(user_request: str) -> str:
    """Determine which agent should handle the request.
    
    Routes to:
    - supply_chain: Supplier selection, ordering, reorder planning
    - ops_consult: Cost analysis, process optimization, recommendations
    - both: Complex problems needing both agents
    
    Args:
        user_request: User's question or problem
    
    Returns:
        JSON with routing decision
    """
    try:
        request_lower = user_request.lower()
        
        # Supply chain keywords
        supply_chain_keywords = ["supplier", "order", "reorder", "delivery", "capacity", "sourcing", "procurement"]
        
        # Ops consult keywords
        ops_keywords = ["cost", "bottleneck", "slow", "efficiency", "process", "throughput", "optimize", "improve", "reduce"]
        
        supply_chain_score = sum(1 for kw in supply_chain_keywords if kw in request_lower)
        ops_score = sum(1 for kw in ops_keywords if kw in request_lower)
        
        if supply_chain_score > ops_score and supply_chain_score > 0:
            route = "supply_chain"
        elif ops_score > supply_chain_score and ops_score > 0:
            route = "ops_consult"
        elif supply_chain_score > 0 and ops_score > 0:
            route = "both"
        else:
            route = "general"
        
        return json.dumps({
            "status": "success",
            "route": route,
            "supply_chain_score": supply_chain_score,
            "ops_score": ops_score,
            "recommendation": f"Route to {route} agent"
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# ============================================================================
# ORCHESTRATOR AGENT
# ============================================================================

orchestrator = Agent(
    system_prompt="""You are a Multi-Agent Orchestrator.

Your job is to understand user requests and route them to the right specialist agents.

AVAILABLE AGENTS:
1. Supply Chain Optimizer Agent
   - Handles: Supplier selection, ordering, reorder planning, disruption scenarios
   - Best for: "I need to choose suppliers", "What if a supplier delays?"

2. Operations Consulting Agent
   - Handles: Cost analysis, process optimization, bottleneck detection, recommendations
   - Best for: "How can we reduce costs?", "Our process is slow"

ROUTING LOGIC:
- If request mentions suppliers, ordering, delivery → Supply Chain Agent
- If request mentions costs, efficiency, bottlenecks → Ops Consult Agent
- If request mentions both → Use both agents and combine insights
- If unclear → Ask for clarification

WORKFLOW:
1. Understand the user's request
2. Route to appropriate agent(s)
3. Combine results if using multiple agents
4. Provide unified response

IMPORTANT:
- Be clear about which agent is handling the request
- Combine insights from multiple agents when relevant
- Always explain the reasoning
- Offer follow-up analysis options""",
    tools=[route_request_tool],
)


# ============================================================================
# MAIN ORCHESTRATION FUNCTION
# ============================================================================

def orchestrate(user_request: str) -> str:
    """
    Main orchestration function.
    Routes request to appropriate agent(s) and combines results.
    """
    
    print("\n" + "=" * 70)
    print("MULTI-AGENT ORCHESTRATOR")
    print("=" * 70)
    
    # Step 1: Route the request
    print("\n[Step 1: Routing request...]")
    routing_result = route_request_tool(user_request)
    routing_data = json.loads(routing_result)
    route = routing_data.get("route", "general")
    
    print(f"Route: {route}")
    
    # Step 2: Send to appropriate agent(s)
    print(f"\n[Step 2: Sending to {route} agent(s)...]")
    
    results = {}
    
    if route == "supply_chain":
        print("→ Supply Chain Optimizer Agent")
        results["supply_chain"] = supply_chain_agent(user_request)
    
    elif route == "ops_consult":
        print("→ Operations Consulting Agent")
        results["ops_consult"] = ops_consult_agent(user_request)
    
    elif route == "both":
        print("→ Supply Chain Optimizer Agent")
        results["supply_chain"] = supply_chain_agent(user_request)
        print("→ Operations Consulting Agent")
        results["ops_consult"] = ops_consult_agent(user_request)
    
    else:
        print("→ Orchestrator Agent (general routing)")
        results["orchestrator"] = orchestrator(user_request)
    
    # Step 3: Combine results
    print(f"\n[Step 3: Combining results...]")
    
    combined_response = []
    combined_response.append("=" * 70)
    combined_response.append("MULTI-AGENT ANALYSIS RESULTS")
    combined_response.append("=" * 70)
    
    if "supply_chain" in results:
        combined_response.append("\n📦 SUPPLY CHAIN ANALYSIS:")
        combined_response.append("-" * 70)
        combined_response.append(results["supply_chain"][:500] + "..." if len(results["supply_chain"]) > 500 else results["supply_chain"])
    
    if "ops_consult" in results:
        combined_response.append("\n🏭 OPERATIONS ANALYSIS:")
        combined_response.append("-" * 70)
        combined_response.append(results["ops_consult"][:500] + "..." if len(results["ops_consult"]) > 500 else results["ops_consult"])
    
    if "orchestrator" in results:
        combined_response.append("\n🤖 ORCHESTRATOR RESPONSE:")
        combined_response.append("-" * 70)
        combined_response.append(results["orchestrator"])
    
    combined_response.append("\n" + "=" * 70)
    combined_response.append("END OF ANALYSIS")
    combined_response.append("=" * 70)
    
    return "\n".join(combined_response)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the multi-agent orchestrator in interactive mode."""
    print("=" * 70)
    print("MULTI-AGENT ORCHESTRATOR")
    print("=" * 70)
    print("\nAvailable Agents:")
    print("  1. Supply Chain Optimizer - Supplier selection & ordering")
    print("  2. Operations Consulting - Cost & process optimization")
    print("\nThe orchestrator will route your request to the right agent(s).")
    print("\nExample queries:")
    print("  'I need 1000 units by day 15. Which suppliers should I use?'")
    print("  'Our manufacturing is slow and costs are high. What should we do?'")
    print("  'What if we reduce supplier costs by 10%?'")
    print("\nType 'exit' to quit\n")
    
    while True:
        try:
            user_input = input("You > ").strip()
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            response = orchestrate(user_input)
            print(f"\n{response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
