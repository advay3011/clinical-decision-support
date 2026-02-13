# Stock Market Predictor Agent - Share This

## What Is This?

An AI agent that analyzes stocks and explains what's happening in plain English.

Think of it as a smart friend who:
- Watches stock prices
- Explains if they're going UP or DOWN
- Tells you WHY they moved
- Predicts where they'll go next
- Says if it's a good time to BUY, SELL, or HOLD

## How to Use It

### Web Version (Easiest - No Terminal)
```bash
python stock_predictor_web.py
```
Then open: `http://localhost:5000`

Just type questions like:
- "Analyze AAPL"
- "Why did TSLA drop?"
- "Should I buy GOOGL?"

### Terminal Version
```bash
python stock_predictor_agent.py
```

Type the same questions.

## What It Can Do

| What | Example |
|------|---------|
| **Trend** | "AAPL is BULLISH (going up)" |
| **Risk** | "TSLA is HIGH risk (big swings)" |
| **Prediction** | "GOOGL will go to $150 in 5 days" |
| **Buy/Sell Zones** | "Support at $140, Resistance at $160" |
| **Explain Moves** | "MSFT dropped because of heavy selling" |
| **Full Report** | "Here's a complete analysis of NVDA" |

## The 7 Tools

1. **Fetch Data** - Gets stock prices
2. **Moving Average** - Says UP or DOWN
3. **Volatility** - Measures risk
4. **Prediction** - Forecasts next 5 days
5. **Support/Resistance** - Finds buy/sell zones
6. **Alibi Analysis** - Explains WHY it moved
7. **Report** - Summarizes everything

## Installation (5 Minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add AWS credentials to .env file
# (Ask for these if you don't have them)

# 3. Run it
python stock_predictor_web.py
```

## Example Conversation

```
You: "Analyze AAPL"

Agent: AAPL is at $150. Here's what's happening:

📈 TREND: BULLISH (going up)
- Current price $150 is above the 7-day average of $145
- This means upward momentum

⚠️ RISK: MEDIUM
- Price swings are moderate
- Not too risky, not too stable

📊 PREDICTION: UP
- Predicted to reach $155 in 5 days
- That's a +3.3% gain

🎯 BUY/SELL ZONES:
- Support (floor): $140 - Good place to buy
- Resistance (ceiling): $160 - Good place to sell
- Current: $150 - In the middle, so HOLD

📰 WHY IT MOVED:
1. Bullish Volume Surge (80% confidence)
   - Heavy buying pressure
   - Volume was 2x normal

2. News Event (70% confidence)
   - Could be positive earnings

3. Support Bounce (45% confidence)
   - Price bounced off support level

💡 RECOMMENDATION: HOLD
Wait for price to drop to $140 to buy, or rise to $160 to sell.

Remember: This is analysis only, not financial advice!
```

## What You Need

- Python 3.11+
- AWS account (free tier works)
- Internet connection
- 5 minutes to set up

## Important

⚠️ **This is NOT financial advice!**
- Use for learning only
- Always do your own research
- Consult a financial advisor
- Past performance ≠ future results

## Questions?

Just ask the agent! It explains everything in simple terms.

---

**Ready to use?**

1. Install: `pip install -r requirements.txt`
2. Run: `python stock_predictor_web.py`
3. Open: `http://localhost:5000`
4. Ask questions!

That's it! 🚀
