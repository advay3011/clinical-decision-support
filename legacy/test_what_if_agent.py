#!/usr/bin/env python3
"""
Test script for What-If Scenario Agent
Run different scenarios and see the analysis
"""

from what_if_scenario_agent import WhatIfScenarioOrchestrator
import json

def test_scenario(scenario_text):
    """Test a single scenario"""
    print("\n" + "="*70)
    print(f"TESTING: {scenario_text}")
    print("="*70)
    
    orchestrator = WhatIfScenarioOrchestrator()
    result = orchestrator.run_workflow(scenario_text)
    
    # Print key findings
    print("\n" + "-"*70)
    print("KEY FINDINGS:")
    print("-"*70)
    
    if "stages" in result and "stage_2" in result["stages"]:
        domains = result["stages"]["stage_2"]["impacted_domains"]
        print(f"\nDomains affected: {len(domains)}")
        for domain in domains:
            print(f"  • {domain}")
    
    if "stages" in result and "stage_5" in result["stages"]:
        rankings = result["stages"]["stage_5"]["rankings"]
        print(f"\nSeverity rankings:")
        for domain, data in rankings.items():
            print(f"  • {domain}: {data['score']}/5 ({data['level']})")
    
    return result

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════╗
║              WHAT-IF SCENARIO AGENT - TEST SUITE                  ║
║                                                                    ║
║  Testing different hypothetical scenarios                         ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Test scenarios
    scenarios = [
        "What if fossil fuels were banned tomorrow?",
        "What if a major earthquake hit Tokyo?",
        "What if all cars became autonomous?",
    ]
    
    results = {}
    for scenario in scenarios:
        results[scenario] = test_scenario(scenario)
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETE")
    print("="*70)
    print(f"\nTested {len(scenarios)} scenarios")
    print("\nTo test your own scenario, run:")
    print("  orchestrator = WhatIfScenarioOrchestrator()")
    print('  result = orchestrator.run_workflow("Your scenario here")')
