# Portfolio Watchdog - Interactive Edition

A fully interactive portfolio monitoring agent with CLI and web dashboard interfaces.

## ✅ Status: COMPLETE & PRODUCTION READY

- ✅ 6 core tools implemented
- ✅ 35 comprehensive tests (all passing)
- ✅ Interactive CLI interface
- ✅ Beautiful web dashboard
- ✅ REST API endpoints
- ✅ Complete documentation

## Quick Start (Choose Your Interface)

### Option 1: Interactive CLI (Recommended for Desktop)

```bash
source new_env/bin/activate
python agents/portfolio_watchdog_interactive.py
```

**Features:**
- Menu-driven interface
- Check single or full portfolio
- Add/remove tickers
- Edit configuration
- Continuous monitoring
- View alerts
- Run tests
- Color-coded output

### Option 2: Web Dashboard (Recommended for Remote Access)

```bash
source new_env/bin/activate
python agents/portfolio_watchdog_web.py
```

Then open: **http://localhost:5000**

**Features:**
- Beautiful responsive UI
- Real-time price updates
- Auto-refresh capability
- Portfolio statistics
- Mobile friendly
- Remote access
- REST API endpoints

### Option 3: Command Line (Programmatic)

```bash
# Single check
python agents/portfolio_watchdog_demo.py --mode single

# Continuous monitoring
python agents/portfolio_watchdog_agent.py
```

## What's Included

### Core Implementation
- `agents/portfolio_watchdog_agent.py` - Main agent with 6 tools
- `agents/portfolio_watchdog_demo.py` - Demo script
- `agents/portfolio_watchdog_interactive.py` - Interactive CLI
- `agents/portfolio_watchdog_web.py` - Web dashboard
- `config.yaml` - Portfolio configuration

### Testing
- `agents/test_portfolio_watchdog.py` - Basic tests
- `agents/test_portfolio_comprehensive.py` - 35 comprehensive tests

### Documentation
- `docs/PORTFOLIO_WATCHDOG_INTERACTIVE.md` - Interactive interfaces guide
- `docs/PORTFOLIO_WATCHDOG_README.md` - Full documentation
- `docs/PORTFOLIO_WATCHDOG_CONFIG_GUIDE.md` - Configuration reference
- `docs/PORTFOLIO_WATCHDOG_ADVANCED.md` - Advanced usage
- `docs/PORTFOLIO_WATCHDOG_QUICKSTART.md` - Quick start
- `docs/PORTFOLIO_WATCHDOG_INDEX.md` - Documentation index

## Features

### Monitoring
- ✅ Real-time stock price tracking
- ✅ Configurable price thresholds (high/low)
- ✅ Volume spike detection (vs 30-day average)
- ✅ News headline fetching for context

### Alerting
- ✅ Slack webhook integration
- ✅ File logging (dry-run mode)
- ✅ Alert history tracking
- ✅ Timestamp tracking

### Interactive Interfaces
- ✅ CLI with 9 menu options
- ✅ Web dashboard with live updates
- ✅ Portfolio management (add/remove tickers)
- ✅ Configuration editing
- ✅ Continuous monitoring
- ✅ Statistics display

### Production Ready
- ✅ Comprehensive error handling
- ✅ Detailed logging
- ✅ Configuration-driven
- ✅ Performance optimized
- ✅ Type-safe data handling
- ✅ REST API endpoints

## CLI Interface

### Main Menu Options

```
1) Check single ticker
   - Enter ticker symbol
   - View price, volume, thresholds
   - See news headlines

2) Check full portfolio
   - Monitor all tickers
   - View all alerts
   - Send alerts automatically

3) View portfolio configuration
   - See all tickers
   - View alert rules
   - Check thresholds

4) Add ticker
   - Add new stock to monitor
   - Set custom thresholds
   - Configure volume sensitivity

5) Remove ticker
   - Remove stock from portfolio
   - Select from list

6) Edit configuration
   - Open config.yaml in editor
   - Make manual changes

7) Continuous monitoring
   - Run continuous checks
   - Customize interval
   - Alerts sent automatically

8) View recent alerts
   - See last 20 alerts
   - Color-coded by severity

9) Run tests
   - Execute full test suite
   - Verify all tools

0) Exit
```

## Web Dashboard

### Dashboard Features

- **Portfolio Overview**: Real-time price display for all tickers
- **Ticker Cards**: Individual cards showing:
  - Current price with % change
  - Trading volume
  - Price thresholds
  - 30-day average volume
  - Alert status

- **Controls**:
  - 🔄 Refresh: Manually refresh data
  - ⏱️ Auto Refresh: Enable/disable auto-refresh (30 seconds)
  - 📊 Stats: View portfolio statistics

- **Statistics**:
  - Total tickers monitored
  - Number of active alerts
  - Number of healthy tickers

### API Endpoints

```bash
# Get all portfolio data
curl http://localhost:5000/api/portfolio

# Get portfolio statistics
curl http://localhost:5000/api/stats

# Check single ticker
curl http://localhost:5000/api/check/AAPL

# Send alert
curl -X POST http://localhost:5000/api/alert \
  -H "Content-Type: application/json" \
  -d '{"message": "AAPL price alert"}'
```

## Configuration

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

slack:
  webhook_url: ""  # Add your Slack webhook
  dry_run: true    # Set to false to enable Slack
```

## Tools

| Tool | Purpose |
|------|---------|
| `load_portfolio()` | Load tickers and alert rules |
| `get_stock_price()` | Fetch live price, volume, % change |
| `check_thresholds()` | Detect price threshold breaches |
| `detect_volume_spike()` | Detect unusual volume activity |
| `get_news_headlines()` | Fetch relevant news for context |
| `send_alert()` | Send Slack or log alerts |

## Test Results

```
Ran 35 tests in 11.753s
Successes: 35
Failures: 0
Errors: 0
✓ PASS
```

## Common Commands

```bash
# Activate environment
source new_env/bin/activate

# Run interactive CLI
python agents/portfolio_watchdog_interactive.py

# Run web dashboard
python agents/portfolio_watchdog_web.py

# Run single check
python agents/portfolio_watchdog_demo.py --mode single

# Run continuous monitoring
python agents/portfolio_watchdog_agent.py

# Run all tests
python agents/test_portfolio_comprehensive.py

# View logs
tail -f portfolio_alerts.log

# Validate configuration
python -c "import yaml; yaml.safe_load(open('config.yaml'))" && echo "Valid!"
```

## Usage Scenarios

### Scenario 1: Quick Portfolio Check
```bash
python agents/portfolio_watchdog_interactive.py
# Select option 2 (Check full portfolio)
# View all tickers and alerts
```

### Scenario 2: Add New Stock
```bash
python agents/portfolio_watchdog_interactive.py
# Select option 4 (Add ticker)
# Enter ticker, thresholds, volume sensitivity
```

### Scenario 3: Monitor from Browser
```bash
python agents/portfolio_watchdog_web.py
# Open http://localhost:5000
# View dashboard
# Click "Auto Refresh" for continuous updates
```

### Scenario 4: Continuous Monitoring
```bash
python agents/portfolio_watchdog_interactive.py
# Select option 7 (Continuous monitoring)
# Set interval (e.g., 60 seconds)
# Monitor runs continuously
```

### Scenario 5: Remote Monitoring
```bash
# On server
python agents/portfolio_watchdog_web.py

# On client machine
# Open http://server-ip:5000
# View dashboard from anywhere
```

## Performance

- CLI startup: <1 second
- Single price fetch: 1-2 seconds
- Full portfolio check: 2-3 seconds per ticker
- Web page load: <1 second
- API response: <2 seconds
- Memory usage: 50-100MB

## Documentation

### Getting Started
- **[Interactive Guide](docs/PORTFOLIO_WATCHDOG_INTERACTIVE.md)** - CLI and web dashboard guide
- **[Quick Start](docs/PORTFOLIO_WATCHDOG_QUICKSTART.md)** - 5-minute setup

### Reference
- **[Full README](docs/PORTFOLIO_WATCHDOG_README.md)** - Complete documentation
- **[Configuration Guide](docs/PORTFOLIO_WATCHDOG_CONFIG_GUIDE.md)** - Configuration reference
- **[Documentation Index](docs/PORTFOLIO_WATCHDOG_INDEX.md)** - Full documentation map

### Advanced
- **[Advanced Usage](docs/PORTFOLIO_WATCHDOG_ADVANCED.md)** - Custom tools and strategies

## Troubleshooting

### CLI not starting
```bash
python -m py_compile agents/portfolio_watchdog_interactive.py
```

### Web dashboard not loading
```bash
# Check if port 5000 is available
lsof -i :5000

# Try different port in code
```

### No data showing
- Check `portfolio_alerts.log` for errors
- Verify internet connection
- Verify ticker symbols are correct
- Run tests: `python agents/test_portfolio_comprehensive.py`

## Next Steps

1. **Choose Interface**: CLI or Web Dashboard
2. **Configure Portfolio**: Edit `config.yaml`
3. **Run Tests**: Verify setup
4. **Start Monitoring**: Use your chosen interface
5. **Enable Alerts**: Add Slack webhook (optional)

## File Structure

```
.
├── config.yaml                                    # Portfolio config
├── portfolio_alerts.log                           # Alert logs
├── agents/
│   ├── portfolio_watchdog_agent.py               # Core agent
│   ├── portfolio_watchdog_demo.py                # Demo script
│   ├── portfolio_watchdog_interactive.py         # CLI interface
│   ├── portfolio_watchdog_web.py                 # Web dashboard
│   ├── test_portfolio_watchdog.py                # Basic tests
│   └── test_portfolio_comprehensive.py           # Full test suite
└── docs/
    ├── PORTFOLIO_WATCHDOG_INTERACTIVE.md         # Interactive guide
    ├── PORTFOLIO_WATCHDOG_README.md              # Full docs
    ├── PORTFOLIO_WATCHDOG_CONFIG_GUIDE.md        # Configuration
    ├── PORTFOLIO_WATCHDOG_ADVANCED.md            # Advanced usage
    ├── PORTFOLIO_WATCHDOG_QUICKSTART.md          # Quick start
    └── PORTFOLIO_WATCHDOG_INDEX.md               # Documentation index
```

## Summary

✅ **Portfolio Watchdog is fully interactive and production-ready.**

Choose your interface:
- **CLI**: `python agents/portfolio_watchdog_interactive.py`
- **Web**: `python agents/portfolio_watchdog_web.py`

Start monitoring your portfolio in seconds! 📈
