#!/usr/bin/env python3
"""
Portfolio Watchdog Web Dashboard
Flask-based web interface for portfolio monitoring
"""

import sys
import json
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request
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

app = Flask(__name__)
load_config()

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio Watchdog</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .timestamp {
            color: #666;
            font-size: 14px;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card-title {
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .ticker-card {
            border-left: 4px solid #667eea;
        }
        
        .ticker-name {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .price {
            font-size: 20px;
            margin: 10px 0;
        }
        
        .price-up {
            color: #10b981;
        }
        
        .price-down {
            color: #ef4444;
        }
        
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
            font-size: 14px;
        }
        
        .metric:last-child {
            border-bottom: none;
        }
        
        .label {
            color: #666;
        }
        
        .value {
            font-weight: bold;
            color: #333;
        }
        
        .alert {
            padding: 12px;
            border-radius: 5px;
            margin-top: 10px;
            font-size: 13px;
        }
        
        .alert-warning {
            background: #fef3c7;
            color: #92400e;
            border-left: 4px solid #f59e0b;
        }
        
        .alert-success {
            background: #d1fae5;
            color: #065f46;
            border-left: 4px solid #10b981;
        }
        
        .controls {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.2s;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
        }
        
        .btn-secondary {
            background: #e5e7eb;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #d1d5db;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: white;
        }
        
        .spinner {
            border: 4px solid rgba(255,255,255,0.3);
            border-top: 4px solid white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-box {
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 28px;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        
        .error {
            background: #fee2e2;
            color: #991b1b;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #dc2626;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📈 Portfolio Watchdog</h1>
            <p class="timestamp" id="timestamp"></p>
        </header>
        
        <div class="controls">
            <button class="btn-primary" onclick="refreshPortfolio()">🔄 Refresh</button>
            <button class="btn-secondary" onclick="toggleAutoRefresh()">⏱️ Auto Refresh</button>
            <button class="btn-secondary" onclick="showStats()">📊 Stats</button>
        </div>
        
        <div id="stats" class="stats" style="display:none;"></div>
        
        <div id="content">
            <div class="loading">
                <div class="spinner"></div>
                <p>Loading portfolio...</p>
            </div>
        </div>
    </div>
    
    <script>
        let autoRefreshInterval = null;
        
        function updateTimestamp() {
            const now = new Date();
            document.getElementById('timestamp').textContent = 
                'Last updated: ' + now.toLocaleString();
        }
        
        async function refreshPortfolio() {
            updateTimestamp();
            try {
                const response = await fetch('/api/portfolio');
                const data = await response.json();
                renderPortfolio(data);
            } catch (error) {
                document.getElementById('content').innerHTML = 
                    '<div class="error">Error loading portfolio: ' + error + '</div>';
            }
        }
        
        function renderPortfolio(data) {
            let html = '<div class="grid">';
            
            for (const ticker of data.tickers) {
                const tickerData = data.data[ticker];
                
                if (!tickerData) {
                    html += `
                        <div class="card ticker-card">
                            <div class="ticker-name">${ticker}</div>
                            <div class="error">Failed to load data</div>
                        </div>
                    `;
                    continue;
                }
                
                const priceClass = tickerData.percent_change >= 0 ? 'price-up' : 'price-down';
                const changeSymbol = tickerData.percent_change >= 0 ? '▲' : '▼';
                
                let alerts = '';
                if (tickerData.threshold_breach) {
                    alerts += `<div class="alert alert-warning">⚠️ ${tickerData.threshold_breach}</div>`;
                }
                if (tickerData.volume_spike) {
                    alerts += `<div class="alert alert-warning">⚠️ ${tickerData.volume_spike}</div>`;
                }
                if (!alerts) {
                    alerts = '<div class="alert alert-success">✓ All clear</div>';
                }
                
                html += `
                    <div class="card ticker-card">
                        <div class="ticker-name">${ticker}</div>
                        <div class="price ${priceClass}">
                            $${tickerData.current_price} ${changeSymbol} ${tickerData.percent_change:+.2f}%
                        </div>
                        <div class="metric">
                            <span class="label">Volume:</span>
                            <span class="value">${(tickerData.volume / 1000000).toFixed(1)}M</span>
                        </div>
                        <div class="metric">
                            <span class="label">Thresholds:</span>
                            <span class="value">$${tickerData.threshold_low}-$${tickerData.threshold_high}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Vol Avg (30d):</span>
                            <span class="value">${(tickerData.avg_volume / 1000000).toFixed(1)}M</span>
                        </div>
                        ${alerts}
                    </div>
                `;
            }
            
            html += '</div>';
            document.getElementById('content').innerHTML = html;
        }
        
        async function showStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                let html = `
                    <div class="stat-box">
                        <div class="stat-number">${stats.total_tickers}</div>
                        <div class="stat-label">Tickers</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">${stats.alerts_triggered}</div>
                        <div class="stat-label">Alerts</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">${stats.healthy_tickers}</div>
                        <div class="stat-label">Healthy</div>
                    </div>
                `;
                
                document.getElementById('stats').innerHTML = html;
                document.getElementById('stats').style.display = 'grid';
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }
        
        function toggleAutoRefresh() {
            if (autoRefreshInterval) {
                clearInterval(autoRefreshInterval);
                autoRefreshInterval = null;
                alert('Auto refresh disabled');
            } else {
                autoRefreshInterval = setInterval(refreshPortfolio, 30000);
                alert('Auto refresh enabled (every 30 seconds)');
            }
        }
        
        // Initial load
        refreshPortfolio();
        updateTimestamp();
        setInterval(updateTimestamp, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Render dashboard"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/portfolio')
def api_portfolio():
    """Get portfolio data"""
    portfolio = load_portfolio()
    tickers = portfolio.get("tickers", [])
    
    data = {
        "tickers": tickers,
        "data": {}
    }
    
    for ticker in tickers:
        price_data = get_stock_price(ticker)
        
        if "error" in price_data:
            data["data"][ticker] = None
            continue
        
        current_price = price_data["current_price"]
        threshold_data = check_thresholds(ticker, current_price)
        volume_data = detect_volume_spike(ticker)
        
        threshold_breach = None
        if threshold_data.get("breached"):
            threshold_breach = threshold_data['breaches'][0]
        
        volume_spike = None
        if "error" not in volume_data and volume_data.get("is_spike"):
            volume_spike = f"Volume spike: {volume_data['spike_percent']:.2f}%"
        
        data["data"][ticker] = {
            "current_price": current_price,
            "percent_change": price_data["percent_change"],
            "volume": price_data["volume"],
            "threshold_low": threshold_data['thresholds']['low'],
            "threshold_high": threshold_data['thresholds']['high'],
            "threshold_breach": threshold_breach,
            "avg_volume": volume_data.get("avg_volume_30d", 0),
            "volume_spike": volume_spike
        }
    
    return jsonify(data)

@app.route('/api/stats')
def api_stats():
    """Get portfolio statistics"""
    portfolio = load_portfolio()
    tickers = portfolio.get("tickers", [])
    
    alerts = 0
    healthy = 0
    
    for ticker in tickers:
        price_data = get_stock_price(ticker)
        
        if "error" not in price_data:
            current_price = price_data["current_price"]
            threshold_data = check_thresholds(ticker, current_price)
            volume_data = detect_volume_spike(ticker)
            
            has_alert = (threshold_data.get("breached") or 
                        ("error" not in volume_data and volume_data.get("is_spike")))
            
            if has_alert:
                alerts += 1
            else:
                healthy += 1
    
    return jsonify({
        "total_tickers": len(tickers),
        "alerts_triggered": alerts,
        "healthy_tickers": healthy
    })

@app.route('/api/check/<ticker>')
def api_check_ticker(ticker):
    """Check single ticker"""
    ticker = ticker.upper()
    
    price_data = get_stock_price(ticker)
    if "error" in price_data:
        return jsonify({"error": price_data["error"]}), 400
    
    current_price = price_data["current_price"]
    threshold_data = check_thresholds(ticker, current_price)
    volume_data = detect_volume_spike(ticker)
    news_data = get_news_headlines(ticker)
    
    return jsonify({
        "ticker": ticker,
        "price": price_data,
        "thresholds": threshold_data,
        "volume": volume_data,
        "news": news_data
    })

@app.route('/api/alert', methods=['POST'])
def api_send_alert():
    """Send alert"""
    data = request.json
    message = data.get("message", "")
    
    if not message:
        return jsonify({"error": "Message required"}), 400
    
    result = send_alert(message)
    return jsonify(result)

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Portfolio Watchdog Web Dashboard")
    print("=" * 70)
    print("\n🌐 Starting web server...")
    print("📍 Open http://localhost:5000 in your browser")
    print("⏹️  Press Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
