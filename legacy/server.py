#!/usr/bin/env python3
"""
What-If Scenario Agent - Backend Server
Connects the HTML frontend to the Python agent
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from what_if_scenario_agent_v2 import FastWhatIfOrchestrator
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze a scenario."""
    try:
        data = request.json
        scenario = data.get('scenario', '').strip()
        
        if not scenario:
            return jsonify({'error': 'Please enter a scenario'}), 400
        
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
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check."""
    return jsonify({'status': 'ok', 'message': 'Backend is running'})

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════════════╗
║         WHAT-IF SCENARIO AGENT - BACKEND SERVER                   ║
║                                                                    ║
║  Backend running on http://localhost:9999                         ║
║  Open what_if_agent.html in your browser                          ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=False, port=9999, host='127.0.0.1')
