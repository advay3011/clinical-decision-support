#!/usr/bin/env python3
"""
Portfolio Watchdog Chatbot
Interactive chatbot with integrated portfolio monitoring
"""

import sys
import re
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

class PortfolioWatchdogChatbot:
    """Chatbot for portfolio monitoring"""
    
    def __init__(self):
        """Initialize chatbot"""
        load_config()
        self.portfolio = load_portfolio()
        self.knowledge_base = self._build_knowledge_base()
    
    def _build_knowledge_base(self) -> dict:
        """Build knowledge base for Q&A"""
        return {
            "threshold": {
                "keywords": ["threshold", "limit", "breach", "alert rule"],
                "response": """A threshold is a price limit you set for a stock. 
• High threshold: Alert if price goes ABOVE this value
• Low threshold: Alert if price goes BELOW this value

Example: If AAPL high threshold is $250, you'll get an alert if AAPL price exceeds $250.
This helps you catch significant price movements automatically."""
            },
            "volume spike": {
                "keywords": ["volume spike", "volume", "unusual volume", "volume alert"],
                "response": """A volume spike is when trading volume is unusually high compared to normal.
• We compare today's volume to the 30-day average
• If today's volume exceeds the threshold (e.g., 50%), we alert you
• High volume often indicates important news or market movement

Example: If AAPL average volume is 50M shares, and today it's 75M (50% spike), you'll get an alert."""
            },
            "portfolio": {
                "keywords": ["portfolio", "what stocks", "tickers", "monitoring"],
                "response": f"""Your portfolio currently has {self.portfolio['total_tickers']} tickers:
{', '.join(self.portfolio['tickers'])}

Each ticker has custom alert rules for price thresholds and volume spikes.
You can add or remove tickers anytime."""
            },
            "alert": {
                "keywords": ["alert", "notification", "warning", "slack"],
                "response": """Alerts are notifications sent when something important happens:
• Price threshold breach (high or low)
• Volume spike detected
• Unusual market activity

Alerts can be sent to:
• Slack (if webhook configured)
• Log file (dry-run mode)

You can view recent alerts with option 8."""
            },
            "how to": {
                "keywords": ["how to", "how do i", "how can i", "help"],
                "response": """Here are common tasks:

1. Check a ticker: Type '1' then enter ticker symbol
2. Check full portfolio: Type '2'
3. Add new ticker: Type '4'
4. Remove ticker: Type '5'
5. Monitor continuously: Type '7'
6. View alerts: Type '8'
7. Run tests: Type '9'

Or just ask me questions! I can explain any feature."""
            },
            "price": {
                "keywords": ["price", "current price", "stock price", "cost"],
                "response": """To check a stock's current price:
1. Type '1' to check a single ticker
2. Enter the ticker symbol (e.g., AAPL)
3. I'll show you:
   • Current price
   • Price change %
   • Trading volume
   • Threshold status
   • News headlines"""
            },
            "configure": {
                "keywords": ["configure", "config", "setup", "settings", "change"],
                "response": """To configure your portfolio:

Option 4: Add a new ticker
• Enter ticker symbol
• Set high price threshold
• Set low price threshold
• Set volume spike sensitivity

Option 5: Remove a ticker
• Select from list

Option 6: Edit configuration
• Opens config.yaml in your editor
• Make manual changes
• Changes apply immediately"""
            },
            "continuous": {
                "keywords": ["continuous", "monitoring", "background", "24/7"],
                "response": """Continuous monitoring runs checks automatically:

Option 7: Continuous monitoring
• Set check interval (default 300 seconds)
• Agent checks portfolio every N seconds
• Alerts sent automatically
• Press Ctrl+C to stop

Or run: python agents/portfolio_watchdog_agent.py
This runs indefinitely with 5-minute intervals."""
            },
            "test": {
                "keywords": ["test", "verify", "check setup", "working"],
                "response": """To verify everything is working:

Option 9: Run tests
• Executes 35 comprehensive tests
• Checks all tools
• Validates data
• Tests error handling

Or run: python agents/test_portfolio_comprehensive.py

All tests should pass ✓"""
            },
            "slack": {
                "keywords": ["slack", "webhook", "notification", "send alert"],
                "response": """To enable Slack alerts:

1. Create Slack webhook: https://api.slack.com/messaging/webhooks
2. Edit config.yaml:
   slack:
     webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
     dry_run: false
3. Restart the agent

Alerts will now be sent to your Slack channel!"""
            },
            "news": {
                "keywords": ["news", "headlines", "context", "information"],
                "response": """News headlines provide context for price movements:

When you check a ticker, we fetch recent news headlines.
This helps you understand WHY a stock is moving.

Example: If AAPL price spikes, we show you recent news about Apple
to help you understand the reason for the movement."""
            },
        }
    
    def print_menu(self):
        """Print menu options"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}Options:{Colors.ENDC}")
        print("  1) Check single ticker")
        print("  2) Check full portfolio")
        print("  3) View portfolio configuration")
        print("  4) Add ticker")
        print("  5) Remove ticker")
        print("  6) Edit configuration")
        print("  7) Continuous monitoring")
        print("  8) View recent alerts")
        print("  9) Run tests")
        print("  0) Exit")
    
    def find_answer(self, query: str) -> Optional[str]:
        """Find answer in knowledge base"""
        query_lower = query.lower()
        
        # Check each topic in knowledge base
        for topic, data in self.knowledge_base.items():
            for keyword in data["keywords"]:
                if keyword in query_lower:
                    return data["response"]
        
        return None
    
    def handle_query(self, query: str) -> bool:
        """Handle user query. Returns True if should continue, False if exit"""
        query = query.strip()
        
        # Check if it's a menu option
        if query in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return self.handle_menu_option(query)
        
        # Check if it's a question
        if "?" in query or any(word in query.lower() for word in ["what", "how", "why", "when", "where", "who"]):
            answer = self.find_answer(query)
            if answer:
                print(f"\n{Colors.GREEN}💡 {answer}{Colors.ENDC}")
                return True
            else:
                print(f"\n{Colors.YELLOW}I'm not sure about that. Try asking about:")
                print("  • Thresholds")
                print("  • Volume spikes")
                print("  • Portfolio")
                print("  • Alerts")
                print("  • How to use features")
                print("  • Slack integration")
                print("  • News headlines")
                print("  • Testing{Colors.ENDC}")
                return True
        
        # Check for commands
        if query.lower() in ["help", "menu", "options"]:
            self.print_menu()
            return True
        
        if query.lower() in ["exit", "quit", "bye"]:
            print(f"\n{Colors.GREEN}Goodbye! Happy monitoring! 📈{Colors.ENDC}\n")
            return False
        
        # Try to interpret as ticker check
        if len(query) <= 5 and query.isupper():
            return self.check_ticker(query)
        
        # Default response
        print(f"\n{Colors.YELLOW}I didn't understand that. You can:")
        print("  • Type a number (1-9) for menu options")
        print("  • Ask me a question (e.g., 'what is a threshold?')")
        print("  • Type a ticker symbol (e.g., 'AAPL')")
        print("  • Type 'help' for menu{Colors.ENDC}")
        
        return True
    
    def handle_menu_option(self, option: str) -> bool:
        """Handle menu option"""
        if option == "0":
            print(f"\n{Colors.GREEN}Goodbye! Happy monitoring! 📈{Colors.ENDC}\n")
            return False
        
        elif option == "1":
            ticker = input(f"\n{Colors.BOLD}Enter ticker symbol (e.g., AAPL): {Colors.ENDC}").upper()
            self.check_ticker(ticker)
        
        elif option == "2":
            self.check_full_portfolio()
        
        elif option == "3":
            self.view_portfolio_config()
        
        elif option == "4":
            self.add_ticker()
        
        elif option == "5":
            self.remove_ticker()
        
        elif option == "6":
            self.edit_config()
        
        elif option == "7":
            self.continuous_monitoring()
        
        elif option == "8":
            self.view_logs()
        
        elif option == "9":
            self.run_tests()
        
        return True
    
    def check_ticker(self, ticker: str) -> bool:
        """Check single ticker"""
        print(f"\n{Colors.BOLD}Checking {ticker}...{Colors.ENDC}")
        
        price_data = get_stock_price(ticker)
        if "error" in price_data:
            print(f"{Colors.RED}✗ Error: {price_data['error']}{Colors.ENDC}")
            return True
        
        current_price = price_data["current_price"]
        percent_change = price_data["percent_change"]
        volume = price_data["volume"]
        
        print(f"{Colors.GREEN}✓ Price: ${current_price} ({percent_change:+.2f}%){Colors.ENDC}")
        print(f"{Colors.GREEN}✓ Volume: {volume:,}{Colors.ENDC}")
        
        threshold_data = check_thresholds(ticker, current_price)
        if threshold_data.get("breached"):
            print(f"{Colors.YELLOW}⚠ {threshold_data['breaches'][0]}{Colors.ENDC}")
        else:
            print(f"{Colors.GREEN}✓ Within thresholds (${threshold_data['thresholds']['low']}-${threshold_data['thresholds']['high']}){Colors.ENDC}")
        
        volume_data = detect_volume_spike(ticker)
        if "error" not in volume_data:
            if volume_data.get("is_spike"):
                print(f"{Colors.YELLOW}⚠ Volume spike: {volume_data['spike_percent']:.2f}%{Colors.ENDC}")
            else:
                print(f"{Colors.GREEN}✓ Volume normal ({volume_data['spike_percent']:.2f}% vs 30-day avg){Colors.ENDC}")
        
        return True
    
    def check_full_portfolio(self) -> bool:
        """Check full portfolio"""
        print(f"\n{Colors.BOLD}Checking full portfolio...{Colors.ENDC}")
        
        tickers = self.portfolio.get("tickers", [])
        alerts = []
        
        for ticker in tickers:
            price_data = get_stock_price(ticker)
            if "error" in price_data:
                print(f"{Colors.RED}✗ {ticker}: Error{Colors.ENDC}")
                continue
            
            current_price = price_data["current_price"]
            threshold_data = check_thresholds(ticker, current_price)
            
            if threshold_data.get("breached"):
                print(f"{Colors.YELLOW}⚠ {ticker}: {threshold_data['breaches'][0]}{Colors.ENDC}")
                alerts.append(f"[{ticker}] {threshold_data['breaches'][0]}")
            else:
                print(f"{Colors.GREEN}✓ {ticker}: ${current_price}{Colors.ENDC}")
        
        if alerts:
            print(f"\n{Colors.BOLD}Sending {len(alerts)} alert(s)...{Colors.ENDC}")
            for alert in alerts:
                send_alert(alert)
                print(f"{Colors.GREEN}✓ Alert sent{Colors.ENDC}")
        
        return True
    
    def view_portfolio_config(self) -> bool:
        """View portfolio configuration"""
        print(f"\n{Colors.BOLD}Portfolio Configuration:{Colors.ENDC}")
        print(f"\n{Colors.CYAN}Tickers ({self.portfolio['total_tickers']}):${Colors.ENDC}")
        for ticker in self.portfolio.get("tickers", []):
            print(f"  • {ticker}")
        
        print(f"\n{Colors.CYAN}Alert Rules:${Colors.ENDC}")
        for ticker, rules in self.portfolio.get("alert_rules", {}).items():
            print(f"\n  {Colors.BOLD}{ticker}:{Colors.ENDC}")
            print(f"    High: ${rules.get('price_threshold_high', 'N/A')}")
            print(f"    Low: ${rules.get('price_threshold_low', 'N/A')}")
            print(f"    Volume spike: {rules.get('volume_spike_percent', 'N/A')}%")
        
        return True
    
    def add_ticker(self) -> bool:
        """Add ticker"""
        ticker = input(f"\n{Colors.BOLD}Enter ticker symbol: {Colors.ENDC}").upper()
        high = input(f"{Colors.BOLD}Enter high threshold: {Colors.ENDC}")
        low = input(f"{Colors.BOLD}Enter low threshold: {Colors.ENDC}")
        volume = input(f"{Colors.BOLD}Enter volume spike %: {Colors.ENDC}")
        
        try:
            import yaml
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f)
            
            if ticker not in config['portfolio']['tickers']:
                config['portfolio']['tickers'].append(ticker)
            
            config['alert_rules'][ticker] = {
                'price_threshold_high': float(high),
                'price_threshold_low': float(low),
                'volume_spike_percent': float(volume)
            }
            
            with open('config.yaml', 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            load_config()
            self.portfolio = load_portfolio()
            print(f"{Colors.GREEN}✓ Added {ticker} to portfolio!{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}✗ Error: {e}{Colors.ENDC}")
        
        return True
    
    def remove_ticker(self) -> bool:
        """Remove ticker"""
        tickers = self.portfolio.get("tickers", [])
        print(f"\n{Colors.BOLD}Current tickers:${Colors.ENDC}")
        for i, ticker in enumerate(tickers, 1):
            print(f"  {i}) {ticker}")
        
        choice = input(f"\n{Colors.BOLD}Enter number to remove: {Colors.ENDC}")
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
                self.portfolio = load_portfolio()
                print(f"{Colors.GREEN}✓ Removed {ticker}!{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}✗ Error: {e}{Colors.ENDC}")
        
        return True
    
    def edit_config(self) -> bool:
        """Edit configuration"""
        import os
        editor = os.environ.get('EDITOR', 'nano')
        os.system(f"{editor} config.yaml")
        load_config()
        self.portfolio = load_portfolio()
        print(f"{Colors.GREEN}✓ Configuration reloaded!{Colors.ENDC}")
        return True
    
    def continuous_monitoring(self) -> bool:
        """Continuous monitoring"""
        import time
        interval = input(f"\n{Colors.BOLD}Enter interval in seconds (default 300): {Colors.ENDC}")
        try:
            interval = int(interval) if interval else 300
        except:
            interval = 300
        
        print(f"{Colors.GREEN}Starting continuous monitoring (every {interval}s)...{Colors.ENDC}")
        print(f"{Colors.YELLOW}Press Ctrl+C to stop{Colors.ENDC}\n")
        
        try:
            cycle = 0
            while True:
                cycle += 1
                print(f"{Colors.BOLD}Cycle {cycle}{Colors.ENDC}")
                self.check_full_portfolio()
                print(f"{Colors.YELLOW}Next check in {interval}s...{Colors.ENDC}\n")
                time.sleep(interval)
        except KeyboardInterrupt:
            print(f"\n{Colors.GREEN}Monitoring stopped{Colors.ENDC}")
        
        return True
    
    def view_logs(self) -> bool:
        """View logs"""
        import os
        if not os.path.exists('portfolio_alerts.log'):
            print(f"{Colors.YELLOW}No logs yet{Colors.ENDC}")
            return True
        
        with open('portfolio_alerts.log', 'r') as f:
            lines = f.readlines()
        
        recent = lines[-20:] if len(lines) > 20 else lines
        
        print(f"\n{Colors.BOLD}Recent Alerts:{Colors.ENDC}")
        for line in recent:
            if 'WARNING' in line:
                print(f"{Colors.YELLOW}{line.strip()}{Colors.ENDC}")
            elif 'ERROR' in line:
                print(f"{Colors.RED}{line.strip()}{Colors.ENDC}")
            else:
                print(f"{Colors.BLUE}{line.strip()}{Colors.ENDC}")
        
        return True
    
    def run_tests(self) -> bool:
        """Run tests"""
        import os
        print(f"\n{Colors.BOLD}Running tests...{Colors.ENDC}\n")
        os.system("python agents/test_portfolio_comprehensive.py 2>&1 | tail -30")
        return True
    
    def run(self):
        """Run chatbot"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'PORTFOLIO WATCHDOG - CHATBOT'.center(70)}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
        
        print(f"\n{Colors.GREEN}Hi! I'm your Portfolio Watchdog chatbot.{Colors.ENDC}")
        print(f"{Colors.GREEN}I can help you monitor your portfolio and answer questions.{Colors.ENDC}")
        print(f"{Colors.GREEN}Type a number (1-9) for menu options, or ask me anything!{Colors.ENDC}")
        
        self.print_menu()
        
        while True:
            user_input = input(f"\n{Colors.BOLD}{Colors.CYAN}You: {Colors.ENDC}").strip()
            
            if not user_input:
                continue
            
            if not self.handle_query(user_input):
                break
            
            self.print_menu()

if __name__ == "__main__":
    try:
        chatbot = PortfolioWatchdogChatbot()
        chatbot.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}Goodbye!{Colors.ENDC}\n")
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.ENDC}")
        sys.exit(1)
