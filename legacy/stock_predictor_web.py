#!/usr/bin/env python3
"""
Stock Predictor Web Server
Flask backend for the stock predictor agent with HTML frontend.
"""

from flask import Flask, render_template, request, jsonify
from stock_predictor_agent import agent
import json
import os

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# Store conversation history
conversation_history = []


@app.route('/')
def index():
    """Serve the main page."""
    return render_template('stock_predictor.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests from the frontend."""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Add user message to history
        conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        
        # Get agent response
        agent_response = agent(user_message)
        
        # Add agent response to history
        conversation_history.append({
            'role': 'agent',
            'content': agent_response
        })
        
        return jsonify({
            'response': agent_response,
            'history': conversation_history
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear conversation history."""
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'cleared'})


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history."""
    return jsonify({'history': conversation_history})


if __name__ == '__main__':
    print("=" * 70)
    print("STOCK PREDICTOR WEB SERVER")
    print("=" * 70)
    print("\nStarting server...")
    print("Open your browser and navigate to http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    # For Replit deployment
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
