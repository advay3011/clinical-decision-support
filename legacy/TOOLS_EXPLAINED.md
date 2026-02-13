# Stock Agent Tools - Simple Explanations

## The 7 Tools

### 1️⃣ Fetch Stock Data
**What:** Gets the last 30 days of stock prices

**Input:** Stock symbol (AAPL, GOOGL, TSLA, etc.)

**Output:** 
- Daily prices (open, high, low, close)
- Trading volume
- Date

**Example:**
```
Fetch AAPL data
→ Returns 30 days of AAPL prices
```

---

### 2️⃣ Moving Average
**What:** Checks if stock is going UP or DOWN

**How:** Compares current price to the 7-day average

**Output:**
- Current price
- Average price
- Trend: BULLISH (📈) or BEARISH (📉)

**Example:**
```
Current price: $150
7-day average: $145
Trend: BULLISH (price is above average = going up!)
```

---

### 3️⃣ Volatility Analysis
**What:** Measures how risky the stock is

**How:** Calculates how much the price jumps around

**Output:**
- Risk level: LOW, MEDIUM, or HIGH
- Price range (lowest to highest)
- Daily returns

**Example:**
```
Risk: LOW
Price range: $140 - $160
Meaning: Stock is stable, not too risky
```

---

### 4️⃣ Price Prediction
**What:** Predicts where the stock will go in 5 days

**How:** Uses math (linear regression) on past prices

**Output:**
- Direction: UP or DOWN
- Target price
- Percentage change

**Example:**
```
Current: $150
Predicted: $155 (in 5 days)
Change: +3.3% UP
```

---

### 5️⃣ Support & Resistance
**What:** Finds the "floor" and "ceiling" prices

**How:** Looks at where price bounces up or gets rejected

**Output:**
- Floor price (support) = BUY zone
- Ceiling price (resistance) = SELL zone
- Trading signal: BUY, SELL, or HOLD

**Example:**
```
Floor: $140 (price bounces here)
Ceiling: $160 (price stops here)
Current: $150 (in the middle)
Signal: HOLD (wait for better time)
```

---

### 6️⃣ Alibi Analysis ⭐ NEW
**What:** Explains WHY the price moved

**How:** Detects patterns in volume, volatility, and price action

**Output:** 3 possible reasons ranked by confidence

**Alibis it detects:**
- 📈 Bullish Volume Surge (buyers came in)
- 📉 Panic Selling (forced liquidation)
- 📰 News Event (earnings, announcement)
- 🎯 Support Bounce (price bounced off floor)
- 🚫 Resistance Rejection (price hit ceiling)
- ➡️ Range-bound (normal movement)

**Example:**
```
Why did TSLA drop $5?

Alibi 1: Panic Selling (80% confidence)
- Volume was 3x normal
- Price gapped down
- Likely: Forced selling or bad news

Alibi 2: News Event (70% confidence)
- High volatility detected
- Could be earnings miss

Alibi 3: Support Bounce (45% confidence)
- Price bounced off support
- But volume was high (suggests selling)
```

---

### 7️⃣ Trading Report
**What:** Summarizes all analysis in one report

**How:** Combines all 6 tools into one formatted document

**Output:** Professional trading report with:
- Current price
- Trend analysis
- Risk assessment
- Prediction
- Support/Resistance levels
- Alibis
- Recommendation

**Example:**
```
═══════════════════════════════════════
STOCK MARKET ANALYSIS REPORT
Symbol: AAPL
═══════════════════════════════════════

TREND: BULLISH (going up)
RISK: MEDIUM (moderate swings)
PREDICTION: UP to $155 in 5 days
SUPPORT: $140 | RESISTANCE: $160
SIGNAL: HOLD (wait for better entry)

WHY IT MOVED:
- Heavy buying (volume 2x normal)
- Positive news catalyst
- Bounced off support level

RECOMMENDATION: HOLD
═══════════════════════════════════════
```

---

## How They Work Together

```
You ask: "Should I buy AAPL?"

Agent does this:
1. Fetch Data → Gets 30 days of prices
2. Moving Average → Checks trend (BULLISH/BEARISH)
3. Volatility → Measures risk (LOW/MEDIUM/HIGH)
4. Prediction → Forecasts next 5 days
5. Support/Resistance → Finds buy/sell zones
6. Alibi Analysis → Explains recent moves
7. Report → Summarizes everything

Agent says: "AAPL is BULLISH, LOW risk, predicted UP. 
Support at $140, Resistance at $160. Current price $150 
is in the middle. HOLD and wait for a dip to $140 to buy."
```

---

## Quick Reference

| Tool | Input | Output | Time |
|------|-------|--------|------|
| Fetch Data | Symbol | 30 days prices | Instant |
| Moving Avg | Prices | UP/DOWN trend | Instant |
| Volatility | Prices | Risk level | Instant |
| Prediction | Prices | Target price | Instant |
| Support/Res | Prices | BUY/SELL/HOLD | Instant |
| Alibi | Prices | 3 reasons | Instant |
| Report | All data | Summary | Instant |

---

## Example Questions & Which Tools They Use

```
"Analyze AAPL"
→ Uses: All 7 tools

"Is AAPL going up or down?"
→ Uses: Moving Average

"How risky is AAPL?"
→ Uses: Volatility

"Where will AAPL go?"
→ Uses: Prediction

"Should I buy AAPL?"
→ Uses: Support/Resistance + Moving Average

"Why did AAPL drop?"
→ Uses: Alibi Analysis

"Give me a full report on AAPL"
→ Uses: All 7 tools + Report
```

---

## Remember

✅ All tools work together automatically
✅ Agent explains everything in simple English
✅ Just ask questions naturally
✅ No need to understand the math

❌ This is NOT financial advice
❌ Don't trade based on this alone
❌ Always do your own research
