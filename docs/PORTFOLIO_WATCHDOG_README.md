# Portfolio Watchdog Agent

A production-ready portfolio monitoring agent built with the Strands Agents SDK. Automatically monitors stock prices, detects threshold breaches, identifies volume spikes, and sends alerts.

## Features

- **Real-time Price Monitoring**: Fetches live stock prices and percentage changes
- **Threshold Alerts**: Configurable high/low price thresholds per ticker
- **Volume Spike Detection**: Compares daily volume against 30-day average
- **News Context**: Fetches relevant news headlines for monitored stocks
- **Smart Alerting**: Sends alerts via Slack or logs to file (dry-run mode)
- **Continuous Monitoring**: Runs on a configurable schedule (default: every 5 minutes)

## Quick Start

### 1. Install Dependencies

```bash
source new_env/bin/activate
pip install -r requirements.txt
```

### 2. Configure Your Portfolio

Edit `config.yaml` to customize:
- Tickers to monitor
- Price thresholds (high/low)
- Volume spike sensitivity
- Slack webhook (optional)

```yaml
portfolio:
  tickers:
    - AAPL
    - GOOGL
    - MSFT

alert_rules:
  AAPL:
    price_threshold_high: 250
    price_threshold_low: 150
    volume_spike_percent: 50
```

### 3. Run the Demo

```bash
# Single check cycle
python agents/portfolio_watchdog_demo.py --mode single

# Continuous monitoring (3 cycles)
python agents/portfolio_watchdog_demo.py --mode continuous
```

### 4. Run the Agent

```bash
# Continuous monitoring (runs indefinitely)
python agents/portfolio_watchdog_agent.py
```

## Configuration

### config.yaml Structure

```yaml
portfolio:
  tickers: [list of stock tickers]

alert_rules:
  [TICKER]:
    price_threshold_high: [price]
    price_threshold_low: [price]
    volume_spike_percent: [percentage]

slack:
  webhook_url: "https://hooks.slack.com/services/..."
  dry_run: true  # Set to false to enable Slack alerts
```

### Alert Rules

- **price_threshold_high**: Alert if price exceeds this value
- **price_threshold_low**: Alert if price falls below this value
- **volume_spike_percent**: Alert if volume exceeds average by this percentage

## Tools

### load_portfolio()
Loads portfolio configuration from `config.yaml`.

**Returns:**
```json
{
  "tickers": ["AAPL", "GOOGL", ...],
  "alert_rules": {...},
  "total_tickers": 5
}
```

### get_stock_price(ticker: str)
Fetches current price, previous close, percentage change, and volume.

**Returns:**
```json
{
  "ticker": "AAPL",
  "current_price": 260.16,
  "previous_price": 261.73,
  "percent_change": -0.6,
  "volume": 20326154,
  "timestamp": "2026-02-13T12:24:13.514023"
}
```

### check_thresholds(ticker: str, current_price: float)
Checks if price breaches configured thresholds.

**Returns:**
```json
{
  "ticker": "AAPL",
  "current_price": 260.16,
  "breached": true,
  "breaches": ["Price $260.16 exceeds high threshold $250"],
  "thresholds": {"high": 250, "low": 150}
}
```

### detect_volume_spike(ticker: str)
Compares today's volume against 30-day average.

**Returns:**
```json
{
  "ticker": "AAPL",
  "today_volume": 20326154,
  "avg_volume_30d": 53480918,
  "spike_percent": -61.99,
  "threshold": 50,
  "is_spike": false
}
```

### get_news_headlines(ticker: str)
Fetches recent news headlines for context.

**Returns:**
```json
{
  "ticker": "AAPL",
  "headlines": [
    {
      "title": "Apple stock rises...",
      "link": "https://...",
      "source": "Reuters"
    }
  ],
  "count": 5
}
```

### send_alert(message: str)
Sends alert via Slack or logs to file.

**Returns:**
```json
{
  "status": "logged",
  "mode": "dry_run",
  "message": "[2026-02-13 12:24:14] Alert message"
}
```

## Slack Integration

To enable Slack alerts:

1. Create a Slack webhook: https://api.slack.com/messaging/webhooks
2. Add webhook URL to `config.yaml`:
   ```yaml
   slack:
     webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
     dry_run: false
   ```
3. Restart the agent

## Logging

Logs are written to `portfolio_alerts.log` and console output.

Log levels:
- **INFO**: Normal operations (price fetches, portfolio loads)
- **WARNING**: Threshold breaches, volume spikes
- **ERROR**: Failed API calls, configuration errors

## Testing

### Run Unit Tests

```bash
python agents/test_portfolio_watchdog.py
```

Tests all individual tools with real market data.

### Run Demo

```bash
# Single check
python agents/portfolio_watchdog_demo.py --mode single

# Continuous (3 cycles)
python agents/portfolio_watchdog_demo.py --mode continuous
```

## Architecture

```
Portfolio Watchdog Agent
├── load_portfolio()
│   └── Reads config.yaml
├── For each ticker:
│   ├── get_stock_price()
│   ├── check_thresholds()
│   ├── detect_volume_spike()
│   └── get_news_headlines()
└── send_alert()
    └── Slack or log file
```

## Performance

- **API Calls**: ~3-4 per ticker per cycle
- **Execution Time**: ~2-3 seconds per ticker
- **Memory**: ~50MB baseline
- **Recommended Interval**: 5 minutes (configurable)

## Troubleshooting

### No alerts being sent
- Check `dry_run: false` in config.yaml
- Verify Slack webhook URL is correct
- Check `portfolio_alerts.log` for errors

### Missing price data
- Verify ticker symbols are correct
- Check internet connection
- yfinance may have rate limits (wait a few minutes)

### Volume spike not detected
- Adjust `volume_spike_percent` threshold in config.yaml
- Lower values = more sensitive

## Future Enhancements

- [ ] Email alerts
- [ ] SMS alerts via Twilio
- [ ] Database persistence
- [ ] Web dashboard
- [ ] Machine learning price predictions
- [ ] Portfolio correlation analysis
- [ ] Risk metrics (Sharpe ratio, VaR)

## License

MIT

## Support

For issues or questions, check the logs in `portfolio_alerts.log`.
