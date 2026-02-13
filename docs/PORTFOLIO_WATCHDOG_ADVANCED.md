# Portfolio Watchdog - Advanced Usage

## Custom Tool Integration

### Extending with Email Alerts

```python
import smtplib
from email.mime.text import MIMEText
from strands import tool

@tool
def send_email_alert(recipient: str, subject: str, message: str) -> dict:
    """Send alert via email"""
    try:
        sender = "your-email@gmail.com"
        password = "your-app-password"
        
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        
        return {"status": "sent", "recipient": recipient}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
```

### Extending with SMS Alerts

```python
from twilio.rest import Client
from strands import tool

@tool
def send_sms_alert(phone: str, message: str) -> dict:
    """Send alert via SMS"""
    try:
        account_sid = "your-account-sid"
        auth_token = "your-auth-token"
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=message,
            from_="+1234567890",
            to=phone
        )
        
        return {"status": "sent", "sid": message.sid}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
```

## Advanced Monitoring Strategies

### Strategy 1: Momentum Trading Alerts

Monitor price momentum with moving averages:

```python
@tool
def detect_momentum(ticker: str) -> dict:
    """Detect price momentum using moving averages"""
    stock = yf.Ticker(ticker)
    hist = stock.history(period="60d")
    
    # Calculate moving averages
    ma_20 = hist['Close'].rolling(window=20).mean()
    ma_50 = hist['Close'].rolling(window=50).mean()
    
    current_price = hist['Close'].iloc[-1]
    momentum = "bullish" if ma_20.iloc[-1] > ma_50.iloc[-1] else "bearish"
    
    return {
        "ticker": ticker,
        "current_price": current_price,
        "ma_20": ma_20.iloc[-1],
        "ma_50": ma_50.iloc[-1],
        "momentum": momentum
    }
```

### Strategy 2: Relative Strength Index (RSI)

Detect overbought/oversold conditions:

```python
@tool
def calculate_rsi(ticker: str, period: int = 14) -> dict:
    """Calculate RSI for overbought/oversold detection"""
    stock = yf.Ticker(ticker)
    hist = stock.history(period="60d")
    
    delta = hist['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    current_rsi = rsi.iloc[-1]
    condition = "overbought" if current_rsi > 70 else "oversold" if current_rsi < 30 else "neutral"
    
    return {
        "ticker": ticker,
        "rsi": round(current_rsi, 2),
        "condition": condition
    }
```

### Strategy 3: Bollinger Bands

Detect volatility extremes:

```python
@tool
def detect_bollinger_bands(ticker: str, period: int = 20) -> dict:
    """Detect price extremes using Bollinger Bands"""
    stock = yf.Ticker(ticker)
    hist = stock.history(period="60d")
    
    sma = hist['Close'].rolling(window=period).mean()
    std = hist['Close'].rolling(window=period).std()
    
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2)
    
    current_price = hist['Close'].iloc[-1]
    
    if current_price > upper_band.iloc[-1]:
        signal = "above_upper_band"
    elif current_price < lower_band.iloc[-1]:
        signal = "below_lower_band"
    else:
        signal = "within_bands"
    
    return {
        "ticker": ticker,
        "current_price": current_price,
        "upper_band": upper_band.iloc[-1],
        "lower_band": lower_band.iloc[-1],
        "signal": signal
    }
```

## Performance Optimization

### Batch Processing

```python
from concurrent.futures import ThreadPoolExecutor

def check_portfolio_parallel(tickers: list) -> list:
    """Check multiple tickers in parallel"""
    results = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(get_stock_price, ticker) for ticker in tickers]
        results = [f.result() for f in futures]
    
    return results
```

### Caching

```python
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def get_cached_price(ticker: str, timestamp: int) -> dict:
    """Cache prices for 60 seconds"""
    return get_stock_price(ticker)

# Use with timestamp bucketing
current_minute = int(time.time() / 60)
price = get_cached_price("AAPL", current_minute)
```

## Database Integration

### Store Alerts in SQLite

```python
import sqlite3
from datetime import datetime

def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect('portfolio_alerts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            ticker TEXT,
            alert_type TEXT,
            message TEXT,
            price REAL
        )
    ''')
    
    conn.commit()
    conn.close()

def log_alert_to_db(ticker: str, alert_type: str, message: str, price: float):
    """Log alert to database"""
    conn = sqlite3.connect('portfolio_alerts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO alerts (timestamp, ticker, alert_type, message, price)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), ticker, alert_type, message, price))
    
    conn.commit()
    conn.close()
```

## Monitoring Dashboard

### Simple Web Dashboard

```python
from flask import Flask, jsonify
import threading

app = Flask(__name__)

portfolio_state = {}

@app.route('/api/portfolio')
def get_portfolio():
    """Get current portfolio state"""
    return jsonify(portfolio_state)

@app.route('/api/alerts')
def get_alerts():
    """Get recent alerts"""
    conn = sqlite3.connect('portfolio_alerts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 50')
    alerts = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'timestamp': a[1],
        'ticker': a[2],
        'type': a[3],
        'message': a[4],
        'price': a[5]
    } for a in alerts])

def run_dashboard():
    """Run dashboard in background"""
    app.run(host='0.0.0.0', port=5000, debug=False)

# Start dashboard in separate thread
dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
dashboard_thread.start()
```

## Alert Routing

### Intelligent Alert Routing

```python
@tool
def route_alert(ticker: str, alert_type: str, severity: str, message: str) -> dict:
    """Route alert based on severity and type"""
    
    routing_rules = {
        "critical": ["slack", "email", "sms"],
        "warning": ["slack", "email"],
        "info": ["slack"]
    }
    
    channels = routing_rules.get(severity, ["slack"])
    results = {}
    
    for channel in channels:
        if channel == "slack":
            results["slack"] = send_alert(message)
        elif channel == "email":
            results["email"] = send_email_alert("user@example.com", f"{ticker} Alert", message)
        elif channel == "sms":
            results["sms"] = send_sms_alert("+1234567890", message)
    
    return results
```

## Custom Conditions

### Correlation-Based Alerts

```python
@tool
def detect_correlation_break(ticker1: str, ticker2: str, threshold: float = 0.8) -> dict:
    """Alert when correlated stocks diverge"""
    stock1 = yf.Ticker(ticker1)
    stock2 = yf.Ticker(ticker2)
    
    hist1 = stock1.history(period="30d")['Close']
    hist2 = stock2.history(period="30d")['Close']
    
    correlation = hist1.corr(hist2)
    
    return {
        "ticker1": ticker1,
        "ticker2": ticker2,
        "correlation": round(correlation, 2),
        "alert": correlation < threshold
    }
```

### Sector Rotation Alerts

```python
@tool
def detect_sector_rotation(sector_tickers: dict) -> dict:
    """Detect sector rotation patterns"""
    sector_performance = {}
    
    for sector, tickers in sector_tickers.items():
        prices = []
        for ticker in tickers:
            price_data = get_stock_price(ticker)
            if "error" not in price_data:
                prices.append(price_data["percent_change"])
        
        avg_change = sum(prices) / len(prices) if prices else 0
        sector_performance[sector] = round(avg_change, 2)
    
    return sector_performance
```

## Testing & Validation

### Unit Tests

```python
import unittest

class TestPortfolioWatchdog(unittest.TestCase):
    
    def test_load_portfolio(self):
        portfolio = load_portfolio()
        self.assertIn("tickers", portfolio)
        self.assertGreater(len(portfolio["tickers"]), 0)
    
    def test_get_stock_price(self):
        price_data = get_stock_price("AAPL")
        self.assertIn("current_price", price_data)
        self.assertGreater(price_data["current_price"], 0)
    
    def test_check_thresholds(self):
        threshold_data = check_thresholds("AAPL", 250)
        self.assertIn("breached", threshold_data)
        self.assertIsInstance(threshold_data["breached"], bool)

if __name__ == '__main__':
    unittest.main()
```

## Production Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "agents/portfolio_watchdog_agent.py"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: portfolio-watchdog
spec:
  replicas: 1
  selector:
    matchLabels:
      app: portfolio-watchdog
  template:
    metadata:
      labels:
        app: portfolio-watchdog
    spec:
      containers:
      - name: watchdog
        image: portfolio-watchdog:latest
        env:
        - name: CONFIG_FILE
          value: /etc/config/config.yaml
        volumeMounts:
        - name: config
          mountPath: /etc/config
      volumes:
      - name: config
        configMap:
          name: portfolio-config
```

## Monitoring the Monitor

### Health Checks

```python
@tool
def health_check() -> dict:
    """Check agent health"""
    try:
        # Test API connectivity
        test_price = get_stock_price("AAPL")
        
        if "error" in test_price:
            return {"status": "unhealthy", "reason": "API error"}
        
        return {
            "status": "healthy",
            "last_check": datetime.now().isoformat(),
            "test_price": test_price["current_price"]
        }
    except Exception as e:
        return {"status": "unhealthy", "reason": str(e)}
```

## Performance Metrics

```python
import time
from collections import defaultdict

metrics = defaultdict(list)

def track_performance(func):
    """Decorator to track function performance"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        metrics[func.__name__].append(duration)
        return result
    return wrapper

@track_performance
def get_stock_price(ticker: str):
    # ... implementation
    pass

def print_metrics():
    """Print performance metrics"""
    for func_name, durations in metrics.items():
        avg_duration = sum(durations) / len(durations)
        print(f"{func_name}: {avg_duration:.2f}s avg")
```
