"""Authentication service with a small in-memory user store."""  # Describe the module purpose.
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer  # Import the standard HTTP server classes.
from pathlib import Path  # Import path handling for centralized configuration.
import json  # Import JSON support.
import sys  # Import Python path support.

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "config"))  # Add the central config directory to the module path.
import auth_config  # Import the language-specific configuration.

USERS = {"demo@example.com": {"password": "demo123", "userId": "u1"}}  # Define the demonstration users.

def login(email, password):  # Validate login credentials.
    user = USERS.get(email)  # Look up the user by email.
    if user and user["password"] == password:  # Check whether the credentials match.
        return {"token": f"token-{user['userId']}", "userId": user["userId"]}  # Return a simple prototype token.
    return None  # Return no token when credentials are invalid.

class Handler(BaseHTTPRequestHandler):  # Define the HTTP request handler.
    def _json(self, status, body):  # Send a JSON response.
        data = json.dumps(body).encode()  # Encode the response as bytes.
        self.send_response(status)  # Send the HTTP status.
        self.send_header("Content-Type", "application/json")  # Set the content type.
        self.send_header("Content-Length", str(len(data)))  # Set the response length.
        self.end_headers()  # Finish response headers.
        self.wfile.write(data)  # Write the response body.

    def do_GET(self):  # Handle GET requests.
        if self.path == "/health": self._json(200, {"status": "ok", "service": auth_config.SERVICE_NAME}); return  # Serve health checks.
        self._json(404, {"error": "Route not found"})  # Reject unknown routes.

    def do_POST(self):  # Handle POST requests.
        if self.path != "/login": self._json(404, {"error": "Route not found"}); return  # Reject unknown routes.
        length = int(self.headers.get("Content-Length", "0"))  # Read the request length.
        body = json.loads(self.rfile.read(length) or b"{}")  # Parse the JSON body.
        result = login(body.get("email", ""), body.get("password", ""))  # Validate credentials.
        self._json(200, result) if result else self._json(401, {"error": "Invalid credentials"})  # Return the result.

    def log_message(self, format, *args):  # Silence default HTTP logs during tests.
        return  # Do nothing for each access log.

def create_server(port=0):  # Create an authentication HTTP server.
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)  # Bind to localhost and return the server.

if __name__ == "__main__":  # Start the service when executed directly.
    create_server(auth_config.PORT).serve_forever()  # Serve requests forever on the configured port.
