#!/usr/bin/env python3
"""Test the stock predictor agent with sample queries."""

from stock_predictor_agent import agent

# Test queries
test_queries = [
    "Analyze AAPL stock for the last 30 days",
    "What's the trend for GOOGL?",
    "Predict MSFT stock price for the next 5 days",
    "Should I buy or sell TSLA?",
]

print("=" * 70)
print("TESTING STOCK PREDICTOR AGENT")
print("=" * 70)

for i, query in enumerate(test_queries, 1):
    print(f"\n[Test {i}]")
    print(f"Query: {query}")
    print("-" * 70)
    
    try:
        response = agent(query)
        print(f"Response:\n{response}")
    except Exception as e:
        print(f"Error: {e}")
    
    print()

print("=" * 70)
print("TESTS COMPLETE")
print("=" * 70)
