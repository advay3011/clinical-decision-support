"""
Spotify OAuth Login Handler
Implements Authorization Code flow to get user access token.
"""

import os
import webbrowser
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")

# Global variable to store the auth code
auth_code = None
server_ready = False

class CallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback from Spotify."""
    
    def do_GET(self):
        global auth_code
        
        # Parse the callback URL
        if "code=" in self.path:
            # Extract authorization code
            auth_code = self.path.split("code=")[1].split("&")[0]
            
            # Send success response
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_content = """
            <html>
            <head><title>Spotify Authorization</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>Authorization Successful!</h1>
                <p>You can close this window and return to the terminal.</p>
                <p>Your Spotify account has been connected.</p>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
        else:
            # Error response
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_content = """
            <html>
            <head><title>Spotify Authorization Error</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>Authorization Failed</h1>
                <p>There was an error during authorization.</p>
                <p>Please try again.</p>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def get_user_access_token():
    """Get user access token using Authorization Code flow."""
    
    global auth_code, server_ready
    
    print("=" * 70)
    print("SPOTIFY OAUTH LOGIN")
    print("=" * 70)
    print()
    
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ Error: SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET not set in .env")
        return None
    
    # Step 1: Start local server to receive callback
    print("Starting local server for OAuth callback...")
    server = HTTPServer(("localhost", 8888), CallbackHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    server_ready = True
    print("✓ Server started on http://localhost:8888")
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
    
    # Wait for callback
    print("Waiting for authorization...")
    timeout = 60
    start_time = time.time()
    
    while auth_code is None and (time.time() - start_time) < timeout:
        time.sleep(0.5)
    
    # Stop server
    server.shutdown()
    
    if auth_code is None:
        print("❌ Authorization timeout. Please try again.")
        return None
    
    print("✓ Authorization code received!")
    print()
    
    # Step 3: Exchange code for access token
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
        
        print("✓ Access token obtained!")
        print(f"  Token expires in: {expires_in} seconds ({expires_in // 3600} hours)")
        print()
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": expires_in,
            "token_type": "Bearer"
        }
    
    except Exception as e:
        print(f"❌ Error exchanging code for token: {e}")
        return None

if __name__ == "__main__":
    token_info = get_user_access_token()
    
    if token_info:
        print("=" * 70)
        print("✓ LOGIN SUCCESSFUL!")
        print("=" * 70)
        print()
        print("Your access token:")
        print(f"  {token_info['access_token'][:50]}...")
        print()
        print("Save this token to use with the agent:")
        print("  export SPOTIFY_USER_TOKEN='<your_access_token>'")
        print()
        print("Or use it directly in the agent code.")
    else:
        print("❌ Login failed. Please try again.")
