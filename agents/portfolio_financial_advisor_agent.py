#!/usr/bin/env python3
"""
Portfolio Financial Advisor Agent
AI-powered financial advisor using Strands SDK for intelligent portfolio analysis
"""

import sys
sys.path.insert(0, '.')

from strands import Agent, tool
from agents.portfolio_watchdog_agent import (
    load_config,
    load_portfolio,
    get_stock_price,
    check_thresholds,
    detect_volume_spike,
    get_news_headlines,
)

# Initialize portfolio
load_config()
portfolio = load_portfolio()

@tool
def analyze_stock(ticker: str) -> dict:
    """Analyze a single stock with price, volume, and threshold data"""
    price_data = get_stock_price(ticker)
    if "error" in price_data:
        return {"error": f"Could not fetch data for {ticker}"}
    
    threshold_data = check_thresholds(ticker, price_data["current_price"])
    volume_data = detect_volume_spike(ticker)
    news_data = get_news_headlines(ticker)
    
    return {
        "ticker": ticker,
        "price": price_data["current_price"],
        "change_percent": price_data["percent_change"],
        "volume": price_data["volume"],
        "threshold_breached": threshold_data.get("breached", False),
        "threshold_high": threshold_data["thresholds"]["high"],
        "threshold_low": threshold_data["thresholds"]["low"],
        "volume_spike": volume_data.get("is_spike", False),
        "volume_spike_percent": volume_data.get("spike_percent", 0),
        "recent_news": [h["title"] for h in news_data.get("headlines", [])[:2] if h["title"] != "N/A"]
    }

@tool
def analyze_portfolio() -> dict:
    """Analyze entire portfolio and return status"""
    tickers = portfolio.get("tickers", [])
    stocks = []
    alerts = 0
    
    for ticker in tickers:
        analysis = analyze_stock(ticker)
        if "error" not in analysis:
            stocks.append(analysis)
            if analysis["threshold_breached"]:
                alerts += 1
    
    return {
        "total_stocks": len(tickers),
        "stocks": stocks,
        "active_alerts": alerts,
        "portfolio_health": "Good" if alerts == 0 else f"Warning: {alerts} alert(s)"
    }

@tool
def get_buy_sell_recommendation(ticker: str) -> str:
    """Get buy/sell/hold recommendation for a stock"""
    analysis = analyze_stock(ticker)
    
    if "error" in analysis:
        return f"Cannot analyze {ticker} - data unavailable"
    
    price_change = analysis["change_percent"]
    threshold_breached = analysis["threshold_breached"]
    volume_spike = analysis["volume_spike"]
    
    recommendation = ""
    
    # Strong signals
    if price_change > 10 and volume_spike:
        recommendation = f"🚀 STRONG BUY - {ticker} is up {price_change:.2f}% with high volume. Momentum is strong!"
    elif price_change < -10 and volume_spike:
        recommendation = f"⚠️ STRONG SELL - {ticker} is down {price_change:.2f}% with high volume. Consider taking profits."
    
    # Moderate signals
    elif price_change > 5:
        recommendation = f"📈 BUY - {ticker} is performing well, up {price_change:.2f}%. Good momentum."
    elif price_change < -5:
        recommendation = f"📉 SELL - {ticker} is down {price_change:.2f}%. Consider reviewing your position."
    
    # Threshold signals
    elif threshold_breached:
        recommendation = f"⚠️ ALERT - {ticker} has breached your price limits. Review your position immediately."
    
    # Neutral
    else:
        recommendation = f"➡️ HOLD - {ticker} is stable at ${analysis['price']}. Monitor for changes."
    
    return recommendation

@tool
def get_risk_assessment() -> str:
    """Assess portfolio risk level"""
    portfolio_analysis = analyze_portfolio()
    stocks = portfolio_analysis["stocks"]
    
    if not stocks:
        return "No stocks to analyze"
    
    # Calculate risk metrics
    avg_change = sum(s["change_percent"] for s in stocks) / len(stocks)
    volatility = max(abs(s["change_percent"]) for s in stocks)
    alerts = portfolio_analysis["active_alerts"]
    
    risk_level = "LOW"
    if volatility > 10 or alerts > 2:
        risk_level = "HIGH"
    elif volatility > 5 or alerts > 0:
        risk_level = "MEDIUM"
    
    assessment = f"""
📊 PORTFOLIO RISK ASSESSMENT:
- Risk Level: {risk_level}
- Average Change: {avg_change:+.2f}%
- Max Volatility: {volatility:.2f}%
- Active Alerts: {alerts}

Recommendation: {'Diversify and reduce exposure' if risk_level == 'HIGH' else 'Monitor closely' if risk_level == 'MEDIUM' else 'Portfolio is stable'}
"""
    return assessment

@tool
def get_diversification_advice() -> str:
    """Get advice on portfolio diversification"""
    portfolio_analysis = analyze_portfolio()
    stocks = portfolio_analysis["stocks"]
    
    if len(stocks) < 3:
        return "⚠️ Your portfolio has fewer than 3 stocks. Consider diversifying across more sectors and companies to reduce risk."
    
    # Analyze sector concentration (simplified)
    tech_stocks = ["AAPL", "GOOGL", "MSFT", "NVDA", "META", "TSLA"]
    finance_stocks = ["JPM", "BAC", "GS", "WFC"]
    
    tech_count = sum(1 for s in stocks if s["ticker"] in tech_stocks)
    finance_count = sum(1 for s in stocks if s["ticker"] in finance_stocks)
    
    advice = "✅ Your portfolio appears well-diversified.\n"
    
    if tech_count > len(stocks) * 0.6:
        advice += "⚠️ You have heavy tech exposure. Consider adding healthcare, finance, or energy stocks.\n"
    
    if finance_count > len(stocks) * 0.6:
        advice += "⚠️ You have heavy finance exposure. Consider adding tech or consumer stocks.\n"
    
    advice += f"\nCurrent holdings: {', '.join(s['ticker'] for s in stocks)}"
    
    return advice

# Create the financial advisor agent
advisor_agent = Agent(
    tools=[
        analyze_stock,
        analyze_portfolio,
        get_buy_sell_recommendation,
        get_risk_assessment,
        get_diversification_advice
    ],
    system_prompt="""You are an expert financial advisor with deep knowledge of stock market analysis, portfolio management, and investment strategy.

Your role is to:
1. Analyze individual stocks and portfolios using the available tools
2. Provide buy/sell/hold recommendations based on price movement, volume, and thresholds
3. Assess portfolio risk and suggest diversification strategies
4. Explain financial concepts in simple, understandable terms
5. Give actionable advice based on data, not speculation

Always:
- Use the tools to get real data before giving advice
- Explain your reasoning clearly
- Mention both opportunities and risks
- Remind users that this is data-based advice, not financial advice
- Be professional but friendly and approachable
- Use emojis to make advice more engaging
- Provide specific, actionable recommendations

When users ask about:
- Specific stocks: Use analyze_stock tool and get_buy_sell_recommendation
- Portfolio status: Use analyze_portfolio tool
- Risk: Use get_risk_assessment tool
- Diversification: Use get_diversification_advice tool
- General advice: Combine multiple tools for comprehensive analysis
"""
)

def get_financial_advice(user_query: str) -> str:
    """Get financial advice from the advisor agent"""
    try:
        response = advisor_agent(user_query)
        return response
    except Exception as e:
        return f"I encountered an error analyzing your request: {str(e)}"

if __name__ == "__main__":
    # Test the advisor
    print("🤖 Portfolio Financial Advisor Agent")
    print("=" * 50)
    
    # Test queries
    test_queries = [
        "What's my portfolio status?",
        "Should I buy AAPL?",
        "Analyze my portfolio risk",
        "How diversified is my portfolio?",
        "Give me investment recommendations"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("-" * 50)
        advice = get_financial_advice(query)
        print(f"💡 Advice:\n{advice}")
        print()
