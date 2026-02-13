"""
Spotify Listening Analyzer Agent
Analyzes user's Spotify listening habits and generates insights using Strands framework.
"""

import os
import json
import requests
from typing import Optional
from datetime import datetime
from collections import Counter
from strands import Agent, tool
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


# ============================================================================
# TOOL 1: SpotifyAuthTool - OAuth2 Authentication
# ============================================================================

@tool
def spotify_auth(client_id: str, client_secret: str, redirect_uri: str = "http://localhost:8888/callback") -> dict:
    """Authenticate with Spotify OAuth2 and get access token.
    
    Args:
        client_id: Spotify app client ID
        client_secret: Spotify app client secret
        redirect_uri: OAuth redirect URI (default: localhost:8888/callback)
    
    Returns:
        Dictionary with access_token and token_type
    """
    auth_url = "https://accounts.spotify.com/api/token"
    
    # Using Client Credentials flow for server-to-server authentication
    # For user data access, use Authorization Code flow instead
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    
    try:
        response = requests.post(auth_url, data=auth_data)
        response.raise_for_status()
        token_data = response.json()
        return {
            "success": True,
            "access_token": token_data.get("access_token"),
            "token_type": token_data.get("token_type", "Bearer"),
            "expires_in": token_data.get("expires_in"),
            "note": "Using Client Credentials flow. For user data, use Authorization Code flow with user consent."
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# TOOL 2: SpotifyDataTool - Fetch Spotify Data
# ============================================================================

@tool
def spotify_get_data(access_token: str, data_type: str, time_range: str = "medium_term", limit: int = 20, offset: int = 0) -> dict:
    """Fetch data from Spotify Web API with pagination support.
    
    Args:
        access_token: Valid Spotify access token
        data_type: Type of data to fetch ('top_artists', 'top_tracks', 'recently_played')
        time_range: Time range for top items ('short_term', 'medium_term', 'long_term')
        limit: Number of items per request (max 50)
        offset: Starting position for pagination (default: 0)
    
    Returns:
        Dictionary with requested data
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    
    endpoints = {
        "top_artists": f"https://api.spotify.com/v1/me/top/artists?time_range={time_range}&limit={limit}&offset={offset}",
        "top_tracks": f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit={limit}&offset={offset}",
        "recently_played": f"https://api.spotify.com/v1/me/player/recently_played?limit={limit}&offset={offset}",
    }
    
    if data_type not in endpoints:
        return {"success": False, "error": f"Unknown data_type: {data_type}"}
    
    try:
        response = requests.get(endpoints[data_type], headers=headers)
        response.raise_for_status()
        data = response.json()
        
        items = data.get("items", [])
        return {
            "success": True,
            "data_type": data_type,
            "count": len(items),
            "offset": offset,
            "total": data.get("total", len(items)),
            "items": items
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# TOOL 3: GenreAggregatorTool - Extract and Count Genres
# ============================================================================

@tool
def aggregate_genres(artists_data: list) -> dict:
    """Extract genres from artists and return frequency count.
    
    Args:
        artists_data: List of artist objects from Spotify API
    
    Returns:
        Dictionary with top genres and their counts
    """
    try:
        all_genres = []
        
        for artist in artists_data:
            genres = artist.get("genres", [])
            all_genres.extend(genres)
        
        if not all_genres:
            return {"success": True, "genres": [], "total_unique": 0}
        
        genre_counts = Counter(all_genres)
        top_genres = genre_counts.most_common(10)
        
        return {
            "success": True,
            "top_genres": [{"genre": g, "count": c} for g, c in top_genres],
            "total_unique": len(genre_counts),
            "total_mentions": len(all_genres)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# TOOL 4: ListeningPatternTool - Analyze Listening Patterns
# ============================================================================

@tool
def analyze_listening_patterns(top_artists: list, top_tracks: list, recently_played: list) -> dict:
    """Analyze listening patterns from user data.
    
    Args:
        top_artists: List of top artists
        top_tracks: List of top tracks
        recently_played: List of recently played tracks
    
    Returns:
        Dictionary with pattern analysis and statistics
    """
    try:
        # Most played artists
        artist_names = [a.get("name") for a in top_artists[:5]]
        
        # Track repeat behavior
        track_names = [t.get("name") for t in top_tracks]
        track_counts = Counter(track_names)
        repeat_count = sum(1 for count in track_counts.values() if count > 1)
        
        # Diversity score (0-100)
        unique_artists = len(set(a.get("id") for a in top_artists))
        total_artists = len(top_artists)
        diversity_score = (unique_artists / total_artists * 100) if total_artists > 0 else 0
        
        # Recently played analysis
        recent_artists = [t.get("artists", [{}])[0].get("name") for t in recently_played[:20]]
        recent_artist_counts = Counter(recent_artists)
        
        return {
            "success": True,
            "top_5_artists": artist_names,
            "repeat_behavior": {
                "repeated_tracks": repeat_count,
                "total_tracks": len(track_counts)
            },
            "diversity_score": round(diversity_score, 1),
            "recent_favorites": [{"artist": a, "plays": c} for a, c in recent_artist_counts.most_common(5)]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# TOOL 5: InsightGeneratorTool - Generate Human-Readable Insights
# ============================================================================

@tool
def generate_insights(patterns: dict, genres: dict, time_range: str = "medium_term") -> dict:
    """Convert statistics into human-readable insights.
    
    Args:
        patterns: Output from analyze_listening_patterns
        genres: Output from aggregate_genres
        time_range: Time range for context ('short_term', 'medium_term', 'long_term')
    
    Returns:
        Dictionary with formatted insights
    """
    try:
        insights = []
        
        # Genre insight
        if genres.get("top_genres"):
            top_genre = genres["top_genres"][0]["genre"]
            insights.append(f"Your most listened genre is {top_genre}.")
        
        # Artist insight
        if patterns.get("top_5_artists"):
            top_artist = patterns["top_5_artists"][0]
            insights.append(f"Your favorite artist is {top_artist}.")
        
        # Repeat behavior insight
        repeat_info = patterns.get("repeat_behavior", {})
        if repeat_info.get("repeated_tracks", 0) > 0:
            insights.append("You replay songs frequently.")
        else:
            insights.append("You enjoy exploring new music.")
        
        # Diversity insight
        diversity = patterns.get("diversity_score", 0)
        if diversity > 80:
            diversity_text = "very high"
        elif diversity > 60:
            diversity_text = "moderate to high"
        elif diversity > 40:
            diversity_text = "moderate"
        else:
            diversity_text = "low"
        insights.append(f"Your listening variety is {diversity_text} ({diversity}%).")
        
        # Time range context
        time_labels = {
            "short_term": "last 4 weeks",
            "medium_term": "last 6 months",
            "long_term": "all time"
        }
        time_label = time_labels.get(time_range, "recent")
        
        return {
            "success": True,
            "time_range": time_label,
            "insights": insights,
            "summary": " ".join(insights)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# TOOL 6: TimeRangeAnalyzerTool - Compare Patterns Across Time Ranges
# ============================================================================

@tool
def compare_time_ranges(short_term_artists: list, medium_term_artists: list, long_term_artists: list) -> dict:
    """Compare listening patterns across different time ranges to identify trends.
    
    Args:
        short_term_artists: Top artists from last 4 weeks
        medium_term_artists: Top artists from last 6 months
        long_term_artists: Top artists from all time
    
    Returns:
        Dictionary with trend analysis
    """
    try:
        short_names = set(a.get("name") for a in short_term_artists[:10])
        medium_names = set(a.get("name") for a in medium_term_artists[:10])
        long_names = set(a.get("name") for a in long_term_artists[:10])
        
        # New favorites (in short term but not in long term)
        new_favorites = short_names - long_names
        
        # Consistent favorites (in all time ranges)
        consistent = short_names & medium_names & long_names
        
        # Fading favorites (in long term but not in short term)
        fading = long_names - short_names
        
        trends = []
        if new_favorites:
            trends.append(f"New favorites: {', '.join(list(new_favorites)[:3])}")
        if consistent:
            trends.append(f"Consistent favorites: {', '.join(list(consistent)[:3])}")
        if fading:
            trends.append(f"Artists you used to listen to: {', '.join(list(fading)[:3])}")
        
        return {
            "success": True,
            "new_favorites": list(new_favorites),
            "consistent_favorites": list(consistent),
            "fading_favorites": list(fading),
            "trends": trends
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# TOOL 7: ArtistTopSongsTool - Get Top Songs from Specific Artist
# ============================================================================

@tool
def get_artist_top_songs(top_tracks: list, artist_name: str, limit: int = 5) -> dict:
    """Get your top favorite songs from a specific artist.
    
    Args:
        top_tracks: List of your top tracks from Spotify
        artist_name: Name of the artist to filter by
        limit: Number of top songs to return (default: 5)
    
    Returns:
        Dictionary with top songs from the artist
    """
    try:
        artist_name_lower = artist_name.lower()
        artist_tracks = []
        
        # Find all tracks by this artist
        for track in top_tracks:
            artists = track.get("artists", [])
            for artist in artists:
                if artist_name_lower in artist.get("name", "").lower():
                    artist_tracks.append(track)
                    break
        
        if not artist_tracks:
            return {
                "success": True,
                "artist": artist_name,
                "found": False,
                "message": f"No tracks found from {artist_name} in your top tracks"
            }
        
        # Get top N tracks
        top_songs = artist_tracks[:limit]
        
        songs_list = []
        for i, track in enumerate(top_songs, 1):
            songs_list.append({
                "rank": i,
                "name": track.get("name"),
                "popularity": track.get("popularity"),
                "album": track.get("album", {}).get("name")
            })
        
        return {
            "success": True,
            "artist": artist_name,
            "found": True,
            "total_tracks_by_artist": len(artist_tracks),
            "top_songs": songs_list
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# TOOL 8: FetchAllTopTracksTool - Paginate Through All Top Tracks
# ============================================================================

@tool
def fetch_all_top_tracks(access_token: str, time_range: str = "medium_term", max_results: int = 1000) -> dict:
    """Fetch all your top tracks by paginating through results.
    
    Args:
        access_token: Valid Spotify access token
        time_range: Time range ('short_term', 'medium_term', 'long_term')
        max_results: Maximum number of tracks to fetch (Spotify limit is ~1000)
    
    Returns:
        Dictionary with all fetched tracks
    """
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        all_tracks = []
        offset = 0
        limit = 50  # Max per request
        
        while len(all_tracks) < max_results:
            url = f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit={limit}&offset={offset}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            items = data.get("items", [])
            if not items:
                break
            
            all_tracks.extend(items)
            offset += limit
        
        return {
            "success": True,
            "total_fetched": len(all_tracks),
            "time_range": time_range,
            "items": all_tracks
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# AGENT SETUP
# ============================================================================

def create_spotify_agent():
    """Create and return the Spotify Listening Analyzer Agent."""
    
    system_prompt = """You are a Spotify Listening Analyzer Agent. Your role is to:
1. Analyze user's Spotify listening habits
2. Retrieve and analyze their music data
3. Generate insights about their listening behavior
4. Answer questions about their favorite artists, genres, and songs

When analyzing data:
- Use fetch_all_top_tracks to get up to 500 of their top tracks
- Use spotify_get_data to fetch top artists and tracks
- Use aggregate_genres to extract genre information
- Use analyze_listening_patterns to find patterns
- Use generate_insights to create readable summaries
- Use compare_time_ranges to identify trends over time
- Use get_artist_top_songs to find their favorite songs from specific artists

Always provide clear, friendly insights with JSON data and readable explanations."""
    
    agent = Agent(
        tools=[
            spotify_get_data,
            aggregate_genres,
            analyze_listening_patterns,
            generate_insights,
            compare_time_ranges,
            get_artist_top_songs,
            fetch_all_top_tracks,
        ],
        system_prompt=system_prompt,
    )
    
    return agent


if __name__ == "__main__":
    # Example usage
    agent = create_spotify_agent()
    
    # Test query
    response = agent("What are my top genres and listening patterns?")
    print(response)
