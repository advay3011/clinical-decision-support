#!/usr/bin/env python3
"""
Quick test script for Portfolio Watchdog Agent
Run individual tools to verify functionality
"""

import sys
sys.path.insert(0, '.')

from agents.portfolio_watchdog_agent import (
    load_config,
    load_portfolio,
    get_stock_price,
    get_news_headlines,
    check_thresholds,
    detect_volume_spike,
    send_alert
)

def test_tools():
    """Test individual tools"""
    print("=" * 60)
    print("Portfolio Watchdog Agent - Tool Testing")
    print("=" * 60)
    
    # Test 1: Load portfolio
    print("\n[1] Testing load_portfolio()...")
    portfolio = load_portfolio()
    print(f"Portfolio: {portfolio}")
    
    if "error" in portfolio:
        print("Error loading portfolio. Exiting.")
        return
    
    tickers = portfolio.get("tickers", [])
    if not tickers:
        print("No tickers found. Exiting.")
        return
    
    # Test with first ticker
    ticker = tickers[0]
    print(f"\nTesting with ticker: {ticker}")
    
    # Test 2: Get stock price
    print(f"\n[2] Testing get_stock_price('{ticker}')...")
    price_data = get_stock_price(ticker)
    print(f"Price Data: {price_data}")
    
    if "error" in price_data:
        print(f"Error fetching price. Skipping threshold tests.")
        return
    
    current_price = price_data.get("current_price")
    
    # Test 3: Check thresholds
    print(f"\n[3] Testing check_thresholds('{ticker}', {current_price})...")
    threshold_data = check_thresholds(ticker, current_price)
    print(f"Threshold Check: {threshold_data}")
    
    # Test 4: Detect volume spike
    print(f"\n[4] Testing detect_volume_spike('{ticker}')...")
    volume_data = detect_volume_spike(ticker)
    print(f"Volume Spike: {volume_data}")
    
    # Test 5: Get news
    print(f"\n[5] Testing get_news_headlines('{ticker}')...")
    news_data = get_news_headlines(ticker)
    print(f"News Headlines: {news_data}")
    
    # Test 6: Send alert
    print(f"\n[6] Testing send_alert()...")
    alert_result = send_alert(f"Test alert for {ticker} at ${current_price}")
    print(f"Alert Result: {alert_result}")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_tools()
