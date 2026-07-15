import json, unittest
from pathlib import Path
from meta_argument.scoring import score_case, score_variable

class VariableScoringTests(unittest.TestCase):
    def test_unknown_is_not_zero(self):
        r=score_variable({'answers':[{'question_id':'G1','answer':'UNKNOWN','weight':1},{'question_id':'G2','answer':'YES','weight':1,'evidence_quality':1}]})
        self.assertEqual(r.raw_score, 3.0)
        self.assertEqual(r.coverage, 0.5)
        self.assertEqual(r.unknown_fraction, 0.5)
    def test_not_applicable_is_excluded(self):
        r=score_variable({'answers':[{'question_id':'F1','answer':'NOT_APPLICABLE'},{'question_id':'F2','answer':'NO','evidence_quality':1}]})
        self.assertEqual(r.raw_score, -3.0)
        self.assertEqual(r.coverage, 1.0)
    def test_weighted_workbook_style_formula(self):
        r=score_variable({'answers':[{'answer':'YES','weight':2,'evidence_quality':1},{'answer':'NO','weight':1,'evidence_quality':1}]})
        self.assertAlmostEqual(r.raw_score, 1.0)

class CaseScoringTests(unittest.TestCase):
    def test_fixture_scores(self):
        c=json.loads(Path('examples/fixture.json').read_text())
        result=score_case(c)
        self.assertEqual(result['status'],'SCORED')
        self.assertEqual(result['variables']['G']['raw_score'],3.0)
        self.assertEqual(result['variables']['T']['raw_score'],-3.0)
        self.assertEqual(result['veto']['variable'],'T')
    def test_refusal_state_prevents_false_precision(self):
        c=json.loads(Path('cases/historical/hiroshima-1945.json').read_text())
        self.assertEqual(score_case(c)['status'],'REFUSED')
if __name__=='__main__': unittest.main()
