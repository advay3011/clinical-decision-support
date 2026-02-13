"""
Spotify Listening Analyzer - Simple Interactive Chatbot
No credential prompts - uses token from .env directly.
"""

import os
from dotenv import load_dotenv
from spotify_analyzer_agent import (
    fetch_all_top_tracks,
    spotify_get_data,
    get_artist_top_songs,
    aggregate_genres,
    analyze_listening_patterns,
    generate_insights,
    compare_time_ranges,
)

load_dotenv()

def main():
    """Run the simple interactive chatbot."""
    
    print("=" * 70)
    print("SPOTIFY LISTENING ANALYZER - CHATBOT")
    print("=" * 70)
    print()
    
    # Get token
    access_token = os.getenv("SPOTIFY_USER_TOKEN")
    
    if not access_token:
        print("Error: SPOTIFY_USER_TOKEN not found in .env")
        print("Run: python3 spotify_oauth_login_v2.py")
        return
    
    print("✓ Connected to Spotify")
    print()
    print("Ask me about your music!")
    print("Examples:")
    print("  - What are my top genres?")
    print("  - Who are my favorite artists?")
    print("  - What are my top 5 songs from Drake?")
    print("  - Show me my top songs from Gunna")
    print()
    print("Type 'quit' to exit")
    print("-" * 70)
    print()
    
    # Fetch all tracks once
    print("Loading your Spotify data...")
    all_tracks_result = fetch_all_top_tracks(access_token, "medium_term", 500)
    
    if not all_tracks_result.get("success"):
        print(f"Error: {all_tracks_result.get('error')}")
        return
    
    all_tracks = all_tracks_result.get("items", [])
    print(f"✓ Loaded {len(all_tracks)} of your top tracks")
    print()
    
    # Chat loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye! 🎵")
                break
            
            print()
            
            # Simple keyword matching for responses
            user_lower = user_input.lower()
            
            if "genre" in user_lower:
                # Get genres
                artists_result = spotify_get_data(access_token, "top_artists", "medium_term", 50)
                if artists_result.get("success"):
                    artists = artists_result.get("items", [])
                    genres_result = aggregate_genres(artists)
                    if genres_result.get("success"):
                        top_genres = genres_result.get("top_genres", [])
                        print("Your top genres:")
                        for i, g in enumerate(top_genres[:10], 1):
                            print(f"  {i}. {g['genre']}: {g['count']} mentions")
                    else:
                        print(f"Error: {genres_result.get('error')}")
                else:
                    print(f"Error: {artists_result.get('error')}")
            
            elif "artist" in user_lower and "favorite" in user_lower:
                # Get top artists
                artists_result = spotify_get_data(access_token, "top_artists", "medium_term", 50)
                if artists_result.get("success"):
                    artists = artists_result.get("items", [])
                    print("Your top 10 artists:")
                    for i, artist in enumerate(artists[:10], 1):
                        print(f"  {i}. {artist.get('name')}")
                else:
                    print(f"Error: {artists_result.get('error')}")
            
            elif "song" in user_lower or "track" in user_lower:
                # Get top songs from specific artist or just top tracks
                if any(artist in user_input for artist in ["Drake", "Gunna", "Future", "A$AP Rocky", "Young Thug", "Daniel Caesar"]):
                    # Extract artist name
                    for artist in ["Drake", "Gunna", "Future", "A$AP Rocky", "Young Thug", "Daniel Caesar"]:
                        if artist.lower() in user_lower:
                            result = get_artist_top_songs(all_tracks, artist, 5)
                            if result.get("success") and result.get("found"):
                                print(f"Your top 5 songs from {artist}:")
                                for song in result.get("top_songs", []):
                                    print(f"  {song['rank']}. {song['name']}")
                                    print(f"     Album: {song['album']}")
                            else:
                                print(result.get("message"))
                            break
                else:
                    # Just show top tracks
                    tracks_result = spotify_get_data(access_token, "top_tracks", "medium_term", 10)
                    if tracks_result.get("success"):
                        tracks = tracks_result.get("items", [])
                        print("Your top 10 tracks:")
                        for i, track in enumerate(tracks, 1):
                            artist = track.get("artists", [{}])[0].get("name", "Unknown")
                            print(f"  {i}. {track.get('name')} - {artist}")
                    else:
                        print(f"Error: {tracks_result.get('error')}")
            
            elif "pattern" in user_lower or "habit" in user_lower:
                # Get listening patterns
                artists_result = spotify_get_data(access_token, "top_artists", "medium_term", 50)
                tracks_result = spotify_get_data(access_token, "top_tracks", "medium_term", 50)
                
                if artists_result.get("success") and tracks_result.get("success"):
                    artists = artists_result.get("items", [])
                    tracks = tracks_result.get("items", [])
                    patterns = analyze_listening_patterns(artists, tracks, [])
                    
                    if patterns.get("success"):
                        print("Your listening patterns:")
                        print(f"  Top 5 artists: {', '.join(patterns.get('top_5_artists', [])[:5])}")
                        print(f"  Diversity score: {patterns.get('diversity_score')}%")
                        repeat = patterns.get("repeat_behavior", {})
                        print(f"  Repeated tracks: {repeat.get('repeated_tracks')} / {repeat.get('total_tracks')}")
                else:
                    print("Error fetching data")
            
            else:
                print("I can help with:")
                print("  - Your top genres")
                print("  - Your favorite artists")
                print("  - Your top songs from an artist")
                print("  - Your listening patterns")
                print()
                print("Try asking: 'What are my top genres?' or 'Show me my top songs from Drake'")
            
            print()
        
        except KeyboardInterrupt:
            print()
            print("Goodbye! 🎵")
            break
        except Exception as e:
            print(f"Error: {e}")
            print()

if __name__ == "__main__":
    main()
