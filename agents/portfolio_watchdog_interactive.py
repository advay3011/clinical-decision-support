#!/usr/bin/env python3
"""
Interactive Portfolio Watchdog Agent
User-friendly CLI interface for portfolio monitoring
"""

import sys
import time
import os
from typing import Optional
sys.path.insert(0, '.')

from agents.portfolio_watchdog_agent import (
    load_config,
    load_portfolio,
    get_stock_price,
    check_thresholds,
    detect_volume_spike,
    get_news_headlines,
    send_alert
)

class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")

def print_menu(options: dict):
    """Print menu options"""
    print(f"\n{Colors.BOLD}Options:{Colors.ENDC}")
    for key, value in options.items():
        print(f"  {Colors.CYAN}{key}{Colors.ENDC}) {value}")
    print()

def get_input(prompt: str) -> str:
    """Get user input"""
    return input(f"{Colors.BOLD}{prompt}{Colors.ENDC} ").strip()

def check_single_ticker():
    """Check a single ticker interactively"""
    print_header("CHECK SINGLE TICKER")
    
    ticker = get_input("Enter ticker symbol (e.g., AAPL):").upper()
    
    if not ticker:
        print_error("Ticker cannot be empty")
        return
    
    print_info(f"Fetching data for {ticker}...")
    
    # Get price
    price_data = get_stock_price(ticker)
    if "error" in price_data:
        print_error(f"Failed to fetch price: {price_data['error']}")
        return
    
    current_price = price_data["current_price"]
    percent_change = price_data["percent_change"]
    volume = price_data["volume"]
    
    print_success(f"Price: ${current_price} ({percent_change:+.2f}%)")
    print_success(f"Volume: {volume:,}")
    
    # Check thresholds
    threshold_data = check_thresholds(ticker, current_price)
    if threshold_data.get("breached"):
        print_warning(f"Threshold breach: {threshold_data['breaches'][0]}")
    else:
        print_success(f"Within thresholds (${threshold_data['thresholds']['low']}-${threshold_data['thresholds']['high']})")
    
    # Check volume
    volume_data = detect_volume_spike(ticker)
    if "error" not in volume_data:
        if volume_data.get("is_spike"):
            print_warning(f"Volume spike: {volume_data['spike_percent']:.2f}% above average")
        else:
            print_success(f"Volume normal ({volume_data['spike_percent']:.2f}% vs 30-day avg)")
    
    # Get news
    print_info("Fetching news headlines...")
    news_data = get_news_headlines(ticker)
    if news_data.get("headlines"):
        print_success(f"Found {news_data['count']} headlines")
        for i, headline in enumerate(news_data["headlines"][:3], 1):
            if headline["title"] and headline["title"] != "N/A":
                print(f"  {i}. {headline['title'][:60]}...")

def check_full_portfolio():
    """Check entire portfolio interactively"""
    print_header("CHECK FULL PORTFOLIO")
    
    portfolio = load_portfolio()
    if "error" in portfolio:
        print_error(f"Failed to load portfolio: {portfolio['error']}")
        return
    
    tickers = portfolio.get("tickers", [])
    print_success(f"Loaded {portfolio['total_tickers']} tickers: {', '.join(tickers)}")
    
    alerts = []
    
    for ticker in tickers:
        print(f"\n{Colors.BOLD}Checking {ticker}...{Colors.ENDC}")
        
        price_data = get_stock_price(ticker)
        if "error" in price_data:
            print_error(f"  Error: {price_data['error']}")
            continue
        
        current_price = price_data["current_price"]
        percent_change = price_data["percent_change"]
        
        print_success(f"  Price: ${current_price} ({percent_change:+.2f}%)")
        
        # Check thresholds
        threshold_data = check_thresholds(ticker, current_price)
        if threshold_data.get("breached"):
            msg = threshold_data['breaches'][0]
            print_warning(f"  {msg}")
            alerts.append(f"[{ticker}] {msg}")
        
        # Check volume
        volume_data = detect_volume_spike(ticker)
        if "error" not in volume_data and volume_data.get("is_spike"):
            msg = f"Volume spike: {volume_data['spike_percent']:.2f}%"
            print_warning(f"  {msg}")
            alerts.append(f"[{ticker}] {msg}")
    
    # Send alerts
    if alerts:
        print(f"\n{Colors.BOLD}Sending {len(alerts)} alert(s)...{Colors.ENDC}")
        for alert in alerts:
            result = send_alert(alert)
            print_success(f"  Alert sent: {result['status']}")
    else:
        print_success("No alerts - portfolio is healthy!")

def view_portfolio_config():
    """View current portfolio configuration"""
    print_header("PORTFOLIO CONFIGURATION")
    
    portfolio = load_portfolio()
    if "error" in portfolio:
        print_error(f"Failed to load portfolio: {portfolio['error']}")
        return
    
    print(f"{Colors.BOLD}Tickers ({portfolio['total_tickers']}):${Colors.ENDC}")
    for ticker in portfolio.get("tickers", []):
        print(f"  • {ticker}")
    
    print(f"\n{Colors.BOLD}Alert Rules:${Colors.ENDC}")
    for ticker, rules in portfolio.get("alert_rules", {}).items():
        print(f"\n  {Colors.CYAN}{ticker}:{Colors.ENDC}")
        print(f"    High threshold: ${rules.get('price_threshold_high', 'N/A')}")
        print(f"    Low threshold: ${rules.get('price_threshold_low', 'N/A')}")
        print(f"    Volume spike %: {rules.get('volume_spike_percent', 'N/A')}%")

def edit_portfolio_config():
    """Edit portfolio configuration"""
    print_header("EDIT PORTFOLIO CONFIGURATION")
    
    print_info("Opening config.yaml in editor...")
    print_info("Edit the file and save to apply changes")
    
    editor = os.environ.get('EDITOR', 'nano')
    os.system(f"{editor} config.yaml")
    
    # Reload config
    load_config()
    print_success("Configuration reloaded!")

def add_ticker():
    """Add a new ticker to portfolio"""
    print_header("ADD TICKER")
    
    ticker = get_input("Enter ticker symbol (e.g., AAPL):").upper()
    if not ticker:
        print_error("Ticker cannot be empty")
        return
    
    high = get_input("Enter high price threshold (e.g., 250):")
    low = get_input("Enter low price threshold (e.g., 150):")
    volume = get_input("Enter volume spike % (e.g., 50):")
    
    try:
        high = float(high)
        low = float(low)
        volume = float(volume)
    except ValueError:
        print_error("Invalid input - please enter numbers")
        return
    
    # Read current config
    import yaml
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Add ticker
    if ticker not in config['portfolio']['tickers']:
        config['portfolio']['tickers'].append(ticker)
    
    config['alert_rules'][ticker] = {
        'price_threshold_high': high,
        'price_threshold_low': low,
        'volume_spike_percent': volume
    }
    
    # Write back
    with open('config.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    load_config()
    print_success(f"Added {ticker} to portfolio!")

def remove_ticker():
    """Remove a ticker from portfolio"""
    print_header("REMOVE TICKER")
    
    portfolio = load_portfolio()
    tickers = portfolio.get("tickers", [])
    
    print(f"{Colors.BOLD}Current tickers:${Colors.ENDC}")
    for i, ticker in enumerate(tickers, 1):
        print(f"  {i}) {ticker}")
    
    choice = get_input("Enter number to remove (or 'cancel'):")
    
    if choice.lower() == 'cancel':
        return
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(tickers):
            ticker = tickers[idx]
            
            import yaml
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f)
            
            config['portfolio']['tickers'].remove(ticker)
            if ticker in config['alert_rules']:
                del config['alert_rules'][ticker]
            
            with open('config.yaml', 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            load_config()
            print_success(f"Removed {ticker} from portfolio!")
        else:
            print_error("Invalid selection")
    except ValueError:
        print_error("Invalid input")

def continuous_monitoring():
    """Run continuous monitoring"""
    print_header("CONTINUOUS MONITORING")
    
    interval = get_input("Enter check interval in seconds (default 300):")
    try:
        interval = int(interval) if interval else 300
    except ValueError:
        interval = 300
    
    print_info(f"Starting continuous monitoring (every {interval} seconds)")
    print_info("Press Ctrl+C to stop\n")
    
    cycle = 0
    try:
        while True:
            cycle += 1
            print(f"{Colors.BOLD}Cycle {cycle} - {time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
            
            portfolio = load_portfolio()
            tickers = portfolio.get("tickers", [])
            
            alerts = []
            for ticker in tickers:
                price_data = get_stock_price(ticker)
                if "error" not in price_data:
                    current_price = price_data["current_price"]
                    threshold_data = check_thresholds(ticker, current_price)
                    
                    if threshold_data.get("breached"):
                        alerts.append(f"[{ticker}] {threshold_data['breaches'][0]}")
            
            if alerts:
                print_warning(f"Found {len(alerts)} alert(s)")
                for alert in alerts:
                    send_alert(alert)
            else:
                print_success("No alerts")
            
            print_info(f"Next check in {interval} seconds...")
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print_info("\nMonitoring stopped")

def view_logs():
    """View recent logs"""
    print_header("RECENT ALERTS")
    
    if not os.path.exists('portfolio_alerts.log'):
        print_info("No logs yet")
        return
    
    with open('portfolio_alerts.log', 'r') as f:
        lines = f.readlines()
    
    # Show last 20 lines
    recent = lines[-20:] if len(lines) > 20 else lines
    
    for line in recent:
        if 'WARNING' in line:
            print_warning(line.strip())
        elif 'ERROR' in line:
            print_error(line.strip())
        else:
            print_info(line.strip())

def run_tests():
    """Run test suite"""
    print_header("RUNNING TESTS")
    
    print_info("Running comprehensive test suite...")
    os.system("python agents/test_portfolio_comprehensive.py 2>&1 | tail -20")

def main_menu():
    """Main interactive menu"""
    while True:
        clear_screen()
        print_header("PORTFOLIO WATCHDOG - INTERACTIVE CLI")
        
        options = {
            "1": "Check single ticker",
            "2": "Check full portfolio",
            "3": "View portfolio configuration",
            "4": "Add ticker",
            "5": "Remove ticker",
            "6": "Edit configuration",
            "7": "Continuous monitoring",
            "8": "View recent alerts",
            "9": "Run tests",
            "0": "Exit"
        }
        
        print_menu(options)
        choice = get_input("Select option:")
        
        if choice == "1":
            check_single_ticker()
        elif choice == "2":
            check_full_portfolio()
        elif choice == "3":
            view_portfolio_config()
        elif choice == "4":
            add_ticker()
        elif choice == "5":
            remove_ticker()
        elif choice == "6":
            edit_portfolio_config()
        elif choice == "7":
            continuous_monitoring()
        elif choice == "8":
            view_logs()
        elif choice == "9":
            run_tests()
        elif choice == "0":
            print_success("Goodbye!")
            break
        else:
            print_error("Invalid option")
        
        if choice != "7":  # Don't pause after continuous monitoring
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

if __name__ == "__main__":
    try:
        load_config()
        main_menu()
    except KeyboardInterrupt:
        print_info("\nExiting...")
    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)
