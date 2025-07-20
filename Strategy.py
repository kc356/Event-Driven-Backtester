from abc import ABCMeta, abstractmethod
from typing import Any


class Strategy(object):
    """
    Strategy is an abstract base class providing an interface for
    all subsequent (inherited) strategy handling objects. This will allow to
    implement several strategies, that can be ran simultaneously on the portfolio
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate_signals(self, event: Any) -> None:
        """
        Provides the mechanisms to calculate the list of signals.
        """
        raise NotImplementedError("Should implement calculate_signals()")
