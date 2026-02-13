#!/usr/bin/env python3
"""
What-If Scenario Agent - Complete App
Frontend + Backend in one Flask app
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from what_if_scenario_agent_v2 import FastWhatIfOrchestrator
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_html():
    """Serve the HTML file."""
    html_path = os.path.join(os.path.dirname(__file__), 'what_if_agent.html')
    return send_file(html_path)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze a scenario."""
    try:
        data = request.json
        scenario = data.get('scenario', '').strip()
        
        if not scenario:
            return jsonify({'error': 'Please enter a scenario'}), 400
        
        print(f"\n[Backend] Analyzing: {scenario[:50]}...")
        
        # Run the orchestrator
        orchestrator = FastWhatIfOrchestrator()
        result = orchestrator.run_workflow(scenario)
        
        print(f"[Backend] Analysis complete")
        
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
        print(f"[Backend] Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check."""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════════════╗
║         WHAT-IF SCENARIO AGENT - FULL APP                         ║
║                                                                    ║
║  Open http://localhost:4000 in your browser                       ║
║  Backend will analyze scenarios in real-time                      ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=False, port=4000, host='127.0.0.1', threaded=True)
