#!/usr/bin/env python3
"""
What-If Scenario Agent - Web App (Simple Version)
Flask backend with inline HTML
"""

from flask import Flask, request, jsonify
from what_if_scenario_agent_v2 import FastWhatIfOrchestrator

app = Flask(__name__)

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>What-If Scenario Agent</title>
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
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }

        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }

        .input-section {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .input-section h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
        }

        textarea {
            width: 100%;
            height: 150px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.3s;
        }

        textarea:focus {
            outline: none;
            border-color: #667eea;
        }

        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }

        button {
            flex: 1;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .btn-analyze {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-analyze:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-analyze:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .btn-clear {
            background: #f0f0f0;
            color: #333;
        }

        .btn-clear:hover {
            background: #e0e0e0;
        }

        .examples {
            margin-top: 20px;
        }

        .examples h3 {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
            text-transform: uppercase;
        }

        .example-btn {
            display: block;
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            background: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 6px;
            cursor: pointer;
            text-align: left;
            font-size: 0.9em;
            color: #666;
            transition: all 0.2s;
        }

        .example-btn:hover {
            background: #e8e8ff;
            border-color: #667eea;
            color: #667eea;
        }

        .results-section {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            max-height: 600px;
            overflow-y: auto;
        }

        .results-section h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
        }

        .loading {
            text-align: center;
            color: #667eea;
            font-size: 1.1em;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #c33;
        }

        .stage {
            margin-bottom: 25px;
            border-left: 4px solid #667eea;
            padding-left: 15px;
        }

        .stage-title {
            font-weight: 600;
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.1em;
        }

        .severity-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }

        .severity-card {
            background: #f9f9f9;
            padding: 12px;
            border-radius: 6px;
            border-left: 4px solid #ddd;
        }

        .severity-card.catastrophic {
            border-left-color: #d32f2f;
            background: #ffebee;
        }

        .severity-card.severe {
            border-left-color: #f57c00;
            background: #fff3e0;
        }

        .severity-card.moderate {
            border-left-color: #fbc02d;
            background: #fffde7;
        }

        .severity-card.minor {
            border-left-color: #388e3c;
            background: #f1f8e9;
        }

        .domain-name {
            font-weight: 600;
            color: #333;
            font-size: 0.9em;
            text-transform: capitalize;
        }

        .score {
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
            margin: 5px 0;
        }

        .level {
            font-size: 0.8em;
            color: #666;
        }

        .impacts-list {
            background: #f9f9f9;
            padding: 12px;
            border-radius: 6px;
            margin-top: 10px;
            font-size: 0.9em;
            color: #555;
        }

        .impact-item {
            margin: 8px 0;
            padding: 8px;
            background: white;
            border-radius: 4px;
            border-left: 3px solid #667eea;
            padding-left: 10px;
        }

        .ripple-section {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
        }

        .ripple-chain {
            background: #f5f5f5;
            padding: 12px;
            border-radius: 6px;
            margin: 10px 0;
            font-size: 0.9em;
        }

        .chain-arrow {
            color: #667eea;
            font-weight: bold;
            margin: 0 5px;
        }

        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }

            header h1 {
                font-size: 1.8em;
            }

            .button-group {
                flex-direction: column;
            }
        }

        .empty-state {
            text-align: center;
            color: #999;
            padding: 40px 20px;
        }

        .empty-state-icon {
            font-size: 3em;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔮 What-If Scenario Agent</h1>
            <p>Analyze hypothetical scenarios through multi-stage reasoning</p>
        </header>

        <div class="main-content">
            <!-- Input Section -->
            <div class="input-section">
                <h2>Enter Scenario</h2>
                <textarea id="scenarioInput" placeholder="What if fossil fuels were banned tomorrow?&#10;What if a major earthquake hit Tokyo?&#10;What if all cars became autonomous?"></textarea>
                
                <div class="button-group">
                    <button class="btn-analyze" onclick="analyzeScenario()">Analyze</button>
                    <button class="btn-clear" onclick="clearInput()">Clear</button>
                </div>

                <div class="examples">
                    <h3>Quick Examples</h3>
                    <button class="example-btn" onclick="setExample('What if fossil fuels were banned tomorrow?')">
                        🌍 Fossil Fuels Ban
                    </button>
                    <button class="example-btn" onclick="setExample('What if a major earthquake hit Tokyo?')">
                        🏢 Tokyo Earthquake
                    </button>
                    <button class="example-btn" onclick="setExample('What if all cars became autonomous?')">
                        🚗 Autonomous Vehicles
                    </button>
                    <button class="example-btn" onclick="setExample('What if the internet went down for 30 days?')">
                        🌐 Internet Outage
                    </button>
                    <button class="example-btn" onclick="setExample('What if humans discovered alien life?')">
                        👽 Alien Discovery
                    </button>
                </div>
            </div>

            <!-- Results Section -->
            <div class="results-section" id="resultsSection">
                <div class="empty-state">
                    <div class="empty-state-icon">📊</div>
                    <p>Enter a scenario and click Analyze to see results</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        function setExample(text) {
            document.getElementById('scenarioInput').value = text;
        }

        function clearInput() {
            document.getElementById('scenarioInput').value = '';
            document.getElementById('resultsSection').innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📊</div>
                    <p>Enter a scenario and click Analyze to see results</p>
                </div>
            `;
        }

        function analyzeScenario() {
            const scenario = document.getElementById('scenarioInput').value.trim();
            
            if (!scenario) {
                alert('Please enter a scenario');
                return;
            }

            const resultsSection = document.getElementById('resultsSection');
            resultsSection.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Analyzing scenario through 6 stages...</p>
                </div>
            `;

            fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ scenario: scenario })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultsSection.innerHTML = `<div class="error">${data.error}</div>`;
                    return;
                }

                displayResults(data);
            })
            .catch(error => {
                resultsSection.innerHTML = `<div class="error">Error: ${error.message}</div>`;
            });
        }

        function displayResults(data) {
            const resultsSection = document.getElementById('resultsSection');
            const summary = data.summary;

            let html = `
                <h2>Analysis Results</h2>
                
                <div class="stage">
                    <div class="stage-title">📍 Scenario Summary</div>
                    <p><strong>Event:</strong> ${data.stages.stage_1.event}</p>
                    <p><strong>Scope:</strong> ${data.stages.stage_1.scope}</p>
                    <p><strong>Duration:</strong> ${data.stages.stage_1.duration}</p>
                    <p><strong>Scale:</strong> ${data.stages.stage_1.scale}</p>
                </div>

                <div class="stage">
                    <div class="stage-title">🌐 Impacted Domains</div>
                    <p>${summary.domains.join(', ')}</p>
                </div>

                <div class="stage">
                    <div class="stage-title">⚡ First-Order Impacts</div>
                    <div class="impacts-list">
                        ${Object.entries(summary.impacts).map(([domain, impacts]) => `
                            <div class="impact-item">
                                <strong>${domain}:</strong> ${impacts[0].description}
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="stage ripple-section">
                    <div class="stage-title">🔗 Ripple Effects</div>
                    <div>
                        <strong>Second-Order:</strong>
                        ${summary.ripples.second_order.map(r => `
                            <div class="ripple-chain">
                                ${r.cause} <span class="chain-arrow">→</span> ${r.effect}
                            </div>
                        `).join('')}
                    </div>
                    <div style="margin-top: 15px;">
                        <strong>Third-Order:</strong>
                        ${summary.ripples.third_order.map(r => `
                            <div class="ripple-chain">
                                ${r.cause} <span class="chain-arrow">→</span> ${r.effect}
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="stage">
                    <div class="stage-title">📊 Severity Rankings</div>
                    <div class="severity-grid">
                        ${Object.entries(summary.severity).map(([domain, ranking]) => {
                            const levelClass = ranking.level.toLowerCase();
                            return `
                                <div class="severity-card ${levelClass}">
                                    <div class="domain-name">${domain}</div>
                                    <div class="score">${ranking.score}/5</div>
                                    <div class="level">${ranking.level}</div>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            `;

            resultsSection.innerHTML = html;
        }

        // Allow Enter key to submit
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('scenarioInput').addEventListener('keydown', function(e) {
                if (e.ctrlKey && e.key === 'Enter') {
                    analyzeScenario();
                }
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main page."""
    return HTML_CONTENT

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze a scenario."""
    data = request.json
    scenario = data.get('scenario', '').strip()
    
    if not scenario:
        return jsonify({'error': 'Please enter a scenario'}), 400
    
    try:
        # Run the orchestrator
        orchestrator = FastWhatIfOrchestrator()
        result = orchestrator.run_workflow(scenario)
        
        # Format response
        response = {
            'status': 'success',
            'scenario': scenario,
            'stages': result['stages'],
            'summary': {
                'domains': result['stages']['stage_2']['impacted_domains'],
                'impacts': result['stages']['stage_3']['first_order_impacts'],
                'ripples': {
                    'second_order': result['stages']['stage_4']['second_order'],
                    'third_order': result['stages']['stage_4']['third_order']
                },
                'severity': result['stages']['stage_5']['rankings']
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check."""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════════════╗
║         WHAT-IF SCENARIO AGENT - WEB APP                          ║
║                                                                    ║
║  Starting Flask server...                                         ║
║  Open http://localhost:3000 in your browser                       ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=False, port=3000, host='127.0.0.1')
