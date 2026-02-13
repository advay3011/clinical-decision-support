#!/usr/bin/env python3
"""
Recipe Agent - Flask Backend
Serves the HTML frontend and connects to the recipe agent
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from recipe_agent_simple import RecipeAgent
import os

app = Flask(__name__)
CORS(app)

# Create the agent
agent = RecipeAgent()

@app.route('/')
def serve_html():
    """Serve the HTML file."""
    html_path = os.path.join(os.path.dirname(__file__), 'recipe_app.html')
    return send_file(html_path)

@app.route('/api/ask', methods=['POST'])
def ask_agent():
    """Ask the agent a question."""
    try:
        data = request.json
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Please enter a question'}), 400
        
        print(f"\n[Backend] Question: {question}")
        
        # Ask the agent
        answer = agent.ask(question)
        
        print(f"[Backend] Answer generated")
        
        return jsonify({
            'status': 'success',
            'question': question,
            'answer': answer
        })
    
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
║              RECIPE AGENT - WEB APP                               ║
║                                                                    ║
║  Open http://localhost:5555 in your browser                       ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=False, port=5555, host='127.0.0.1', threaded=True)
