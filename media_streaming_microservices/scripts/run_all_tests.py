"""Run every language-specific test suite from one command."""  # Describe the script.
from pathlib import Path  # Import path handling.
import subprocess  # Import process execution.
import sys  # Import Python executable information.

ROOT = Path(__file__).resolve().parents[1]  # Calculate the project root.
COMMANDS = [ # Define all test commands.
    ["npm", "test", "--", "--runInBand"], # Run catalog tests.
]

def run(command, cwd):  # Execute one test command.
    print(f"Running: {' '.join(command)} in {cwd}")  # Print the command for visibility.
    return subprocess.run(command, cwd=cwd, check=False).returncode  # Return the command exit code.

def main():  # Run the full test sequence.
    failures = 0  # Count failed suites.
    failures += run(["npm", "test", "--", "--runInBand"], ROOT / "sample_microservices/catalog-service")  # Test catalog.
    failures += run(["npm", "test", "--", "--runInBand"], ROOT / "sample_microservices/streaming-service")  # Test streaming.
    failures += run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"], ROOT / "sample_microservices/auth-service") if False else 0  # Keep the script portable; Python services are run below.
    for service in ["auth-service", "recommendation-service"]: # Run both Python service suites.
        failures += run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"], ROOT / "sample_microservices" / service) # Execute Python tests.
    for service in ["watchlist-service", "history-service"]: # Run Java service suites.
        failures += run(["mvn", "test"], ROOT / "sample_microservices" / service) # Execute Maven tests.
    for service in ["subscription-service", "notification-service"]: # Run .NET service suites.
        failures += run(["dotnet", "test", "tests"], ROOT / "sample_microservices" / service) # Execute xUnit tests.
    if failures: raise SystemExit(failures) # Fail when any suite fails.
    print("All language-specific tests passed.") # Report successful testing.

if __name__ == "__main__": main() # Run the script directly.
