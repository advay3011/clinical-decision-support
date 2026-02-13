"""
Test Spotify Token
Verify your access token is valid.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("SPOTIFY_USER_TOKEN")

if not token:
    print("No token found in .env")
    exit(1)

print(f"Testing token: {token[:30]}...")
print()

headers = {"Authorization": f"Bearer {token}"}

try:
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        print("✓ Token is valid!")
        print(f"  User: {user_data.get('display_name')}")
        print(f"  Email: {user_data.get('email')}")
        print(f"  Followers: {user_data.get('followers', {}).get('total')}")
    else:
        print(f"✗ Token error: {response.status_code}")
        print(f"  {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")
