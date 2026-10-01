"""Analyze the MediaStreamX repository and write a small JSON report."""  # Explain the purpose of this file.
from pathlib import Path  # Import the path helper used to inspect folders.
import json  # Import JSON support for the generated report.

ROOT = Path(__file__).resolve().parents[1]  # Calculate the project root directory.
SERVICES = ["catalog-service", "streaming-service", "auth-service", "recommendation-service", "watchlist-service", "history-service", "subscription-service", "notification-service"]  # List all services.
LANGUAGES = {"catalog-service":"JavaScript", "streaming-service":"JavaScript", "auth-service":"Python", "recommendation-service":"Python", "watchlist-service":"Java", "history-service":"Java", "subscription-service":"C#", "notification-service":"C#"}  # Map each service to its language.
PORTS = {"catalog-service":8101, "streaming-service":8102, "auth-service":8103, "recommendation-service":8104, "watchlist-service":8105, "history-service":8106, "subscription-service":8107, "notification-service":8108}  # Map services to ports.

def analyze():  # Define the repository analysis function.
    report = []  # Create the output list.
    for service in SERVICES:  # Visit every service.
        service_dir = ROOT / "sample_microservices" / service  # Calculate the service folder.
        test_count = len(list((service_dir / "tests").glob("test_*"))) if (service_dir / "tests").exists() else 0  # Count test files.
        report.append({"service": service, "language": LANGUAGES[service], "port": PORTS[service], "test_files": test_count})  # Add service facts.
    return report  # Return the completed report.

if __name__ == "__main__":  # Run only when executed directly.
    output = ROOT / "analyzer_result.json"  # Select the report destination.
    output.write_text(json.dumps(analyze(), indent=2), encoding="utf-8")  # Write the JSON report.
    print(output)  # Print the report path for CI logs.
