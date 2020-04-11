import numpy as np

from src.primitives import Note


class CantusFirmus:
    _MODE_MAP = {
        'dorian': [
            Note('D', 4),
            Note('F', 4),
            Note('E', 4),
            Note('D', 4),
            Note('G', 4),
            Note('F', 4),
            Note('A', 5),
            Note('G', 5),
            Note('F', 4),
            Note('E', 5),
            Note('D', 5),
        ],
    }

    def __init__(self, mode, voice):
        self.notes = self._MODE_MAP[mode]
        self.voice = voice

    @property
    def note_numbers(self):
        if hasattr(self, '_note_numbers'):
            return self._note_numbers
        self._note_numbers = np.array([note.note_number for note in self.notes])
        return self.note_numbers
