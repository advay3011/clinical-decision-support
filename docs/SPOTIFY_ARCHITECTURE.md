# Spotify Listening Analyzer Agent - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (CLI / Chat Interface)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    User Query / Question
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STRANDS AGENT CORE                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Agent Loop:                                             │  │
│  │  1. Parse user query                                     │  │
│  │  2. Decide which tools to call                           │  │
│  │  3. Execute tools                                        │  │
│  │  4. Combine results                                      │  │
│  │  5. Generate response                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    Tool Selection & Execution
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   ┌─────────┐          ┌─────────┐         ┌──────────┐
   │ Tool 1  │          │ Tool 2  │         │ Tool 3   │
   │ Auth    │          │ Data    │         │ Genres   │
   └────┬────┘          └────┬────┘         └────┬─────┘
        │                    │                    │
        │                    ▼                    │
        │            ┌──────────────┐             │
        │            │ Spotify API  │             │
        │            │ Endpoints    │             │
        │            └──────────────┘             │
        │                    │                    │
        │                    ▼                    │
        │            ┌──────────────┐             │
        │            │ Raw Data:    │             │
        │            │ - Artists    │             │
        │            │ - Tracks     │             │
        │            │ - Genres     │             │
        │            └──────────────┘             │
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   ┌─────────┐          ┌─────────┐         ┌──────────┐
   │ Tool 4  │          │ Tool 5  │         │ Tool 6   │
   │Patterns │          │Insights │         │ Trends   │
   └────┬────┘          └────┬────┘         └────┬─────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    Analysis & Processing
                             │
                             ▼
        ┌────────────────────────────────────┐
        │  Structured Output:                │
        │  - JSON data                       │
        │  - Readable insights               │
        │  - Trend analysis                  │
        └────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FORMATTED RESPONSE                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ {                                                        │  │
│  │   "status": "success",                                   │  │
│  │   "data": {                                              │  │
│  │     "top_genres": [...],                                 │  │
│  │     "insights": [...],                                   │  │
│  │     "summary": "..."                                     │  │
│  │   }                                                      │  │
│  │ }                                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
                    Display to User
```

---

## Tool Dependency Graph

```
User Query
    │
    ├─→ SpotifyAuthTool
    │       │
    │       └─→ Access Token
    │
    ├─→ SpotifyDataTool (uses token)
    │       │
    │       ├─→ Top Artists
    │       ├─→ Top Tracks
    │       └─→ Recently Played
    │
    ├─→ GenreAggregatorTool (uses artists)
    │       │
    │       └─→ Genre Frequencies
    │
    ├─→ ListeningPatternTool (uses all data)
    │       │
    │       └─→ Pattern Statistics
    │
    ├─→ InsightGeneratorTool (uses patterns + genres)
    │       │
    │       └─→ Readable Insights
    │
    └─→ TimeRangeAnalyzerTool (uses artists from 3 ranges)
            │
            └─→ Trend Analysis
```

---

## Data Flow Example: "What are my top genres?"

```
User: "What are my top genres?"
    │
    ▼
Agent analyzes query
    │
    ├─ Needs: Top artists data
    ├─ Needs: Genre extraction
    └─ Needs: Readable insights
    │
    ▼
Call SpotifyAuthTool
    │
    ├─ Input: client_id, client_secret
    └─ Output: access_token
    │
    ▼
Call SpotifyDataTool
    │
    ├─ Input: access_token, data_type="top_artists"
    └─ Output: [Artist1, Artist2, Artist3, ...]
    │
    ▼
Call GenreAggregatorTool
    │
    ├─ Input: [Artist1, Artist2, Artist3, ...]
    └─ Output: [
        {"genre": "hip-hop", "count": 45},
        {"genre": "rap", "count": 38},
        ...
      ]
    │
    ▼
Call InsightGeneratorTool
    │
    ├─ Input: genres data
    └─ Output: "Your most listened genre is hip-hop (45 mentions)..."
    │
    ▼
Format Response
    │
    └─ Return JSON + readable text
```

---

## Tool Interaction Matrix

| Tool | Depends On | Used By | Spotify API Calls |
|------|-----------|---------|------------------|
| SpotifyAuthTool | None | All others | 1 (token endpoint) |
| SpotifyDataTool | SpotifyAuthTool | GenreAgg, Patterns, TimeRange | 1-3 (per data type) |
| GenreAggregatorTool | SpotifyDataTool | InsightGenerator | 0 (local processing) |
| ListeningPatternTool | SpotifyDataTool | InsightGenerator | 0 (local processing) |
| InsightGeneratorTool | GenreAgg, Patterns | User | 0 (local processing) |
| TimeRangeAnalyzerTool | SpotifyDataTool | User | 0 (local processing) |

---

## Data Structures

### Artist Object (from Spotify API)
```
Artist
├── id: string
├── name: string
├── genres: [string]
├── popularity: number (0-100)
├── followers: {total: number}
└── images: [{url: string}]
```

### Track Object (from Spotify API)
```
Track
├── id: string
├── name: string
├── artists: [Artist]
├── popularity: number (0-100)
├── duration_ms: number
└── album: {name: string}
```

### Genre Analysis (from GenreAggregatorTool)
```
GenreAnalysis
├── top_genres: [
│   ├── genre: string
│   └── count: number
│ ]
├── total_unique: number
└── total_mentions: number
```

### Pattern Analysis (from ListeningPatternTool)
```
PatternAnalysis
├── top_5_artists: [string]
├── repeat_behavior: {
│   ├── repeated_tracks: number
│   └── total_tracks: number
│ }
├── diversity_score: number (0-100)
└── recent_favorites: [
    ├── artist: string
    └── plays: number
  ]
```

### Insights (from InsightGeneratorTool)
```
Insights
├── time_range: string
├── insights: [string]
└── summary: string
```

### Trends (from TimeRangeAnalyzerTool)
```
Trends
├── new_favorites: [string]
├── consistent_favorites: [string]
├── fading_favorites: [string]
└── trends: [string]
```

---

## Agent Decision Tree

```
User Query
    │
    ├─ Contains "genre"?
    │   └─→ Call SpotifyDataTool + GenreAggregatorTool
    │
    ├─ Contains "artist"?
    │   └─→ Call SpotifyDataTool + ListeningPatternTool
    │
    ├─ Contains "repeat" or "replay"?
    │   └─→ Call SpotifyDataTool + ListeningPatternTool
    │
    ├─ Contains "pattern" or "habit"?
    │   └─→ Call SpotifyDataTool + ListeningPatternTool
    │
    ├─ Contains "change" or "trend" or "time"?
    │   └─→ Call SpotifyDataTool (3 ranges) + TimeRangeAnalyzerTool
    │
    ├─ Contains "diversity" or "variety"?
    │   └─→ Call SpotifyDataTool + ListeningPatternTool
    │
    └─ Default: Call all relevant tools for comprehensive analysis
```

---

## Error Handling Flow

```
Tool Call
    │
    ├─ Success?
    │   └─→ Return data
    │
    └─ Failure?
        │
        ├─ Authentication error?
        │   └─→ "Please re-authenticate with Spotify"
        │
        ├─ API error?
        │   └─→ "Unable to fetch data from Spotify"
        │
        ├─ Rate limit?
        │   └─→ "Too many requests, please try again later"
        │
        └─ Other error?
            └─→ "An error occurred: [error message]"
```

---

## Performance Characteristics

| Operation | Time | API Calls | Notes |
|-----------|------|-----------|-------|
| Authenticate | ~500ms | 1 | One-time per session |
| Fetch top artists | ~200ms | 1 | Cached for session |
| Fetch top tracks | ~200ms | 1 | Cached for session |
| Fetch recently played | ~200ms | 1 | Cached for session |
| Aggregate genres | ~50ms | 0 | Local processing |
| Analyze patterns | ~50ms | 0 | Local processing |
| Generate insights | ~100ms | 0 | Local processing |
| Compare time ranges | ~100ms | 0 | Local processing |
| **Total (full analysis)** | **~1.5s** | **3-4** | Depends on query |

---

## Scalability Considerations

### Current Design
- Single-threaded execution
- Sequential tool calls
- No caching between queries
- No database storage

### For Production
- Add result caching (Redis/Memcached)
- Implement async tool execution
- Add database for user profiles
- Implement rate limiting per user
- Add monitoring and logging
- Use connection pooling for API calls

---

## Security Considerations

✓ **Token Management**
- Access tokens stored in memory only
- No hardcoded credentials
- Environment variables for secrets

✓ **API Security**
- HTTPS for all Spotify API calls
- OAuth2 authentication
- No sensitive data in logs

✓ **Input Validation**
- Validate all user inputs
- Sanitize API responses
- Error handling for malformed data

---

## See Also

- [Tool Reference](SPOTIFY_TOOLS_REFERENCE.md)
- [README](SPOTIFY_ANALYZER_README.md)
- [Quick Start](SPOTIFY_QUICK_START.md)
