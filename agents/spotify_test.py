"""
Spotify Listening Analyzer Agent - Test Script
Tests the agent with a single query.
"""

import os
from dotenv import load_dotenv
from spotify_analyzer_agent import create_spotify_agent

# Load environment variables
load_dotenv()

def test_agent():
    """Test the Spotify analyzer agent."""
    
    print("=" * 70)
    print("SPOTIFY LISTENING ANALYZER AGENT - TEST")
    print("=" * 70)
    print()
    
    # Check credentials
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ Spotify credentials not found in .env")
        return
    
    print("✓ Credentials loaded")
    print()
    
    # Create agent
    print("Creating agent...")
    agent = create_spotify_agent()
    print("✓ Agent created")
    print()
    
    # Test query
    query = "What are my top genres?"
    print(f"Query: {query}")
    print("-" * 70)
    
    try:
        response = agent(query)
        print("Response:")
        print(response)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_agent()
