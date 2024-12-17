from datetime import datetime
from typing import Optional, List
from .trade import Trade

class Portfolio:
    def __init__(self, initial_cash: float = 100000.0):
        self.cash: float = initial_cash
        self.open_trade: Optional[Trade] = None
        self.completed_trades: List[Trade] = []
        self._current_time: Optional[datetime] = None

    def set_current_time(self, current_time: datetime):
        self._current_time = current_time

    def open_position(self, direction: str, price: float, commission: float = 2.0) -> bool:
        if self.open_trade is not None:
            # Already have an open trade
            return False

        # Create a new Trade instance
        new_trade = Trade(direction=direction, open_time=self._current_time, open_price=price)

        # Deduct commission immediately from portfolio cash
        self.cash -= commission
        # Record this commission in the trade
        new_trade.commissions += commission
        # Margin if short
        if direction == "short":
            margin_required = 0.5 * price * new_trade.size
            self.cash -= margin_required

        self.open_trade = new_trade
        return True


    def close_position(self, price: float, commission: float = 2.0) -> None:
        if self.open_trade is None:
            return

        # Deduct commission for closing
        self.cash -= commission
        self.open_trade.commissions += commission
        # Close the trade and calculate realized PnL
        self.open_trade.close_trade(close_time=self._current_time, close_price=price)

        # Return margin for short trades
        if self.open_trade.direction == "short":
            margin_return = 0.5 * self.open_trade.open_price * self.open_trade.size
            self.cash += margin_return

        # Add net realized PnL to cash (already includes commissions)
        self.cash += self.open_trade.realized_pnl

        # Move trade to completed trades
        self.completed_trades.append(self.open_trade)
        self.open_trade = None

    def get_unrealized_pnl(self, current_price: float) -> float:
        if self.open_trade is None:
            return 0.0
        if self.open_trade.direction == "long":
            return (current_price - self.open_trade.open_price)*self.open_trade.size
        else:
            return (self.open_trade.open_price - current_price)*self.open_trade.size

    def total_equity(self, current_price: float) -> float:
        return self.cash + self.get_unrealized_pnl(current_price=current_price)
