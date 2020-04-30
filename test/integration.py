import unittest

from ..src.primitives import Arrangement, Note
from ..src.species import FirstSpeciesTwoVoices
from ..src.voices import CantusFirmus
from ..src.voices import Voice


class FuxExampleTestCase(unittest.TestCase):
    def test_first_fux_example_is_valid(self):
        dorian_cf = CantusFirmus('dorian')
        arrangement = Arrangement(FirstSpeciesTwoVoices, cantus_firmus=dorian_cf, cantus_firmus_voice_index=0)
        arrangement.insert_voice(
            1,
            Voice([Note('A', 4), Note('A', 4), Note('G', 4), Note('A', 4), Note('B', 4), Note('C', 5), Note('C', 5), Note('B', 4), Note('D', 5), Note('C#', 5), Note('D', 5)]),
        )

        validation_results = arrangement.validate()

        self.assertFalse(validation_results.is_empty(), 'Validation results should not be empty')
        self.assertTrue(validation_results, 'Valid example is failing validation')

    def test_first_fux_counterexample_is_invalid(self):
        dorian_cf = CantusFirmus('dorian')
        arrangement = Arrangement(FirstSpeciesTwoVoices, cantus_firmus=dorian_cf, cantus_firmus_voice_index=1)
        arrangement.insert_voice(
            0,
            Voice([Note('G', 3), Note('D', 4), Note('A', 3), Note('F', 3), Note('E', 3), Note('D', 3), Note('F', 3), Note('C', 4), Note('D', 4), Note('C#', 4), Note('D', 4)]),
        )

        validation_results = arrangement.validate()

        self.assertFalse(validation_results.is_empty(), 'Validation results should not be empty')
        self.assertFalse(validation_results, 'Invalid example is passing validation')


if __name__ == '__main__':
    unittest.main()
