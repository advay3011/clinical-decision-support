# Spotify Login Guide - Use Your Own Account

Get your personal Spotify access token and analyze your real listening data.

## Quick Start (3 Steps)

### Step 1: Run the OAuth Login Script

```bash
source spotify_env/bin/activate
cd agents
python3 spotify_oauth_login.py
```

This will:
- Start a local server
- Open Spotify login in your browser
- Ask you to authorize the app
- Get your access token

### Step 2: Authorize in Browser

When your browser opens:
1. Log in with your Spotify account
2. Click "Agree" to authorize the app
3. You'll be redirected to a success page
4. Return to the terminal

### Step 3: Save Your Token

The script will show your access token. Add it to `.env`:

```bash
# In .env file, add:
SPOTIFY_USER_TOKEN='your_access_token_here'
```

## Run Analysis with Your Data

Once you have your token:

```bash
source spotify_env/bin/activate
cd agents
python3 spotify_personal_agent.py
```

This will:
- Fetch your top artists
- Fetch your top tracks
- Fetch your recently played
- Analyze your listening patterns
- Generate personalized insights
- Show trends over time

## What Permissions Are Requested?

The app requests:
- `user-top-read` - Access to your top artists and tracks
- `user-read-recently-played` - Access to your recently played tracks

**No write permissions** - The app only reads your data, doesn't modify anything.

## Example Output

```
SPOTIFY LISTENING ANALYZER - YOUR PERSONAL DATA
======================================================================

✓ Access token found

Fetching your Spotify data...
----------------------------------------------------------------------
Fetching top artists...
✓ Got 50 top artists
Fetching top tracks...
✓ Got 50 top tracks
Fetching recently played...
✓ Got 50 recently played tracks

Analyzing your listening data...
----------------------------------------------------------------------

STEP 1: Your Top Genres
----------------------------------------------------------------------
Found 24 unique genres
Top genres:
  1. hip-hop: 18 mentions
  2. rap: 15 mentions
  3. trap: 12 mentions
  4. r-n-b: 8 mentions
  5. pop: 6 mentions

STEP 2: Your Listening Patterns
----------------------------------------------------------------------
Top 5 artists:
  1. Drake
  2. The Weeknd
  3. Kendrick Lamar
  4. J. Cole
  5. Kanye West

Diversity score: 85.2%
Repeated tracks: 8 / 50

Recent favorites:
  • Drake: 12 plays
  • The Weeknd: 9 plays
  • Kendrick Lamar: 7 plays

STEP 3: Your Insights
----------------------------------------------------------------------
Time range: last 6 months

Insights:
  • Your most listened genre is hip-hop.
  • Your favorite artist is Drake.
  • You replay songs frequently.
  • Your listening variety is high (85.2%).

Summary:
  Your most listened genre is hip-hop. Your favorite artist is Drake. 
  You replay songs frequently. Your listening variety is high (85.2%).

STEP 4: Your Trends Over Time
----------------------------------------------------------------------
Trends:
  • New favorites: Playboi Carti, Lil Baby
  • Consistent favorites: Drake, The Weeknd, Kendrick Lamar
  • Artists you used to listen to: Old Kanye, Jay-Z

======================================================================
✓ ANALYSIS COMPLETE!
======================================================================
```

## Troubleshooting

### "SPOTIFY_USER_TOKEN not found"
- Run `python3 spotify_oauth_login.py` to get your token
- Add it to `.env` as `SPOTIFY_USER_TOKEN='...'`

### "401 Unauthorized"
- Your token may have expired (tokens last 1 hour)
- Run the login script again to get a fresh token

### "Browser didn't open"
- Copy the URL from the terminal and open it manually in your browser
- Complete the authorization
- The token will be displayed in the terminal

### "Connection refused"
- Make sure port 8888 is available
- Or modify the redirect URI in the script

## Token Expiration

Access tokens expire after 1 hour. To get a new one:

```bash
python3 spotify_oauth_login.py
```

Then update `.env` with the new token.

## Security Notes

- Your token is stored in `.env` (local file only)
- Never share your token publicly
- The app only reads your data, doesn't modify it
- You can revoke access anytime in Spotify settings

## Next Steps

1. Run the login script
2. Authorize in your browser
3. Save your token to `.env`
4. Run the personal agent
5. See your personalized insights!

## Files

- `spotify_oauth_login.py` - Get your access token
- `spotify_personal_agent.py` - Analyze your data
- `.env` - Store your token (keep private!)

---

Ready to analyze your Spotify data? Let's go!
