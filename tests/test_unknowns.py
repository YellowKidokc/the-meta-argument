import unittest
from meta_argument.scoring import score_variable
class UnknownTests(unittest.TestCase):
    def test_all_unknown_has_no_score(self):
        r=score_variable({'answers':[{'answer':'UNKNOWN'}]})
        self.assertIsNone(r.raw_score)
        self.assertEqual(r.coverage,0.0)
