"""
Spotify Listening Analyzer Agent - Full Test with Tool Calls
Tests the agent with actual Spotify API calls.
"""

import os
from dotenv import load_dotenv
from spotify_analyzer_agent import (
    spotify_auth,
    spotify_get_data,
    aggregate_genres,
    analyze_listening_patterns,
    generate_insights,
    compare_time_ranges,
)

# Load environment variables
load_dotenv()

def test_tools():
    """Test all Spotify tools."""
    
    print("=" * 70)
    print("SPOTIFY LISTENING ANALYZER - TOOL TEST")
    print("=" * 70)
    print()
    
    # Get credentials
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ Spotify credentials not found in .env")
        return
    
    print("✓ Credentials loaded")
    print()
    
    # Test 1: Authentication
    print("TEST 1: Spotify Authentication")
    print("-" * 70)
    auth_result = spotify_auth(client_id, client_secret)
    
    if not auth_result.get("success"):
        print(f"❌ Authentication failed: {auth_result.get('error')}")
        return
    
    access_token = auth_result.get("access_token")
    print(f"✓ Authentication successful")
    print(f"  Token: {access_token[:20]}...")
    print(f"  Expires in: {auth_result.get('expires_in')} seconds")
    print()
    
    # Test 2: Fetch top artists
    print("TEST 2: Fetch Top Artists")
    print("-" * 70)
    artists_result = spotify_get_data(
        access_token=access_token,
        data_type="top_artists",
        time_range="medium_term",
        limit=10
    )
    
    if not artists_result.get("success"):
        print(f"❌ Failed to fetch artists: {artists_result.get('error')}")
        return
    
    artists = artists_result.get("items", [])
    print(f"✓ Fetched {len(artists)} top artists")
    for i, artist in enumerate(artists[:3], 1):
        print(f"  {i}. {artist.get('name')} - Genres: {', '.join(artist.get('genres', [])[:2])}")
    print()
    
    # Test 3: Fetch top tracks
    print("TEST 3: Fetch Top Tracks")
    print("-" * 70)
    tracks_result = spotify_get_data(
        access_token=access_token,
        data_type="top_tracks",
        time_range="medium_term",
        limit=10
    )
    
    if not tracks_result.get("success"):
        print(f"❌ Failed to fetch tracks: {tracks_result.get('error')}")
        return
    
    tracks = tracks_result.get("items", [])
    print(f"✓ Fetched {len(tracks)} top tracks")
    for i, track in enumerate(tracks[:3], 1):
        artist_name = track.get("artists", [{}])[0].get("name", "Unknown")
        print(f"  {i}. {track.get('name')} - {artist_name}")
    print()
    
    # Test 4: Fetch recently played
    print("TEST 4: Fetch Recently Played")
    print("-" * 70)
    recent_result = spotify_get_data(
        access_token=access_token,
        data_type="recently_played",
        limit=10
    )
    
    if not recent_result.get("success"):
        print(f"❌ Failed to fetch recently played: {recent_result.get('error')}")
        return
    
    recent = recent_result.get("items", [])
    print(f"✓ Fetched {len(recent)} recently played tracks")
    for i, item in enumerate(recent[:3], 1):
        track = item.get("track", {})
        artist_name = track.get("artists", [{}])[0].get("name", "Unknown")
        print(f"  {i}. {track.get('name')} - {artist_name}")
    print()
    
    # Test 5: Aggregate genres
    print("TEST 5: Aggregate Genres")
    print("-" * 70)
    genres_result = aggregate_genres(artists)
    
    if not genres_result.get("success"):
        print(f"❌ Failed to aggregate genres: {genres_result.get('error')}")
        return
    
    top_genres = genres_result.get("top_genres", [])
    print(f"✓ Found {genres_result.get('total_unique')} unique genres")
    print(f"  Top genres:")
    for genre_data in top_genres[:5]:
        print(f"    - {genre_data['genre']}: {genre_data['count']} mentions")
    print()
    
    # Test 6: Analyze patterns
    print("TEST 6: Analyze Listening Patterns")
    print("-" * 70)
    patterns_result = analyze_listening_patterns(artists, tracks, recent)
    
    if not patterns_result.get("success"):
        print(f"❌ Failed to analyze patterns: {patterns_result.get('error')}")
        return
    
    print(f"✓ Pattern analysis complete")
    print(f"  Top 5 artists: {', '.join(patterns_result.get('top_5_artists', [])[:3])}")
    print(f"  Diversity score: {patterns_result.get('diversity_score')}%")
    repeat_info = patterns_result.get("repeat_behavior", {})
    print(f"  Repeated tracks: {repeat_info.get('repeated_tracks')} / {repeat_info.get('total_tracks')}")
    print()
    
    # Test 7: Generate insights
    print("TEST 7: Generate Insights")
    print("-" * 70)
    insights_result = generate_insights(patterns_result, genres_result, "medium_term")
    
    if not insights_result.get("success"):
        print(f"❌ Failed to generate insights: {insights_result.get('error')}")
        return
    
    print(f"✓ Insights generated")
    print(f"  Time range: {insights_result.get('time_range')}")
    print(f"  Insights:")
    for insight in insights_result.get("insights", []):
        print(f"    - {insight}")
    print()
    
    # Test 8: Compare time ranges
    print("TEST 8: Compare Time Ranges")
    print("-" * 70)
    
    # Fetch artists for different time ranges
    short_artists = spotify_get_data(access_token, "top_artists", "short_term", 10).get("items", [])
    medium_artists = spotify_get_data(access_token, "top_artists", "medium_term", 10).get("items", [])
    long_artists = spotify_get_data(access_token, "top_artists", "long_term", 10).get("items", [])
    
    trends_result = compare_time_ranges(short_artists, medium_artists, long_artists)
    
    if not trends_result.get("success"):
        print(f"❌ Failed to compare time ranges: {trends_result.get('error')}")
        return
    
    print(f"✓ Time range comparison complete")
    print(f"  Trends:")
    for trend in trends_result.get("trends", []):
        print(f"    - {trend}")
    print()
    
    print("=" * 70)
    print("✓ ALL TESTS PASSED!")
    print("=" * 70)

if __name__ == "__main__":
    test_tools()
