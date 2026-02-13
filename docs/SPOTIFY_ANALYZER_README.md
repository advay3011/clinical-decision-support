# Spotify Listening Analyzer Agent

A Strands-based agent that analyzes your Spotify listening habits and generates descriptive insights about your music preferences.

## Overview

This agent connects to the Spotify Web API to retrieve your listening data and provides human-readable insights about:
- Your top genres and artists
- Listening patterns and repeat behavior
- Music diversity score
- Trends over time (short-term vs long-term)

**Note:** This is a descriptive analytics tool only—no predictions or simulations.

## Architecture

### 6 Core Tools

#### 1. **SpotifyAuthTool**
- Handles OAuth2 authentication with Spotify
- Retrieves and manages access tokens
- Returns: `access_token`, `token_type`, `expires_in`

#### 2. **SpotifyDataTool**
- Fetches data from Spotify Web API
- Supports:
  - `top_artists` - Your most-played artists
  - `top_tracks` - Your most-played tracks
  - `recently_played` - Recently played tracks
- Configurable time ranges: `short_term` (4 weeks), `medium_term` (6 months), `long_term` (all-time)

#### 3. **GenreAggregatorTool**
- Extracts genres from artist data
- Counts genre frequency
- Returns top 10 genres with occurrence counts

#### 4. **ListeningPatternTool**
- Analyzes listening behavior
- Calculates:
  - Top 5 artists
  - Repeat behavior (how often you replay tracks)
  - Diversity score (0-100%)
  - Recent favorites

#### 5. **InsightGeneratorTool**
- Converts raw statistics into human-readable insights
- Generates contextual descriptions
- Example outputs:
  - "Your most listened genre is hip-hop."
  - "You replay songs frequently."
  - "Your listening variety is moderate (65%)."

#### 6. **TimeRangeAnalyzerTool**
- Compares patterns across time ranges
- Identifies trends:
  - New favorites (recent additions)
  - Consistent favorites (always in top)
  - Fading favorites (used to listen to)

## Setup

### 1. Install Dependencies

```bash
pip install strands-agents strands-agents-tools requests
```

### 2. Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in or create an account
3. Create a new app
4. Accept the terms and create the app
5. Copy your **Client ID** and **Client Secret**

### 3. Set Environment Variables

```bash
export SPOTIFY_CLIENT_ID='your_client_id_here'
export SPOTIFY_CLIENT_SECRET='your_client_secret_here'
```

### 4. Configure LLM Provider

The agent uses Bedrock by default. Choose your provider:

**Bedrock (Default):**
```bash
export AWS_BEDROCK_API_KEY='your_bedrock_api_key'
```

**Anthropic:**
```bash
pip install 'strands-agents[anthropic]'
export ANTHROPIC_API_KEY='your_anthropic_key'
```

**OpenAI:**
```bash
pip install 'strands-agents[openai]'
export OPENAI_API_KEY='your_openai_key'
```

## Usage

### Basic Usage

```python
from agents.spotify_analyzer_agent import create_spotify_agent

# Create agent
agent = create_spotify_agent()

# Ask a question
response = agent("What are my top genres?")
print(response)
```

### Example Queries

```python
agent = create_spotify_agent()

# Query 1: Top genres
response = agent("What genre do I listen to most?")

# Query 2: Top artists
response = agent("Who are my top artists?")

# Query 3: Repeat behavior
response = agent("Do I repeat songs often?")

# Query 4: Listening patterns
response = agent("What are my listening patterns?")

# Query 5: Trends
response = agent("How have my tastes changed over time?")
```

### Running the Demo

```bash
python agents/spotify_demo.py
```

This launches an interactive session where you can ask questions about your listening habits.

## Response Format

The agent returns responses in this format:

```json
{
  "status": "success",
  "data": {
    "top_genres": [
      {"genre": "hip-hop", "count": 45},
      {"genre": "rap", "count": 38}
    ],
    "insights": [
      "Your most listened genre is hip-hop.",
      "Your favorite artist is [Artist Name].",
      "You replay songs frequently.",
      "Your listening variety is moderate (65%)."
    ],
    "summary": "Your most listened genre is hip-hop. Your favorite artist is [Artist Name]. You replay songs frequently. Your listening variety is moderate (65%)."
  }
}
```

## Agent Behavior

1. **User asks a question** about their music habits
2. **Agent decides which tools to call** based on the query
3. **Tools fetch and analyze data** from Spotify API
4. **Agent combines results** into a coherent response
5. **Returns formatted insights** with JSON data + readable explanation

## Example Workflow

```
User: "What are my top genres?"
  ↓
Agent: Calls spotify_get_data(data_type='top_artists')
  ↓
Agent: Calls aggregate_genres(artists_data)
  ↓
Agent: Calls generate_insights(patterns, genres)
  ↓
Response: "Your most listened genre is hip-hop (45 mentions). 
           You also enjoy rap (38 mentions) and R&B (32 mentions)."
```

## Supported Time Ranges

- `short_term` - Last 4 weeks
- `medium_term` - Last 6 months (default)
- `long_term` - All-time

## Limitations

- **Descriptive only** - No predictions or forecasting
- **No ML models** - Uses simple statistics and counting
- **No vector databases** - No RAG or semantic search
- **Spotify API limits** - Rate limited by Spotify (180 requests per minute)
- **Authentication** - Requires valid Spotify credentials

## Troubleshooting

### "Access denied" error
- Verify Spotify credentials are correct
- Check environment variables are set
- Ensure app is created in Spotify Developer Dashboard

### "Token expired" error
- Spotify access tokens expire after 1 hour
- Agent automatically handles token refresh
- If issue persists, re-authenticate

### "No data returned"
- Ensure you have listening history on Spotify
- Check time range (short_term requires recent activity)
- Verify API credentials have correct permissions

## File Structure

```
agents/
├── spotify_analyzer_agent.py    # Main agent with all 6 tools
└── spotify_demo.py              # Interactive demo script

docs/
└── SPOTIFY_ANALYZER_README.md   # This file
```

## Next Steps

1. Set up Spotify API credentials
2. Configure your LLM provider
3. Run the demo: `python agents/spotify_demo.py`
4. Ask questions about your listening habits
5. Integrate into your own applications

## API Reference

### Tool: spotify_auth
```python
spotify_auth(
    client_id: str,
    client_secret: str,
    redirect_uri: str = "http://localhost:8888/callback"
) -> dict
```

### Tool: spotify_get_data
```python
spotify_get_data(
    access_token: str,
    data_type: str,  # 'top_artists', 'top_tracks', 'recently_played'
    time_range: str = "medium_term",  # 'short_term', 'medium_term', 'long_term'
    limit: int = 20
) -> dict
```

### Tool: aggregate_genres
```python
aggregate_genres(artists_data: list) -> dict
```

### Tool: analyze_listening_patterns
```python
analyze_listening_patterns(
    top_artists: list,
    top_tracks: list,
    recently_played: list
) -> dict
```

### Tool: generate_insights
```python
generate_insights(
    patterns: dict,
    genres: dict,
    time_range: str = "medium_term"
) -> dict
```

### Tool: compare_time_ranges
```python
compare_time_ranges(
    short_term_artists: list,
    medium_term_artists: list,
    long_term_artists: list
) -> dict
```

## License

MIT
