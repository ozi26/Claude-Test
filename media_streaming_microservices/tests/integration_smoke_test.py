"""Check the health endpoint of every running MediaStreamX service."""  # Explain the smoke test.
import json  # Import JSON support for request bodies.
from urllib.request import urlopen, Request  # Import standard HTTP client helpers.

SERVICES = {"catalog-service":8101,"streaming-service":8102,"auth-service":8103,"recommendation-service":8104,"watchlist-service":8105,"history-service":8106,"subscription-service":8107,"notification-service":8108}  # Define all service endpoints.

def main():  # Run the deployment smoke test.
    failures = []  # Store unavailable services.
    for name, port in SERVICES.items():  # Check every service.
        try:  # Protect each check from connection errors.
            with urlopen(f"http://127.0.0.1:{port}/health", timeout=5) as response:  # Call the health endpoint.
                if response.status != 200: failures.append(name)  # Record non-success responses.
        except Exception: failures.append(name)  # Record connection failures.
    if failures: raise SystemExit(f"Health checks failed: {failures}")  # Fail CI when a service is down.
    print("All eight service health checks passed.")  # Report success.

if __name__ == "__main__": main()  # Execute the smoke test directly.
