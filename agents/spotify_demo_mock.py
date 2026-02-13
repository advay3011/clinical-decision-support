"""
Spotify Listening Analyzer Agent - Demo with Mock Data
Demonstrates the agent with sample Spotify data.
"""

import os
from dotenv import load_dotenv
from spotify_analyzer_agent import (
    aggregate_genres,
    analyze_listening_patterns,
    generate_insights,
    compare_time_ranges,
)

# Load environment variables
load_dotenv()

# Mock Spotify data
MOCK_ARTISTS = [
    {
        "id": "1",
        "name": "Drake",
        "genres": ["hip-hop", "rap", "canadian hip-hop"],
        "popularity": 95,
        "followers": {"total": 50000000}
    },
    {
        "id": "2",
        "name": "The Weeknd",
        "genres": ["r-n-b", "hip-hop", "pop"],
        "popularity": 94,
        "followers": {"total": 40000000}
    },
    {
        "id": "3",
        "name": "Kendrick Lamar",
        "genres": ["hip-hop", "rap", "west coast hip-hop"],
        "popularity": 92,
        "followers": {"total": 35000000}
    },
    {
        "id": "4",
        "name": "J. Cole",
        "genres": ["hip-hop", "rap", "r-n-b"],
        "popularity": 90,
        "followers": {"total": 30000000}
    },
    {
        "id": "5",
        "name": "Kanye West",
        "genres": ["hip-hop", "rap", "pop"],
        "popularity": 88,
        "followers": {"total": 28000000}
    },
    {
        "id": "6",
        "name": "Travis Scott",
        "genres": ["hip-hop", "trap", "rap"],
        "popularity": 87,
        "followers": {"total": 25000000}
    },
    {
        "id": "7",
        "name": "Post Malone",
        "genres": ["hip-hop", "pop", "trap"],
        "popularity": 86,
        "followers": {"total": 24000000}
    },
    {
        "id": "8",
        "name": "Lil Baby",
        "genres": ["hip-hop", "trap", "rap"],
        "popularity": 85,
        "followers": {"total": 22000000}
    },
    {
        "id": "9",
        "name": "Playboi Carti",
        "genres": ["hip-hop", "trap", "rap"],
        "popularity": 84,
        "followers": {"total": 20000000}
    },
    {
        "id": "10",
        "name": "Juice WRLD",
        "genres": ["hip-hop", "emo rap", "trap"],
        "popularity": 83,
        "followers": {"total": 19000000}
    },
]

MOCK_TRACKS = [
    {"id": "1", "name": "One Dance", "artists": [{"name": "Drake"}], "popularity": 95},
    {"id": "2", "name": "Blinding Lights", "artists": [{"name": "The Weeknd"}], "popularity": 94},
    {"id": "3", "name": "HUMBLE.", "artists": [{"name": "Kendrick Lamar"}], "popularity": 92},
    {"id": "4", "name": "No Role Modelz", "artists": [{"name": "J. Cole"}], "popularity": 90},
    {"id": "5", "name": "Stronger", "artists": [{"name": "Kanye West"}], "popularity": 88},
    {"id": "6", "name": "SICKO MODE", "artists": [{"name": "Travis Scott"}], "popularity": 87},
    {"id": "7", "name": "Circles", "artists": [{"name": "Post Malone"}], "popularity": 86},
    {"id": "8", "name": "Drip Too Hard", "artists": [{"name": "Lil Baby"}], "popularity": 85},
    {"id": "9", "name": "Magnolia", "artists": [{"name": "Playboi Carti"}], "popularity": 84},
    {"id": "10", "name": "Lucid Dreams", "artists": [{"name": "Juice WRLD"}], "popularity": 83},
]

MOCK_RECENT = [
    {"track": {"id": "1", "name": "One Dance", "artists": [{"name": "Drake"}]}},
    {"track": {"id": "2", "name": "Blinding Lights", "artists": [{"name": "The Weeknd"}]}},
    {"track": {"id": "3", "name": "HUMBLE.", "artists": [{"name": "Kendrick Lamar"}]}},
    {"track": {"id": "1", "name": "One Dance", "artists": [{"name": "Drake"}]}},
    {"track": {"id": "4", "name": "No Role Modelz", "artists": [{"name": "J. Cole"}]}},
]

def demo():
    """Run demo with mock data."""
    
    print("=" * 70)
    print("SPOTIFY LISTENING ANALYZER - DEMO WITH MOCK DATA")
    print("=" * 70)
    print()
    
    # Test 1: Aggregate genres
    print("STEP 1: Aggregate Genres")
    print("-" * 70)
    genres_result = aggregate_genres(MOCK_ARTISTS)
    
    print(f"✓ Found {genres_result.get('total_unique')} unique genres")
    print(f"  Top genres:")
    for genre_data in genres_result.get("top_genres", [])[:5]:
        print(f"    - {genre_data['genre']}: {genre_data['count']} mentions")
    print()
    
    # Test 2: Analyze patterns
    print("STEP 2: Analyze Listening Patterns")
    print("-" * 70)
    patterns_result = analyze_listening_patterns(MOCK_ARTISTS, MOCK_TRACKS, MOCK_RECENT)
    
    print(f"✓ Pattern analysis complete")
    print(f"  Top 5 artists: {', '.join(patterns_result.get('top_5_artists', []))}")
    print(f"  Diversity score: {patterns_result.get('diversity_score')}%")
    repeat_info = patterns_result.get("repeat_behavior", {})
    print(f"  Repeated tracks: {repeat_info.get('repeated_tracks')} / {repeat_info.get('total_tracks')}")
    print()
    
    # Test 3: Generate insights
    print("STEP 3: Generate Insights")
    print("-" * 70)
    insights_result = generate_insights(patterns_result, genres_result, "medium_term")
    
    print(f"✓ Insights generated")
    print(f"  Time range: {insights_result.get('time_range')}")
    print(f"  Insights:")
    for insight in insights_result.get("insights", []):
        print(f"    • {insight}")
    print()
    print(f"  Summary:")
    print(f"  {insights_result.get('summary')}")
    print()
    
    # Test 4: Compare time ranges
    print("STEP 4: Compare Time Ranges")
    print("-" * 70)
    
    # Use same mock data for all ranges (in real scenario, would be different)
    trends_result = compare_time_ranges(MOCK_ARTISTS[:5], MOCK_ARTISTS[2:7], MOCK_ARTISTS)
    
    print(f"✓ Time range comparison complete")
    print(f"  Trends:")
    for trend in trends_result.get("trends", []):
        print(f"    • {trend}")
    print()
    
    print("=" * 70)
    print("✓ DEMO COMPLETE!")
    print("=" * 70)
    print()
    print("To use with real Spotify data:")
    print("1. Get a user access token from Spotify OAuth")
    print("2. Use the spotify_get_data tool with your access token")
    print("3. Pass the results to the analysis tools")
    print()

if __name__ == "__main__":
    demo()
