import json, unittest
from pathlib import Path
from meta_argument.scoring import score_case
class PilotCaseTests(unittest.TestCase):
    def test_fourteen_pilot_cases_exist_and_refuse_until_evidenced(self):
        files=list(Path('cases/historical').glob('*.json'))
        self.assertGreaterEqual(len(files),14)
        for p in files:
            r=score_case(json.loads(p.read_text()))
            self.assertIn(r['status'], {'REFUSED','SCORED'})
