"""
Ask the Spotify Agent a Question
Simple script to ask the agent a single question and get a response.
"""

import os
import sys
from dotenv import load_dotenv
from spotify_analyzer_agent import create_spotify_agent

load_dotenv()

def ask_agent(question):
    """Ask the agent a question and get a response."""
    
    # Check for token
    access_token = os.getenv("SPOTIFY_USER_TOKEN")
    
    if not access_token:
        print("Error: SPOTIFY_USER_TOKEN not found in .env")
        return
    
    # Create agent
    agent = create_spotify_agent()
    
    # Ask question
    print(f"Question: {question}")
    print("-" * 70)
    response = agent(question)
    print(response)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        ask_agent(question)
    else:
        print("Usage: python3 ask_agent.py 'Your question here'")
        print()
        print("Examples:")
        print("  python3 ask_agent.py 'What are my top genres?'")
        print("  python3 ask_agent.py 'Who are my favorite artists?'")
        print("  python3 ask_agent.py 'What are my top 5 songs from Gunna?'")
