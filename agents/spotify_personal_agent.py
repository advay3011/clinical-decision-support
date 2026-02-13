"""
Spotify Listening Analyzer Agent - Personal Version
Uses your personal Spotify access token to analyze your listening data.
"""

import os
from dotenv import load_dotenv
from spotify_analyzer_agent import (
    spotify_get_data,
    aggregate_genres,
    analyze_listening_patterns,
    generate_insights,
    compare_time_ranges,
)

# Load environment variables
load_dotenv()

def analyze_your_spotify():
    """Analyze your personal Spotify listening data."""
    
    print("=" * 70)
    print("SPOTIFY LISTENING ANALYZER - YOUR PERSONAL DATA")
    print("=" * 70)
    print()
    
    # Get access token
    access_token = os.getenv("SPOTIFY_USER_TOKEN")
    
    if not access_token:
        print("❌ Error: SPOTIFY_USER_TOKEN not found in .env")
        print()
        print("To get your access token:")
        print("1. Run: python3 spotify_oauth_login.py")
        print("2. Authorize the app in your browser")
        print("3. Copy the access token")
        print("4. Add to .env: SPOTIFY_USER_TOKEN='<your_token>'")
        return
    
    print("✓ Access token found")
    print()
    
    # Fetch your data
    print("Fetching your Spotify data...")
    print("-" * 70)
    
    # Get top artists (last 6 months)
    print("Fetching top artists...")
    artists_result = spotify_get_data(
        access_token=access_token,
        data_type="top_artists",
        time_range="medium_term",
        limit=50
    )
    
    if not artists_result.get("success"):
        print(f"❌ Error: {artists_result.get('error')}")
        return
    
    artists = artists_result.get("items", [])
    print(f"✓ Got {len(artists)} top artists")
    
    # Get top tracks
    print("Fetching top tracks...")
    tracks_result = spotify_get_data(
        access_token=access_token,
        data_type="top_tracks",
        time_range="medium_term",
        limit=50
    )
    
    if not tracks_result.get("success"):
        print(f"❌ Error: {tracks_result.get('error')}")
        return
    
    tracks = tracks_result.get("items", [])
    print(f"✓ Got {len(tracks)} top tracks")
    
    # Get recently played
    print("Fetching recently played...")
    recent_result = spotify_get_data(
        access_token=access_token,
        data_type="recently_played",
        limit=50
    )
    
    if not recent_result.get("success"):
        print(f"⚠ Warning: {recent_result.get('error')}")
        recent = []
    else:
        recent = recent_result.get("items", [])
    
    print(f"✓ Got {len(recent)} recently played tracks" if recent else "✓ No recently played data available")
    print()
    
    # Analyze
    print("Analyzing your listening data...")
    print("-" * 70)
    print()
    
    # Step 1: Genres
    print("STEP 1: Your Top Genres")
    print("-" * 70)
    genres_result = aggregate_genres(artists)
    
    if genres_result.get("success"):
        top_genres = genres_result.get("top_genres", [])
        print(f"Found {genres_result.get('total_unique')} unique genres")
        print("Top genres:")
        for i, genre_data in enumerate(top_genres[:10], 1):
            print(f"  {i}. {genre_data['genre']}: {genre_data['count']} mentions")
    print()
    
    # Step 2: Patterns
    print("STEP 2: Your Listening Patterns")
    print("-" * 70)
    patterns_result = analyze_listening_patterns(artists, tracks, recent)
    
    if patterns_result.get("success"):
        print(f"Top 5 artists:")
        for i, artist in enumerate(patterns_result.get("top_5_artists", []), 1):
            print(f"  {i}. {artist}")
        
        print()
        print(f"Diversity score: {patterns_result.get('diversity_score')}%")
        
        repeat_info = patterns_result.get("repeat_behavior", {})
        print(f"Repeated tracks: {repeat_info.get('repeated_tracks')} / {repeat_info.get('total_tracks')}")
        
        print()
        print("Recent favorites:")
        for fav in patterns_result.get("recent_favorites", [])[:5]:
            print(f"  • {fav['artist']}: {fav['plays']} plays")
    print()
    
    # Step 3: Insights
    print("STEP 3: Your Insights")
    print("-" * 70)
    insights_result = generate_insights(patterns_result, genres_result, "medium_term")
    
    if insights_result.get("success"):
        print(f"Time range: {insights_result.get('time_range')}")
        print()
        print("Insights:")
        for insight in insights_result.get("insights", []):
            print(f"  • {insight}")
        print()
        print("Summary:")
        print(f"  {insights_result.get('summary')}")
    print()
    
    # Step 4: Trends
    print("STEP 4: Your Trends Over Time")
    print("-" * 70)
    
    # Fetch artists for different time ranges
    short_artists = spotify_get_data(access_token, "top_artists", "short_term", 20).get("items", [])
    medium_artists = spotify_get_data(access_token, "top_artists", "medium_term", 20).get("items", [])
    long_artists = spotify_get_data(access_token, "top_artists", "long_term", 20).get("items", [])
    
    trends_result = compare_time_ranges(short_artists, medium_artists, long_artists)
    
    if trends_result.get("success"):
        print("Trends:")
        for trend in trends_result.get("trends", []):
            print(f"  • {trend}")
    print()
    
    print("=" * 70)
    print("✓ ANALYSIS COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    analyze_your_spotify()
