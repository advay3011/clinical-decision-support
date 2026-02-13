#!/usr/bin/env python3
"""
Portfolio Watchdog Conversational Chatbot
Friendly, conversational AI assistant for portfolio monitoring
"""

import sys
import re
import random
from datetime import datetime
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

class ConversationalChatbot:
    """Conversational chatbot for portfolio monitoring"""
    
    def __init__(self):
        """Initialize chatbot"""
        load_config()
        self.portfolio = load_portfolio()
        self.user_name = None
        self.conversation_count = 0
        
        # Company name to ticker mapping
        self.company_to_ticker = {
            "apple": "AAPL",
            "google": "GOOGL",
            "alphabet": "GOOGL",
            "microsoft": "MSFT",
            "tesla": "TSLA",
            "amazon": "AMZN",
            "meta": "META",
            "facebook": "META",
            "nvidia": "NVDA",
            "netflix": "NFLX",
            "twitter": "TWTR",
            "x": "TWTR",
            "intel": "INTC",
            "amd": "AMD",
            "qualcomm": "QCOM",
            "cisco": "CSCO",
            "ibm": "IBM",
            "oracle": "ORCL",
            "salesforce": "CRM",
            "adobe": "ADBE",
            "paypal": "PYPL",
            "square": "SQ",
            "stripe": "STRIPE",
            "uber": "UBER",
            "lyft": "LYFT",
            "airbnb": "ABNB",
            "zoom": "ZM",
            "slack": "SLACK",
            "shopify": "SHOP",
            "spotify": "SPOT",
            "pinterest": "PINS",
            "snapchat": "SNAP",
            "tiktok": "TIKTOK",
            "discord": "DISCORD",
            "roblox": "RBLX",
            "coinbase": "COIN",
            "robinhood": "HOOD",
            "gamestop": "GME",
            "amc": "AMC",
            "boeing": "BA",
            "lockheed": "LMT",
            "raytheon": "RTX",
            "general dynamics": "GD",
            "northrop": "NOC",
            "exxon": "XOM",
            "chevron": "CVX",
            "shell": "SHEL",
            "bp": "BP",
            "saudi aramco": "2222.SR",
            "coca cola": "KO",
            "pepsi": "PEP",
            "mcdonalds": "MCD",
            "starbucks": "SBUX",
            "walmart": "WMT",
            "target": "TGT",
            "costco": "COST",
            "home depot": "HD",
            "lowes": "LOW",
            "nike": "NKE",
            "adidas": "ADDYY",
            "lululemon": "LULU",
            "gap": "GPS",
            "h&m": "HNNMY",
            "zara": "IDEXY",
            "uniqlo": "UNIQF",
            "johnson & johnson": "JNJ",
            "pfizer": "PFE",
            "moderna": "MRNA",
            "astrazeneca": "AZN",
            "merck": "MRK",
            "eli lilly": "LLY",
            "bristol myers": "BMY",
            "abbvie": "ABBV",
            "amgen": "AMGN",
            "gilead": "GILD",
            "regeneron": "REGN",
            "vertex": "VRTX",
            "biogen": "BIIB",
            "incyte": "INCY",
            "seagen": "SGEN",
            "bluebird": "BLUE",
            "crispr": "CRSP",
            "editas": "EDIT",
            "intellia": "NTLA",
            "beam": "BEAM",
            "sangamo": "SGMO",
            "exonics": "EXON",
            "translate": "TRNSL",
            "geron": "GERN",
            "fate": "FATE",
            "juno": "JUNO",
            "kite": "KITE",
            "bluerock": "BLUA",
            "arcus": "ARCUS",
            "jounce": "JOUNCE",
            "tmunity": "TMUNITY",
            "eureka": "EURK",
            "forty seven": "FTSV",
            "jounce": "JOUNCE",
            "tmunity": "TMUNITY",
        }
        
        # Conversational responses
        self.greetings = [
            "Hey there! 👋 How's your day going?",
            "Hello! Great to see you! How are you doing?",
            "Hi! Welcome back! How's everything?",
            "Hey! Good to see you! What's up?",
        ]
        
        self.small_talk = {
            "how are you": [
                "I'm doing great, thanks for asking! Ready to help you with your portfolio. 😊",
                "Doing fantastic! I'm here to help you make smart investment decisions.",
                "I'm all good! Excited to help you monitor your stocks today.",
            ],
            "what's up": [
                "Just here monitoring the markets and ready to help you! 📈",
                "Not much, just keeping an eye on your portfolio. How about you?",
                "All good! Ready to check your stocks whenever you are.",
            ],
            "how's it going": [
                "Going great! Your portfolio is looking good. Want me to check it?",
                "Pretty good! Markets are active today. Anything you want to check?",
                "Excellent! Ready to help you with your investments.",
            ],
            "thanks": [
                "You're welcome! Happy to help! 😊",
                "Anytime! That's what I'm here for.",
                "My pleasure! Let me know if you need anything else.",
            ],
            "bye": [
                "See you later! Happy investing! 📈",
                "Goodbye! Keep an eye on those stocks!",
                "Take care! Come back anytime you need portfolio help!",
            ],
        }
        
        self.suggestions = [
            "💡 Tip: You have 5 tickers monitored. Want me to check them all?",
            "💡 Suggestion: Your AAPL threshold is $250. Want to adjust it?",
            "💡 Did you know? Volume spikes can indicate important news. Check option 2!",
            "💡 Pro tip: You can add more tickers to diversify your monitoring.",
            "💡 Reminder: Your alerts are in dry-run mode. Enable Slack for real notifications!",
            "💡 Suggestion: Run tests (option 9) to verify everything is working perfectly.",
            "💡 Did you know? You can monitor continuously with option 7.",
            "💡 Tip: Check recent alerts (option 8) to see what's been happening.",
        ]
        
        # Explanations for options
        self.option_explanations = {
            "1": {
                "title": "Check a Single Ticker",
                "simple": "Pick one stock (like AAPL or GOOGL) and I'll show you its current price, whether it's up or down, and if any alerts are triggered.",
                "details": "I'll fetch the live price, compare it to your thresholds, check for volume spikes, and show you recent news about that stock."
            },
            "2": {
                "title": "Check My Full Portfolio",
                "simple": "I'll check ALL your stocks at once and show you which ones are healthy and which ones have alerts.",
                "details": "Perfect for a quick overview! I'll check all 5 tickers, show you prices, and automatically send any alerts that are triggered."
            },
            "3": {
                "title": "View My Portfolio Configuration",
                "simple": "See all the stocks you're monitoring and the alert rules you've set for each one.",
                "details": "Shows your tickers, high/low price thresholds, and volume spike sensitivity for each stock."
            },
            "4": {
                "title": "Add a New Ticker",
                "simple": "Add a new stock to monitor! Just tell me the ticker symbol and set your alert thresholds.",
                "details": "I'll ask for the stock symbol, high price limit, low price limit, and volume spike sensitivity. Then I'll add it to your portfolio."
            },
            "5": {
                "title": "Remove a Ticker",
                "simple": "Stop monitoring a stock. I'll show you your current stocks and you pick which one to remove.",
                "details": "Select from your list of tickers and I'll remove it from your portfolio."
            },
            "6": {
                "title": "Edit My Configuration",
                "simple": "Open your configuration file to make manual changes to your portfolio settings.",
                "details": "Opens config.yaml in your text editor so you can make detailed changes if needed."
            },
            "7": {
                "title": "Start Continuous Monitoring",
                "simple": "Let me monitor your portfolio automatically! I'll check it every N seconds and send alerts when needed.",
                "details": "Set an interval (like 60 seconds) and I'll keep checking your portfolio in the background. Press Ctrl+C to stop."
            },
            "8": {
                "title": "View Recent Alerts",
                "simple": "See the last 20 alerts that have been triggered. Great for reviewing what happened!",
                "details": "Shows your alert history with timestamps so you can see what triggered alerts and when."
            },
            "9": {
                "title": "Run Tests",
                "simple": "Verify that everything is working correctly. I'll run 35 tests to make sure all tools are functioning.",
                "details": "Tests all the monitoring tools, data validation, error handling, and performance. All tests should pass!"
            },
        }
        
        # Explanations for concepts
        self.concept_explanations = {
            "threshold": "A price limit you set. If a stock goes ABOVE the high threshold or BELOW the low threshold, you get an alert!",
            "volume spike": "When a stock has way more trading activity than usual. Like if a stock normally trades 50M shares but today it's 75M - that's a spike!",
            "ticker": "The short code for a stock. Like AAPL for Apple, GOOGL for Google, MSFT for Microsoft.",
            "alert": "A notification sent to you when something important happens - like a price breach or unusual volume.",
            "portfolio": "All the stocks you're monitoring together. Your collection of tickers.",
            "dry-run": "Test mode! Alerts are logged to a file instead of sent to Slack. Great for testing without spamming your team.",
            "slack": "A messaging app. If you connect it, I can send alerts directly to your Slack channel!",
            "continuous monitoring": "Let me keep checking your portfolio automatically instead of you checking manually.",
            "adding a new ticker": "You tell me a stock symbol (like AAPL or GOOGL) and set price limits for it. Then I'll start monitoring that stock and alert you if prices go outside your limits.",
            "add ticker": "You tell me a stock symbol (like AAPL or GOOGL) and set price limits for it. Then I'll start monitoring that stock and alert you if prices go outside your limits.",
            "new ticker": "You tell me a stock symbol (like AAPL or GOOGL) and set price limits for it. Then I'll start monitoring that stock and alert you if prices go outside your limits.",
        }
    
    def print_header(self):
        """Print chatbot header"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'PORTFOLIO WATCHDOG - CONVERSATIONAL ASSISTANT'.center(70)}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}\n")
    
    def print_menu(self):
        """Print menu options"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}What would you like to do?{Colors.ENDC}")
        print("  1️⃣  Check a single ticker")
        print("  2️⃣  Check my full portfolio")
        print("  3️⃣  View my portfolio configuration")
        print("  4️⃣  Add a new ticker")
        print("  5️⃣  Remove a ticker")
        print("  6️⃣  Edit my configuration")
        print("  7️⃣  Start continuous monitoring")
        print("  8️⃣  View recent alerts")
        print("  9️⃣  Run tests")
        print("  0️⃣  Exit")
    
    def company_name_to_ticker(self, company_name: str) -> str:
        """Convert company name to ticker symbol"""
        company_lower = company_name.lower().strip()
        
        # Direct match
        if company_lower in self.company_to_ticker:
            return self.company_to_ticker[company_lower]
        
        # Partial match
        for company, ticker in self.company_to_ticker.items():
            if company in company_lower or company_lower in company:
                return ticker
        
        # If not found, assume it's already a ticker
        return company_name.upper()
    
    def get_greeting(self) -> str:
        """Get random greeting"""
        return random.choice(self.greetings)
    
    def get_suggestion(self) -> str:
        """Get random suggestion"""
        return random.choice(self.suggestions)
        """Handle small talk. Returns True if handled"""
        user_lower = user_input.lower()
        
        for key, responses in self.small_talk.items():
            if key in user_lower:
                response = random.choice(responses)
                print(f"\n{Colors.GREEN}Assistant: {response}{Colors.ENDC}")
                return True
        
        return False
    
    def handle_menu_option(self, option: str) -> bool:
        """Handle menu option. Returns True if should continue"""
        if option == "0":
            print(f"\n{Colors.GREEN}Assistant: Thanks for using Portfolio Watchdog! Happy investing! 📈{Colors.ENDC}\n")
            return False
        
        elif option == "1":
            print(f"\n{Colors.BOLD}Assistant: Great! Let me explain what we're about to do:{Colors.ENDC}")
            print(f"  I'll ask you for a stock ticker (like AAPL or GOOGL)")
            print(f"  Or just the company name (like Apple or Google)!")
            print(f"  Then I'll show you its current price, if it's up or down, and any alerts")
            print(f"  Finally, I'll explain everything in simple terms and answer your questions!\n")
            company_input = input(f"{Colors.BOLD}You - Enter ticker or company name (e.g., AAPL or Apple): {Colors.ENDC}").strip()
            if company_input:
                ticker = self.company_name_to_ticker(company_input)
                self.check_ticker(ticker)
        
        elif option == "2":
            print(f"\n{Colors.BOLD}Assistant: Perfect! Here's what I'm about to do:{Colors.ENDC}")
            print(f"  I'll check ALL your stocks at once")
            print(f"  Show you which ones are healthy (green ✓) and which have alerts (yellow ⚠️)")
            print(f"  Then I'll explain what it all means in simple terms")
            print(f"  And give you my advisor recommendations on whether to hold or sell!\n")
            self.check_full_portfolio()
        
        elif option == "3":
            print(f"\n{Colors.BOLD}Assistant: Here's what you'll see:{Colors.ENDC}")
            print(f"  All the stocks you're currently monitoring")
            print(f"  The price limits (thresholds) you set for each one")
            print(f"  Your volume spike sensitivity settings\n")
            self.view_portfolio_config()
        
        elif option == "4":
            print(f"\n{Colors.BOLD}Assistant: Let's add a new stock! Here's what happens:{Colors.ENDC}")
            print(f"  I'll ask you for a ticker symbol (like AAPL)")
            print(f"  Then you set a HIGH price limit (alert if it goes above this)")
            print(f"  Then a LOW price limit (alert if it goes below this)")
            print(f"  Then volume sensitivity (how much volume change triggers an alert)")
            print(f"  And boom - I'll start monitoring it for you!\n")
            self.add_ticker()
        
        elif option == "5":
            print(f"\n{Colors.BOLD}Assistant: Let's remove a stock! Here's what happens:{Colors.ENDC}")
            print(f"  I'll show you all your current stocks")
            print(f"  You pick which one to remove")
            print(f"  And I'll stop monitoring it\n")
            self.remove_ticker()
        
        elif option == "6":
            print(f"\n{Colors.BOLD}Assistant: We're opening your configuration file:{Colors.ENDC}")
            print(f"  This is where all your settings are stored")
            print(f"  You can make manual changes if you want")
            print(f"  Just save and close when you're done!\n")
            self.edit_config()
        
        elif option == "7":
            print(f"\n{Colors.BOLD}Assistant: Let's set up continuous monitoring! Here's how it works:{Colors.ENDC}")
            print(f"  I'll check your portfolio automatically every N seconds")
            print(f"  You tell me the interval (like 60 seconds)")
            print(f"  I'll keep checking and send alerts if anything changes")
            print(f"  Press Ctrl+C anytime to stop\n")
            self.continuous_monitoring()
        
        elif option == "8":
            print(f"\n{Colors.BOLD}Assistant: Let me show you your recent alerts:{Colors.ENDC}")
            print(f"  These are all the notifications I've sent you")
            print(f"  With timestamps so you know when they happened\n")
            self.view_logs()
        
        elif option == "9":
            print(f"\n{Colors.BOLD}Assistant: Running tests to verify everything works:{Colors.ENDC}")
            print(f"  I'll run 35 comprehensive tests")
            print(f"  Checking all tools, data validation, and error handling")
            print(f"  Everything should pass! ✓\n")
            self.run_tests()
        
        return True
    
    def check_ticker(self, ticker: str) -> bool:
        """Check single ticker"""
        # Don't treat single digits as tickers
        if len(ticker) <= 1 or ticker.isdigit():
            print(f"\n{Colors.YELLOW}Assistant: That doesn't look like a valid ticker symbol. Try something like AAPL, GOOGL, or MSFT!{Colors.ENDC}")
            return True
        
        print(f"\n{Colors.BOLD}Assistant: Let me check {ticker} for you...{Colors.ENDC}")
        
        price_data = get_stock_price(ticker)
        if "error" in price_data:
            print(f"{Colors.RED}Hmm, I couldn't find data for {ticker}. Make sure it's a valid ticker symbol.{Colors.ENDC}")
            return True
        
        current_price = price_data["current_price"]
        percent_change = price_data["percent_change"]
        volume = price_data["volume"]
        
        change_emoji = "📈" if percent_change >= 0 else "📉"
        
        print(f"\n{Colors.CYAN}Here's what I found:{Colors.ENDC}")
        print(f"  {Colors.BOLD}{ticker}{Colors.ENDC}: ${current_price} {change_emoji} ({percent_change:+.2f}%)")
        print(f"  Volume: {volume:,} shares")
        
        threshold_data = check_thresholds(ticker, current_price)
        if threshold_data.get("breached"):
            print(f"  {Colors.YELLOW}⚠️  Alert: {threshold_data['breaches'][0]}{Colors.ENDC}")
        else:
            print(f"  {Colors.GREEN}✓ Price is within thresholds (${threshold_data['thresholds']['low']}-${threshold_data['thresholds']['high']}){Colors.ENDC}")
        
        volume_data = detect_volume_spike(ticker)
        if "error" not in volume_data:
            if volume_data.get("is_spike"):
                print(f"  {Colors.YELLOW}⚠️  Volume spike detected: {volume_data['spike_percent']:.2f}% above average{Colors.ENDC}")
            else:
                print(f"  {Colors.GREEN}✓ Volume is normal{Colors.ENDC}")
        
        # Get news
        news_data = get_news_headlines(ticker)
        if news_data.get("headlines"):
            print(f"\n{Colors.CYAN}Recent news:{Colors.ENDC}")
            for i, headline in enumerate(news_data["headlines"][:2], 1):
                if headline["title"] and headline["title"] != "N/A":
                    print(f"  {i}. {headline['title'][:60]}...")
        
        # Wait for discussion
        self.discuss_ticker(ticker, current_price, percent_change)
        
        return True
    
    def discuss_ticker(self, ticker: str, current_price: float, percent_change: float):
        """Discuss ticker with user - wait for questions"""
        print(f"\n{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}What would you like to know about {ticker}?{Colors.ENDC}")
        print(f"{Colors.YELLOW}(Ask me anything or press Enter to go back){Colors.ENDC}\n")
        
        while True:
            user_q = input(f"{Colors.BOLD}You: {Colors.ENDC}").strip()
            
            if not user_q:
                print(f"\n{Colors.GREEN}Assistant: Got it! Let me know if you need anything else.{Colors.ENDC}")
                break
            
            # Handle common questions
            if any(word in user_q.lower() for word in ["price", "cost", "how much"]):
                print(f"\n{Colors.GREEN}Assistant: {ticker} is currently trading at ${current_price}. That's {percent_change:+.2f}% compared to yesterday.{Colors.ENDC}\n")
            
            elif any(word in user_q.lower() for word in ["up", "down", "change", "percent"]):
                direction = "UP 📈" if percent_change >= 0 else "DOWN 📉"
                print(f"\n{Colors.GREEN}Assistant: {ticker} is {direction} by {abs(percent_change):.2f}% today!{Colors.ENDC}\n")
            
            elif any(word in user_q.lower() for word in ["buy", "sell", "hold", "keep", "remove", "advice"]):
                self.give_ticker_advice(ticker, current_price, percent_change)
                break
            
            elif any(word in user_q.lower() for word in ["threshold", "limit", "alert"]):
                threshold_data = check_thresholds(ticker, current_price)
                print(f"\n{Colors.GREEN}Assistant: Your limits for {ticker} are:")
                print(f"  High: ${threshold_data['thresholds']['high']} (alert if above)")
                print(f"  Low: ${threshold_data['thresholds']['low']} (alert if below)")
                print(f"  Current price: ${current_price}")
                if threshold_data.get("breached"):
                    print(f"  ⚠️  ALERT: Price has breached your limits!{Colors.ENDC}\n")
                else:
                    print(f"  ✓ Price is within your limits{Colors.ENDC}\n")
            
            elif any(word in user_q.lower() for word in ["volume", "trading"]):
                volume_data = detect_volume_spike(ticker)
                if "error" not in volume_data:
                    print(f"\n{Colors.GREEN}Assistant: Volume info for {ticker}:")
                    print(f"  Today's volume: {volume_data['today_volume']:,} shares")
                    print(f"  30-day average: {volume_data['avg_volume_30d']:,} shares")
                    print(f"  Difference: {volume_data['spike_percent']:.2f}%")
                    if volume_data.get("is_spike"):
                        print(f"  🔥 This is a volume spike!{Colors.ENDC}\n")
                    else:
                        print(f"  ✓ Volume is normal{Colors.ENDC}\n")
            
            elif any(word in user_q.lower() for word in ["news", "headline", "what's happening"]):
                news_data = get_news_headlines(ticker)
                if news_data.get("headlines"):
                    print(f"\n{Colors.GREEN}Assistant: Recent news about {ticker}:")
                    for i, headline in enumerate(news_data["headlines"][:3], 1):
                        if headline["title"] and headline["title"] != "N/A":
                            print(f"  {i}. {headline['title']}{Colors.ENDC}\n")
            
            else:
                print(f"\n{Colors.GREEN}Assistant: I can help you with questions about {ticker}'s price, volume, thresholds, news, or whether you should buy/sell. What else would you like to know?{Colors.ENDC}\n")
    
    def give_ticker_advice(self, ticker: str, current_price: float, percent_change: float):
        """Give advice on a specific ticker"""
        print(f"\n{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}💡 My advice for {ticker}:{Colors.ENDC}\n")
        
        if percent_change > 5:
            print(f"{Colors.GREEN}📈 Stock is UP {percent_change:.2f}%")
            print(f"This is good! Consider HOLDING if you believe in the company.{Colors.ENDC}")
        elif percent_change < -5:
            print(f"{Colors.YELLOW}📉 Stock is DOWN {percent_change:.2f}%")
            print(f"This might be a buying opportunity if you like the company!{Colors.ENDC}")
        else:
            print(f"{Colors.BLUE}➡️  Stock is stable ({percent_change:+.2f}%)")
            print(f"Good time to hold and monitor.{Colors.ENDC}")
        
        threshold_data = check_thresholds(ticker, current_price)
        if threshold_data.get("breached"):
            print(f"\n{Colors.YELLOW}⚠️  Price hit your limit!")
            print(f"Consider reviewing if you want to SELL or adjust your limits.{Colors.ENDC}")
        
        volume_data = detect_volume_spike(ticker)
        if "error" not in volume_data and volume_data.get("is_spike"):
            print(f"\n{Colors.RED}🔥 High volume detected - Something big is happening!")
            print(f"Stay alert!{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Remember:{Colors.ENDC}")
        print(f"  • This is data-based advice, not financial advice")
        print(f"  • Always do your own research")
        print(f"  • Don't panic - think long term!")
        print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
    
    def discuss_portfolio(self):
        """Discuss portfolio with user - wait for questions"""
        print(f"\n{Colors.BOLD}Do you have any questions about your portfolio?{Colors.ENDC}")
        print(f"{Colors.YELLOW}(Ask me anything, type 'back' or 'menu' to return, or press Enter to continue){Colors.ENDC}\n")
        
        while True:
            user_q = input(f"{Colors.BOLD}You: {Colors.ENDC}").strip().lower()
            
            if not user_q or user_q in ["back", "menu", "no", "nope", "done", "ok", "thanks"]:
                print(f"\n{Colors.GREEN}Assistant: Got it! Let me know if you need anything else.{Colors.ENDC}")
                break
            
            # Handle common questions
            if any(word in user_q for word in ["advice", "should", "buy", "sell", "hold"]):
                self.give_portfolio_advice()
                break
            
            elif any(word in user_q for word in ["healthy", "good", "bad", "status"]):
                print(f"\n{Colors.GREEN}Assistant: Your portfolio status looks good! All stocks are being monitored with your custom alerts.{Colors.ENDC}\n")
            
            elif any(word in user_q for word in ["alert", "warning", "notification"]):
                print(f"\n{Colors.GREEN}Assistant: Alerts are sent when a stock price hits your limits or volume spikes. Check option 8 to see recent alerts!{Colors.ENDC}\n")
            
            elif any(word in user_q for word in ["add", "remove", "change", "modify"]):
                print(f"\n{Colors.GREEN}Assistant: You can add tickers with option 4, remove with option 5, or edit settings with option 6.{Colors.ENDC}\n")
            
            else:
                print(f"\n{Colors.GREEN}Assistant: I can help with advice, alerts, adding/removing stocks, or anything else about your portfolio. What else?{Colors.ENDC}\n")
    
    def check_full_portfolio(self) -> bool:
        """Check full portfolio"""
        print(f"\n{Colors.BOLD}Assistant: Let me check your entire portfolio...{Colors.ENDC}\n")
        
        tickers = self.portfolio.get("tickers", [])
        alerts = []
        healthy = 0
        
        for ticker in tickers:
            price_data = get_stock_price(ticker)
            if "error" in price_data:
                print(f"{Colors.RED}✗ {ticker}: Couldn't fetch data{Colors.ENDC}")
                continue
            
            current_price = price_data["current_price"]
            percent_change = price_data["percent_change"]
            threshold_data = check_thresholds(ticker, current_price)
            
            change_emoji = "📈" if percent_change >= 0 else "📉"
            
            if threshold_data.get("breached"):
                print(f"{Colors.YELLOW}⚠️  {ticker}: ${current_price} {change_emoji} ({percent_change:+.2f}%) - {threshold_data['breaches'][0]}{Colors.ENDC}")
                alerts.append(f"[{ticker}] {threshold_data['breaches'][0]}")
            else:
                print(f"{Colors.GREEN}✓ {ticker}: ${current_price} {change_emoji} ({percent_change:+.2f}%){Colors.ENDC}")
                healthy += 1
        
        # Summary
        print(f"\n{Colors.CYAN}Portfolio Summary:{Colors.ENDC}")
        print(f"  Total tickers: {len(tickers)}")
        print(f"  Healthy: {healthy}")
        print(f"  Alerts: {len(alerts)}")
        
        if alerts:
            print(f"\n{Colors.BOLD}Assistant: I found {len(alerts)} alert(s). Sending them now...{Colors.ENDC}")
            for alert in alerts:
                send_alert(alert)
            print(f"{Colors.GREEN}✓ Alerts sent!{Colors.ENDC}")
        else:
            print(f"\n{Colors.GREEN}Assistant: Great news! Your portfolio looks healthy! 🎉{Colors.ENDC}")
        
        # Explain in simple terms
        self.explain_portfolio_check()
        
        # Wait for discussion
        self.discuss_portfolio()
        
        return True
    
    def explain_portfolio_check(self):
        """Explain portfolio check in simple terms"""
        print(f"\n{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}Let me explain what you just saw:{Colors.ENDC}\n")
        
        print(f"{Colors.GREEN}✓ Green checkmarks{Colors.ENDC} = Your stocks are doing fine, prices are where you want them")
        print(f"{Colors.YELLOW}⚠️  Yellow warnings{Colors.ENDC} = A stock price went outside your limits - that's why you got an alert!")
        print(f"{Colors.CYAN}📈 Up arrow{Colors.ENDC} = Stock price went UP (good news!)")
        print(f"{Colors.CYAN}📉 Down arrow{Colors.ENDC} = Stock price went DOWN (might be a buying opportunity!)")
        print(f"\n{Colors.BOLD}Think of it like this:{Colors.ENDC}")
        print(f"  You set price limits for each stock (like 'alert me if AAPL goes above $250')")
        print(f"  I check all your stocks and tell you which ones hit those limits")
        print(f"  If any did, I send you an alert so you know right away!")
        
        print(f"\n{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"\n{Colors.BOLD}Do you have any questions about what you just saw?{Colors.ENDC}")
        print(f"{Colors.YELLOW}(Type your question or press Enter to continue){Colors.ENDC}\n")
        
        # Wait for questions
        while True:
            user_q = input(f"{Colors.BOLD}You: {Colors.ENDC}").strip()
            
            if not user_q:
                print(f"\n{Colors.GREEN}Assistant: Great! Let me know if you need anything else.{Colors.ENDC}")
                break
            
            # Handle common questions
            if any(word in user_q.lower() for word in ["green", "checkmark", "✓"]):
                print(f"\n{Colors.GREEN}Assistant: Green checkmarks mean that stock is doing good! The price is within the limits you set, so no alerts needed.{Colors.ENDC}\n")
            
            elif any(word in user_q.lower() for word in ["yellow", "warning", "⚠️"]):
                print(f"\n{Colors.GREEN}Assistant: Yellow warnings mean ATTENTION! That stock's price went outside your limits. That's why I sent you an alert!{Colors.ENDC}\n")
            
            elif any(word in user_q.lower() for word in ["arrow", "up", "down", "📈", "📉"]):
                print(f"\n{Colors.GREEN}Assistant: The arrows show if the price went UP (📈) or DOWN (📉) compared to yesterday. It helps you see the trend!{Colors.ENDC}\n")
            
            elif any(word in user_q.lower() for word in ["alert", "warning"]):
                print(f"\n{Colors.GREEN}Assistant: Alerts are notifications I send you when something important happens - like a stock price hitting your limits!{Colors.ENDC}\n")
            
            elif any(word in user_q.lower() for word in ["limit", "threshold"]):
                print(f"\n{Colors.GREEN}Assistant: Limits are the price boundaries you set. Like 'tell me if AAPL goes above $250 or below $150'. I watch for those!{Colors.ENDC}\n")
            
            elif any(word in user_q.lower() for word in ["healthy", "good"]):
                print(f"\n{Colors.GREEN}Assistant: Healthy means all your stocks are within the price limits you set. No alerts needed - everything is good!{Colors.ENDC}\n")
            
            elif any(word in user_q.lower() for word in ["advice", "should", "keep", "sell", "hold", "remove"]):
                self.give_portfolio_advice()
                break
            
            else:
                print(f"\n{Colors.GREEN}Assistant: Good question! I can explain more about the data, alerts, limits, or anything else you saw. What would you like to know?{Colors.ENDC}\n")
    
    def give_portfolio_advice(self):
        """Give investment advice on portfolio"""
        print(f"\n{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}💡 My Investment Advisor Recommendations:{Colors.ENDC}\n")
        
        tickers = self.portfolio.get("tickers", [])
        
        for ticker in tickers:
            price_data = get_stock_price(ticker)
            if "error" in price_data:
                continue
            
            current_price = price_data["current_price"]
            percent_change = price_data["percent_change"]
            threshold_data = check_thresholds(ticker, current_price)
            volume_data = detect_volume_spike(ticker)
            
            print(f"{Colors.BOLD}{ticker}:{Colors.ENDC}")
            
            # Advice based on price change
            if percent_change > 5:
                print(f"  📈 Stock is UP {percent_change:.2f}% - This is good! Consider HOLDING if you believe in the company.")
            elif percent_change < -5:
                print(f"  📉 Stock is DOWN {percent_change:.2f}% - This might be a buying opportunity if you like the company!")
            else:
                print(f"  ➡️  Stock is stable ({percent_change:+.2f}%) - Good time to hold and monitor.")
            
            # Advice based on thresholds
            if threshold_data.get("breached"):
                print(f"  ⚠️  ALERT: Price hit your limit! Consider reviewing if you want to SELL or adjust your limits.")
            else:
                print(f"  ✓ Price is healthy - Keep monitoring!")
            
            # Advice based on volume
            if "error" not in volume_data and volume_data.get("is_spike"):
                print(f"  🔥 High volume detected - Something big is happening! Stay alert!")
            
            print()
        
        print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"\n{Colors.BOLD}Remember:{Colors.ENDC}")
        print(f"  • This is just data-based advice, not financial advice")
        print(f"  • Always do your own research before making decisions")
        print(f"  • Diversify your portfolio to reduce risk")
        print(f"  • Don't panic sell - think long term!")
        print(f"\n{Colors.YELLOW}Want to remove any stocks or adjust limits? Just let me know!{Colors.ENDC}\n")
    
    def view_portfolio_config(self) -> bool:
        """View portfolio configuration"""
        print(f"\n{Colors.BOLD}Assistant: Here's your portfolio setup:{Colors.ENDC}")
        
        print(f"\n{Colors.CYAN}📊 Tickers ({self.portfolio['total_tickers']}):${Colors.ENDC}")
        for ticker in self.portfolio.get("tickers", []):
            print(f"  • {ticker}")
        
        print(f"\n{Colors.CYAN}⚙️  Alert Rules:${Colors.ENDC}")
        for ticker, rules in self.portfolio.get("alert_rules", {}).items():
            print(f"\n  {Colors.BOLD}{ticker}:{Colors.ENDC}")
            print(f"    High threshold: ${rules.get('price_threshold_high', 'N/A')}")
            print(f"    Low threshold: ${rules.get('price_threshold_low', 'N/A')}")
            print(f"    Volume spike: {rules.get('volume_spike_percent', 'N/A')}%")
        
        return True
    
    def add_ticker(self) -> bool:
        """Add ticker"""
        print(f"\n{Colors.BOLD}Assistant: Great! Let's add a new ticker to your portfolio.{Colors.ENDC}")
        
        ticker = input(f"{Colors.BOLD}You - Ticker symbol: {Colors.ENDC}").upper()
        high = input(f"{Colors.BOLD}You - High price threshold: ${Colors.ENDC}")
        low = input(f"{Colors.BOLD}You - Low price threshold: ${Colors.ENDC}")
        volume = input(f"{Colors.BOLD}You - Volume spike % (e.g., 50): {Colors.ENDC}")
        
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
            print(f"\n{Colors.GREEN}Assistant: Perfect! I've added {ticker} to your portfolio. You're all set! ✓{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}Assistant: Oops, something went wrong: {e}{Colors.ENDC}")
        
        return True
    
    def remove_ticker(self) -> bool:
        """Remove ticker"""
        tickers = self.portfolio.get("tickers", [])
        print(f"\n{Colors.BOLD}Assistant: Which ticker would you like to remove?{Colors.ENDC}")
        for i, ticker in enumerate(tickers, 1):
            print(f"  {i}) {ticker}")
        
        choice = input(f"\n{Colors.BOLD}You: {Colors.ENDC}")
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
                print(f"\n{Colors.GREEN}Assistant: Done! I've removed {ticker} from your portfolio.{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}Assistant: Hmm, something went wrong: {e}{Colors.ENDC}")
        
        return True
    
    def edit_config(self) -> bool:
        """Edit configuration"""
        import os
        print(f"\n{Colors.BOLD}Assistant: Opening your configuration file...{Colors.ENDC}")
        editor = os.environ.get('EDITOR', 'nano')
        os.system(f"{editor} config.yaml")
        load_config()
        self.portfolio = load_portfolio()
        print(f"\n{Colors.GREEN}Assistant: Configuration updated! ✓{Colors.ENDC}")
        return True
    
    def continuous_monitoring(self) -> bool:
        """Continuous monitoring"""
        import time
        print(f"\n{Colors.BOLD}Assistant: Let's set up continuous monitoring!{Colors.ENDC}")
        interval = input(f"{Colors.BOLD}You - Check interval in seconds (default 300): {Colors.ENDC}")
        try:
            interval = int(interval) if interval else 300
        except:
            interval = 300
        
        print(f"\n{Colors.GREEN}Assistant: Starting continuous monitoring every {interval} seconds...{Colors.ENDC}")
        print(f"{Colors.YELLOW}Press Ctrl+C to stop{Colors.ENDC}\n")
        
        try:
            cycle = 0
            while True:
                cycle += 1
                print(f"{Colors.BOLD}Cycle {cycle} - {datetime.now().strftime('%H:%M:%S')}{Colors.ENDC}")
                self.check_full_portfolio()
                print(f"{Colors.YELLOW}Next check in {interval}s...{Colors.ENDC}\n")
                time.sleep(interval)
        except KeyboardInterrupt:
            print(f"\n{Colors.GREEN}Assistant: Monitoring stopped. See you next time! 👋{Colors.ENDC}")
        
        return True
    
    def view_logs(self) -> bool:
        """View logs"""
        import os
        if not os.path.exists('portfolio_alerts.log'):
            print(f"\n{Colors.YELLOW}Assistant: No alerts yet! Your portfolio is quiet. 😊{Colors.ENDC}")
            return True
        
        with open('portfolio_alerts.log', 'r') as f:
            lines = f.readlines()
        
        recent = lines[-20:] if len(lines) > 20 else lines
        
        print(f"\n{Colors.BOLD}Assistant: Here are your recent alerts:{Colors.ENDC}\n")
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
        print(f"\n{Colors.BOLD}Assistant: Running tests to verify everything is working...{Colors.ENDC}\n")
        os.system("python agents/test_portfolio_comprehensive.py 2>&1 | tail -30")
        return True
    
    def explain_option(self, option: str) -> bool:
        """Explain what an option does"""
        if option in self.option_explanations:
            exp = self.option_explanations[option]
            print(f"\n{Colors.CYAN}{exp['title']}:{Colors.ENDC}")
            print(f"\n{Colors.GREEN}Simple explanation:{Colors.ENDC}")
            print(f"  {exp['simple']}")
            print(f"\n{Colors.GREEN}More details:{Colors.ENDC}")
            print(f"  {exp['details']}")
            return True
        return False
    
    def explain_concept(self, concept: str) -> bool:
        """Explain a concept"""
        concept_lower = concept.lower()
        
        for key, explanation in self.concept_explanations.items():
            if key in concept_lower:
                print(f"\n{Colors.CYAN}{key.upper()}:{Colors.ENDC}")
                print(f"  {explanation}")
                return True
        
        return False
    
    def find_explanation(self, user_input: str) -> bool:
        """Find and explain what user is asking about"""
        user_lower = user_input.lower()
        
        # Check for option numbers
        for i in range(10):
            if f"option {i}" in user_lower or f"choice {i}" in user_lower or f"#{i}" in user_lower:
                return self.explain_option(str(i))
        
        # Check for specific phrases
        if "add" in user_lower and "ticker" in user_lower:
            return self.explain_option("4")
        
        if "remove" in user_lower and "ticker" in user_lower:
            return self.explain_option("5")
        
        if "check" in user_lower and "portfolio" in user_lower:
            return self.explain_option("2")
        
        if "check" in user_lower and "single" in user_lower:
            return self.explain_option("1")
        
        if "continuous" in user_lower and "monitor" in user_lower:
            return self.explain_option("7")
        
        if "alert" in user_lower and "view" in user_lower:
            return self.explain_option("8")
        
        if "test" in user_lower:
            return self.explain_option("9")
        
        if "config" in user_lower or "edit" in user_lower:
            return self.explain_option("6")
        
        if "view" in user_lower and "config" in user_lower:
            return self.explain_option("3")
        
        # Check for concepts
        for concept in self.concept_explanations.keys():
            if concept in user_lower:
                explanation = self.concept_explanations[concept]
                print(f"\n{Colors.GREEN}Assistant: {explanation}{Colors.ENDC}")
                return True
        
        return False
    
    def run(self):
        """Run chatbot"""
        self.print_header()
        
        # Initial greeting
        greeting = self.get_greeting()
        print(f"{Colors.GREEN}Assistant: {greeting}{Colors.ENDC}")
        
        # Ask for name
        name = input(f"\n{Colors.BOLD}You: {Colors.ENDC}").strip()
        if name:
            self.user_name = name
            print(f"\n{Colors.GREEN}Assistant: Nice to meet you, {name}! 😊 I'm here to help you manage your portfolio.{Colors.ENDC}")
        
        # Main loop
        while True:
            self.print_menu()
            
            # Random suggestion
            if random.random() < 0.3:  # 30% chance
                print(f"\n{Colors.CYAN}💡 {self.get_suggestion()}{Colors.ENDC}")
            
            user_input = input(f"\n{Colors.BOLD}You: {Colors.ENDC}").strip()
            
            if not user_input:
                continue
            
            # Check if it's a menu option (only if it's just a number, not part of a question)
            if user_input in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                if not self.handle_menu_option(user_input):
                    break
            
            # Check for small talk
            elif self.handle_small_talk(user_input):
                pass
            
            # Check for help
            elif "help" in user_input.lower() or "?" in user_input:
                print(f"\n{Colors.GREEN}Assistant: I can help you with:")
                print("  • Checking your portfolio")
                print("  • Adding or removing tickers")
                print("  • Viewing alerts")
                print("  • Continuous monitoring")
                print("  • And much more!")
                print(f"Just pick an option from the menu above! 😊{Colors.ENDC}")
            
            # Check for "what does" or "explain" questions
            elif any(phrase in user_input.lower() for phrase in ["what does", "what is", "explain", "what's", "meaning of", "can you explain", "tell me about"]):
                if not self.find_explanation(user_input):
                    print(f"\n{Colors.GREEN}Assistant: I can explain:")
                    print("  • Any option (1-9) - just ask 'what does option 4 do?'")
                    print("  • Concepts like: threshold, volume spike, ticker, alert, portfolio, slack, adding a new ticker, etc.")
                    print(f"What would you like to know more about?{Colors.ENDC}")
            
            # Default response
            else:
                responses = [
                    f"I'm not sure what you mean, {self.user_name or 'friend'}. Pick an option from the menu!",
                    "Hmm, I didn't catch that. Try picking a number from the menu above.",
                    "Let me help you with one of the options above!",
                ]
                print(f"\n{Colors.YELLOW}Assistant: {random.choice(responses)}{Colors.ENDC}")

if __name__ == "__main__":
    try:
        chatbot = ConversationalChatbot()
        chatbot.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}Assistant: Thanks for chatting! Goodbye! 👋{Colors.ENDC}\n")
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.ENDC}")
        sys.exit(1)
