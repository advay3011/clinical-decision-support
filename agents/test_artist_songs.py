"""
Test Artist Top Songs Tool
Demonstrates the new tool that finds your top 5 songs from any artist.
"""

import os
from dotenv import load_dotenv
from spotify_analyzer_agent import (
    spotify_get_data,
    get_artist_top_songs,
)

load_dotenv()

def test_artist_songs():
    """Test the artist top songs tool."""
    
    print("=" * 70)
    print("SPOTIFY - YOUR TOP SONGS FROM ANY ARTIST")
    print("=" * 70)
    print()
    
    # Get access token
    access_token = os.getenv("SPOTIFY_USER_TOKEN")
    
    if not access_token:
        print("Error: SPOTIFY_USER_TOKEN not found in .env")
        return
    
    # Fetch your top tracks
    print("Fetching your top tracks...")
    tracks_result = spotify_get_data(
        access_token=access_token,
        data_type="top_tracks",
        time_range="medium_term",
        limit=50
    )
    
    if not tracks_result.get("success"):
        print(f"Error: {tracks_result.get('error')}")
        return
    
    tracks = tracks_result.get("items", [])
    print(f"✓ Got {len(tracks)} top tracks")
    print()
    
    # Test with different artists
    test_artists = ["Drake", "Future", "A$AP Rocky", "Daniel Caesar", "Young Thug"]
    
    for artist in test_artists:
        print(f"Your top songs from {artist}:")
        print("-" * 70)
        
        result = get_artist_top_songs(tracks, artist, limit=5)
        
        if result.get("success") and result.get("found"):
            songs = result.get("top_songs", [])
            for song in songs:
                print(f"  {song['rank']}. {song['name']}")
                print(f"     Album: {song['album']}")
                print(f"     Popularity: {song['popularity']}/100")
            print(f"  Total tracks by {artist}: {result.get('total_tracks_by_artist')}")
        else:
            print(f"  {result.get('message')}")
        
        print()

if __name__ == "__main__":
    test_artist_songs()
