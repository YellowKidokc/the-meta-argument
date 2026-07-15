import copy, json, unittest
from pathlib import Path
from meta_argument.anti_gaming import compare_scores
class IdentitySwapTests(unittest.TestCase):
    def test_identical_answers_pass(self):
        a=json.loads(Path('examples/fixture.json').read_text()); b=copy.deepcopy(a); b['actor']='Identity B'
        passed, delta=compare_scores(a,b)
        self.assertTrue(passed); self.assertEqual(delta,0)
