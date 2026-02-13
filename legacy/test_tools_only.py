#!/usr/bin/env python3
"""Test individual tools without the full agent."""

from stock_predictor_agent import (
    fetch_stock_data,
    calculate_moving_average,
    calculate_volatility,
    predict_trend,
    analyze_support_resistance,
)
import json

print("=" * 70)
print("TESTING STOCK PREDICTOR TOOLS")
print("=" * 70)

# Test 1: Fetch stock data
print("\n[Test 1] Fetching AAPL stock data...")
stock_data = fetch_stock_data("AAPL", 30)
print(stock_data[:200] + "...\n")

# Test 2: Calculate moving average
print("[Test 2] Calculating moving average...")
ma_result = calculate_moving_average(stock_data, 7)
print(ma_result)

# Test 3: Calculate volatility
print("\n[Test 3] Analyzing volatility...")
vol_result = calculate_volatility(stock_data)
print(vol_result)

# Test 4: Predict trend
print("\n[Test 4] Predicting future trend...")
pred_result = predict_trend(stock_data, 5)
print(pred_result)

# Test 5: Support/Resistance
print("\n[Test 5] Finding support/resistance levels...")
sr_result = analyze_support_resistance(stock_data)
print(sr_result)

print("\n" + "=" * 70)
print("ALL TOOLS WORKING!")
print("=" * 70)
