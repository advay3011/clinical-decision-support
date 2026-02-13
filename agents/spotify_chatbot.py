"""
Spotify Listening Analyzer - Interactive Chatbot
Chat with the agent about your Spotify listening habits.
"""

import os
from dotenv import load_dotenv
from spotify_analyzer_agent import create_spotify_agent

load_dotenv()

def main():
    """Run the interactive chatbot."""
    
    print("=" * 70)
    print("SPOTIFY LISTENING ANALYZER - INTERACTIVE CHATBOT")
    print("=" * 70)
    print()
    
    # Check for token
    access_token = os.getenv("SPOTIFY_USER_TOKEN")
    
    if not access_token:
        print("Error: SPOTIFY_USER_TOKEN not found in .env")
        print("Please run: python3 spotify_oauth_login_v2.py")
        return
    
    print("✓ Connected to your Spotify account")
    print()
    print("Ask me anything about your listening habits!")
    print("Examples:")
    print("  - What are my top genres?")
    print("  - Who are my favorite artists?")
    print("  - What are my top 5 songs from Drake?")
    print("  - Show me my top songs from Gunna")
    print("  - How have my tastes changed?")
    print("  - What's my music diversity?")
    print()
    print("Type 'quit' or 'exit' to leave")
    print("-" * 70)
    print()
    
    # Create agent
    agent = create_spotify_agent()
    
    # Conversation loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit", "q", "bye"]:
                print()
                print("Thanks for using Spotify Listening Analyzer! Goodbye! 🎵")
                break
            
            print()
            print("Agent: ", end="")
            response = agent(user_input)
            print(response)
            print()
        
        except KeyboardInterrupt:
            print()
            print()
            print("Goodbye! 🎵")
            break
        except Exception as e:
            print(f"Error: {e}")
            print()

if __name__ == "__main__":
    main()
