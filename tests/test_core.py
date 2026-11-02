import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.core.config import Config

class TestConfig(unittest.TestCase):
    def test_config_defaults(self):
        config = Config()
        self.assertEqual(config.KALSHI_ENV, 'demo')
        self.assertEqual(config.MAX_POSITION_SIZE, 0.05)

if __name__ == '__main__':
    unittest.main()
