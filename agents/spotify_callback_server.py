"""
Spotify OAuth Callback Server
Simple web server to handle Spotify OAuth redirects.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

# Global to store the auth code
auth_code = None
error_message = None

class CallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback from Spotify."""
    
    def do_GET(self):
        global auth_code, error_message
        
        # Parse the URL
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Check for authorization code
        if "code" in query_params:
            auth_code = query_params["code"][0]
            
            # Send success response
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            html = """
            <html>
            <head>
                <title>Spotify Authorization</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        padding: 50px;
                        background: linear-gradient(135deg, #1DB954 0%, #191414 100%);
                        color: white;
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }
                    .container {
                        background: rgba(0, 0, 0, 0.5);
                        padding: 40px;
                        border-radius: 10px;
                    }
                    h1 { color: #1DB954; }
                    p { font-size: 16px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Authorization Successful!</h1>
                    <p>Your Spotify account has been connected.</p>
                    <p>You can close this window and return to the terminal.</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        
        # Check for error
        elif "error" in query_params:
            error_message = query_params["error"][0]
            
            # Send error response
            self.send_response(400)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            html = f"""
            <html>
            <head>
                <title>Spotify Authorization Error</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        text-align: center;
                        padding: 50px;
                        background: linear-gradient(135deg, #1DB954 0%, #191414 100%);
                        color: white;
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }}
                    .container {{
                        background: rgba(0, 0, 0, 0.5);
                        padding: 40px;
                        border-radius: 10px;
                    }}
                    h1 {{ color: #FF6B6B; }}
                    p {{ font-size: 16px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Authorization Failed</h1>
                    <p>Error: {error_message}</p>
                    <p>Please try again.</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        
        else:
            # Unknown request
            self.send_response(400)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            html = """
            <html>
            <head>
                <title>Invalid Request</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        padding: 50px;
                    }
                </style>
            </head>
            <body>
                <h1>Invalid Request</h1>
                <p>This page is for Spotify OAuth callbacks only.</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def start_callback_server(port=8888):
    """Start the callback server."""
    server = HTTPServer(("127.0.0.1", port), CallbackHandler)
    print(f"Callback server started on http://127.0.0.1:{port}")
    return server

def get_auth_code():
    """Get the authorization code from the callback."""
    global auth_code
    return auth_code

def get_error():
    """Get any error from the callback."""
    global error_message
    return error_message

if __name__ == "__main__":
    server = start_callback_server()
    print("Waiting for Spotify authorization...")
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.shutdown()
