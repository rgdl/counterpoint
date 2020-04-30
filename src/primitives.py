import itertools

import numpy as np

from . import constants


# All rules here (my local machine):
# ~/Documents/Gradus Ad Parnassum Summarised.docx


class StepResult:
    """
    Collects the results of applying all rules at a given step
    """
    def __init__(self, step):
        self.step = step
        self._rule_results = []

    def push(self, description, rule, voices, rule_passed):
        self._rule_results.append(
            {
                'description': description,
                'rule': rule,
                'voices': voices,
                'rule_passed': rule_passed,
            }
        )

    def __bool__(self):
        return all([result['rule_passed'] for result in self._rule_results])


class ArrangementResult:
    """
    Collects a `StepResult` at each step of an `Arrangement`
    """
    def __init__(self, arrangement):
        self.arrangement = arrangement
        self._step_results = {}

    def __bool__(self):
        return all([step_result for step_result in self._step_results])

    def __getitem__(self, step):
        print('self._step_results =', self._step_results)
        return self._step_results.get(step, StepResult(step))

    def __repr__(self):
        return str(self._step_results)

    def is_empty(self):
        return self._step_results == {}


class Arrangement:
    def __init__(self, species_and_voices, cantus_firmus=None, cantus_firmus_voice_index=None):
        # Use the arguments to generate a numpy matrix.
        # Rows are voices, columns are time steps
        # Cantus firmus, if supplied, should be inserted into one row
        self.species_and_voices = species_and_voices

        if cantus_firmus is not None:
            self.n_time_steps = len(cantus_firmus.notes) * species_and_voices.steps_per_bar
            self.notes = np.empty([species_and_voices.n_voices, self.n_time_steps], np.int8)
            self.notes[cantus_firmus_voice_index, :] = cantus_firmus.note_numbers
            self.cantus_firmus = cantus_firmus
            self.cantus_firmus_voice_index = cantus_firmus_voice_index
        else:
            raise NotImplemented

    def insert_voice(self, voice_index, voice):
        if voice_index == self.cantus_firmus_voice_index:
            raise IndexError("Can't overwrite Cantus Firmus")
        self.notes[voice_index, :] = voice.note_numbers

    def validate(self):
        """
        Apply all rules in the species.

        Should return a 2D array of some kind of collected results.
        Probably a class that has all rules and whether they were passed or not.
        __bool__ method returns True iff all tests passed
        """

        result = ArrangementResult(self)
        voices = tuple(range(self.species_and_voices.n_voices))

        for (description, rule), time_step in itertools.product(
            self.species_and_voices.rules.items(),
            range(self.n_time_steps),
        ):
            if rule.n_voices is None:
                # TODO: what does n_voices == None actually mean?
                result[time_step].push(description, rule, voices, rule(self, voices, time_step))
                raise Exception('I am not sure what n_voices == None means. When is it appropriate?')

            for n_voices in list(range(1, self.species_and_voices.n_voices + 1)):
                for voices in itertools.combinations(voices, n_voices):
                    if rule.n_voices == n_voices:
                        result[time_step].push(description, rule, voices, rule(self, voices, time_step))

        return result

    def __repr__(self):
        return str(self.notes)


class Mode:
    pass


class Pitch:
    """
    Make use of `NOTE_LOOKUP` in constants.py
    """


class TimeUnit:
    BAR = 'BAR'
    MINIM = 'MINIM'
    CROTCHET = 'CROTCHET'
    QUAVER = 'QUAVER'


class Voice:
    # TODO: Maybe be don't actually need this class?
    # there should be an Arrangement that wraps a numpy matrix.
    # then a Voice just needs a reference to the arrangement and a row number
    # A lot of the logic could then be handled by matrix algebra, including finding errors
    # Counterpoint could be generated by stepping through an arrangement, branching through all possibilities, and dropping those that hit a dead end
    pass


class Interval:
    pass


class HarmonicInterval(Interval):
    pass


class MelodicInterval(Interval):
    pass


# TODO: this isn't a primitive, it's a description of what's going on in two voices
class Motion:
    DIRECT = 'DIRECT'
    OBLIQUE = 'OBLIQUE'
    CONTRARY = 'CONTRARY'


class Tie:
    pass


class Note:
    NOTE_NUMBERS = range(128)
    OCTAVES = range(-1, 10)
    NOTE_NAMES = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

    def __init__(self, note_name=None, octave=None, note_number=None):
        assert any([
            note_name is None and octave is None and note_number in constants.NOTE_NUMBERS,
            note_name in constants.NOTE_NAMES and octave in constants.OCTAVES and note_number is None,
        ]), "Invalid arguments - require (name AND octave) XOR (number)"

        if note_number is not None:
            self.note_number = note_number
        else:
            self.note_number = constants.get_note_number(note_name, octave)
