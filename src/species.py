"""
Might be able to do some kind of multiple inheritance trickery here later
For now, keep it simple
"""
import abc

from src.rules import Rule

# TODO get rid of magic numbers? e.g. consts for intervals?


# Harmonic Intervals


class _BaseIntervalRule(Rule):
    """
    N.B.: doesn't distinguish unisons from octaves
    """
    def get_relevant_intervals(self):
        raise NotImplementedError

    def logic(self, arrangement, voices, time_step):
        assert len(voices) == 2
        lower_note = arrangement.notes[voices, time_step].min()
        upper_note = arrangement.notes[voices, time_step].max()

        return (upper_note - lower_note) % 12 in self.get_relevant_intervals()


class ImperfectConsonance(_BaseIntervalRule):
    def get_relevant_intervals(self):
        return 3, 4, 8, 9


class PerfectInterval(_BaseIntervalRule):
    def get_relevant_intervals(self):
        return 0, 7


class SpecificInterval(_BaseIntervalRule):
    def __init__(self, interval_of_interest):
        self._interval_of_interest = interval_of_interest

    def get_relevant_intervals(self):
        return self._interval_of_interest


class Unison(Rule):
    """
    Specific check, because usual treatment doesn't distinguish it from an octave
    """
    def logic(self, arrangement, voices, time_step):
        assert len(voices) == 2
        return arrangement.notes[voices[0], time_step] == arrangement.notes[voices[1], time_step]


class Octave(Rule):
    """
    Specific check, because usual treatment doesn't distinguish it from a unison
    """
    def logic(self, arrangement, voices, time_step):
        assert len(voices) == 2
        lower_note = arrangement.notes[voices, time_step].min()
        upper_note = arrangement.notes[voices, time_step].max()
        return (upper_note > lower_note) and ((upper_note - lower_note) % 12) == 0


class DissonantInterval(_BaseIntervalRule):
    def __init__(self, perfect_fourths_dissonant=True, tritones_dissonant=True):
        self._dissonant_intervals = [1, 2, 10, 11]
        if perfect_fourths_dissonant:
            self._dissonant_intervals.append(5)
        if tritones_dissonant:
            self._dissonant_intervals.append(6)

    def get_relevant_intervals(self):
        return self._dissonant_intervals


# Movement types


class _BaseMotionRule(Rule):
    @abc.abstractmethod
    def check_motion_product(self, product):
        raise NotImplemented

    def logic(self, arrangement, voices, time_step):
        assert len(voices) == 2
        assert time_step > 0

        first_voice_motion = arrangement.notes[voices[0], time_step] - arrangement.notes[voices[0], time_step - 1]
        second_voice_motion = arrangement.notes[voices[1], time_step] - arrangement.notes[voices[1], time_step - 1]

        return self.compare_motion(first_voice_motion, second_voice_motion)


class DirectMotion(_BaseMotionRule):
    def compare_motion(self, first_voice_motion, second_voice_motion):
        return first_voice_motion * second_voice_motion > 0


class ObliqueMotion(_BaseMotionRule):
    def compare_motion(self, first_voice_motion, second_voice_motion):
        return first_voice_motion * second_voice_motion == 0


class ContraryMotion(_BaseMotionRule):
    def compare_motion(self, first_voice_motion, second_voice_motion):
        return first_voice_motion * second_voice_motion < 0


class InwardMotion(_BaseMotionRule):
    def compare_motion(self, first_voice_motion, second_voice_motion):
        return first_voice_motion * second_voice_motion < 0


class NoteRepeated(Rule):
    def __init__(self, times_used):
        self.times_used = times_used

    def logic(self, arrangement, voices, time_step):
        # TODO: might need child class for Rule that say whether they apply to single voices, pairs of voices, etc.
        assert len(voices) == 1
        voice = voices[0]

        if time_step < self.times_used - 1:
            return False
        # TODO: this should have a unit test, because the number of steps calculation would be easy to get wrong
        return arrangement.notes[voice, (time_step - self.times_used):time_step]

# When in the arrangement?


class FirstHarmony(Rule):
    def logic(self, arrangement, voices, time_step):
        return time_step == 0


class LastHarmony(Rule):
    def logic(self, arrangement, voices, time_step):
        return time_step == arrangement.time_steps - 1


class SecondLastHarmony(Rule):
    def logic(self, arrangement, voices, time_step):
        return time_step == arrangement.time_steps - 2


# Specifics about arrangement

class CantusFirmusInLowerVoice(Rule):
    def logic(self, arrangement, voices, time_step):
        return arrangement.cantus_firmus_voice_index == 0


# Start defining rules per species
class FirstSpeciesTwoVoices:
    rules = {
        'No direct motion to a perfect interval': ~(DirectMotion() & PerfectInterval()),
        'No dissonance at all': ~DissonantInterval(),
        'Begin with octave, or 5th IF c.f. is in lower voice': ~FirstHarmony() | (
            Octave() | (SpecificInterval(7) & CantusFirmusInLowerVoice())
        ),
        'End with octave': ~LastHarmony() | Octave(),
        'If C.F. below, 2nd last bar should be major 6th': ~CantusFirmusInLowerVoice() | (SecondLastHarmony() & SpecificInterval(9)),
        'If C.F. above, 2nd last bar should be minor 3rd': CantusFirmusInLowerVoice() | (SecondLastHarmony() & SpecificInterval(3)),
        'Unison only acceptable in final bar': ~Unison() | LastHarmony(),
        'Don\'t use the same note more that 2 times in a row': ~NoteRepeated(times_used=3),
    }

    # Things that don't mark it as a failure, but should be avoided if possible
    preferences = {
        # TODO: Implement "Avoid octava Battuta"
        'Prefer contrary and oblique motion': ContraryMotion() | ObliqueMotion(),
        'Prefer imperfect consonances': ImperfectConsonance(),
    }


if __name__ == '__main__':
    # TODO: Read back over all of my notes when writing later species. The book doesn't present all rules in order
    # TODO: implement "sharps lead up, flats lead down", and how to implement sharps/flats generally? I guess there are acceptable alterations that can be made for a given mode, if it makes it possible to satisfy rules and maybe also preferences? There could be an option for that

    # TODO: unittest for Octava Battuta. Good test of rule composition
    pass
