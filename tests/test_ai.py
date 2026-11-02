import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ai.decision_engine import DecisionEngine, KalshiAnalysis

class TestDecisionEngine(unittest.TestCase):
    def test_analyze_event(self):
        engine = DecisionEngine()
        result = engine.analyze_event({"ticker": "TEST"}, "Some news")
        self.assertIsInstance(result, KalshiAnalysis)
        self.assertEqual(result.yes_confidence, 0.6)
        self.assertEqual(result.no_confidence, 0.4)

if __name__ == '__main__':
    unittest.main()
