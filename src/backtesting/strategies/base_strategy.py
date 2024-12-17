from enum import Enum
from abc import ABC, abstractmethod


class Strategy(ABC):
    """Base class for all strategies."""
    @abstractmethod
    def update_price(self, future_price: float) -> None:
        pass

    @abstractmethod
    def generate_signal(self) -> str:
        """
        Return "buy", "sell", or "hold"
        """
        pass