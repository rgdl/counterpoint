import abc
from typing import Tuple

from src.primitives import Arrangement


class Rule(abc.ABC):
    """
    Represent whether a harmony has a given property (e.g. is_consonant, is_direct_motion)

    Atomic Rules can be composed to create more complex rules

    Initialised from a function, which contains the actual logic

    A rule often applies to a specific number of voices (e.g. things about intervals for 2 voices)
    If not (e.g. FirstHarmony), leave `n_voices` == None
    """
    n_voices = None

    @abc.abstractmethod
    def logic(self, arrangement: Arrangement, voices: Tuple[int], time_step: int):
        raise NotImplementedError

    def __call__(self, arrangement: Arrangement, voices: Tuple[int], time_step: int) -> bool:
        """
        This method enforces that the `logic` function behaves as expected and is being given correct inputs
        """

        assert hasattr(self, 'n_voices'), 'A rule must know how many voices there are'
        try:
            assert getattr(self, 'n_voices') is None or getattr(self, 'n_voices') == len(voices), f'Wrong number of voices provided: {self.n_voices} != {len(voices)}'
        except Exception:
            print('here')
        assert arrangement.__class__.__name__ == 'Arrangement', f'`arrangement` should be class Arrangement, instead it\'s: {type(arrangement)}'
        assert isinstance(voices, tuple), '`voices` should be a tuple'
        assert all([isinstance(v, int) for v in voices]), '`voices` should be a tuple of integers'
        assert isinstance(time_step, int), '`time_step` should be an integer'

        result = self.logic(arrangement=arrangement, voices=voices, time_step=time_step)
        try:
            assert isinstance(result, bool), 'The result of applying a rule should be a boolean'
        except Exception:
            print('here')

        return result

    def _combine_n_voices(self, other):
        if self.n_voices is None and other.n_voices is None:
            return None
        if self.n_voices is not None and other.n_voices is not None:
            assert self.n_voices == other.n_voices, 'Rules with incompatible numbers of voices can\'t be combined'
            return self.n_voices
        if self.n_voices is not None:
            return self.n_voices
        return other.n_voices

    def __or__(self, other):
        original = self

        class NewRule(Rule):
            n_voices = original._combine_n_voices(other)

            def logic(self, *args, **kwargs):
                return original(*args, **kwargs) or other(*args, **kwargs)

        return NewRule()

    def __and__(self, other):
        original = self

        class NewRule(Rule):
            n_voices = original._combine_n_voices(other)

            def logic(self, *args, **kwargs):
                return original(*args, **kwargs) and other(*args, **kwargs)

        return NewRule()

    def __xor__(self, other):
        original = self

        class NewRule(Rule):
            n_voices = original._combine_n_voices(other)

            def logic(self, *args, **kwargs):
                return original(*args, **kwargs) != other(*args, **kwargs)

        return NewRule()

    def __invert__(self):
        original = self

        class NewRule(Rule):
            n_voices = original.n_voices

            def logic(self, *args, **kwargs):
                return not original(*args, **kwargs)

        return NewRule()


if __name__ == '__main__':
    print('here')
