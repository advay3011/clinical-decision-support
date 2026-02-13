# Spotify Analyzer Agent - Quick Start

Get up and running in 5 minutes.

## 1. Install

```bash
pip install strands-agents strands-agents-tools requests
```

## 2. Get Spotify Credentials

1. Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create an app
3. Copy **Client ID** and **Client Secret**

## 3. Set Environment Variables

```bash
export SPOTIFY_CLIENT_ID='your_id'
export SPOTIFY_CLIENT_SECRET='your_secret'
export AWS_BEDROCK_API_KEY='your_bedrock_key'  # or use Anthropic/OpenAI
```

## 4. Run the Demo

```bash
python agents/spotify_demo.py
```

## 5. Ask Questions

```
You: What are my top genres?
Agent: Your most listened genre is hip-hop...

You: Who are my favorite artists?
Agent: Your favorite artist is [Artist Name]...

You: Do I repeat songs often?
Agent: You replay songs frequently...
```

## Example Code

```python
from agents.spotify_analyzer_agent import create_spotify_agent

agent = create_spotify_agent()

# Single query
response = agent("What are my listening patterns?")
print(response)

# Multi-turn conversation
agent("My name is Alex")
response = agent("What are my top 3 genres?")
print(response)
```

## Tools Available

| Tool | Purpose |
|------|---------|
| `spotify_auth` | Authenticate with Spotify |
| `spotify_get_data` | Fetch top artists, tracks, recently played |
| `aggregate_genres` | Extract and count genres |
| `analyze_listening_patterns` | Analyze repeat behavior, diversity |
| `generate_insights` | Convert stats to readable text |
| `compare_time_ranges` | Identify trends over time |

## Common Queries

- "What genre do I listen to most?"
- "Who are my top artists?"
- "Do I repeat songs often?"
- "What are my listening patterns?"
- "How have my tastes changed?"
- "What's my music diversity score?"
- "Who are my recent favorites?"

## Troubleshooting

**Error: "Credentials not found"**
- Set environment variables: `export SPOTIFY_CLIENT_ID='...'`

**Error: "Access denied"**
- Verify credentials in Spotify Developer Dashboard
- Check app permissions

**Error: "No data"**
- Ensure you have Spotify listening history
- Try different time range (short_term requires recent activity)

## Next Steps

- Integrate into your app
- Add custom tools
- Deploy to production
- Add more analysis features

See `SPOTIFY_ANALYZER_README.md` for full documentation.
