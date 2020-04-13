import numpy as np

from src.primitives import Note


class Voice:
    def __init__(self, notes):
        self.notes = notes

    @property
    def note_numbers(self):
        if hasattr(self, '_note_numbers'):
            return self._note_numbers
        self._note_numbers = np.array([note.note_number for note in self.notes])
        return self.note_numbers


class CantusFirmus(Voice):
    _MODE_MAP = {
        'dorian': [Note('D', 4), Note('F', 4), Note('E', 4), Note('D', 4), Note('G', 4), Note('F', 4), Note('A', 4), Note('G', 4), Note('F', 4), Note('E', 4), Note('D', 4)],
    }

    def __init__(self, mode):
        super().__init__(notes=self._MODE_MAP[mode])
