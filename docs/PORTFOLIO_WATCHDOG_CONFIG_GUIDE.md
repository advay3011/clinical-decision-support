# Portfolio Watchdog Configuration Guide

## Overview

The Portfolio Watchdog agent is configured via `config.yaml`. This guide explains each configuration option.

## Basic Configuration

### Portfolio Section

```yaml
portfolio:
  tickers:
    - AAPL
    - GOOGL
    - MSFT
    - TSLA
    - AMZN
```

**tickers**: List of stock symbols to monitor. Use standard ticker symbols (e.g., AAPL for Apple).

## Alert Rules

Each ticker can have custom alert rules:

```yaml
alert_rules:
  AAPL:
    price_threshold_high: 250
    price_threshold_low: 150
    volume_spike_percent: 50
```

### Price Thresholds

- **price_threshold_high**: Maximum acceptable price. Alert if exceeded.
- **price_threshold_low**: Minimum acceptable price. Alert if breached.

Example:
```yaml
AAPL:
  price_threshold_high: 250  # Alert if AAPL > $250
  price_threshold_low: 150   # Alert if AAPL < $150
```

### Volume Spike Threshold

- **volume_spike_percent**: Percentage above 30-day average to trigger alert.

Example:
```yaml
AAPL:
  volume_spike_percent: 50  # Alert if today's volume > 50% above average
```

## Slack Configuration

### Enable Slack Alerts

```yaml
slack:
  webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
  dry_run: false
```

### Dry Run Mode

```yaml
slack:
  webhook_url: ""
  dry_run: true  # Alerts logged to file instead of Slack
```

When `dry_run: true`, alerts are logged to `portfolio_alerts.log` instead of sent to Slack.

## Complete Example

```yaml
portfolio:
  tickers:
    - AAPL
    - GOOGL
    - MSFT
    - TSLA
    - AMZN
    - NVDA
    - META

alert_rules:
  AAPL:
    price_threshold_high: 250
    price_threshold_low: 150
    volume_spike_percent: 50
  
  GOOGL:
    price_threshold_high: 200
    price_threshold_low: 100
    volume_spike_percent: 50
  
  MSFT:
    price_threshold_high: 500
    price_threshold_low: 300
    volume_spike_percent: 50
  
  TSLA:
    price_threshold_high: 400
    price_threshold_low: 150
    volume_spike_percent: 75  # More sensitive for volatile stock
  
  AMZN:
    price_threshold_high: 250
    price_threshold_low: 100
    volume_spike_percent: 50
  
  NVDA:
    price_threshold_high: 200
    price_threshold_low: 80
    volume_spike_percent: 60
  
  META:
    price_threshold_high: 150
    price_threshold_low: 50
    volume_spike_percent: 50

slack:
  webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
  dry_run: false
```

## Configuration Tips

### Setting Thresholds

1. **Research current prices**: Check current prices before setting thresholds
2. **Use realistic ranges**: Set thresholds based on historical price ranges
3. **Consider volatility**: Volatile stocks may need wider ranges

Example for TSLA (volatile):
```yaml
TSLA:
  price_threshold_high: 400
  price_threshold_low: 150
  volume_spike_percent: 75  # Higher threshold = fewer false alerts
```

Example for MSFT (stable):
```yaml
MSFT:
  price_threshold_high: 500
  price_threshold_low: 300
  volume_spike_percent: 50  # Lower threshold = more sensitive
```

### Volume Spike Sensitivity

- **50%**: Moderate sensitivity (default)
- **25%**: High sensitivity (more alerts)
- **75%**: Low sensitivity (fewer alerts)

### Slack Webhook Setup

1. Go to https://api.slack.com/apps
2. Create a new app
3. Enable "Incoming Webhooks"
4. Create a new webhook for your channel
5. Copy the webhook URL to `config.yaml`

## Monitoring Multiple Portfolios

Create separate config files:

```bash
config_aggressive.yaml
config_conservative.yaml
config_tech_stocks.yaml
```

Run multiple agents:

```bash
# Terminal 1
CONFIG_FILE=config_aggressive.yaml python agents/portfolio_watchdog_agent.py

# Terminal 2
CONFIG_FILE=config_conservative.yaml python agents/portfolio_watchdog_agent.py
```

## Common Configurations

### Tech Stock Portfolio

```yaml
portfolio:
  tickers:
    - AAPL
    - GOOGL
    - MSFT
    - NVDA
    - META

alert_rules:
  AAPL:
    price_threshold_high: 250
    price_threshold_low: 150
    volume_spike_percent: 50
  GOOGL:
    price_threshold_high: 200
    price_threshold_low: 100
    volume_spike_percent: 50
  MSFT:
    price_threshold_high: 500
    price_threshold_low: 300
    volume_spike_percent: 50
  NVDA:
    price_threshold_high: 200
    price_threshold_low: 80
    volume_spike_percent: 60
  META:
    price_threshold_high: 150
    price_threshold_low: 50
    volume_spike_percent: 50
```

### Dividend Stock Portfolio

```yaml
portfolio:
  tickers:
    - JNJ
    - PG
    - KO
    - PEP
    - MCD

alert_rules:
  JNJ:
    price_threshold_high: 160
    price_threshold_low: 140
    volume_spike_percent: 40
  PG:
    price_threshold_high: 170
    price_threshold_low: 150
    volume_spike_percent: 40
  KO:
    price_threshold_high: 70
    price_threshold_low: 55
    volume_spike_percent: 40
  PEP:
    price_threshold_high: 95
    price_threshold_low: 75
    volume_spike_percent: 40
  MCD:
    price_threshold_high: 310
    price_threshold_low: 270
    volume_spike_percent: 40
```

### Aggressive Growth Portfolio

```yaml
portfolio:
  tickers:
    - TSLA
    - PLTR
    - RIOT
    - MSTR
    - COIN

alert_rules:
  TSLA:
    price_threshold_high: 400
    price_threshold_low: 150
    volume_spike_percent: 75
  PLTR:
    price_threshold_high: 50
    price_threshold_low: 15
    volume_spike_percent: 80
  RIOT:
    price_threshold_high: 30
    price_threshold_low: 5
    volume_spike_percent: 100
  MSTR:
    price_threshold_high: 500
    price_threshold_low: 200
    volume_spike_percent: 80
  COIN:
    price_threshold_high: 200
    price_threshold_low: 50
    volume_spike_percent: 90
```

## Validation

Before running the agent, validate your config:

```bash
python -c "import yaml; yaml.safe_load(open('config.yaml'))" && echo "Config valid!"
```

## Troubleshooting

### Invalid YAML syntax
- Use spaces (not tabs) for indentation
- Check for missing colons
- Verify quotes are balanced

### Ticker not found
- Verify ticker symbol is correct
- Check for typos
- Use uppercase letters

### Thresholds never trigger
- Check if thresholds are realistic
- Verify current price is between thresholds
- Check logs for price data

## Next Steps

1. Edit `config.yaml` with your portfolio
2. Test with `python agents/portfolio_watchdog_demo.py --mode single`
3. Run continuous monitoring: `python agents/portfolio_watchdog_agent.py`
