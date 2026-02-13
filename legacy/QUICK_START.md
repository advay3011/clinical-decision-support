# Quick Start (2 Minutes)

## Step 1: Install
```bash
pip install -r requirements.txt
```

## Step 2: Add AWS Keys
Create `.env` file with:
```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-1
```

## Step 3: Run

**Web Version (Easiest):**
```bash
python stock_predictor_web.py
```
Open: http://localhost:5000

**Terminal Version:**
```bash
python stock_predictor_agent.py
```

## Step 4: Ask Questions

```
"Analyze AAPL"
"Why did TSLA drop?"
"Should I buy GOOGL?"
"What's the trend for MSFT?"
```

## That's It!

The agent explains everything in simple English.

---

## All 7 Tools

| Tool | What It Does |
|------|-------------|
| **Fetch Data** | Gets stock prices |
| **Moving Average** | Says UP or DOWN |
| **Volatility** | Measures risk |
| **Prediction** | Forecasts next 5 days |
| **Support/Resistance** | Finds buy/sell zones |
| **Alibi Analysis** | Explains WHY it moved |
| **Report** | Summarizes everything |

---

## Example Output

```
You > "Why did AAPL drop?"

Agent > AAPL dropped $2.50 (1.2%) in the last 5 days.

Here are 3 possible reasons:

1. 📰 News Event (70% confidence)
   Heavy selling pressure detected. Volume was 2x normal.
   Likely: Earnings miss or bad news.

2. ➡️ Range-bound (55% confidence)
   Price moved within normal range. No major catalyst.

3. 🎯 Support Bounce (45% confidence)
   Price bounced off support level at $165.

Current Status: HOLD (wait for better entry)
```

---

**Remember:** This is for learning only. Not financial advice!
