# Stock Market Predictor Agent

A simple AI agent that analyzes stocks and explains what's happening in plain English.

## What It Does

Ask it questions about any stock, and it will:
- Tell you if the stock is going UP or DOWN
- Explain WHY the price moved
- Predict where it might go next
- Tell you if it's a good time to BUY, SELL, or HOLD

## How to Use It

### Option 1: Web Interface (Easiest)
```bash
python stock_predictor_web.py
```
Then open: `http://localhost:5000`

Click buttons or type questions like:
- "Analyze AAPL"
- "Why did TSLA drop?"
- "Should I buy GOOGL?"

### Option 2: Terminal
```bash
python stock_predictor_agent.py
```

Type questions and get answers instantly.

## Installation

1. Install Python 3.11+
2. Run:
```bash
pip install -r requirements.txt
```

3. Set up AWS credentials (in `.env` file):
```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-1
```

## All Tools (What It Can Do)

### 1. **Fetch Stock Data**
Gets the last 30 days of price history for any stock.
- Input: Stock symbol (e.g., "AAPL")
- Output: Daily prices, volume, highs/lows

### 2. **Moving Average**
Checks if the stock is going UP or DOWN.
- Compares current price to the 7-day average
- Says: "BULLISH" (going up) or "BEARISH" (going down)

### 3. **Volatility Analysis**
Measures how risky the stock is.
- LOW = Stable (safe)
- MEDIUM = Normal swings
- HIGH = Risky (big jumps)

### 4. **Price Prediction**
Predicts where the stock will go in the next 5 days.
- Uses math to find the trend
- Says: "UP" or "DOWN" with a target price

### 5. **Support & Resistance**
Finds the "floor" and "ceiling" prices.
- Floor = Price where it bounces back up (BUY zone)
- Ceiling = Price where it gets rejected (SELL zone)
- Gives signal: BUY, SELL, or HOLD

### 6. **Alibi Analysis** ⭐ NEW
Explains WHY the price moved.
- Detects: Volume surge, news events, support bounces
- Gives 3 possible reasons ranked by confidence
- Example: "Heavy selling (panic) - volume was 2x normal"

### 7. **Trading Report**
Generates a formatted summary of all analysis.

## Example Questions

```
"Analyze AAPL stock"
→ Gets data, calculates all indicators, explains everything

"Why did TSLA drop yesterday?"
→ Shows 3 alibis (reasons) ranked by confidence

"Should I buy GOOGL?"
→ Checks trend, support/resistance, gives BUY/SELL/HOLD signal

"What's the trend for MSFT?"
→ Moving average + prediction + risk level

"Explain NVDA's spike"
→ Analyzes volatility, volume, and possible catalysts
```

## What You Need

- Python 3.11 or higher
- AWS account (free tier works)
- Internet connection

## How It Works (Simple Version)

1. You ask a question
2. Agent fetches stock data
3. Agent runs all 7 tools
4. Agent explains results in simple English
5. You get your answer

## Important Notes

⚠️ **This is NOT financial advice!**
- Use this for learning only
- Always do your own research
- Consult a financial advisor before trading
- Past performance ≠ future results

## Troubleshooting

**"ModuleNotFoundError: No module named 'strands'"**
→ Run: `pip install -r requirements.txt`

**"AWS credentials error"**
→ Add AWS keys to `.env` file

**"Port 5000 already in use"**
→ Change port in `stock_predictor_web.py` line 50

## Questions?

The agent explains everything in simple terms. Just ask!

---

**Built with:** Strands AI Agent Framework + Flask + AWS Bedrock
