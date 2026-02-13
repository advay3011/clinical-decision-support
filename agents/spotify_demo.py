"""
Spotify Listening Analyzer Agent - Demo
Shows how to use the agent with real Spotify API calls.
"""

import os
from dotenv import load_dotenv
from spotify_analyzer_agent import create_spotify_agent

# Load environment variables
load_dotenv()


def main():
    """Run the Spotify analyzer agent demo."""
    
    print("=" * 70)
    print("SPOTIFY LISTENING ANALYZER AGENT")
    print("=" * 70)
    print()
    
    # Create agent
    agent = create_spotify_agent()
    
    # Example queries
    queries = [
        "What are my top genres?",
        "Who are my favorite artists?",
        "Do I repeat songs often?",
        "What are my listening patterns?",
        "How has my taste changed over time?",
    ]
    
    print("SETUP REQUIRED:")
    print("-" * 70)
    print("1. Get Spotify API credentials:")
    print("   - Go to https://developer.spotify.com/dashboard")
    print("   - Create an app")
    print("   - Copy Client ID and Client Secret")
    print()
    print("2. Set environment variables:")
    print("   export SPOTIFY_CLIENT_ID='your_client_id'")
    print("   export SPOTIFY_CLIENT_SECRET='your_client_secret'")
    print()
    print("3. Authenticate with Spotify to get your access token")
    print()
    print("-" * 70)
    print()
    
    # Check for credentials
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")
    
    if not client_id or not client_secret:
        print("⚠️  Spotify credentials not found in environment variables.")
        print("Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET to run the demo.")
        print()
        print("Example queries the agent can handle:")
        for i, query in enumerate(queries, 1):
            print(f"  {i}. {query}")
        return
    
    print("✓ Spotify credentials found!")
    print()
    print("EXAMPLE QUERIES:")
    print("-" * 70)
    for i, query in enumerate(queries, 1):
        print(f"  {i}. {query}")
    print()
    print("-" * 70)
    print()
    
    # Interactive mode
    print("Enter a query (or 'quit' to exit):")
    print()
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        print()
        print("Agent: ", end="")
        response = agent(user_input)
        print(response)
        print()


if __name__ == "__main__":
    main()
