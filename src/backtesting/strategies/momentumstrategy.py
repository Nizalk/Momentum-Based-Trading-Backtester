from collections import deque
from .base_strategy import Strategy

class MomentumStrategy(Strategy):
    def __init__(self, threshold: float = 0.0005):
        # Deque will hold the last 10 prices
        self._prices = deque(maxlen=10)
        self._threshold = threshold
        self._last_signal = "hold"

    def update_price(self, future_price: float) -> None:
        self._prices.append(future_price)

    def can_compute_momentum(self) -> bool:
        return len(self._prices) == 10

    def compute_momentum(self) -> float:
        prices_list = list(self._prices)
        prev_window = prices_list[:5]
        current_window = prices_list[5:]
        X_n = sum(current_window) / 5.0
        X_n_1 = sum(prev_window) / 5.0
        momentum = (X_n - X_n_1) / X_n
        return momentum

    def generate_signal(self) -> str:
        """
        If momentum > threshold => "buy"
        If momentum < -threshold => "sell"
        Otherwise => "hold"
        """
        if not self.can_compute_momentum():
            return "hold"
        
        momentum = self.compute_momentum()

        if momentum > self._threshold:
            return "buy"
        
        elif momentum < -self._threshold:
            return "sell"
        
        else:
            return "hold"
