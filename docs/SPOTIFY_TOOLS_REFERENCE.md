# Spotify Analyzer Agent - Tools Reference

Complete documentation for all 6 tools in the Spotify Listening Analyzer Agent.

## Tool 1: SpotifyAuthTool

**Purpose:** Authenticate with Spotify OAuth2 and retrieve access tokens.

**Function:** `spotify_auth()`

**Parameters:**
- `client_id` (str, required): Your Spotify app Client ID
- `client_secret` (str, required): Your Spotify app Client Secret
- `redirect_uri` (str, optional): OAuth redirect URI (default: `http://localhost:8888/callback`)

**Returns:**
```json
{
  "success": true,
  "access_token": "BQDu3...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**Example:**
```python
result = spotify_auth(
    client_id="your_client_id",
    client_secret="your_client_secret"
)
access_token = result["access_token"]
```

**Error Response:**
```json
{
  "success": false,
  "error": "Invalid client credentials"
}
```

---

## Tool 2: SpotifyDataTool

**Purpose:** Fetch data from Spotify Web API (top artists, top tracks, recently played).

**Function:** `spotify_get_data()`

**Parameters:**
- `access_token` (str, required): Valid Spotify access token
- `data_type` (str, required): Type of data to fetch
  - `"top_artists"` - Your most-played artists
  - `"top_tracks"` - Your most-played tracks
  - `"recently_played"` - Recently played tracks
- `time_range` (str, optional): Time range for top items
  - `"short_term"` - Last 4 weeks (default for recent activity)
  - `"medium_term"` - Last 6 months (default)
  - `"long_term"` - All-time
- `limit` (int, optional): Number of items to fetch (1-50, default: 20)

**Returns:**
```json
{
  "success": true,
  "data_type": "top_artists",
  "count": 20,
  "items": [
    {
      "id": "artist_id",
      "name": "Artist Name",
      "genres": ["hip-hop", "rap"],
      "popularity": 85,
      "followers": {"total": 1000000}
    }
  ]
}
```

**Example:**
```python
# Get top artists from last 6 months
result = spotify_get_data(
    access_token="BQDu3...",
    data_type="top_artists",
    time_range="medium_term",
    limit=20
)

# Get recently played tracks
result = spotify_get_data(
    access_token="BQDu3...",
    data_type="recently_played",
    limit=50
)
```

**Error Response:**
```json
{
  "success": false,
  "error": "Invalid access token"
}
```

---

## Tool 3: GenreAggregatorTool

**Purpose:** Extract genres from artist data and count frequency.

**Function:** `aggregate_genres()`

**Parameters:**
- `artists_data` (list, required): List of artist objects from Spotify API

**Returns:**
```json
{
  "success": true,
  "top_genres": [
    {"genre": "hip-hop", "count": 45},
    {"genre": "rap", "count": 38},
    {"genre": "r-n-b", "count": 32},
    {"genre": "trap", "count": 28}
  ],
  "total_unique": 24,
  "total_mentions": 143
}
```

**Example:**
```python
# First get artists
artists_result = spotify_get_data(
    access_token="BQDu3...",
    data_type="top_artists",
    limit=50
)

# Then aggregate genres
genres_result = aggregate_genres(artists_result["items"])
print(genres_result["top_genres"])
```

**Explanation:**
- `top_genres`: Top 10 genres with occurrence counts
- `total_unique`: Number of unique genres found
- `total_mentions`: Total genre mentions across all artists

---

## Tool 4: ListeningPatternTool

**Purpose:** Analyze listening patterns and generate statistics.

**Function:** `analyze_listening_patterns()`

**Parameters:**
- `top_artists` (list, required): List of top artists
- `top_tracks` (list, required): List of top tracks
- `recently_played` (list, required): List of recently played tracks

**Returns:**
```json
{
  "success": true,
  "top_5_artists": [
    "Artist 1",
    "Artist 2",
    "Artist 3",
    "Artist 4",
    "Artist 5"
  ],
  "repeat_behavior": {
    "repeated_tracks": 8,
    "total_tracks": 50
  },
  "diversity_score": 65.5,
  "recent_favorites": [
    {"artist": "Artist A", "plays": 12},
    {"artist": "Artist B", "plays": 9},
    {"artist": "Artist C", "plays": 7}
  ]
}
```

**Example:**
```python
# Get all data
artists = spotify_get_data(access_token, "top_artists", limit=50)["items"]
tracks = spotify_get_data(access_token, "top_tracks", limit=50)["items"]
recent = spotify_get_data(access_token, "recently_played", limit=50)["items"]

# Analyze patterns
patterns = analyze_listening_patterns(artists, tracks, recent)
print(f"Diversity Score: {patterns['diversity_score']}%")
```

**Metrics Explained:**
- `top_5_artists`: Your 5 most-played artists
- `repeat_behavior`: How often you replay tracks
- `diversity_score`: 0-100% (higher = more variety)
- `recent_favorites`: Artists you've been listening to recently

---

## Tool 5: InsightGeneratorTool

**Purpose:** Convert statistics into human-readable insights.

**Function:** `generate_insights()`

**Parameters:**
- `patterns` (dict, required): Output from `analyze_listening_patterns()`
- `genres` (dict, required): Output from `aggregate_genres()`
- `time_range` (str, optional): Time range context
  - `"short_term"` - Last 4 weeks
  - `"medium_term"` - Last 6 months (default)
  - `"long_term"` - All-time

**Returns:**
```json
{
  "success": true,
  "time_range": "last 6 months",
  "insights": [
    "Your most listened genre is hip-hop.",
    "Your favorite artist is Drake.",
    "You replay songs frequently.",
    "Your listening variety is moderate (65%)."
  ],
  "summary": "Your most listened genre is hip-hop. Your favorite artist is Drake. You replay songs frequently. Your listening variety is moderate (65%)."
}
```

**Example:**
```python
# Generate insights
insights = generate_insights(
    patterns=patterns_result,
    genres=genres_result,
    time_range="medium_term"
)

print(insights["summary"])
# Output: "Your most listened genre is hip-hop. Your favorite artist is Drake..."
```

**Insight Types:**
1. **Genre Insight**: "Your most listened genre is [genre]."
2. **Artist Insight**: "Your favorite artist is [artist]."
3. **Repeat Insight**: "You replay songs frequently." or "You enjoy exploring new music."
4. **Diversity Insight**: "Your listening variety is [very high/moderate/low] ([score]%)."

---

## Tool 6: TimeRangeAnalyzerTool

**Purpose:** Compare listening patterns across time ranges to identify trends.

**Function:** `compare_time_ranges()`

**Parameters:**
- `short_term_artists` (list, required): Top artists from last 4 weeks
- `medium_term_artists` (list, required): Top artists from last 6 months
- `long_term_artists` (list, required): Top artists from all-time

**Returns:**
```json
{
  "success": true,
  "new_favorites": [
    "New Artist 1",
    "New Artist 2"
  ],
  "consistent_favorites": [
    "Consistent Artist 1",
    "Consistent Artist 2"
  ],
  "fading_favorites": [
    "Old Artist 1",
    "Old Artist 2"
  ],
  "trends": [
    "New favorites: New Artist 1, New Artist 2",
    "Consistent favorites: Consistent Artist 1, Consistent Artist 2",
    "Artists you used to listen to: Old Artist 1, Old Artist 2"
  ]
}
```

**Example:**
```python
# Get artists for each time range
short = spotify_get_data(access_token, "top_artists", "short_term", 10)["items"]
medium = spotify_get_data(access_token, "top_artists", "medium_term", 10)["items"]
long = spotify_get_data(access_token, "top_artists", "long_term", 10)["items"]

# Compare trends
trends = compare_time_ranges(short, medium, long)
print(trends["trends"])
```

**Trend Categories:**
- **New Favorites**: Artists in short-term but not in long-term (recent discoveries)
- **Consistent Favorites**: Artists in all time ranges (always in top)
- **Fading Favorites**: Artists in long-term but not in short-term (used to listen to)

---

## Tool Usage Workflow

### Typical Agent Flow

```
User Query
    ↓
Agent decides which tools to call
    ↓
1. spotify_get_data() - Fetch raw data
    ↓
2. aggregate_genres() - Extract genres
    ↓
3. analyze_listening_patterns() - Analyze patterns
    ↓
4. generate_insights() - Create readable text
    ↓
5. compare_time_ranges() - Identify trends (optional)
    ↓
Response with JSON + readable explanation
```

### Example: "What are my top genres?"

```python
# Step 1: Get top artists
artists = spotify_get_data(token, "top_artists", limit=50)

# Step 2: Extract genres
genres = aggregate_genres(artists["items"])

# Step 3: Generate insights
insights = generate_insights(
    patterns={"top_5_artists": [...]},
    genres=genres
)

# Response
print(insights["summary"])
```

---

## Error Handling

All tools return a `success` field:

```python
result = spotify_get_data(...)

if result["success"]:
    # Process data
    data = result["items"]
else:
    # Handle error
    error = result["error"]
    print(f"Error: {error}")
```

---

## Rate Limits

- Spotify API: 180 requests per minute
- Agent handles rate limiting automatically
- No caching implemented (each query fetches fresh data)

---

## Data Structures

### Artist Object
```json
{
  "id": "artist_id",
  "name": "Artist Name",
  "genres": ["genre1", "genre2"],
  "popularity": 85,
  "followers": {"total": 1000000},
  "images": [{"url": "image_url"}]
}
```

### Track Object
```json
{
  "id": "track_id",
  "name": "Track Name",
  "artists": [{"name": "Artist Name"}],
  "popularity": 75,
  "duration_ms": 240000
}
```

---

## Best Practices

1. **Always check `success` field** before accessing data
2. **Use appropriate time ranges** for different queries
3. **Combine tools** for richer insights
4. **Cache results** if making multiple queries
5. **Handle errors gracefully** with user-friendly messages

---

## See Also

- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)
- [Spotify Analyzer README](SPOTIFY_ANALYZER_README.md)
- [Quick Start Guide](SPOTIFY_QUICK_START.md)
