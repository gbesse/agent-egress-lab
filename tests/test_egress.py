import sys
import unittest
from pathlib import Path
from egress_lab import run

ROOT = Path(__file__).resolve().parents[1]


class EgressTests(unittest.TestCase):
    def test_detects_synthetic_canary(self):
        result = run([sys.executable, str(ROOT / 'examples/leaky_agent.py')], 'SYNTHETIC-CANARY-123', ['127.0.0.1'])
        self.assertFalse(result['pass'])
        self.assertGreater(result['canary_exposures'], 0)
        self.assertEqual(result['disallowed_destinations'], [])

    def test_clean_agent_passes(self):
        result = run([sys.executable, '-c', 'print("done")'], 'SYNTHETIC-CANARY-123', [])
        self.assertTrue(result['pass'])
