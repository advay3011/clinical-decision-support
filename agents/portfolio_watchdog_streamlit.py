#!/usr/bin/env python3
"""
Portfolio Watchdog Streamlit App
Beautiful web interface for portfolio monitoring
"""

import sys
import streamlit as st
from datetime import datetime
sys.path.insert(0, '.')

from agents.portfolio_watchdog_agent import (
    load_config,
    load_portfolio,
    get_stock_price,
    check_thresholds,
    detect_volume_spike,
    get_news_headlines,
    send_alert
)

# Page config
st.set_page_config(
    page_title="Portfolio Watchdog",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .alert-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .alert-warning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        color: #856404;
    }
    .alert-success {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        color: #155724;
    }
    .alert-info {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'portfolio' not in st.session_state:
    load_config()
    st.session_state.portfolio = load_portfolio()
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    page = st.radio(
        "Choose a page:",
        ["📊 Dashboard", "🔍 Check Ticker", "⚡ Alerts", "⚙️ Configuration", "💬 Chat"]
    )
    
    st.divider()
    
    st.subheader("Portfolio Info")
    st.metric("Tickers Monitored", st.session_state.portfolio['total_tickers'])
    
    if st.button("🔄 Refresh Portfolio"):
        load_config()
        st.session_state.portfolio = load_portfolio()
        st.rerun()

# Main content
st.title("📈 Portfolio Watchdog")
st.markdown("Your AI-powered portfolio monitoring assistant")

if page == "📊 Dashboard":
    st.header("Portfolio Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Tickers", st.session_state.portfolio['total_tickers'])
    
    with col2:
        st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
    
    with col3:
        st.metric("Status", "🟢 Active")
    
    st.divider()
    
    st.subheader("Portfolio Overview")
    
    tickers = st.session_state.portfolio.get("tickers", [])
    alerts_count = 0
    healthy_count = 0
    
    cols = st.columns(2)
    col_idx = 0
    
    for ticker in tickers:
        price_data = get_stock_price(ticker)
        
        if "error" in price_data:
            continue
        
        current_price = price_data["current_price"]
        percent_change = price_data["percent_change"]
        threshold_data = check_thresholds(ticker, current_price)
        
        with cols[col_idx % 2]:
            with st.container(border=True):
                col_left, col_right = st.columns([2, 1])
                
                with col_left:
                    st.subheader(ticker)
                    st.write(f"**Price:** ${current_price}")
                    st.write(f"**Change:** {percent_change:+.2f}%")
                
                with col_right:
                    if percent_change >= 0:
                        st.write("📈")
                    else:
                        st.write("📉")
                
                if threshold_data.get("breached"):
                    st.warning(f"⚠️ {threshold_data['breaches'][0]}")
                    alerts_count += 1
                else:
                    st.success("✓ Within thresholds")
                    healthy_count += 1
        
        col_idx += 1
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Healthy Tickers", healthy_count)
    with col2:
        st.metric("Active Alerts", alerts_count)

elif page == "🔍 Check Ticker":
    st.header("Check a Ticker")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker_input = st.text_input(
            "Enter ticker symbol or company name",
            placeholder="e.g., AAPL or Apple"
        )
    
    with col2:
        check_btn = st.button("🔍 Check", use_container_width=True)
    
    if check_btn and ticker_input:
        # Convert company name to ticker if needed
        company_to_ticker = {
            "apple": "AAPL", "google": "GOOGL", "microsoft": "MSFT",
            "tesla": "TSLA", "amazon": "AMZN", "meta": "META",
            "nvidia": "NVDA", "netflix": "NFLX"
        }
        
        ticker = company_to_ticker.get(ticker_input.lower(), ticker_input.upper())
        
        price_data = get_stock_price(ticker)
        
        if "error" in price_data:
            st.error(f"❌ Could not find data for {ticker}")
        else:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Current Price",
                    f"${price_data['current_price']}",
                    f"{price_data['percent_change']:+.2f}%"
                )
            
            with col2:
                st.metric("Volume", f"{price_data['volume']:,}")
            
            with col3:
                st.metric("Previous Close", f"${price_data['previous_price']}")
            
            st.divider()
            
            # Thresholds
            threshold_data = check_thresholds(ticker, price_data['current_price'])
            
            st.subheader("Price Thresholds")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**High:** ${threshold_data['thresholds']['high']}")
            with col2:
                st.write(f"**Current:** ${price_data['current_price']}")
            with col3:
                st.write(f"**Low:** ${threshold_data['thresholds']['low']}")
            
            if threshold_data.get("breached"):
                st.warning(f"⚠️ Alert: {threshold_data['breaches'][0]}")
            else:
                st.success("✓ Price is within thresholds")
            
            st.divider()
            
            # Volume
            volume_data = detect_volume_spike(ticker)
            
            st.subheader("Volume Analysis")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Today:** {volume_data['today_volume']:,}")
            with col2:
                st.write(f"**30-day Avg:** {volume_data['avg_volume_30d']:,}")
            with col3:
                st.write(f"**Change:** {volume_data['spike_percent']:.2f}%")
            
            if volume_data.get("is_spike"):
                st.warning("🔥 Volume spike detected!")
            else:
                st.info("✓ Volume is normal")
            
            st.divider()
            
            # News
            st.subheader("Recent News")
            news_data = get_news_headlines(ticker)
            
            if news_data.get("headlines"):
                for i, headline in enumerate(news_data["headlines"][:3], 1):
                    if headline["title"] and headline["title"] != "N/A":
                        st.write(f"{i}. {headline['title']}")
            else:
                st.info("No recent news available")

elif page == "⚡ Alerts":
    st.header("Recent Alerts")
    
    import os
    
    if not os.path.exists('portfolio_alerts.log'):
        st.info("No alerts yet!")
    else:
        with open('portfolio_alerts.log', 'r') as f:
            lines = f.readlines()
        
        recent = lines[-20:] if len(lines) > 20 else lines
        
        for line in reversed(recent):
            if 'WARNING' in line:
                st.warning(line.strip())
            elif 'ERROR' in line:
                st.error(line.strip())
            else:
                st.info(line.strip())

elif page == "⚙️ Configuration":
    st.header("Portfolio Configuration")
    
    st.subheader("📊 Monitored Tickers")
    
    tickers = st.session_state.portfolio.get("tickers", [])
    
    for ticker in tickers:
        st.write(f"• {ticker}")
    
    st.divider()
    
    st.subheader("⚙️ Alert Rules")
    
    for ticker, rules in st.session_state.portfolio.get("alert_rules", {}).items():
        with st.expander(f"{ticker} Settings"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**High:** ${rules.get('price_threshold_high', 'N/A')}")
            with col2:
                st.write(f"**Low:** ${rules.get('price_threshold_low', 'N/A')}")
            with col3:
                st.write(f"**Volume Spike:** {rules.get('volume_spike_percent', 'N/A')}%")

elif page == "💬 Chat":
    from agents.portfolio_financial_advisor_agent import get_financial_advice
    
    st.header("💬 Chat with Your Financial Advisor")
    st.write("Ask me anything about your portfolio and investment strategy!")
    
    # Display all messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask me something...")
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Generate response using the advisor agent
        with st.spinner("Analyzing your portfolio..."):
            response = get_financial_advice(user_input)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Rerun to display new messages
        st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    Portfolio Watchdog • Powered by AI • Last updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
</div>
""", unsafe_allow_html=True)
