# Spotify Listening Analyzer Agent - Documentation Index

Complete documentation for the Spotify Listening Analyzer Agent built with Strands framework.

## 📚 Documentation Files

### Getting Started
- **[SPOTIFY_QUICK_START.md](SPOTIFY_QUICK_START.md)** - 5-minute setup guide
  - Installation
  - Credentials setup
  - Running the demo
  - Common queries

### Main Documentation
- **[SPOTIFY_ANALYZER_README.md](SPOTIFY_ANALYZER_README.md)** - Complete guide
  - Overview and architecture
  - Setup instructions
  - Usage examples
  - Response format
  - Troubleshooting

### Technical Reference
- **[SPOTIFY_TOOLS_REFERENCE.md](SPOTIFY_TOOLS_REFERENCE.md)** - Detailed tool documentation
  - All 6 tools with parameters
  - Return values and examples
  - Error handling
  - Data structures
  - Best practices

### Architecture & Design
- **[SPOTIFY_ARCHITECTURE.md](SPOTIFY_ARCHITECTURE.md)** - System design
  - System architecture diagram
  - Tool dependency graph
  - Data flow examples
  - Tool interaction matrix
  - Performance characteristics

### Project Summary
- **[SPOTIFY_BUILD_SUMMARY.md](SPOTIFY_BUILD_SUMMARY.md)** - Build overview
  - What was built
  - Key features
  - Quick start
  - File structure
  - Next steps

---

## 🚀 Quick Navigation

### I want to...

**Get started quickly**
→ Read [SPOTIFY_QUICK_START.md](SPOTIFY_QUICK_START.md)

**Understand the full system**
→ Read [SPOTIFY_ANALYZER_README.md](SPOTIFY_ANALYZER_README.md)

**Learn about specific tools**
→ Read [SPOTIFY_TOOLS_REFERENCE.md](SPOTIFY_TOOLS_REFERENCE.md)

**Understand the architecture**
→ Read [SPOTIFY_ARCHITECTURE.md](SPOTIFY_ARCHITECTURE.md)

**See what was built**
→ Read [SPOTIFY_BUILD_SUMMARY.md](SPOTIFY_BUILD_SUMMARY.md)

---

## 📁 File Structure

```
agents/
├── spotify_analyzer_agent.py    # Main agent with 6 tools
└── spotify_demo.py              # Interactive demo

docs/
├── SPOTIFY_INDEX.md             # This file
├── SPOTIFY_QUICK_START.md       # 5-minute setup
├── SPOTIFY_ANALYZER_README.md   # Full documentation
├── SPOTIFY_TOOLS_REFERENCE.md   # Tool documentation
├── SPOTIFY_ARCHITECTURE.md      # System design
└── SPOTIFY_BUILD_SUMMARY.md     # Build overview

spotify_requirements.txt          # Dependencies
```

---

## 🛠️ The 6 Tools

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| **SpotifyAuthTool** | OAuth2 authentication | Client ID, Secret | Access token |
| **SpotifyDataTool** | Fetch Spotify data | Token, data type | Artists, tracks, genres |
| **GenreAggregatorTool** | Extract genres | Artist list | Genre frequencies |
| **ListeningPatternTool** | Analyze patterns | All data | Statistics, diversity |
| **InsightGeneratorTool** | Create insights | Patterns, genres | Readable text |
| **TimeRangeAnalyzerTool** | Compare trends | Artists (3 ranges) | Trend analysis |

---

## 💡 Example Queries

The agent can answer:
- "What genre do I listen to most?"
- "Who are my top artists?"
- "Do I repeat songs often?"
- "What are my listening patterns?"
- "How have my tastes changed over time?"
- "What's my music diversity score?"
- "Who are my recent favorites?"

---

## 🔧 Setup Steps

1. **Install dependencies**
   ```bash
   pip install -r spotify_requirements.txt
   ```

2. **Get Spotify credentials**
   - Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create an app
   - Copy Client ID and Client Secret

3. **Set environment variables**
   ```bash
   export SPOTIFY_CLIENT_ID='your_id'
   export SPOTIFY_CLIENT_SECRET='your_secret'
   export AWS_BEDROCK_API_KEY='your_bedrock_key'
   ```

4. **Run the demo**
   ```bash
   python agents/spotify_demo.py
   ```

---

## 📖 Documentation by Topic

### Authentication & Setup
- [SPOTIFY_QUICK_START.md](SPOTIFY_QUICK_START.md) - Setup guide
- [SPOTIFY_ANALYZER_README.md](SPOTIFY_ANALYZER_README.md#setup) - Detailed setup
- [SPOTIFY_TOOLS_REFERENCE.md](SPOTIFY_TOOLS_REFERENCE.md#tool-1-spotifyauthtool) - Auth tool docs

### Using the Agent
- [SPOTIFY_QUICK_START.md](SPOTIFY_QUICK_START.md#5-ask-questions) - Example queries
- [SPOTIFY_ANALYZER_README.md](SPOTIFY_ANALYZER_README.md#usage) - Usage guide
- [SPOTIFY_ANALYZER_README.md](SPOTIFY_ANALYZER_README.md#example-queries) - Query examples

### Understanding Tools
- [SPOTIFY_TOOLS_REFERENCE.md](SPOTIFY_TOOLS_REFERENCE.md) - Complete tool reference
- [SPOTIFY_ARCHITECTURE.md](SPOTIFY_ARCHITECTURE.md#tool-dependency-graph) - Tool dependencies
- [SPOTIFY_ARCHITECTURE.md](SPOTIFY_ARCHITECTURE.md#tool-interaction-matrix) - Tool interactions

### System Design
- [SPOTIFY_ARCHITECTURE.md](SPOTIFY_ARCHITECTURE.md) - Full architecture
- [SPOTIFY_ANALYZER_README.md](SPOTIFY_ANALYZER_README.md#architecture) - Architecture overview
- [SPOTIFY_BUILD_SUMMARY.md](SPOTIFY_BUILD_SUMMARY.md#architecture-overview) - Build summary

### Troubleshooting
- [SPOTIFY_QUICK_START.md](SPOTIFY_QUICK_START.md#troubleshooting) - Quick troubleshooting
- [SPOTIFY_ANALYZER_README.md](SPOTIFY_ANALYZER_README.md#troubleshooting) - Detailed troubleshooting
- [SPOTIFY_TOOLS_REFERENCE.md](SPOTIFY_TOOLS_REFERENCE.md#error-handling) - Error handling

---

## 🎯 Key Features

✓ **6 Specialized Tools** - Each handles a specific task
✓ **Descriptive Analytics** - No ML or predictions
✓ **Modular Design** - Tools are independent
✓ **Beginner-Friendly** - Clear code and documentation
✓ **Multi-Turn Conversations** - Agent maintains context
✓ **Flexible LLM Support** - Works with multiple providers
✓ **Error Handling** - Graceful failures
✓ **Time Range Analysis** - Compare patterns over time

---

## 📊 Response Format

All agent responses include:
- **JSON data** - Structured analysis results
- **Readable insights** - Human-friendly descriptions
- **Summary** - Quick overview of findings

Example:
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
      "Your favorite artist is Drake.",
      "You replay songs frequently.",
      "Your listening variety is moderate (65%)."
    ],
    "summary": "Your most listened genre is hip-hop..."
  }
}
```

---

## 🔗 External Resources

- **Spotify Web API** - https://developer.spotify.com/documentation/web-api
- **Spotify Developer Dashboard** - https://developer.spotify.com/dashboard
- **Strands Framework** - See Kiro IDE documentation
- **Python Requests** - https://requests.readthedocs.io/

---

## 📝 Code Files

### Main Agent
**File:** `agents/spotify_analyzer_agent.py`
- 6 tool implementations
- Agent creation function
- ~350 lines of clean, modular code

### Demo Application
**File:** `agents/spotify_demo.py`
- Interactive CLI
- Multi-turn conversation support
- Example usage

### Dependencies
**File:** `spotify_requirements.txt`
- All required packages
- Optional provider extensions

---

## 🚀 Next Steps

1. **Read** [SPOTIFY_QUICK_START.md](SPOTIFY_QUICK_START.md) for 5-minute setup
2. **Run** `python agents/spotify_demo.py` to test the agent
3. **Explore** [SPOTIFY_TOOLS_REFERENCE.md](SPOTIFY_TOOLS_REFERENCE.md) for tool details
4. **Integrate** into your own applications
5. **Extend** with custom tools and features

---

## ❓ FAQ

**Q: Do I need Spotify Premium?**
A: No, the agent works with any Spotify account.

**Q: What LLM providers are supported?**
A: Bedrock (default), Anthropic, OpenAI, Google Gemini, Meta Llama.

**Q: Can I use this without Spotify credentials?**
A: No, you need valid Spotify API credentials to fetch data.

**Q: Is this a predictive system?**
A: No, it's purely descriptive analytics. No ML or predictions.

**Q: Can I add more tools?**
A: Yes, the design is modular and extensible.

**Q: How often can I query the agent?**
A: Limited by Spotify API rate limits (180 requests/minute).

---

## 📞 Support

- **Setup Issues** → See [SPOTIFY_QUICK_START.md](SPOTIFY_QUICK_START.md#troubleshooting)
- **Tool Questions** → See [SPOTIFY_TOOLS_REFERENCE.md](SPOTIFY_TOOLS_REFERENCE.md)
- **Architecture Questions** → See [SPOTIFY_ARCHITECTURE.md](SPOTIFY_ARCHITECTURE.md)
- **General Questions** → See [SPOTIFY_ANALYZER_README.md](SPOTIFY_ANALYZER_README.md)

---

## 📄 Document Versions

- **SPOTIFY_INDEX.md** - Documentation index (this file)
- **SPOTIFY_QUICK_START.md** - Quick setup guide
- **SPOTIFY_ANALYZER_README.md** - Complete documentation
- **SPOTIFY_TOOLS_REFERENCE.md** - Tool reference
- **SPOTIFY_ARCHITECTURE.md** - System architecture
- **SPOTIFY_BUILD_SUMMARY.md** - Build summary

---

**Last Updated:** February 2026
**Framework:** Strands Agents SDK
**Status:** Production Ready ✓
