import base64
import requests
import urllib.parse
import webbrowser
import http.server
import socketserver

class SpotifyUserAuth:
    def __init__(self, client_id, client_secret, redirect_uri="http://127.0.0.1:8888/callback", scope=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope or "playlist-read-private playlist-read-collaborative user-library-read user-read-recently-played"
        self.access_token = None
        self.refresh_token = None

    def get_auth_url(self):
        query_params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": self.scope
        }
        url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(query_params)
        return url

    def open_browser_for_auth(self):
        url = self.get_auth_url()
        print("Opening browser for Spotify login...")
        webbrowser.open(url)

    def exchange_code_for_token(self, code):
        auth_string = f"{self.client_id}:{self.client_secret}"
        b64_auth = base64.b64encode(auth_string.encode()).decode()

        token_url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }

        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()

        tokens = response.json()
        self.access_token = tokens.get("access_token")
        self.refresh_token = tokens.get("refresh_token")

        return tokens

class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        code = params.get('code')
        if code:
            self.server.auth_code = code[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h1>Authorization complete! You can close this window.</h1>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<h1>Error: No code found.</h1>")

def start_local_server(port=8888):
    handler = OAuthCallbackHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Waiting for redirect on http://127.0.0.1:{port}/callback ...")
        httpd.handle_request()
        return httpd.auth_code