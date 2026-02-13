#!/usr/bin/env python3.11
"""
What-If Scenario Agent - Interactive Runner with Real LLM Analysis
Uses Ollama + Llama 2 directly for intelligent analysis
"""

import json
import requests
from what_if_scenario_agent import WhatIfScenarioOrchestrator

def call_llama(prompt: str) -> str:
    """Call Llama 2 via Ollama for intelligent analysis."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2:latest",
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Connection error: {e}"

def enhance_scenario_analysis(scenario: str, orchestrator_output: dict) -> str:
    """Use LLM to enhance the orchestrator output with real reasoning."""
    
    prompt = f"""Analyze this hypothetical scenario and provide detailed reasoning:

SCENARIO: {scenario}

Based on this scenario, provide:
1. Key immediate impacts (first 24 hours)
2. Secondary effects (days 1-7)
3. Long-term consequences (weeks+)
4. Most vulnerable populations/systems
5. Potential recovery strategies

Be specific and detailed. Think through the cascading effects."""

    print("\n[LLM Analysis in progress...]")
    analysis = call_llama(prompt)
    return analysis

def main():
    print("\n" + "="*70)
    print("WHAT-IF SCENARIO AGENT - INTERACTIVE MODE")
    print("="*70)
    print("\nInitializing agent...\n")
    
    orchestrator = WhatIfScenarioOrchestrator()
    
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
            # Run orchestrator for structured analysis
            print("\n[Running 6-stage workflow...]")
            structured_output = orchestrator.run_workflow(scenario)
            
            # Enhance with LLM reasoning
            llm_analysis = enhance_scenario_analysis(scenario, structured_output)
            
            print("\n" + "-"*70)
            print("ENHANCED LLM ANALYSIS:")
            print("-"*70)
            print(llm_analysis)
            
            print("\n" + "-"*70)
            print("STRUCTURED WORKFLOW OUTPUT:")
            print("-"*70)
            print(json.dumps(structured_output, indent=2)[:1000] + "...")
            
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n")

if __name__ == "__main__":
    main()
