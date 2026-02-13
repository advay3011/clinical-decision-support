"""
Spotify OAuth Login Handler v2
Uses custom callback server for OAuth redirects.
"""

import os
import webbrowser
import requests
import threading
import time
from urllib.parse import urlencode
from dotenv import load_dotenv
from spotify_callback_server import start_callback_server, get_auth_code, get_error

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")

def get_user_access_token():
    """Get user access token using Authorization Code flow."""
    
    print("=" * 70)
    print("SPOTIFY OAUTH LOGIN v2")
    print("=" * 70)
    print()
    
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET not set in .env")
        return None
    
    # Step 1: Start callback server
    print("Starting callback server...")
    server = start_callback_server(port=8888)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print(f"Callback server running on {REDIRECT_URI}")
    print()
    
    # Step 2: Generate authorization URL
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "user-top-read user-read-recently-played",
        "show_dialog": "true"
    }
    
    full_auth_url = f"{auth_url}?{urlencode(params)}"
    
    print("Opening Spotify login in your browser...")
    print("Please authorize the app to access your listening data.")
    print()
    
    # Open browser
    webbrowser.open(full_auth_url)
    
    # Step 3: Wait for callback
    print("Waiting for authorization...")
    timeout = 120
    start_time = time.time()
    
    while (time.time() - start_time) < timeout:
        auth_code = get_auth_code()
        error = get_error()
        
        if auth_code:
            print("Authorization code received!")
            break
        
        if error:
            print(f"Authorization error: {error}")
            server.shutdown()
            return None
        
        time.sleep(0.5)
    
    # Stop server
    server.shutdown()
    
    if not auth_code:
        print("Authorization timeout. Please try again.")
        return None
    
    print()
    
    # Step 4: Exchange code for access token
    print("Exchanging code for access token...")
    token_url = "https://accounts.spotify.com/api/token"
    
    token_data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    
    try:
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        token_response = response.json()
        
        access_token = token_response.get("access_token")
        refresh_token = token_response.get("refresh_token")
        expires_in = token_response.get("expires_in")
        
        print("Access token obtained!")
        print(f"Token expires in: {expires_in} seconds ({expires_in // 3600} hours)")
        print()
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": expires_in,
            "token_type": "Bearer"
        }
    
    except Exception as e:
        print(f"Error exchanging code for token: {e}")
        return None

if __name__ == "__main__":
    token_info = get_user_access_token()
    
    if token_info:
        print("=" * 70)
        print("LOGIN SUCCESSFUL!")
        print("=" * 70)
        print()
        
        access_token = token_info['access_token']
        
        # Find .env file (look in parent directory)
        import pathlib
        env_file = pathlib.Path(__file__).parent.parent / ".env"
        
        # Read existing .env
        try:
            with open(env_file, 'r') as f:
                env_content = f.read()
        except FileNotFoundError:
            env_content = ""
        
        # Update or add SPOTIFY_USER_TOKEN
        if 'SPOTIFY_USER_TOKEN=' in env_content:
            # Replace existing token
            lines = env_content.split('\n')
            new_lines = []
            for line in lines:
                if line.startswith('SPOTIFY_USER_TOKEN='):
                    new_lines.append(f'SPOTIFY_USER_TOKEN="{access_token}"')
                else:
                    new_lines.append(line)
            env_content = '\n'.join(new_lines)
        else:
            # Add new token
            if env_content and not env_content.endswith('\n'):
                env_content += '\n'
            env_content += f'SPOTIFY_USER_TOKEN="{access_token}"'
        
        # Write back to .env
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"Token saved to {env_file}!")
        print()
        print(f"Full token: {access_token}")
        print()
        print("You can now run:")
        print("  python3 spotify_personal_agent.py")
    else:
        print("Login failed. Please try again.")
