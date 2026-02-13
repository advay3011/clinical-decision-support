import time
import yaml
import json
import logging
from datetime import datetime
from typing import Optional
import yfinance as yf
import requests
from strands import Agent, tool

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('portfolio_alerts.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global config
CONFIG = None
VOLUME_HISTORY = {}

def load_config():
    """Load configuration from config.yaml"""
    global CONFIG
    try:
        with open('config.yaml', 'r') as f:
            CONFIG = yaml.safe_load(f)
        logger.info("Configuration loaded successfully")
        return CONFIG
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return None

@tool
def load_portfolio() -> dict:
    """Load portfolio tickers and alert rules from config.yaml"""
    if CONFIG is None:
        load_config()
    
    if CONFIG is None:
        return {"error": "Failed to load configuration"}
    
    portfolio = {
        "tickers": CONFIG.get("portfolio", {}).get("tickers", []),
        "alert_rules": CONFIG.get("alert_rules", {}),
        "total_tickers": len(CONFIG.get("portfolio", {}).get("tickers", []))
    }
    logger.info(f"Portfolio loaded: {portfolio['total_tickers']} tickers")
    return portfolio

@tool
def get_stock_price(ticker: str) -> dict:
    """Fetch live stock price, volume, and % change via yfinance"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2d")
        
        if len(hist) < 1:
            return {"error": f"No data found for {ticker}"}
        
        current = hist.iloc[-1]
        previous = hist.iloc[-2] if len(hist) > 1 else current
        
        current_price = float(current['Close'])
        previous_price = float(previous['Close'])
        percent_change = ((current_price - previous_price) / previous_price * 100) if previous_price != 0 else 0
        volume = int(current['Volume'])
        
        result = {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "previous_price": round(previous_price, 2),
            "percent_change": round(percent_change, 2),
            "volume": volume,
            "timestamp": datetime.now().isoformat()
        }
        logger.info(f"Price fetched for {ticker}: ${current_price:.2f} ({percent_change:+.2f}%)")
        return result
    except Exception as e:
        logger.error(f"Error fetching price for {ticker}: {e}")
        return {"error": str(e), "ticker": ticker}

@tool
def get_news_headlines(ticker: str) -> dict:
    """Fetch recent news headlines for a ticker"""
    try:
        stock = yf.Ticker(ticker)
        
        # Try to get news from yfinance
        headlines = []
        try:
            news_list = stock.news
            if news_list:
                for item in news_list[:5]:
                    if isinstance(item, dict):
                        headlines.append({
                            "title": item.get("title", "N/A"),
                            "link": item.get("link", ""),
                            "source": item.get("source", "N/A")
                        })
        except:
            pass
        
        # If no headlines found, provide a placeholder
        if not headlines:
            headlines = [{
                "title": f"No recent news available for {ticker}",
                "link": "",
                "source": "N/A"
            }]
        
        result = {
            "ticker": ticker,
            "headlines": headlines,
            "count": len(headlines)
        }
        logger.info(f"News fetched for {ticker}: {len(headlines)} headlines")
        return result
    except Exception as e:
        logger.error(f"Error fetching news for {ticker}: {e}")
        return {"error": str(e), "ticker": ticker, "headlines": []}

@tool
def check_thresholds(ticker: str, current_price: float) -> dict:
    """Check if price breaches alert rules from config.yaml"""
    if CONFIG is None:
        load_config()
    
    rules = CONFIG.get("alert_rules", {}).get(ticker, {})
    
    if not rules:
        return {"ticker": ticker, "breached": False, "message": "No rules configured"}
    
    breaches = []
    high_threshold = rules.get("price_threshold_high")
    low_threshold = rules.get("price_threshold_low")
    
    if high_threshold and current_price > high_threshold:
        breaches.append(f"Price ${current_price:.2f} exceeds high threshold ${high_threshold}")
    
    if low_threshold and current_price < low_threshold:
        breaches.append(f"Price ${current_price:.2f} below low threshold ${low_threshold}")
    
    result = {
        "ticker": ticker,
        "current_price": float(current_price),
        "breached": len(breaches) > 0,
        "breaches": breaches,
        "thresholds": {
            "high": high_threshold,
            "low": low_threshold
        }
    }
    
    if breaches:
        logger.warning(f"Threshold breach for {ticker}: {breaches}")
    
    return result

@tool
def detect_volume_spike(ticker: str) -> dict:
    """Compare today's volume vs 30 day average"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="30d")
        
        if len(hist) < 2:
            return {"error": f"Insufficient data for {ticker}"}
        
        today_volume = int(hist.iloc[-1]['Volume'])
        avg_volume = int(hist['Volume'].mean())
        spike_percent = ((today_volume - avg_volume) / avg_volume * 100) if avg_volume > 0 else 0
        
        rules = CONFIG.get("alert_rules", {}).get(ticker, {}) if CONFIG else {}
        spike_threshold = rules.get("volume_spike_percent", 50)
        
        is_spike = spike_percent > spike_threshold
        
        result = {
            "ticker": ticker,
            "today_volume": today_volume,
            "avg_volume_30d": avg_volume,
            "spike_percent": round(float(spike_percent), 2),
            "threshold": spike_threshold,
            "is_spike": bool(is_spike)
        }
        
        if is_spike:
            logger.warning(f"Volume spike detected for {ticker}: {spike_percent:.2f}%")
        
        return result
    except Exception as e:
        logger.error(f"Error detecting volume spike for {ticker}: {e}")
        return {"error": str(e), "ticker": ticker}

@tool
def send_alert(message: str) -> dict:
    """Send alert via Slack webhook or log to file in dry run mode"""
    if CONFIG is None:
        load_config()
    
    slack_config = CONFIG.get("slack", {})
    webhook_url = slack_config.get("webhook_url", "")
    dry_run = slack_config.get("dry_run", True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    
    if dry_run or not webhook_url:
        logger.info(f"[DRY RUN] Alert: {full_message}")
        return {
            "status": "logged",
            "mode": "dry_run",
            "message": full_message
        }
    
    try:
        payload = {
            "text": full_message,
            "timestamp": timestamp
        }
        response = requests.post(webhook_url, json=payload, timeout=5)
        
        if response.status_code == 200:
            logger.info(f"Alert sent to Slack: {full_message}")
            return {
                "status": "sent",
                "mode": "slack",
                "message": full_message
            }
        else:
            logger.error(f"Failed to send Slack alert: {response.status_code}")
            return {
                "status": "failed",
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        logger.error(f"Error sending alert: {e}")
        return {
            "status": "failed",
            "error": str(e)
        }

def main():
    """Main function to run the Portfolio Watchdog agent"""
    load_config()
    
    # Initialize agent with tools
    agent = Agent(
        tools=[
            load_portfolio,
            get_stock_price,
            get_news_headlines,
            check_thresholds,
            detect_volume_spike,
            send_alert
        ],
        system_prompt="""You are a portfolio monitoring agent. Your job is to:
1. Load the portfolio and check each ticker
2. Fetch current prices and detect any threshold breaches
3. Detect volume spikes that might indicate unusual activity
4. Fetch relevant news headlines for context
5. Send alerts when something needs attention

Be thorough but concise. Focus on actionable alerts."""
    )
    
    logger.info("Portfolio Watchdog Agent started")
    
    try:
        while True:
            logger.info("=" * 60)
            logger.info("Running portfolio check cycle")
            
            # Run the agent
            agent("Check my portfolio and alert me if anything needs attention.")
            
            logger.info("Portfolio check cycle completed. Sleeping for 5 minutes...")
            time.sleep(300)  # Check every 5 minutes
    except KeyboardInterrupt:
        logger.info("Portfolio Watchdog Agent stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error in agent loop: {e}")

if __name__ == "__main__":
    main()
