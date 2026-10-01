# Unit tests for recommendation logic.
import sys  # Import module path support.
from pathlib import Path  # Import path support.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))  # Add service source to the path.
from app import recommendations  # Import recommendation logic.
import unittest  # Import test support.

class RecommendationUnitTests(unittest.TestCase):  # Define unit tests.
    def test_known_user(self): self.assertEqual(recommendations("u1"), ["m2", "m3"])  # Verify known recommendations.
    def test_unknown_user(self): self.assertEqual(recommendations("unknown"), ["m1", "m2"])  # Verify default recommendations.

if __name__ == "__main__": unittest.main()  # Run tests directly.
