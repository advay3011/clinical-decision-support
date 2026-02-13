# Portfolio Watchdog - Quick Start Guide

Get your portfolio monitoring agent running in 5 minutes.

## Prerequisites

- Python 3.9+
- Virtual environment (already created: `new_env`)

## Step 1: Activate Environment

```bash
source new_env/bin/activate
```

## Step 2: Verify Installation

All dependencies are already installed. Verify:

```bash
pip list | grep -E "strands-agents|yfinance|pyyaml"
```

Should show:
- strands-agents
- yfinance
- pyyaml

## Step 3: Configure Your Portfolio

Edit `config.yaml`:

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
  # ... add more tickers
```

## Step 4: Test the Agent

Run a single check cycle:

```bash
python agents/portfolio_watchdog_demo.py --mode single
```

Expected output:
```
======================================================================
PORTFOLIO WATCHDOG - SINGLE CHECK CYCLE
======================================================================

[STEP 1] Loading portfolio configuration...
✓ Portfolio loaded with 3 tickers: AAPL, GOOGL, MSFT

[STEP 2] Checking AAPL...
  ✓ Price: $259.97 (-0.67%)
  ✓ Volume: 20,406,109
  ✓ Within thresholds ($150-$250)
  ✓ Volume normal (-61.85% vs 30-day avg)

[STEP 3] Sending 0 alert(s)...
No alerts to send - portfolio is healthy!

======================================================================
CHECK CYCLE COMPLETE
======================================================================
```

## Step 5: Run Comprehensive Tests

```bash
python agents/test_portfolio_comprehensive.py
```

Expected: All 35 tests pass ✓

## Step 6: Run Continuous Monitoring

Option A: Demo mode (3 cycles, 10 seconds apart):
```bash
python agents/portfolio_watchdog_demo.py --mode continuous
```

Option B: Production mode (runs indefinitely, 5 minutes between checks):
```bash
python agents/portfolio_watchdog_agent.py
```

Press `Ctrl+C` to stop.

## Step 7: Check Logs

View alerts in real-time:

```bash
tail -f portfolio_alerts.log
```

## Configuration Examples

### Tech Stocks

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

### Dividend Stocks

```yaml
portfolio:
  tickers:
    - JNJ
    - PG
    - KO

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
```

## Enable Slack Alerts

1. Create Slack webhook: https://api.slack.com/messaging/webhooks
2. Update `config.yaml`:

```yaml
slack:
  webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
  dry_run: false
```

3. Restart the agent

## Troubleshooting

### No alerts showing up?
- Check `portfolio_alerts.log`
- Verify thresholds are realistic
- Run demo mode to see what's happening

### "No data found" error?
- Verify ticker symbols are correct
- Check internet connection
- Wait a few minutes (yfinance rate limits)

### Want to monitor different stocks?
- Edit `config.yaml`
- Restart the agent
- No code changes needed!

## Next Steps

- Read [Configuration Guide](PORTFOLIO_WATCHDOG_CONFIG_GUIDE.md) for advanced options
- Read [Advanced Usage](PORTFOLIO_WATCHDOG_ADVANCED.md) for custom tools
- Read [Full Documentation](PORTFOLIO_WATCHDOG_README.md) for complete reference

## File Structure

```
.
├── config.yaml                          # Your portfolio configuration
├── portfolio_alerts.log                 # Alert logs
├── agents/
│   ├── portfolio_watchdog_agent.py      # Main agent (production)
│   ├── portfolio_watchdog_demo.py       # Demo script
│   ├── test_portfolio_watchdog.py       # Basic tests
│   └── test_portfolio_comprehensive.py  # Full test suite
└── docs/
    ├── PORTFOLIO_WATCHDOG_README.md     # Full documentation
    ├── PORTFOLIO_WATCHDOG_CONFIG_GUIDE.md
    ├── PORTFOLIO_WATCHDOG_ADVANCED.md
    └── PORTFOLIO_WATCHDOG_QUICKSTART.md # This file
```

## Common Commands

```bash
# Activate environment
source new_env/bin/activate

# Run single check
python agents/portfolio_watchdog_demo.py --mode single

# Run continuous demo (3 cycles)
python agents/portfolio_watchdog_demo.py --mode continuous

# Run production agent
python agents/portfolio_watchdog_agent.py

# Run all tests
python agents/test_portfolio_comprehensive.py

# View logs
tail -f portfolio_alerts.log

# Validate config
python -c "import yaml; yaml.safe_load(open('config.yaml'))" && echo "Valid!"
```

## Support

For issues:
1. Check `portfolio_alerts.log`
2. Run tests: `python agents/test_portfolio_comprehensive.py`
3. Check configuration: `python -c "import yaml; print(yaml.safe_load(open('config.yaml')))"`

## What's Next?

- Monitor your portfolio 24/7
- Get alerts when prices breach thresholds
- Detect unusual volume activity
- Stay informed with news headlines
- Customize alerts via Slack

Happy monitoring! 📈
