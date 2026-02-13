#!/usr/bin/env python3
"""
What-If Scenario Agent - Web App
Flask backend for the agent
"""

from flask import Flask, render_template, request, jsonify
from what_if_scenario_agent_v2 import FastWhatIfOrchestrator
import json
import os

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# Store results for display
results_cache = {}

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

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
║  Open http://localhost:5000 in your browser                       ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, port=5000)
