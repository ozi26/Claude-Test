# Integration tests for the authentication HTTP server.
import json  # Import JSON support.
import threading  # Import background server support.
import unittest  # Import the test framework.
from http.client import HTTPConnection  # Import the standard HTTP client.
import sys  # Import path support.
from pathlib import Path  # Import path handling.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))  # Add source to the path.
from app import create_server  # Import the real HTTP server.

class AuthIntegrationTests(unittest.TestCase):  # Define integration tests.
    def test_login_endpoint(self):  # Test the login endpoint.
        server = create_server(0)  # Start on an ephemeral port.
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()  # Run the server in the background.
        conn = HTTPConnection("127.0.0.1", server.server_port)  # Connect to the real server.
        payload = json.dumps({"email":"demo@example.com","password":"demo123"})  # Create the request body.
        conn.request("POST", "/login", payload, {"Content-Type":"application/json"})  # Send the login request.
        response = conn.getresponse()  # Read the response.
        body = json.loads(response.read())  # Parse the JSON response.
        server.shutdown(); server.server_close()  # Stop the server.
        self.assertEqual(response.status, 200)  # Verify HTTP status.
        self.assertEqual(body["userId"], "u1")  # Verify the user ID.

if __name__ == "__main__": unittest.main()  # Run tests directly when requested.
