# Stock Market Predictor Agent - Complete Guide

## Quick Summary

**What:** An AI agent that analyzes stocks and explains everything in simple English.

**How:** Ask questions → Agent analyzes → Agent explains

**Tools:** 7 specialized tools for stock analysis

---

## The 7 Tools (Complete List)

### 1. **Fetch Stock Data**
- **What it does:** Gets 30 days of stock price history
- **Input:** Stock symbol (AAPL, GOOGL, TSLA, etc.)
- **Output:** Daily prices, volume, highs/lows
- **Example:** "Get AAPL data" → Returns 30 days of AAPL prices

### 2. **Moving Average**
- **What it does:** Checks if stock is going UP or DOWN
- **How:** Compares current price to 7-day average
- **Output:** BULLISH (📈) or BEARISH (📉)
- **Example:** Price $150 vs Average $145 = BULLISH

### 3. **Volatility Analysis**
- **What it does:** Measures how risky the stock is
- **Output:** LOW (safe), MEDIUM (normal), HIGH (risky)
- **Example:** "AAPL is LOW risk - stable price"

### 4. **Price Prediction**
- **What it does:** Predicts where stock will go in 5 days
- **How:** Uses math (linear regression) on past prices
- **Output:** Direction (UP/DOWN) + target price
- **Example:** "AAPL will go UP to $155 in 5 days"

### 5. **Support & Resistance**
- **What it does:** Finds "floor" (support) and "ceiling" (resistance)
- **Output:** BUY zone, SELL zone, trading signal
- **Example:** "Support at $140, Resistance at $160, Signal: HOLD"

### 6. **Alibi Analysis** ⭐ NEW
- **What it does:** Explains WHY the price moved
- **Output:** 3 possible reasons ranked by confidence
- **Detects:**
  - 📈 Bullish Volume Surge (buyers came in)
  - 📉 Panic Selling (forced liquidation)
  - 📰 News Event (earnings, announcement)
  - 🎯 Support Bounce (price bounced off floor)
  - 🚫 Resistance Rejection (price hit ceiling)
  - ➡️ Range-bound (normal movement)
- **Example:** "TSLA dropped because of panic selling (80% confidence) - volume was 3x normal"

### 7. **Trading Report**
- **What it does:** Summarizes all analysis in one document
- **Output:** Professional formatted report
- **Includes:** Trend, risk, prediction, support/resistance, alibis, recommendation

---

## How to Use It

### Installation (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add AWS credentials to .env file
# AWS_ACCESS_KEY_ID=your_key
# AWS_SECRET_ACCESS_KEY=your_secret
# AWS_DEFAULT_REGION=us-east-1

# 3. Run the web server
python stock_predictor_web.py

# 4. Open browser
# http://localhost:5000
```

### Example Questions

```
"Analyze AAPL"
→ Uses all 7 tools, gives complete analysis

"Why did TSLA drop?"
→ Uses Alibi Analysis, shows 3 possible reasons

"Should I buy GOOGL?"
→ Uses Moving Average + Support/Resistance, gives signal

"What's the trend for MSFT?"
→ Uses Moving Average + Prediction

"How risky is NVDA?"
→ Uses Volatility Analysis

"Explain the spike in AMZN"
→ Uses Alibi Analysis + Volatility
```

---

## Example Output

```
User: "Why did AAPL drop?"

Agent: AAPL dropped $2.50 (1.2%) in the last 5 days.

Here are 3 possible reasons:

1. 📰 News Event / Earnings (70% confidence)
   Big price swing detected. Likely earnings miss or bad news.
   Signals: High volatility, unusual movement

2. ➡️ Range-bound Movement (55% confidence)
   Price moved within normal range. No major catalyst.
   Signals: Normal volatility, consolidation

3. 🎯 Support Bounce (45% confidence)
   Price bounced off support level at $165.
   Signals: Touched support, recovery move

Current Status: HOLD (wait for better entry)

Remember: This is just analysis, not financial advice!
```

---

## Files to Share

### Minimum (Just to run it)
- `stock_predictor_agent.py` - Main agent
- `stock_predictor_web.py` - Web server
- `templates/stock_predictor.html` - Web interface
- `requirements.txt` - Dependencies
- `.env` - AWS credentials
- `QUICK_START.md` - Setup instructions

### Recommended (So they understand it)
- `SIMPLE_EXPLANATION.txt` - Simple overview
- `TOOLS_EXPLAINED.md` - Detailed tool info
- `SHARE_THIS.md` - How to share it

### Complete (Everything)
- All of the above
- `STOCK_AGENT_README.md` - Full documentation
- `AGENT_SUMMARY.txt` - Complete summary
- `test_alibi_tool.py` - Test the alibi tool
- `test_tools_only.py` - Test all tools

---

## What You Need

✓ Python 3.11+
✓ AWS account (free tier works)
✓ Internet connection
✓ 5 minutes to set up

---

## Important Notes

⚠️ **This is NOT financial advice!**
- Use for learning only
- Always do your own research
- Consult a financial advisor before trading
- Past performance does not guarantee future results

---

## How It Works (Simple Version)

```
You ask a question
        ↓
Agent fetches stock data
        ↓
Agent runs all 7 tools
        ↓
Agent analyzes results
        ↓
Agent explains in simple English
        ↓
You get your answer
```

---

## Quick Reference

| Tool | Input | Output | Time |
|------|-------|--------|------|
| Fetch Data | Symbol | 30 days prices | Instant |
| Moving Avg | Prices | UP/DOWN | Instant |
| Volatility | Prices | Risk level | Instant |
| Prediction | Prices | Target price | Instant |
| Support/Res | Prices | BUY/SELL/HOLD | Instant |
| Alibi | Prices | 3 reasons | Instant |
| Report | All data | Summary | Instant |

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'strands'"**
→ Run: `pip install -r requirements.txt`

**"AWS credentials error"**
→ Add AWS keys to `.env` file

**"Port 5000 already in use"**
→ Change port in `stock_predictor_web.py`

**"Python not found"**
→ Install Python 3.11+ from python.org

---

## To Share With Someone

1. Send them the files (see "Files to Share" section)
2. They run: `pip install -r requirements.txt`
3. They run: `python stock_predictor_web.py`
4. They open: `http://localhost:5000`
5. They ask questions!

---

## Built With

- **Strands AI Agent Framework** - Agent orchestration
- **Flask** - Web server
- **AWS Bedrock** - Claude AI model
- **Python 3.11+** - Programming language

---

## Summary

This is a complete stock analysis agent with 7 specialized tools that work together to:
- Analyze stock trends
- Measure risk
- Predict future prices
- Find buy/sell zones
- Explain price movements
- Generate reports

All in simple, beginner-friendly language.

**Ready to use?** Start with `QUICK_START.md` or `START_HERE.txt`
