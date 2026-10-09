import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ai.decision_engine import DecisionEngine

class TestDecisionEngine(unittest.TestCase):
    def test_analyze_event(self):
        engine = DecisionEngine()
        result = engine.analyze_event({"ticker": "TEST"}, "Some news")
        self.assertIn("yes_confidence", result)
        self.assertIn("no_confidence", result)

if __name__ == '__main__':
    unittest.main()
