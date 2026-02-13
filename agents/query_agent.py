"""
Query the Spotify Agent
Simple script to answer questions about your Spotify data.
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

def answer_question(question):
    """Answer a question about Spotify data."""
    
    access_token = os.getenv("SPOTIFY_USER_TOKEN")
    
    if not access_token:
        print("Error: SPOTIFY_USER_TOKEN not found in .env")
        return
    
    question_lower = question.lower()
    
    print(f"Question: {question}")
    print("-" * 70)
    
    # How have tastes changed
    if "change" in question_lower or "taste" in question_lower or "evolved" in question_lower:
        print("Analyzing how your tastes have changed over time...")
        print()
        
        # Get artists for different time ranges
        short = spotify_get_data(access_token, "top_artists", "short_term", 20).get("items", [])
        medium = spotify_get_data(access_token, "top_artists", "medium_term", 20).get("items", [])
        long = spotify_get_data(access_token, "top_artists", "long_term", 20).get("items", [])
        
        trends = compare_time_ranges(short, medium, long)
        
        if trends.get("success"):
            print("Your Music Taste Evolution:")
            print()
            for trend in trends.get("trends", []):
                print(f"  • {trend}")
            print()
            print("New Favorites (recent discoveries):")
            for artist in trends.get("new_favorites", [])[:5]:
                print(f"  - {artist}")
            print()
            print("Consistent Favorites (always in top):")
            for artist in trends.get("consistent_favorites", [])[:5]:
                print(f"  - {artist}")
            print()
            print("Artists You Used to Listen to:")
            for artist in trends.get("fading_favorites", [])[:5]:
                print(f"  - {artist}")
    
    # Top genres
    elif "genre" in question_lower:
        print("Fetching your top genres...")
        print()
        
        artists = spotify_get_data(access_token, "top_artists", "medium_term", 50).get("items", [])
        genres = aggregate_genres(artists)
        
        if genres.get("success"):
            print("Your Top Genres:")
            for g in genres.get("top_genres", [])[:10]:
                print(f"  • {g['genre']}: {g['count']} mentions")
    
    # Top artists
    elif "artist" in question_lower and "favorite" in question_lower:
        print("Fetching your favorite artists...")
        print()
        
        artists = spotify_get_data(access_token, "top_artists", "medium_term", 20).get("items", [])
        
        print("Your Top 10 Artists:")
        for i, artist in enumerate(artists[:10], 1):
            print(f"  {i}. {artist.get('name')}")
    
    # Top songs from artist
    elif "song" in question_lower or "track" in question_lower:
        print("Fetching your top tracks...")
        print()
        
        tracks = spotify_get_data(access_token, "top_tracks", "medium_term", 10).get("items", [])
        
        print("Your Top 10 Tracks:")
        for i, track in enumerate(tracks, 1):
            artist = track.get("artists", [{}])[0].get("name", "Unknown")
            print(f"  {i}. {track.get('name')} - {artist}")
    
    # Listening patterns
    elif "pattern" in question_lower or "habit" in question_lower:
        print("Analyzing your listening patterns...")
        print()
        
        artists = spotify_get_data(access_token, "top_artists", "medium_term", 50).get("items", [])
        tracks = spotify_get_data(access_token, "top_tracks", "medium_term", 50).get("items", [])
        
        patterns = analyze_listening_patterns(artists, tracks, [])
        
        if patterns.get("success"):
            print("Your Listening Patterns:")
            print(f"  Top 5 Artists: {', '.join(patterns.get('top_5_artists', [])[:5])}")
            print(f"  Diversity Score: {patterns.get('diversity_score')}%")
            repeat = patterns.get("repeat_behavior", {})
            print(f"  Repeated Tracks: {repeat.get('repeated_tracks')} / {repeat.get('total_tracks')}")
    
    else:
        print("I can help with:")
        print("  - How have your tastes changed?")
        print("  - What are your top genres?")
        print("  - Who are your favorite artists?")
        print("  - What are your top songs?")
        print("  - What are your listening patterns?")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        answer_question(question)
    else:
        print("Usage: python3 query_agent.py 'Your question here'")
