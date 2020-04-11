import unittest

from ..src.primitives import Arrangement, Note
from ..src.primitives import Species
from ..src.cantus_firmi import CantusFirmus


class FuxExampleTestCase(unittest.TestCase):
    def test_first_fux_example_is_valid(self):
        dorian_cf = CantusFirmus('dorian', voice=0)
        arrangement = Arrangement(2, Species.FIRST, cantus_firmus=dorian_cf)
        arrangement.insert_voice(
            1,
            [
                Note('A', 4),
                Note('A', 4),
                Note('G', 4),
                Note('A', 4),
                Note('B', 4),
                Note('C', 5),
                Note('C', 5),
                Note('B', 4),
                Note('D', 5),
                Note('C#', 5),
                Note('D', 5),
            ],
        )

        self.assertTrue(arrangement.valid().all(), 'Valid example is failing validation')


if __name__ == '__main__':
    unittest.main()