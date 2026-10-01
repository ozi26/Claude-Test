"""Recommendation service that returns deterministic media suggestions."""  # Describe the service.
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer  # Import standard HTTP server classes.
from pathlib import Path  # Import path support.
import json  # Import JSON support.
import sys  # Import module path support.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "config"))  # Add central config to the path.
import recommendation_config  # Load service configuration.

CATALOG = {"u1": ["m2", "m3"], "u2": ["m1", "m3"]}  # Define deterministic recommendations.

def recommendations(user_id):  # Return recommendations for one user.
    return CATALOG.get(user_id, ["m1", "m2"])  # Return known or default recommendations.

class Handler(BaseHTTPRequestHandler):  # Define the HTTP handler.
    def _json(self, status, body):  # Send JSON output.
        data = json.dumps(body).encode()  # Serialize the response.
        self.send_response(status); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)  # Send headers and body.
    def do_GET(self):  # Handle GET requests.
        if self.path == "/health": self._json(200, {"status":"ok","service":recommendation_config.SERVICE_NAME}); return  # Serve health checks.
        if self.path.startswith("/recommendations/"): self._json(200, {"userId":self.path.split("/")[-1],"mediaIds":recommendations(self.path.split("/")[-1])}); return  # Serve recommendations.
        self._json(404, {"error":"Route not found"})  # Reject unknown routes.
    def log_message(self, format, *args): return  # Disable access logs.

def create_server(port=0):  # Create the HTTP server.
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)  # Return the configured server.

if __name__ == "__main__": create_server(recommendation_config.PORT).serve_forever()  # Start the service.
