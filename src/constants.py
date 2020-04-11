import itertools

# TODO: Maybe this stuff should all live inside the Note class?

# Note numbers etc. based on MIDI standard
NOTE_NUMBERS = range(128)
OCTAVES = range(-1, 10)
NOTE_NAMES = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

# Build the full lookup
_note_number_iter = iter(NOTE_NUMBERS)
NOTE_LOOKUP = tuple(
    (next(_note_number_iter), note_name, octave) for octave, note_name in itertools.product(OCTAVES, NOTE_NAMES)
)


# Spot checks
def get_note_number(_name, _octave):
    return next(
        number for (number, name, octave) in NOTE_LOOKUP if name == _name and octave == _octave
    )


assert get_note_number('D', 0) == 14, 'D0 should be 14'
assert get_note_number('B', 3) == 59, 'B3 should be 59'
assert get_note_number('G', 9) == 127, 'G9 should be 127'
assert get_note_number('C', 4) == 60, 'Middle C should be 60'

if __name__ == '__main__':
    pass
