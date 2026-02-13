#!/usr/bin/env python3.11
"""
What-If Scenario Agent - Interactive Runner
Uses Method 2 (LLM-driven Strands Agent)
"""

import json
from what_if_scenario_agent import create_what_if_agent

def main():
    print("\n" + "="*70)
    print("WHAT-IF SCENARIO AGENT - INTERACTIVE MODE")
    print("="*70)
    print("\nCreating agent with Llama 2...\n")
    
    agent = create_what_if_agent()
    
    scenarios = [
        "What if fossil fuels were banned tomorrow?",
        "What if a major earthquake hit Tokyo?",
        "What if all cars became autonomous?",
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print("\n" + "█"*70)
        print(f"SCENARIO {i}: {scenario}")
        print("█"*70)
        
        try:
            print("\nAgent is analyzing...\n")
            response = agent(scenario)
            
            print("\n" + "-"*70)
            print("AGENT RESPONSE:")
            print("-"*70)
            print(response)
            
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n")

if __name__ == "__main__":
    main()
