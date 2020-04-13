import abc
from typing import Tuple

from src.primitives import Arrangement


class Rule(abc.ABC):
    """
    Represent whether a harmony has a given property (e.g. is_consonant, is_direct_motion)

    Atomic Rules can be composed to create more complex rules

    Initialised from a function, which contains the actual logic
    """

    @abc.abstractmethod
    def logic(self, arrangement: Arrangement, voices: Tuple[int], time_step: int):
        raise NotImplemented

    def __call__(self, arrangement: Arrangement, voices: Tuple[int], time_step: int) -> bool:
        """
        This method enforces that the `logic` function behaves as expected and is being given correct inputs
        """
        assert all([
            isinstance(arrangement, Arrangement),
            isinstance(voices, tuple),
            all([isinstance(v, int) for v in voices]),
            isinstance(time_step, int),
        ])
        result = self.logic(arrangement=arrangement, voices=voices, time_step=time_step)
        assert isinstance(result, bool)
        return result

    def __or__(self, other):
        class NewRule(Rule):
            def logic(self, *args, **kwargs):
                return self(*args, **kwargs) or other(*args, **kwargs)

        return NewRule

    def __and__(self, other):
        class NewRule(Rule):
            def logic(self, *args, **kwargs):
                return self(*args, **kwargs) and other(*args, **kwargs)

        return NewRule

    def __xor__(self, other):
        class NewRule(Rule):
            def logic(self, *args, **kwargs):
                return self(*args, **kwargs) != other(*args, **kwargs)

        return NewRule

    def __invert__(self):
        class NewRule(Rule):
            def logic(self, *args, **kwargs):
                return not self(*args, **kwargs)

        return NewRule


if __name__ == '__main__':
    print('here')