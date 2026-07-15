import copy, json, unittest
from pathlib import Path
from meta_argument.scoring import score_case
class SymmetryTests(unittest.TestCase):
    def test_names_do_not_change_score(self):
        a=json.loads(Path('examples/fixture.json').read_text()); b=copy.deepcopy(a)
        b['actor']='Swapped identity'; b['target']='Opposite identity'
        self.assertEqual(score_case(a)['direction'], score_case(b)['direction'])
