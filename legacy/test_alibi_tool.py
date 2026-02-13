#!/usr/bin/env python3
"""Test the alibi tool."""

from stock_predictor_agent import fetch_stock_data, analyze_price_movement
import json

print("=" * 70)
print("TESTING ALIBI AGENT - PRICE MOVEMENT EXPLANATIONS")
print("=" * 70)

# Fetch stock data
print("\n[Step 1] Fetching TSLA stock data...")
stock_data = fetch_stock_data("TSLA", 30)

# Analyze price movements
print("\n[Step 2] Analyzing why the price moved...")
alibi_result = analyze_price_movement(stock_data, 5)

# Pretty print
result = json.loads(alibi_result)
print(json.dumps(result, indent=2))

print("\n" + "=" * 70)
print("ALIBI ANALYSIS COMPLETE")
print("=" * 70)
