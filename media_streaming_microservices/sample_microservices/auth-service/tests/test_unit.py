# Unit tests for authentication logic.
import sys  # Import path support.
from pathlib import Path  # Import path handling.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))  # Add the source folder to the test path.
from app import login  # Import the business function.
import unittest  # Import Python's standard testing framework.

class AuthUnitTests(unittest.TestCase):  # Define authentication unit tests.
    def test_valid_login(self):  # Test valid credentials.
        self.assertEqual(login("demo@example.com", "demo123")["userId"], "u1")  # Confirm the correct user is returned.
    def test_invalid_login(self):  # Test invalid credentials.
        self.assertIsNone(login("demo@example.com", "wrong"))  # Confirm invalid credentials fail.

if __name__ == "__main__": unittest.main()  # Run tests when the file is executed directly.
