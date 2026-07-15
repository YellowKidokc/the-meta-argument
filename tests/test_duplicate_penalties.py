import unittest
from meta_argument.anti_gaming import run_anti_gaming
class DuplicatePenaltyTests(unittest.TestCase):
    def test_missing_packet_is_visible(self):
        r=run_anti_gaming({})
        self.assertFalse(r['duplicate_penalty']['passed'])
