import unittest

from ..src.primitives import Arrangement, Note
from ..src.species import FirstSpecies
from ..src.voices import CantusFirmus
from ..src.voices import Voice


class FuxExampleTestCase(unittest.TestCase):
    def test_first_fux_example_is_valid(self):
        dorian_cf = CantusFirmus('dorian')
        arrangement = Arrangement(2, FirstSpecies, cantus_firmus=dorian_cf, cantus_firmus_voice_index=0)
        arrangement.insert_voice(
            1,
            Voice([Note('A', 4), Note('A', 4), Note('G', 4), Note('A', 4), Note('B', 4), Note('C', 5), Note('C', 5), Note('B', 4), Note('D', 5), Note('C#', 5), Note('D', 5)]),
        )

        print(arrangement)

        self.assertTrue(arrangement.validate().all(), 'Valid example is failing validation')


if __name__ == '__main__':
    unittest.main()
