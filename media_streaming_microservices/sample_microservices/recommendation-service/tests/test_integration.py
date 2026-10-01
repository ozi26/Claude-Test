# Integration tests for the recommendation HTTP endpoint.
import json  # Import JSON support.
import threading  # Import background server support.
import unittest  # Import test support.
from http.client import HTTPConnection  # Import the HTTP client.
import sys  # Import module path support.
from pathlib import Path  # Import path support.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))  # Add source to the path.
from app import create_server  # Import the real server.

class RecommendationIntegrationTests(unittest.TestCase):  # Define integration tests.
    def test_recommendation_endpoint(self):  # Test the HTTP API.
        server = create_server(0); threading.Thread(target=server.serve_forever, daemon=True).start()  # Start the server.
        conn = HTTPConnection("127.0.0.1", server.server_port); conn.request("GET", "/recommendations/u1")  # Call the API.
        response = conn.getresponse(); body = json.loads(response.read()); server.shutdown(); server.server_close()  # Read and stop the service.
        self.assertEqual(response.status, 200); self.assertEqual(body["mediaIds"], ["m2", "m3"])  # Verify the API result.

if __name__ == "__main__": unittest.main()  # Run tests directly.
