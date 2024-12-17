from datetime import datetime
from typing import Optional

class Trade:
    def __init__(self, direction: str, open_time: datetime, open_price: float, size: float = 1.0):
        self.direction = direction          # "long" or "short"
        self.open_time = open_time
        self.open_price = open_price
        self.size = size
        self.close_time: Optional[datetime] = None
        self.close_price: Optional[float] = None
        self.realized_pnl: Optional[float] = None
        self.commissions: float = 0.0

    def close_trade(self, close_time: datetime, close_price: float) -> None:
        self.close_time = close_time
        self.close_price = close_price

        # Calculate realized PnL accounting for direction
        if self.direction == "long":
            self.realized_pnl = (self.close_price - self.open_price) * self.size 

        elif self.direction == "short":
            self.realized_pnl = (self.open_price - self.close_price) * self.size 
