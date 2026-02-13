#!/usr/bin/env python3
"""
Portfolio Watchdog Agent Demo
Demonstrates the agent checking a portfolio and sending alerts
"""

import sys
import time
sys.path.insert(0, '.')

from agents.portfolio_watchdog_agent import (
    load_config,
    load_portfolio,
    get_stock_price,
    check_thresholds,
    detect_volume_spike,
    send_alert
)

def demo_single_check():
    """Run a single portfolio check cycle"""
    print("\n" + "=" * 70)
    print("PORTFOLIO WATCHDOG - SINGLE CHECK CYCLE")
    print("=" * 70)
    
    # Load portfolio
    print("\n[STEP 1] Loading portfolio configuration...")
    portfolio = load_portfolio()
    
    if "error" in portfolio:
        print(f"ERROR: {portfolio['error']}")
        return
    
    tickers = portfolio.get("tickers", [])
    print(f"✓ Portfolio loaded with {portfolio['total_tickers']} tickers: {', '.join(tickers)}")
    
    # Check each ticker
    alerts_triggered = []
    
    for ticker in tickers:
        print(f"\n[STEP 2] Checking {ticker}...")
        
        # Get price
        price_data = get_stock_price(ticker)
        if "error" in price_data:
            print(f"  ✗ Error fetching price: {price_data['error']}")
            continue
        
        current_price = price_data["current_price"]
        percent_change = price_data["percent_change"]
        volume = price_data["volume"]
        
        print(f"  ✓ Price: ${current_price} ({percent_change:+.2f}%)")
        print(f"  ✓ Volume: {volume:,}")
        
        # Check thresholds
        threshold_data = check_thresholds(ticker, current_price)
        if threshold_data.get("breached"):
            print(f"  ⚠ THRESHOLD BREACH: {threshold_data['breaches'][0]}")
            alerts_triggered.append({
                "ticker": ticker,
                "type": "threshold",
                "message": threshold_data['breaches'][0]
            })
        else:
            print(f"  ✓ Within thresholds (${threshold_data['thresholds']['low']}-${threshold_data['thresholds']['high']})")
        
        # Check volume spike
        volume_data = detect_volume_spike(ticker)
        if "error" not in volume_data:
            if volume_data.get("is_spike"):
                print(f"  ⚠ VOLUME SPIKE: {volume_data['spike_percent']:.2f}% above 30-day average")
                alerts_triggered.append({
                    "ticker": ticker,
                    "type": "volume",
                    "message": f"Volume spike: {volume_data['spike_percent']:.2f}% above average"
                })
            else:
                print(f"  ✓ Volume normal ({volume_data['spike_percent']:.2f}% vs 30-day avg)")
    
    # Send alerts if any triggered
    print("\n" + "-" * 70)
    if alerts_triggered:
        print(f"\n[STEP 3] Sending {len(alerts_triggered)} alert(s)...")
        for alert in alerts_triggered:
            message = f"[{alert['ticker']}] {alert['message']}"
            result = send_alert(message)
            print(f"  ✓ Alert sent: {result['status']} ({result['mode']})")
    else:
        print("\n[STEP 3] No alerts to send - portfolio is healthy!")
    
    print("\n" + "=" * 70)
    print("CHECK CYCLE COMPLETE")
    print("=" * 70)

def demo_continuous_monitoring():
    """Run continuous monitoring (limited to 3 cycles for demo)"""
    print("\n" + "=" * 70)
    print("PORTFOLIO WATCHDOG - CONTINUOUS MONITORING (3 cycles)")
    print("=" * 70)
    
    for cycle in range(1, 4):
        print(f"\n>>> CYCLE {cycle}/3 - {time.strftime('%Y-%m-%d %H:%M:%S')}")
        demo_single_check()
        
        if cycle < 3:
            print("\nWaiting 10 seconds before next cycle...")
            time.sleep(10)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Portfolio Watchdog Agent Demo")
    parser.add_argument(
        "--mode",
        choices=["single", "continuous"],
        default="single",
        help="Run mode: single check or continuous monitoring"
    )
    
    args = parser.parse_args()
    
    if args.mode == "continuous":
        demo_continuous_monitoring()
    else:
        demo_single_check()
