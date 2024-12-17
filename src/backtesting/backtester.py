from datetime import timedelta
from typing import Dict
import pandas as pd
from .strategies import Strategy
from .portfolio import Portfolio



class Backtester:
    """Simple backtester that goes over the data in incremental time
    steps. The size of the time steps depend on the granularity of the
    data. When working with 1-minute interval data, each time step is
    taken 1 minute into the future.
    """
    def __init__(self, strategy: Strategy, initial_cash: float = 100000.0) -> None:
        self._strategy: Strategy = strategy
        self._portfolio: Portfolio  = Portfolio(initial_cash=initial_cash)
        self._index_data = None
        self._future_data = None
        self._times = None
        self._current_index = -1
        self._current_time = None
        self._current_index_price = None
        self._current_future_price = None
        self._close_schedule: Dict[pd.Timestamp, bool] = {}
        # For daily summaries and live trade tracking
        self._current_day = None
        # Dictionary to track daily PnL, trades, etc.
        # daily_stats[date_str] = {"trades": [], "daily_pnl": float}
        self.daily_stats = {}


    def load_data(self, index_file: str, future_file: str) -> None:
        """Load the index and future data from CSV and align their time indexes."""
        self._index_data = pd.read_csv(index_file, parse_dates=True, index_col="Datetime")
        self._future_data = pd.read_csv(future_file, parse_dates=True, index_col="Datetime")

        # Ensure both are sorted by datetime index just in case
        self._index_data.sort_index(inplace=True)
        self._future_data.sort_index(inplace=True)

        # Find the intersection of the two time indexes
        common_times = self._index_data.index.intersection(self._future_data.index)

        # Filter both DataFrames to only the common times
        self._index_data = self._index_data.loc[common_times]
        self._future_data = self._future_data.loc[common_times]

        # Extract the combined timeline as a list (for iteration)
        self._times = list(common_times)

        print(f"Data aligned. Common time steps: {len(self._times)}")
        


    def run(self) -> None:
        # Example run method that simply iterates through all times
        while self.next():
            # At each step, we have self._current_time, _current_index_price, _current_future_price
            # Strategy logic check:
            self.check_strategy()
            # Other logic...
        self.print_performance()

    def next(self) -> bool:
        """Continue to the next time step.

        :return: True when there is a new time step, False otherwise
        """
        self._current_index += 1
        if self._current_index >= len(self._times):
            # End of data
            # Print final day's summary if not done yet
            if self._current_day:
                self.print_end_of_day_summary(self._current_day)
            return False
        
        self._current_time = self._times[self._current_index]

        # Fetch the current data row for index and future
        current_index_row = self._index_data.loc[self._current_time]
        current_future_row = self._future_data.loc[self._current_time]

        # Store current prices (e.g., 'Close' price or whichever you use for the strategy)
        self._current_index_price = current_index_row["Close"]
        self._current_future_price = current_future_row["Close"]

        # Update the portfolio's current time to align with the new time step
        self._portfolio.set_current_time(self._current_time)

        # Close any positions that have expired based on the current time
        self.close_expired_positions()
        # Determine current day as a string (e.g. "2024-12-03")
        new_day = self._current_time.date().isoformat()

        if self._current_day is None:
            # First iteration, initialize current_day and daily stats
            self._current_day = new_day
            self.daily_stats[new_day] = {"trades": [], "daily_pnl": 0.0}
        elif self._current_day != new_day:
            # Day has changed, print summary of the old day
            self.print_end_of_day_summary(self._current_day)

            # Start tracking the new day
            self._current_day = new_day
            self.daily_stats[new_day] = {"trades": [], "daily_pnl": 0.0}

        # Return True to signal that there are more time steps to process
        return True

    def check_strategy(self) -> bool:
        """Check if the currently active strategy should take any
        action.

        :return: True if we need to buy or sell a position, False
        otherwise
        """
        # # Update the strategy with the current future price
        # if self._current_future_price is not None:
        #     self._strategy.update_price(self._current_future_price)

        #     # Generate a trading signal from the strategy
        #     signal = self._strategy.generate_signal()

        #     # Use the signal to open/close positions as needed
        #     if signal == "buy":
        #         self.open_position(direction="long", price=self._current_index_price)
        #     elif signal == "sell":
        #         self.open_position(direction="short", price=self._current_index_price)
        #     else:
        #         self.close_expired_positions()
        # Update strategy with current future price
        self._strategy.update_price(self._current_future_price)

        # Get trading signal
        signal = self._strategy.generate_signal()

        # If signal = buy/sell and no open position, open one
        if signal == "buy" and self._portfolio.open_trade is None:
            opened = self.open_position(direction="long", price=self._current_index_price)
            if opened:
                close_time = self._current_time + timedelta(minutes=10)
                self._close_schedule[close_time] = True

        elif signal == "sell" and self._portfolio.open_trade is None:
            opened = self.open_position(direction="short", price=self._current_index_price)
            if opened:
                close_time = self._current_time + timedelta(minutes=10)
                self._close_schedule[close_time] = True
        # If hold or position already open, do nothing special here


    def open_position(self, direction: str, price: float) -> bool:
        """Mock placing an OPENING order that trades yielding a new
        position.
        """
        opened = self._portfolio.open_position(direction, price)
        if opened and self._portfolio.open_trade:
            trade = self._portfolio.open_trade
            # Print trade details as it's opened
            print(f"[{trade.open_time}] OPEN {trade.direction.upper()} at {trade.open_price:.2f}, Commission: {trade.commissions:.2f}, Cash: {self._portfolio.cash:.2f}")
            # Record this trade in daily stats
            self.daily_stats[self._current_day]["trades"].append({
                "direction": trade.direction,
                "open_time": trade.open_time,
                "open_price": trade.open_price,
                "type": "open"
            })
        return opened

    def close_position(self) -> None:
        """Mock placing a CLOSING order that trades to close an existing
        position.
        """
        if self._portfolio.open_trade:
            open_trade = self._portfolio.open_trade
            self._portfolio.close_position(price=self._current_index_price)
            closed_trade = self._portfolio.completed_trades[-1]
            # Print trade details as it's closed
            print(f"[{closed_trade.close_time}] CLOSE {closed_trade.direction.upper()} at {closed_trade.close_price:.2f}, PnL: {closed_trade.realized_pnl:.2f}, Cash: {self._portfolio.cash:.2f}")
            # Record the closing trade in daily stats
            self.daily_stats[self._current_day]["trades"].append({
                "direction": closed_trade.direction,
                "open_time": closed_trade.open_time,
                "open_price": closed_trade.open_price,
                "close_time": closed_trade.close_time,
                "close_price": closed_trade.close_price,
                "realized_pnl": closed_trade.realized_pnl,
                "type": "close"
            })
            # Update daily PnL
            self.daily_stats[self._current_day]["daily_pnl"] += closed_trade.realized_pnl


    def close_expired_positions(self) -> None:
        # If current_time in close_schedule and True, close position
        if self._current_time in self._close_schedule and self._close_schedule[self._current_time]:
            self.close_position()
            self._close_schedule[self._current_time] = False


    def print_end_of_day_summary(self, day_str: str) -> None:
        """Print summary of the given day if data exists."""
        if day_str in self.daily_stats:
            day_data = self.daily_stats[day_str]
            trades = day_data["trades"]
            daily_pnl = day_data["daily_pnl"]
            num_trades = sum(1 for t in trades if t["type"] == "close")
            print(f"=== End of day {day_str} Summary ===")
            print(f"Trades closed this day: {num_trades}")
            print(f"Daily PnL: {daily_pnl:.2f}")
            print("Details:")
            for t in trades:
                if t["type"] == "close":
                    print(f" - {t['direction'].upper()} from {t['open_time']} at {t['open_price']:.2f}, closed {t['close_time']} at {t['close_price']:.2f}, PnL: {t['realized_pnl']:.2f}")       
   
    def print_performance(self) -> None:
        """Print the realized performance to the console.

        Details to include:
        - Executed trades
        - Winners (positions making money)
        - Losers (positions losing money)
        - Geometric Profit/Loss (PnL)
        - Sharpe Ratio
        """
        completed_trades = self._portfolio.completed_trades
        if not completed_trades:
            print("No trades executed.")
            return

        pnls = [t.realized_pnl for t in completed_trades if t.realized_pnl is not None]
        winners = sum(1 for p in pnls if p > 0)
        losers = sum(1 for p in pnls if p < 0)
        avg_pnl = sum(pnls)/len(pnls) if pnls else 0.0

        # Geometric mean of returns per trade:
        initial_capital = 100000.0
        returns = [(1 + (p/initial_capital)) for p in pnls]
        # Compute geometric mean
        # geom_mean = (product of returns)^(1/N) - 1
        N=len(returns)
        if N > 0:
            product_of_returns = 1.0
            for r in returns:
                product_of_returns *= r
            geom_mean = product_of_returns**(1/N) - 1
        else:
            geom_mean = 0.0
        # Sharpe ratio
        # mean_ret = sum((p/initial_capital) for p in pnls)/len(pnls) if pnls else 0.0
        # var_ret = sum((p/initial_capital - mean_ret)**2 for p in pnls)/(len(pnls)-1) if len(pnls) > 1 else 0
        # std_ret = var_ret**0.5
        # sharpe = mean_ret/std_ret if std_ret > 0 else 0.0
        if N > 0:
            trade_returns = [p/initial_capital for p in pnls]
            mean_ret = sum(trade_returns)/N
        else:
            mean_ret = 0.0

        if N > 1:
            var = sum((r - mean_ret)**2 for r in trade_returns)/(N-1)
            std_ret = var**0.5
        else:
            std_ret = 0.0

        sharpe = mean_ret/std_ret if std_ret > 0 else 0.0


        final_equity = self._portfolio.total_equity(current_price=self._current_index_price)

        print("=== Performance Summary ===")
        print(f"Number of Trades: {len(pnls)}")
        print(f"Winners: {winners}")
        print(f"Losers: {losers}")
        print(f"Average PnL: {avg_pnl:.2f}")
        print(f"Geometric Mean PnL per Trade: {geom_mean:.2e}")
        print(f"Sharpe Ratio: {sharpe:.4f}")
        print(f"Final Portfolio Value: {final_equity:.2f}")
